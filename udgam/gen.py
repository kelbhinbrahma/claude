"""Generates the 5 UDGAM 2K26 posters as editable 1080x1080 SVGs (fonts + logos embedded).
Run: python3 gen.py && node render.js"""
import base64, math, pathlib, random
from PIL import Image, ImageFont

ROOT = pathlib.Path(__file__).parent
S = 1080
FONTS = {  # family -> [(file, weight, style)]
    "Anton": [("Anton-400.ttf", 400, "normal")],
    "Syne": [("Syne-800.ttf", 800, "normal")],
    "Fraunces": [("Fraunces-900.ttf", 900, "normal"), ("Fraunces-400i.ttf", 400, "italic")],
    "Instrument Serif": [("InstrumentSerif-400.ttf", 400, "normal"), ("InstrumentSerif-400i.ttf", 400, "italic")],
    "Inter Tight": [("InterTight-400.ttf", 400, "normal"), ("InterTight-600.ttf", 600, "normal"), ("InterTight-800.ttf", 800, "normal")],
    "Space Mono": [("SpaceMono-400.ttf", 400, "normal"), ("SpaceMono-700.ttf", 700, "normal")],
    "Shrikhand": [("Shrikhand-400.ttf", 400, "normal")],
    "Caveat": [("Caveat-700.ttf", 700, "normal")],
}
DATES = "30 · 31 OCT &amp; 01 NOV 2026"


def width(text, font_file, size, ls=0):
    return ImageFont.truetype(str(ROOT / "fonts" / font_file), 200).getlength(text) * size / 200 + ls * len(text)


ASSETS = {n: (base64.b64encode((ROOT / f"assets/{n}.png").read_bytes()).decode(), Image.open(ROOT / f"assets/{n}.png").size)
          for n in ("udgam-logo", "quarks", "dominos")}


def img(name, x, y, w, id=None):
    data, (iw, ih) = ASSETS[name]
    return f'<image id="{id or name}" x="{x}" y="{y}" width="{w}" height="{w * ih / iw:.1f}" href="data:image/png;base64,{data}"/>'


def svg(body, fams, title, defs=""):
    css = "".join(
        f"@font-face{{font-family:'{f}';font-weight:{w};font-style:{s};src:url(data:font/ttf;base64,"
        f"{base64.b64encode((ROOT / 'fonts' / fn).read_bytes()).decode()})}}"
        for f in fams for fn, w, s in FONTS[f])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{S}" height="{S}" viewBox="0 0 {S} {S}">
<title>{title}</title>
<style>{css}</style>
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 0.4"/></feComponentTransfer></filter>
  <mask id="m-yt"><rect x="0" y="3" width="30" height="21" rx="6" fill="#fff"/><path d="M12 8.5 L12 18.5 L20.5 13.5Z" fill="#000"/></mask>
  <mask id="m-fb"><circle cx="13.5" cy="13.5" r="13.5" fill="#fff"/><path d="M15.1 27 V15.6 H18.4 L18.9 12 H15.1 V9.9 C15.1 8.9 15.4 8.2 16.9 8.2 H19 V5 C18.6 4.9 17.4 4.8 16.1 4.8 C13.3 4.8 11.4 6.5 11.4 9.6 V12 H8.3 V15.6 H11.4 V27Z" fill="#000"/></mask>
  {defs}
</defs>
{body}
</svg>'''


def grain(op=.5):
    return f'<rect id="grain-texture" width="{S}" height="{S}" filter="url(#grain)" opacity="{op}" style="mix-blend-mode:multiply" pointer-events="none"/>'


def socials(x, y, col, anchor="start", size=1.0):
    """YouTube, Facebook, Instagram icons + @UDGAM. (x,y) = left (or right if anchor=end) / vertical centre."""
    w = 119 * size + width("@UDGAM", "InterTight-800.ttf", 22 * size, 1.5 * size)
    x0 = x - w if anchor == "end" else x
    return f'''<g id="socials" transform="translate({x0:.1f},{y - 13.5 * size:.1f}) scale({size})" fill="{col}">
<rect id="youtube" width="30" height="27" mask="url(#m-yt)"/>
<g id="facebook" transform="translate(39,0)"><rect width="27" height="27" mask="url(#m-fb)"/></g>
<g id="instagram" transform="translate(78,0)"><rect x="1.3" y="1.3" width="24.4" height="24.4" rx="7" fill="none" stroke="{col}" stroke-width="2.6"/><circle cx="13.5" cy="13.5" r="5.6" fill="none" stroke="{col}" stroke-width="2.6"/><circle cx="20.3" cy="6.7" r="1.7"/></g>
<text x="119" y="21.5" font-family="Inter Tight" font-weight="800" font-size="22" letter-spacing="1.5">@UDGAM</text></g>'''


def sponsors(x, y, h=58, bg="#fff", label="#6b6478", stroke=None, rx=None):
    """Chip with 'Powered by' + Quarks + Domino's logos. Returns (markup, width)."""
    lh = h * .46
    qw, dw = lh * 600 / 147, lh * 1.06 * 700 / 152
    lab = width("POWERED BY", "SpaceMono-700.ttf", 12, 1.6)
    w = 22 + lab + 22 + qw + 22 + 1.5 + 22 + dw + 22
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ""
    return f'''<g id="sponsors" transform="translate({x},{y})">
<rect width="{w:.1f}" height="{h}" rx="{rx if rx is not None else h / 2}" fill="{bg}"{st}/>
<text x="22" y="{h / 2 + 4.2}" font-family="Space Mono" font-weight="700" font-size="12" letter-spacing="1.6" fill="{label}">POWERED BY</text>
{img("quarks", round(44 + lab, 1), (h - lh) / 2, round(qw, 1), "sponsor-quarks")}
<rect x="{66 + lab + qw:.1f}" y="{h * .25}" width="1.5" height="{h * .5}" fill="{label}" opacity=".35"/>
{img("dominos", round(89.5 + lab + qw, 1), (h - lh * 1.06) / 2, round(dw, 1), "sponsor-dominos")}
</g>''', w


# ---------- shared motifs ----------
def petal_d(r):  # cherry petal pointing up, base at origin, notched tip
    return (f"M0 0 C{-.62 * r:.1f} {-.3 * r:.1f} {-.6 * r:.1f} {-.93 * r:.1f} {-.2 * r:.1f} {-r:.1f} "
            f"L0 {-.84 * r:.1f} L{.2 * r:.1f} {-r:.1f} C{.6 * r:.1f} {-.93 * r:.1f} {.62 * r:.1f} {-.3 * r:.1f} 0 0Z")


def blossom(cx, cy, r, fill, center=None, rot=0, stroke=None, sw=2, op=1, id=None, blend=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ""
    bl = f' style="mix-blend-mode:{blend}"' if blend else ""
    g = "".join(f'<path d="{petal_d(r)}" transform="rotate({rot + i * 72})"/>' for i in range(5))
    if center:
        g += "".join(f'<line x1="0" y1="0" x2="{.36 * r * math.sin(math.radians(rot + 36 + i * 72)):.1f}" y2="{-.36 * r * math.cos(math.radians(rot + 36 + i * 72)):.1f}" stroke="{center}" stroke-width="{max(1, r * .035):.1f}"/>'
                     f'<circle cx="{.4 * r * math.sin(math.radians(rot + 36 + i * 72)):.1f}" cy="{-.4 * r * math.cos(math.radians(rot + 36 + i * 72)):.1f}" r="{r * .045:.1f}" fill="{center}"/>' for i in range(5))
        g += f'<circle r="{r * .11:.1f}" fill="{center}"/>'
    return f'<g{f" id=\"{id}\"" if id else ""} transform="translate({cx},{cy})" fill="{fill}"{st} opacity="{op}"{bl}>{g}</g>'


def petal(x, y, r, rot, fill, op=1):
    return f'<path d="{petal_d(r)}" transform="translate({x:.0f},{y:.0f}) rotate({rot:.0f}) scale(.62,1) translate(0,{r / 2:.1f})" fill="{fill}" opacity="{op:.2f}"/>'


def halftone(cx, cy, R, step, rmax, fill, angle=15, falloff=1.0, clip=None, id=None, blend="multiply"):
    """True halftone: dot size shrinks from centre outward. Single path for compact SVG."""
    a = math.radians(angle)
    d = []
    n = int(R / step) + 2
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            u, v = i * step, j * step
            x, y = cx + u * math.cos(a) - v * math.sin(a), cy + u * math.sin(a) + v * math.cos(a)
            t = math.hypot(x - cx, y - cy) / R
            if t >= 1:
                continue
            r = rmax * (1 - t ** falloff) ** .7
            if r > .5:
                d.append(f"M{x - r:.1f} {y:.1f}a{r:.1f} {r:.1f} 0 1 0 {2 * r:.1f} 0a{r:.1f} {r:.1f} 0 1 0 {-2 * r:.1f} 0")
    cp = f' clip-path="url(#{clip})"' if clip else ""
    return f'<path{f" id=\"{id}\"" if id else ""} d="{"".join(d)}" fill="{fill}"{cp} style="mix-blend-mode:{blend}"/>'


def torn(x, y, w, h, fill, rot=0, seed=1, amp=2.6, id=None, blend=""):
    rnd = random.Random(seed)
    pts = []
    for (x0, y0, x1, y1) in ((0, 0, w, 0), (w, 0, w, h), (w, h, 0, h), (0, h, 0, 0)):
        L = math.hypot(x1 - x0, y1 - y0)
        k = max(2, int(L / 7))
        for s in range(k):
            t = s / k
            nx, ny = (y1 - y0) / L, -(x1 - x0) / L
            j = rnd.uniform(-amp, amp)
            pts.append(f"{x0 + (x1 - x0) * t + nx * j:.1f},{y0 + (y1 - y0) * t + ny * j:.1f}")
    bl = f' style="mix-blend-mode:{blend}"' if blend else ""
    return f'<polygon{f" id=\"{id}\"" if id else ""} points="{" ".join(pts)}" fill="{fill}" transform="translate({x},{y}) rotate({rot} {w / 2} {h / 2})"{bl}/>'


def tape(x, y, w, rot, col="#fffaf0", op=.62):
    return torn(x, y, w, 30, col, rot, seed=int(x * 7 + y), amp=1.4).replace("<polygon", f'<polygon opacity="{op}"')


# ======================================================================
# 01 · RISO TYPE COLLAGE — "The bloom is back"
# ======================================================================
def p1():
    PAPER, PINK, BLUE, YEL, INK = "#F2EBDD", "#FF4FA3", "#2F5BD3", "#FFD23F", "#1F1B2D"
    bl_path = "".join(f'<path d="{petal_d(330)}" transform="translate(790,330) rotate({8 + i * 72})"/>' for i in range(5))
    defs = f'<clipPath id="bloom-clip">{bl_path}</clipPath>'
    letters = [  # (char, font-family, weight, size, glyph colour, tile, tile colour, dx, dy, rot)
        ("U", "Anton", 400, 230, PAPER, "torn", BLUE, 0, 0, -4),
        ("D", "Fraunces", 900, 230, PINK, None, None, 0, -8, 3),
        ("G", "Shrikhand", 400, 190, INK, "rect", YEL, 0, 14, -2),
        ("A", "Syne", 800, 190, PAPER, "circle", INK, 0, -6, 5),
        ("M", "Anton", 400, 230, BLUE, "torn", PINK, 0, 10, -3),
    ]
    tiles = ""
    for i, (ch, fam, wt, fs, col, tile, tcol, dx, dy, rot) in enumerate(letters):
        x, y = 58 + i * 196 + dx, 178 + dy
        cx, cy = x + 92, y + 120
        t = ""
        if tile == "torn":
            t = torn(x, y, 184, 240, tcol, 0, seed=i + 3, blend="multiply")
        elif tile == "rect":
            t = f'<rect x="{x + 4}" y="{y + 10}" width="176" height="220" fill="{tcol}" style="mix-blend-mode:multiply"/>'
        elif tile == "circle":
            t = f'<circle cx="{cx}" cy="{cy}" r="96" fill="{tcol}"/>'
        base = cy + fs * (.36 if fam in ("Anton",) else .33)
        tiles += f'''<g id="letter-{ch}" transform="rotate({rot} {cx} {cy})">{t}
<text x="{cx}" y="{base:.0f}" text-anchor="middle" font-family="{fam}" font-weight="{wt}" font-size="{fs}" fill="{col}"{"" if col == PAPER else ' style="mix-blend-mode:multiply"'}>{ch}</text></g>'''
    acts = [("LIVE CONCERTS", INK, PAPER, -2), ("DJ NIGHTS", PINK, INK, 2), ("DANCE-OFFS", YEL, INK, -1),
            ("GAMES &amp; FUN ZONES", BLUE, PAPER, 1.5), ("FOOD STALLS", PAPER, INK, -2.5)]
    al = ""
    for i, (t, bg, fg, rot) in enumerate(acts):
        w = width(t.replace("&amp;", "&"), "Anton-400.ttf", 34, 1) + 28
        x, y = 1022 - w - (i % 2) * 34, 690 + i * 50
        stroke = f' stroke="{INK}" stroke-width="2"' if bg == PAPER else ""
        al += f'''<g transform="rotate({rot} {x + w / 2} {y + 22})"><rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="44" fill="{bg}"{stroke} style="mix-blend-mode:multiply"/>
<text x="{x + 14:.0f}" y="{y + 36}" font-family="Anton" font-size="34" letter-spacing="1" fill="{fg}">{t}</text></g>'''
    sp, _ = sponsors(58, 970, 64, "#fff", stroke=INK, rx=4)
    body = f'''<rect width="{S}" height="{S}" fill="{PAPER}"/>
<g id="riso-blossom">{halftone(790, 330, 470, 11, 5.2, PINK, 15, 1.3, clip="bloom-clip")}
{blossom(804, 342, 330, "none", rot=8, stroke=BLUE, sw=3, blend="multiply")}</g>
{halftone(205, 790, 210, 10, 4.6, YEL, 45, 1.1, id="riso-sun")}
<g id="masthead">{img("udgam-logo", 46, 30, 215)}
{torn(690, 34, 350, 98, PAPER, -1.5, seed=21)}
<g font-family="Space Mono" font-weight="700" font-size="17" letter-spacing="2" fill="{INK}" text-anchor="end">
<text x="1026" y="64">NIT SIKKIM PRESENTS</text><text x="1026" y="90">ANNUAL CULTURAL FEST</text><text x="1026" y="116" fill="{PINK}">ISSUE Nº 2K26</text></g></g>
<g id="headline-UDGAM">{tiles}</g>
{tape(150, 168, 120, -18)}{tape(845, 404, 110, 14)}
<g id="year-label" transform="rotate(3 840 470)">{torn(700, 438, 320, 92, INK, 0, seed=11)}
<text x="860" y="510" text-anchor="middle" font-family="Space Mono" font-weight="700" font-size="74" letter-spacing="2" fill="{YEL}">2K26</text></g>
<text id="tagline" x="66" y="512" font-family="Caveat" font-weight="700" font-size="88" fill="{PINK}" transform="rotate(-5 250 490)" style="mix-blend-mode:multiply">Chase the Bloom</text>
<g id="hook"><text x="60" y="610" font-family="Fraunces" font-style="italic" font-size="50" fill="{INK}">The bloom is back —</text>
<text x="60" y="648" font-family="Inter Tight" font-weight="600" font-size="25" fill="{INK}">and this time it brought a soundtrack.</text></g>
<g id="ticket" transform="rotate(-3 260 800)">
<path d="M60 690 H460 V760 a18 18 0 0 0 0 36 V880 H60 V796 a18 18 0 0 0 0 -36Z" fill="{BLUE}" style="mix-blend-mode:multiply"/>
<line x1="372" y1="702" x2="372" y2="868" stroke="{PAPER}" stroke-width="2" stroke-dasharray="6 6"/>
<text x="84" y="724" font-family="Space Mono" font-weight="700" font-size="16" letter-spacing="2" fill="{YEL}">ADMIT ALL · 3 DAYS</text>
<text x="82" y="800" font-family="Anton" font-size="76" fill="{PAPER}">30·31 OCT</text>
<text x="84" y="852" font-family="Anton" font-size="40" letter-spacing="1" fill="{YEL}">&amp; 01 NOV 2026</text>
<text x="416" y="785" font-family="Space Mono" font-weight="700" font-size="16" letter-spacing="2" fill="{PAPER}" transform="rotate(-90 416 785)" text-anchor="middle">NIT SIKKIM</text></g>
<g id="sticker" transform="rotate(12 512 728)"><circle cx="512" cy="728" r="50" fill="{PINK}"/>
<text x="512" y="724" text-anchor="middle" font-family="Anton" font-size="30" fill="{PAPER}">3 DAYS</text>
<text x="512" y="746" text-anchor="middle" font-family="Space Mono" font-weight="700" font-size="13" letter-spacing="1" fill="{INK}">OF BLOOM</text></g>
<g id="activities">{al}</g>
{blossom(985, 615, 26, PINK, YEL, 20)}{blossom(470, 940, 18, BLUE, PAPER, 5, op=.9)}
<line x1="58" y1="950" x2="1022" y2="950" stroke="{INK}" stroke-width="2"/>
{sp}
{socials(1022, 1002, INK, "end", 1.15)}
{grain(.55)}'''
    return svg(body, ["Anton", "Fraunces", "Shrikhand", "Syne", "Space Mono", "Caveat", "Inter Tight"], "UDGAM 2K26 — Riso Collage", defs)


# ======================================================================
# 02 · ABSTRACT MODERNISM × MIXED MEDIA — "Where the mountains meet the music"
# ======================================================================
def jag(pts, amp, seed, step=7):
    """Polyline with torn-paper jitter along every segment."""
    rnd, out = random.Random(seed), []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        k, nx, ny = max(1, int(L / step)), (y1 - y0) / L, -(x1 - x0) / L
        for s in range(k):
            t, j = s / k, rnd.uniform(-amp, amp)
            out.append(f"{x0 + (x1 - x0) * t + nx * j:.1f},{y0 + (y1 - y0) * t + ny * j:.1f}")
    return " ".join(out)


def brush(x, y, w, h, col, seed=1, gap="#ECE3D0", id=None):
    """Dry-brush paint stroke: ragged edges, tapered tail, bristle streaks."""
    rnd, n = random.Random(seed), 60
    top, bot = [], []
    for i in range(n + 1):
        t = i / n
        hw = h / 2 * min(1, (t / .05) ** .5) * (1 - .8 * max(0, (t - .8) / .2) ** 1.4)
        cy = y + h / 2 + math.sin(t * math.pi * 1.4) * h * .08
        top.append(f"{x + w * t:.1f},{cy - hw + rnd.uniform(-1.6, 1.6):.1f}")
        bot.append(f"{x + w * t:.1f},{cy + hw + rnd.uniform(-1.6, 1.6):.1f}")
    streaks = "".join(
        f'<line x1="{x + w * rnd.uniform(.05, .3):.0f}" y1="{y + h * (.2 + .6 * k / 5):.0f}" x2="{x + w * rnd.uniform(.75, .97):.0f}" y2="{y + h * (.2 + .6 * k / 5) + rnd.uniform(-3, 3):.0f}" '
        f'stroke="{gap}" stroke-width="{rnd.uniform(1, 2.6):.1f}" stroke-dasharray="{rnd.randint(30, 90)} {rnd.randint(4, 18)} {rnd.randint(10, 60)} {rnd.randint(3, 10)}" opacity=".55"/>'
        for k in range(6))
    return f'<g{f" id=\"{id}\"" if id else ""}><polygon points="{" ".join(top + bot[::-1])}" fill="{col}"/>{streaks}</g>'


def scribble(cx, cy, r, col, seed=1, loops=3, sw=2.2, op=.85):
    """Hand-drawn pencil loops."""
    rnd, pts = random.Random(seed), []
    for i in range(loops * 36):
        a = i / 36 * 2 * math.pi
        rr = r * (1 + rnd.uniform(-.018, .018) + .05 * math.sin(i / 9 + loops))
        pts.append(f"{cx + rr * math.cos(a) * 1.04:.1f},{cy + rr * math.sin(a):.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def cutout(cx, cy, r, fill, seed=1, rot=0, stroke=None, sw=3):
    """Matisse-style paper cut-out blossom (each petal a little different)."""
    rnd = random.Random(seed)
    st = f' fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else f' fill="{fill}"'
    return (f'<g transform="translate({cx},{cy}) rotate({rot})"{st}>' +
            "".join(f'<path d="{petal_d(r * rnd.uniform(.86, 1.08))}" transform="rotate({i * 72 + rnd.uniform(-8, 8):.1f})"/>' for i in range(5)) + "</g>")


def p2():
    PAPER, NAVY, PINK, ORANGE, TEAL, MAG, CREAM, INK = "#ECE3D0", "#1C1E4A", "#FF5C8A", "#F6A23A", "#22A6A8", "#B0177F", "#FFF4E2", "#141432"
    arch = "M70 790 V320 A250 250 0 0 1 570 320 V790 Z"
    defs = f'''<linearGradient id="dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFC07A"/><stop offset=".42" stop-color="#F7839A"/><stop offset=".75" stop-color="#9C4AA8"/><stop offset="1" stop-color="#3C2C79"/></linearGradient>
<clipPath id="arch-clip"><path d="{arch}"/></clipPath><clipPath id="sleeve-clip"><rect x="640" y="262" width="250" height="250"/></clipPath>
<path id="sticker-ring" d="M0 0 m-47 0 a47 47 0 1 1 94 0 a47 47 0 1 1 -94 0"/>'''
    mtn = lambda pts, col, seed, amp=3.2: f'<polygon points="{jag(pts + [pts[0]], amp, seed)}" fill="{col}"/>'
    flags = ""
    for i in range(10):  # Sikkimese prayer flags (lungta colours) strung across the valley
        t = i / 9
        fx, fy = 100 + 430 * t, 560 - 95 * t + 22 * math.sin(math.pi * t)
        flags += f'<rect x="{fx:.0f}" y="{fy:.0f}" width="24" height="30" fill="{["#2F5BD3", CREAM, "#E2364B", "#1E9E5A", "#FFD23F"][i % 5]}" transform="rotate({-8 + 4 * math.sin(i)} {fx:.0f} {fy:.0f})"/>'
    rnd = random.Random(7)
    arch_petals = "".join(petal(rnd.uniform(90, 550), rnd.uniform(140, 640), rnd.uniform(7, 13), rnd.uniform(0, 360), rnd.choice((CREAM, "#FFD1E3", PINK)), .95) for _ in range(14))
    grooves = "".join(f'<circle cx="905" cy="387" r="{r}" fill="none" stroke="#3a3a5e" stroke-width="1.3"/>' for r in range(46, 112, 7))
    U = width("UDGAM", "Syne-800.ttf", 100, -2)
    fs = 960 / U * 100
    sp, spw = sponsors(60, 982, 62)
    body = f'''<rect width="{S}" height="{S}" fill="{PAPER}"/>
<text id="side-label" x="46" y="790" transform="rotate(-90 46 790)" font-family="Space Mono" font-weight="700" font-size="17" letter-spacing="3.5" fill="{NAVY}">NIT SIKKIM · ANNUAL CULTURAL FEST</text>
<path id="arch-shadow" d="{arch}" fill="none" stroke="{NAVY}" stroke-width="3" transform="translate(14,14)"/>
<g id="arch-window" clip-path="url(#arch-clip)">
<rect x="60" y="60" width="520" height="740" fill="url(#dusk)"/>
<circle cx="320" cy="392" r="132" fill="#FFE6A8"/>
{halftone(320, 392, 230, 9, 4.2, "#FF6F61", 20, 1.4, id="sun-halftone")}
{scribble(320, 392, 150, NAVY, 3, 2, 2)}
{mtn([(60, 620), (140, 500), (205, 550), (300, 432), (385, 520), (455, 472), (580, 560), (580, 800), (60, 800)], "#6E4AA6", 1)}
{mtn([(60, 690), (170, 565), (250, 622), (360, 500), (470, 612), (580, 580), (580, 800), (60, 800)], NAVY, 2)}
{mtn([(360, 500), (328, 538), (346, 533), (358, 548), (373, 531), (394, 540)], CREAM, 3, 1.6)}
{mtn([(170, 565), (150, 590), (163, 587), (172, 598), (184, 586), (195, 592)], CREAM, 4, 1.4)}
<path d="M100 560 Q330 {520} 540 465" fill="none" stroke="{CREAM}" stroke-width="1.5" opacity=".8"/><g id="prayer-flags">{flags}</g>
{mtn([(60, 742), (160, 692), (262, 732), (382, 668), (500, 722), (580, 700), (580, 800), (60, 800)], TEAL, 5)}
{halftone(200, 790, 180, 8, 3.2, NAVY, 45, 1.2, id="ground-halftone")}
<g id="arch-petals">{arch_petals}</g>
</g>
<path d="{arch}" fill="none" stroke="{NAVY}" stroke-width="3"/>
<g id="cutout-blossom">{cutout(572, 236, 150, MAG, 9, 14)}{cutout(584, 226, 150, None, 9, 14, stroke=PINK, sw=3)}
{halftone(572, 236, 62, 7, 3.3, "#FFD23F", 10, 1, id="blossom-core", blend="normal")}<circle cx="572" cy="236" r="12" fill="{NAVY}"/></g>
{img("udgam-logo", 790, 46, 244)}
<g id="record">
<circle cx="905" cy="387" r="118" fill="{INK}"/>{grooves}<circle cx="905" cy="387" r="38" fill="{ORANGE}"/><circle cx="905" cy="387" r="5" fill="{PAPER}"/></g>
<g id="sleeve"><rect x="640" y="262" width="250" height="250" fill="{NAVY}"/>
<g clip-path="url(#sleeve-clip)">{halftone(890, 262, 260, 10, 4.6, PINK, 30, 1.1, blend="normal")}</g>
<text x="658" y="352" font-family="Syne" font-weight="800" font-size="54" letter-spacing="-1.5" fill="{CREAM}">2K26</text>
<text x="662" y="488" font-family="Space Mono" font-weight="700" font-size="17" letter-spacing="2" fill="{CREAM}">SIDE A — LIVE</text>
<rect x="654" y="368" width="228" height="28" fill="{NAVY}"/><text x="662" y="388" font-family="Space Mono" font-weight="700" font-size="17" letter-spacing="2" fill="{ORANGE}">3 DAYS · 3 NIGHTS</text></g>
{tape(828, 248, 96, 38)}
<g id="dates" transform="rotate(-2 830 610)">{torn(620, 552, 420, 118, NAVY, 0, seed=31, amp=3)}
<text x="1018" y="604" text-anchor="end" font-family="Syne" font-weight="800" font-size="44" letter-spacing="-1" fill="{CREAM}">30—31 OCT</text>
<text x="1018" y="650" text-anchor="end" font-family="Syne" font-weight="800" font-size="34" letter-spacing="-.5" fill="{ORANGE}">&amp; 01 NOV 2026</text></g>
<g id="live-sticker" transform="translate(546,640) rotate(-12)"><circle r="66" fill="{ORANGE}"/><circle r="59" fill="none" stroke="{NAVY}" stroke-width="1.5" stroke-dasharray="3 5"/>
<text font-family="Space Mono" font-weight="700" font-size="14" letter-spacing="2.6" fill="{NAVY}"><textPath href="#sticker-ring">LIVE MUSIC ✦ DANCE ✦ ART ✦ </textPath></text>
<text y="12" text-anchor="middle" font-family="Anton" font-size="34" fill="{NAVY}">LIVE</text></g>
{brush(600, 686, 440, 84, PINK, 4, gap=PAPER, id="brush-stroke")}
<text id="tagline" x="626" y="742" font-family="Fraunces" font-style="italic" font-size="50" fill="{CREAM}">Chase the Bloom.</text>
<text id="hook" x="1036" y="808" text-anchor="end" font-family="Inter Tight" font-weight="600" font-size="25" fill="{NAVY}">Where the mountains meet the music.</text>
<g id="headline-UDGAM" font-family="Syne" font-weight="800" font-size="{fs:.1f}" letter-spacing="{-2 * fs / 100:.1f}">
<text x="68" y="958" fill="{PINK}" style="mix-blend-mode:multiply">UDGAM</text><text x="60" y="952" fill="{NAVY}" style="mix-blend-mode:multiply">UDGAM</text></g>
{sp}
{socials(1036, 1013, NAVY, "end", 1.15)}
{grain(.5)}'''
    return svg(body, ["Syne", "Fraunces", "Inter Tight", "Space Mono", "Anton"], "UDGAM 2K26 — Abstract Mixed Media", defs)

# ======================================================================
# 03 · MINIMALISM — "The bloom returns."
# ======================================================================
def p3():
    BG, INK, PINK, DPINK, BARK = "#F6F0E8", "#2B2230", "#F49AB8", "#E2557F", "#3B2A2C"
    flowers = [(700, 268, 44, PINK, -10), (868, 196, 36, DPINK, 18), (566, 338, 30, PINK, 40), (985, 168, 26, PINK, 5), (790, 300, 22, DPINK, 30)]
    buds = [(620, 300), (930, 150), (745, 225), (1040, 190)]
    sp, spw = sponsors(60, 984, 62, "none", "#8a7f86", stroke="#d8cdc6")
    body = f'''<rect width="{S}" height="{S}" fill="{BG}"/>
<g id="branch" fill="none" stroke="{BARK}" stroke-linecap="round">
<path d="M1090 96 C980 140 900 160 820 220 C740 280 640 300 520 360" stroke-width="5"/>
<path d="M880 176 C900 150 925 140 945 132" stroke-width="3"/><path d="M760 250 C745 230 740 215 742 200" stroke-width="2.5"/>
<path d="M640 310 C625 300 615 290 612 280" stroke-width="2"/><path d="M1000 130 C1015 150 1030 170 1050 180" stroke-width="2.5"/></g>
<g id="buds">{"".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="9" fill="{DPINK}"/>' for x, y in buds)}</g>
<g id="blossoms">{"".join(blossom(x, y, r, c, BARK, rot) for x, y, r, c, rot in flowers)}</g>
<g id="falling-petals">{petal(560, 470, 16, 40, PINK)}{petal(460, 560, 12, 120, DPINK, .8)}{petal(900, 520, 14, -30, PINK, .9)}</g>
{img("udgam-logo", 52, 46, 240)}
<g id="headline">
<text x="60" y="586" font-family="Space Mono" font-weight="700" font-size="18" letter-spacing="2.6" fill="{INK}">NIT SIKKIM · THE ANNUAL CULTURAL FEST</text>
<text x="54" y="730" font-family="Instrument Serif" font-size="164" letter-spacing="-3" fill="{INK}">The bloom</text>
<text x="54" y="866" font-family="Instrument Serif" font-style="italic" font-size="164" letter-spacing="-3" fill="{DPINK}">returns.</text></g>
<g id="details" text-anchor="end" fill="{INK}">
<text x="1020" y="790" font-family="Inter Tight" font-weight="800" font-size="30" letter-spacing="1">UDGAM 2K26</text>
<text x="1020" y="828" font-family="Inter Tight" font-weight="600" font-size="27">30 · 31 Oct &amp; 01 Nov 2026</text>
<text x="1020" y="866" font-family="Instrument Serif" font-style="italic" font-size="34" fill="{DPINK}">Chase the Bloom</text></g>
<text x="60" y="938" font-family="Inter Tight" font-weight="400" font-size="24" fill="{INK}" opacity=".85">Three days of music, dance, art &amp; everything in between.</text>
<line x1="60" y1="964" x2="1020" y2="964" stroke="{INK}" stroke-opacity=".25"/>
{sp}
{socials(1020, 1015, INK, "end", 1.15)}
{grain(.3)}'''
    return svg(body, ["Instrument Serif", "Inter Tight", "Space Mono"], "UDGAM 2K26 — Minimal")


# ======================================================================
# 04 · NIGHT CONCERT — gradient + grain, "Louder than spring"
# ======================================================================
def p4():
    CREAM, PINK, LPINK, SIL = "#FFF1E6", "#FF6FA8", "#FFC2DA", "#0A0614"
    rnd = random.Random(26)
    stars = "".join(f'<circle cx="{rnd.uniform(0, S):.0f}" cy="{rnd.uniform(0, 420):.0f}" r="{rnd.uniform(.6, 1.8):.1f}" fill="#fff" opacity="{rnd.uniform(.3, .9):.2f}"/>' for _ in range(90))
    beams = "".join(f'<polygon points="{x0},860 {x0 + 14},860 {xt + 70},-40 {xt - 70},-40" fill="url(#beam)" style="mix-blend-mode:screen"/>'
                    for x0, xt in [(300, -40), (420, 260), (540, 560), (660, 840), (780, 1120)])
    crowd = ""
    for row, (yb, rmin, rmax, n) in enumerate([(918, 13, 16, 30), (958, 17, 21, 22), (1010, 22, 27, 16)]):
        for i in range(n):
            x = (i + rnd.uniform(.1, .9)) * S / n
            r = rnd.uniform(rmin, rmax)
            y = yb + rnd.uniform(-8, 8)
            crowd += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}"/><rect x="{x - r * 1.5:.0f}" y="{y + r * .8:.0f}" width="{r * 3:.0f}" height="200" rx="{r:.0f}"/>'
            if rnd.random() < .35:
                s = rnd.choice((-1, 1))
                hx, hy = x + s * r * rnd.uniform(.8, 1.8), y - r * rnd.uniform(2.6, 3.6)
                crowd += f'<path d="M{x + s * r * 1.1:.0f} {y + r * 1.3:.0f} L{hx:.0f} {hy:.0f}" stroke="{SIL}" stroke-width="{r * .55:.1f}" stroke-linecap="round"/>'
                if rnd.random() < .5:
                    crowd += f'<circle cx="{hx:.0f}" cy="{hy - 4:.0f}" r="9" fill="#fff" opacity=".35" filter="url(#glow)"/><circle cx="{hx:.0f}" cy="{hy - 4:.0f}" r="2.4" fill="#fff"/>'
    petals = "".join(petal(rnd.uniform(0, S), rnd.uniform(60, 880), rnd.uniform(6, 15), rnd.uniform(0, 360), rnd.choice((PINK, LPINK, "#FFD1E3")), rnd.uniform(.5, 1)) for _ in range(46))
    defs = f'''<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0C0726"/><stop offset=".5" stop-color="#341052"/><stop offset=".85" stop-color="#8E1F63"/><stop offset="1" stop-color="#C2366E"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFD27A"/><stop offset=".55" stop-color="#FF8A6B"/><stop offset="1" stop-color="#FF4F9A"/></linearGradient>
<linearGradient id="beam" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#FFD9EC" stop-opacity=".32"/><stop offset="1" stop-color="#FFD9EC" stop-opacity="0"/></linearGradient>
<radialGradient id="stage-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FF7FB5" stop-opacity=".75"/><stop offset="1" stop-color="#FF7FB5" stop-opacity="0"/></radialGradient>
<filter id="glow" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="soft" x="-.2" y="-.2" width="1.4" height="1.4"><feGaussianBlur stdDeviation="18"/></filter>
<filter id="neon" x="-.3" y="-.6" width="1.6" height="2.2"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="neon-thin" x="-.3" y="-1" width="1.6" height="3"><feGaussianBlur stdDeviation="5"/></filter>
<radialGradient id="spot" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFE3F0" stop-opacity=".35"/><stop offset=".6" stop-color="#FF8FC0" stop-opacity=".12"/><stop offset="1" stop-color="#FF8FC0" stop-opacity="0"/></radialGradient>'''
    sp, spw = sponsors(56, 996, 60)
    body = f'''<rect width="{S}" height="{S}" fill="url(#sky)"/>
<g id="stars">{stars}</g>
<g id="sun-disc"><circle cx="540" cy="650" r="250" fill="url(#sun)" opacity=".35" filter="url(#soft)"/><circle cx="540" cy="650" r="230" fill="url(#sun)"/>
{"".join(f'<rect x="300" y="{660 + i * 22 + i * i * 1.5:.0f}" width="480" height="{4 + i * 2.6:.0f}" fill="#4A1259"/>' for i in range(6))}</g>
<g id="himalaya"><polygon points="0,760 120,650 190,700 330,560 420,640 470,610 560,690 690,540 790,650 880,600 1080,720 1080,860 0,860" fill="#2A0D44"/>
<polygon points="330,560 305,585 322,582 333,595 347,580 360,588" fill="#E8D6F0" opacity=".8"/><polygon points="690,540 664,568 681,563 693,577 708,562 722,570" fill="#E8D6F0" opacity=".8"/>
<polygon points="0,820 160,740 300,800 450,730 600,800 760,720 900,790 1080,740 1080,880 0,880" fill="#1A0830"/></g>
<ellipse cx="540" cy="860" rx="520" ry="120" fill="url(#stage-glow)"/>
<g id="light-beams">{beams}</g>
<g id="petals">{petals}</g>
<ellipse id="title-spotlight" cx="540" cy="330" rx="520" ry="230" fill="url(#spot)" style="mix-blend-mode:screen"/>
<g id="top">{img("udgam-logo", 48, 38, 205)}
<g font-family="Space Mono" font-weight="700" font-size="17" letter-spacing="2.6" fill="{CREAM}" text-anchor="end"><text x="1030" y="74">NIT SIKKIM</text><text x="1030" y="100" fill="{LPINK}">ANNUAL CULTURAL FEST</text></g></g>
<g id="headline" text-anchor="middle">
<g id="neon-tag"><rect x="335" y="178" width="410" height="50" rx="25" fill="none" stroke="{PINK}" stroke-width="5" filter="url(#neon-thin)"/>
<rect x="335" y="178" width="410" height="50" rx="25" fill="#1A0830" fill-opacity=".55" stroke="{LPINK}" stroke-width="2.5"/>
<text x="540" y="211" font-family="Space Mono" font-weight="700" font-size="21" letter-spacing="6" fill="{CREAM}">LOUDER THAN SPRING</text></g>
<g id="title" font-family="Fraunces" font-weight="900" font-size="236" letter-spacing="-6">
<text x="540" y="430" fill="{PINK}" filter="url(#neon)" opacity=".95">UDGAM</text>
<text x="547" y="437" fill="#FF3D8B">UDGAM</text>
<text x="540" y="430" fill="{CREAM}">UDGAM</text></g>
<g id="tagline-pill"><rect x="290" y="462" width="500" height="68" rx="34" fill="#FF4F9A"/><rect x="296" y="468" width="488" height="56" rx="28" fill="none" stroke="#1A0830" stroke-width="1.5" stroke-dasharray="2 6" opacity=".6"/>
<text x="540" y="508" fill="#1A0830"><tspan font-family="Space Mono" font-weight="700" font-size="27" letter-spacing="1">2K26 · </tspan><tspan font-family="Fraunces" font-style="italic" font-size="40">chase the bloom</tspan></text></g></g>
<g id="details" text-anchor="middle">
<rect x="134" y="732" width="812" height="118" rx="22" fill="none" stroke="{PINK}" stroke-width="6" filter="url(#neon-thin)"/>
<rect x="134" y="732" width="812" height="118" rx="22" fill="#12061F" fill-opacity=".78" stroke="{LPINK}" stroke-width="2"/>
<text x="540" y="790" font-family="Space Mono" font-weight="700" font-size="34" letter-spacing="2" fill="{CREAM}">{DATES}</text>
<text x="540" y="828" font-family="Inter Tight" font-weight="800" font-size="20" letter-spacing="3.5" fill="{LPINK}">LIVE CONCERTS · DJ NIGHTS · DANCE · FUN ZONES · FOOD</text></g>
<g id="crowd" fill="{SIL}">{crowd}</g>
{sp}
{socials(1026, 1026, CREAM, "end", 1.15)}
{grain(.45)}'''
    return svg(body, ["Fraunces", "Space Mono", "Inter Tight"], "UDGAM 2K26 — Night Concert", defs)


# ======================================================================
# 05 · RETRO CARNIVAL — "Come for the music, stay for the magic"
# ======================================================================
def p5():
    Y1, Y2, NAVY, MAG, PINK, TEAL, CREAM, ORANGE = "#FFD45C", "#FFC23D", "#1D1F4E", "#B5179E", "#FF5C8A", "#1FA9A6", "#FFF4DF", "#F27B2A"
    cx, cy = 540, 1150
    rays = "".join(f'<path d="M{cx} {cy} L{cx + 1800 * math.cos(math.radians(a)):.0f} {cy + 1800 * math.sin(math.radians(a)):.0f} L{cx + 1800 * math.cos(math.radians(a + 6)):.0f} {cy + 1800 * math.sin(math.radians(a + 6)):.0f}Z"/>' for a in range(180, 360, 12))
    # bunting
    flags = ""
    for k, (y0, sag, n, off) in enumerate([(30, 70, 13, 0), (8, 55, 11, 40)]):
        pts = [i * S / n + off for i in range(n + 1)]
        flags += f'<path d="M0 {y0} Q540 {y0 + sag * 2} 1080 {y0}" fill="none" stroke="{NAVY}" stroke-width="2"/>'
        for i, x in enumerate(pts[:-1]):
            t = (x + 26) / S
            yy = y0 + 4 * sag * t * (1 - t) - 3
            flags += f'<polygon points="{x + 6:.0f},{yy:.0f} {x + 46:.0f},{yy:.0f} {x + 26:.0f},{yy + 44:.0f}" fill="{[PINK, TEAL, MAG, CREAM][(i + k) % 4]}"/>'
    # ferris wheel
    wx, wy, wr = 800, 640, 200
    spokes = "".join(f'<line x1="{wx}" y1="{wy}" x2="{wx + wr * math.cos(math.radians(a)):.1f}" y2="{wy + wr * math.sin(math.radians(a)):.1f}" stroke="{NAVY}" stroke-width="3"/>' for a in range(0, 360, 30))
    cars = "".join(f'<g transform="translate({wx + wr * math.cos(math.radians(a)):.1f},{wy + wr * math.sin(math.radians(a)):.1f})"><line y2="16" stroke="{NAVY}" stroke-width="3"/>'
                   f'<path d="M-20 14 H20 V30 a10 10 0 0 1 -10 10 H-10 a10 10 0 0 1 -10 -10Z" fill="{[PINK, TEAL, MAG, ORANGE][i % 4]}" stroke="{NAVY}" stroke-width="3"/></g>' for i, a in enumerate(range(15, 375, 30)))
    star = lambda x, y, r, n=24, k=.82: " ".join(f"{x + (r if i % 2 == 0 else r * k) * math.cos(math.pi * i / n):.1f},{y + (r if i % 2 == 0 else r * k) * math.sin(math.pi * i / n):.1f}" for i in range(2 * n))
    defs = '<clipPath id="corner"><rect width="1080" height="960"/></clipPath>'
    sp, spw = sponsors(56, 988, 62, CREAM)
    body = f'''<rect width="{S}" height="{S}" fill="{Y1}"/>
<g id="sunburst" fill="{Y2}">{rays}</g>
<g clip-path="url(#corner)">{halftone(1080, 0, 420, 12, 5, ORANGE, 30, 1.2, id="halftone-corner")}{halftone(0, 960, 380, 12, 5, PINK, 30, 1.2, id="halftone-corner-2")}</g>
<g id="bunting">{flags}</g>
<g id="ferris-wheel">
<path d="M{wx} {wy} L{wx - 120} 962 M{wx} {wy} L{wx + 120} 962" stroke="{NAVY}" stroke-width="10" stroke-linecap="round"/>
<circle cx="{wx}" cy="{wy}" r="{wr}" fill="none" stroke="{MAG}" stroke-width="10"/><circle cx="{wx}" cy="{wy}" r="{wr - 24}" fill="none" stroke="{NAVY}" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
{spokes}{cars}{blossom(wx, wy, 50, PINK, NAVY, 0, stroke=NAVY, sw=3)}</g>
<g id="logo-sticker" transform="rotate(5 905 245)"><rect x="782" y="160" width="248" height="170" rx="22" fill="{CREAM}" stroke="{NAVY}" stroke-width="3"/>{img("udgam-logo", 796, 172, 220)}</g>
<g id="headline">
<text x="62" y="236" font-family="Space Mono" font-weight="700" font-size="20" letter-spacing="4" fill="{NAVY}">COME ONE, COME ALL!</text>
<text x="66" y="396" font-family="Shrikhand" font-size="172" fill="{NAVY}">Udgam</text>
<text x="58" y="388" font-family="Shrikhand" font-size="172" fill="{MAG}" stroke="{CREAM}" stroke-width="3" paint-order="stroke">Udgam</text>
<g transform="rotate(14 650 236)"><polygon points="{star(650, 236, 66)}" fill="{PINK}" stroke="{NAVY}" stroke-width="3"/>
<text x="650" y="250" text-anchor="middle" font-family="Anton" font-size="44" fill="{CREAM}">2K26</text></g>
<g id="ribbon"><path d="M48 428 H80 V470 H48 L62 449Z M600 428 H568 V470 H600 L586 449Z" fill="{MAG}"/>
<rect x="70" y="418" width="508" height="44" fill="{NAVY}"/>
<text x="324" y="450" text-anchor="middle" font-family="Anton" font-size="28" letter-spacing="8" fill="{CREAM}">CHASE THE BLOOM</text></g>
<text font-family="Fraunces" font-style="italic" font-size="38" fill="{NAVY}"><tspan x="62" y="536">Come for the music,</tspan><tspan x="62" y="580">stay for the magic.</tspan></text></g>
<g id="ticket" transform="rotate(-2 270 720)">
<path d="M60 630 H480 V700 a16 16 0 0 0 0 32 V810 H60 V732 a16 16 0 0 0 0 -32Z" fill="{CREAM}" stroke="{NAVY}" stroke-width="3"/>
<rect x="76" y="646" width="388" height="148" fill="none" stroke="{MAG}" stroke-width="1.5" stroke-dasharray="5 5"/>
<text x="94" y="676" font-family="Space Mono" font-weight="700" font-size="16" letter-spacing="2" fill="{MAG}">★ ADMIT ONE · ALL 3 DAYS ★</text>
<text x="92" y="740" font-family="Anton" font-size="62" fill="{NAVY}">30 · 31 OCT</text>
<text x="94" y="780" font-family="Anton" font-size="30" letter-spacing="1" fill="{MAG}">&amp; 01 NOV 2026 · NIT SIKKIM</text></g>
<text x="62" y="872" font-family="Space Mono" font-weight="700" font-size="19" letter-spacing="1" fill="{NAVY}">CONCERTS · RIDES · DANCE · GAMES · FOOD</text>
<text x="62" y="906" font-family="Inter Tight" font-weight="600" font-size="21" fill="{NAVY}">The annual cultural fest of NIT Sikkim</text>
{blossom(520, 560, 22, PINK, NAVY, 10)}{blossom(1010, 430, 18, CREAM, MAG, 30)}{petal(600, 590, 12, 50, MAG)}{petal(990, 860, 10, -20, PINK)}
<rect id="ground" y="960" width="{S}" height="120" fill="{NAVY}"/>
{sp}
{socials(1026, 1019, CREAM, "end", 1.15)}
{grain(.5)}'''
    return svg(body, ["Shrikhand", "Anton", "Fraunces", "Space Mono", "Inter Tight"], "UDGAM 2K26 — Retro Carnival", defs)


if __name__ == "__main__":
    for name, fn in [("01-riso-collage", p1), ("02-abstract-modern", p2), ("03-minimal-bloom", p3), ("04-night-concert", p4), ("05-retro-carnival", p5)]:
        (ROOT / f"{name}.svg").write_text(fn())
        print(name)
