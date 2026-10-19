"""Add a reviewed post from JSON, then run build.py to generate the website."""
import argparse, json, re
from datetime import date, datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('file',type=Path,help='JSON file containing metadata and body_html')
args=parser.parse_args()
new=json.loads(args.file.read_text(encoding='utf-8-sig'))
required=['slug','title','date','published','topic','excerpt','author_note','body_html']
missing=[key for key in required if not isinstance(new.get(key),str) or not new[key].strip()]
if missing:raise SystemExit('Missing required fields: '+', '.join(missing))
if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',new['slug']):raise SystemExit('Slug must use lowercase letters, numbers, and hyphens.')
route=new.get('route',new['slug']+'/')
if route not in (new['slug']+'/', 'blog/'+new['slug']+'/'):raise SystemExit('Post route must be the slug followed by /, optionally prefixed with blog/.')
date.fromisoformat(new['date'])
timestamp=datetime.fromisoformat(new['published'].replace('Z','+00:00'))
if timestamp.tzinfo is None:raise SystemExit('Publication timestamp must include a timezone offset or Z.')
if timestamp.date().isoformat()!=new['date']:raise SystemExit('Publication date and timestamp must match.')
if date.fromisoformat(new['date'])>date.today():raise SystemExit('Future posts must remain drafts outside content/posts.json until publication.')
posts_path=ROOT/'content/posts.json'
posts=json.loads(posts_path.read_text(encoding='utf-8'))
if any(p['slug']==new['slug'] or p.get('route',p['slug']+'/')==route for p in posts) or (ROOT/'dist'/route).exists():raise SystemExit('Slug or route already exists; choose a unique slug.')
if any(p['author_note']==new['author_note'] for p in posts):raise SystemExit('Write a unique, relevant author note for this article.')
if re.search(r'<\s*(script|iframe|style)|\son\w+\s*=|javascript:|carver|twitter\.com',new['body_html'],re.I):raise SystemExit('Use plain semantic article HTML without scripts, event handlers, obsolete firm references, or Twitter links.')
body=new.pop('body_html')
new.setdefault('archived',False)
new.setdefault('categories',[])
new.setdefault('id','post-'+new['slug'])
(ROOT/'content/posts'/f'{new["slug"]}.html').write_text(body,encoding='utf-8')
posts.append(new)
posts_path.write_text(json.dumps(posts,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Added {new["title"]}. Run scripts/build.py to rebuild all static pages.')
