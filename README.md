# NOLAPATENT static website

A local, responsive replacement for Matt Miller’s WordPress website. The published website is plain HTML, CSS, JavaScript, and images. It needs no PHP, WordPress, database, package installation, CDN, or build tools on the web server.

## Open it locally

Double-click **Open Website.cmd**, or open **dist/index.html** in your browser. Links, article search, topic filters, and mobile navigation also work directly from the filesystem.

For a local HTTP preview, double-click **Preview Website.cmd**, then visit **http://127.0.0.1:8000/**. Keep the preview window open; press Ctrl+C to stop it. The preview binds only to your own computer. It uses the existing Codex Python runtime when available, falling back to `python`.

## What is included

- Scrollable homepage introducing Matt, his technical background, practice areas, writing, and contact information.
- Updated Kean Miller portrait, biography, direct telephone, email, and New Orleans office address.
- All 33 published WordPress posts, with their original slugs and publication dates.
- A different, subject-specific author note on every migrated article.
- Searchable and filterable journal, four practice pages, representative experience page, profile, contact page, project history, disclaimer, privacy page, and legacy category pages.
- Eighteen representative matters sourced from the October 11, 2025 archived professional biography, with current affiliation and contact details kept separate from that historical source.
- LinkedIn profile links and locally served historical Tesla and Bell patent drawings with captions and sources.
- Semantic HTML, responsive layouts, keyboard navigation, skip link, reduced-motion support, print styling, local images, and system fonts.
- Canonical URLs, descriptions, Open Graph previews, JSON-LD, sitemap, RSS, robots.txt, and an optional llms.txt.
- Apache configuration and a static-host redirect file for old feed and pagination routes.

The `dist` directory is the entire deployable website. The source archive stays outside it.

## Edit and rebuild

Edit biography/contact facts in `content/profile.json`, article metadata in `content/posts.json`, article bodies in `content/posts/*.html`, and selected matters in `content/representative-experience.json`. Shared templates live in `scripts/build.py`; visual styles and interactions live in `assets/site.css` and `assets/site.js`.

Double-click **Build Website.cmd** after changes. The normal build uses only the Python standard library and works offline. It regenerates navigation, related articles, author notes, JSON-LD, the feed, and sitemap. Do not edit generated `dist` files as the primary source.

`scripts/prepare_content.py` and `scripts/import_wordpress.py` are one-time migration tools. **Do not rerun them when adding posts**: prepare_content regenerates imported content from the original export. The original cached WordPress data is retained in `source/` for reference. Migration/QA tools use the bundled lxml and Pillow libraries; the normal build does not.

## Add an article with Codex

See **CONTENT_GUIDE.md**. A future request can be as simple as:

> Add a post to this NOLAPATENT site about [topic]. Follow CONTENT_GUIDE.md, verify legal statements against primary sources, write a unique and relevant author note, and rebuild the static website. Keep it local.

The included `post-template.json` is an unlisted template, not a published article. To use it, copy it to a new JSON file, replace its fields with the reviewed post, and run:

```powershell
python scripts/add_post.py path-to-reviewed-post.json
python scripts/build.py
```

Posts require no server-side code. New posts are not labeled as archival. When substantially updating an old post, review the entire article, set `archived` to false, and add an accurate `modified` ISO timestamp. Do not merely refresh a date to make old legal analysis appear current.

## Validation

```powershell
python scripts/check.py
```

Checks cover every local HTML link/fragment, original post coverage, unique titles and author notes, image dimensions/alt attributes, descriptions, canonical tags, structured-data JSON, and feed/sitemap XML. The bundled browser check (`scripts/browser-check.cjs`) also checks desktop/mobile layouts, navigation, filters, empty states, query persistence, the 404 response, and direct-file navigation using the Codex Playwright runtime.

Screenshots from the browser review are saved in `qa/`. The migration record is `migration-report.json`.

## Publication later

### GitHub and server updates

The project repository is `https://github.com/UnlicensedDoctorTiki/nolapatent`. Both the editable source and the generated `dist/` website are versioned. Temporary files, QA screenshots, and ZIP packages are excluded.

After editing, run the build and checks locally, then commit and push the source changes together with the regenerated `dist/` files. The server does not need Python or a build step.

For a server with Git and SSH access, clone the repository outside the public web directory and configure the web server's document root to point to the checkout's `dist/` directory. A private repository requires GitHub authentication; a read-only deploy key can give the server access. Do not serve the repository root, because it also contains source files and Git metadata.

After the initial clone and web-server configuration, run this command inside the server checkout to publish subsequent pushed updates:

```sh
git pull --ff-only
```

Keep the server checkout free of manual edits; make changes here and push them through GitHub. This repository connection does not itself change the live hosting or DNS.

### Manual upload

Nothing has been published or changed on the existing website. Read **LAUNCH_NOTES.md** before replacing it. Upload the *contents* of `dist/` to the new web root. This includes `.htaccess` on Apache, or `_redirects` on a host that supports that format. Some file managers hide dotfiles.

The website’s canonical address is `https://www.nolapatent.com`. For a different final domain, change `base_url` in the profile and rebuild. Avoid indexing a duplicate staging copy: keep it private or use host-level access protection.

## Known migration limit

The Southern Food and Beverage Museum post depended on an old NextGEN gallery. Its gallery was not available in the public page rendering or REST export. The text is retained with a short explanation. All 41 referenced downloadable assets collected by the importer were saved successfully. Existing legal analysis was migrated as an archive, not independently reverified as current law.
