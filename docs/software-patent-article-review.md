# Software patent article — implementation and editorial review

Prepared October 19, 2026. Matt authorized publication to GitHub on October 19, 2026. The article and integration changes are approved for the repository push. Production deployment still requires running the existing Linux update script.

## Article and scope

- Title/H1: **Can Software Be Patented? A Software Patent Attorney Explains**.
- Intended canonical URL: **https://www.nolapatent.com/blog/can-software-be-patented/**.
- Generated review copy: `dist/blog/can-software-be-patented/index.html`.
- HTML title follows the existing blog convention, appending `| Matt Miller · NOLAPATENT`.
- Description: “Can software be patented in the United States? Matt Miller explains eligibility, technical disclosure, current USPTO guidance, and what inventors should prepare.”
- Approximately 1,960 words, seven substantive sections, about nine minutes’ reading time.

The 34 existing article titles and bodies were inspected for overlap. The closest article, *AI and Patent Law: Navigating the New Frontier* (September 27, 2024), discusses an AI presentation, inventorship, and the July 2024 guidance/examples. The new article addresses software eligibility generally, drafting and disclosure, illustrative technologies, current examination materials, and an inventor preparation checklist. The existing article is preserved as historical content.

No design, navigation, CSS, JavaScript, shared identity/schema definitions, or existing article text was changed. Existing post metadata and routes were compared against the repository baseline and are identical. Normal rebuilds update featured/related article cards to include the new article; those generated changes do not revise the historical articles themselves.

## Legal and editorial points for Matt’s review before publication

1. **Eligibility explanation (sections 1–2).** Review the plain-language summary of Alice/Mayo and the USPTO’s Steps 1, 2A, and 2B. The discussion distinguishes eligibility from novelty, nonobviousness, and disclosure. The USPTO’s practical-application inquiry is described as examination guidance, without suggesting that commercial usefulness or industry limitations alone establish eligibility. Confirm the level of simplification is appropriate for your audience.
2. **Technical disclosure and examples (sections 3–4).** Review the explanation of written description, enablement across claim scope, and the five hypothetical software examples. They are expressly illustrations for investigation, not eligibility findings, representative matters, or assurances of issuance. This article does not undertake a full § 112(f) or functional-claim analysis.
3. **2025–2026 updates (section 5).** Confirm your characterization of the December 2025 *Desjardins* notice and the April/September 2026 SMED materials. The article distinguishes the April memorandum superseding the December 2025 applicant best-practices memorandum from the separate December 2025 examiner memorandum, which remains linked. The September 29 supplement introduces no new procedure. Evidence cannot replace disclosure required at filing. Agency guidance is distinguished from controlling court precedent.
4. **Disclosure timing and intake (section 6).** Review the limited summary of inventor-originated U.S. disclosure exceptions and the risk to foreign rights. It does not offer a blanket one-year grace period for all events. Specific public uses, sales, disclosures, priority support, and foreign law require individual analysis. Your exact engagement/confidentiality warning appears before the final practice discussion and in the existing contact panel.
5. **First-person voice and experience (introduction and section 7).** Confirm the drafting/prosecution observations reflect your preferred voice. Credentials and the two descriptions of work as counsel come from existing verified site material and your firm biography; the article separates client prosecution matters from your three inventor patents. No clients, results, anecdotes, or new representative matters were invented.

These review flags are outside the public article. The public article contains the normal general-information notice.

## Primary authorities checked

All sources below were checked on October 19, 2026. Links appear next to the corresponding legal discussion in the article.

- [Alice Corp. v. CLS Bank International, 573 U.S. 208 (2014)](https://www.govinfo.gov/content/pkg/USREPORTS-573/pdf/USREPORTS-573-208.pdf): Supreme Court framework and generic-computer implementation.
- [MPEP § 2106](https://www.uspto.gov/web/offices/pac/mpep/s2106.html): statutory categories, exceptions, USPTO analysis, and technological improvements.
- [August 4, 2025 eligibility memorandum](https://www.uspto.gov/sites/default/files/documents/memo-101-20250804.pdf): mental processes, whole-claim analysis, and improvements.
- [December 5, 2025 Desjardins MPEP notice](https://www.uspto.gov/sites/default/files/documents/memo-desjardins.pdf): disclosed improvements and their reflection in the claims.
- [April 30, 2026 SMED applicant memorandum](https://www.uspto.gov/sites/default/files/documents/smeds-application-practitioners-4302026.pdf) and [official issuance announcement](https://www.uspto.gov/subscription-center/2026/updated-smed-best-practices-memorandum-issued): superseding applicant best-practices guidance.
- [September 29, 2026 SMED supplement](https://www.uspto.gov/sites/default/files/documents/smeds-memo-20260929.pdf): optional declarations, focused evidence, timing, and analysis flowchart.
- [December 4, 2025 SMED examiner memorandum](https://www.uspto.gov/sites/default/files/documents/smeds-corps.pdf): nexus to the claims and limits on supplementing disclosure.
- [2024 Examples 47–49](https://www.uspto.gov/sites/default/files/documents/2024-AI-SMEUpdateExamples47-49.pdf): still listed among the USPTO’s current examples; illustrative claim differences, including network security.
- [MPEP § 2151](https://www.uspto.gov/web/offices/pac/mpep/s2151.html), [§ 2141](https://www.uspto.gov/web/offices/pac/mpep/s2141.html), [§ 2161.01](https://www.uspto.gov/web/offices/pac/mpep/s2161.html), and [§ 2164](https://www.uspto.gov/web/offices/pac/mpep/s2164.html): distinct patentability and disclosure requirements.
- [MPEP § 2153](https://www.uspto.gov/web/offices/pac/mpep/s2153.html) and [USPTO international-filing guidance](https://www.uspto.gov/patents/basics/international-protection/filing-patents-abroad): disclosure exceptions and foreign-filing risks.
- [USPTO current eligibility materials](https://www.uspto.gov/patents/laws/examination-policy/subject-matter-eligibility): checked for subsequent guidance through the preparation date.
- [Kean Miller biography](https://www.keanmiller.com/team/j-matthew-miller-iii/): current position, location, patent and engineering experience. Duke degree wording follows Matt’s direct correction: one B.A., Computer Science and Psychology.

## Links and machine-readable integration

- The software patent practice page has one new contextual link, under its eligibility heading, to the new article.
- The new article links to the software patent practice page, About Matt, representative experience at `#patents`, contact page, and official firm biography.
- Existing blog index, homepage featured articles, relevant category archives, practice cards, and related-article cards pick up the new post through the existing generator.
- Sitemap and RSS include the canonical `/blog/can-software-be-patented/` URL. Robots policy is unchanged; the page has `index, follow` and a self-referencing canonical.
- Server-delivered JSON-LD contains the existing WebPage/BlogPosting graph, connected to **https://www.nolapatent.com/#matt-miller**. Publication timestamp comes from this local preparation’s metadata; no unsupported modification date was added.
- Minimal optional `route` metadata supports this nested blog URL. Existing posts omit it and retain their original URLs. All cards, RSS, canonical URLs, schema IDs, and generated redirect targets honor it. The importer rejects paths outside the existing root convention or `blog/{slug}/`.

## Verification

- `scripts/build.py`: generated 67 regular pages/redirects and 35 posts; including the copied root 404 document there are 68 HTML files.
- `scripts/check.py`: PASS, all 68 HTML files, local links/fragments, unique titles, JSON-LD vocabulary/identity references, sitemap and RSS.
- `scripts/workflow-check.py`: PASS, isolated new nested-post import, rebuild, homepage/RSS/sitemap integration, duplicate rejection, and unsafe-route rejection. Existing root-level posts remain covered by the complete site check.
- Preservation comparison: all 34 pre-existing article bodies and metadata match the baseline.
- Local HTTP GET at the intended path: **200**, substantive content in response HTML; canonical, robots, sitemap, feed, and normal hyperlinks checked.
- Desktop 1280 × 900 and phone 390 × 844: typography, section navigation, byline, and reading layout checked; no horizontal overflow at phone width.
- Schema.org Validator, generated JSON-LD snippet: **0 errors, 0 warnings**. BlogPosting is connected as the WebPage’s main entity; automated checks also verify the BlogPosting type, author ID, canonical ID, headline, and metadata dates.
- Proof files are under ignored `qa/software-patent-article-*`; these are local QA records, not deployed assets.

No production deployment has been performed for this article. The existing Linux update script remains the server deployment step after the authorized repository push.

## Files changed

Source and tooling:

- `content/posts/can-software-be-patented.html` — new article body.
- `content/new-posts/can-software-be-patented.json` — reproducible import source with metadata and body.
- `content/posts.json` — one new post entry.
- `content/pages/software-patents.html` — one contextual article link.
- `scripts/build.py` — optional nested post routes in existing output paths and links.
- `scripts/add_post.py` — validated optional route support.
- `scripts/check.py` and `scripts/check_structured_data.py` — check actual post routes.
- `scripts/workflow-check.py` — exercise nested import and reject unsafe paths.
- `CONTENT_GUIDE.md` — document the optional route field.
- `docs/software-patent-article-review.md` — this review and implementation report.
- `migration-report.json` — regenerated page/post totals.

Generated public outputs are listed below. Existing article file changes contain automatic related-card updates only.

- `dist/.htaccess`
- `dist/455-2/index.html`
- `dist/ai-and-patent-law-navigating-the-new-frontier/index.html`
- `dist/aint-dere-no/index.html`
- `dist/blog/can-software-be-patented/index.html`
- `dist/blog/index.html`
- `dist/brand-important/index.html`
- `dist/category/patent/index.html`
- `dist/category/technology/software/index.html`
- `dist/federal-trade-commission-crackdown-on-non-compete-agreements/index.html`
- `dist/feed.xml`
- `dist/index.html`
- `dist/inventors-are-shocked-at-this-one-little-trick-that-patent-examiners-use/index.html`
- `dist/is-chatgpt-fair-use/index.html`
- `dist/louisiana-state-trademark-registration/index.html`
- `dist/practice/patents/index.html`
- `dist/practice/software-patents/index.html`
- `dist/sitemap.xml`
- `dist/turkey-thermometer-patent/index.html`
- `dist/were-attorneys-not-businessmen/index.html`
- `dist/why-the-best-patent-strategy-doesnt-stop-at-allowance/index.html`
