# NOLAPATENT: a lawyer's website, back to static HTML

**The source and generated website for [www.nolapatent.com](https://www.nolapatent.com), maintained by [Matt Miller](https://github.com/UnlicensedDoctorTiki/) with Codex.**

I'm J. Matthew Miller, III, a registered U.S. patent attorney and Special Counsel at [Kean Miller](https://www.keanmiller.com/team/j-matthew-miller-iii/) in New Orleans. Before becoming a lawyer, I was a software engineer. This project brings those two parts of my background together: a website for my intellectual property practice, built from files I can understand, inspect, and edit.

The site replaces an aging WordPress installation with plain HTML, CSS, JavaScript, and images. Its purpose is to introduce my practice, explain how my development experience informs my legal work, preserve my articles, and give readers a useful way to explore patents, trademarks, copyright, software contracts, licensing, and open-source issues.

Read [There and Back Again: A Blog's Tale](https://www.nolapatent.com/there-and-back-again-a-blogs-tale/) for the reasoning behind this approach. The [article's source](content/posts/there-and-back-again-a-blogs-tale.html) is here too.

## How I use Codex to maintain the site

I've written code and HTML in Vim. Knowing how to edit a page isn't the difficult part; keeping every page, link, layout, and article listing in step takes time and attention. Blogging software used to manage those details for me. For this website, I now work with Codex, OpenAI's agentic coding system, to manage the underlying files directly.

I describe the design and functionality I want, supply and review content, inspect the results locally, and work with Codex to refine the implementation. Shared templates and a small Python build script keep repetitive work consistent. Codex can update the design across the site or turn reviewed article content into a complete page with the surrounding navigation, listings, and metadata.

The workflow is:

1. **Edit and review locally.** Change the content, templates, styles, or interactions with Codex and preview the result.
2. **Build and check.** Generate the complete static site in `dist/` and run the validation script.
3. **Push from Codex to GitHub.** Commit the editable source and generated website together, then push them to this repository.
4. **Pull on my Linux server.** Retrieve the latest commit and copy the contents of `dist/` into `/var/www/nolapatent/`.

The build happens before deployment. The production server serves ordinary files; it needs no WordPress installation, content database, PHP application, Python runtime, or package installation for this site. GitHub stores the project and its history; my Linux server hosts the website. A push to GitHub does not automatically deploy the website.

## What generates everything?

[`scripts/build.py`](scripts/build.py) is the offline generator. It uses the Python standard library to combine content and shared templates into the finished website. It generates:

- The homepage, biography, contact information, practice pages, and representative experience.
- A separate HTML file for each article, with its byline, relevant author note, reading time, related articles, and a table of contents when headings are present.
- Blog listings, topic archives, and a compact search index used in the reader's browser.
- Consistent headers, navigation, footers, and relative links that also work when opening the files locally.
- Page titles, descriptions, canonical links, Open Graph previews, and JSON-LD structured data.
- The RSS feed, XML sitemap, robots.txt, optional llms.txt, redirects, and 404 page.

The journal search runs in the visitor's browser against a generated index. It doesn't query a database or load every article into one hidden page. Semantic HTML and structured data make the content easier for readers, search engines, and other tools to understand; they don't guarantee rankings or recommendations.

## Where the files live

| Location | Purpose |
| --- | --- |
| `content/profile.json` | Current professional identity and contact information |
| `content/posts.json` | Article titles, dates, slugs, excerpts, topics, and unique author notes |
| `content/posts/*.html` | Article bodies, without the surrounding site layout |
| `content/representative-experience.json` | Selected patent, trademark, copyright, and domain-name matters |
| `scripts/build.py` | Shared page templates and the static-site generator |
| `assets/site.css` and `assets/site.js` | Responsive styles, navigation, and local search behavior |
| `assets/` | Local portraits, historical patent drawings, and article media |
| `dist/` | The complete generated website to deploy |
| `source/` | Cached migration material and notes supporting biographical and historical details |
| `CONTENT_GUIDE.md` | Voice, factual corrections, author notes, and future article workflow |
| `docs/github-profile.md` | Source text for the README displayed on my GitHub profile |

Edit the source and rebuild; don't use `dist/` as the primary place to make changes. Both source and output are versioned so the server can deploy a checked build without generating pages itself. Temporary files, QA screenshots, and ZIP packages are excluded from Git.

## Open and rebuild locally

On Windows, double-click **Open Website.cmd**, or open `dist/index.html` directly. Navigation, journal search, topic filters, and the mobile menu also work from the filesystem.

For an HTTP preview, double-click **Preview Website.cmd**, then visit `http://127.0.0.1:8000/`. It serves only `dist/` and binds to the local computer. Stop it with Ctrl+C when finished.

After making changes, double-click **Build Website.cmd**, or use Python:

```sh
python scripts/build.py
python scripts/check.py
```

The normal build uses only the Python standard library and works offline. The validation script additionally uses `lxml`; image preparation and some migration tools use Pillow. The Windows launchers can use the installed Codex runtime or fall back to `python`.

## Adding an article

I can bring a draft or finished text to Codex, review changes, and have it integrated with the site's existing design. The article body stays separate from the layout so adding content doesn't mean maintaining every surrounding HTML file by hand.

For example:

> Add this reviewed article to NOLAPATENT. Follow CONTENT_GUIDE.md, preserve my supplied wording, write a relevant and unique author note, and rebuild and check the site. Let me review the result locally before pushing.

To add a new article through the command line, copy `post-template.json`, fill in the metadata and reviewed HTML body, and run:

```sh
python scripts/add_post.py path-to-reviewed-post.json
python scripts/build.py
python scripts/check.py
```

See [CONTENT_GUIDE.md](CONTENT_GUIDE.md) for the full process. New articles use their actual publication dates. Historical posts keep their original dates; substantive revisions receive a modification timestamp. A biography or layout change alone isn't a substantive update to an old legal article.

`scripts/import_wordpress.py` and `scripts/prepare_content.py` are one-time migration tools. **Do not rerun them to add or edit posts:** the preparation script recreates imported content from the original export and can overwrite later edits.

## Deployment to my Linux server

The configured workflow keeps a repository checkout at `/var/www/nolapatent-repo` and serves the generated files from `/var/www/nolapatent`. The commands below assume Git, rsync, sudo access, and that any old website has already been moved out of the destination.

Set up the repository once:

```sh
sudo git clone https://github.com/UnlicensedDoctorTiki/nolapatent.git /var/www/nolapatent-repo
```

Install the site, or deploy later pushed updates, with:

```sh
sudo git -C /var/www/nolapatent-repo pull --ff-only && sudo rsync -rltp --delete --chmod=D755,F644 /var/www/nolapatent-repo/dist/ /var/www/nolapatent/
```

The trailing slash on `dist/` copies its contents, including `.htaccess`, directly into the web root. `--delete` removes destination files no longer present in the generated site, so `/var/www/nolapatent/` must be dedicated to this website. The command sets readable file and directory permissions. It doesn't change the server's virtual-host, DNS, or HTTPS configuration.

Serve only `/var/www/nolapatent/`, not the repository root. Make changes in the local source project and push them through GitHub rather than editing the server checkout. If the pull fails, the `&&` prevents the copy from running.

For a manual upload instead, copy the **contents** of `dist/` to the web root. Read [LAUNCH_NOTES.md](LAUNCH_NOTES.md) for hosting details. The canonical domain is `https://www.nolapatent.com`; change `base_url` in `content/profile.json` and rebuild if the domain changes.

## What is included and checked

The migration preserves 33 original WordPress posts at their original slugs and dates, alongside new writing. The site includes four practice pages, a biography, 18 representative matters, software project history, a searchable journal, current contact information, and historical Tesla and Bell patent drawings with captions and sources.

Each article has a distinct author note connecting the subject to relevant experience. Current affiliation and contact details are kept separate from historical article dates and past matters. The design uses local assets, system fonts, responsive layouts, keyboard navigation, a skip link, reduced-motion support, and print styles.

`scripts/check.py` checks local links and fragments, titles, metadata, image attributes, JSON-LD, RSS and sitemap XML, imported-post coverage, and unique author notes. `scripts/browser-check.cjs` supplies additional browser checks for desktop/mobile layouts, navigation, search, filters, empty states, and the 404 response. Browser tooling is used for development, not by the published website.

## Historical material and remaining limits

The Southern Food and Beverage Museum post relied on an old NextGEN photo gallery that was unavailable during migration. The original article text is retained with an explanatory note. The migration record is in `migration-report.json`; source notes document the representative matters, biography corrections, and historical drawings.

Archived legal articles reflect their original publication period and have not been independently updated unless expressly indicated. This is my personal website and project, not a statement of Kean Miller's views. General information on the site is not legal advice. Portraits, quotations, and historical media retain their respective source attributions.
