#!/usr/bin/env python3
"""
generate_cv.py  —  Reads _data/cv.yml + scripts/cv_template.html → outputs PDF.
Usage:
    python scripts/generate_cv.py                   # default: files/CV_Junwei_Huang.pdf
    python scripts/generate_cv.py -o custom_name.pdf
"""

import argparse, os, re, sys, pathlib
import yaml
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup
from weasyprint import HTML

# ── Resolve paths relative to repo root ──────────────────
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILE = REPO_ROOT / "_data" / "cv.yml"
TEMPLATE_DIR = REPO_ROOT / "scripts"
TEMPLATE_NAME = "cv_template.html"
DEFAULT_OUTPUT = REPO_ROOT / "files" / "CV_Junwei_Huang.pdf"


def bold_author(text):
    """Jinja filter: bold 'J. Huang' in publication text."""
    return Markup(re.sub(
        r'\bJ\.\s*Huang\b',
        '<span class="author-me">J. Huang</span>',
        text
    ))


def main():
    parser = argparse.ArgumentParser(description="Generate CV PDF from YAML")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="Output PDF path (default: files/CV_Junwei_Huang.pdf)")
    parser.add_argument("-d", "--data", type=str, default=None,
                        help="YAML data file (default: _data/cv.yml)")
    args = parser.parse_args()

    data_path = pathlib.Path(args.data) if args.data else DATA_FILE
    output_path = pathlib.Path(args.output) if args.output else DEFAULT_OUTPUT

    # Load YAML
    with open(data_path, "r", encoding="utf-8") as f:
        cv = yaml.safe_load(f)

    # Check photo and compress if needed
    photo_path = REPO_ROOT / cv.get("contact", {}).get("photo", "")
    photo_exists = photo_path.is_file()
    photo_uri = ""
    if photo_exists:
        try:
            from PIL import Image
            import io, base64, tempfile
            img = Image.open(photo_path)
            if img.mode == 'RGBA':
                bg = Image.new('RGB', img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            # Resize to max 400px
            if max(img.size) > 400:
                ratio = 400 / max(img.size)
                img = img.resize((int(img.width * ratio), int(img.height * ratio)), Image.LANCZOS)
            # Save as compressed JPEG to temp file
            tmp = pathlib.Path(tempfile.gettempdir()) / "cv_photo_compressed.jpg"
            img.save(tmp, format="JPEG", quality=85, optimize=True)
            photo_uri = tmp.as_uri()
            print(f"   Photo: {photo_path.stat().st_size/1024:.0f} KB → {tmp.stat().st_size/1024:.0f} KB")
        except ImportError:
            photo_uri = photo_path.as_uri()
    

    # Set up Jinja
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    env.filters["bold_author"] = bold_author
    template = env.get_template(TEMPLATE_NAME)

    html_str = template.render(
        cv=cv,
        photo_exists=photo_exists,
        photo_uri=photo_uri,
    )

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Render PDF
    HTML(string=html_str, base_url=str(REPO_ROOT)).write_pdf(str(output_path))
    print(f"✅ CV generated → {output_path}")
    print(f"   Size: {output_path.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
