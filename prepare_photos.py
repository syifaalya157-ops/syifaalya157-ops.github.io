#!/usr/bin/env python3
"""
Prepare your photos for the website.

What it does, for every JPG / PNG / TIFF / WebP in a folder:
  1. Rotates it the right way up (using the camera's orientation tag).
  2. Makes two web-sized WebP copies: 800 px and 1600 px wide
     (never enlarges a photo that is already smaller).
  3. Removes ALL hidden metadata (EXIF), including GPS location,
     so you don't accidentally publish where you live.
  4. Prints ready-to-paste HTML for the gallery, with the correct
     width/height filled in, plus the lines to add to sitemap.xml.

Your original files are never changed.

Setup (once):   pip install Pillow
Usage:          python tools/prepare_photos.py path/to/your/originals
Optional:       --out images    (where web copies go; default: images)
                --quality 82    (WebP quality 1-100; default: 82)
                --site https://syifaalya157-ops.github.io   (for sitemap lines)
                --name "Your Name"   (for the copyright lines)
"""

import argparse
import re
import sys
from datetime import date
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install Pillow")

WIDTHS = (800, 1600)
EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp"}


def slugify(name: str) -> str:
    """'IMG 2041 (Final).JPG' -> 'img-2041-final'. Descriptive file names help SEO,
    so rename originals first, e.g. 'harbour-at-dawn.jpg'."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    return name.strip("-") or "photo"


def process(src: Path, out_dir: Path, quality: int):
    with Image.open(src) as im:
        im = ImageOps.exif_transpose(im)          # fix rotation
        im = im.convert("RGB")                    # drops alpha/odd modes
        slug = slugify(src.stem)
        made = {}
        for w in WIDTHS:
            copy = im.copy()
            if copy.width > w:
                h = round(copy.height * w / copy.width)
                copy = copy.resize((w, h), Image.LANCZOS)
            dest = out_dir / f"{slug}-{w}.webp"
            # Saving without exif=... means no metadata is written.
            copy.save(dest, "WEBP", quality=quality, method=6)
            made[w] = (dest, copy.width, copy.height)
        return slug, made


def gallery_snippet(slug, made, img_dir):
    small, large = made[800], made[1600]
    w, h = large[1], large[2]
    ar = round(w / h, 4)
    return f"""<figure class="shot" style="--ar: {ar}">
  <a class="shot-link" href="{img_dir}/{large[0].name}">
    <img src="{img_dir}/{small[0].name}"
         srcset="{img_dir}/{small[0].name} {small[1]}w, {img_dir}/{large[0].name} {large[1]}w"
         sizes="(max-width: 40rem) 100vw, 45vw"
         width="{w}" height="{h}" loading="lazy" decoding="async"
         alt="DESCRIBE THIS PHOTO: what is in it, where">
  </a>
  <figcaption>Photo title <span>Place, year</span></figcaption>
</figure>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path, help="folder with your original photos")
    ap.add_argument("--out", type=Path, default=Path("images"))
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--site", default="https://syifaalya157-ops.github.io")
    ap.add_argument("--name", default="Alya Syifa", help="your name, for the copyright lines")
    ap.add_argument("--year", default=str(date.today().year))
    args = ap.parse_args()

    if not args.source.is_dir():
        sys.exit(f"Not a folder: {args.source}")
    args.out.mkdir(parents=True, exist_ok=True)

    files = sorted(p for p in args.source.iterdir() if p.suffix.lower() in EXTENSIONS)
    if not files:
        sys.exit(f"No JPG/PNG/TIFF/WebP files found in {args.source}")

    # Path used inside the website, e.g. "images". If a full folder path was
    # given for --out, fall back to just its last part.
    web_dir = args.out.name if args.out.is_absolute() else args.out.as_posix().strip("/")

    snippets, snippets_it, sitemap, jsonld = [], [], [], []
    total_kb = 0
    for f in files:
        slug, made = process(f, args.out, args.quality)
        size = sum(p.stat().st_size for p, _, _ in made.values()) // 1024
        total_kb += size
        print(f"  ok  {f.name}  ->  {slug}-800.webp, {slug}-1600.webp  ({size} KB)", file=sys.stderr)
        snippets.append(gallery_snippet(slug, made, web_dir))
        snippets_it.append(gallery_snippet(slug, made, "../" + web_dir))  # pages in it/ are one folder deeper
        url = f"{args.site.rstrip('/')}/{web_dir}/{made[1600][0].name}"
        sitemap.append(f"    <image:image><image:loc>{url}</image:loc></image:image>")
        jsonld.append(
            "      {\n"
            '        "@type": "ImageObject",\n'
            f'        "contentUrl": "{url}",\n'
            f'        "creator": {{ "@id": "{args.site.rstrip("/")}/#me" }},\n'
            f'        "creditText": "{args.name}",\n'
            f'        "copyrightNotice": "© {args.year} {args.name}"\n'
            "      }")

    print(f"\nDone: {len(files)} photos, {total_kb / 1024:.1f} MB total.\n", file=sys.stderr)
    print("<!-- ===== ENGLISH pages (index.html, graduation.html, ...): paste into a gallery ===== -->\n")
    print("\n\n".join(snippets))
    print("\n<!-- ===== ITALIAN pages (files in the it/ folder): paste into the matching gallery ===== -->\n")
    print("\n\n".join(snippets_it))
    print("\n<!-- ===== sitemap.xml: paste inside the <url> of EACH page that shows the photo ===== -->\n")
    print("\n".join(sitemap))
    print("\n<!-- ===== Optional: add to the \"@graph\" list of the page that shows the photo (copyright info) ===== -->\n")
    print(",\n".join(jsonld))


if __name__ == "__main__":
    main()
