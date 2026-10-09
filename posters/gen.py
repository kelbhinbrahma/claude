"""Generates the 5 Nasha Mukt posters as editable A4 SVGs (fonts embedded, also in ./fonts)."""
import base64, pathlib

ROOT = pathlib.Path(__file__).parent
FONTS = {  # family -> [(file, weight, style)]
    "Anton": [("Anton-400.ttf", 400, "normal")],
    "Bricolage Grotesque": [("BricolageGrotesque-800.ttf", 800, "normal")],
    "Instrument Serif": [("InstrumentSerif-400.ttf", 400, "normal"), ("InstrumentSerif-400i.ttf", 400, "italic")],
    "Inter Tight": [("InterTight-400.ttf", 400, "normal"), ("InterTight-600.ttf", 600, "normal"), ("InterTight-800.ttf", 800, "normal")],
    "Rozha One": [("RozhaOne-400.ttf", 400, "normal")],
    "Mukta": [("Mukta-400.ttf", 400, "normal"), ("Mukta-600.ttf", 600, "normal"), ("Mukta-800.ttf", 800, "normal")],
    "Yatra One": [("YatraOne-400.ttf", 400, "normal")],
    "Caveat": [("Caveat-700.ttf", 700, "normal")],
}

# palette
NAVY, BLUE, GREEN, LEAF, ORANGE, CREAM = "#0B1F5C", "#1D3FBB", "#1E8F4E", "#2BB673", "#FF6A1A", "#F4EFE6"


def svg(body, fams, title):
    css = "".join(
        f"@font-face{{font-family:'{f}';font-weight:{w};font-style:{s};src:url(data:font/ttf;base64,"
        f"{base64.b64encode((ROOT / 'fonts' / fn).read_bytes()).decode()})}}"
        for f in fams for fn, w, s in FONTS[f])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="210mm" height="297mm" viewBox="0 0 2100 2970">
<title>{title}</title>
<style>{css}</style>
<defs>
  <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncA type="table" tableValues="0 0.35"/></feComponentTransfer></filter>
</defs>
{body}
</svg>'''


def grain(op=.5):
    return f'<rect id="grain-texture" width="2100" height="2970" filter="url(#grain)" opacity="{op}" style="mix-blend-mode:multiply" pointer-events="none"/>'


def footer(fg, sub, rule, accent, y=2680):
    return f'''<g id="footer">
<line x1="110" y1="{y}" x2="1990" y2="{y}" stroke="{rule}" stroke-width="3"/>
<g id="logo-placeholder"><circle cx="200" cy="{y+120}" r="84" fill="none" stroke="{fg}" stroke-width="5"/><circle cx="200" cy="{y+120}" r="66" fill="none" stroke="{fg}" stroke-width="3" stroke-dasharray="9 9" opacity=".5"/>
<text x="200" y="{y+130}" text-anchor="middle" font-family="Inter Tight" font-weight="800" font-size="27" letter-spacing="3" fill="{fg}">LOGO</text></g>
<text x="320" y="{y+105}" font-family="Inter Tight" font-weight="800" font-size="40" fill="{fg}">National Institute of Technology Sikkim</text>
<text x="320" y="{y+172}" font-family="Mukta" font-weight="600" font-size="44" fill="{sub}">राष्ट्रीय प्रौद्योगिकी संस्थान सिक्किम</text>
<g id="helpline" font-family="Inter Tight, Mukta" font-weight="800" font-size="25" letter-spacing="4" fill="{accent}">
<text x="1340" y="{y+70}">HELPLINE · <tspan font-family="Mukta" letter-spacing="0" font-size="30">हेल्पलाइन</tspan></text>
<line x1="1340" y1="{y+125}" x2="1990" y2="{y+125}" stroke="{fg}" stroke-width="3" opacity=".7"/>
<text x="1340" y="{y+175}">SUPPORT · <tspan font-family="Mukta" letter-spacing="0" font-size="30">सहायता केंद्र</tspan></text>
<line x1="1340" y1="{y+228}" x2="1990" y2="{y+228}" stroke="{fg}" stroke-width="3" opacity=".7"/>
</g></g>'''


# ---------- 01 · Swiss "NO." ----------
def p1():
    msgs = [("01", ["Drugs destroy", "dreams"], ["नशा सपनों को", "नष्ट करता है"]),
            ("02", ["Protect your family", "and future"], ["अपने परिवार और", "भविष्य की रक्षा करें"]),
            ("03", ["Seek help,", "stay strong"], ["मदद लें,", "मजबूत रहें"])]
    cols = ""
    for i, (n, en, hi) in enumerate(msgs):
        x = 110 + i * 630
        cols += f'''<g id="message-{n}"><text x="{x}" y="2060" font-family="Anton" font-size="96" fill="{ORANGE}">{n}</text>
<text font-family="Inter Tight" font-weight="600" font-size="50" fill="#fff"><tspan x="{x}" y="2150">{en[0]}</tspan><tspan x="{x}" y="2212">{en[1]}</tspan></text>
<text font-family="Mukta" font-weight="400" font-size="44" fill="#9FE3BC"><tspan x="{x}" y="2282">{hi[0]}</tspan><tspan x="{x}" y="2340">{hi[1]}</tspan></text></g>'''
    body = f'''<rect width="2100" height="2970" fill="{NAVY}"/>
<g id="meta" font-family="Inter Tight, Mukta" font-weight="600" font-size="30" letter-spacing="6" fill="#fff" opacity=".8">
<text x="110" y="170">NASHA MUKT BHARAT  /  <tspan font-family="Mukta" letter-spacing="0" font-size="36">नशा मुक्त भारत</tspan></text>
<text x="1990" y="170" text-anchor="end">N°01 — PUBLIC AWARENESS</text></g>
<line x1="110" y1="210" x2="1990" y2="210" stroke="#fff" stroke-opacity=".25" stroke-width="3"/>
<text id="say" x="104" y="520" font-family="Inter Tight" font-weight="800" font-size="230" letter-spacing="-8" fill="{ORANGE}">Say</text>
<text id="no" x="70" y="1640" font-family="Anton" font-size="1240" letter-spacing="-16" fill="#fff">NO</text>
<circle id="dot" cx="1420" cy="1545" r="100" fill="{ORANGE}"/>
<text id="hindi-na" x="1990" y="760" text-anchor="end" font-family="Rozha One" font-size="520" fill="{LEAF}">ना</text>
<text x="1990" y="860" text-anchor="end" font-family="Inter Tight" font-weight="600" font-size="34" letter-spacing="5" fill="#fff" opacity=".7">SAY NO · CHOOSE LIFE</text>
<text id="to-drugs" x="110" y="1850" font-family="Instrument Serif" font-style="italic" font-size="230" fill="#fff">to drugs.</text>
<text x="1990" y="1840" text-anchor="end" font-family="Mukta" font-weight="800" font-size="120" fill="{LEAF}">नशे को ना कहें</text>
<line x1="110" y1="1930" x2="1990" y2="1930" stroke="#fff" stroke-opacity=".25" stroke-width="3"/>
{cols}
<g id="banner"><rect x="110" y="2400" width="1880" height="200" fill="{GREEN}"/>
<text x="160" y="2490" font-family="Inter Tight" font-weight="800" font-size="56" fill="#fff">Together we can make Sikkim Nasha Mukt</text>
<text x="160" y="2564" font-family="Mukta" font-weight="600" font-size="48" fill="#DFF7E8">मिलकर हम सिक्किम को नशा मुक्त बना सकते हैं</text>
<text x="1940" y="2540" text-anchor="end" font-family="Anton" font-size="120" fill="{NAVY}" opacity=".35">→</text></g>
{grain(.35)}
{footer("#fff", "#FFC69E", "#ffffff55", ORANGE)}'''
    return svg(body, ["Anton", "Inter Tight", "Instrument Serif", "Rozha One", "Mukta"], "Say No — Nasha Mukt Bharat")


# ---------- 02 · Riso "Break the Chain" ----------
def p2():
    RB, RG, RO, INK = "#2244C0", "#00A95C", "#FF6C2F", "#1A1F3A"
    links, y = "", -80
    for i in range(9):
        if i == 4:
            y += 210
            continue
        if i % 2 == 0:
            links += f'<rect x="-110" y="{y}" width="220" height="380" rx="110" fill="none" stroke="{RG}" stroke-width="58"/>'
        else:
            links += f'<rect x="-29" y="{y}" width="58" height="380" rx="29" fill="{RG}"/>'
        y += 260
    burst = "".join(f'<line x1="0" y1="0" x2="{dx}" y2="{dy}" stroke="{RO}" stroke-width="22" stroke-linecap="round" transform="translate(0,1125)"/>'
                    for dx, dy in [(-190, -40), (190, 30), (-150, 110), (160, -110), (-40, -170), (40, 170), (-200, 60)])
    msgs = [("Drugs destroy dreams", "नशा सपनों को नष्ट करता है"), ("Protect your family and future", "अपने परिवार और भविष्य की रक्षा करें"),
            ("Seek help, stay strong", "मदद लें, मजबूत रहें"), ("Together we can make Sikkim Nasha Mukt", "मिलकर हम सिक्किम को नशा मुक्त बना सकते हैं")]
    ml = "".join(f'''<text x="{110 + (i % 2) * 950}" y="{2290 + (i // 2) * 170}" font-family="Inter Tight" font-weight="800" font-size="40" fill="{RB}">→ {e}</text>
<text x="{168 + (i % 2) * 950}" y="{2346 + (i // 2) * 170}" font-family="Mukta" font-weight="600" font-size="40" fill="{INK}" opacity=".8">{h}</text>''' for i, (e, h) in enumerate(msgs))
    head = lambda col, dx, op: f'''<g font-family="Anton" font-size="600" letter-spacing="-6" fill="{col}" opacity="{op}" transform="translate({dx},{dx})">
<text x="95" y="900">BREAK</text><text x="95" y="1420">THE</text><text x="95" y="1940">CHAIN</text></g>'''
    body = f'''<rect width="2100" height="2970" fill="#F2EDE1"/>
<defs><pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><circle cx="15" cy="15" r="10" fill="{RO}"/></pattern>
<radialGradient id="fade"><stop offset=".55" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="sunmask"><circle cx="1480" cy="1080" r="640" fill="url(#fade)"/></mask></defs>
<circle id="halftone-sun" cx="1480" cy="1080" r="640" fill="url(#dots)" mask="url(#sunmask)" style="mix-blend-mode:multiply"/>
<g id="tag" transform="rotate(-4 400 210)"><rect x="100" y="150" width="1020" height="110" fill="{RB}"/>
<text x="130" y="228" font-family="Inter Tight" font-weight="800" font-size="46" letter-spacing="5" fill="#F2EDE1">NASHA MUKT BHARAT · <tspan font-family="Mukta" letter-spacing="0" font-size="54">नशा मुक्त भारत</tspan></text></g>
<g id="headline">{head(RO, 18, .95)}{head(RB, 0, 1)}</g>
<g id="chain" transform="translate(1660,0) rotate(14) scale(.82)" style="mix-blend-mode:multiply">{links}{burst}</g>
<text id="hindi-headline" x="100" y="2140" font-family="Yatra One" font-size="190" fill="{RG}" style="mix-blend-mode:multiply">नशे की ज़ंजीर तोड़ो</text>
<text x="1990" y="1760" text-anchor="end" font-family="Caveat" font-weight="700" font-size="92" fill="{RO}" transform="rotate(-6 1800 1750)">you are stronger!</text>
<line x1="110" y1="2205" x2="1990" y2="2205" stroke="{INK}" stroke-width="3" opacity=".6"/>
{ml}
<text x="110" y="2620" font-family="Inter Tight" font-weight="800" font-size="34" letter-spacing="8" fill="{RO}">SAY NO TO DRUGS – CHOOSE LIFE  ·  <tspan font-family="Mukta" letter-spacing="0" font-size="40">नशे को ना कहें – जीवन चुनें</tspan></text>
{grain(.6)}
{footer(INK, RB, INK, RO, 2670)}'''
    return svg(body, ["Anton", "Inter Tight", "Mukta", "Yatra One", "Caveat"], "Break the Chain — Nasha Mukt Bharat")


# ---------- 03 · Editorial serif "Choose Life." ----------
def p3():
    half = f'M-130 0 L-95 -28 L-55 8 L-15 -30 L25 6 L65 -26 L100 4 L130 -20 L130 230 A130 130 0 0 1 -130 230 Z'
    msgs = [("Drugs destroy dreams", "नशा सपनों को नष्ट करता है"), ("Protect your family and future", "अपने परिवार और भविष्य की रक्षा करें"),
            ("Seek help, stay strong", "मदद लें, मजबूत रहें"), ("Together we can make Sikkim Nasha Mukt", "मिलकर हम सिक्किम को नशा मुक्त बना सकते हैं")]
    ml = ""
    for i, (e, h) in enumerate(msgs):
        x, y = 110 + (i % 2) * 960, 2400 + (i // 2) * 140
        ml += f'''<line x1="{x}" y1="{y-60}" x2="{x+920}" y2="{y-60}" stroke="{NAVY}" stroke-width="2" opacity=".35"/>
<text x="{x}" y="{y}" font-family="Instrument Serif" font-style="italic" font-size="54" fill="{NAVY}"><tspan font-family="Inter Tight" font-style="normal" font-weight="800" font-size="26" fill="{ORANGE}">0{i+1}  </tspan>{e}</text>
<text x="{x+58}" y="{y+52}" font-family="Mukta" font-size="38" fill="{NAVY}" opacity=".75">{h}</text>'''
    body = f'''<rect width="2100" height="2970" fill="{CREAM}"/>
<g id="meta" font-family="Inter Tight" font-weight="600" font-size="28" letter-spacing="6" fill="{NAVY}">
<text x="110" y="170">N°03</text><text x="1050" y="170" text-anchor="middle">A CAMPAIGN FOR A DRUG-FREE SIKKIM</text><text x="1990" y="170" text-anchor="end">2026</text></g>
<line x1="110" y1="205" x2="1990" y2="205" stroke="{NAVY}" stroke-width="2"/>
<text x="1050" y="330" text-anchor="middle" font-family="Inter Tight" font-weight="800" font-size="72" letter-spacing="18" fill="{NAVY}">NASHA MUKT BHARAT</text>
<text x="1050" y="420" text-anchor="middle" font-family="Mukta" font-weight="600" font-size="64" fill="{GREEN}">नशा मुक्त भारत</text>
<g id="illustration">
<circle cx="1050" cy="1110" r="520" fill="#E3EDDC"/>
<circle cx="1050" cy="1110" r="520" fill="none" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 14" transform="rotate(10 1050 1110)"/>
<ellipse cx="1050" cy="1520" rx="430" ry="34" fill="{NAVY}" opacity=".12"/>
<g id="sprout" fill="none" stroke-linecap="round">
<path d="M1050 1400 C1040 1220 1080 1080 1040 860" stroke="{GREEN}" stroke-width="26"/>
<path d="M1046 1010 C900 1010 790 920 760 780 C900 780 1010 860 1046 1010Z" fill="{GREEN}" stroke="none"/>
<path d="M1060 920 C1180 900 1290 810 1320 660 C1180 680 1080 770 1060 920Z" fill="{LEAF}" stroke="none"/>
<path d="M1040 862 C1000 780 1010 700 1060 640 C1100 710 1090 790 1040 862Z" fill="{GREEN}" stroke="none"/>
<path d="M1046 1010 C960 980 870 920 820 840" stroke="#fff" stroke-width="5" opacity=".6"/>
<path d="M1060 920 C1140 890 1220 820 1270 730" stroke="#fff" stroke-width="5" opacity=".6"/></g>
<g id="capsule-left" transform="translate(800,1360) rotate(-58)"><path d="{half}" fill="{ORANGE}"/></g>
<g id="capsule-right" transform="translate(1310,1370) rotate(56)"><path d="{half}" fill="#fff" stroke="{NAVY}" stroke-width="14" stroke-linejoin="round"/></g>
<g fill="{NAVY}"><circle cx="700" cy="1512" r="9"/><circle cx="745" cy="1526" r="5"/><circle cx="1500" cy="1520" r="8"/><circle cx="1545" cy="1508" r="5"/></g>
</g>
<text id="headline" x="1050" y="1990" text-anchor="middle" font-family="Instrument Serif" font-size="400" letter-spacing="-8" fill="{NAVY}">Choose <tspan font-style="italic" fill="{GREEN}">Life.</tspan></text>
<text x="1050" y="2210" text-anchor="middle" font-family="Rozha One" font-size="190" fill="{ORANGE}">जीवन चुनें</text>
<text x="1050" y="2290" text-anchor="middle" font-family="Inter Tight" font-weight="800" font-size="30" letter-spacing="10" fill="{NAVY}">SAY NO TO DRUGS  ·  <tspan font-family="Mukta" letter-spacing="0" font-size="38">नशे को ना कहें</tspan></text>
{ml}
{grain(.3)}
{footer(NAVY, GREEN, NAVY, ORANGE)}'''
    return svg(body, ["Inter Tight", "Instrument Serif", "Rozha One", "Mukta"], "Choose Life — Nasha Mukt Bharat")


# ---------- 04 · Sikkim mountains ----------
def p4():
    import math, random
    random.seed(7)
    stars = "".join(f'<circle cx="{random.randint(0,2100)}" cy="{random.randint(0,1100)}" r="{random.choice([2,3,3,4,5])}" fill="#fff" opacity="{random.choice([.4,.6,.9])}"/>' for _ in range(90))
    cols = ["#2E5BD8", "#FFFFFF", "#E8402A", "#1E8F4E", "#FFC21A"]
    flags = ""
    for i in range(24):
        t = i / 23
        x, y = -20 + t * 2140, 300 + 170 * math.sin(math.pi * t) - 120 * t
        flags += f'<path d="M{x:.0f} {y:.0f} l64 6 l-4 90 l-60 -6Z" fill="{cols[i % 5]}" opacity=".95"/>'
    msgs = [("Drugs destroy dreams", "नशा सपनों को नष्ट करता है"), ("Protect your family and future", "अपने परिवार और भविष्य की रक्षा करें"),
            ("Seek help, stay strong", "मदद लें, मजबूत रहें"), ("Say No to Drugs – Choose Life", "नशे को ना कहें – जीवन चुनें")]
    ml = "".join(f'''<circle cx="{126 + (i % 2) * 950}" cy="{2318 + (i // 2) * 150}" r="14" fill="{ORANGE}"/>
<text x="{165 + (i % 2) * 950}" y="{2333 + (i // 2) * 150}" font-family="Inter Tight" font-weight="600" font-size="44" fill="#fff">{e}</text>
<text x="{165 + (i % 2) * 950}" y="{2388 + (i // 2) * 150}" font-family="Mukta" font-size="40" fill="#BFE9CF">{h}</text>''' for i, (e, h) in enumerate(msgs))
    body = f'''<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#060F33"/><stop offset=".35" stop-color="#14327E"/><stop offset=".52" stop-color="#C8566A"/><stop offset=".62" stop-color="#FF9A4D"/></linearGradient>
<radialGradient id="sunglow"><stop offset="0" stop-color="#FFE3B0"/><stop offset=".4" stop-color="#FFB46B" stop-opacity=".6"/><stop offset="1" stop-color="#FF8A3D" stop-opacity="0"/></radialGradient></defs>
<rect width="2100" height="2970" fill="url(#sky)"/>
<g id="stars">{stars}</g>
<circle cx="1050" cy="1720" r="620" fill="url(#sunglow)"/><circle id="sun" cx="1050" cy="1720" r="250" fill="#FFE1A8"/>
<g id="prayer-flags"><path d="M-20 300 Q1050 700 2120 180" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3"/>{flags}</g>
<text x="1050" y="150" text-anchor="middle" font-family="Inter Tight" font-weight="600" font-size="30" letter-spacing="10" fill="#fff" opacity=".85">NASHA MUKT BHARAT · <tspan font-family="Mukta" letter-spacing="0" font-size="38">नशा मुक्त भारत</tspan></text>
<text x="1050" y="720" text-anchor="middle" font-family="Instrument Serif" font-style="italic" font-size="150" fill="#fff">Together, let’s make</text>
<text id="sikkim" x="1050" y="1290" text-anchor="middle" font-family="Anton" font-size="640" letter-spacing="10" fill="#fff">SIKKIM</text>
<text id="nasha-mukt" x="1050" y="1580" text-anchor="middle" font-family="Anton" font-size="320" letter-spacing="24" fill="#FFE1A8">NASHA MUKT</text>
<g id="mountains">
<g transform="translate(0,230)"><path d="M0 1700 L180 1560 L300 1620 L470 1440 L610 1560 L760 1380 L860 1470 L940 1330 L1060 1460 L1180 1350 L1330 1520 L1500 1420 L1640 1560 L1820 1470 L2100 1620 V2970 H0Z" fill="#8FA4D8"/>
<path d="M760 1380 L700 1452 L740 1440 L770 1470 L800 1430 L825 1440Z M940 1330 L890 1390 L925 1380 L950 1410 L985 1375 L1010 1384Z M1180 1350 L1140 1395 L1170 1388 L1195 1410 L1220 1385 L1245 1392Z M470 1440 L430 1490 L465 1480 L490 1500 L520 1478Z" fill="#fff"/>
<path d="M0 1820 L260 1660 L420 1740 L640 1600 L860 1760 L1100 1640 L1340 1780 L1580 1650 L1820 1760 L2100 1680 V2970 H0Z" fill="#2B4A9E"/></g>
<path d="M0 1960 Q300 1820 620 1900 T1240 1880 T2100 1840 V2970 H0Z" fill="#1E7A4C"/>
<path d="M0 2090 Q500 1960 1050 2050 T2100 2000 V2970 H0Z" fill="#0D4A31"/>
</g>
<text x="1050" y="2210" text-anchor="middle" font-family="Mukta" font-weight="800" font-size="84" fill="#fff">मिलकर हम सिक्किम को नशा मुक्त बना सकते हैं</text>
{ml}
{grain(.3)}
{footer("#fff", "#FFC69E", "#ffffff55", "#FFB46B", 2630)}'''
    return svg(body, ["Anton", "Inter Tight", "Instrument Serif", "Mukta"], "Sikkim Nasha Mukt — Nasha Mukt Bharat")


# ---------- 05 · Bold "Be the Change" ----------
def p5():
    stamp_txt = "STAY DRUG FREE ★ नशा मुक्त रहें ★ STAY DRUG FREE ★ नशा मुक्त रहें ★ "
    pills = [("Drugs destroy dreams", "नशा सपनों को नष्ट करता है", NAVY, "#fff", "#BFD0FF"),
             ("Protect your family &amp; future", "अपने परिवार और भविष्य की रक्षा करें", "none", NAVY, GREEN),
             ("Seek help, stay strong", "मदद लें, मजबूत रहें", "none", NAVY, GREEN),
             ("Say No to Drugs – Choose Life", "नशे को ना कहें – जीवन चुनें", ORANGE, "#fff", "#FFE6D4")]
    pl = ""
    for i, (e, h, bg, fg, sub) in enumerate(pills):
        x, y = 110 + (i % 2) * 950, 2060 + (i // 2) * 200
        pl += f'''<g id="sticker-{i+1}"><rect x="{x}" y="{y}" width="930" height="170" rx="85" fill="{bg}" stroke="{NAVY}" stroke-width="5"/>
<text x="{x+465}" y="{y+75}" text-anchor="middle" font-family="Inter Tight" font-weight="800" font-size="44" fill="{fg}">{e}</text>
<text x="{x+465}" y="{y+132}" text-anchor="middle" font-family="Mukta" font-weight="600" font-size="40" fill="{sub}">{h}</text></g>'''
    body = f'''<rect width="2100" height="2970" fill="#F4F0E8"/>
<g id="meta" font-family="Inter Tight" font-weight="600" font-size="30" letter-spacing="6" fill="{NAVY}">
<text x="110" y="170">NASHA MUKT BHARAT · <tspan font-family="Mukta" letter-spacing="0" font-size="38">नशा मुक्त भारत</tspan></text><text x="1990" y="170" text-anchor="end">N°05</text></g>
<text id="be-the" x="96" y="700" font-family="Bricolage Grotesque" font-weight="800" font-size="520" letter-spacing="-26" fill="{NAVY}">Be the</text>
<g id="change" transform="rotate(-4 1050 1030)"><rect x="40" y="800" width="2020" height="470" fill="{GREEN}"/>
<text x="1050" y="1180" text-anchor="middle" font-family="Bricolage Grotesque" font-weight="800" font-size="470" letter-spacing="-22" fill="#fff">change.</text></g>
<g id="annotation" fill="none" stroke="{ORANGE}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round">
<path d="M1660 330 C1720 420 1740 480 1700 560"/><path d="M1662 524 L1700 566 L1740 518"/></g>
<text x="1560" y="300" font-family="Caveat" font-weight="700" font-size="96" fill="{ORANGE}" transform="rotate(-8 1660 300)">yes, you!</text>
<g id="stamp" transform="translate(1720,1420)">
<circle r="270" fill="{ORANGE}"/><circle r="200" fill="none" stroke="#fff" stroke-width="4" stroke-dasharray="2 12"/>
<path id="ring" d="M0 -222 A222 222 0 1 1 -0.1 -222" fill="none"/>
<text font-family="Inter Tight, Mukta" font-weight="800" font-size="34" fill="#fff"><textPath href="#ring" xlink:href="#ring" textLength="1360" lengthAdjust="spacing">{stamp_txt}</textPath></text>
<text y="70" text-anchor="middle" font-family="Rozha One" font-size="210" fill="#fff">ना</text></g>
<text id="hindi-headline" x="100" y="1650" font-family="Yatra One" font-size="300" fill="{NAVY}">बदलाव बनें</text>
<text x="110" y="1850" font-family="Mukta" font-weight="800" font-size="130" fill="{GREEN}">नशा मुक्त रहें</text>
<text x="1990" y="1950" text-anchor="end" font-family="Inter Tight" font-weight="800" font-size="40" letter-spacing="8" fill="{NAVY}">BE THE CHANGE – STAY DRUG FREE</text>
{pl}
<g id="banner"><rect x="110" y="2460" width="1880" height="150" rx="75" fill="{GREEN}"/>
<text x="1050" y="2532" text-anchor="middle" font-family="Inter Tight" font-weight="800" font-size="46" fill="#fff">Together we can make Sikkim Nasha Mukt</text>
<text x="1050" y="2586" text-anchor="middle" font-family="Mukta" font-weight="600" font-size="40" fill="#DFF7E8">मिलकर हम सिक्किम को नशा मुक्त बना सकते हैं</text></g>
{grain(.3)}
{footer(NAVY, GREEN, NAVY, ORANGE)}'''
    return svg(body, ["Bricolage Grotesque", "Inter Tight", "Rozha One", "Mukta", "Yatra One", "Caveat"], "Be the Change — Nasha Mukt Bharat")


if __name__ == "__main__":
    names = ["01-say-no", "02-break-the-chain", "03-choose-life", "04-sikkim-nasha-mukt", "05-be-the-change"]
    for n, f in zip(names, [p1, p2, p3, p4, p5]):
        (ROOT / f"{n}.svg").write_text(f())
        print(n)
