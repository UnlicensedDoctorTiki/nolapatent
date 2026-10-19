"""Exercise adding a new post in an isolated copy without changing real content."""
import json, shutil, subprocess, sys, tempfile, zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
(ROOT/'qa').mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix='post-workflow-',dir=ROOT/'qa') as work:
    stage=Path(work)
    shutil.copytree(ROOT/'content',stage/'content')
    shutil.copytree(ROOT/'assets',stage/'assets')
    shutil.copytree(ROOT/'source',stage/'source')
    (stage/'scripts').mkdir()
    for name in ['add_post.py','build.py','structured_data.py','check.py','check_structured_data.py']:
        shutil.copy2(ROOT/'scripts'/name,stage/'scripts'/name)
    post={'slug':'workflow-verification-article','title':'A new article workflow verification','date':'2026-10-17','published':'2026-10-17T12:00:00-05:00','topic':'Patents','excerpt':'A local test of the future publishing workflow.','author_note':'This temporary test note is unique and is never published to the real website.','body_html':'<p>A new article body.</p><h2>A useful section</h2><p>See the <a href="https://www.nolapatent.com/practice/patents/">patent practice page</a>.</p>'}
    template=stage/'new.json'
    template.write_text(json.dumps(post),encoding='utf-8')
    for command in [['add_post.py',str(template)],['build.py'],['check.py']]:
        result=subprocess.run([sys.executable,str(stage/'scripts'/command[0]),*command[1:]],capture_output=True,text=True)
        if result.returncode:raise SystemExit(result.stdout+result.stderr)
    article=(stage/'dist'/post['slug']/'index.html').read_text(encoding='utf-8')
    assert 'class="archive-notice"' not in article,'New post incorrectly marked archival'
    assert post['slug'] in (stage/'dist/index.html').read_text(encoding='utf-8'),'New post missing from homepage'
    assert post['slug'] in (stage/'dist/feed.xml').read_text(encoding='utf-8'),'New post missing from RSS'
    assert post['slug'] in (stage/'dist/sitemap.xml').read_text(encoding='utf-8'),'New post missing from sitemap'
    duplicate=subprocess.run([sys.executable,str(stage/'scripts/add_post.py'),str(template)],capture_output=True,text=True)
    assert duplicate.returncode!=0,'Duplicate slug should be rejected'
print('PASS: new post creation, complete rebuild, homepage promotion, non-archive rendering, local links, RSS/sitemap, and duplicate-slug rejection in isolated copy.')
archive=ROOT/'nolapatent-static.zip'
if archive.exists():
    with zipfile.ZipFile(archive) as package:
        names={name.replace('\\','/') for name in package.namelist()}
        assert '.htaccess' in names,'Deployable archive is missing .htaccess'
        assert 'index.html' in names,'Deployable archive has wrong root'
    print('PASS: deployable ZIP includes homepage and Apache configuration at root.')
