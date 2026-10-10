# UDGAM 2K26 — announcement posters (1080 × 1080)

| File | Style | Hook line |
|---|---|---|
| `01-riso-collage.svg` | Risograph + type collage: halftone blossom, ransom-note letters, ticket stub | "The bloom is back —" |
| `02-abstract-modern.svg` | Abstract modernism × mixed media: arch window with torn-paper Himalaya, prayer flags, halftone sun, pencil scribble, paper-cut blossom, record sleeve, brush stroke | "Where the mountains meet the music." |
| `03-minimal-bloom.svg` | Minimalism: one cherry branch, editorial serif | "The bloom returns." |
| `04-night-concert.svg` | Gradient + grain night concert: spotlight, neon-glow title, Himalayan sunset, crowd | "Louder than spring" |
| `05-retro-carnival.svg` | Retro carnival: sunburst, ferris wheel, bunting, admit-one ticket | "Come for the music, stay for the magic." |

## Exports (`export/`)
- `instagram-png/*_1080.png` — upload to Instagram / Facebook / X (1080 × 1080, with paper grain).
- `instagram-png/*_2160-hires.png` — 2× version for WhatsApp, LinkedIn, screens.
- `social-jpg/*_1080.jpg` — lighter JPGs for sites that dislike PNG.
- `print-pdf/*.pdf` — vector PDFs (text and shapes stay sharp at any size; grain left off for clean printing).
  Scale freely to any square size. Printers that need CMYK or bleed can convert/add it from these.

## Editing
Open the `.svg` in Figma, Illustrator, Inkscape or Affinity. All text is live text and groups are named
(`headline`, `ticket`, `sponsors`, `socials`, …). Install the fonts in `fonts/` first (all free/OFL:
Anton, Syne, Fraunces, Instrument Serif, Inter Tight, Space Mono, Shrikhand, Caveat).
Logos are in `assets/`.

To regenerate everything after changing `gen.py`: `python3 gen.py && node render.js` (Playwright + Chromium).
