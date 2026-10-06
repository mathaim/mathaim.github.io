# Personal Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and deploy a single-page editorial-style academic site for Madelyn Mathai at https://mathaim.github.io.

**Architecture:** One static `index.html` + `style.css`, images and CV PDF in `assets/`. A small Python check script (`scripts/check_site.py`) is the test: it asserts every local reference resolves, required sections/links exist, and no placeholder text ships. Deployed by force-replacing the `master` branch of `github.com/mathaim/mathaim.github.io` (old site history kept as tag `old-site`).

**Tech Stack:** HTML5, CSS, Google Fonts (Source Serif 4), Python 3 stdlib (check script), macOS `sips` (image crops), git/GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-10-06-personal-website-design.md`

**Deviation from spec:** The supplied photo (`assets/IMG_5801.jpg`, 3024×4032) is a wide mountain-overlook shot with Madelyn small in frame. A round headshot crop would lose the scene, so the About photo is a soft-cornered 4:5 portrait crop centered on her. A separate square crop is used for the link-preview (Open Graph) image.

---

## File Structure

| File | Responsibility |
|---|---|
| `index.html` | All page content and meta tags |
| `style.css` | All styling (tokens, layout, responsive) |
| `favicon.svg` | "MM" monogram tab icon |
| `assets/photo.jpg` | 4:5 About photo (800×1000) |
| `assets/og.jpg` | 1200×1200 square link-preview image |
| `assets/Madelyn_Mathai_CV.pdf` | Downloadable CV |
| `scripts/check_site.py` | Site checks (the "test suite") |
| `assets/IMG_5801.jpg` | Original photo — not committed (gitignored) |

---

### Task 1: Check script (failing test first)

**Files:**
- Create: `scripts/check_site.py`

- [ ] **Step 1: Write the check script**

```python
#!/usr/bin/env python3
"""Static checks for the site. Exit 0 = pass."""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_IDS = ["about", "research", "publications", "service", "experience"]
REQUIRED_LINKS = [
    "mailto:mathaimadelyn@gmail.com",
    "https://github.com/mathaim",
    "https://www.linkedin.com/in/madelynmathai/",
    "assets/Madelyn_Mathai_CV.pdf",
]
BANNED = ["TODO", "TBD", "lorem", "placeholder", "href=\"#\""]


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.refs = set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.add(a["id"])
        for key in ("href", "src"):
            if a.get(key):
                self.refs.append(a[key])


def main():
    errors = []
    index = ROOT / "index.html"
    if not index.exists():
        print("FAIL: index.html missing")
        return 1
    html = index.read_text()
    p = Collector()
    p.feed(html)

    for i in REQUIRED_IDS:
        if i not in p.ids:
            errors.append(f"missing section id #{i}")
    for link in REQUIRED_LINKS:
        if link not in p.refs:
            errors.append(f"missing link {link}")
    for ref in p.refs:
        if ref.startswith("#") and ref[1:] not in p.ids:
            errors.append(f"broken anchor {ref}")
        elif not re.match(r"^(https?:|mailto:|#)", ref):
            if not (ROOT / ref).exists():
                errors.append(f"missing local file {ref}")
    for word in BANNED:
        if word.lower() in html.lower():
            errors.append(f"banned text: {word}")

    for e in errors:
        print("FAIL:", e)
    print("PASS" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Run it — expect failure**

Run: `python3 scripts/check_site.py`
Expected: `FAIL: index.html missing`, exit 1.

- [ ] **Step 3: Commit**

```bash
git add scripts/check_site.py
git commit -m "Add site check script"
```

---

### Task 2: Assets

**Files:**
- Create: `assets/photo.jpg`, `assets/og.jpg`, `assets/Madelyn_Mathai_CV.pdf`, `favicon.svg`
- Modify: `.gitignore`

- [ ] **Step 1: Crop photos** (subject centered near x≈1460, y≈2100 in the original)

```bash
cd assets
sips -c 2000 1600 --cropOffset 1300 680 IMG_5801.jpg --out photo.jpg
sips -Z 1000 photo.jpg
sips -c 1700 1700 --cropOffset 1500 610 IMG_5801.jpg --out og.jpg
sips -Z 1200 og.jpg
cd ..
```

Then view `assets/photo.jpg` and confirm Madelyn is centered with mountains behind. Adjust offsets if not.

- [ ] **Step 2: Copy CV**

```bash
cp "/Users/madelynmathai/Desktop/CV Madelyn Mathai.pdf" assets/Madelyn_Mathai_CV.pdf
```

- [ ] **Step 3: Favicon** — `favicon.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#b5452b"/><text x="32" y="43" font-family="Georgia,serif" font-size="28" fill="#faf8f3" text-anchor="middle">MM</text></svg>
```

- [ ] **Step 4: Ignore the original photo** — append `assets/IMG_5801.jpg` to `.gitignore`.

- [ ] **Step 5: Commit**

```bash
git add .gitignore favicon.svg assets/photo.jpg assets/og.jpg assets/Madelyn_Mathai_CV.pdf
git commit -m "Add photo crops, CV, favicon"
```

---

### Task 3: Stylesheet

**Files:**
- Create: `style.css`

- [ ] **Step 1: Write `style.css`**

```css
:root {
  --bg: #faf8f3;
  --text: #222;
  --muted: #666;
  --rule: #e2ddd2;
  --accent: #b5452b;
  --serif: "Source Serif 4", Georgia, "Times New Roman", serif;
  --sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 64px; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font: 18px/1.65 var(--serif);
  -webkit-font-smoothing: antialiased;
}
a { color: var(--accent); text-decoration: none; border-bottom: 1px solid transparent; }
a:hover { border-bottom-color: var(--accent); }
img { max-width: 100%; display: block; }

/* Nav */
.nav {
  position: sticky; top: 0; z-index: 10;
  background: rgba(250, 248, 243, .94);
  backdrop-filter: blur(6px);
  border-bottom: 1px solid var(--rule);
}
.nav-inner {
  max-width: 760px; margin: 0 auto; padding: 14px 16px;
  display: flex; gap: 20px; align-items: baseline; flex-wrap: wrap;
  font: 13px/1.4 var(--sans); letter-spacing: .04em;
}
.nav-name { font-weight: 700; color: var(--text); text-transform: uppercase; margin-right: auto; }
.nav a:not(.nav-name) { color: var(--muted); }
.nav a:not(.nav-name):hover { color: var(--accent); }

/* Layout */
main { max-width: 760px; margin: 0 auto; padding: 0 16px; }
section { padding: 40px 0; border-top: 1px solid var(--rule); }
section:first-child { border-top: 0; }
h1 { font-size: 44px; line-height: 1.1; font-weight: 600; margin: 0 0 6px; }
h2 {
  font: 600 13px/1 var(--sans); letter-spacing: .12em; text-transform: uppercase;
  color: var(--muted); margin: 0 0 24px;
}
h3 { font-size: 21px; line-height: 1.3; font-weight: 600; margin: 0 0 4px; }
p { margin: 0 0 14px; }

/* About */
.about { display: grid; grid-template-columns: 240px 1fr; gap: 36px; align-items: start; padding-top: 48px; }
.about img { border-radius: 10px; aspect-ratio: 4 / 5; object-fit: cover; }
.role { font: 15px/1.4 var(--sans); color: var(--muted); margin-bottom: 20px; }
.links { font: 14px/1.6 var(--sans); display: flex; flex-wrap: wrap; gap: 6px 18px; margin-top: 18px; }
.tags { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 20px; padding: 0; list-style: none; }
.tags li { font: 12px/1 var(--sans); border: 1px solid var(--rule); border-radius: 999px; padding: 6px 10px; color: var(--muted); }

/* Entries */
.entry { margin-bottom: 32px; }
.entry:last-child { margin-bottom: 0; }
.meta { font: 13px/1.5 var(--sans); color: var(--muted); margin-bottom: 8px; }
.pub { margin-bottom: 18px; }
.pub .title { font-style: italic; }
.badge {
  display: inline-block; font: 600 11px/1 var(--sans); letter-spacing: .06em; text-transform: uppercase;
  color: var(--accent); border: 1px solid var(--accent); border-radius: 3px; padding: 3px 6px; margin-left: 6px;
  vertical-align: 2px;
}
.badge.quiet { color: var(--muted); border-color: var(--rule); }
.compact { list-style: none; padding: 0; margin: 0; }
.compact li { display: flex; justify-content: space-between; gap: 16px; padding: 8px 0; border-bottom: 1px dotted var(--rule); }
.compact li:last-child { border-bottom: 0; }
.compact .when { font: 13px/1.9 var(--sans); color: var(--muted); white-space: nowrap; }
.sub { display: block; font-size: 16px; color: var(--muted); }

footer {
  max-width: 760px; margin: 0 auto; padding: 32px 16px 48px;
  border-top: 1px solid var(--rule); font: 13px/1.5 var(--sans); color: var(--muted);
}

@media (max-width: 640px) {
  body { font-size: 17px; }
  .nav-name { width: 100%; }
  .nav-inner { gap: 14px; }
  .about { grid-template-columns: 1fr; gap: 24px; padding-top: 28px; }
  .about img { max-width: 240px; }
  h1 { font-size: 36px; }
  .compact li { flex-direction: column; gap: 0; }
}
```

- [ ] **Step 2: Commit**

```bash
git add style.css
git commit -m "Add editorial stylesheet"
```

---

### Task 4: Page content

**Files:**
- Create: `index.html`

- [ ] **Step 1: Write `index.html`**

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Madelyn Mathai</title>
  <meta name="description" content="Madelyn Mathai, PhD student in Data Science at the University of Virginia researching mechanistic interpretability for AI safety and AI weather models.">
  <meta property="og:title" content="Madelyn Mathai">
  <meta property="og:description" content="PhD student in Data Science at UVA. Mechanistic interpretability for AI safety, and what AI weather models have learned.">
  <meta property="og:image" content="https://mathaim.github.io/assets/og.jpg">
  <meta property="og:url" content="https://mathaim.github.io/">
  <meta name="twitter:card" content="summary">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a class="nav-name" href="#about">Madelyn Mathai</a>
      <a href="#research">Research</a>
      <a href="#publications">Publications</a>
      <a href="#service">Fellowships &amp; Service</a>
      <a href="#experience">Experience</a>
      <a href="assets/Madelyn_Mathai_CV.pdf">CV</a>
    </div>
  </nav>

  <main>
    <section id="about" class="about">
      <img src="assets/photo.jpg" alt="Madelyn Mathai sitting on a rock outcrop above a mountain valley">
      <div>
        <h1>Madelyn Mathai</h1>
        <div class="role">PhD Student, Data Science · University of Virginia</div>
        <p>I study what AI models learn internally. My research is in mechanistic interpretability for AI safety: understanding models' internal representations well enough to verify them, test them causally, and selectively remove them, across models of different modalities.</p>
        <p>I've also brought these methods to AI weather and climate models, helping introduce them to the climate science community. Beyond my core research, I apply data science to civic and equity-focused work with nonprofits, and I want my technical work to inform AI policy.</p>
        <p>Before my PhD, I was a data analyst at Ubisoft and an investment analyst at Cambridge Associates.</p>
        <div class="links">
          <a href="mailto:mathaimadelyn@gmail.com">Email</a>
          <a href="https://github.com/mathaim">GitHub</a>
          <a href="https://www.linkedin.com/in/madelynmathai/">LinkedIn</a>
          <a href="assets/Madelyn_Mathai_CV.pdf">CV (PDF)</a>
        </div>
        <ul class="tags">
          <li>Mechanistic interpretability</li>
          <li>AI safety</li>
          <li>Sparse autoencoders</li>
          <li>AI for climate</li>
          <li>AI policy</li>
        </ul>
      </div>
    </section>

    <section id="research">
      <h2>Research</h2>
      <div class="entry">
        <h3>Mechanistic Interpretability of Atmospheric Rivers in GraphCast</h3>
        <div class="meta">Jan – Aug 2026 · with Dr. Chirag Agarwal (Aikyam Lab) and Dr. Antonios Mamalakis (Mamalakis Lab)</div>
        <p>GraphCast is a state-of-the-art AI weather model, but what has it learned about the atmosphere? I applied sparse autoencoders to its internal activations to surface the physical features driving its predictions, and introduced matryoshka sparse autoencoders to climate science as a way to learn hierarchical, multi-scale feature dictionaries. I traced atmospheric river concepts across the model's depth and showed they are causal by steering those features directly.</p>
      </div>
      <div class="entry">
        <h3>Data Efficiency in Sparse Autoencoders</h3>
        <div class="meta">Jun – Aug 2026 · with Dr. Chirag Agarwal (Aikyam Lab)</div>
        <p>How much data does a sparse autoencoder need? Across 3 language models, 4 architectures, and budgets from 5M to 500M tokens, reconstruction nears full-data performance at just 5% of the budget, but the learned features keep changing. Strict one-to-one feature matches rise from 2% at 1% of the data to 29% at 10%, so functional metrics plateau long before features become reproducible. Diversity-based data selection improves automated interpretability and unlearning, while random sampling best preserves reconstruction.</p>
      </div>
    </section>

    <section id="publications">
      <h2>Publications</h2>
      <div class="pub">
        <strong>Mathai, M.</strong>, Higgins, T. B., Grise, K. M., Agarwal, C., &amp; Mamalakis, A. (2026).
        <span class="title">Mechanistic Interpretability of Atmospheric Rivers in GraphCast.</span>
        NeurIPS 2026 Tackling Climate Change with Machine Learning Workshop.
        <span class="badge">Spotlight</span>
      </div>
      <div class="pub">
        Ghosh, S., <strong>Mathai, M.</strong>, Radhakrishnan, V. B., &amp; Agarwal, C. (2026).
        <span class="title">Diminishing Returns of Data in Sparse Autoencoders: Functional Behavior does not Guarantee Feature Reproducibility.</span>
        <span class="badge quiet">Under review</span>
      </div>
    </section>

    <section id="service">
      <h2>Fellowships &amp; Service</h2>
      <div class="entry">
        <h3>Community Data Fellowship, University of Virginia</h3>
        <div class="meta">2025 – present</div>
        <p>One of four graduate fellows leading a community-centered data science project with the Center for Community Partnerships. I'm partnering with The Fountain Fund, a nonprofit providing low-interest loans to formerly incarcerated people, on data analysis that supports their lending and advocacy.</p>
      </div>
      <div class="entry">
        <h3>Standing Committee on AI in Teaching and Learning, UVA Provost's Office</h3>
        <div class="meta">2026 – present</div>
        <p>The only student on a university-wide committee advising on AI policy, pedagogy, and responsible use in education.</p>
      </div>
      <div class="entry">
        <h3>Fox Research and Service Fellowship, University of Pennsylvania</h3>
        <div class="meta">2019 – 2020</div>
        <p>Analyzed U.S. political outcomes using public opinion and election data with Penn Opinion Research Election Studies faculty.</p>
      </div>
      <div class="entry">
        <h3>Volunteer Data Associate, Correctional Association of New York</h3>
        <div class="meta">2023</div>
        <p>Built a Python text extraction tool to pull text from images of death records in New York prisons.</p>
      </div>
    </section>

    <section id="experience">
      <h2>Experience &amp; Education</h2>
      <ul class="compact">
        <li><span>PhD, Data Science <span class="sub">University of Virginia</span></span><span class="when">expected 2029</span></li>
        <li><span>Graduate Teaching Assistant <span class="sub">UVA: Intro to Data Science, Intro to Programming</span></span><span class="when">2024 – 2025</span></li>
        <li><span>Junior Game Data Analyst <span class="sub">Ubisoft</span></span><span class="when">2021 – 2024</span></li>
        <li><span>Investment Analyst <span class="sub">Cambridge Associates</span></span><span class="when">2020 – 2021</span></li>
        <li><span>BA, Economics, cum laude <span class="sub">University of Pennsylvania · minors in Mathematics, Survey Research &amp; Data Analytics</span></span><span class="when">2020</span></li>
      </ul>
    </section>
  </main>

  <footer>
    <a href="mailto:mathaimadelyn@gmail.com">mathaimadelyn@gmail.com</a> · Last updated October 2026
  </footer>
</body>
</html>
```

- [ ] **Step 2: Run checks — expect pass**

Run: `python3 scripts/check_site.py`
Expected: `PASS`, exit 0.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "Add single-page site content"
```

---

### Task 5: Visual verification

- [ ] **Step 1:** Open `index.html` in the browser pane (file URL or `python3 -m http.server 8000`). Screenshot at desktop width; confirm photo beside text, nav sticky, fonts load, Spotlight badge rust.
- [ ] **Step 2:** Resize to mobile (375px). Confirm photo stacks above text, no horizontal scroll, nav wraps cleanly.
- [ ] **Step 3:** Click every nav link and the CV link; confirm each lands correctly.
- [ ] **Step 4:** Fix any issues, re-run `python3 scripts/check_site.py`, commit.

---

### Task 6: Deploy (ask user before pushing)

- [ ] **Step 1:** Add remote and tag old site:

```bash
git remote add origin https://github.com/mathaim/mathaim.github.io.git
git fetch origin master
git tag old-site origin/master
```

- [ ] **Step 2:** Confirm with the user, then replace the live site:

```bash
git push --force origin master
git push origin old-site
```

- [ ] **Step 3:** Wait ~1 minute, open https://mathaim.github.io, confirm the new site is live and the CV downloads.
