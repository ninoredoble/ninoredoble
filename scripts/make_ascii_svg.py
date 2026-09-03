import sys
import html
from PIL import Image, ImageEnhance

SRC = sys.argv[1] if len(sys.argv) > 1 else source-prepped.png
OUT = sys.argv[2] if len(sys.argv) > 2 else nino-ascii.svg

COLS = 100
ROWS = 53
CELL_W = 8
CELL_H = 15
RAMP =  .:-=+*cs#%@

CONTRAST = 1.08
BRIGHTNESS = 1.0
GAMMA = 1.18
WHITE_FLOOR = 0.82

PAD = 20
TITLEBAR_H = 30
STATUS_H = 30
ART_W = COLS * CELL_W
ART_H = ROWS * CELL_H
CANVAS_W = ART_W + PAD * 2
CANVAS_H = TITLEBAR_H + ART_H + STATUS_H + PAD

BG_TOP = #111722
BG_BOT = #0d1117
FRAME = #30363d
TITLE_TEXT = #7d8590
INK = #c9d1d9
ROW_DUR = 0.11

im = Image.open(SRC).convert(L)
im = ImageEnhance.Brightness(im).enhance(BRIGHTNESS)
im = ImageEnhance.Contrast(im).enhance(CONTRAST)
im = im.resize((COLS, ROWS), Image.Resampling.LANCZOS)
px = im.load()

rows_txt = []
for y in range(ROWS):
    chars = []
    for x in range(COLS):
        lum = px[x, y] / 255.0
        lum = pow(lum, GAMMA)
        if lum >= WHITE_FLOOR:
            chars.append( )
        else:
            idx = int((1.0 - lum) * (len(RAMP) - 1))
            chars.append(RAMP[max(0, min(len(RAMP) - 1, idx))])
    rows_txt.append(".join(chars))

svg = [
 f'<svg xmlns=http://www.w3.org/2000/svg width={CANVAS_W} height={CANVAS_H} viewBox=0 0 {CANVAS_W} {CANVAS_H} font-family=ui-monospace, SFMono-Regular, Menlo, Consolas, monospace>',
 f'<defs><linearGradient id=bg x1=0 y1=0 x2=0 y2=1><stop offset=0 stop-color={BG_TOP}/><stop offset=1 stop-color={BG_BOT}/></linearGradient></defs>',
 f'<rect width={CANVAS_W} height={CANVAS_H} rx=12 fill=url(#bg)/>',
 f'<rect x=0.5 y=0.5 width={CANVAS_W-1} height={CANVAS_H-1} rx=12 fill=none stroke={FRAME} stroke-width=1/>',
 f'<line x1=0 y1={TITLEBAR_H} x2={CANVAS_W} y2={TITLEBAR_H} stroke={FRAME}/>',
 f'<circle cx=20 cy=15 r=5 fill=#ff5f56/>',
 f'<circle cx=36 cy=15 r=5 fill=#ffbd2e/>',
 f'<circle cx=52 cy=15 r=5 fill=#27c93f/>',
 f'<text x={CANVAS_W/2} y=19 fill={TITLE_TEXT} font-size=12 text-anchor=middle>ninoredoble@github: ~$ ./portrait.sh</text>'
]

for y, row in enumerate(rows_txt):
 t_start = y * ROW_DUR
 t_end = t_start + ROW_DUR
 y_pos = TITLEBAR_H + 7 + (y * CELL_H)
 text_y = y_pos + 11.1
 
 svg.append(f'<clipPath id=r{y}><rect x={PAD} y={y_pos} height={CELL_H} width=0><animate attributeName=width from=0 to={ART_W} begin={t_start:.3f}s dur={ROW_DUR:.2f}s fill=freeze/></rect></clipPath>')
 svg.append(f'<g clip-path=url(#r{y})><text xml:space=preserve x={PAD} y={text_y} fill={INK} font-size=12.9 textLength={ART_W} lengthAdjust=spacing>{html.escape(row)}</text></g>')
 svg.append(f'<rect y={y_pos+1} width=8 height={CELL_H-2} fill={INK} opacity=0><animate attributeName=x from={PAD} to={PAD+ART_W} begin={t_start:.3f}s dur={ROW_DUR:.2f}s fill=freeze/><set attributeName=opacity to=0.85 begin={t_start:.3f}s/><set attributeName=opacity to=0 begin={t_end:.3f}s/></rect>')

svg.append('</svg>')

with open(OUT, w, encoding=utf-8) as f:
 f.write(\n.join(svg))

print(fGenerated animated SVG saved to {OUT})
