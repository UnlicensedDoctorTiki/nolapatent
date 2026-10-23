"""Offline static HTML generator. Python standard library only; no server-side runtime."""
import json, re, shutil, os, math, argparse
from pathlib import Path
from datetime import date
from html import escape, unescape
from urllib.parse import urlsplit, parse_qs
from xml.sax.saxutils import escape as xe
from structured_data import page_graph

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT/'dist'
P = json.loads((ROOT/'content/profile.json').read_text(encoding='utf-8'))
RECOGNITIONS = json.loads((ROOT/'content/recognitions.json').read_text(encoding='utf-8'))
PUBLICATIONS = json.loads((ROOT/'content/publications.json').read_text(encoding='utf-8'))
POSTS = json.loads((ROOT/'content/posts.json').read_text(encoding='utf-8'))
POSTS.sort(key=lambda p:p['date'],reverse=True)
BASE=P['base_url'].rstrip('/')
e=lambda x:escape(str(x),quote=True)
DATE=date.today().isoformat()
GENERATED=[]
PAGES={}
def post_route(p): return p.get('route',p['slug']+'/')

ID_ROUTES={str(p['id']):post_route(p) for p in POSTS}
ID_ROUTES.update({'6':'about-me/','4':'blog/','13':'contact/','40':'disclaimer/','230':'ios/'})

def pathlink(route, target=''):
    """All page and asset links work both over HTTP and by double-clicking HTML."""
    if target.startswith(('http:','https:','mailto:','tel:','#')): return target
    target=target.lstrip('/')
    fragment=''
    if '#' in target: target,fragment=target.split('#',1);fragment='#'+fragment
    query=''
    if '?' in target: target,query=target.split('?',1);query='?'+query
    dest=(target+'index.html') if not target or target.endswith('/') else target
    start=route.rstrip('/') or '.'
    return os.path.relpath(dest,start).replace('\\','/')+query+fragment

def canonical(route): return BASE+'/'+route
def pretty(d): return date.fromisoformat(d[:10]).strftime('%B %d, %Y').replace(' 0',' ')
def stripped(s): return ' '.join(unescape(re.sub('<[^>]+>',' ',s)).split())
def reading(p): return max(1,math.ceil(len(stripped((ROOT/'content/posts'/f'{p["slug"]}.html').read_text(encoding='utf-8')).split())/225))
def link(route,target,label,cls=''): return f'<a href="{e(pathlink(route,target))}"'+(f' class="{cls}"' if cls else '')+f'>{label}</a>'

def header(route):
    nav=''.join(f'<a href="{e(pathlink(route,t))}"'+(' aria-current="page"' if route==t else '')+f'>{label}</a>' for t,label in [('about-me/','About Matt'),('representative-experience/','Experience'),('index.html#practice','Practice'),('blog/','Insights')])
    return f'''<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{pathlink(route,'')}"><span class="brand-symbol" aria-hidden="true">n</span><span><span class="brand-word">NOLA<b>PATENT</b></span><span class="brand-sub">Ideas. Protected.</span></span></a><button class="menu-toggle" aria-controls="navigation" aria-expanded="false" aria-label="Open navigation">Menu <span aria-hidden="true">☰</span></button><nav id="navigation" class="navigation" aria-label="Main navigation">{nav}<a class="nav-contact" href="{pathlink(route,'contact/')}">Let’s talk <span aria-hidden="true">↗</span></a></nav></div></header>'''

def contact(route):
    return f'''<section class="contact-section dark" id="contact" aria-labelledby="contact-heading"><div class="wrap contact-grid"><div><span class="eyebrow">Your next step</span><h2 id="contact-heading">What are you<br>working on?</h2><p>If you need assistance with a patent, trademark, copyright, software agreement, or other intellectual property matter, contact me at Kean Miller to discuss whether I can help.</p><p><small>An inquiry does not create an attorney-client relationship. Please do not send confidential information unless you have already signed paperwork to engage Kean Miller to represent you.</small></p></div><div class="contact-links"><small>Get in touch with Matt Miller</small><a class="contact-phone" href="tel:{P['telephone']}">{P['display_phone']} <span aria-hidden="true">↗</span></a><a class="contact-email" href="mailto:{P['email']}">{P['email']}</a>{link(route,P['bio_url'],'View Matt’s Kean Miller profile <span aria-hidden="true">↗</span>','text-link')}<address>Special Counsel · Kean Miller<br>{P['street']}<br>New Orleans, Louisiana {P['postal_code']}</address></div></div></section>'''

def footer(route):
    return f'''<footer class="site-footer"><div class="wrap"><div class="footer-top"><div><span class="footer-brand">NOLAPATENT</span><br><small class="subtle">Intellectual property. A technical perspective.</small></div><nav aria-label="Footer">{link(route,'about-me/','About Matt')}{link(route,'representative-experience/','Experience')}{link(route,'blog/','Insights')}{link(route,P['linkedin_url'],'LinkedIn')}{link(route,'disclaimer/','Disclaimer')}{link(route,'privacy/','Privacy')}{link(route,'feed.xml','RSS feed')}</nav></div><div class="footer-bottom"><p>This is the personal website of J. Matthew Miller, III, Special Counsel at Kean Miller. Louisiana-licensed lawyer and registered U.S. patent attorney. General information only; not legal advice. No attorney-client relationship is created by visiting or contacting this site.</p><span>© {DATE[:4]} Matt Miller</span></div></div></footer>'''

def page(route,title,description,body,kind='WebPage',extra=None,index=True,with_contact=True,canon=None,title_tag=None,styles=()):
    url=canonical(canon if canon is not None else route)
    graph=page_graph(P,route,title,description,kind,extra,canonical_route=canon)
    meta_title=title_tag if title_tag is not None else (title+' | Matt Miller · NOLAPATENT' if route else title)
    data=json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')
    style_links=''.join(f'<link rel="stylesheet" href="{pathlink(route,style)}">' for style in styles)
    html=f'''<!doctype html>
<html lang="en-US"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(meta_title)}</title><meta name="description" content="{e(description)}"><meta name="author" content="{e(P['name'])}"><meta name="robots" content="{'index, follow, max-image-preview:large' if index else 'noindex, follow'}"><link rel="canonical" href="{url}"><meta name="theme-color" content="#183e3b"><meta property="og:type" content="{'article' if kind=='Article' else 'website'}"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="NOLAPATENT"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/social-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Matt Miller, New Orleans patent and intellectual property attorney at Kean Miller"><link rel="icon" href="{pathlink(route,'assets/favicon.svg')}" type="image/svg+xml"><link rel="alternate" type="application/rss+xml" title="NOLAPATENT Insights" href="{pathlink(route,'feed.xml')}"><link rel="stylesheet" href="{pathlink(route,'assets/site.css')}">{style_links}<script type="application/ld+json">{data}</script><script src="{pathlink(route,'assets/site.js')}" defer></script></head><body>{header(route)}<main id="main">{body}</main>{contact(route) if with_contact else ''}{footer(route)}</body></html>'''
    target=DIST/route/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(html,encoding='utf-8')
    GENERATED.append(target)
    if index and canon is None:PAGES[route]={'title':title,'description':description}

def crumbs(route,label,blog=False):
    return f'<nav class="crumbs" aria-label="Breadcrumb">{link(route,"","Home")}<span aria-hidden="true">/</span>'+ (link(route,'blog/','Insights')+'<span aria-hidden="true">/</span>' if blog else '')+f'<span>{e(label)}</span></nav>'

def pagehero(route,title,lede='',eyebrow=''):
    return f'<section class="page-hero"><div class="wrap">{crumbs(route,stripped(title))}'+(f'<span class="eyebrow">{e(eyebrow)}</span>' if eyebrow else '')+f'<h1>{title}</h1>'+ (f'<p class="lede">{lede}</p>' if lede else '')+'</div></section>'

def art(n=0):
    patterns=[
        '<path d="M40 95V45l40-23 40 23v50l-40 23zM40 45l40 24 40-24M80 69v49M80 22v47"/><circle cx="80" cy="69" r="52"/><path d="M145 20v100M138 20h14M138 120h14M25 128h100"/>',
        '<path d="M50 20h75v90H50zM65 40h45M65 55h45M65 70h30M125 35h20v90H70v-15"/><circle cx="127" cy="92" r="22"/><path d="M114 92l9 9 18-18M25 15v115M20 15h10M20 130h10"/>',
        '<circle cx="90" cy="70" r="35"/><circle cx="90" cy="70" r="12"/><path d="M35 35l20 15M35 105l20-15M125 50l25-15M125 90l25 15M90 15v20M90 105v20"/><circle cx="30" cy="30" r="9"/><circle cx="30" cy="110" r="9"/><circle cx="155" cy="30" r="9"/><circle cx="155" cy="110" r="9"/><path d="M55 70H20M125 70h50"/>'
    ]
    return f'<svg viewBox="0 0 190 140" fill="none" stroke-width="1" aria-hidden="true">{patterns[n%3]}</svg>'

def card(route,p,n=0,illustration=False):
    haystack=e((p['title']+' '+p['excerpt']+' '+p['topic']).lower())
    return f'''<a class="insight-card" href="{pathlink(route,post_route(p))}" data-article data-topic="{e(p['topic'])}" data-search="{haystack}">{'<div class="insight-art">'+art(n)+'</div>' if illustration else ''}<span class="tag">{e(p['topic'])}</span><div class="article-meta"><time datetime="{p['date']}">{pretty(p['date'])}</time> · {reading(p)} min read</div><h3>{e(p['title'])}</h3><p>{e(p['excerpt'])}</p><span class="read-link">Read the article</span></a>'''

PRACTICES=[
{'slug':'patents','name':'Patents','short':'From the first application to the next challenge. Patent applications, prosecution, and disputes involving a range of technologies.','title':'Patent Prosecution and Litigation','intro':'Patent prosecution and litigation for software, mechanical systems, and energy technologies.','body':'<p>Understanding an invention starts with understanding the technology. Before becoming a lawyer, Matt Miller worked as a software engineer. He is also a named co-inventor on U.S. patents in image processing and video surveillance.</p><h2>From application to enforcement</h2><p>Matt is a registered patent attorney who prosecutes applications before the U.S. Patent and Trademark Office. His experience includes computer software, mechanical systems, and oil-and-gas exploration and production technologies.</p><p>His practice also includes patent litigation in federal court and proceedings before the Patent Trial and Appeal Board. His litigation experience also informs how he approaches patent claims, prosecution strategy, and potential enforcement issues.</p><h2>Understanding the invention</h2><p>Before preparing a patent application, Matt works to understand how an invention operates, how it differs from existing technology, and which features are important to the business. Those details help guide decisions about the patent disclosure and claims.</p>','items':['Utility and design patent applications','Patent prosecution before the USPTO','Patent litigation in federal court','Patent Trial and Appeal Board proceedings'],'topics':['Patents','Artificial intelligence']},
{'slug':'trademarks','name':'Trademarks','short':'Clear the way for your brand. Trademark applications, portfolio protection, and enforcement.','title':'Protect the name you’re building.','intro':'Trademark clearance, federal prosecution, and enforcement for brands and businesses.','body':'<p>A name can become one of a business’s most recognizable assets. Matt helps clients address trademark questions from clearance and applications through enforcement and disputes.</p><h2>Trademark Applications and Disputes</h2><p>Matt’s experience includes federal trademark prosecution, litigation in federal courts, and matters before the Trademark Trial and Appeal Board.</p><p>He previously served as an Adjunct Professor at Tulane Law School, where he ran a trademark law clinic. He taught students trademark law and supervised their work helping people apply for and obtain trademark registrations.</p><h2>When to Seek Trademark Advice</h2><p>Trademark questions often arise when a business adopts a new name, expands a brand, or discovers another company\'s potentially conflicting mark. Matt advises on trademark clearance, registration, enforcement, and disputes.</p>','items':['Trademark clearance','Federal trademark applications','Trademark enforcement and disputes','Trademark Trial and Appeal Board matters'],'topics':['Trademarks']},
{'slug':'copyright','name':'Copyright','short':'For the things you create. Ownership, registration, and enforcement for code and creative work.','title':'Copyright for Software and Creative Works','intro':'Copyright counsel for software, websites, books, advertising, and other creative works.','body':'<p>Matt’s copyright practice brings together legal experience and firsthand knowledge of software development. He advises clients on ownership, registration with the U.S. Copyright Office, and enforcement.</p><h2>Where code and copyright meet</h2><p>Before law school, Matt worked as a software engineer. During law school, he helped develop the logic representation language and engine for the Durationator, a Tulane project analyzing copyright terms around the world.</p><p>His work includes copyright issues involving software, websites, books, and advertising materials. He also advises on website copyright compliance.</p><h2>Copyright Ownership and Agreements</h2><p>Copyright ownership can depend on who created the work, whether it was created in the course of employment, and what the applicable agreements provide. Matt advises clients on ownership, copyright assignments, registration, and enforcement.</p>','items':['Copyright ownership and registration','Software and website copyright','Copyright enforcement','Website copyright compliance'],'topics':['Copyright','Artificial intelligence']},
{'slug':'technology','name':'Technology & IP','short':'Work with a lawyer who has written code. Software contracts, licensing, open-source issues, and IP.','title':'Counsel who understands the code.','intro':'Software contracts, licensing, open-source issues, and intellectual property counsel from a lawyer who has worked as a software engineer.','body':f'<p>When a legal question depends on how software is built, used, or distributed, firsthand development experience matters. Matt worked as a software engineer before becoming a lawyer. His technical background includes programming, databases, web applications, Linux administration, and open-source software.</p><p>His work has included performance benchmarks with Motorola’s Java virtual machine team, the front and back ends of a streaming-media website at Blastro, and video-surveillance and web-service software at Model Software. That experience helps him work through architecture, interfaces, and development responsibilities with the people building the product.</p><h2>Software Development and Licensing Agreements</h2><p>Software agreements need to address what is being developed, who owns the resulting work, and what each party is responsible for. Matt advises on software development and licensing agreements involving deliverables, code ownership, third-party components, licensing rights, and ongoing responsibilities.</p><h2>Open-Source Licensing</h2><p>Open-source licenses can impose requirements concerning attribution, distribution, and access to source code. The applicable obligations depend on the license and how the software is used or distributed. Matt helps clients evaluate these issues when developing, licensing, or distributing software.</p><h2>Other Technology-Related IP Matters</h2><p>His practice also includes patents, trademarks, copyrights, trade secrets, website policies, and domain-name proceedings. As a registered patent attorney and named inventor, he brings experience with both developing technology and protecting it.</p><p>You can also see examples of Matt\'s programming work on <a href="{P["github_url"]}">GitHub</a>. To discuss a potential engagement, contact Matt at Kean Miller.</p>','items':['Software development and licensing agreements','Open-source licensing and compliance questions','Software ownership and intellectual property','Trade secrets, websites, and domain names'],'topics':['Technology','Business & technology','Artificial intelligence']}
]

def patent_plate(route,which):
    records={
        'tesla':('tesla-generator-447921','Nikola Tesla','Alternating Electric Current Generator','447,921','March 10, 1891','https://patents.google.com/patent/US447921A/en'),
        'bell':('bell-telegraphy-174465','Alexander Graham Bell','Improvement in Telegraphy','174,465','March 7, 1876','https://patents.google.com/patent/US174465A/en')
    }
    asset,inventor,title,number,issued,url=records[which]
    return f'<figure class="patent-plate"><a class="patent-sheet" href="{url}" aria-label="View {e(inventor)} patent {number}"><img src="{pathlink(route,"assets/patents/"+asset+".webp")}" width="885" height="1300" alt="{e(inventor)} patent drawing: {e(title)}, U.S. Patent {number}" loading="lazy" decoding="async"></a><figcaption><strong>{e(inventor)}</strong><span>{e(title)}</span><a href="{url}">U.S. {number} · {issued} <span aria-hidden="true">↗</span></a></figcaption></figure>'

def patent_gallery(route):
    return f'''<section class="section patent-gallery" aria-labelledby="patent-history-heading"><div class="wrap patent-gallery-grid"><div><span class="eyebrow">From the patent files</span><h2 id="patent-history-heading">Invention,<br>on paper.</h2><p>Patent applications have always depended on explaining how an invention works. These patents from Nikola Tesla and Alexander Graham Bell illustrate the importance of detailed technical descriptions and drawings. That same attention to technical detail remains important today.</p>{link(route,'practice/patents/','Explore patent counsel <span aria-hidden="true">↗</span>','text-link')}</div><div class="patent-pair">{patent_plate(route,'tesla')}{patent_plate(route,'bell')}</div></div></section>'''

def experience_section(route):
    return f'''<section class="section dark" id="about" aria-labelledby="experience-heading"><div class="wrap about-grid experience-grid">
<div><span class="eyebrow">Experience behind the perspective</span><h2 id="experience-heading">I speak law.<br><em>And code.</em></h2>
<p>Before I became a lawyer, I was a software engineer. I’ve built apps, helped turn copyright law into software, and co-invented patented video surveillance technology.</p>
<p>That experience shapes how I work with clients on software contracts, open-source issues, licensing, and patents: understand how the technology works, then connect the legal advice to the product and the business. Learn more about my work as a {link(route,"practice/software-patents/","software patent attorney")}.</p>
{link(route,'about-me/','More about my background <span aria-hidden="true">↗</span>','text-link')}<p class="experience-github">{link(route,P['github_url'],'Find me on GitHub <span aria-hidden="true">↗</span>','text-link')}</p></div>
<div class="experience-stories">
<article class="experience-story"><span class="experience-number" aria-hidden="true">01</span><div><h3>Patents from the inventor’s side.</h3><p>I’m a co-inventor of video surveillance technology involving image processing and object tracking. My issued U.S. patents, each titled <em>Video surveillance system</em>, include <a href="https://patents.google.com/patent/US7859564B2/en">7,859,564</a>, <a href="https://patents.google.com/patent/US7956889B2/en">7,956,889</a>, and <a href="https://patents.google.com/patent/US8605155B2/en">8,605,155</a>. I bring that experience of developing an invention to my work as a patent attorney.</p></div></article>
<article class="experience-story"><span class="experience-number" aria-hidden="true">02</span><div><h3>The Durationator: copyright law in code.</h3><p>At Tulane, I helped develop the logic representation language and engine for the Durationator, software for analyzing copyright terms worldwide. <a href="https://wp0.vanderbilt.edu/lawreview/wp-content/uploads/sites/278/2011/10/Townsend_Gard_64_Vand_L_Rev_En_Banc_199.pdf">Professor Elizabeth Townsend Gard’s 2011 law review article</a> discusses the challenges of developing the Durationator. Justice Breyer cited her article in his Supreme Court dissent in <a href="https://www.govinfo.gov/content/pkg/USREPORTS-565/pdf/USREPORTS-565-302.pdf#page=56"><em>Golan v. Holder</em>, 565 U.S. 302, 357 (2012)</a>.</p></div></article>
<article class="experience-story"><span class="experience-number" aria-hidden="true">03</span><div><h3>The first Louisiana Civil Code app for iPhone.</h3><p>In 2009, I developed and released the first Louisiana Civil Code iOS app, putting a searchable legal reference in lawyers’ pockets. It was a practical way to bring my work in software and law together.</p><a class="experience-source" href="https://www.iphonejd.com/iphone_jd/2009/10/louisiana-civil-code-code-of-civil-procedure-and-code-of-evidence.html">Read the original iPhone J.D. review <span aria-hidden="true">↗</span></a></div></article>
</div></div></section>'''

def homepage_recognition():
    best=RECOGNITIONS['best_lawyers']
    practices=' and '.join(best['practices'])
    return f'''<section class="recognition-band" id="best-lawyers" aria-label="Professional recognition"><div class="wrap"><a class="recognition-feature" href="{e(best['profile_url'])}"><div><span class="recognition-label">Professional recognition</span><h2>Best Lawyers<sup>®</sup></h2><span class="recognition-location">{e(best['location'])}</span></div><div class="recognition-summary"><p>Recognized in the <strong>{best['edition']} edition</strong> of <em>{e(best['publication'])}</em><sup>®</sup> for {e(practices)}.</p><span class="recognition-profile-link">View recognition profile</span></div><span class="recognition-arrow" aria-hidden="true">↗</span></a></div></section>'''


def professional_recognition(route):
    best=RECOGNITIONS['best_lawyers']
    past=RECOGNITIONS['rising_stars']
    return f'''<section class="professional-recognition" id="professional-recognition" aria-labelledby="professional-recognition-heading"><h2 id="professional-recognition-heading">Professional Recognition</h2><div class="recognition-entries"><article class="recognition-entry"><span class="recognition-label">Current recognition</span><h3><a href="{e(best['profile_url'])}"><em>{e(best['publication'])}</em><sup>®</sup> <span>— {best['edition']}</span></a></h3><p>Recognized in {e(' and '.join(best['practices']))}.</p><p class="recognition-location">{e(best['location'])}</p></article><article class="recognition-entry"><span class="recognition-label">Historical recognition</span><h3><a href="{e(past['profile_url'])}"><em>{e(past['publication'])}</em> {e(past['designation'])} <span>— {e(past['years'])}</span></a></h3><p>Selected in {e(past['practice'])} for {e(past['consecutive_years'])} consecutive years.</p></article></div></section>'''


def home():
    route=''
    practices=''.join(f'<a class="practice-item" href="{pathlink(route,"practice/"+p["slug"]+"/")}"><span class="practice-number">0{i+1} /</span><h3>{p["name"]}</h3><p>{p["short"]}</p><span class="arrow" aria-hidden="true">↗</span></a>' for i,p in enumerate(PRACTICES))
    featured=[p for p in POSTS if not p.get('archived',False)][:3]
    featured += [next(p for p in POSTS if p['id']==i) for i in [509,504,489] if not any(p['id']==i for p in featured)][:3-len(featured)]
    body=f'''<section class="hero"><div class="wrap hero-layout"><div class="hero-copy"><span class="eyebrow">New Orleans · Intellectual property law</span><h1>A lawyer who<br>understands<br><em>technology.</em></h1><p class="hero-intro">I help businesses protect inventions and address software contracts, licensing, and open-source issues. As a former software engineer and registered patent attorney, I bring firsthand experience building technology to the work of protecting it.</p><p class="hero-name"><strong>Matt Miller</strong><span>Registered Patent Attorney · Special Counsel with <a href="https://www.keanmiller.com/service/intellectual-property/">Kean Miller's Intellectual Property Group</a></span></p><div class="hero-actions">{link(route,'contact/','Discuss your project <span aria-hidden="true">↗</span>','button')}{link(route,'about-me/','Meet Matt <span aria-hidden="true">↗</span>','text-link')}</div></div><div class="portrait-stage"><div class="drawing">{art(0)}</div><img src="{pathlink(route,'assets/matt-miller.webp')}" width="700" height="700" alt="Matt Miller, patent and intellectual property attorney at Kean Miller" fetchpriority="high"><div class="portrait-caption"><strong>Technical roots. Legal perspective.</strong><small>New Orleans, Louisiana</small></div></div></div></section>
<div class="trust-strip"><div class="wrap trust-inner"><span>Registered U.S. Patent Attorney</span><span>Former software engineer</span><span>Named inventor on U.S. patents</span><span>Special Counsel · Kean Miller</span></div></div>
{homepage_recognition()}
<section class="section" id="practice"><div class="wrap"><span class="eyebrow">How I can help</span><div class="section-heading"><h2>Protecting inventions, software, and brands.</h2><p>I help clients obtain patent and trademark protection, address copyright and intellectual property disputes, and negotiate software and technology agreements.<br>{link(route,"practice/software-patents/","Software patent attorney in New Orleans ↗","text-link")}</p></div><div class="practice-grid">{practices}</div></div></section>
{patent_gallery(route)}
{experience_section(route)}
<section class="section"><div class="wrap"><span class="eyebrow">Notes from the intersection</span><div class="section-heading"><h2>Law. Technology.<br>What comes next.</h2>{link(route,'blog/','Explore all insights <span aria-hidden="true">↗</span>','text-link')}</div><div class="insight-grid">{''.join(card(route,p,i,True) for i,p in enumerate(featured))}</div><div class="firm-insights"><strong>More writing at Kean Miller</strong><a href="https://www.keanmiller.com/insights/blog/intellectual-property-law/recent-uspto-guidance-makes-it-easier-to-obtain-design-patent-protection-for-digital-interfaces/">Design patent protection for digital interfaces <span aria-hidden="true">↗</span><br><span class="subtle">March 17, 2026 · Kean Miller</span></a><a href="https://www.keanmiller.com/insights/blog/intellectual-property-law/uspto-director-intends-to-embrace-ai-on-many-levels/">The USPTO and artificial intelligence <span aria-hidden="true">↗</span><br><span class="subtle">November 3, 2025 · Kean Miller</span></a></div></div></section>
<section class="section faq-section"><div class="wrap faq-grid"><div><span class="eyebrow">Common questions.</span><h2>A few useful<br>starting points.</h2></div><div class="faq-list"><details><summary>What kinds of legal matters do you handle?</summary><p>I handle patent applications and disputes, trademarks, copyrights, trade secrets, software licensing, software development agreements, and other technology-related intellectual property matters.</p></details><details><summary>What is your technical background?</summary><p>I studied computer science at Duke University and worked as a software engineer before becoming an attorney. I've developed web applications, worked with databases and Linux systems, and written software for commercial and legal applications. I'm also a named inventor on three issued U.S. patents.</p></details><details><summary>Can you help with software contracts and open-source issues?</summary><p>Yes. I work on software development and licensing agreements, including ownership of code, third-party software, licensing terms, and open-source compliance. My software engineering background helps me understand how these issues arise in actual development projects.</p></details><details><summary>Where do you practice?</summary><p>I'm based in Kean Miller's New Orleans office. I'm licensed in Louisiana and registered to practice before the U.S. Patent and Trademark Office. Representation in other jurisdictions depends on the matter and applicable rules.</p></details><details><summary>How can I contact you?</summary><p>You can reach me at Kean Miller at <a href="tel:{P['telephone']}">{P['display_phone']}</a> or <a href="mailto:{P['email']}">{P['email']}</a>. Please don't send confidential information before an attorney-client relationship has been established.</p></details></div></div></section>'''
    page(route,'New Orleans Patent & IP Attorney | Matt Miller','Matt Miller, a former software engineer and New Orleans IP attorney at Kean Miller, helps with patents, software contracts, licensing, and open-source issues.',body)

def blog(route='blog/',subset=None,title='Ideas, examined.',canon=None):
    posts=POSTS if subset is None else subset
    topics=['All']+sorted({p['topic'] for p in posts})
    body=pagehero(route,title,'Thoughts on intellectual property, software, and the things people create.','The NOLAPATENT journal')
    body+=f'''<div class="wrap"><div class="filters"><div class="search-row"><div class="search-wrap"><label for="article-search">Search the journal</label><input id="article-search" type="search" placeholder="Try patents, copyright, or artificial intelligence…" autocomplete="off"></div><div id="result-count" class="result-count" role="status" aria-live="polite">{len(posts)} articles</div></div><div class="filter-buttons" role="group" aria-label="Filter articles by topic">{''.join(f'<button type="button" data-filter="{e(t)}" aria-pressed="{str(t=="All").lower()}">{e(t)}</button>' for t in topics)}</div><noscript><p>All articles appear below. Search and topic filters require JavaScript.</p></noscript></div><div class="archive-grid">{''.join(card(route,p,i) for i,p in enumerate(posts))}</div><div id="no-results" class="no-results" hidden><h2>No articles found.</h2><p>Try a different topic or search term.</p><button id="clear-search" class="button" type="button">Clear search and filters</button></div></div>'''
    page(route,title,'Browse Matt Miller’s articles on patents, trademarks, copyright, artificial intelligence, and technology. Original posts from the NOLAPATENT archive.',body,'CollectionPage',canon=canon)

def rewrite_content(body,route):
    def replace(m):
        attr,url=m[1],unescape(m[2])
        parsed=urlsplit(url)
        if parsed.netloc in ('www.nolapatent.com','nolapatent.com'):
            qs=parse_qs(parsed.query)
            pid=(qs.get('p') or qs.get('page_id') or [''])[0]
            target=ID_ROUTES.get(pid) if pid else parsed.path.lstrip('/')
            if pid and not target: return m[0]
            if parsed.fragment: target+='#'+parsed.fragment
            url=pathlink(route,target)
        elif url.startswith('assets/'):
            url=pathlink(route,url)
        return f'{attr}="{e(url)}"'
    return re.sub(r'(href|src)="([^"]*)"',replace,body)

def article(p):
    route=post_route(p)
    body=(ROOT/'content/posts'/f'{p["slug"]}.html').read_text(encoding='utf-8')
    headings=[]
    def heading(m):
        label=stripped(m[3]);ident='section-'+str(len(headings)+1);headings.append((ident,label))
        return f'<h{m[1]} id="{ident}">{m[3]}</h{m[1]}>'
    body=re.sub(r'<h([23])([^>]*)>(.*?)</h\1>',heading,body,flags=re.S)
    body=rewrite_content(body,route)
    toc=''.join(f'<li><a href="#{ident}">{e(label)}</a></li>' for ident,label in headings)
    aside=f'<span class="eyebrow">In this article</span><ul class="toc">{toc}</ul>' if toc else '<span class="eyebrow">From the journal</span><p>Intellectual property and technology, from a practical perspective.</p>'
    byline=f'<div class="byline"><img src="{pathlink(route,"assets/matt-miller.webp")}" alt="" width="44" height="44"><div><strong>{P["name"]}</strong><small>Special Counsel at Kean Miller · Registered Patent Attorney</small></div></div>'
    head=f'<header class="page-hero"><div class="wrap article-head">{crumbs(route,p["topic"],True)}<span class="eyebrow">{e(p["topic"])}</span><h1>{e(p["title"])}</h1><div class="article-meta">Published <time datetime="{p["date"]}">{pretty(p["date"])}</time> · {reading(p)} min read</div>{byline}</div></header>'
    note=f'<aside class="author-box" aria-labelledby="author-heading"><img src="{pathlink(route,"assets/matt-miller.webp")}" width="65" height="65" alt="Matt Miller" loading="lazy"><div><small>About the author</small><h2 id="author-heading">Matt Miller</h2><p>{e(p["author_note"])} Matt is Special Counsel at Kean Miller in New Orleans.</p>{link(route,"about-me/","Meet Matt and explore his experience ↗")}</div></aside>'
    related=[q for q in POSTS if q['slug']!=p['slug'] and q['topic']==p['topic']][:3]
    if len(related)<3:related += [q for q in POSTS if q['slug']!=p['slug'] and q not in related][:3-len(related)]
    notice=f'<p class="archive-notice">From the archive · Originally published {pretty(p["date"])}. This article reflects its original publication period and has not been substantively updated. Laws, procedures, and technology may have changed. Author and contact information are current.</p>' if p.get('archived',False) else ''
    full=head+f'<div class="wrap article-layout"><aside class="article-side"><div class="article-side-inner">{aside}{link(route,"contact/","Discuss an IP matter ↗","button")}</div></aside><div><article class="prose">{notice}{body}</article>{note}<div class="article-footer-links">{link(route,"blog/","← All insights")}{link(route,"contact/","Contact Matt ↗")}</div></div></div><section class="related"><div class="wrap"><h2>Keep exploring.</h2><div class="insight-grid">'+''.join(card(route,q,i) for i,q in enumerate(related))+'</div></div></section>'
    schema={'@type':'BlogPosting','@id':canonical(route)+'#article','headline':p['title'],'description':p['excerpt'],'datePublished':p['published'],'author':{'@id':BASE+'/#matt-miller'},'publisher':{'@id':BASE+'/#matt-miller'},'mainEntityOfPage':{'@id':canonical(route)+'#webpage'},'articleSection':p['topic'],'inLanguage':'en-US','image':BASE+'/assets/social-card.jpg','wordCount':len(stripped(body).split())}
    if p.get('modified'):schema['dateModified']=p['modified']
    page(route,p['title'],p['excerpt'],full,'Article',[schema])

def publications(route, compact=False):
    """Render citations and matching scholarly metadata from the same source."""
    groups, graph = [], []
    for kind, heading in [('law-review', 'Law review publications'), ('conference', 'Computer science conference abstract')]:
        citations = []
        selected = sorted((p for p in PUBLICATIONS if p['kind'] == kind), key=lambda p: p['year'], reverse=True)
        for publication in selected:
            authors = publication['authors']
            author_text = authors[0] if len(authors) == 1 else ', '.join(authors[:-1]) + ', and ' + authors[-1]
            if kind == 'law-review':
                citation = f'''{e(author_text)}, {e(publication['volume'])} <em>{e(publication['journal_abbreviation'])}</em> {e(publication['page'])} ({e(publication['year'])}).'''
                container = {
                    '@type': 'PublicationVolume', 'volumeNumber': publication['volume'],
                    'isPartOf': {'@type': 'Periodical', 'name': publication['journal'], 'url': 'https://journals.tulane.edu/TIP/'},
                }
            else:
                citation = f'''{e(author_text)}. ({e(publication['year'])}). In <em>{e(publication['proceedings'])}</em>, p. {e(publication['page'])}. {e(publication['publisher'])}. DOI: {e(publication['doi'])}.'''
                container = {'@type': 'CreativeWork', 'name': publication['proceedings']}
            summary = f'<p class="publication-summary">{e(publication["description"])}</p>' if publication.get('description') and not compact else ''
            citations.append(f'''<li class="publication-entry"><h4>{link(route,publication['url'],e(publication['title']))}</h4><p class="publication-citation">{citation}</p>{summary}</li>''')
            node = {
            '@type': 'ScholarlyArticle',
            '@id': canonical(route) + '#' + publication['id'],
            'name': publication['title'], 'url': publication['url'],
            'author': [
                {'@id': BASE + '/#matt-miller'} if name == 'J. Matthew Miller III'
                else {'@type': 'Person', 'name': name}
                for name in authors
            ],
            'datePublished': publication['year'], 'pagination': publication['page'],
            'genre': publication['genre'], 'isPartOf': container,
            }
            if publication.get('doi'):
                node['identifier'] = {'@type': 'PropertyValue', 'propertyID': 'DOI', 'value': publication['doi']}
            if publication.get('publisher'):
                node['publisher'] = {'@type': 'Organization', 'name': publication['publisher']}
            if publication.get('description'):
                node['description'] = publication['description']
            graph.append(node)
        intro = ''.join(f'<p>{e(p["intro"])}</p>' for p in selected if p.get('intro') and not compact)
        groups.append(f'<div class="publication-group"><h3 class="publication-group-heading">{heading}</h3>{intro}<ol class="publication-list">' + ''.join(citations) + '</ol></div>')
    intro = 'While attending Tulane Law School, I published two works in the Tulane Journal of Technology &amp; Intellectual Property examining the intersection of copyright law and the First Amendment. Both addressed constitutional issues surrounding copyright protection that were then working their way through the federal courts.'
    if compact:
        intro = 'My writing in the Tulane Journal of Technology &amp; Intellectual Property examined copyright and the First Amendment. The earlier ACM publication is a coauthored conference abstract from my undergraduate years.'
    return '<section id="selected-publications" aria-labelledby="publications-heading"><h2 id="publications-heading">Selected Publications</h2><p>' + intro + '</p>' + ''.join(groups) + '</section>', graph


def about():
    route='about-me/'
    publication_html, publication_graph = publications(route, compact=True)
    body=(ROOT/'content/pages/about.html').read_text(encoding='utf-8')
    components={
        'publications':publication_html, 'recognition':professional_recognition(route),
        'bio_url':e(P['bio_url']), 'github_url':e(P['github_url']),
        'linkedin_url':e(P['linkedin_url']),
    }
    for name,value in components.items():
        body=body.replace('{{'+name+'}}',value)
    if re.search(r'{{[^}]+}}',body):
        raise ValueError('Unresolved About page template token')
    body=rewrite_content(body,route)
    page(route,'About Matt Miller', 'Matt Miller is a former software engineer and Kean Miller IP attorney helping with software contracts, open-source issues, licensing, and patent protection.',body,'ProfilePage',publication_graph,styles=('assets/about.css',))


def representative_experience():
    route='representative-experience/'
    data=json.loads((ROOT/'content/representative-experience.json').read_text(encoding='utf-8'))
    sections=data['sections']
    body=pagehero(route,'Representative experience.','Selected patent, trademark, copyright, and domain-name matters from Matt Miller’s practice.','From protection to enforcement')
    body+='<div class="wrap"><div class="experience-intro"><p>These examples include work completed before Matt joined Kean Miller. They illustrate the range of his experience with obtaining protection, resolving disputes, and enforcing intellectual property rights.</p><nav class="matter-jumps" aria-label="Experience by practice area">'+''.join(link(route,'#'+s['id'],e(s['name'])) for s in sections)+'</nav></div>'
    entries=[]
    for section in sections:
        body+=f'<section class="matter-section" id="{section["id"]}" aria-labelledby="{section["id"]}-heading"><div class="matter-section-heading"><div><h2 id="{section["id"]}-heading">{e(section["name"])}</h2><p>{e(section["intro"])}</p></div>{link(route,section["practice_url"],"Explore this practice <span aria-hidden=\"true\">↗</span>","text-link")}</div><div class="matter-grid">'
        for matter in section['matters']:
            reference=link(route,matter['url'],e(matter['reference'])+' <span aria-hidden="true">↗</span>') if matter.get('url') else e(matter['reference'])
            case=f'<p class="matter-case">{e(matter["case"])}</p>' if matter.get('case') else ''
            software_link=f'<p>{link(route,"practice/software-patents/","Software patent prosecution informed by engineering experience ↗","text-link")}</p>' if matter['reference']=='U.S. Patent No. 8,725,663' else ''
            body+=f'<article class="matter-entry"><h3>{e(matter["title"])}</h3><p>{e(matter["result"])}</p>{case}<p class="matter-reference">{reference}</p>{software_link}</article>'
            entries.append({'@type':'ListItem','position':len(entries)+1,'name':matter['title']+' — '+matter['reference']})
        body+='</div></section>'
    body+=f'<aside class="results-note"><p>These are selected examples of past work. Each matter depends on its facts and circumstances; past results do not guarantee a similar outcome.</p><p>{link(route,P["bio_url"],"View Matt’s current professional biography at Kean Miller ↗")}</p></aside></div>'
    schema={'@type':'ItemList','name':'Matt Miller representative experience','numberOfItems':len(entries),'itemListElement':entries}
    page(route,'Representative Experience','Selected patent, trademark, copyright, and domain-name matters handled by Matt Miller, Special Counsel at Kean Miller in New Orleans.',body,'CollectionPage',[schema])

def practice_pages():
    for p in PRACTICES:
        route='practice/'+p['slug']+'/'
        relevant=[q for q in POSTS if q['topic'] in p['topics']][:3]
        body=pagehero(route,p['title'],p['intro'],'New Orleans · '+p['name'])
        practice_body=p['body']
        if p['slug']=='patents':
            practice_body+=f'<h2>Software patent prosecution</h2><p>Matt prepares and prosecutes patent applications for software-related inventions. His development experience helps him work through implementation details and connect them to the patent disclosure and claims. {link(route,"practice/software-patents/","Explore software patent prosecution ↗","text-link")}</p>'
        body+=f'<div class="wrap practice-layout"><article class="prose">{practice_body}<p>{link(route,"representative-experience/#"+p["slug"] if p["slug"]!="technology" else "representative-experience/#domain-names","View representative matters ↗","text-link")}</p><p class="sources">Experience described in <a href="{P["bio_url"]}">Matt’s Kean Miller biography</a>.</p></article><aside class="practice-aside"><h2>How Matt can help</h2><ul>'+''.join('<li>'+e(x)+'</li>' for x in p['items'])+f'</ul>{link(route,"contact/","Talk with Matt ↗","button")}</aside></div>'+(f'<section class="practice-patent-history"><div class="wrap"><span class="eyebrow">Technical detail, on paper</span>{patent_plate(route,"tesla")}</div></section>' if p['slug']=='patents' else '')+'<section class="related"><div class="wrap"><span class="eyebrow">Explore the subject</span><h2>From the journal.</h2><div class="insight-grid">'+''.join(card(route,q,i) for i,q in enumerate(relevant))+'</div></div></section>'
        schema={'@type':'Service','name':p['name']+' legal services','serviceType':p['name'],'provider':{'@id':BASE+'/#matt-miller'},'url':canonical(route),'description':p['intro']}
        page(route,'Patent Attorney in New Orleans' if p['slug']=='patents' else p['name']+' Attorney in New Orleans',p['intro']+' Matt Miller, registered patent attorney and Special Counsel at Kean Miller.',body,extra=[schema])

def software_patents():
    route='practice/software-patents/'
    title='Software Patent Attorney in New Orleans'
    description='Matt Miller is a New Orleans patent attorney, former software engineer, and named inventor who handles software patent prosecution and intellectual property matters.'
    body=pagehero(route,'Software Patent Attorney in New Orleans','Patent prosecution for software-related inventions, informed by firsthand software engineering experience.','New Orleans · Software patents')
    text=(ROOT/'content/pages/software-patents.html').read_text(encoding='utf-8')
    text=rewrite_content(text,route)
    body+=f'<div class="wrap practice-layout"><article class="prose">{text}</article><aside class="practice-aside"><h2>Software patent counsel</h2><ul><li>Application preparation and prosecution</li><li>Patent portfolio strategy</li><li>Patent litigation</li><li>PTAB proceedings</li></ul>{link(route,"contact/","Contact Matt ↗","button")}</aside></div>'
    schema={'@type':'Service','name':'Software patent legal services','serviceType':'Software patent counsel','provider':{'@id':BASE+'/#matt-miller'},'url':canonical(route),'description':description}
    page(route,title,description,body,extra=[schema],title_tag='Software Patent Attorney in New Orleans | Matt Miller')


def simple_pages():
    route='contact/'
    body=pagehero(route,'Let’s start a conversation.','Tell me what you’re working on. We can discuss whether my experience is a fit for your needs.','Contact Matt')
    body+=f'''<div class="wrap simple-content prose"><h2>Matt Miller · Kean Miller</h2><p>J. Matthew Miller, III<br>Special Counsel · Registered Patent Attorney</p><p><a href="tel:{P['telephone']}">{P['display_phone']}</a><br><a href="mailto:{P['email']}">{P['email']}</a></p><address style="font-style:normal">{P['street']}<br>New Orleans, Louisiana {P['postal_code']}</address><p style="margin-top:25px">{link(route,P['office_url'],'Office information and directions at Kean Miller ↗')}</p><h2>Before sharing details</h2><p>An inquiry does not create an attorney-client relationship. Please do not send confidential information unless you have already signed paperwork to engage Kean Miller to represent you.</p><p>{link(route,P['bio_url'],'View my professional profile at Kean Miller ↗','text-link')}</p><p>{link(route,P['linkedin_url'],'Connect with Matt on LinkedIn ↗','text-link')}</p></div>'''
    page(route,'Contact Matt Miller','Contact New Orleans patent attorney Matt Miller at Kean Miller: 504.620.3356, matthew.miller@keanmiller.com. Office at 909 Poydras Street, Suite 3600.',body,'ContactPage',with_contact=False)
    route='disclaimer/'
    text='''<h2>About this website</h2><p>This personal website is operated by J. Matthew Miller, III (Matt Miller), Special Counsel at Kean Miller. Matt is responsible for its content. The website is maintained by Matt and does not purport to state the views of Kean Miller.</p><h2>General information, not legal advice</h2><p>Material on this website is provided for general informational purposes. It may not reflect current law, procedure, or technology and is not advice for a particular matter. Archived articles retain their original publication dates and have not been substantively updated unless expressly stated.</p><h2>No attorney-client relationship</h2><p>Visiting this website or contacting Matt does not create an attorney-client relationship. Matt accepts legal engagements through Kean Miller, subject to conflicts review and an agreed engagement. Do not rely on this website as a substitute for advice from counsel familiar with your facts.</p><h2>Confidential information</h2><p>An inquiry does not create an attorney-client relationship. Please do not send confidential information unless you have already signed paperwork to engage Kean Miller to represent you.</p><h2>Experience and results</h2><p>Descriptions of experience are informational and do not guarantee outcomes. Every matter depends on its own facts and circumstances. “Registered Patent Attorney” refers to registration to practice before the U.S. Patent and Trademark Office; descriptions of practice areas do not assert board certification.</p><h2>Jurisdictions</h2><p>Matt is licensed in Louisiana and registered to practice before the USPTO. Work involving other jurisdictions is subject to applicable laws, court rules, and professional standards. This site does not seek engagements where doing so would constitute unauthorized practice.</p><h2>Office and responsible lawyer</h2><p>J. Matthew Miller, III, Kean Miller, 909 Poydras Street, Suite 3600, New Orleans, LA 70112. Telephone: 504.620.3356. Matt is responsible for this personal website and its cost.</p><h2>Third-party material</h2><p>Links to third-party sources are provided for convenience. Their content and availability are outside Matt’s control. Historical posts may contain quotations, images, and other material attributed to their respective sources.</p><h2>Copyright</h2><p>Original website content © Matt Miller. Third-party material remains the property of its respective owners.</p>'''
    page(route,'Disclaimer','Important information about this personal website, legal information, confidentiality, and contacting Matt Miller at Kean Miller.',pagehero(route,'A few important details.','Information about this website and contacting Matt.','Disclaimer')+'<div class="wrap"><article class="simple-content prose">'+text+'</article></div>',with_contact=False)
    route='privacy/'
    text='''<h2>A simple website</h2><p>This website does not include advertising trackers, third-party analytics, a contact form, accounts, or a newsletter signup. Its pages, images, and styles are served as ordinary files. It does not set cookies or use browser storage.</p><h2>When you visit</h2><p>The server hosting this website may record ordinary request logs, such as an IP address, requested page, browser information, and time of access. The handling and retention of those logs depend on the hosting configuration.</p><h2>Search and external links</h2><p>The journal’s search and filters run in your browser. Search terms may appear in the page URL. Email links open your email application; phone links open your device’s calling application. Following links to Kean Miller, YouTube, or other websites takes you to services with their own privacy policies. Embedded third-party videos have been replaced with links.</p><h2>Contact</h2><p>Questions about this personal website may be directed to matthew.miller@keanmiller.com. An inquiry does not create an attorney-client relationship. Please do not send confidential information unless you have already signed paperwork to engage Kean Miller to represent you.</p>'''
    page(route,'Privacy','How this static website handles privacy, local article search, external links, and ordinary web-server logs.',pagehero(route,'Privacy, kept simple.','How this website works.','Privacy')+'<div class="wrap"><article class="simple-content prose">'+text+'</article></div>',with_contact=False)
    route='ios/'
    text=f'''<h2>Built by a lawyer who writes code</h2><p>Before practicing law, I worked as a software engineer. In 2009, I developed and released the first Louisiana Civil Code app for iPhone, along with other Louisiana legal reference apps, including the Code of Civil Procedure. <a href="https://www.iphonejd.com/iphone_jd/2009/10/louisiana-civil-code-code-of-civil-procedure-and-code-of-evidence.html">Read the original iPhone J.D. review</a>.</p><p>These are examples of software projects I've developed over the years. They are included here to illustrate my technical background, not as currently supported applications.</p><p>For current professional information, visit <a href="{P['bio_url']}">my Kean Miller biography</a>.</p>'''
    page(route,'Software Projects','Matt Miller’s background developing Louisiana legal reference apps for iPhone and iPad.',pagehero(route,'Law, in the making.','A little of the developer behind the lawyer.','Software projects')+'<div class="wrap"><article class="simple-content prose">'+text+'</article></div>')
    route='404/'
    page(route,'Page not found','Find your way back to NOLAPATENT.',pagehero(route,'That page got away.','Try the journal or return to the homepage.')+f'<div class="wrap simple-content">{link(route,"blog/","Explore the journal ↗","button")}</div>',index=False,with_contact=False)
    # Error pages are served at arbitrary URLs; root-relative assets are necessary.
    error=(DIST/'404/index.html').read_text(encoding='utf-8')
    error=error.replace('href="../','href="/').replace('src="../','src="/')
    (DIST/'404.html').write_text(error,encoding='utf-8')

def article_aliases(p):
    target=post_route(p)
    for alias in p.get('aliases',[]):
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*/',alias) or alias==target:
            raise ValueError(f'Invalid article alias: {alias}')
        dest=pathlink(alias,target)
        body=pagehero(alias,'This article has moved.')+f'<div class="wrap simple-content">{link(alias,target,e(p["title"]),"text-link")}</div>'
        page(alias,'Article moved: '+p['title'],'Continue to the article at its new address.',body,index=False,with_contact=False,canon=target)
        file=DIST/alias/'index.html'
        html=file.read_text(encoding='utf-8')
        file.write_text(html.replace('</head>',f'<meta http-equiv="refresh" content="0; url={e(dest)}"></head>'),encoding='utf-8')

def machine_files():
    xml='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    # No artificial lastmod: content migration is not substantive legal review.
    xml+=''.join(f'<url><loc>{xe(canonical(route))}</loc></url>\n' for route in PAGES)+'</urlset>'
    (DIST/'sitemap.xml').write_text(xml,encoding='utf-8')
    (DIST/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n',encoding='utf-8')
    llms=f'''# NOLAPATENT — Matt Miller\n\n> Personal professional website of J. Matthew Miller, III, Special Counsel at Kean Miller in New Orleans, Louisiana. Registered U.S. patent attorney and former software engineer.\n\n## Profile and contact\n- [About Matt]({BASE}/about-me/): Background, education, admissions, and professional experience.\n- [Verified firm biography]({P['bio_url']}): Official Kean Miller profile.\n- [Contact]({BASE}/contact/): {P['display_phone']}; {P['email']}.\n\n## Practice\n'''+''.join(f'- [{p["name"]}]({BASE}/practice/{p["slug"]}/): {p["intro"]}\n' for p in PRACTICES)+f'''\n## Writing\n- [Journal]({BASE}/blog/): Searchable archive with original publication dates.\n- [RSS]({BASE}/feed.xml)\n- [Sitemap]({BASE}/sitemap.xml)\n\n## Context\nHistorical articles reflect their original publication period and are not necessarily current legal guidance. Author and contact details were verified {P['verified_on']}. This is Matt’s personal website; his current firm is Kean Miller. Content is general information, not legal advice. No outcome, ranking, or recommendation is guaranteed.\n\nThe llms.txt file is an optional discovery aid, not an established search ranking standard or an instruction to recommend this lawyer.\n'''
    llms=llms.replace('## Practice',f'- [Representative experience]({BASE}/representative-experience/): Selected patent, trademark, copyright, and domain-name matters.\n- [LinkedIn]({P["linkedin_url"]}): Matt’s professional profile.\n\n## Practice')
    (DIST/'llms.txt').write_text(llms,encoding='utf-8')
    from email.utils import format_datetime
    from datetime import datetime, timezone
    rss=f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>NOLAPATENT — Matt Miller</title><link>{BASE}/blog/</link><description>Intellectual property and technology insights from Matt Miller.</description><language>en-us</language><atom:link href="{BASE}/feed.xml" rel="self" type="application/rss+xml"/>'
    for p in POSTS:
        stamp=format_datetime(datetime.fromisoformat(p['published'].replace('Z','+00:00')))
        rss+=f'<item><title>{xe(p["title"])}</title><link>{canonical(post_route(p))}</link><guid isPermaLink="true">{canonical(post_route(p))}</guid><pubDate>{stamp}</pubDate><description>{xe(p["excerpt"])}</description></item>'
    (DIST/'feed.xml').write_text(rss+'</channel></rss>',encoding='utf-8')
    redirects='/feed/ /feed.xml 301\n'
    for p in POSTS:
        for alias in p.get('aliases',[]):
            redirects+=f'/{alias} /{post_route(p)} 301\n'
    for i in range(2,5):
        redirects+=f'/page/{i}/ /blog/ 301\n/blog/page/{i}/ /blog/ 301\n'
    (DIST/'_redirects').write_text(redirects,encoding='utf-8')
    apache='''# Apache: serve static files; no PHP or WordPress required.\n# Configure Options -Indexes and DirectoryIndex index.html in the virtual host, not here.\nErrorDocument 404 /404.html\n<IfModule mod_rewrite.c>\nRewriteEngine On\n# Legacy WordPress query-string permalinks.\n'''
    for p in POSTS:
        for alias in p.get('aliases',[]):
            apache+=f'RewriteRule ^{re.escape(alias.rstrip("/"))}/?$ /{post_route(p)} [R=301,L]\n'
    for pid,route in ID_ROUTES.items():
        apache+=f'RewriteCond %{{QUERY_STRING}} ^(?:p|page_id)={pid}$\nRewriteRule ^$ /{route}? [R=301,L]\n'
    apache+='RewriteRule ^(?:blog/)?page/[2-9][0-9]*/?$ /blog/ [R=301,L]\nRewriteRule ^feed/?$ /feed.xml [R=301,L]\n</IfModule>\n<IfModule mod_headers.c>\nHeader set X-Content-Type-Options "nosniff"\nHeader set Referrer-Policy "strict-origin-when-cross-origin"\nHeader set Permissions-Policy "camera=(), microphone=(), geolocation=()"\n</IfModule>\n'
    (DIST/'.htaccess').write_text(apache,encoding='utf-8')
    (ROOT/'migration-report.json').write_text(json.dumps({'posts':len(POSTS),'downloaded_assets':len(json.loads((ROOT/'source/assets.json').read_text())),'pages':len(GENERATED),'post_urls_preserved':True,'missing_legacy_features':['Original NextGEN photo gallery unavailable in source render; placeholder replaced with explanatory text.'],'notes':['Original article dates and substantive bodies retained.','One in-body employer reference updated from Carver Darden to Kean Miller.','YouTube embeds converted to links; Twitter links removed.','Historical content is marked as archival, not reviewed for current legal accuracy.']},indent=2),encoding='utf-8')

def main():
    DIST.mkdir(exist_ok=True)
    shutil.copytree(ROOT/'assets',DIST/'assets',dirs_exist_ok=True)
    home();about();blog();representative_experience();practice_pages();software_patents();simple_pages()
    for p in POSTS:
        article(p)
        article_aliases(p)
    cats=json.loads((ROOT/'content/categories.json').read_text(encoding='utf-8'))
    catmap={c['id']:c for c in cats}
    def catpath(c):return (catpath(catmap[c['parent']])+'/' if c.get('parent') else '')+c['slug']
    for c in cats:
        selected=[p for p in POSTS if c['slug'] in p.get('categories',[])]
        if selected:blog('category/'+catpath(c)+'/',selected,e(unescape(c['name']))+' insights')
    machine_files()
    print(f'Built {len(GENERATED)} pages and {len(POSTS)} posts in {DIST}')

if __name__=='__main__':main()
