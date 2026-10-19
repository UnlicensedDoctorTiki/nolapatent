"""Check generated pages, local links, metadata, structured data, and archive coverage."""
import json, re
from pathlib import Path
from urllib.parse import urlsplit, unquote
from lxml import html
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
errors=[]
pages=list(DIST.rglob('*.html'))
titles={}
notes=[]
for path in pages:
    raw=path.read_text(encoding='utf-8')
    doc=html.fromstring(raw)
    def require(test,message):
        if not test: errors.append(f'{path.relative_to(DIST)}: {message}')
    require(len(doc.xpath('//h1'))==1,'Expected one h1')
    require(len(doc.xpath('//main'))==1,'Expected one main landmark')
    require(bool(doc.xpath('//meta[@name="description"]/@content')),'Missing description')
    require(bool(doc.xpath('//link[@rel="canonical"]/@href')),'Missing canonical')
    require(not re.search(r'carver|twitter\.com|t\.co/|\[nggallery|wp-json|wp-admin|wp-login\.php',raw,re.I),'Obsolete firm/social/plugin reference')
    title=doc.xpath('string(//title)')
    if path.name!='404.html' and '404' not in path.parts:
        require(title not in titles,'Duplicate title')
        titles[title]=str(path)
    for script in doc.xpath('//script[@type="application/ld+json"]/text()'):
        try: json.loads(script)
        except Exception as exc: errors.append(f'{path}: Invalid JSON-LD: {exc}')
    for element in doc.xpath('//*[@href or @src]'):
        attr='href' if 'href' in element.attrib else 'src'
        value=element.get(attr)
        url=urlsplit(value)
        if url.scheme or url.netloc:continue
        target=(DIST/unquote(url.path).lstrip('/')) if url.path.startswith('/') else path.parent/unquote(url.path)
        target=target.resolve()
        if not url.path:target=path
        if target.is_dir():target=target/'index.html'
        require(target.exists(),f'Broken local {attr}: {value}')
        if url.fragment and target.exists() and target.suffix=='.html':
            linked=html.fromstring(target.read_text(encoding='utf-8'))
            require(bool(linked.xpath('//*[@id=$id or @name=$id]',id=unquote(url.fragment))),f'Missing fragment: {value}')
    for image in doc.xpath('//img'):
        require('alt' in image.attrib,'Image missing alt')
        require(bool(image.get('width') and image.get('height')),'Image lacks dimensions')
posts=json.loads((ROOT/'content/posts.json').read_text(encoding='utf-8'))
require(len({p['author_note'] for p in posts})==len(posts),'Author notes must be unique')
for post in posts:
    require((DIST/post.get('route',post['slug']+'/')/'index.html').exists(),f'Missing post: {post["slug"]}')
for path in ['sitemap.xml','feed.xml']:
    from lxml import etree
    etree.parse(str(DIST/path))
from check_structured_data import validate_site
schema_errors, _ = validate_site(ROOT)
errors.extend(schema_errors)
if errors:
    print('\n'.join(errors))
    raise SystemExit(f'{len(errors)} checks failed')
print(f'PASS: {len(pages)} HTML pages; all local links and fragments; unique titles; JSON-LD; RSS/sitemap XML; {len(posts)} preserved posts and unique author notes.')
