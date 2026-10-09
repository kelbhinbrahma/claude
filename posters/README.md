# Nasha Mukt Bharat — poster series (A4, 210 × 297 mm)

| File | Concept |
|---|---|
| `01-say-no.svg` | Swiss editorial — giant "NO." |
| `02-break-the-chain.svg` | Risograph collage — halftone + broken chain |
| `03-choose-life.svg` | Serif editorial — sprout from a broken capsule |
| `04-sikkim-nasha-mukt.svg` | Himalayan skyline + prayer flags |
| `05-be-the-change.svg` | Bold type, stamp & stickers |

**Editing:** open the `.svg` in Figma, Illustrator, Inkscape or Affinity. All text is live text,
and layers are named (`logo-placeholder`, `helpline`, `headline`, …). Install the fonts in `fonts/` first
(Anton, Bricolage Grotesque, Instrument Serif, Inter Tight, Mukta, Rozha One, Yatra One, Caveat — all OFL).
Replace `logo-placeholder` with the NIT Sikkim logo, and write numbers on the `helpline` lines.

**Exports** (`export/`): 300-dpi PNGs with paper grain, and vector PDFs without grain for clean offset printing.
To regenerate: `python3 gen.py && node render.js` (Playwright + Chromium).
