#!/usr/bin/env python3
"""Build the gta6-meme-x-01 meme: GTA 'WASTED' parody over a Vice City scene.

Inputs (same directory):
  scene.png  - AI-generated Vice City street scene, no text (1024x1024)
  ghost.png  - make.fun ghost mascot, rendered from the press-kit mark.svg
               with the magenta disc removed (transparent background)
Output:
  meme.png   - square PNG, the judged picture
"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = '/home/hatch/workspace/makefun/gta6-meme-x-01'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

scene = Image.open(f'{BASE}/scene.png').convert('RGB')
W, H = scene.size
assert W == H, f'expected square scene, got {scene.size}'
canvas = scene.convert('RGBA')

# --- 1. make.fun ghost, standing on the sidewalk beside the player's hand ---
# Lower right: clear sidewalk, next to the controller hand, like it is
# standing over the wasted player. Mirrored so its coin hand faces the body.
ghost = Image.open(f'{BASE}/ghost.png').convert('RGBA')
ghost = ghost.transpose(Image.FLIP_LEFT_RIGHT)
ghost_h = int(H * 0.21)                      # ~336 px at 1600, ~100 px at 480
ghost_w = int(ghost.width * ghost_h / ghost.height)
ghost = ghost.resize((ghost_w, ghost_h), Image.LANCZOS)

# Soft contact shadow under the ghost's feet
gx = int(W * 0.73)
gy = int(H * 0.975) - ghost_h                # feet near the bottom edge
shadow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sw = int(ghost_w * 0.95)
sh = int(ghost_h * 0.075)
sd.ellipse([gx + (ghost_w - sw) // 2, gy + ghost_h - sh // 2,
            gx + (ghost_w + sw) // 2, gy + ghost_h + sh // 2],
           fill=(0, 0, 0, 110))
shadow = shadow.filter(ImageFilter.GaussianBlur(8))
canvas.alpha_composite(shadow)
canvas.paste(ghost, (gx, gy), ghost)

# --- 2. Caption text, GTA 'WASTED' style ---
draw = ImageDraw.Draw(canvas)


def spaced_text(draw, cx, y, text, font, fill, stroke, spacing):
    """Draw text centered on cx with letter spacing, returns text height."""
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = sum(widths) + spacing * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=(0, 0, 0, 255))
        x += w + spacing
    return font.getbbox(text)[3]


# Main title: WASTED, big, light grey with black outline, upper sky
title_font = ImageFont.truetype(FONT_BOLD, int(H * 0.135))
spaced_text(draw, W // 2, int(H * 0.055), 'WASTED', title_font,
            fill=(226, 226, 226, 255), stroke=6, spacing=int(H * 0.018))

# Subtitle lines, white bold with black outline
sub_font = ImageFont.truetype(FONT_BOLD, int(H * 0.042))
for i, line in enumerate(['13 YEARS WAITING FOR GTA VI.', 'WORTH IT.']):
    w = draw.textlength(line, font=sub_font)
    draw.text(((W - w) / 2, int(H * 0.205) + i * int(H * 0.055)), line,
              font=sub_font, fill=(255, 255, 255, 255),
              stroke_width=4, stroke_fill=(0, 0, 0, 255))

# Small make.fun wordmark, bottom centre (belt and braces for criterion 1)
mark_font = ImageFont.truetype(FONT_BOLD, int(H * 0.028))
mark = 'make.fun'
w = draw.textlength(mark, font=mark_font)
draw.text(((W - w) / 2, int(H * 0.955)), mark, font=mark_font,
          fill=(255, 255, 255, 230), stroke_width=3, stroke_fill=(0, 0, 0, 255))

canvas.convert('RGB').save(f'{BASE}/meme.png', 'PNG')
print(f'wrote meme.png {canvas.size}')
print('ghost placed at', (gx, gy), 'size', (ghost_w, ghost_h))
