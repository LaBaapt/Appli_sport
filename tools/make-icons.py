#!/usr/bin/env python3
"""Génère les icônes de la PWA S7 (fond #161514, « S » en Anton #FF5B4D).

Usage (depuis la racine du dépôt) : python3 tools/make-icons.py
Dépendance : Pillow (FreeType avec support WOFF2, standard dans les wheels Pillow).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts" / "anton-latin-400-normal.woff2"
OUT = ROOT / "icons"
BG = "#161514"
FG = "#FF5B4D"
TEXT = "S"
SS = 4  # suréchantillonnage pour un rendu net


def make(size: int, text_height_ratio: float) -> Image.Image:
    """text_height_ratio : hauteur de la lettre / côté de l’icône."""
    big = size * SS
    img = Image.new("RGB", (big, big), BG)
    draw = ImageDraw.Draw(img)
    # Taille de police pour que la lettre occupe la hauteur visée
    probe = ImageFont.truetype(str(FONT), 1000)
    l, t, r, b = probe.getbbox(TEXT)
    fs = int(1000 * big * text_height_ratio / (b - t))
    font = ImageFont.truetype(str(FONT), fs)
    l, t, r, b = font.getbbox(TEXT)
    # Centrage optique sur la boîte réelle des glyphes
    x = (big - (r - l)) / 2 - l
    y = (big - (b - t)) / 2 - t
    draw.text((x, y), TEXT, font=font, fill=FG)
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    # Icônes « any » et apple-touch : lettre grande (iOS arrondit les coins lui-même)
    for size, name in [(180, "apple-touch-icon.png"), (192, "icon-192.png"), (512, "icon-512.png")]:
        make(size, 0.6).save(OUT / name, optimize=True)
    # Maskable : la lettre tient dans la zone sûre (cercle de 80 % du côté)
    for size in (192, 512):
        make(size, 0.46).save(OUT / f"icon-maskable-{size}.png", optimize=True)
    print("Icônes écrites dans", OUT)


if __name__ == "__main__":
    main()
