# Junwei Huang — Personal Website Context Document
*Last updated: April 2026. Use this file as context in Claude Code.*

---

## 1. Basic Info

| Field | Value |
|---|---|
| Name | Junwei Huang (黄俊威) |
| Website | https://jwhuang-power.github.io |
| GitHub Repo | github.com/jwhuang-power/jwhuang-power.github.io |
| Template | academicpages (Jekyll, GitHub Pages) |
| Emails | jwhuang@berkeley.edu · jwhuang@um.edu.mo |
| Phone | +1 (510) 994-8860 |
| Google Scholar | https://scholar.google.com/citations?user=NETRgSoAAAAJ |

---

## 2. Repository Structure

```
jwhuang-power.github.io/
├── _data/
│   └── cv.yml                  ← Single source of truth for CV PDF
├── _pages/
│   ├── about.md                ← Homepage (permalink: /)
│   └── publications.md         ← Publications page
├── _research/
│   └── research.md             ← Research page
├── _publications/              ← Individual paper .md files (not used for main pub page)
├── assets/
│   └── css/
│       ├── chip-gallery.css    ← Chip photo gallery styles
│       ├── pub-stats.css       ← Publications stats banner styles
│       └── text-justify.css    ← Justified text for .page__content p and li
├── images/
│   ├── bio.png                 ← Profile photo (400px JPEG, compressed)
│   ├── chip_one_pin.jpg        ← ① CICC 2026 chip photo
│   ├── chip_dual_loop.jpg      ← ② ISSCC 2025 chip photo
│   ├── chip_aux_transient.jpg  ← ③ CICC 2024 chip photo
│   ├── chip_inductor_first.jpg ← ④ CICC 2023 chip photo
│   ├── chip_sdsd.jpg           ← ⑤ TCAS-I 2022 chip photo
│   ├── fig_one_pin.jpg         ← Research section figure for paper 1
│   ├── fig_dual_loop.jpg       ← Research section figure for paper 2
│   ├── fig_aux_transient.jpg   ← Research section figure for paper 3
│   ├── fig_inductor_first.jpg  ← Research section figure for paper 4
│   └── fig_sdsd.jpg            ← Research section figure for paper 5
├── files/
│   └── CV_Junwei_Huang.pdf     ← Auto-generated PDF CV
├── scripts/
│   ├── cv_template.html        ← Jinja2 template for PDF CV
│   └── generate_cv.py          ← Python script (WeasyPrint + Jinja2)
└── .github/
    └── workflows/              ← GitHub Actions: auto-generates PDF on push
```

---

## 3. Critical Jekyll/CSS Rules

**NEVER put `<style>` blocks in `.md` files.**
CSS colons are parsed as YAML syntax → build error.

✅ Correct approach:
```markdown
<link rel="stylesheet" href="/assets/css/your-file.css">
```

❌ Wrong:
```markdown
<style>
.chip-gallery { margin: 30px 0; }   ← YAML parse error!
</style>
```

**Front matter must have blank line before HTML:**
```markdown
---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---
                    ← blank line required here
<link rel="stylesheet" ...>
```

---

## 4. about.md (`_pages/about.md`)

**Front matter:**
```yaml
---
permalink: /
title: ""
excerpt: "About me"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---
```
Note: NO `layout:` field — use default.

**Page structure:**
1. Welcome paragraph (intro + research interests + CV link)
2. Research Highlights (chip gallery, same HTML as research.md)
3. Education
4. Academic Appointments
5. Research Summary (Berkeley → Macau)
6. Technical Skills
7. Awards & Service

**Professor links:**
- Robert Pilawa-Podgurski: https://pilawa-group.berkeley.edu/people/
- Yan Lu: https://web.ee.tsinghua.edu.cn/luyan/en/index.htm
- Rui P. Martins: https://rto.um.edu.mo/prof-rui-paulo-da-silva-martins/
- Chi-Seng Lam: https://www.fst.um.edu.mo/personal/cslam/

---

## 5. research.md (`_research/research.md`)

**Front matter:**
```yaml
---
layout: archive
title: "Research"
permalink: /research/
author_profile: true
---
```

**Page structure:**
1. `<link>` to chip-gallery.css and text-justify.css
2. Chip gallery HTML (2+3 layout using `.chip-row-top` / `.chip-row-bottom`)
3. Italic intro paragraph
4. 5 research sections (newest first: CICC 2026 → ISSCC 2025 → CICC 2024 → CICC 2023 → TCAS-I 2022)

**Chip gallery HTML pattern:**
```html
<div class="chip-gallery">
  <div class="chip-row chip-row-top">     ← 2 cards
    <div class="chip-card">...</div>
    <div class="chip-card">...</div>
  </div>
  <div class="chip-row chip-row-bottom">  ← 3 cards
    <div class="chip-card">...</div>
    <div class="chip-card">...</div>
    <div class="chip-card">...</div>
  </div>
</div>
```

**Five research papers (newest → oldest):**

| # | Title | Venue | Process |
|---|---|---|---|
| 1 | Scalable Distributed 12-to-1V Fast-Slow Hybrid DC-DC Combo with One-Pin Current Balancing | CICC 2026 | 180nm BCD & 65nm CMOS |
| 2 | 20MHz-1MHz Dual-Loop NonUniform-Multi-Inductor Hybrid DC-DC Converter | ISSCC 2025 Highlight | 180nm BCD |
| 3 | Fast-Slow Two-Module High-Power-Density DC-DC Solution | CICC 2024 / JSSC 2025 | 180nm BCD |
| 4 | Multi-Path Inductor-First Inductor-on-Ground Switched-Capacitor Hybrid DC-DC | CICC 2023 / JSSC 2024 | 180nm BCD |
| 5 | Symmetrical Double Step-Down Converter with Extended VCR | TCAS-I 2022 | 65nm CMOS |

Each section structure:
```markdown
## N) Full Paper Title

**Challenge:** ...

**Approach:** ...

**Highlights:**
- bullet 1
- bullet 2
- bullet 3

![alt text](/images/fig_xxx.jpg)

*Published at VENUE (YEAR)*
```

---

## 6. publications.md (`_pages/publications.md`)

**Front matter:**
```yaml
---
title: "Publications"
permalink: /publications/
layout: single
author_profile: true
toc: true
toc_label: "On this page"
---
```

**Page structure:**
1. `<link>` to pub-stats.css
2. Stats banner (dark header table)
3. Google Scholar link
4. First-Author Papers (Journal → Conference)
5. Co-Author Papers (Journal → Conference)

**Publication counts (27 total, 7 first-author):**

| Venue | First-Author | Co-Author |
|---|---|---|
| JSSC | ×2 | ×3 |
| TCAS-I | ×1 | — |
| OJ-SSCS | — | ×1 |
| JOS | — | ×1 |
| ISSCC | ×1 (Highlight) | ×5 |
| CICC | ×3 | ×5 |
| ISCAS | — | ×3 |

**Styling:**
- First-author name: `**J. Huang**` (bold)
- Red tag: `<span class="pub-highlight">Highlight Paper</span>`
- Green tag: `<span class="pub-accepted">Accepted</span>`

---

## 7. CV Pipeline

**Flow:** `_data/cv.yml` → `scripts/generate_cv.py` (WeasyPrint + Jinja2) → `files/CV_Junwei_Huang.pdf`
**Trigger:** GitHub Actions on every push

**cv.yml key fields:**
```yaml
name, contact, research_interests, education, appointments,
research_summary, skills, awards, publications
```

**publications entries have:**
```yaml
- id: "C1"
  first_author: true        ← NEW: controls 4-group sorting in template
  text: "full citation..."
  tags: [highlight]         ← or [accepted]
  note: "IVR-relevant: ..."  ← optional, shown in gray italic
```

**cv_template.html key features:**
- 4-group publication order: First-Author Conf → First-Author Journal → Co-Author Conf → Co-Author Journal
- `{{ p.text | bold_author }}` filter bolds "J. Huang" in citation text
- `{% for p in cv.publications.conference if p.first_author %}` filters by group
- Technical Skills section rendered from `cv.skills`

**If binary PDF merge conflict on push:**
```bash
git pull --no-edit --strategy-option=ours
```

---

## 8. CSS Files Summary

### `chip-gallery.css`
Controls the 2+3 chip photo gallery layout on both homepage and research page.
Key classes: `.chip-gallery`, `.chip-row`, `.chip-row-top`, `.chip-row-bottom`, `.chip-card`, `.chip-caption`, `.chip-venue`

### `pub-stats.css`
Controls the publications stats banner table.
Key classes: `.pub-banner`, `.pub-table`, `.venue.top` (red), `.fa` (red text), `.ca` (blue text), `.pub-highlight` (red badge), `.pub-accepted` (green badge)

### `text-justify.css`
Applies `text-align: justify` to `.page__content p` and `li`.

---

## 9. Research Identity / IVR Framing

**Current positioning:** Hybrid SC/inductor DC-DC converters → IVR/HV-IVR for AI GPU/CPU power delivery

**Key metrics to always cite:**
- 96.1% peak efficiency (4-to-1.2V, inductor-first)
- 1.46 A/mm² current density (12:1, one-pin array)
- 63 mV droop @ 3.5 A load step (dual-loop LLSC, ISSCC 2025)
- 1.02 A/mm² at 10:1 (inductor-first, CICC 2023)
- Berkeley target: >3.0 A/mm², >20 MHz, HV-IVR >6V input

**Berkeley research framing:**
"Co-design of board-level power electronics and on-interposer HV-IVR (>6V input) for next-generation GPU/CPU power delivery, leveraging hybrid SC/inductor topologies and scalable distributed converter arrays."

---

## 10. Editing Cheat Sheet

| Task | File to edit | How |
|---|---|---|
| Update homepage text | `_pages/about.md` | GitHub web editor or VS Code (press `.`) |
| Update research content | `_research/research.md` | Same |
| Update publications | `_pages/publications.md` | Same |
| Regenerate PDF CV | `_data/cv.yml` | Edit → push → Actions auto-runs |
| Change CV layout/template | `scripts/cv_template.html` | Same |
| Add chip photo | `images/chip_xxx.jpg` | Upload via GitHub Add file |
| Add research figure | `images/fig_xxx.jpg` | Upload via GitHub Add file |
| Update gallery CSS | `assets/css/chip-gallery.css` | Edit and upload |
| Force refresh browser | Ctrl+Shift+R | — |
