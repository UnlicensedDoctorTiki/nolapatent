"""Validate delivered JSON-LD against a pinned official Schema.org vocabulary."""
import argparse
from collections import Counter
from datetime import date, datetime
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
VOCABULARY = ROOT / 'source/schemaorg/schemaorg-current-https.jsonld'


def sequence(value):
    return value if isinstance(value, list) else [value]


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


class Vocabulary:
    def __init__(self, path):
        graph = json.loads(path.read_text(encoding='utf-8'))['@graph']
        self.terms = {n['@id'][7:]: n for n in graph if n.get('@id', '').startswith('schema:')}

    def ancestors(self, name):
        found, pending = set(), [name]
        while pending:
            name = pending.pop()
            if name in found:
                continue
            found.add(name)
            for parent in sequence(self.terms.get(name, {}).get('rdfs:subClassOf', [])):
                if parent['@id'].startswith('schema:'):
                    pending.append(parent['@id'][7:])
        return found

    def includes(self, term, key):
        return {n['@id'][7:] for n in sequence(self.terms[term].get(key, []))}

    def is_class(self, name):
        return 'rdfs:Class' in sequence(self.terms.get(name, {}).get('@type', []))

    def value_matches(self, value, ranges, definitions):
        if isinstance(value, dict):
            resolved = definitions.get(value.get('@id'), value)
            return any(self.ancestors(t) & ranges for t in sequence(resolved.get('@type', [])))
        if isinstance(value, bool):
            return 'Boolean' in ranges
        if isinstance(value, int):
            return bool({'Integer', 'Number'} & ranges)
        if isinstance(value, float):
            return bool({'Float', 'Number'} & ranges)
        if not isinstance(value, str):
            return False
        if 'Text' in ranges:
            return True
        if {'Date', 'DateTime'} & ranges:
            try:
                if 'T' in value:
                    return 'DateTime' in ranges and datetime.fromisoformat(value.replace('Z', '+00:00')) is not None
                return 'Date' in ranges and date.fromisoformat(value) is not None
            except ValueError:
                return False
        if urlsplit(value).scheme in ('https', 'http'):
            # Schema.org permits URL shorthand for entity-valued properties such as item/image.
            return 'URL' in ranges or any('Thing' in self.ancestors(t) for t in ranges)
        return False

    def validate_node(self, node, definitions):
        issues = []
        types = sequence(node.get('@type', []))
        inherited = set().union(*(self.ancestors(t) for t in types)) if types else set()
        for type_name in types:
            if not self.is_class(type_name):
                issues.append(f'Unknown Schema.org type: {type_name}')
        for prop, values in node.items():
            if prop in ('@id', '@type'):
                continue
            if prop.startswith('@') or prop not in self.terms or 'rdf:Property' not in sequence(self.terms[prop].get('@type', [])):
                issues.append(f'Unknown Schema.org property: {prop}')
                continue
            domains = self.includes(prop, 'schema:domainIncludes')
            if domains and not inherited & domains:
                issues.append(f'{prop} is not applicable to {types}')
            ranges = self.includes(prop, 'schema:rangeIncludes')
            for value in sequence(values):
                if ranges and not self.value_matches(value, ranges, definitions):
                    issues.append(f'{prop} has an invalid value type; expected {sorted(ranges)}')
        return issues


def validate_site(root=ROOT, baseline=None):
    profile = json.loads((root / 'content/profile.json').read_text(encoding='utf-8'))
    posts = json.loads((root / 'content/posts.json').read_text(encoding='utf-8'))
    base = profile['base_url'].rstrip('/')
    person_id, firm_id = base + '/#matt-miller', base + '/#kean-miller'
    vocabulary = Vocabulary(root / 'source/schemaorg/schemaorg-current-https.jsonld')
    errors, shared, counts = [], {}, Counter()
    pages = sorted((root / 'dist').rglob('*.html'))

    def require(test, message):
        if not test:
            errors.append(message)

    require(base == 'https://www.nolapatent.com', 'Site entity URLs must use canonical HTTPS/www base')
    for path in pages:
        label = path.relative_to(root).as_posix()
        raw = path.read_text(encoding='utf-8')
        doc = html.fromstring(raw)
        scripts = doc.xpath('//script[@type="application/ld+json"]/text()')
        require(len(scripts) == 1, f'{label}: expected one delivered JSON-LD graph')
        if len(scripts) != 1:
            continue
        try:
            data = json.loads(scripts[0])
        except ValueError as exc:
            errors.append(f'{label}: JSON syntax: {exc}')
            continue
        require(data.get('@context') == 'https://schema.org', f'{label}: unexpected context')
        graph = data.get('@graph')
        if not isinstance(graph, list):
            errors.append(f'{label}: missing @graph array')
            continue
        nodes = [node for node in objects(graph) if '@type' in node or '@id' in node]
        definitions = {}
        for node in nodes:
            if '@id' in node and '@type' in node:
                ident = node['@id']
                require(ident not in definitions, f'{label}: duplicate entity definition {ident}')
                definitions[ident] = node
                serialized = json.dumps(node, sort_keys=True, ensure_ascii=False)
                require(ident not in shared or shared[ident] == serialized,
                        f'{label}: conflicting definition for {ident}')
                shared.setdefault(ident, serialized)
        for node in nodes:
            counts.update(sequence(node.get('@type', [])))
            for issue in vocabulary.validate_node(node, definitions):
                errors.append(f'{label}: {node.get("@id", node.get("@type"))}: {issue}')
            if '@id' in node:
                ident = node['@id']
                require(ident.startswith(base + '/'), f'{label}: noncanonical entity identifier {ident}')
                require(ident in definitions, f'{label}: unresolved entity reference {ident}')
            for value in node.values():
                for literal in sequence(value):
                    if isinstance(literal, str) and literal.startswith(('http:', 'https:')):
                        parsed = urlsplit(literal)
                        if parsed.hostname in ('nolapatent.com', 'www.nolapatent.com'):
                            require(literal.startswith(base + '/'), f'{label}: noncanonical site URL {literal}')
            require(not {'LocalBusiness', 'LegalService'} & set(sequence(node.get('@type', []))),
                    f'{label}: personal site must not be marked as a separate law firm')
            for prop in ('datePublished', 'dateModified'):
                if prop in node:
                    require(node.get('@type') == 'BlogPosting', f'{label}: unsupported {prop} outside post metadata')

        people = [n for n in graph if n.get('@type') == 'Person']
        require(len(people) == 1 and people[0].get('@id') == person_id, f'{label}: inconsistent Person identity')
        if not people:
            continue
        person = people[0]
        require(person.get('name') == profile['name'] and person.get('alternateName') == profile['short_name'],
                f'{label}: Person names disagree with source profile')
        require(person.get('jobTitle') == 'Registered Patent Attorney', f'{label}: incorrect professional title')
        require(profile['job_title'] in person.get('description', '') and
                'Former professional software engineer' in person.get('description', ''),
                f'{label}: current firm role/prior engineering background missing or conflicting')
        require(person.get('worksFor') == {'@id': firm_id}, f'{label}: incorrect employer relationship')
        require(set(person.get('sameAs', [])) == {profile['bio_url'], profile['github_url'], profile['linkedin_url']},
                f'{label}: unverified/missing sameAs profile')
        require(person.get('email') == profile['email'] and person.get('telephone') == profile['telephone'],
                f'{label}: contact details disagree with source profile')
        require({'Software patents', 'Patent prosecution', 'Patent litigation', 'Software licensing',
                 'Intellectual property litigation', 'Trademark law', 'Copyright law'} <= set(person.get('knowsAbout', [])),
                f'{label}: requested knowledge areas missing')
        firm = definitions.get(firm_id, {})
        require(firm.get('name') == profile['firm'] and firm.get('url') == 'https://www.keanmiller.com/',
                f'{label}: incorrect firm entity')
        address = definitions.get(base + '/#office-address', {})
        require(address.get('addressLocality') == profile['city'] and address.get('addressRegion') == profile['region'],
                f'{label}: incorrect work location')
        credential = definitions.get(base + '/#duke-ba', {})
        require(credential.get('name') == 'Duke University, B.A., Computer Science, Psychology',
                f'{label}: incorrect degree (one B.A., two majors)')
        require(credential.get('recognizedBy') == {'@id': base + '/#duke-university'},
                f'{label}: degree is not associated with Duke')

        canonical = doc.xpath('string(//link[@rel="canonical"]/@href)')
        if doc.xpath('//meta[@http-equiv="refresh"]'):
            require(not any('WebPage' in vocabulary.ancestors(n.get('@type', 'Thing')) for n in graph),
                    f'{label}: redirect must not redefine its canonical destination')
            continue
        webpage = definitions.get(canonical + '#webpage', {})
        require(bool(webpage), f'{label}: missing canonical WebPage')
        if not webpage:
            continue
        require('WebPage' in vocabulary.ancestors(webpage.get('@type', 'Thing')), f'{label}: incorrect page type')
        require(webpage.get('url') == canonical, f'{label}: page URL disagrees with canonical')
        require(webpage.get('description') == doc.xpath('string(//meta[@name="description"]/@content)'),
                f'{label}: schema description disagrees with page metadata')
        require({'@id': person_id} in sequence(webpage.get('about', [])), f'{label}: page is not linked to Person')
        require(profile['name'] in doc.text_content() and profile['firm'] in doc.text_content(),
                f'{label}: visible professional identity missing')
        if canonical == base + '/about-me/':
            require(webpage.get('@type') == 'ProfilePage' and webpage.get('mainEntity') == {'@id': person_id},
                    f'{label}: profile does not identify the canonical Person')
            require(credential['name'] in doc.text_content(), f'{label}: education not supported by visible biography')
        if canonical == base + '/practice/software-patents/':
            topics = {definitions[n['@id']].get('name') for n in webpage.get('about', [])}
            require({'Software patents', 'Software patent prosecution', 'Patent eligibility under 35 U.S.C. § 101'} <= topics,
                    f'{label}: software patent subjects missing')

    for post in posts:
        route = post.get('route', post['slug'] + '/')
        url = base + '/' + route
        node = json.loads(shared.get(url + '#article', '{}'))
        require(node.get('@type') == 'BlogPosting', f'{post["slug"]}: missing BlogPosting')
        require(node.get('author') == {'@id': person_id} and node.get('publisher') == {'@id': person_id},
                f'{post["slug"]}: incorrect author/publisher')
        require(node.get('datePublished') == post['published'], f'{post["slug"]}: unsupported publication date')
        require(node.get('dateModified') == post.get('modified'), f'{post["slug"]}: unsupported modification date')
        require(node.get('headline') == post['title'], f'{post["slug"]}: headline disagrees with content metadata')
        doc = html.fromstring((root / 'dist' / route / 'index.html').read_text(encoding='utf-8'))
        require(doc.xpath('string(//h1)') == post['title'], f'{post["slug"]}: headline disagrees with visible heading')
        require(doc.xpath('//time/@datetime')[0] == post['date'], f'{post["slug"]}: visible publication date differs')
        webpage = json.loads(shared.get(url + '#webpage', '{}'))
        require(webpage.get('mainEntity') == {'@id': url + '#article'}, f'{post["slug"]}: post and page are not connected')

    if baseline:
        before = json.loads(Path(baseline).read_text(encoding='utf-8'))
        after = {}
        for path in (root / 'dist').rglob('*'):
            if not path.is_file():
                continue
            content = path.read_bytes()
            if path.suffix == '.html':
                content = re.sub(rb'<script type="application/ld\+json">.*?</script>', b'', content, flags=re.S)
            after[path.relative_to(root / 'dist').as_posix()] = hashlib.sha256(content).hexdigest()
        require(before == after, 'Non-schema deployed content/assets/URLs changed: ' +
                ', '.join(sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))))

    summary = {'html_pages': len(pages), 'blog_posts': len(posts), 'schema_types': dict(sorted(counts.items())),
               'person_id': person_id, 'vocabulary_sha256': hashlib.sha256((root / 'source/schemaorg/schemaorg-current-https.jsonld').read_bytes()).hexdigest(),
               'errors': errors, 'non_schema_baseline_checked': bool(baseline)}
    return errors, summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, help='Optional pre-change non-schema hashes')
    parser.add_argument('--report', type=Path, help='Optional JSON validation report')
    args = parser.parse_args()
    errors, summary = validate_site(baseline=args.baseline)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'PASS: {summary["html_pages"]} delivered JSON-LD graphs; official vocabulary domains/ranges; '
          f'canonical entities/references; {summary["blog_posts"]} article dates/authors; visible identity agreement.' +
          (' Non-schema HTML and assets are byte-for-byte unchanged.' if args.baseline else ''))
