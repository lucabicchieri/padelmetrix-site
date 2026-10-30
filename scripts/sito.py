"""Struttura comune delle pagine del sito in tre lingue: dati normalizzati, layout, schede-card, coppie di confronto, percorsi.

La lingua corrente si imposta con set_lang("it"|"en"|"es"); L(it, en, es) sceglie il testo, P(sezione, slug) il percorso.
"""
import html
import json
import pathlib
import re

from comune import racket_svg
import traduci as T
import consenso as C

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "racchette"
SITO = "https://www.padelmetrix.com"
LINGUE = ("it", "en", "es")
e = html.escape

_LANG = ["it"]


def set_lang(l):
    _LANG[0] = l


def lang():
    return _LANG[0]


def L(it, en, es):
    return {"it": it, "en": en, "es": es}[_LANG[0]]


def tr(x):
    """Traduce un testo dei dati (scritto in italiano) nella lingua corrente."""
    return T.t(x, _LANG[0]) if isinstance(x, str) else x


# ---------------------------------------------------------------- date e numeri

MESI = {"it": ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre", "novembre", "dicembre"],
        "en": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
        "es": ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]}
OGGI = "2026-10-24"


def data_txt(iso=OGGI):
    y, m, d = (int(x) for x in iso.split("-"))
    mese = MESI[_LANG[0]][m - 1]
    return L(f"{d} {mese} {y}", f"{d} {mese} {y}", f"{d} de {mese} de {y}")


def data_it_to_iso(txt):
    m = re.match(r"(\d+) (\w+) (\d{4})", txt or "")
    if not m:
        return OGGI
    return f"{m.group(3)}-{MESI['it'].index(m.group(2)) + 1:02d}-{int(m.group(1)):02d}"


OGGI_TXT = "24 ottobre 2026"


def euro(x, dec=True):
    """Prezzo nel formato della lingua: 1.234,5 € (it/es), €1,234.5 (en)."""
    if dec:
        s = f"{x:,.2f}"
        if s.endswith(".00"):
            s = s[:-3]
    else:
        s = f"{x:,.0f}"
    if _LANG[0] == "en":
        return "€" + s
    return s.replace(",", "X").replace(".", ",").replace("X", ".") + " €"


def numero(v):
    s = f"{v:g}"
    return s if _LANG[0] == "en" else s.replace(".", ",")


# ---------------------------------------------------------------- percorsi

SEZ = {
    "home": ("", "", ""),
    "racchette": ("racchette", "rackets", "palas"),
    "marche": ("marche", "brands", "marcas"),
    "confronta": ("confronta", "compare", "comparar"),
    "guide": ("guide", "guides", "guias"),
    "bambini": ("bambini", "kids", "ninos"),
    "abbigliamento": ("abbigliamento", "clothing", "ropa"),
    "chi-siamo": ("chi-siamo", "about", "quienes-somos"),
    "report": ("report", "report", "informe"),
    "dati": ("dati", "data", "datos"),
    "glossario": ("glossario", "glossary", "glosario"),
    "domande": ("domande", "questions", "preguntas"),
    "pickleball": ("pickleball", "pickleball", "pickleball"),
    "selettore": ("trova-la-tua-racchetta", "racket-finder", "encuentra-tu-pala"),
    "articoli": ("articoli", "articles", "articulos"),
    "privacy": ("privacy", "privacy", "privacidad"),
    "cookie": ("cookie", "cookies", "cookies"),
}

# slug italiani -> (inglese, spagnolo)
SLUG = {
    "racchetta-padel-principianti": ("padel-racket-for-beginners", "pala-padel-principiantes"),
    "racchetta-padel-epicondilite": ("padel-racket-tennis-elbow", "pala-padel-epicondilitis"),
    "forme-racchetta-padel": ("padel-racket-shapes", "formas-pala-padel"),
    "racchette-padel-donna": ("womens-padel-rackets", "palas-padel-mujer"),
    "racchette-padel-economiche": ("cheap-padel-rackets", "palas-padel-baratas"),
    "racchette-padel-controllo": ("control-padel-rackets", "palas-padel-control"),
    "racchette-padel-potenza": ("power-padel-rackets", "palas-padel-potencia"),
    "racchette-giocatori-professionisti": ("pro-players-padel-rackets", "palas-jugadores-profesionales"),
    "racchette-padel-2026-2027-in-numeri": ("padel-rackets-2026-2027-in-numbers", "palas-padel-2026-2027-en-cifras"),
    "racchette-padel-2027-novita-per-marca": ("padel-rackets-2027-whats-new-by-brand", "palas-padel-2027-novedades-por-marca"),
    "siux-diablo-pro-2026-vs-2027-cosa-cambia": ("siux-diablo-pro-2026-vs-2027-whats-changed", "siux-diablo-pro-2026-vs-2027-que-cambia"),
    "bilanciamento": ("balance", "balance"),
    "swingweight": ("swingweight", "swingweight"),
    "sweet-spot": ("sweet-spot", "punto-dulce"),
    "eva": ("eva-rubber", "goma-eva"),
    "foam": ("foam", "foam"),
    "carbonio-3k-12k-18k": ("carbon-3k-12k-18k", "carbono-3k-12k-18k"),
    "fibra-di-vetro": ("fiberglass", "fibra-de-vidrio"),
    "racchetta-diamante": ("diamond-racket", "pala-diamante"),
    "racchetta-rotonda": ("round-racket", "pala-redonda"),
    "racchetta-goccia": ("teardrop-racket", "pala-lagrima"),
    "superficie-ruvida": ("rough-face", "superficie-rugosa"),
    "misure-regolamentari": ("official-dimensions", "medidas-reglamentarias"),
    "quanto-pesa-una-racchetta-da-padel": ("how-much-does-a-padel-racket-weigh", "cuanto-pesa-una-pala-de-padel"),
    "quanto-costa-una-racchetta-da-padel": ("how-much-does-a-padel-racket-cost", "cuanto-cuesta-una-pala-de-padel"),
    "forma-racchetta-padel-piu-diffusa": ("most-common-padel-racket-shape", "forma-de-pala-de-padel-mas-comun"),
}


def _slug(s, l):
    if s is None:
        return None
    if l == "it":
        return s
    if s in SLUG:
        return SLUG[s][0 if l == "en" else 1]
    m = re.match(r"racchetta-(.+)$", s)
    if m and not s.startswith("racchetta-padel"):
        return f"{m.group(1)}-padel-racket" if l == "en" else f"pala-{m.group(1)}"
    return s


def P(sez, slug=None, l=None):
    """Percorso di una pagina nella lingua indicata (o in quella corrente)."""
    l = l or _LANG[0]
    base = f"/{l}/" + (SEZ[sez][LINGUE.index(l)] + "/" if SEZ[sez][LINGUE.index(l)] else "")
    s = _slug(slug, l)
    return base + (f"{s}/" if s else "")


def ALT(sez, slug=None):
    return {l: P(sez, slug, l) for l in LINGUE}


def loc(u):
    """Converte un link interno italiano (/it/... o /racchette/...) nel percorso della lingua corrente."""
    if not u or u.startswith("http") or u.startswith("#"):
        return u
    q = ""
    if "?" in u:
        u, q = u.split("?", 1)
        q = "?" + q
    if u.startswith("/racchette/") or u.startswith("/confronta/"):
        u = "/it" + u
    parts = [x for x in u.strip("/").split("/") if x]
    if not parts or parts[0] != "it":
        return u + q
    rev = {v[0]: k for k, v in SEZ.items() if v[0]}
    if len(parts) == 1:
        return P("home") + q
    sez = rev.get(parts[1])
    if not sez:
        return u + q
    slug = parts[2] if len(parts) > 2 else None
    return P(sez, slug) + q


def loc_html(s):
    """Riscrive i link interni italiani dentro un frammento HTML."""
    if not s or _LANG[0] == "it":
        return s
    return re.sub(r'href="(/[^"]*)"', lambda m: f'href="{loc(m.group(1))}"', s)


# ---------------------------------------------------------------- vocabolario dei dati

FORMA_IT = {"diamante": "Diamante", "rotonda": "Rotonda", "goccia": "Goccia", "ibrida": "Ibrida"}
_FORMA = {"diamante": ("Diamante", "Diamond", "Diamante"), "rotonda": ("Rotonda", "Round", "Redonda"),
          "goccia": ("Goccia", "Teardrop", "Lágrima"), "ibrida": ("Ibrida", "Hybrid", "Híbrida")}
LIV = ["principiante", "principiante-intermedio", "intermedio", "intermedio-avanzato", "avanzato", "professionale"]
LIV_IT = {"principiante": "Principiante", "principiante-intermedio": "Principiante / intermedio", "intermedio": "Intermedio",
          "intermedio-avanzato": "Intermedio / avanzato", "avanzato": "Avanzato", "professionale": "Avanzato / professionale"}
_LIV = {"principiante": ("Principiante", "Beginner", "Principiante"),
        "principiante-intermedio": ("Principiante / intermedio", "Beginner / intermediate", "Principiante / intermedio"),
        "intermedio": ("Intermedio", "Intermediate", "Intermedio"),
        "intermedio-avanzato": ("Intermedio / avanzato", "Intermediate / advanced", "Intermedio / avanzado"),
        "avanzato": ("Avanzato", "Advanced", "Avanzado"),
        "professionale": ("Avanzato / professionale", "Advanced / professional", "Avanzado / profesional")}
STILE_IT = {"offensivo": "Attacco", "controllo": "Controllo", "polivalente": "Polivalente"}
_STILE = {"offensivo": ("Attacco", "Attack", "Ataque"), "controllo": ("Controllo", "Control", "Control"),
          "polivalente": ("Polivalente", "All-round", "Polivalente")}


def FORMA(k):
    return _FORMA[k][LINGUE.index(_LANG[0])] if k in _FORMA else None


def LIVN(k):
    return _LIV[k][LINGUE.index(_LANG[0])] if k in _LIV else None


def STILEN(k):
    return _STILE[k][LINGUE.index(_LANG[0])] if k in _STILE else None


def forme_d():
    return {k: FORMA(k) for k in _FORMA}


def stili_d():
    return {k: STILEN(k) for k in _STILE}


# ---------------------------------------------------------------- dati

def slugify(t):
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def _stile(s):
    s = (s or "").lower()
    if any(w in s for w in ("attacco", "offens", "potenza")):
        return "offensivo"
    if "controllo" in s:
        return "controllo"
    return "polivalente" if s else None


def _peso(d):
    if isinstance(d.get("peso"), str):
        return d["peso"]
    if isinstance(d.get("peso_g"), list):
        return f"{d['peso_g'][0]}–{d['peso_g'][1]} g"
    return None


_DB = []


def carica():
    if _DB:
        return _DB
    out = []
    for f in sorted(DATA.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if "pagina" not in d:
            continue
        p = d["pagina"]
        peso = _peso(d)
        pm = re.findall(r"\d{3}", peso or "")
        liv = d.get("livello") if d.get("livello") in LIV else None
        forma = d.get("forma") if d.get("forma") in FORMA_IT else None
        n = dict(
            slug=d["slug"], marca=d["marca"], marca_slug=slugify(d["marca"]), modello=d["modello"], anno=d["anno"],
            titolo=p["titolo"], forma=forma, livello=liv, stile=_stile(d.get("stile")), peso=peso.split(" (")[0] if peso else None,
            peso_min=int(pm[0]) if pm else None, prezzo=d.get("prezzo_listino_eur"), categoria=d.get("categoria", "adulto"),
            donna=bool(d.get("donna")), giocatore=d.get("giocatore"), superficie=d.get("superficie") or d.get("plano"),
            sensazione=d.get("sensazione") or d.get("tatto"), bilanciamento=d.get("bilanciamento"), nucleo=d.get("nucleo") or d.get("gomma"),
            val=p.get("valutazioni"), lead=p.get("lead", ""), d=d,
        )
        n["nome"] = n["titolo"].replace(n["marca"] + " ", "", 1)
        if str(n["anno"]) not in n["nome"]:
            n["nome"] += f" {n['anno']}"
        out.append(n)
    _DB.extend(out)
    return _DB


def url_r(n):
    return P("racchette", n["slug"])


def coppie(db):
    """Coppie di confronto da pubblicare come pagine: stesso modello in anni diversi + primo simile interno."""
    per_slug = {n["slug"]: n for n in db}
    ks = set()
    for n in db:
        for o in db:
            if o is not n and o["marca"] == n["marca"] and o["modello"] == n["modello"]:
                ks.add(tuple(sorted((n["slug"], o["slug"]))))
        for s in n["d"]["pagina"].get("simili", []):
            u = s["url"]
            if u.startswith("/racchette/"):
                t = u.strip("/").split("/")[-1]
                if t in per_slug:
                    ks.add(tuple(sorted((n["slug"], t))))
                    break
    return sorted(ks)


def confronto_slug(a, b):
    x, y = sorted((a, b))
    return f"{x}-vs-{y}"


def confronto_url(a, b):
    return P("confronta", confronto_slug(a, b))


# ---------------------------------------------------------------- layout

LOGO = '<svg width="36" height="36" viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="14" width="52" height="36" rx="4" fill="none" stroke="#0F3D2E" stroke-width="4"/><line x1="19" y1="14" x2="19" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="45" y1="14" x2="45" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="19" y1="32" x2="45" y2="32" stroke="#0F3D2E" stroke-width="2"/><line x1="32" y1="9" x2="32" y2="55" stroke="#0F3D2E" stroke-width="4" stroke-linecap="round"/><circle cx="45" cy="23" r="6.5" fill="#C6F432" stroke="#0F3D2E" stroke-width="2"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F3D2E'/%3E%3Crect x='8' y='16' width='48' height='32' rx='3' fill='none' stroke='%23EAF5EC' stroke-width='4'/%3E%3Cline x1='32' y1='11' x2='32' y2='53' stroke='%23EAF5EC' stroke-width='4'/%3E%3Ccircle cx='45' cy='25' r='7' fill='%23C6F432'/%3E%3C/svg%3E"
CSS = (ROOT / "scripts" / "scheda.css").read_text(encoding="utf-8") + (ROOT / "scripts" / "pagine.css").read_text(encoding="utf-8")


def nav():
    return [("racchette", L("Racchette", "Rackets", "Palas"), P("racchette")),
            ("pickleball", "Pickleball", P("pickleball")),
            ("bambini", L("Bambini", "Kids", "Niños"), P("bambini")),
            ("confronta", L("Confronta", "Compare", "Comparar"), P("confronta")),
            ("guide", L("Guide", "Guides", "Guías"), P("guide")),
            ("articoli", L("Articoli", "Articles", "Artículos"), P("articoli"))]


def header(on, alt=None):
    l = _LANG[0]
    alt = alt or ALT("home")
    items = "\n".join(f'<a{" class=\"on\"" if k == on else ""} href="{h}">{t}</a>' for k, t, h in nav())
    langs = " · ".join(f'<a{" class=\"on\"" if x == l else ""} href="{alt.get(x, P("home", l=x))}" hreflang="{x}">{x.upper()}</a>' for x in LINGUE)
    return f'''<header class="site"><div class="wrap">
<a class="brand" href="{P("home")}">{LOGO}<span><b>padel</b>metrix</span></a>
<nav class="main" aria-label="{L("Principale", "Main", "Principal")}">
{items}
</nav>
<div class="langs" aria-label="{L("Lingua", "Language", "Idioma")}">{langs}</div>
</div></header>'''


def footer():
    testo = L("PadelMetrix è un sito indipendente di Luca Bicchieri. In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Alcuni link verso altri negozi sono link di affiliazione.",
              "PadelMetrix is an independent website by Luca Bicchieri. As an Amazon Associate, PadelMetrix earns from qualifying purchases. Some links to other shops are affiliate links.",
              "PadelMetrix es una web independiente de Luca Bicchieri. Como Afiliado de Amazon, PadelMetrix obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Algunos enlaces a otras tiendas son enlaces de afiliado.")
    links = [(P("racchette"), L("Racchette", "Rackets", "Palas")), (P("guide"), L("Guide", "Guides", "Guías")),
             (P("articoli"), L("Articoli", "Articles", "Artículos")), (P("domande"), L("Domande", "Questions", "Preguntas")), (P("glossario"), L("Glossario", "Glossary", "Glosario")),
             (P("dati"), L("Dati aperti", "Open data", "Datos abiertos")), (P("chi-siamo"), L("Chi siamo e metodo", "About and method", "Quiénes somos y método")),
             (P("privacy"), L("Privacy", "Privacy", "Privacidad")), (P("cookie"), L("Cookie", "Cookies", "Cookies"))]
    return f'''<footer><div class="wrap">
<span style="max-width:760px">{testo}</span>
<span>{" · ".join([f'<a href="{u}">{t}</a>' for u, t in links] + ([C.link_footer(_LANG[0])] if C.attivo() else []))} · © 2026 PadelMetrix</span>
</div></footer>'''


def crumbs(items):
    """items = [(nome, url|None)]; restituisce html e JSON-LD BreadcrumbList."""
    parts, ld = [], []
    for i, (nome, u) in enumerate(items, 1):
        parts.append(f'<a href="{u}">{e(nome)}</a>' if u else f"<span>{e(nome)}</span>")
        el = {"@type": "ListItem", "position": i, "name": nome}
        if u:
            el["item"] = SITO + u
        ld.append(el)
    htm = f'<nav class="crumbs" aria-label="{L("Percorso", "Breadcrumb", "Ruta")}">' + "<span>›</span>".join(parts) + "</nav>"
    return htm, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}


def home_crumb():
    return ("Home", P("home"))


OG_LOCALE = {"it": "it_IT", "en": "en_GB", "es": "es_ES"}


def pagina(titolo, desc, path, corpo, on=None, ld=(), extra_js="", alt=None):
    """alt = {lingua: percorso} delle versioni della stessa pagina, per hreflang e selettore lingua."""
    l = _LANG[0]
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    hreflang = ""
    if alt:
        hreflang = "\n".join(f'<link rel="alternate" hreflang="{x}" href="{SITO}{alt[x]}">' for x in LINGUE if x in alt)
        hreflang += f'\n<link rel="alternate" hreflang="x-default" href="{SITO}{alt.get("en", alt.get("it"))}">'
    return f'''<!doctype html>
<html lang="{l}">
<head>
<meta charset="utf-8">
{C.head(l)}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITO}{path}">
{hreflang}
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITO}{path}">
<meta property="og:type" content="website">
<meta property="og:locale" content="{OG_LOCALE[l]}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
{lds}
<style>
{CSS}
</style>
</head>
<body>
{header(on, alt)}
<main class="wrap">
{corpo}
</main>
{footer()}
{extra_js}
{C.body(l, P("cookie"))}
</body>
</html>
'''


def card(n, extra=""):
    bits = [x for x in (FORMA(n["forma"]), n["peso"], LIVN(n["livello"])) if x]
    attrs = (f'data-marca="{n["marca_slug"]}" data-forma="{n["forma"] or ""}" data-livello="{n["livello"] or ""}" '
             f'data-stile="{n["stile"] or ""}" data-cat="{"junior" if n["categoria"] == "junior" else ("donna" if n["donna"] else "adulto")}" '
             f'data-prezzo="{n["prezzo"] or ""}" data-anno="{n["anno"]}" data-nome="{e((n["titolo"] + " " + (n["giocatore"] or "")).lower())}"')
    return (f'<a class="rcard" href="{url_r(n)}" {attrs}><div class="ill">{racket_svg(n["forma"], 64, n["titolo"])}</div>'
            f'<div><small>{e(n["marca"])} · {n["anno"]}</small><b>{e(n["nome"])}</b><small>{e(" · ".join(bits))}</small>{extra}</div></a>')


def griglia(items):
    return '<div class="rgrid">' + "\n".join(card(n) for n in items) + "</div>"


def ordina(items):
    return sorted(items, key=lambda n: (-n["anno"], n["marca"], n["nome"]))


def autore():
    return {"@type": "Person", "name": "Luca Bicchieri", "url": SITO + P("chi-siamo")}


def editore():
    return {"@type": "Organization", "name": "PadelMetrix", "url": SITO + P("home")}


def data_riga(femm=False):
    agg = L("Aggiornata" if femm else "Aggiornato", "Updated", "Actualizada" if femm else "Actualizado")
    by = L("a cura di", "by", "por")
    return f'<p class="note">{agg} {L("il ", "on ", "el ")}{data_txt()} · {by} <a href="{P("chi-siamo")}">Luca Bicchieri, PadelMetrix</a></p>'


PAGINE = []  # (percorso, {lingua: percorso}) per la sitemap


def scrivi(path, html_txt, alt=None):
    dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_txt, encoding="utf-8")
    PAGINE.append({"path": path, "alt": alt or {}})
