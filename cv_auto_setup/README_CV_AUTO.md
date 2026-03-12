# Auto CV Generation Setup

## How It Works

```
Edit _data/cv.yml → git push → GitHub Action runs → PDF auto-generated → committed back to repo
```

Your website's Jekyll pages can also read from `_data/cv.yml` using `{{ site.data.cv }}`.

## Files to Add to Your Repo

```
_data/cv.yml                          ← Single source of truth (edit this!)
scripts/generate_cv.py                ← Python: YAML → HTML → PDF
scripts/cv_template.html              ← Jinja2 template (matches your CV style)
.github/workflows/generate-cv.yml     ← GitHub Action (auto-triggers on push)
```

## Quick Start

1. Copy these 4 files into your repo (`jwhuang-power.github.io`)
2. Push to GitHub
3. The Action triggers whenever `_data/cv.yml` or the template/script changes
4. Generated PDF appears at `files/CV_Junwei_Huang.pdf`
5. Update your `about.md` CV link to point to `/files/CV_Junwei_Huang.pdf`

## Adding a New Publication

Open `_data/cv.yml`, add an entry under `publications.conference` or `publications.journal`:

```yaml
    - id: "C18"
      text: >-
        J. Huang, ... "Title," in Venue, Year.
      tags: [accepted]    # optional: highlight, accepted
```

Push. Done. PDF regenerates automatically.

## Local Testing (Optional)

```bash
pip install weasyprint jinja2 pyyaml
python scripts/generate_cv.py
# → files/CV_Junwei_Huang.pdf
```

## Customizing Output Path

```bash
python scripts/generate_cv.py -o my_custom_cv.pdf
```

## Linking Website Data to YAML

In any Jekyll page, you can access `site.data.cv` directly:

```liquid
{% for pub in site.data.cv.publications.journal %}
  [{{ pub.id }}] {{ pub.text }}
{% endfor %}
```

This lets your Publications page and your CV PDF share the same data source.

## Notes

- The `[skip ci]` in the auto-commit message prevents infinite action loops
- `workflow_dispatch` lets you manually trigger from GitHub's Actions tab
- Photo: place your photo at the path specified in `cv.yml` (`images/profile.jpg`)
- WeasyPrint renders HTML → PDF; if you need to tweak fonts/margins, edit `cv_template.html`
