"""Original character-grid cat; terminal motion adapted from ascii.rest (MIT).
Run `node src/frames.mjs`, then `python src/render.py` (requires Pillow).
"""
from pathlib import Path
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT = next(p for p in [Path('C:/Windows/Fonts/0xProtoNerdFontMono-Regular.ttf'), Path('C:/Windows/Fonts/consola.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')] if p.exists())
def font(n): return ImageFont.truetype(str(FONT), n)
TEXT, LABEL, GLYPH = font(16), font(14), font(10)

def sprite(blink=False):
    im = Image.new('L', (48, 36), 0)
    d = ImageDraw.Draw(im)
    # The small source grid deliberately keeps the silhouette stepped and flat.
    d.line([(29,30),(37,30),(42,27),(44,22),(43,18),(40,17)], fill=1, width=6)
    d.line([(30,30),(37,29),(41,26),(42,22),(41,19)], fill=4, width=3)
    d.line([(35,30),(39,28),(42,25)], fill=5, width=2)
    d.polygon([(13,16),(29,16),(33,21),(35,30),(32,33),(9,33),(8,30),(10,22)], fill=1)
    d.polygon([(14,17),(28,17),(31,22),(33,30),(30,32),(11,32),(10,29),(12,22)], fill=3)
    d.polygon([(12,23),(16,20),(21,21),(20,29),(18,32),(11,31)], fill=4)
    d.polygon([(25,20),(29,22),(31,28),(30,31),(25,32),(23,29)], fill=2)
    d.polygon([(17,19),(25,19),(24,26),(22,30),(18,30),(17,26)], fill=6)
    d.polygon([(20,21),(23,21),(22,27),(20,28)], fill=7)
    d.line([(15,25),(15,30),(13,32)], fill=2, width=1)
    d.line([(26,25),(26,30),(28,32)], fill=1, width=1)
    d.line([(12,32),(17,32)], fill=7)
    d.line([(27,32),(30,32)], fill=4)
    # Adult, angular face: narrow eyes, modest muzzle, no costume or lashes.
    d.polygon([(8,12),(9,1),(11,1),(17,5),(24,5),(30,0),(32,0),(33,12),(31,17),(26,20),(15,20),(10,17)], fill=1)
    d.polygon([(10,10),(11,3),(17,7),(24,7),(30,3),(31,11),(30,16),(26,18),(15,18),(11,16)], fill=4)
    d.polygon([(11,4),(15,8),(11,9)], fill=8)
    d.polygon([(27,7),(30,4),(30,9)], fill=8)
    d.polygon([(12,10),(15,7),(24,7),(29,10),(27,12),(14,12)], fill=5)
    d.polygon([(12,13),(15,14),(20,15),(21,18),(15,18),(11,16)], fill=6)
    d.polygon([(29,13),(26,14),(22,15),(21,18),(26,18),(30,16)], fill=7)
    d.line([(18,7),(19,10),(20,11)], fill=2)
    d.line([(23,7),(22,10),(21,11)], fill=2)
    d.line([(11,11),(14,12)], fill=2)
    d.line([(30,11),(27,12)], fill=2)
    d.line([(12,12),(16,12)], fill=1)
    d.line([(25,12),(29,12)], fill=1)
    if not blink:
        d.line([(13,13),(16,13)], fill=9)
        d.line([(25,13),(28,13)], fill=9)
        d.point((15,13),fill=1)
        d.point((26,13),fill=1)
    d.line([(20,15),(22,15)], fill=1)
    d.point((21,16),fill=1)
    d.line([(19,17),(23,17)], fill=2)
    d.line([(7,14),(11,15)],fill=7)
    d.line([(7,16),(10,16)],fill=4)
    d.line([(30,15),(35,14)],fill=7)
    d.line([(31,16),(34,17)],fill=4)
    # A single dark collar and a small brass diamond tag.
    d.line([(15,19),(26,19)],fill=2,width=2)
    d.line([(16,19),(25,19)],fill=8)
    d.polygon([(21,19),(23,21),(21,23),(19,21)],fill=9)
    d.point((21,21),fill=10)
    return im

THEMES = {
 'dark': dict(bg='#12161d',ink='#d5dfe7',muted='#8594a6',line='#2c3644',accent='#88d8cf',
  colors=['', '#526285','#53629a','#7184ae','#7ca3c5','#a1cad7','#b4c7d4','#e0dfcc','#b69fe0','#e2b76b','#fff0be']),
 'light': dict(bg='#faf9f6',ink='#293446',muted='#6b7889',line='#d7dce1',accent='#327b81',
  colors=['', '#354765','#505e94','#5a74a3','#4e91b2','#6cb5be','#90a8bb','#b3ac97','#8972b4','#b88735','#ede0a9'])
}
frames = json.loads((ROOT/'src/frames.json').read_text(encoding='utf-8'))
for theme,p in THEMES.items():
    rendered=[]
    for i, terminal in enumerate(frames):
        im=Image.new('RGB',(1280,440),p['bg']); d=ImageDraw.Draw(im)
        d.line((32,32,1248,32),fill=p['line'])
        d.text((36,49),'M4idCat',font=TEXT,fill=p['ink'])
        d.text((1090,49),'~/research',font=LABEL,fill=p['muted'])
        d.line((603,98,603,363),fill=p['line'])
        cat=sprite(i%67 in (51,52))
        for y in range(cat.height):
            for x in range(cat.width):
                v=cat.getpixel((x,y))
                if not v: continue
                glyph = ['','88','##','88','88','88','oo','oo','::','88','++'][v]
                if v not in (1,9,10) and (x+y*3)%13==0: glyph='%%'
                # A small glint travels across the collar, without moving the cat.
                if v==8 and y==19 and x==15+(i//3)%13: glyph='//'
                d.text((67+x*10,82+y*8),glyph,font=GLYPH,fill=p['colors'][v])
        d.text((181,373),'[  M 4 i d C a t  ]',font=LABEL,fill=p['muted'])
        for row,line in enumerate(terminal.splitlines()):
            color=p['accent'] if row in (0,11) or 'y4ng ~ $' in line else p['ink']
            d.text((634,102+row*23),line,font=TEXT,fill=color)
        d.line((32,406,1248,406),fill=p['line'])
        d.text((36,418),'y4ng.cn',font=font(11),fill=p['muted'])
        d.text((1057,418),'C / Python / Linux',font=font(11),fill=p['muted'])
        if i==0: im.save(OUT/f'banner-{theme}.png')
        rendered.append(im)
    # One shared palette avoids color shimmer between frames.
    pal=rendered[0].quantize(colors=128)
    indexed=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in rendered]
    indexed[0].save(OUT/f'banner-{theme}.gif',save_all=True,append_images=indexed[1:],duration=100,loop=0,optimize=True,disposal=1)
    print(theme,len(indexed),(OUT/f'banner-{theme}.gif').stat().st_size)
