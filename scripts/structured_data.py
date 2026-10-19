"""Shared Schema.org graph builders; no network access or page-content changes."""
from copy import deepcopy


KNOWLEDGE = [
    'Software patents', 'Patent prosecution', 'Patent litigation',
    'Software licensing', 'Intellectual property litigation', 'Trademark law',
    'Copyright law', 'Software engineering', 'Computer science',
    'Software contracts', 'Open-source software', 'Trade secrets',
]

PRACTICE_SUBJECTS = {
    'practice/software-patents/': [
        ('software-patents', 'Software patents'),
        ('software-patent-prosecution', 'Software patent prosecution'),
        ('patent-eligibility', 'Patent eligibility under 35 U.S.C. § 101'),
    ],
    'practice/patents/': [('patents', 'Patents'), ('patent-prosecution', 'Patent prosecution')],
    'practice/trademarks/': [('trademark-law', 'Trademark law')],
    'practice/copyright/': [('copyright-law', 'Copyright law')],
    'practice/technology/': [
        ('software-licensing', 'Software licensing'),
        ('software-contracts', 'Software contracts'),
        ('open-source-software', 'Open-source software'),
    ],
}


def identity_graph(profile):
    """The same Person and supporting entities are emitted on every page."""
    base = profile['base_url'].rstrip('/')
    ref = lambda fragment: {'@id': base + '/#' + fragment}
    person = {
        '@type': 'Person', **ref('matt-miller'),
        'name': profile['name'], 'alternateName': profile['short_name'],
        'url': base + '/about-me/',
        'image': base + '/assets/matt-miller.webp',
        'jobTitle': 'Registered Patent Attorney',
        'description': (
            f'Registered U.S. patent attorney and {profile["job_title"]} at {profile["firm"]} '
            f'in {profile["city"]}, Louisiana. Former professional software engineer '
            'with a Duke University B.A. in Computer Science and Psychology.'
        ),
        'worksFor': ref('kean-miller'),
        'address': ref('office-address'), 'workLocation': ref('new-orleans-office'),
        'email': profile['email'], 'telephone': profile['telephone'],
        'sameAs': [profile['bio_url'], profile['github_url'], profile['linkedin_url']],
        'alumniOf': [ref('duke-university'), ref('tulane-law-school')],
        'hasCredential': ref('duke-ba'), 'knowsAbout': KNOWLEDGE[:],
    }
    return [
        person,
        {'@type': 'Organization', **ref('kean-miller'),
         'name': profile['firm'], 'url': 'https://www.keanmiller.com/'},
        {'@type': 'PostalAddress', **ref('office-address'),
         'streetAddress': profile['street'], 'addressLocality': profile['city'],
         'addressRegion': profile['region'], 'postalCode': profile['postal_code'],
         'addressCountry': 'US'},
        {'@type': 'Place', **ref('new-orleans-office'),
         'name': 'Kean Miller New Orleans office', 'url': profile['office_url'],
         'address': ref('office-address')},
        {'@type': 'CollegeOrUniversity', **ref('duke-university'), 'name': 'Duke University'},
        {'@type': 'CollegeOrUniversity', **ref('tulane-law-school'),
         'name': 'Tulane University Law School'},
        {'@type': 'EducationalOccupationalCredential', **ref('duke-ba'),
         'name': 'Duke University, B.A., Computer Science, Psychology',
         'credentialCategory': 'Bachelor of Arts',
         'recognizedBy': ref('duke-university'),
         'about': [ref('computer-science'), ref('psychology')]},
        {'@type': 'DefinedTerm', **ref('computer-science'), 'name': 'Computer science'},
        {'@type': 'DefinedTerm', **ref('psychology'), 'name': 'Psychology'},
    ]


def page_graph(profile, route, title, description, kind='WebPage', extra=None,
               canonical_route=None):
    base = profile['base_url'].rstrip('/')
    person_ref = {'@id': base + '/#matt-miller'}
    website_ref = {'@id': base + '/#website'}
    graph = identity_graph(profile)
    graph.append({
        '@type': 'WebSite', **website_ref, 'name': 'NOLAPATENT', 'url': base + '/',
        'description': (
            f'The personal professional website of {profile["name"]} '
            f'({profile["short_name"]}), a registered U.S. patent attorney and {profile["job_title"]} '
            f'at {profile["firm"]} in {profile["city"]}, Louisiana.'
        ),
        'publisher': person_ref, 'about': person_ref, 'inLanguage': 'en-US',
    })
    # A redirect must not redefine its destination's WebPage as an "article moved" page.
    if canonical_route is not None:
        return graph

    url = base + '/' + route
    page_ref = {'@id': url + '#webpage'}
    # The containing HTML page and its BlogPosting are distinct, linked entities.
    webpage = {
        '@type': 'WebPage' if kind == 'Article' else kind, **page_ref,
        'url': url, 'name': title, 'description': description,
        'inLanguage': 'en-US', 'isPartOf': website_ref, 'about': [person_ref],
    }
    if route in ('', 'about-me/'):
        webpage['mainEntity'] = person_ref
    graph.append(webpage)

    for slug, label in PRACTICE_SUBJECTS.get(route, []):
        topic = {'@type': 'DefinedTerm', '@id': base + '/#' + slug, 'name': label}
        graph.append(topic)
        webpage['about'].append({'@id': topic['@id']})

    for original in extra or []:
        node = deepcopy(original)
        node_type = node['@type']
        if node_type == 'Service':
            node['@id'] = url + '#service'
            node['provider'] = person_ref
            node['mainEntityOfPage'] = page_ref
            webpage['mainEntity'] = {'@id': node['@id']}
        elif node_type == 'BlogPosting':
            node['url'] = url
            node['author'] = person_ref
            node['publisher'] = person_ref
            node['mainEntityOfPage'] = page_ref
            node['isPartOf'] = website_ref
            webpage['mainEntity'] = {'@id': node['@id']}
        elif node_type == 'ItemList':
            node['@id'] = url + '#items'
            webpage['mainEntity'] = {'@id': node['@id']}
        graph.append(node)

    if route:
        breadcrumb = {
            '@type': 'BreadcrumbList', '@id': url + '#breadcrumb',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': base + '/'},
                {'@type': 'ListItem', 'position': 2, 'name': title, 'item': url},
            ],
        }
        graph.append(breadcrumb)
        webpage['breadcrumb'] = {'@id': breadcrumb['@id']}
    return graph
