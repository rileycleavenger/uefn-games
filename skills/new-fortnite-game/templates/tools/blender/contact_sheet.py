"""Tiles preview renders into one labelled image (needs Pillow: py -m pip install --user pillow).

  py tools/blender/contact_sheet.py SM_ build/models/sheet.png [columns]
  py tools/blender/contact_sheet.py <folder> <out.png> [columns]     # every .png in a folder
"""
import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PREVIEWS = os.path.normpath(os.path.join(HERE, "..", "..", "build", "models", "previews"))


def main(prefix, out, cols=4, cell=420):
    if os.path.isdir(prefix):
        files, prefix = sorted(glob.glob(os.path.join(prefix, "*.png"))), ""
    else:
        files = sorted(glob.glob(os.path.join(PREVIEWS, prefix + "*.png")))
    if not files:
        print("no previews matching", prefix)
        return 1
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 28)), (20, 16, 26))
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except OSError:
        font = ImageFont.load_default()
    for i, f in enumerate(files):
        img = Image.open(f).convert("RGB")
        w, h = img.size
        side = min(w, h)
        img = img.crop(((w - side) // 2, (h - side) // 2, (w + side) // 2, (h + side) // 2)).resize((cell, cell))
        x, y = (i % cols) * cell, (i // cols) * (cell + 28)
        sheet.paste(img, (x, y))
        label = os.path.splitext(os.path.basename(f))[0].replace(prefix, "")
        draw.text((x + 10, y + cell + 3), label, fill=(240, 220, 160), font=font)
    sheet.save(out)
    print("sheet", out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 4))
