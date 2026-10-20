# Targeted editorial cleanup — October 20, 2026

Implemented in content sources and the existing Python templates, then rebuilt `dist`. Matt authorized the GitHub push on October 20, 2026. Production deployment still requires running the existing Linux update script.

## Page-by-page summary

| Page | Changes |
| --- | --- |
| Homepage `/` | Replaced the practice heading and introduction; simplified the Tesla/Bell explanation; changed the FAQ label to “Common questions.” and used all five supplied first-person questions and answers. Kept the patent illustrations and all existing links. |
| About `/about-me/` | Used “Why my software background matters.” and “My experience as a software engineer.” Removed the verification-date paragraph. Existing Kean Miller and LinkedIn profile links remain. |
| Patents `/practice/patents/` | H1 is “Patent Prosecution and Litigation”. HTML title is “Patent Attorney in New Orleans” with the existing suffix. Used the supplied litigation and invention paragraphs and the “Understanding the invention” heading. |
| Software patents `/practice/software-patents/` | Used the supplied H1, subtitle, introductory paragraphs, and claims paragraph. Kept the inventor/counsel distinction once; retained all five patent links, separate headings, representative matters, and the past-results disclaimer. |
| Technology & IP `/practice/technology/` | Replaced the three specified headings and the software-agreement and open-source paragraphs. Specific engineering examples remain. |
| Trademarks `/practice/trademarks/` | Used “Trademark Applications and Disputes”, “When to Seek Trademark Advice”, and the supplied advice paragraph. Preserved the Tulane clinic experience. |
| Copyright `/practice/copyright/` | Used “Copyright for Software and Creative Works”, “Copyright Ownership and Agreements”, and the supplied ownership paragraph. Preserved the Durationator discussion. |
| Software projects `/ios/` | Replaced the project-history/App Store explanation with the supplied two sentences. Preserved the iPhone J.D. review link and other project details. |
| Software patent article `/blog/can-software-be-patented/` | Used the supplied first-person opening and examples wording. Kept the software practice, About, and firm biography links in a short separate paragraph. Preserved the examples, citations, and legal-analysis sections. |
| Shared contact section | Used the supplied introduction. Removed duplicate notices from practice-page bodies while retaining the shared engagement notice, standalone Contact page notice, and footer disclaimer. |

## Scope and verification

- All 45 targeted source replacements matched. **No requested wording was unmatched.** The homepage’s former heading contained an HTML line break; it was matched as that heading and replaced with the supplied text.
- No independently introduced factual claims, personal anecdotes, or legal conclusions. The requested editorial changes do not revise the legal analysis.
- All 34 historical article bodies and their metadata remain unchanged, including the deliberately sensational patent-examiner title. All post publication dates, modification dates, excerpts, and author notes remain unchanged.
- All 68 output URLs, canonical URLs, meta descriptions, and link destinations are preserved. The only HTML-title change is the requested Patents correction. Its WebPage name updates through the existing structured-data generator. BlogPosting word count follows the edited article body.
- No CSS, JavaScript, design, navigation, dependencies, Person identity definitions, robots policy, sitemap, RSS, or routing changes.
- The 59 pages outside the nine specifically edited pages are text-identical after excluding the requested shared contact-section change. The shared section was checked on all 62 pages that include it. Contact, Disclaimer, Privacy, and 404 content remain unchanged.
- `scripts/build.py` and `scripts/check.py` pass: 68 HTML files, links/fragments, unique titles, JSON-LD vocabulary and identity references, RSS, and sitemap.
- Desktop preview: revised homepage heading, paragraph, and patent-service layout. Mobile preview at 390 × 844: first-person FAQ interaction, software patent introduction, and copyright H1; no horizontal overflow. Revised article opening and retained links checked in the browser.
- Rebuilt `nolapatent-static.zip` for local upload; generated public HTML was never edited directly.

## Files

Content and templates:

- `scripts/build.py`
- `content/pages/software-patents.html`
- `content/posts/can-software-be-patented.html`
- `content/new-posts/can-software-be-patented.json` — synchronized article import source.
- `docs/editorial-cleanup-2026-10-20.md` — this report.

The rebuild updates 62 generated HTML files: nine specifically edited pages and the remaining pages containing the shared contact section. No other generated files changed. Local screenshots and preservation-check records are in ignored `qa/editorial-*` files; the ZIP is also ignored by Git.
