# Structured-data implementation report

Validated October 18, 2026. Scope: Schema.org JSON-LD only. The site still has the same 67 HTML files, visible content, page titles, canonical tags, URLs, navigation, styles, images, feeds, and sitemap. An automated byte comparison removed only the JSON-LD script before comparing each deployed HTML file and verified that every remaining byte, plus all non-HTML deployed files, is unchanged.

## 1. Files changed

Source and validation files:

- [`.gitattributes`](../.gitattributes): preserves the pinned vocabulary's original LF line endings and checksum across operating systems.
- [`scripts/build.py`](../scripts/build.py): delegates graph construction to a reusable module; no content/layout changes.
- [`scripts/structured_data.py`](../scripts/structured_data.py): shared Person, employer, education, work location, WebSite, page, topic, and article relationships.
- [`scripts/check_structured_data.py`](../scripts/check_structured_data.py): syntax, official vocabulary, domain/range, identity/reference, metadata/date, and visible-fact checks; optional non-schema baseline comparison.
- [`scripts/check.py`](../scripts/check.py): runs the new structured-data checks with normal site checks.
- [`scripts/workflow-check.py`](../scripts/workflow-check.py): copies the new modules when verifying a future post in an isolated workspace.
- [`source/schemaorg/schemaorg-current-https.jsonld`](../source/schemaorg/schemaorg-current-https.jsonld): pinned, unmodified official Schema.org vocabulary, used only during validation.
- [`source/schemaorg/README.md`](../source/schemaorg/README.md): vocabulary provenance and checksum.
- This report, `docs/structured-data-report.md`.

The 67 generated HTML files listed at the end have updated JSON-LD only. The ignored deployment ZIP was also regenerated. Content source files, `content/profile.json`, article metadata/dates, and assets were not edited.

## 2. Schema types and placement

| Location | Schema and relationships |
| --- | --- |
| Every delivered HTML file | One consistent Person definition, Kean Miller Organization, work Place/PostalAddress, Duke and Tulane CollegeOrUniversity entities, one Duke EducationalOccupationalCredential, educational DefinedTerm subjects, and WebSite |
| Homepage | WebPage with the Person as `about` and `mainEntity`; personal WebSite published by Matt |
| About Me | ProfilePage with the same Person as `mainEntity`; one B.A. with Computer Science and Psychology majors |
| Software Patent Attorney | WebPage referring to the Person and DefinedTerm subjects for software patents, software patent prosecution, and patent eligibility under 35 U.S.C. § 101; Service referring to Matt as provider |
| Other practice pages | WebPage, relevant DefinedTerm subjects, and Service; provider is Matt, whose employer is Kean Miller |
| All 34 posts | WebPage containing exactly one BlogPosting, with Matt as author and publisher and reciprocal page/article references |
| Journal and category archives | Existing CollectionPage types retained and linked to the same WebSite and Person |
| Representative experience | Existing CollectionPage and ItemList retained, with stable identifiers |
| Contact | Existing ContactPage retained |
| Pages with breadcrumbs | BreadcrumbList has a stable identifier and is referenced by its WebPage |
| Historical redirect alias | Shared identity/site graph only; does not redefine the destination WebPage using the redirect's different title |

Existing schema was consolidated rather than layered with a second competing graph. In particular, an article's HTML container is now a WebPage, while the article itself is its BlogPosting. There is no separate Article entity for the same post. Each entity definition appears once per graph and relationships use `@id` references.

No LegalService or LocalBusiness markup is emitted. NOLAPATENT is a WebSite, not an Organization or a separate law firm. Kean Miller is the only entity explicitly typed Organization; the universities use CollegeOrUniversity. No employment relationship with NOLAPATENT is asserted.

`datePublished` and, where present, `dateModified` come only from the existing article metadata. Schema implementation does not add new publication, review, or modification dates to articles or other pages.

## 3. Canonical identity

Person: `https://www.nolapatent.com/#matt-miller`

Other shared identifiers:

- WebSite: `https://www.nolapatent.com/#website`
- Employer: `https://www.nolapatent.com/#kean-miller`
- Work office: `https://www.nolapatent.com/#new-orleans-office`
- Office address: `https://www.nolapatent.com/#office-address`
- Duke: `https://www.nolapatent.com/#duke-university`
- Duke degree: `https://www.nolapatent.com/#duke-ba`
- Tulane Law School: `https://www.nolapatent.com/#tulane-law-school`

Page-specific identifiers use the canonical HTTPS/www page URL followed by `#webpage`, `#article`, `#service`, or `#breadcrumb`, as appropriate. Redirects do not create a second identity for their destination.

The Person's `jobTitle` is Registered Patent Attorney, as requested. Its description also preserves the current Special Counsel role at Kean Miller and explicitly describes software engineering as prior professional experience. It does not imply current employment as a software engineer.

The `sameAs` list consists only of the already verified [Kean Miller biography](https://www.keanmiller.com/team/j-matthew-miller-iii/), [GitHub profile](https://github.com/UnlicensedDoctorTiki/), and [LinkedIn profile](https://www.linkedin.com/in/jmatthew3/).

## 4. Verification and omissions

Identity, current affiliation, registration, office details, and software patent experience are supported by the visible site and the official Kean Miller biography. Education uses Matt's direct correction, which is already visible on the About and software patents pages: one Duke B.A., double major in Computer Science and Psychology. The contradictory separate Psychology B.S. entry in the external biography is not imported.

No professional registration number, unverified qualification, award, review, rating, client relationship, or additional representative matter was added. There was no sufficiently verified source in the implementation inputs for a USPTO registration number, so no number was invented. No precise past-employment chronology or current software-engineer occupation was added. Existing, supported Tulane alumni information was retained without introducing an additional degree claim.

## 5. Validation results and remaining checks

Automated results:

- All 67 server-delivered JSON-LD graphs parse as JSON and contain exactly one Person definition with the canonical identifier.
- Every emitted type and property is recognized by the pinned official Schema.org vocabulary; inherited domains and value ranges pass.
- Every local entity reference resolves within its page graph; no duplicate/conflicting definitions were found within or across pages.
- Current names, employer, job title, prior engineering description, contact details, work location, verified profiles, and single-degree wording agree with the source facts.
- All 34 BlogPosting authors, headlines, publication dates, and optional modification dates match the real article metadata; visible post headings and publication dates also agree.
- Non-schema HTML and all other deployed files are byte-for-byte unchanged.
- The regular site check passes for all 67 pages, and the isolated future-post workflow still passes.
- Negative validator checks reject an unknown type/property, a wrong property domain, a numeric job title, and a Person used as the employer value.

Schema.org Validator code-snippet tests submitted the complete generated HTML for these representative pages:

| Page | Errors | Warnings |
| --- | --- | --- |
| `/` | 0 | 0 |
| `/about-me/` | 0 | 0 |
| `/practice/software-patents/` | 0 | 0 |
| `/there-and-back-again-a-blogs-tale/` | 0 | 0 |

Screenshots and the local machine-readable check report are in the ignored `qa/` directory. No unresolved structured-data errors or warnings were found in these checks.

**Remaining manual verification:** after deploying, use the [Schema.org Validator](https://validator.schema.org/) Fetch URL mode on the public homepage, About page, software patents page, and a blog post. Code-snippet validation checks the generated files, but cannot establish that the production server, redirects, or caches are delivering the newly deployed version. This implementation has not changed production hosting or validated a post-deployment public URL.

To rerun the offline validation:

```sh
python scripts/check_structured_data.py
python scripts/check.py
```

The official vocabulary snapshot SHA-256 is `0a4b8c4c910fc831ec8695196510973390906a5ee34dc6b862dfec4d21a12f74`.

## Generated files changed

- [`dist/404.html`](../dist/404.html)
- [`dist/404/index.html`](../dist/404/index.html)
- [`dist/455-2/index.html`](../dist/455-2/index.html)
- [`dist/494-2/index.html`](../dist/494-2/index.html)
- [`dist/about-me/index.html`](../dist/about-me/index.html)
- [`dist/ai-and-patent-law-navigating-the-new-frontier/index.html`](../dist/ai-and-patent-law-navigating-the-new-frontier/index.html)
- [`dist/aint-dere-no/index.html`](../dist/aint-dere-no/index.html)
- [`dist/american-sniper-discussion/index.html`](../dist/american-sniper-discussion/index.html)
- [`dist/bitcoin-part-2-practical-benefits/index.html`](../dist/bitcoin-part-2-practical-benefits/index.html)
- [`dist/blog/index.html`](../dist/blog/index.html)
- [`dist/brand-important/index.html`](../dist/brand-important/index.html)
- [`dist/category/artificial-intelligence/index.html`](../dist/category/artificial-intelligence/index.html)
- [`dist/category/competition/index.html`](../dist/category/competition/index.html)
- [`dist/category/copyright/index.html`](../dist/category/copyright/index.html)
- [`dist/category/defamation/index.html`](../dist/category/defamation/index.html)
- [`dist/category/digital-millennium-copyright-act/index.html`](../dist/category/digital-millennium-copyright-act/index.html)
- [`dist/category/online-reputation-management/index.html`](../dist/category/online-reputation-management/index.html)
- [`dist/category/ownership/index.html`](../dist/category/ownership/index.html)
- [`dist/category/patent/index.html`](../dist/category/patent/index.html)
- [`dist/category/privacy/index.html`](../dist/category/privacy/index.html)
- [`dist/category/projects/index.html`](../dist/category/projects/index.html)
- [`dist/category/security/index.html`](../dist/category/security/index.html)
- [`dist/category/technology/bitcoin/index.html`](../dist/category/technology/bitcoin/index.html)
- [`dist/category/technology/index.html`](../dist/category/technology/index.html)
- [`dist/category/technology/iphone/index.html`](../dist/category/technology/iphone/index.html)
- [`dist/category/technology/software/index.html`](../dist/category/technology/software/index.html)
- [`dist/category/trademark/index.html`](../dist/category/trademark/index.html)
- [`dist/category/uncategorized/index.html`](../dist/category/uncategorized/index.html)
- [`dist/cello/index.html`](../dist/cello/index.html)
- [`dist/contact/index.html`](../dist/contact/index.html)
- [`dist/continued-software-security-threats/index.html`](../dist/continued-software-security-threats/index.html)
- [`dist/copyright-and-artificial-intelligence/index.html`](../dist/copyright-and-artificial-intelligence/index.html)
- [`dist/copyright-assignments/index.html`](../dist/copyright-assignments/index.html)
- [`dist/copyright-notice/index.html`](../dist/copyright-notice/index.html)
- [`dist/difference-patents-copyrights-trademarks/index.html`](../dist/difference-patents-copyrights-trademarks/index.html)
- [`dist/disclaimer/index.html`](../dist/disclaimer/index.html)
- [`dist/dmca-copyright-agent/index.html`](../dist/dmca-copyright-agent/index.html)
- [`dist/dmca-misconceptions/index.html`](../dist/dmca-misconceptions/index.html)
- [`dist/equation-group-practical-tips/index.html`](../dist/equation-group-practical-tips/index.html)
- [`dist/federal-trade-commission-crackdown-on-non-compete-agreements/index.html`](../dist/federal-trade-commission-crackdown-on-non-compete-agreements/index.html)
- [`dist/from-wordpress-back-to-static-html-with-ai/index.html`](../dist/from-wordpress-back-to-static-html-with-ai/index.html)
- [`dist/ghostbusters-huey-lewis/index.html`](../dist/ghostbusters-huey-lewis/index.html)
- [`dist/index.html`](../dist/index.html)
- [`dist/inventors-are-shocked-at-this-one-little-trick-that-patent-examiners-use/index.html`](../dist/inventors-are-shocked-at-this-one-little-trick-that-patent-examiners-use/index.html)
- [`dist/ios/index.html`](../dist/ios/index.html)
- [`dist/is-chatgpt-fair-use/index.html`](../dist/is-chatgpt-fair-use/index.html)
- [`dist/louisiana-state-trademark-registration/index.html`](../dist/louisiana-state-trademark-registration/index.html)
- [`dist/owns-copyright-work/index.html`](../dist/owns-copyright-work/index.html)
- [`dist/pinterests-privacy-policy/index.html`](../dist/pinterests-privacy-policy/index.html)
- [`dist/practice/copyright/index.html`](../dist/practice/copyright/index.html)
- [`dist/practice/patents/index.html`](../dist/practice/patents/index.html)
- [`dist/practice/software-patents/index.html`](../dist/practice/software-patents/index.html)
- [`dist/practice/technology/index.html`](../dist/practice/technology/index.html)
- [`dist/practice/trademarks/index.html`](../dist/practice/trademarks/index.html)
- [`dist/privacy/index.html`](../dist/privacy/index.html)
- [`dist/public-domain-day-2015/index.html`](../dist/public-domain-day-2015/index.html)
- [`dist/representative-experience/index.html`](../dist/representative-experience/index.html)
- [`dist/ripoff-report-help-manage-online-reputation/index.html`](../dist/ripoff-report-help-manage-online-reputation/index.html)
- [`dist/southern-food-beverage-museum-open/index.html`](../dist/southern-food-beverage-museum-open/index.html)
- [`dist/supreme-court-requires-copyright-registration-before-litigation/index.html`](../dist/supreme-court-requires-copyright-registration-before-litigation/index.html)
- [`dist/there-and-back-again-a-blogs-tale/index.html`](../dist/there-and-back-again-a-blogs-tale/index.html)
- [`dist/thinking-getting-iphone-6/index.html`](../dist/thinking-getting-iphone-6/index.html)
- [`dist/turkey-thermometer-patent/index.html`](../dist/turkey-thermometer-patent/index.html)
- [`dist/were-attorneys-not-businessmen/index.html`](../dist/were-attorneys-not-businessmen/index.html)
- [`dist/what-is-bitcoin/index.html`](../dist/what-is-bitcoin/index.html)
- [`dist/what-pet-seuss-copyright-term/index.html`](../dist/what-pet-seuss-copyright-term/index.html)
- [`dist/why-the-best-patent-strategy-doesnt-stop-at-allowance/index.html`](../dist/why-the-best-patent-strategy-doesnt-stop-at-allowance/index.html)
