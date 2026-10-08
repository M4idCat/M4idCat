from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json
ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)
frames = json.loads((ROOT / "src/frames.json").read_text(encoding="utf-8"))
FONT = Path("C:/Windows/Fonts/0xProtoNerdFontMono-Regular.ttf")
if not FONT.exists():
    FONT = Path("C:/Windows/Fonts/consola.ttf")
def font(size): return ImageFont.truetype(str(FONT), size)
mono, small, label = font(14), font(17), font(15)
palettes = {
    "light": dict(bg="#faf9f7", ink="#1a1f29", muted="#606775", accent="#2f3a82", line="#d8d7d2", tag="#a35a4e", green="#4f8367"),
    "dark": dict(bg="#14171e", ink="#e9e7df", muted="#aeb3bd", accent="#9aa6ee", line="#343944", tag="#cf9085", green="#84b89a")
}
for theme, p in palettes.items():
    rendered = []
    for idx, frame in enumerate(frames):
        im = Image.new("RGB",(1280,380),p["bg"])
        d = ImageDraw.Draw(im)
        d.line((34,33,1246,33),fill=p["line"],width=1)
        d.text((36,50),"Y4NG / M4idCat",font=label,fill=p["ink"])
        d.text((990,50),"NOTES FROM THE SHELL",font=label,fill=p["muted"])
        d.line((616,99,616,300),fill=p["line"],width=1)
        for row,text in enumerate(frame[theme].splitlines()):
            d.text((28,104+row*20),text,font=mono,fill=p["accent"])
        d.text((48,280),"binary exploitation  /  LLM4Sec  /  AI",font=small,fill=p["muted"])
        for row,text in enumerate(frame["terminal"].splitlines()):
            color=p["accent"] if row==0 or row==10 else p["ink"]
            if "y4ng ~ $" in text: color=p["green"]
            d.text((670,94+row*20),text,font=mono,fill=color)
        d.line((34,331,1246,331),fill=p["line"],width=1)
        d.text((36,345),"y4ng.cn",font=label,fill=p["accent"])
        d.text((490,345),"read / break / understand",font=label,fill=p["muted"])
        d.text((1110,345),"[ =^.^= ]",font=label,fill=p["tag"])
        if idx==0: im.save(ASSETS/f"banner-{theme}.png")
        rendered.append(im.quantize(colors=32,method=Image.Quantize.MEDIANCUT))
    # Stop after one full pass; the stable opening frame is also provided.
    rendered[0].save(ASSETS/f"banner-{theme}.gif",save_all=True,append_images=rendered[1:],duration=80,optimize=True,disposal=1)
    print(theme,len(rendered),(ASSETS/f"banner-{theme}.gif").stat().st_size)

