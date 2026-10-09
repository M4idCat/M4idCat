"""Original character-grid cat; terminal motion adapted from ascii.rest (MIT).
Run `node src/frames.mjs`, then `python src/render.py` (requires Pillow).
"""
from pathlib import Path
from functools import lru_cache
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
FONT = next(p for p in [Path('C:/Windows/Fonts/0xProtoNerdFontMono-Regular.ttf'), Path('C:/Windows/Fonts/consola.ttf'), Path('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')] if p.exists())
def font(n): return ImageFont.truetype(str(FONT), n)
TEXT, LABEL, GLYPH = font(16), font(14), font(10)

def sprite():
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
    # Avatar reference: gray crown, cream muzzle and relaxed closed eyes.
    d.polygon([(8,12),(9,1),(11,1),(17,5),(24,5),(30,0),(32,0),(33,12),(31,17),(26,20),(15,20),(10,17)], fill=1)
    d.polygon([(10,10),(11,3),(17,7),(24,7),(30,3),(31,11),(30,16),(26,18),(15,18),(11,16)], fill=4)
    d.polygon([(11,4),(15,8),(11,9)], fill=6)
    d.polygon([(27,7),(30,4),(30,9)], fill=6)
    d.polygon([(12,10),(15,7),(24,7),(29,10),(27,12),(14,12)], fill=5)
    d.polygon([(12,13),(15,14),(20,15),(21,18),(15,18),(11,16)], fill=6)
    d.polygon([(29,13),(26,14),(22,15),(21,18),(26,18),(30,16)], fill=7)
    d.polygon([(18,8),(23,8),(24,13),(21,15),(17,13)],fill=7)
    d.line([(12,13),(14,12),(16,12),(17,13)], fill=2)
    d.line([(24,13),(25,12),(27,12),(29,13)], fill=2)
    d.line([(20,15),(22,15)], fill=12)
    d.point((21,16),fill=12)
    d.line([(20,18),(21,17),(22,18)], fill=2)
    d.line([(7,14),(11,15)],fill=7)
    d.line([(7,16),(10,16)],fill=4)
    d.line([(30,15),(35,14)],fill=7)
    d.line([(31,16),(34,17)],fill=4)
    # Small black ribbon ties and a stepped ivory ruffle echo the avatar.
    d.polygon([(7,6),(10,7),(10,10),(7,12),(5,10),(5,7)],fill=11)
    d.polygon([(7,11),(10,12),(8,18),(5,19),(6,15)],fill=11)
    d.polygon([(32,6),(35,7),(37,10),(34,12),(31,10)],fill=11)
    d.polygon([(33,11),(36,12),(36,16),(38,19),(35,20),(33,16)],fill=11)
    d.line([(7,7),(8,9)],fill=2)
    d.line([(34,8),(35,10)],fill=2)
    d.line([(9,8),(11,5),(16,3),(24,3),(29,4),(32,7),(33,11)],fill=11,width=2)
    d.polygon([(8,8),(8,5),(11,5),(11,3),(14,3),(14,1),(17,2),(19,0),(22,2),(25,0),(27,2),(30,2),(30,4),(33,4),(33,7),(35,8),(34,12),(32,12),(31,8),(28,6),(24,5),(17,5),(12,7),(10,10)],fill=7)
    d.line([(11,5),(14,4),(17,3),(24,3),(28,4),(31,6)],fill=6)
    d.point((15,3),fill=10)
    d.point((26,3),fill=10)
    d.line([(15,19),(26,19)],fill=11,width=2)
    d.polygon([(20,19),(22,21),(21,23),(19,21)],fill=11)
    d.line([(22,22),(24,25),(24,28)],fill=11,width=2)
    return im

THEMES = {
 'dark': dict(bg='#12161d',ink='#d5dfe7',muted='#8594a6',line='#2c3644',accent='#88d8cf',
  colors=['', '#687886','#8e9295','#a8adab','#b9bfba','#ccd0c5','#d5d1bd','#eee6d0','#a6c6c1','#d6bf86','#fff4d9','#3d4958','#c68f88']),
 'light': dict(bg='#faf9f6',ink='#293446',muted='#6b7889',line='#d7dce1',accent='#327b81',
  colors=['', '#596a79','#747e85','#8c9695','#9eaaa3','#abb7ae','#b5ab90','#c8bfa5','#74a3a0','#aa8846','#d8c9a8','#343e4e','#b57b77'])
}

@lru_cache(maxsize=2)
def cat_art(theme):
    p=THEMES[theme]
    im=Image.new('RGB',(585,290),p['bg']); d=ImageDraw.Draw(im)
    cat=sprite()
    for y in range(cat.height):
        for x in range(cat.width):
            v=cat.getpixel((x,y))
            if not v: continue
            glyph=['','88','##','88','88','88','oo','oo','::','88','++','88','oo'][v]
            if v not in (1,11,12) and (x+y*3)%13==0: glyph='%%'
            d.text((67+x*10,y*8),glyph,font=GLYPH,fill=p['colors'][v])
    return im

frames = json.loads((ROOT/'src/frames.json').read_text(encoding='utf-8'))
for theme,p in THEMES.items():
    rendered=[]
    still_saved=False
    for i, terminal in enumerate(frames):
        im=Image.new('RGB',(1280,440),p['bg']); d=ImageDraw.Draw(im)
        d.line((32,32,1248,32),fill=p['line'])
        d.text((36,49),'M4idCat',font=TEXT,fill=p['ink'])
        d.text((1090,49),'~/research',font=LABEL,fill=p['muted'])
        d.line((603,98,603,363),fill=p['line'])
        im.paste(cat_art(theme),(0,82))
        d.text((181,373),'[  M 4 i d C a t  ]',font=LABEL,fill=p['muted'])
        for row,line in enumerate(terminal.splitlines()):
            color=p['accent'] if row in (0,11) or 'y4ng ~ $' in line else p['ink']
            d.text((634,102+row*23),line,font=TEXT,fill=color)
        d.line((32,406,1248,406),fill=p['line'])
        d.text((36,418),'y4ng.cn',font=font(11),fill=p['muted'])
        d.text((1017,418),'C/C++ / Python / Rust',font=font(11),fill=p['muted'])
        if not still_saved and 'C/C++ / Python / Rust' in terminal and 'clear' not in terminal:
            im.save(OUT/f'banner-{theme}.png')
            still_saved=True
        rendered.append(im)
    assert still_saved, 'The reduced-motion banner must show interests and skills.'
    # One shared palette avoids color shimmer between frames.
    pal=rendered[0].quantize(colors=128)
    indexed=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in rendered]
    indexed[0].save(OUT/f'banner-{theme}.gif',save_all=True,append_images=indexed[1:],duration=100,loop=0,optimize=True,disposal=1)
    print(theme,len(indexed),(OUT/f'banner-{theme}.gif').stat().st_size)
