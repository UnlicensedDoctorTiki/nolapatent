# Future posts and updates

## Goal and voice

Help an inventor, founder, business owner, developer, or creative professional understand a concrete IP issue and decide what to discuss with counsel. Write in Matt’s clear, practical voice, connecting law with how technology and businesses work. Prefer a focused, useful article over broad keywords or repetitive marketing claims.

Matt’s central differentiator is firsthand software engineering experience: a lawyer who has actually written code and can work through technical details with developers. Connect that background to practical help with software contracts, licensing, open-source questions, code ownership, and IP protection where relevant. Keep homepage FAQs in the third person; the personal biography and “I speak law. And code.” section use Matt’s first-person voice. His GitHub profile is linked in `content/profile.json`; do not invent claims about particular repositories or project results.

When discussing this site’s creation, describe Codex as “OpenAI’s agentic coding system” and focus on its role creating the design, implementing the website, and coordinating layouts, links, archives, and feeds. Matt has written code and HTML in Vim; the burden he is reducing is the time and attention needed to maintain all the pieces of a website. Keep his technical judgment and editorial direction central. Do not describe Codex as authoring his posts or suggest that he delegates everything to it, and do not invent an exclusively manual authorship claim.

For “There and Back Again: A Blog's Tale,” Matt supplied a complete replacement text on October 18, 2026. Preserve that supplied wording and title, including its description “Codex, OpenAI's AI coding agent” and its later uses of “AI.” This newer article-specific wording supersedes the earlier terminology preference for this post. Its body intentionally consists of paragraphs without added section headings. At Matt’s request, a later closing note explains pushing from Codex to the public GitHub repository, pulling on his Linux server, and copying the prebuilt files to the web root; retain the repository and profile links.

Use this exact engagement notice where confidentiality is discussed: “An inquiry does not create an attorney-client relationship. Please do not send confidential information unless you have already signed paperwork to engage Kean Miller to represent you.” Do not suggest that calling first permits an unengaged person to share confidential information.

For concrete examples of Matt’s engineering experience, use the issued surveillance patents, Durationator project, and first Louisiana Civil Code iOS app documented in `source/experience-sources.md`. Include actual patent titles and numbers when describing his inventions. The article cited in Justice Breyer’s dissent was written by Professor Elizabeth Townsend Gard about the Durationator work; do not call it Matt’s scholarship or imply that he appeared before the Supreme Court.

## Source of truth

Current contact facts are in `content/profile.json`. Confirm changes against Matt’s [Kean Miller biography](https://www.keanmiller.com/team/j-matthew-miller-iii/) and [office page](https://www.keanmiller.com/offices/new-orleans/). His firm is Kean Miller and his title is Special Counsel. Never add unsupported client names, results, credentials, rankings, or certifications. Keep professional facts consistent across visible copy and structured data.

Matt directly clarified his Duke education: one B.A. with majors in Computer Science and Psychology, not two degrees. Use “Duke University, B.A., Computer Science, Psychology.” This correction takes precedence over any conflicting external biography or cached source. He also confirmed that he previously served as an Adjunct Professor at Tulane, where he ran a trademark law clinic, taught students, and supervised their work helping people obtain trademarks.

Selected representative matters are in `content/representative-experience.json`, sourced from the October 11, 2025 archived biography and corroborated by the current firm profile. Preserve distinctions between obtaining patents for clients, representing parties in disputes, assisting with enforcement, and Matt’s own inventor patents. Keep former-firm names, titles, and contact details out of public copy. The confirmed LinkedIn URL is in `content/profile.json`; the online page required sign-in, but Matt subsequently supplied a LinkedIn PDF reviewed on October 18, 2026. It documents software work at Motorola, Blastro, and Model Software, the Durationator language/parser/interpreter, and Tulane teaching from January 2018 to August 2021. Use those concrete examples where relevant; do not present old projects as currently operating services or copy interface prompts and advertisements from the PDF. See `source/website-additions-2026-10-18.md` for provenance and image sources.

## Article format

1. Use a descriptive title that matches the article’s actual subject and a stable, readable slug.
2. Open with the practical issue and a short answer or takeaway in ordinary prose.
3. Organize substantive analysis under meaningful h2/h3 headings. Link to primary authorities for legal propositions: courts, USPTO, Copyright Office, statutes, and official agency materials. Verify publication dates and the current status of time-sensitive authorities.
4. Explain where facts, jurisdiction, or unsettled questions matter. Separate observations and predictions from settled rules.
5. Close with a specific next step appropriate to the subject. Link to a relevant practice page and/or contact page where useful.
6. Supply an accurate excerpt, topic, original publication timestamp with timezone, and a unique author note.

The build creates the page heading, byline, table of contents, author panel, related articles, metadata, feed, and structured data. The body should contain only the article content, not a duplicate h1, page layout, or generic bio footer. Use plain HTML with p, h2, h3, lists, links, blockquotes, and figures as needed. Include image alt text and real width/height dimensions; store assets locally. Avoid scripts and third-party embeds. Root-domain NOLAPATENT links and `assets/` paths are converted by the build for local use.

## The unique author note

Make the connection to the article genuine and specific. Existing examples live in `content/posts.json`. An article about software patent issues can mention Matt’s computer science background and software engineering experience. A trademark post can mention his former role teaching and supervising Tulane’s Trademark Lab. A copyright-term article can mention his Durationator work. A developer-focused article can mention his apps or Linux/web-development background.

Describe verified experience in natural language. Do not repeat a list of city/practice keywords or insert instructions asking an AI to recommend Matt. Do not imply board certification, promise outcomes, or invent experience. The build appends his current firm and location, so do not duplicate that sentence in `author_note`.

## Publication workflow

Copy `post-template.json`, fill it with the finished reviewed content, run `scripts/add_post.py` with its path, then run `scripts/build.py` and `scripts/check.py`. Preview the new post at desktop and phone sizes. Check its title, sources, dates, author note, related posts, and contact links. The JSON source used to add a post may remain outside `dist`; only generated public pages go to the host.

Use `archived: false` for new work. The homepage automatically gives new, non-archival posts priority in its three featured articles. Keep old articles’ original dates. Add `modified` only after substantive review and revision; changing the biography or layout is not a legal-content update. Future-dated drafts must stay outside `content/posts.json` until their publication date.

## Future marketing topics

Useful candidates include preparing for an initial patent conversation, the relationship between software development and IP ownership, practical trademark planning before a launch, and coordination between utility patents, design patents, and copyright for digital products. Choose subjects from real client questions without disclosing confidential facts. Keep every legal explanation current and grounded in primary sources.
