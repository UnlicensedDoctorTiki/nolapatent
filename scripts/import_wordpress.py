"""One-time public WordPress export; cached sources make normal builds offline."""
import json, re, urllib.request, urllib.parse, hashlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from lxml import html

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
ASSETS = ROOT / 'assets'
SOURCE.mkdir(exist_ok=True)
(ASSETS / 'archive').mkdir(exist_ok=True)

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'NolaPatent static migration/1.0'})
    with urllib.request.urlopen(req, timeout=50) as response:
        return response.read(), dict(response.headers)

def api(kind):
    output = []
    page = 1
    while True:
        data, headers = fetch(f'https://www.nolapatent.com/wp-json/wp/v2/{kind}?per_page=100&page={page}')
        output += json.loads(data)
        if page >= int(headers.get('X-WP-TotalPages', headers.get('x-wp-totalpages', '1'))):
            break
        page += 1
    (SOURCE / f'{kind}-api.json').write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'{kind}: {len(output)}', flush=True)
    return output

posts = api('posts')
pages = api('pages')
categories = api('categories')
media = api('media')
urls = {'https://www.keanmiller.com/wp-content/uploads/2025/10/Miller-Matthew.png'}
for post in posts + pages:
    tree = html.fragment_fromstring(post['content']['rendered'], create_parent=True)
    for el in tree.xpath('//*[@src or @href]'):
        value = el.get('src') or el.get('href') or ''
        if 'nolapatent.com/wp-content/uploads/' in value or (el.tag == 'img' and value.startswith('http')):
            urls.add(value.replace('http:', 'https:'))
for item in media:
    if item.get('post') == 165:
        urls.add(item['source_url'].replace('http:', 'https:'))

# NextGEN galleries were rendered by a plugin, outside the WordPress REST body.
try:
    data, _ = fetch('https://www.nolapatent.com/southern-food-beverage-museum-open/')
    (SOURCE / 'gallery-original.html').write_bytes(data)
    tree = html.fromstring(data)
    for el in tree.xpath('//img[@src] | //a[@href]'):
        value = el.get('src') or el.get('href')
        if '/wp-content/gallery/' in value:
            urls.add(value.replace('http:', 'https:'))
except Exception as error:
    print(f'Gallery source: {error}', flush=True)

manifest = {}
errors = []
def download(url):
    ext = Path(urllib.parse.urlsplit(url).path).suffix.lower() or '.bin'
    name = 'matt-miller.png' if 'Miller-Matthew.png' in url else f'archive/{hashlib.sha256(url.encode()).hexdigest()[:12]}{ext}'
    path = ASSETS / name
    try:
        if not path.exists():
            data, _ = fetch(url)
            path.write_bytes(data)
        return url, 'assets/' + name, None
    except Exception as error:
        return url, None, str(error)
with ThreadPoolExecutor(max_workers=8) as executor:
    for url, local, error in executor.map(download, sorted(urls)):
        if error:
            errors.append({'url': url, 'error': error})
        else:
            manifest[url] = local
(SOURCE / 'assets.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
(SOURCE / 'download-errors.json').write_text(json.dumps(errors, indent=2), encoding='utf-8')
print(f'Assets downloaded: {len(manifest)}; failures: {len(errors)}', flush=True)
