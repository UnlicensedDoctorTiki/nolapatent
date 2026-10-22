# Professional recognition — local approval package

Prepared October 22, 2026. **The user authorized a GitHub push on October 22; live website deployment and email submission have not been performed.** No external approval is recorded. The user will handle production deployment after the necessary approvals.

## Presentation

- **Homepage:** a prominent text-based recognition row below the existing credentials strip, which follows the hero. The whole row links to Matt’s official Best Lawyers profile. It includes Best Lawyers® as plain, nonitalic company-name text, the italicized publication name, 2027 edition, Patent Law and Copyright Law, and New Orleans, Louisiana, United States. Super Lawyers appears nowhere in the homepage HTML.
The homepage row uses the site’s serif typography, open spacing, fine divider rules, and a simple profile arrow.

- **About Me:** a Professional Recognition section immediately before Education and admissions. Two entries appear side by side on desktop and stack on mobile. “Current recognition” identifies the 2027 Best Lawyers edition; “Historical recognition” identifies the 2016–2019 Rising Stars selection. Publication names are italicized; both titles link to official profiles.
- **Assets:** no licensed official badge/logo or express permission covering this website was provided or located in the project. No proprietary graphics were downloaded, imitated, or used. The treatment is ordinary HTML text using the existing site fonts and restrained colors. If an official asset is later proposed, obtain and verify permission covering this use and the applicable license period before replacing this treatment.

## Sources checked

- [Best Lawyers publicizing guidelines](https://www.bestlawyers.com/methodology/publicizing-guidelines): read before implementation, including marks, publication formatting, country/year/practice identification, profile links, graphics licensing, and prior approval. The text does not characterize Matt as “the best lawyer,” claim Lawyer of the Year recognition, compare skill, guarantee results, or suggest endorsement.
- [Official Best Lawyers profile](https://www.bestlawyers.com/lawyers/j-matthew-miller-iii/321008): confirms The Best Lawyers in America® 2027, Patent Law, Copyright Law, and New Orleans, Louisiana.
- [Official Super Lawyers profile](https://profiles.superlawyers.com/louisiana/new-orleans/lawyer/j-matthew-miller-iii/7936c2c6-c25d-44eb-89f1-3d256264e30f.html): confirms Intellectual Property and Rising Stars selection in 2016–2019.
- [Kean Miller biography](https://www.keanmiller.com/team/j-matthew-miller-iii/): independently lists the 2027 Best Lawyers and 2016–2019 Rising Stars recognitions.
- [LSBA advertising guidance](https://www.lsba.org/PracticeAidGuide/PAG9.aspx) and [advertising resources](https://www.lsba.org/LawyerAdvertising/): distinguish website filing exemptions from the continuing obligation to comply with content rules. The LSBA-linked [LADB rule compilation](https://www.ladb.org/docs/Publication/ROPC/ROPC.pdf) identifies amendments through May 10, 2023; it is not treated here as proof that no later amendments exist.

## Approval and compliance still needed

1. Matt/Kean Miller should review the final treatment against the currently applicable Louisiana rules, including accuracy, award characterizations, office/licensure disclosures, and any subsequent amendments. Existing notices and disclosure pages remain intact. No Louisiana compliance opinion or LSBA evaluation has been obtained. For a website-only change, confirm the applicable exemption rather than assuming that a non-exempt advertisement filing is required. Reuse in other advertising media requires a separate assessment.
2. After that review, send `email-draft.txt` to **admaterials@bestlawyers.com** with the four screenshots and `proposed-copy.txt`. Best Lawyers requests approval of promotional materials using its name before public release; obtain written approval and incorporate any requested changes.
3. Matt authorized the repository push on October 22. Production deployment remains pending and separate from that push. No external approval has been received by Codex, and no hosted website preview was created; the preview runs locally.

## Preview materials

- `homepage-desktop.jpg` — homepage recognition row and credentials strip in desktop context.
- `homepage-mobile.jpg` — recognition panel at phone width.
- `about-recognition-desktop.jpg` — current and historical entries together, followed by credentials.
- `about-recognition-mobile.jpg` — stacked entries at phone width.
- `proposed-copy.txt` — accessible text of both treatments and profile destinations.
- `email-draft.txt` — short approval request; not sent.

These materials are outside `dist` and are not served by the website. A convenience ZIP named `recognition-approval-materials.zip` is available in the project root. It contains only this review package, not deployable website files.

## Implementation and preservation

- `content/recognitions.json` — verified recognition facts and source-profile URLs in one reusable data file.
- `scripts/build.py` — adds the homepage panel and About section using that data.
- `assets/site.css` — scoped recognition and card styles and a mobile stacking breakpoint. Existing selectors and navigation behavior are unchanged.
- Generated outputs changed: `dist/index.html`, `dist/about-me/index.html`, and `dist/assets/site.css`.
- Approval materials added under `docs/recognition-approval/` as listed above, plus this report.

SEO titles, descriptions, canonicals, JSON-LD, shared Person identity, sitemap, RSS, URLs, existing page text, and existing links are unchanged. The optional Person recognition update was not needed for this limited visible treatment; keeping the graph unchanged also avoids distributing the historical Rising Stars entry onto other pages.

## Validation

- Normal build and `scripts/check.py`: PASS, all 68 HTML pages, local links and fragments, unique titles, JSON-LD vocabulary/identity checks, RSS, and sitemap.
- `scripts/workflow-check.py`: PASS, isolated new-post import/build/check flow, homepage promotion, nested routes, RSS/sitemap integration, and invalid/duplicate route rejection with the new recognition data file included.
- Preservation check: existing homepage and About text/links match the baseline after removing only the added sections. Their head metadata and JSON-LD are identical. No unrelated HTML output changed.
- Both treatments are readable server-delivered HTML. No third-party scripts, widgets, trackers, fonts, or new runtime dependencies were added.
- Desktop and phone layouts inspected; neither overflows horizontally. Registered symbols, italicized publication names, recognition dates, location, practice areas, and profile links were checked.
- Local QA details are saved in ignored `qa/recognition-validation.json`.

Technical checks do not constitute brand approval or Louisiana advertising clearance.
