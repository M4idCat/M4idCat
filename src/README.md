The cat is an original 48 × 36 character-grid design, rendered using a small flat palette and stepped outlines. Its gray-and-cream fur, closed eyes, ivory ruffled headband, and dark ribbon ties reference M4idCat's GitHub avatar (https://avatars.githubusercontent.com/u/92365441?v=4, consulted 2026-10-09). The two-column composition and ASCII treatment take inspiration from https://ascii.rest/#ui and its logo gallery.

`terminal.ts` adapts the MIT-licensed terminal animation from ascii.rest. See `../LICENSE-ascii.rest.txt` for the upstream copyright and license.

Regenerate from the repository root with Node.js 24 and Python + Pillow:

```sh
node src/frames.mjs
python src/render.py
```

The renderer uses 0xProto Nerd Font Mono or Consolas on Windows, or DejaVu Sans Mono on Linux. Generated `src/frames.json` is an intermediate file.
