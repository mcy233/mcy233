"""Generate assets/profile-banner.png — run: python scripts/gen_banner.py"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile-banner.png"


def main() -> None:
    w, h = 1200, 320
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        for x in range(w):
            s = x / max(w - 1, 1)
            r = int(18 + 55 * s + 25 * t)
            g = int(28 + 40 * (1 - s) + 45 * t)
            b = int(52 + 90 * s + 35 * (1 - t))
            px[x, y] = (min(r, 255), min(g, 255), min(b, 255))

    draw = ImageDraw.Draw(img)
    # subtle grid (game-like)
    for g in range(0, w, 40):
        draw.line([(g, 0), (g, h)], fill=(42, 52, 82))
    for g in range(0, h, 40):
        draw.line([(0, g), (w, g)], fill=(38, 48, 78))

    font_paths = [
        r"C:\Windows\Fonts\msyh.ttc",
        r"C:\Windows\Fonts\segoeuib.ttf",
    ]
    font_title = font_sub = None
    for p in font_paths:
        try:
            font_title = ImageFont.truetype(p, 48)
            font_sub = ImageFont.truetype(p, 22)
            break
        except OSError:
            continue
    if font_title is None:
        font_title = font_sub = ImageFont.load_default()

    title = "Chuyu Ma · 马楚昱"
    sub = "Ph.D. · AI + Games · Intelligent Agents · TJU & BZCA"
    tw = draw.textlength(title, font=font_title) if hasattr(draw, "textlength") else None
    bbox = draw.textbbox((0, 0), title, font=font_title)
    tw = bbox[2] - bbox[0]
    x0 = (w - tw) // 2
    draw.text((x0, 88), title, font=font_title, fill=(230, 240, 255))
    bbox2 = draw.textbbox((0, 0), sub, font=font_sub)
    sw = bbox2[2] - bbox2[0]
    draw.text(((w - sw) // 2, 168), sub, font=font_sub, fill=(160, 190, 230))

    accent = (110, 200, 255)
    draw.rounded_rectangle([72, h - 52, w - 72, h - 22], radius=6, outline=accent, width=2)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    print("Wrote", OUT)


if __name__ == "__main__":
    main()
