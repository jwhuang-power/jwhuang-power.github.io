# CLAUDE.md — Instructions for Claude Code
*Place this file in the root of your cloned repo.*

---

## Project Overview

This is Junwei Huang's personal academic website built on the **academicpages Jekyll template**, hosted on GitHub Pages at https://jwhuang-power.github.io.

Always read `WEBSITE_CONTEXT.md` before making any changes. It contains the full file structure, CSS rules, content details, and CV pipeline documentation.

---

## Critical Rules

### 1. NEVER use `<style>` blocks in `.md` files
Jekyll/YAML will throw a parse error because CSS colons conflict with YAML syntax.
Always use external CSS files under `assets/css/` and reference with `<link>` tags.

### 2. about.md must NOT have `layout:` in front matter
The homepage (`_pages/about.md`) uses `permalink: /` and should not specify a layout.

### 3. Always leave a blank line after front matter `---` before any HTML
```markdown
---
title: "..."
---
              ← blank line here
<link rel="stylesheet" ...>
```

### 4. Chip gallery uses `.chip-row-top` / `.chip-row-bottom` classes
Not `.row` — those are the correct classes that match `chip-gallery.css`.

### 5. CV pipeline
`_data/cv.yml` is the single source of truth. Edit it → push → GitHub Actions regenerates PDF automatically. Never edit the PDF directly.

---

## File Map

| What you want to change | File |
|---|---|
| Homepage content | `_pages/about.md` |
| Research page | `_research/research.md` |
| Publications page | `_pages/publications.md` |
| CV content (auto-generates PDF) | `_data/cv.yml` |
| CV PDF layout/template | `scripts/cv_template.html` |
| Chip gallery CSS | `assets/css/chip-gallery.css` |
| Publications banner CSS | `assets/css/pub-stats.css` |
| Justified text CSS | `assets/css/text-justify.css` |
| Chip photos (gallery) | `images/chip_one_pin.jpg` etc. |
| Research figures | `images/fig_one_pin.jpg` etc. |

---

## Publication Groups (cv_template.html)

The CV template renders publications in 4 groups using `first_author: true/false` in cv.yml:
1. First-Author Conference Papers
2. First-Author Journal Papers
3. Co-Authored Conference Papers
4. Co-Authored Journal Papers

When adding a new paper to cv.yml, always include:
```yaml
- id: "C18"
  first_author: true   # or false
  text: "full citation..."
  tags: [accepted]     # optional: highlight, accepted
  note: "IVR-relevant: ..."  # optional, shown in gray italic in PDF
```

---

## Common Tasks

### Add a new publication
1. Edit `_data/cv.yml` — add entry to `publications.conference` or `publications.journal`
2. Edit `_pages/publications.md` — add to the correct section with bold `**J. Huang**`
3. Update the stats table counts in publications.md

### Update homepage after new paper
1. Edit `_pages/about.md` — update the "25 publications" bullet in Research Summary
2. Also update `_data/cv.yml` research_summary bullets

### Add a research figure
1. Upload image to `images/fig_xxx.jpg`
2. In `_research/research.md`, add after the Highlights section:
```markdown
![Description](/images/fig_xxx.jpg)
```

### Fix CSS not updating
Browser cached old CSS → user should press Ctrl+Shift+R

### Fix binary PDF merge conflict
```bash
git pull --no-edit --strategy-option=ours
```
