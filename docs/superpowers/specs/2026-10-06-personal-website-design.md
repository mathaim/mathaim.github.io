# Personal Website — Design Spec

**Owner:** Madelyn Mathai · **Date:** 2026-10-06 · **Goal:** help land research internships/jobs (AI interpretability / safety, climate AI, data science).

## Stack & hosting
- Static, hand-written `index.html` + `style.css`. No framework, no build step, no JS beyond a few lines (none required).
- Deployed to `github.com/mathaim/mathaim.github.io` (`master` branch), replacing the old site entirely. No `CNAME` exists, so the site lives at https://mathaim.github.io. History of the old R Markdown site stays in git.
- Files: `index.html`, `style.css`, `assets/photo.jpg` (square crop, ~600px), `assets/Madelyn_Mathai_CV.pdf`, `favicon.svg`.
- Responsive down to 360px wide; `<title>`, meta description and Open Graph tags (name, one-line summary, photo).

## Visual style — editorial
- Background `#faf8f3`, text `#222`, secondary `#666`, single accent rust `#b5452b` (links, highlights, Spotlight badge).
- Serif body/headings via Google Fonts (e.g. EB Garamond or Source Serif); small sans-serif (system UI) for nav, dates, labels.
- ~680px reading column, generous whitespace, thin rules between sections. Light mode only.

## Page (single page, in order)
Sticky top nav: name + About · Research · Publications · Fellowships & Service · Experience · CV (PDF).

1. **About** — photo (round) beside name and "PhD Student, Data Science, University of Virginia". 3–4 sentence bio adapted from CV summary. Links: Email (mathaimadelyn@gmail.com) · GitHub (github.com/mathaim) · LinkedIn (linkedin.com/in/madelynmathai) · CV (PDF).
2. **Research interests** — tags: mechanistic interpretability, AI safety, sparse autoencoders, AI for climate, AI policy.
3. **Research** — two entries, each: title, dates, advisors, 2–3 plain-language sentences, optional figure.
   - Mechanistic Interpretability of Atmospheric Rivers in GraphCast (Jan–Aug 2026; Agarwal, Mamalakis).
   - Data Efficiency in Sparse Autoencoders (Jun–Aug 2026; Agarwal) — headline result: strict one-to-one feature matches rise from 2% → 29% (1% → 10% of data).
4. **Publications** — CV citation format, author name bolded; "Spotlight" badge on NeurIPS 2026 TCCML paper; second paper marked "under review". [PDF]/[Code] links only where real URLs exist.
5. **Fellowships & Service** — Community Data Fellowship (UVA, 2025–present, Fountain Fund); Standing Committee on AI in Teaching and Learning (UVA Provost, 2026–present, only student member); Fox Research and Service Fellowship (Penn, 2019–20); Volunteer Data Associate, Correctional Association of New York (2023).
6. **Experience** — one line each: Ubisoft, Junior Game Data Analyst (2021–24); Cambridge Associates, Investment Analyst (2020–21); Graduate TA, UVA (Fall 2024, Spring 2025). Education: PhD UVA (exp. 2029); BA Economics, Penn (cum laude, 2020).
7. **Footer** — email, "Last updated October 2026".

## Out of scope
Blog, news feed, dark mode, contact form, analytics, multiple pages.

## Open inputs
- Photo: accessible copy of headshot (Messages attachment is blocked by macOS privacy).
- Optional: GraphCast figure; public PDF/arXiv/code links per paper. Omitted if not provided — no placeholders ship.

## Verification
Open locally in browser at desktop and mobile widths; check all links resolve; confirm live site after push.
