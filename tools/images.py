#!/usr/bin/env python3
"""Resize source photos into the responsive files the site uses.

  python3 tools/images.py heater=path/to/heater.png utility=path/to/room.png van=path/to/van.png

Writes assets/img/<name>-<width>.webp and .jpg for each width in build.py,
plus assets/og.jpg (1200x630 social preview from the heater photo).
Needs Pillow (python3 -m pip install pillow).
"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from build import IMAGES  # noqa: E402

OUT = ROOT / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)


def cover(im, w, h):
    """Center-crop im to the w:h aspect ratio, then resize to w x h."""
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    im = im.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = (im.width - w) // 2
    y = (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


for arg in sys.argv[1:]:
    name, src = arg.split("=", 1)
    spec = IMAGES[name]
    im = Image.open(src).convert("RGB")
    im = cover(im, spec["w"], spec["h"])
    for w in spec["widths"]:
        h = round(spec["h"] * w / spec["w"])
        r = im.resize((w, h), Image.LANCZOS)
        r.save(OUT / f"{name}-{w}.webp", "WEBP", quality=72, method=6)
        r.save(OUT / f"{name}-{w}.jpg", "JPEG", quality=76, optimize=True, progressive=True)
        print(name, w, (OUT / f"{name}-{w}.webp").stat().st_size // 1024, "KB webp")
    if name == "heater":
        cover(im, 1200, 630).save(ROOT / "assets" / "og.jpg", "JPEG", quality=80, optimize=True, progressive=True)
