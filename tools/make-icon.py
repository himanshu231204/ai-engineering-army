"""Optional generator for the plugin listing icon.

This script is NOT part of the dependency-free CLI. It is never imported by
`tools/aiea.py`, never run by validation, packaging, or CI, and it is the only
file in this repository that needs a third-party package:

    python -m pip install pillow
    python tools/make-icon.py

It writes `.claude-plugin/icon.png`, a square PNG that the Claude Code plugin
directory uses as the listing icon. The directory fixes the icon the first time
a plugin is saved or submitted, so regenerate and re-submit deliberately.

Keep the output square, between 512 and 2048 pixels on each side, and under
2 MB.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
OUTPUT = Path(__file__).resolve().parents[1] / ".claude-plugin" / "icon.png"

BACKGROUND_TOP = (11, 18, 32)
BACKGROUND_BOTTOM = (30, 41, 59)
LETTER = (251, 191, 36)
CHECK = (45, 212, 191)


def background() -> Image.Image:
    """Return the rounded-square backdrop with a vertical gradient."""
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gradient = Image.new("RGBA", (SIZE, SIZE))
    draw = ImageDraw.Draw(gradient)
    for y in range(SIZE):
        ratio = y / (SIZE - 1)
        colour = tuple(
            round(BACKGROUND_TOP[channel] + (BACKGROUND_BOTTOM[channel] - BACKGROUND_TOP[channel]) * ratio)
            for channel in range(3)
        )
        draw.line([(0, y), (SIZE, y)], fill=colour + (255,))
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, SIZE - 1, SIZE - 1], radius=180, fill=255)
    image.paste(gradient, (0, 0), mask)
    return image


def letter(draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont) -> None:
    """Draw the A that names the project."""
    box = draw.textbbox((0, 0), "A", font=font)
    width, height = box[2] - box[0], box[3] - box[1]
    draw.text(
        ((SIZE - width) / 2 - box[0] - 40, (SIZE - height) / 2 - box[1] - 55),
        "A",
        font=font,
        fill=LETTER + (255,),
    )


def check(draw: ImageDraw.ImageDraw) -> None:
    """Draw the evidence check that the skill contract is built on."""
    points = [(600, 745), (690, 830), (855, 610)]
    draw.line(points, fill=CHECK + (255,), width=66, joint="curve")
    for x, y in points:
        draw.ellipse([x - 33, y - 33, x + 33, y + 33], fill=CHECK + (255,))


def main() -> None:
    image = background()
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 620)
    letter(draw, font)
    check(draw)
    image.convert("RGB").save(OUTPUT, format="PNG", optimize=True)
    size = OUTPUT.stat().st_size
    print(f"Wrote {OUTPUT} ({SIZE}x{SIZE}, {size} bytes)")


if __name__ == "__main__":
    main()
