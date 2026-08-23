#!/usr/bin/env python3
"""Auto-annotate UI Hunt screenshots with colored boxes and labels.

All CSS coords × DPR(2) = PNG pixel coords.
Viewport: 1470×780 CSS → 2940×1560 PNG.

Coord sources:
  rd.go.th  — Chrome DevTools getBoundingClientRect at scrollY=0
  sso.go.th — Chrome DevTools getBoundingClientRect at scrollY=0
  amazon search — Chrome DevTools; DPR=2 confirmed
  amazon product — pixel sampling on 2940×1560 screenshot
  booking results — Chrome DevTools getBoundingClientRect
  booking hotel — pixel sampling on 2940×1560 screenshot
"""
from PIL import Image, ImageDraw, ImageFont
import os

ASSETS = os.path.dirname(os.path.abspath(__file__))


def get_font(size):
    for path in [
        '/System/Library/Fonts/Helvetica.ttc',
        '/System/Library/Fonts/Arial.ttf',
        '/Library/Fonts/Arial.ttf',
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def annotate(filename, boxes):
    """boxes: [(x, y, w, h, hex_color, label), ...]"""
    src = os.path.join(ASSETS, filename)
    img = Image.open(src).convert('RGBA')
    font = get_font(48)

    for (x, y, w, h, color, label) in boxes:
        x1, y1 = max(0, x), max(0, y)
        x2, y2 = min(img.width, x + w), min(img.height, y + h)
        if x2 <= x1 or y2 <= y1:
            print(f'  SKIP clipped box for "{label}"')
            continue

        r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)

        draw = ImageDraw.Draw(img)

        # 8px border only — no fill overlay
        for t in range(8):
            draw.rectangle([x1+t, y1+t, x2-t, y2-t], outline=(r, g, b, 255))

        # Label pill — place INSIDE the box if it would clip above image
        if label:
            try:
                bb = font.getbbox(label)
                tw, th = bb[2] - bb[0], bb[3] - bb[1]
            except Exception:
                tw, th = len(label) * 26, 44
            pad = 16
            pill_w = tw + pad * 2
            pill_h = th + pad * 2
            # X: left-anchor; right-anchor if would overflow right edge
            if x1 + 8 + pill_w <= img.width - 4:
                lx = x1 + 8
            else:
                lx = max(4, img.width - pill_w - 4)
            # Y: above box; inside-top if would clip above image
            ly = y1 - pill_h - 6
            if ly < 0:
                ly = y1 + 8
            draw.rectangle([lx, ly, lx + pill_w, ly + pill_h], fill=(r, g, b, 230))
            draw.text((lx + pad, ly + pad), label, fill=(255, 255, 255, 255), font=font)

    out = filename.replace('.png', '_ann.png')
    img.convert('RGB').save(os.path.join(ASSETS, out))
    print(f'  ✓ {out}')


# ══════════════════════════════════════════════════════════════════════════════
# rd.go.th
# Nav CSS {0,0,1470,95} → PNG {0,0,2940,190}
# Banner CSS {0,95,1470,380} → PNG {0,190,2940,760}
# Service grid CSS {0,495,1470,334} → PNG {0,990,2940,668} (clips at 1560 in vp)
# ══════════════════════════════════════════════════════════════════════════════
print('rd.go.th...')

annotate('ss_rd_main_vp.png', [
    # Nav bar — single-weight navigation, no primary action
    (0, 0, 2940, 190, 'E74C3C', 'Nav: all links equal weight, no primary CTA'),
    # Banner/carousel — decorative, wastes prime real estate
    (0, 190, 2940, 760, 'E67E22', 'Banner carousel: announcements occupy top content area'),
    # Service icon grid starts at y:990
    (0, 990, 2940, 570, 'C0392B', '30+ icons identical size — no logical grouping or hierarchy'),
])

annotate('ss_rd_scroll.png', [
    # scrollY=300: icon grid at CSS {0,195,1470,334} → PNG {0,390,2940,668}
    (0, 390, 2940, 668, 'C0392B', 'Icon grid: 30+ items equal size, no grouping, no search'),
])

# ══════════════════════════════════════════════════════════════════════════════
# sso.go.th
# Nav1 CSS {0,0,1470,90} → PNG {0,0,2940,180}
# Nav2 CSS {0,90,1470,108} → PNG {0,180,2940,216}  (both navbars = 0-396)
# Banner CSS {0,198,1470,412} → PNG {0,396,2940,824}
# Icon row CSS {-54,610,542,90} → PNG starts at left edge ~{0,1220,1084,180}
# Content/news starts CSS y≈700 → PNG y≈1400
# ══════════════════════════════════════════════════════════════════════════════
print('sso.go.th...')

annotate('ss_sso_main_vp.png', [
    # Both nav bars combined (dual navbar = inconsistency itself)
    (0, 0, 2940, 396, 'E74C3C', 'System 1: Dual nav bars — dropdowns with 10-15 items each'),
    # Hero banner carousel
    (0, 396, 2940, 824, '8E44AD', 'System 2: Banner carousel — ministry announcements'),
    # Icon shortcuts (starts at y:1220)
    (0, 1220, 2940, 180, '2980B9', 'System 3: Icon shortcuts — no persistent text labels'),
    # Content/news peeking below icon row (CSS y:700 → PNG y:1400)
    (0, 1400, 2940, 160, '27AE60', '3 systems visible in one viewport, no shared card style'),
])

annotate('ss_sso_scroll.png', [
    # News feed / content below fold
    (0, 0, 2940, 1560, '27AE60', 'News feed column: 3rd competing visual system, different card pattern'),
])

# ══════════════════════════════════════════════════════════════════════════════
# Amazon search
# Card1 CSS {304,215,1154,242} → PNG {608,430,2308,484}
# Card2 CSS {304,457,1154,289} → PNG {608,914,2308,578}
# "Sponsored" label CSS {1181,766,58,14} → PNG {2362,1532,116,28}
# ══════════════════════════════════════════════════════════════════════════════
print('amazon.com search...')

annotate('ss_amazon_search.png', [
    # Results 1-2: CSS {304,215} {304,457} → PNG {608,430} {608,914}
    # Cards shown at identical visual weight — organic or sponsored indistinguishable
    (608, 430, 2308, 484, 'E74C3C', 'Card: identical style whether organic or sponsored'),
    (608, 914, 2308, 578, 'E74C3C', 'Card: "Overall Pick" badge = one of several competing labels'),
    # Sponsored label at bottom right: CSS {1181,766} → PNG {2362,1532}
    # Box drawn AROUND it so the label pill sits above (inside viewport)
    (2200, 1450, 500, 110, 'E67E22', '"Sponsored" tiny grey label — easy to miss'),
])

# ══════════════════════════════════════════════════════════════════════════════
# Amazon product
# From pixel sampling of ss_amazon_product.png (2940×1560):
#   Dark header:          y:0–150  (Amazon dark navy)
#   Product image (left): x:0–1000, y:150–1100 (colorful product photo)
#   Right buybox:         x:2416–2904
#     Price area:         y:470–540
#     ATC button orange:  y:1240–1360  (confirmed by (255,164,28) at x:2700)
#     Buy Now blue:       y:1380–1460  (confirmed by (63,120,174) at x:2700)
# ══════════════════════════════════════════════════════════════════════════════
print('amazon.com product...')

annotate('ss_amazon_product.png', [
    # Right buybox column: CSS {1208,236,244,800} → PNG {2416,472,488,1088}
    (2416, 472, 488, 1088, 'E74C3C', 'Buy box: price, badges, ATC, Buy Now — all same visual weight'),
    # ATC button (orange, pixel-verified at x:2700 y:1240-1360): CSS {1228,581} → PNG {2456,1162}
    (2416, 1140, 488, 124, 'E67E22', '"Add to Cart" — primary action (orange)'),
    # Buy Now (blue, pixel y:1380-1460): CSS {1228,621} → PNG {2456,1242}
    (2416, 1264, 488, 124, '2980B9', '"Buy Now" — same size as ATC: no clear primary CTA'),
])

# ══════════════════════════════════════════════════════════════════════════════
# Booking results
# sortLabel CSS {467,277,310,36} → PNG {934,554,620,72}
# card1 CSS {467,329,815,328} → PNG {934,658,1630,656}
# price1 CSS {1172,469,93,28} → PNG {2344,938,186,56}
# taxNote CSS {1119,497,146,18} → PNG {2238,994,292,36}
# ══════════════════════════════════════════════════════════════════════════════
print('booking.com results...')

annotate('ss_booking_results.png', [
    # "Top Picks for Solo Travelers" sort label
    (934, 554, 620, 72, 'E74C3C', '"Top Picks" — opaque algorithm, not price or rating'),
    # Full hotel result card 1
    (934, 658, 1630, 656, 'E67E22', 'Card: 7-9 info blocks, no clear reading priority'),
    # Price display
    (2238, 900, 650, 80, '27AE60', 'Nightly price — includes taxes here but layout varies'),
    # Tax line note
    (2144, 960, 700, 60, '8E44AD', '"Includes taxes" note — not always shown at this stage'),
])

# ══════════════════════════════════════════════════════════════════════════════
# Booking hotel
# From pixel sampling of ss_booking_hotel.png (2940×1560):
#   y=0–250: header/hotel info area (color variation suggests images + ratings)
#   y=250–350: gap/white
#   y=350–650: room rows / table content (dark text rows at y:350, 450, 550, 600)
#   y=650–1560: mostly white (page not loaded or single room listing below fold)
# ══════════════════════════════════════════════════════════════════════════════
print('booking.com hotel...')

annotate('ss_booking_hotel.png', [
    # scrollY=1722: table header CSS {186,149,888,52} → PNG {372,298,1776,104}
    # Row with urgency badge: CSS {208,240} urgency → PNG {416,480}
    # Price: CSS {580,208,160,46} → PNG {1160,416,320,92}

    # 1. Urgency badge callout — bigger box around the tiny badge
    (300, 400, 700, 180, 'E74C3C', '"We have 1 left" — loss aversion badge on every row'),
    # 2. Price + tax note (separate, below urgency, no overlap)
    (1060, 650, 900, 200, '27AE60', 'Price: +THB 1,147 taxes revealed only at checkout'),
])

print('\nAll done.')
