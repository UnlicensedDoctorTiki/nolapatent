"""Convert the cached export into editable static-site source (run once)."""
import json, re, html as h
from pathlib import Path
from lxml import html, etree
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
load = lambda name: json.loads((ROOT / 'source' / name).read_text(encoding='utf-8-sig'))
assets = load('assets.json')
categories = {c['id']: c for c in load('categories-api.json')}
posts = load('posts-api.json')
notes = {
514: 'For inventors responding to prior-art rejections, Matt brings the perspective of both a registered patent attorney and a named co-inventor on U.S. patents.',
509: 'Matt helps clients develop patent protection for software, mechanical systems, and energy technologies, bringing technical experience to decisions throughout prosecution.',
504: 'A former software engineer, Matt advises on copyright ownership, registration, and enforcement involving software and other creative works.',
494: 'Matt studied computer science at Duke and worked as a software engineer before law school, a background that informs his writing about emerging technology.',
489: 'Matt combines a computer science background with experience prosecuting patents before the USPTO and litigating patent disputes in federal court and before the PTAB.',
485: 'Matt’s intellectual property practice includes trade secrets as well as patents, trademarks, and copyrights, with a practical understanding of technology businesses.',
468: 'Matt’s work at the intersection of copyright and software includes helping develop the Durationator, a project analyzing copyright terms around the world.',
462: 'Matt counsels creators and businesses on copyright registration and enforcement involving websites, books, software, and advertising materials.',
455: 'A registered patent attorney, Matt works with applicants before the USPTO on inventions ranging from software to mechanical and oil-and-gas technologies.',
445: 'Before practicing law, Matt worked in software engineering; his technical experience includes Linux administration, databases, web applications, and open-source software.',
437: 'Matt’s copyright practice includes registration and enforcement, connecting the steps taken to protect a work with the issues that arise in a dispute.',
424: 'Matt’s trademark experience covers clearance, federal applications, and disputes in federal court and before the Trademark Trial and Appeal Board.',
385: 'Matt brings experience in programming, database development, and web applications to his work on intellectual property and technology issues.',
359: 'With a computer science degree and professional software engineering experience, Matt approaches technology questions with an understanding of the systems behind them.',
339: 'Matt’s background includes Linux server administration and open-source development, alongside his legal work on software, websites, and intellectual property.',
325: 'Matt advises on internet-related intellectual property issues, including domain-name disputes, website copyright compliance, and website policies.',
322: 'As both a registered patent attorney and a named inventor, Matt understands the technical and practical work involved in developing an invention.',
307: 'Matt helped build the Durationator copyright-term analysis engine while at Tulane Law School, bringing a technical perspective to copyright questions.',
293: 'Matt’s technology practice includes advising on website terms of service and privacy policies, informed by his earlier work developing web applications.',
282: 'Matt writes about the overlap between law, culture, and technology, drawing on an intellectual property practice that includes copyright and online issues.',
276: 'Matt helped develop Tulane’s Durationator copyright-analysis software. Professor Elizabeth Townsend Gard’s article about that work was cited in Justice Breyer’s dissent in Golan v. Holder.',
260: 'Matt is a lawyer and former software engineer whose interests extend to the ways people create, develop, and share ideas across different fields.',
223: 'Matt’s patent prosecution experience extends beyond software to mechanical systems, with a technical background that helps him understand how an invention works.',
193: 'Matt handles trademark clearance, federal prosecution, and enforcement, and previously supervised students in Tulane Law School’s Trademark Lab.',
179: 'Matt advises businesses on copyright ownership involving software, websites, and other works, informed by firsthand experience writing code and developing applications.',
171: 'Matt counsels on website copyright compliance and copyright enforcement, bringing a developer’s perspective to the legal issues facing online services.',
165: 'Based in New Orleans, Matt writes about intellectual property, technology, and the creative life of the city where he practices.',
97: 'Matt’s copyright work includes registration and enforcement, and his writing explores the ways copyright disputes intersect with music and popular culture.',
86: 'Matt’s practice spans patents, trademarks, copyrights, and trade secrets, helping clients consider different forms of protection for their ideas, brands, and creative work.',
82: 'Matt developed Louisiana Civil Code and Louisiana Code of Civil Procedure apps for iPhone and iPad, combining his software background with legal practice.',
37: 'Matt advises on internet and technology issues, including website copyright compliance, and has a background in web application development and server administration.',
31: 'Matt helps clients address copyright ownership and registration, including issues involving software, websites, and work created for businesses.',
26: 'Matt assists with trademark clearance, prosecution, and enforcement, and previously taught IP strategy as part of Tulane Law School’s Trademark Lab.'
}
overrides = {514:'Patents',509:'Patents',504:'Copyright',494:'Technology',489:'Artificial intelligence',485:'Business & technology',468:'Artificial intelligence',455:'Patents'}
cat_topics = {9:'Patents',3:'Copyright',2:'Trademarks',18:'Artificial intelligence'}
output=[]
(ROOT/'content/posts').mkdir(parents=True,exist_ok=True)
for p in posts:
    body = html.fragment_fromstring(p['content']['rendered'], create_parent='div')
    for comment in body.xpath('//comment()'):
        comment.getparent().remove(comment)
    for el in list(body.iterdescendants()):
        if el.tag in ('script','style','noscript'):
            el.drop_tree(); continue
        if el.tag == 'iframe':
            link=el.get('src','').replace('http:', 'https:')
            vid=re.search(r'youtube.com/embed/([^?]+)',link)
            a=html.Element('a', href='https://www.youtube.com/watch?v='+vid[1] if vid else link)
            a.text='Watch the referenced video on YouTube' if vid else 'View the referenced media'
            el.getparent().replace(el,a);continue
        if el.tag=='center': el.tag='div';el.set('class','figure-caption')
        for key in list(el.attrib):
            if key not in ('href','src','alt','width','height','colspan','rowspan','id','class'):
                del el.attrib[key]
        if el.tag=='img':
            src=el.get('src','').replace('http:','https:')
            if src in assets: el.set('src',assets[src])
            if src in assets and (not el.get('width') or not el.get('height')):
                with Image.open(ROOT/assets[src]) as image:
                    el.set('width',str(image.width));el.set('height',str(image.height))
            if not el.get('alt'): el.set('alt',h.unescape(p['title']['rendered']).strip('\ufeff'))
            el.set('loading','lazy');el.set('decoding','async')
        if el.tag=='a':
            href=el.get('href','').strip()
            if re.search(r'(twitter\.com|x\.com|t\.co)/',href):
                el.drop_tag();continue
            if 'carverdarden.com' in href: el.set('href','https://www.keanmiller.com/team/j-matthew-miller-iii/')
            if '/wp-content/uploads/' in href and href.replace('http:','https:') in assets:
                el.set('href',assets[href.replace('http:','https:')])
    text=html.tostring(body,encoding='unicode')
    text=text[text.find('>')+1:text.rfind('</div>')]
    text=text.replace('Carver Darden (my employer)','Kean Miller (my firm)').replace('engagement form you','engagement from you')
    text=re.sub(r'\[nggallery[^\]]+\]', '<em>The original photo gallery is no longer available.</em>', text)
    text=re.sub(r'\[/?caption[^\]]*\]','',text)
    for asset,local in assets.items(): text=text.replace(asset,local).replace(asset.replace('https:','http:'),local)
    title=h.unescape(re.sub('<[^>]+>','',p['title']['rendered'])).replace('\ufeff','').strip()
    topic=overrides.get(p['id']) or next((cat_topics[c] for c in p['categories'] if c in cat_topics),'Technology')
    clean=html.fragment_fromstring(text,create_parent=True).text_content()
    excerpt=' '.join(clean.split())[:185].rsplit(' ',1)[0].rstrip('.,:;')+'…'
    item={'id':p['id'],'slug':p['slug'],'title':title,'date':p['date'][:10], 'published':p['date_gmt']+'Z','topic':topic,'excerpt':excerpt,'author_note':notes[p['id']],'source_url':p['link'],'categories':[categories[c]['slug'] for c in p['categories']]}
    item['archived']=True
    (ROOT/'content/posts'/f'{p["slug"]}.html').write_text(text,encoding='utf-8')
    output.append(item)
(ROOT/'content/posts.json').write_text(json.dumps(output,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'content/categories.json').write_text(json.dumps(list(categories.values()),ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Prepared {len(output)} editable articles.')
