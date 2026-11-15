"""Illustrazioni vettoriali PadelMetrix per guide e schede (disegnate a mano in SVG, colori del marchio).

Ogni illustrazione è una scena 320x180 su sfondo pieno: verde scuro, lime o crema. Nessuna immagine esterna,
quindi le pagine restano leggere e le illustrazioni si vedono anche senza connessione alle CDN."""

G, GD, LI, CR, SO, IN = "#0F3D2E", "#0B2E23", "#C6F432", "#FAFAF7", "#EEF2EC", "#1F2D27"

TESTE = {
    "rotonda": "M100 18 C150 18 178 52 178 104 C178 156 146 188 100 196 C54 188 22 156 22 104 C22 52 50 18 100 18 Z",
    "goccia": "M100 14 C146 14 176 44 178 92 C180 140 150 182 100 198 C50 182 20 140 22 92 C24 44 54 14 100 14 Z",
    "diamante": "M100 14 C128 14 156 30 170 58 C182 82 178 116 162 146 C146 174 122 190 100 198 C78 190 54 174 38 146 C22 116 18 82 30 58 C44 30 72 14 100 14 Z",
}
FORI = [(76, 62), (100, 62), (124, 62), (64, 84), (88, 84), (112, 84), (136, 84), (64, 106), (88, 106), (112, 106), (136, 106), (76, 128), (100, 128), (124, 128), (88, 150), (112, 150)]


def racchetta(x, y, s, forma="goccia", corpo=G, bordo=LI, ang=0, fori=CR):
    """Racchetta (viewBox 200x300) posizionata in (x, y) con scala s e rotazione ang."""
    d = TESTE[forma]
    f = "".join(f'<circle cx="{a}" cy="{b}" r="4.5" fill="{fori}" fill-opacity=".55"/>' for a, b in FORI)
    return (f'<g transform="translate({x} {y}) rotate({ang}) scale({s}) translate(-100 -150)">'
            f'<path d="{d}" fill="{corpo}"/><path d="{d}" fill="none" stroke="{bordo}" stroke-width="6"/>{f}'
            f'<path d="M84 194 L100 214 L116 194 Z" fill="{corpo}" stroke="{bordo}" stroke-width="5" stroke-linejoin="round"/><rect x="88" y="208" width="24" height="80" rx="8" fill="{corpo}" stroke="{bordo}" stroke-width="5"/>'
            f'<rect x="88" y="238" width="24" height="5" fill="{bordo}"/><rect x="88" y="254" width="24" height="5" fill="{bordo}"/></g>')


def palla(x, y, r, c=LI, riga=G):
    return (f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
            f'<path d="M{x - r * .72} {y - r * .7} C{x - r * .1} {y - r * .25} {x - r * .1} {y + r * .25} {x - r * .72} {y + r * .7}" fill="none" stroke="{riga}" stroke-width="{max(1.5, r * .12)}" stroke-opacity=".55"/>'
            f'<path d="M{x + r * .72} {y - r * .7} C{x + r * .1} {y - r * .25} {x + r * .1} {y + r * .25} {x + r * .72} {y + r * .7}" fill="none" stroke="{riga}" stroke-width="{max(1.5, r * .12)}" stroke-opacity=".55"/>')


def campo(c=LI, op=".18"):
    """Linee di un campo da padel visto dall'alto, come texture di sfondo."""
    return (f'<g fill="none" stroke="{c}" stroke-opacity="{op}" stroke-width="3">'
            '<rect x="-20" y="22" width="360" height="136" rx="6"/><line x1="160" y1="22" x2="160" y2="158" stroke-width="5"/>'
            '<line x1="70" y1="22" x2="70" y2="158"/><line x1="250" y1="22" x2="250" y2="158"/><line x1="70" y1="90" x2="250" y2="90"/></g>')


def scena(sfondo, contenuto, label):
    return (f'<svg viewBox="0 0 320 180" role="img" aria-label="{label}" preserveAspectRatio="xMidYMid slice">'
            f'<rect width="320" height="180" fill="{sfondo}"/>{contenuto}</svg>')


def _principianti():
    return scena(G, campo() + racchetta(120, 98, .5, "rotonda", ang=-14) +
                 palla(214, 64, 20) + '<path d="M196 112 l6 14 l14 6 l-14 6 l-6 14 l-6 -14 l-14 -6 l14 -6 z" fill="#C6F432"/>'
                 '<path d="M246 116 l4 9 l9 4 l-9 4 l-4 9 l-4 -9 l-9 -4 l9 -4 z" fill="#C6F432" fill-opacity=".7"/>', "Prima racchetta")


def _epicondilite():
    braccio = (f'<path d="M30 150 C70 140 110 128 150 108 C170 98 186 82 204 66" fill="none" stroke="{G}" stroke-width="30" stroke-linecap="round"/>'
               f'<path d="M204 66 C214 56 224 48 238 44" fill="none" stroke="{G}" stroke-width="22" stroke-linecap="round"/>')
    onde = "".join(f'<circle cx="150" cy="108" r="{r}" fill="none" stroke="{LI if i else G}" stroke-width="4" stroke-opacity="{.9 - i * .25}"/>' for i, r in enumerate((12, 26, 40)))
    return scena(SO, braccio + onde + f'<circle cx="150" cy="108" r="8" fill="{LI}" stroke="{G}" stroke-width="3"/>' +
                 racchetta(262, 46, .32, "rotonda", ang=30), "Gomito e braccio")


def _forme():
    return scena(CR, racchetta(70, 92, .42, "rotonda") + racchetta(160, 92, .42, "goccia") + racchetta(250, 92, .42, "diamante") +
                 "".join(f'<rect x="{x - 26}" y="160" width="52" height="8" rx="4" fill="{c}"/>' for x, c in ((70, LI), (160, G), (250, LI))), "Tre forme di racchetta")


def _donna():
    piuma = (f'<path d="M232 30 C196 52 180 98 188 150 C214 120 238 80 232 30 Z" fill="{LI}"/>'
             f'<path d="M230 36 C214 72 200 110 190 148" fill="none" stroke="{G}" stroke-width="3"/>'
             + "".join(f'<path d="M{216 - i * 5} {64 + i * 18} l-14 6" stroke="{G}" stroke-width="2"/>' for i in range(4)))
    return scena(G, campo(op=".12") + racchetta(118, 94, .46, "goccia", ang=-10) + piuma, "Racchetta leggera")


def _economiche():
    moneta = (f'<circle cx="214" cy="96" r="44" fill="{LI}"/><circle cx="214" cy="96" r="34" fill="none" stroke="{G}" stroke-width="3" stroke-dasharray="6 5"/>'
              f'<text x="214" y="114" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="50" fill="{G}">€</text>')
    return scena(SO, racchetta(106, 94, .46, "rotonda", ang=-18) + moneta +
                 f'<circle cx="262" cy="148" r="16" fill="{G}"/><text x="262" y="154" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="17" fill="{LI}">€</text>', "Racchette economiche")


def _controllo():
    bersaglio = "".join(f'<circle cx="190" cy="90" r="{r}" fill="{c}"/>' for r, c in ((70, G), (52, CR), (34, G), (16, LI)))
    return scena(CR, bersaglio + palla(196, 84, 11, CR, G) +
                 f'<path d="M40 150 C80 120 120 100 182 88" fill="none" stroke="{G}" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>', "Precisione e controllo")


def _potenza():
    scie = "".join(f'<path d="M{40 + i * 6} {70 + i * 22} L{168 - i * 4} {84 + i * 8}" stroke="{LI}" stroke-width="{7 - i * 1.5}" stroke-linecap="round" stroke-opacity="{.9 - i * .2}"/>' for i in range(4))
    fulmine = f'<path d="M254 26 L224 92 L246 92 L230 154 L278 74 L254 74 L270 26 Z" fill="{LI}"/>'
    return scena(G, scie + palla(188, 92, 26) + fulmine, "Potenza e smash")


def _pro():
    coppa = (f'<path d="M126 36 H194 V72 C194 98 178 114 160 116 C142 114 126 98 126 72 Z" fill="{LI}"/>'
             f'<path d="M126 46 C100 46 100 82 128 86 M194 46 C220 46 220 82 192 86" fill="none" stroke="{LI}" stroke-width="7"/>'
             f'<rect x="152" y="114" width="16" height="22" fill="{LI}"/><rect x="128" y="136" width="64" height="14" rx="4" fill="{LI}"/>'
             f'<path d="M160 52 l5 11 l12 1 l-9 8 l3 12 l-11 -6 l-11 6 l3 -12 l-9 -8 l12 -1 z" fill="{G}"/>')
    return scena(G, campo(op=".1") + racchetta(62, 98, .34, "diamante", ang=-24) + racchetta(258, 98, .34, "diamante", ang=24) + coppa, "Racchette dei professionisti")


def _bambini():
    return scena(SO, racchetta(126, 92, .5, "goccia", ang=-8) + racchetta(214, 112, .32, "rotonda", corpo=LI, bordo=G, fori=G, ang=12) +
                 palla(262, 52, 13, G, LI), "Racchette per bambini")


def _peso():
    bilancia = (f'<rect x="156" y="40" width="8" height="112" fill="{G}"/><rect x="124" y="150" width="72" height="10" rx="5" fill="{G}"/>'
                f'<path d="M70 62 L250 50" stroke="{G}" stroke-width="7" stroke-linecap="round"/><circle cx="160" cy="56" r="9" fill="{LI}" stroke="{G}" stroke-width="3"/>'
                f'<path d="M70 62 L48 108 H92 Z M250 50 L228 96 H272 Z" fill="none" stroke="{G}" stroke-width="3"/>'
                f'<path d="M44 108 H96 C96 124 44 124 44 108 Z M224 96 H276 C276 112 224 112 224 96 Z" fill="{G}"/>')
    return scena(LI, bilancia + palla(70, 96, 11, CR, G) + palla(250, 76, 15, CR, G), "Peso e bilanciamento")


def _over50():
    return scena(G, campo(op=".12") + racchetta(110, 94, .46, "rotonda", ang=-12) +
                 f'<circle cx="222" cy="88" r="46" fill="{LI}"/><text x="222" y="104" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="40" fill="{G}">50+</text>', "Padel dopo i 50 anni")


def _carbonio():
    trama = "".join(f'<rect x="{x}" y="{y}" width="26" height="26" fill="{G if (x // 26 + y // 26) % 2 else GD}"/>'
                    for x in range(0, 320, 26) for y in range(0, 182, 26))
    lab = "".join(f'<g><rect x="{x}" y="70" width="78" height="42" rx="21" fill="{c}"/><text x="{x + 39}" y="99" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="22" fill="{t}">{s}</text></g>'
                  for x, s, c, t in ((24, "3K", CR, G), (121, "12K", LI, G), (218, "18K", CR, G)))
    return scena(G, trama + lab, "Fibra di carbonio")


def _durata():
    clessidra = (f'<path d="M126 30 H194 M126 150 H194" stroke="{G}" stroke-width="8" stroke-linecap="round"/>'
                 f'<path d="M134 34 C134 70 160 78 160 90 C160 102 134 110 134 146 H186 C186 110 160 102 160 90 C160 78 186 70 186 34 Z" fill="{CR}" stroke="{G}" stroke-width="4"/>'
                 f'<path d="M142 50 H178 C174 66 164 74 160 80 C156 74 146 66 142 50 Z M140 142 C146 120 156 112 160 108 C164 112 174 120 180 142 Z" fill="{LI}" stroke="{G}" stroke-width="2"/>')
    return scena(SO, clessidra + racchetta(250, 96, .3, "goccia", ang=18) + racchetta(70, 96, .3, "goccia", ang=-18), "Quanto dura una racchetta")


def _scarpe():
    suola = f'<path d="M58 54 C110 34 220 40 262 70 C284 86 280 128 248 134 C190 146 104 142 66 126 C38 114 34 66 58 54 Z" fill="{G}"/>'
    spina = "".join(f'<path d="M{x} 66 l10 12 l-10 12 M{x} 92 l10 12 l-10 12" fill="none" stroke="{LI}" stroke-width="5" stroke-linecap="round"/>' for x in range(80, 250, 22))
    return scena(CR, suola + spina, "Suola a spina di pesce")


def _regole():
    c = (f'<rect x="40" y="26" width="240" height="128" rx="4" fill="{G}"/><g fill="none" stroke="{CR}" stroke-width="3">'
         '<line x1="160" y1="26" x2="160" y2="154" stroke-width="5"/><line x1="94" y1="26" x2="94" y2="154"/><line x1="226" y1="26" x2="226" y2="154"/>'
         '<line x1="94" y1="90" x2="226" y2="90"/></g>'
         f'<path d="M70 132 C110 40 150 40 196 70" fill="none" stroke="{LI}" stroke-width="3" stroke-dasharray="3 7" stroke-linecap="round"/>')
    return scena(LI, c + palla(200, 72, 9), "Campo e regole")


def _quiz():
    righe = "".join(f'<rect x="132" y="{y}" width="{w}" height="12" rx="6" fill="{G}" fill-opacity=".85"/>'
                    f'<rect x="102" y="{y - 4}" width="20" height="20" rx="6" fill="{LI if i < 2 else CR}" stroke="{G}" stroke-width="3"/>'
                    + (f'<path d="M106 {y + 6} l5 5 l9 -10" fill="none" stroke="{G}" stroke-width="3.5" stroke-linecap="round"/>' if i < 2 else "")
                    for i, (y, w) in enumerate(((50, 96), (82, 74), (114, 88))))
    return scena(SO, f'<rect x="84" y="26" width="168" height="130" rx="14" fill="{CR}" stroke="{G}" stroke-width="4"/>' + righe +
                 f'<circle cx="252" cy="140" r="26" fill="{G}"/><text x="252" y="151" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="30" fill="{LI}">?</text>', "Test della racchetta")


def _offerte():
    etichetta = (f'<path d="M150 40 H244 C252 40 258 46 258 54 V126 C258 134 252 140 244 140 H150 L112 90 Z" fill="{LI}"/>'
                 f'<circle cx="138" cy="90" r="8" fill="{G}"/>'
                 f'<text x="196" y="104" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="40" fill="{G}">−%</text>')
    return scena(G, campo(op=".1") + racchetta(64, 96, .34, "goccia", ang=-20) + etichetta, "Offerte")


def _confronto():
    return scena(CR, racchetta(98, 92, .44, "diamante", ang=-12) + racchetta(222, 92, .44, "diamante", corpo=LI, bordo=G, fori=G, ang=12) +
                 f'<circle cx="160" cy="92" r="24" fill="{G}"/><text x="160" y="100" text-anchor="middle" font-family="Space Grotesk,Arial,sans-serif" font-weight="700" font-size="20" fill="{LI}">VS</text>', "Confronto tra racchette")


ILL = {
    "principianti": _principianti, "epicondilite": _epicondilite, "forme": _forme, "donna": _donna, "economiche": _economiche,
    "controllo": _controllo, "potenza": _potenza, "pro": _pro, "bambini": _bambini, "peso": _peso, "over50": _over50,
    "carbonio": _carbonio, "durata": _durata, "scarpe": _scarpe, "regole": _regole, "quiz": _quiz, "offerte": _offerte, "confronto": _confronto,
}


def ill(k):
    return ILL[k]()


def eroe():
    """Illustrazione grande per la testata della pagina guide: tre racchette, la palla e il percorso."""
    return (f'<svg viewBox="0 0 520 300" role="img" aria-label="Racchette da padel" preserveAspectRatio="xMidYMid meet">'
            f'<g fill="none" stroke="{LI}" stroke-opacity=".22" stroke-width="3"><rect x="20" y="40" width="480" height="230" rx="10"/>'
            '<line x1="260" y1="40" x2="260" y2="270" stroke-width="6"/><line x1="140" y1="40" x2="140" y2="270"/><line x1="380" y1="40" x2="380" y2="270"/><line x1="140" y1="155" x2="380" y2="155"/></g>'
            + racchetta(150, 168, .7, "rotonda", ang=-16) + racchetta(268, 150, .78, "goccia") + racchetta(388, 168, .7, "diamante", ang=16, corpo=LI, bordo=CR, fori=G)
            + f'<path d="M60 250 C120 120 300 30 452 64" fill="none" stroke="{LI}" stroke-width="4" stroke-dasharray="3 10" stroke-linecap="round"/>'
            + palla(456, 62, 20) + '</svg>')
