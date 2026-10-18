# Replacing the old WordPress site

## What the local version already does

The public pages contain complete HTML without requiring JavaScript to render the articles. Each has a description and canonical URL. The current lawyer is identified as a Person linked to the official firm biography. ProfilePage, BlogPosting, BreadcrumbList, WebSite, and Service structured data describe corresponding visible content. The profile, practice pages, bylines, topic-specific author notes, and contact links make the professional relationship clear to readers and machines.

`robots.txt` allows crawlers by default. It does not block ordinary search engines or AI search crawlers. Hosting firewalls, bot challenges, access protection, and DNS can still prevent access and must be checked after launch.

`llms.txt` offers a concise plain-text directory. It is an optional, emerging convention, not a proven ranking factor or a guarantee of AI citations or referrals. Google states that ordinary search fundamentals remain relevant for its AI features; there is no special markup required for inclusion. Structured data can help describe the website but does not guarantee rich results or rankings.

References: [Google AI features and websites](https://developers.google.com/search/docs/appearance/ai-features), [article structured data](https://developers.google.com/search/docs/appearance/structured-data/article), and [structured-data policies](https://developers.google.com/search/docs/appearance/structured-data/sd-policies).

## Before replacing production

Apache hosting note: the generated `.htaccess` leaves `Options` and `DirectoryIndex` to the server configuration. The current server rejects `Options` in `.htaccess` with a 500 error, and `DirectoryIndex` requires its own override permission. Configure `Options -Indexes` and `DirectoryIndex index.html` in the appropriate virtual-host `<Directory /var/www/nolapatent>` block if needed; the usual Debian index configuration already includes `index.html`. Do not add those directives back to the generated `.htaccess` or broaden `AllowOverride` just to make them work. Redirects, error documents, and headers still depend on the corresponding overrides being allowed.

1. Back up the old WordPress files and database. The public API export in this project is a migration source, not a complete server backup.
2. Review the homepage, professional biography, disclaimer, privacy text, office details, and author notes. The disclaimer was rewritten for the current affiliation; it is draft website copy for Matt to review before public use. If the host adds analytics, forms, cookies, or third-party services, update the privacy page to match.
3. Decide which historical legal posts need substantive updates. Their archive notices intentionally prevent readers from mistaking the original analysis for a current review. The 2024 FTC noncompete post, DMCA material, and AI/copyright discussions are examples where current status deserves attention before active promotion.
4. Configure HTTPS and choose `https://www.nolapatent.com` as the canonical hostname. Configure the host to redirect HTTP and non-www requests to that address. The included files do not assume how a future host terminates TLS.
5. Upload only the contents of `dist/` to a clean document root. Remove or deactivate old WordPress entry points as part of the actual server migration; copying static files on top of a vulnerable installation does not remove WordPress.
6. Preserve exact post slugs and trailing-slash directory routes. `.htaccess` supports WordPress `?p=ID` and `?page_id=ID` routes on Apache. Other hosts need equivalent query-string redirects. `_redirects` covers feed/pagination redirects on compatible static hosts. New server software may require its own configuration; do not assume these files apply everywhere.
7. Ensure unknown paths return a real 404 status and display `404.html`. Confirm caching, compression, and bot access on the actual host.
8. Verify representative original URLs, images, the current contact page, RSS, sitemap, canonicals, and structured data at the public domain. Use Google’s Rich Results Test and Search Console after deployment; the local checks do not establish search eligibility or indexing.
9. Submit the sitemap in Google Search Console and Bing Webmaster Tools. Check for crawl errors and whether canonical pages are indexed.

## Building the marketing value over time

Keep contact and biographical details consistent with Kean Miller’s official profile and any professional directories Matt maintains. Publish specific, useful commentary from his own technical and legal experience. Add relevant internal links between new posts and practice pages, and keep old articles current when they continue attracting readers. Periodically review genuine inquiries and search queries to identify what prospective clients need.

No page, schema field, footer variation, or crawler file can compel an AI system to recommend a lawyer. The site supplies accessible, consistent, evidence-backed information so people and search systems can evaluate Matt’s relevant experience.
