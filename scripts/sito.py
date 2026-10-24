"""Struttura comune delle pagine italiane del sito: dati normalizzati, layout, schede-card, coppie di confronto."""
import html
import json
import pathlib
import re

from comune import racket_svg

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "racchette"
SITO = "https://www.padelmetrix.com"
OGGI_TXT = "24 ottobre 2026"
e = html.escape

FORMA_IT = {"diamante": "Diamante", "rotonda": "Rotonda", "goccia": "Goccia", "ibrida": "Ibrida"}
LIV = ["principiante", "principiante-intermedio", "intermedio", "intermedio-avanzato", "avanzato", "professionale"]
LIV_IT = {"principiante": "Principiante", "principiante-intermedio": "Principiante / intermedio", "intermedio": "Intermedio",
          "intermedio-avanzato": "Intermedio / avanzato", "avanzato": "Avanzato", "professionale": "Avanzato / professionale"}
STILE_IT = {"offensivo": "Attacco", "controllo": "Controllo", "polivalente": "Polivalente"}

NAV = [("racchette", "Racchette", "/it/racchette/"), ("abbigliamento", "Abbigliamento", "/it/abbigliamento/"),
       ("bambini", "Bambini", "/it/bambini/"), ("confronta", "Confronta", "/it/confronta/"),
       ("guide", "Guide", "/it/guide/")]

LOGO = '<svg width="36" height="36" viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="14" width="52" height="36" rx="4" fill="none" stroke="#0F3D2E" stroke-width="4"/><line x1="19" y1="14" x2="19" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="45" y1="14" x2="45" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="19" y1="32" x2="45" y2="32" stroke="#0F3D2E" stroke-width="2"/><line x1="32" y1="9" x2="32" y2="55" stroke="#0F3D2E" stroke-width="4" stroke-linecap="round"/><circle cx="45" cy="23" r="6.5" fill="#C6F432" stroke="#0F3D2E" stroke-width="2"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F3D2E'/%3E%3Crect x='8' y='16' width='48' height='32' rx='3' fill='none' stroke='%23EAF5EC' stroke-width='4'/%3E%3Cline x1='32' y1='11' x2='32' y2='53' stroke='%23EAF5EC' stroke-width='4'/%3E%3Ccircle cx='45' cy='25' r='7' fill='%23C6F432'/%3E%3C/svg%3E"
CSS = (ROOT / "scripts" / "scheda.css").read_text(encoding="utf-8") + (ROOT / "scripts" / "pagine.css").read_text(encoding="utf-8")


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


def carica():
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
            val=p.get("valutazioni"), lead=p.get("lead", ""), d=d, url=f"/it/racchette/{d['slug']}/",
        )
        n["nome"] = n["titolo"].replace(n["marca"] + " ", "", 1)
        if str(n["anno"]) not in n["nome"]:
            n["nome"] += f" {n['anno']}"
        out.append(n)
    return out


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


def confronto_url(a, b):
    x, y = sorted((a, b))
    return f"/it/confronta/{x}-vs-{y}/"


def header(on):
    nav = "\n".join(f'<a{" class=\"on\"" if k == on else ""} href="{h}">{l}</a>' for k, l, h in NAV)
    return f'''<header class="site"><div class="wrap">
<a class="brand" href="/it/">{LOGO}<b>padel</b><span>metrix</span></a>
<nav class="main" aria-label="Principale">
{nav}
</nav>
<div class="langs" aria-label="Lingua"><a class="on" href="/it/">IT</a> · <a href="/en/">EN</a> · <a href="/es/">ES</a></div>
</div></header>'''


FOOTER = '''<footer><div class="wrap">
<span style="max-width:760px">PadelMetrix è un sito indipendente di Luca Bicchieri. In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Alcuni link verso altri negozi sono link di affiliazione.</span>
<span><a href="/it/racchette/">Racchette</a> · <a href="/it/guide/">Guide</a> · <a href="/it/domande/">Domande</a> · <a href="/it/glossario/">Glossario</a> · <a href="/it/dati/">Dati aperti</a> · <a href="/it/chi-siamo/">Chi siamo e metodo</a> · © 2026 PadelMetrix</span>
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
    htm = '<nav class="crumbs" aria-label="Percorso">' + "<span>›</span>".join(parts) + "</nav>"
    return htm, {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": ld}


def pagina(titolo, desc, path, corpo, on=None, ld=(), extra_js=""):
    lds = "\n".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titolo)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITO}{path}">
<meta property="og:title" content="{e(titolo)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITO}{path}">
<meta property="og:type" content="website">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
{lds}
<style>
{CSS}
</style>
</head>
<body>
{header(on)}
<main class="wrap">
{corpo}
</main>
{FOOTER}
{extra_js}
</body>
</html>
'''


def card(n, extra=""):
    bits = [x for x in (FORMA_IT.get(n["forma"]), n["peso"], LIV_IT.get(n["livello"])) if x]
    attrs = (f'data-marca="{n["marca_slug"]}" data-forma="{n["forma"] or ""}" data-livello="{n["livello"] or ""}" '
             f'data-stile="{n["stile"] or ""}" data-cat="{"junior" if n["categoria"] == "junior" else ("donna" if n["donna"] else "adulto")}" '
             f'data-prezzo="{n["prezzo"] or ""}" data-anno="{n["anno"]}" data-nome="{e((n["titolo"] + " " + (n["giocatore"] or "")).lower())}"')
    return (f'<a class="rcard" href="{n["url"]}" {attrs}><div class="ill">{racket_svg(n["forma"], 64, n["titolo"])}</div>'
            f'<div><small>{e(n["marca"])} · {n["anno"]}</small><b>{e(n["nome"])}</b><small>{e(" · ".join(bits))}</small>{extra}</div></a>')


def griglia(items):
    return '<div class="rgrid">' + "\n".join(card(n) for n in items) + "</div>"


def ordina(items):
    return sorted(items, key=lambda n: (-n["anno"], n["marca"], n["nome"]))
