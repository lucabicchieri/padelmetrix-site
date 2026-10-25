#!/usr/bin/env python3
"""Genera le home in /it/, /en/, /es/, la pagina radice e il file _redirects.

Uso:  python3 scripts/genera_home.py
"""
import html
import json
import re
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comune import LINGUE, racket_svg, url  # noqa: E402
import sito as S  # noqa: E402
import consenso as C  # noqa: E402
from sito import L, P  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "racchette"
e = html.escape
SITO = "https://www.padelmetrix.com"

IN_EVIDENZA = [
    "adidas-metalbone-hrd-plus-2026",
    "nox-at10-genius-12k-xtrem-2027",
    "bullpadel-hack-05-2027",
    "starvie-raptor-plus-2027",
]

T = {
    "it": {
        "html_lang": "it", "title": "PadelMetrix · La guida indipendente all'attrezzatura da padel",
        "desc": "Schede tecniche, confronti e consigli su racchette da padel, abbigliamento e attrezzatura per bambini. Trova la racchetta giusta per il tuo gioco.",
        "claim": "Il Padel, Analizzato.",
        "nav": ["Racchette", "Abbigliamento", "Bambini", "Confronta", "Guide"],
        "h1": "La guida indipendente per scegliere l'attrezzatura da padel.",
        "intro": "PadelMetrix raccoglie in un solo posto schede tecniche, confronti e consigli su racchette, abbigliamento e attrezzatura per bambini. Ti aiutiamo a capire cosa fa per te; poi compri dove preferisci.",
        "cta1": "Trova la tua racchetta in 2 minuti", "cta2": "Esplora le racchette",
        "cerca_label": "Cerca un modello o una marca", "cerca_ph": "Es. Metalbone, AT10, Viper", "cerca_btn": "Cerca",
        "conta": "{n} racchette di {m} marche nel database, aggiornate ogni settimana",
        "sez_titolo": "Cosa trovi su PadelMetrix", "sez_sub": "Tre sezioni, per tutto quello che serve in campo.",
        "sezioni": [
            ("racchette", "Racchette", "Schede con tutti i dati tecnici, sintesi delle recensioni e modelli simili. Filtra per livello, forma, peso e marca.", "Vai alle racchette"),
            ("abbigliamento", "Abbigliamento", "Scarpe da padel, abbigliamento uomo e donna, borse porta-racchette e accessori: palline, overgrip e protezioni.", "Vai all'abbigliamento"),
            ("bambini", "Bambini", "Racchette junior divise per età, con una guida per scegliere quella giusta, più scarpe e abbigliamento per i più piccoli.", "Vai alla sezione bambini"),
        ],
        "tool": "Strumento",
        "t1": ("Trova la tua racchetta", "7 domande su livello, stile e budget: ti proponiamo le 3 racchette più adatte.", "Fai il test"),
        "t2": ("Confronta racchette", "Affianca fino a 3 modelli e guarda subito dove si differenziano.", "Apri il comparatore"),
        "come_titolo": "Come lavoriamo",
        "come": [
            ("Dati verificati", "Le caratteristiche tecniche arrivano dai produttori e da fonti specializzate, organizzate in modo uniforme per confrontare davvero."),
            ("Recensioni in sintesi", "Leggiamo i test pubblicati online e ne riassumiamo pregi e limiti con parole nostre, sempre con il link alla fonte."),
            ("Trasparenza", "Non vendiamo nulla. Alcuni link portano a negozi partner: se acquisti, possiamo ricevere una piccola commissione, senza costi per te."),
        ],
        "evid_titolo": "Racchette in evidenza", "evid_tutte": "Vedi tutte le racchette",
        "evid_nota": "",
        "marche_titolo": "Le marche nel database",
        "racchette_n": "{n} racchette", "racchetta_1": "1 racchetta",
        "footer_sez": "Sezioni", "footer_str": "Strumenti", "footer_info": "PadelMetrix",
        "chi": "Chi siamo", "privacy": "Privacy", "cookie": "Cookie",
        "disclosure": "In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Alcuni link verso altri negozi sono link di affiliazione.",
        "forme": {"diamante": "Diamante", "rotonda": "Rotonda", "goccia": "Goccia"},
        "lingua": "Lingua",
    },
    "en": {
        "html_lang": "en", "title": "PadelMetrix · The independent guide to padel gear",
        "desc": "Specs, comparisons and advice on padel rackets, clothing and kids' gear. Find the right racket for your game.",
        "claim": "Padel, Analyzed.",
        "nav": ["Rackets", "Clothing", "Kids", "Compare", "Guides"],
        "h1": "The independent guide to choosing your padel gear.",
        "intro": "PadelMetrix brings together specs, comparisons and advice on rackets, clothing and kids' gear in one place. We help you work out what suits you; then you buy wherever you like.",
        "cta1": "Find your racket in 2 minutes", "cta2": "Browse rackets",
        "cerca_label": "Search for a model or brand", "cerca_ph": "E.g. Metalbone, AT10, Viper", "cerca_btn": "Search",
        "conta": "{n} rackets from {m} brands in our database, updated every week",
        "sez_titolo": "What you'll find on PadelMetrix", "sez_sub": "Three sections covering everything you need on court.",
        "sezioni": [
            ("racchette", "Rackets", "Full specs, review summaries and similar models for every racket. Filter by level, shape, weight and brand.", "Go to rackets"),
            ("abbigliamento", "Clothing", "Padel shoes, men's and women's clothing, racket bags and accessories: balls, overgrips and protection.", "Go to clothing"),
            ("bambini", "Kids", "Junior rackets grouped by age, with a guide to choosing the right one, plus shoes and clothing for young players.", "Go to kids"),
        ],
        "tool": "Tool",
        "t1": ("Racket finder", "7 questions about your level, style and budget: we suggest the 3 rackets that suit you best.", "Take the quiz"),
        "t2": ("Compare rackets", "Put up to 3 models side by side and see straight away where they differ.", "Open the comparison"),
        "come_titolo": "How we work",
        "come": [
            ("Checked data", "Specs come from manufacturers and specialist sources, organised the same way so you can genuinely compare."),
            ("Reviews in brief", "We read the tests published online and sum up strengths and weaknesses in our own words, always linking to the source."),
            ("Transparency", "We don't sell anything. Some links go to partner shops: if you buy, we may earn a small commission at no extra cost to you."),
        ],
        "evid_titolo": "Featured rackets", "evid_tutte": "See all rackets",
        "evid_nota": "",
        "marche_titolo": "Brands in our database",
        "racchette_n": "{n} rackets", "racchetta_1": "1 racket",
        "footer_sez": "Sections", "footer_str": "Tools", "footer_info": "PadelMetrix",
        "chi": "About us", "privacy": "Privacy", "cookie": "Cookies",
        "disclosure": "As an Amazon Associate, PadelMetrix earns from qualifying purchases. Some links to other shops are affiliate links.",
        "forme": {"diamante": "Diamond", "rotonda": "Round", "goccia": "Teardrop"},
        "lingua": "Language",
    },
    "es": {
        "html_lang": "es", "title": "PadelMetrix · La guía independiente del material de pádel",
        "desc": "Fichas técnicas, comparativas y consejos sobre palas de pádel, ropa y material para niños. Encuentra la pala ideal para tu juego.",
        "claim": "El Pádel, Analizado.",
        "nav": ["Palas", "Ropa", "Niños", "Comparar", "Guías"],
        "h1": "La guía independiente para elegir tu material de pádel.",
        "intro": "PadelMetrix reúne en un solo lugar fichas técnicas, comparativas y consejos sobre palas, ropa y material para niños. Te ayudamos a saber qué te conviene; después compras donde prefieras.",
        "cta1": "Encuentra tu pala en 2 minutos", "cta2": "Ver las palas",
        "cerca_label": "Busca un modelo o una marca", "cerca_ph": "Ej. Metalbone, AT10, Viper", "cerca_btn": "Buscar",
        "conta": "{n} palas de {m} marcas en nuestra base de datos, actualizada cada semana",
        "sez_titolo": "Qué encontrarás en PadelMetrix", "sez_sub": "Tres secciones con todo lo que necesitas en la pista.",
        "sezioni": [
            ("racchette", "Palas", "Fichas con todos los datos técnicos, resumen de las reseñas y modelos similares. Filtra por nivel, forma, peso y marca.", "Ir a las palas"),
            ("abbigliamento", "Ropa", "Zapatillas de pádel, ropa de hombre y mujer, paleteros y accesorios: pelotas, overgrips y protecciones.", "Ir a la ropa"),
            ("bambini", "Niños", "Palas junior por edades, con una guía para elegir la adecuada, además de zapatillas y ropa para los más pequeños.", "Ir a niños"),
        ],
        "tool": "Herramienta",
        "t1": ("Encuentra tu pala", "7 preguntas sobre tu nivel, estilo y presupuesto: te proponemos las 3 palas que mejor te encajan.", "Hacer el test"),
        "t2": ("Comparar palas", "Pon hasta 3 modelos lado a lado y ve al instante en qué se diferencian.", "Abrir el comparador"),
        "come_titolo": "Cómo trabajamos",
        "come": [
            ("Datos verificados", "Las características técnicas proceden de los fabricantes y de fuentes especializadas, organizadas igual para poder comparar de verdad."),
            ("Reseñas resumidas", "Leemos las pruebas publicadas en internet y resumimos virtudes y límites con nuestras palabras, siempre con el enlace a la fuente."),
            ("Transparencia", "No vendemos nada. Algunos enlaces llevan a tiendas asociadas: si compras, podemos recibir una pequeña comisión sin coste para ti."),
        ],
        "evid_titolo": "Palas destacadas", "evid_tutte": "Ver todas las palas",
        "evid_nota": "",
        "marche_titolo": "Marcas en nuestra base de datos",
        "racchette_n": "{n} palas", "racchetta_1": "1 pala",
        "footer_sez": "Secciones", "footer_str": "Herramientas", "footer_info": "PadelMetrix",
        "chi": "Quiénes somos", "privacy": "Privacidad", "cookie": "Cookies",
        "disclosure": "Como Afiliado de Amazon, PadelMetrix obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Algunos enlaces a otras tiendas son enlaces de afiliado.",
        "forme": {"diamante": "Diamante", "rotonda": "Redonda", "goccia": "Lágrima"},
        "lingua": "Idioma",
    },
}

CSS = """
:root{--g:#0F3D2E;--gd:#0B2E23;--lime:#C6F432;--ink:#1F2D27;--ink2:#3D4D45;--mut:#5B6B63;--line:#E1E5DF;--soft:#EEF2EC;--bg:#FAFAF7}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:'IBM Plex Sans',system-ui,sans-serif;line-height:1.55}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;margin:0;letter-spacing:-.02em}
a{color:var(--g)}a:hover{color:#0a2a20}
.wrap{max-width:1200px;margin:0 auto;padding:0 24px}
header.site{border-bottom:1px solid var(--line);background:var(--bg)}
header.site .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:12px 32px;padding-top:14px;padding-bottom:14px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--g);font-family:'Space Grotesk',sans-serif;font-size:26px;letter-spacing:-.03em}
.brand b{font-weight:700}.brand span{font-weight:400}
nav.main{display:flex;flex-wrap:wrap;gap:4px 24px;font-size:15px;font-weight:500;flex:1 1 auto}
nav.main a{text-decoration:none;color:var(--ink);padding:10px 0}
.langs{font-size:14px;font-weight:600;color:#8A968F}.langs a{text-decoration:none;color:var(--mut);padding:10px 2px}.langs a.on{color:var(--g)}
.hero{background:var(--g);color:#fff}
.hero .wrap{padding-top:72px;padding-bottom:72px;display:flex;flex-wrap:wrap;align-items:center;gap:48px}
.hero .txt{flex:1 1 540px;display:flex;flex-direction:column;gap:22px}
.claim{font-size:14px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--lime)}
.hero h1{font-size:clamp(2.2rem,5vw,3.5rem);line-height:1.06;letter-spacing:-.03em}
.hero p{margin:0;font-size:19px;color:#D3E2DA;max-width:600px}
.ctas{display:flex;flex-wrap:wrap;gap:12px}
.btn{display:inline-block;text-decoration:none;font-weight:600;font-size:16px;padding:14px 22px;border-radius:10px}
.btn.lime{background:var(--lime);color:var(--g)}.btn.out{border:1.5px solid #fff;color:#fff;padding:13px 22px}
.btn.dark{background:var(--g);color:#fff}
form.cerca{display:flex;flex-wrap:wrap;gap:8px;max-width:600px}
form.cerca label{width:100%;font-size:14px;color:#D3E2DA}
form.cerca input{flex:1 1 240px;height:48px;border-radius:10px;border:none;padding:0 16px;font-size:16px;font-family:inherit}
form.cerca button{height:48px;padding:0 20px;border-radius:10px;border:none;background:#fff;color:var(--g);font-weight:600;font-size:16px;cursor:pointer}
.conta{font-size:14px;color:#D3E2DA}
.hero .art{flex:1 1 340px;display:flex;justify-content:center}
section.block{padding:56px 0 8px}
.head{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:12px;margin-bottom:24px}
.head h2{font-size:32px}.head p{margin:6px 0 0;color:var(--ink2);font-size:17px}
.grid3{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}
.card{background:#fff;border:1px solid var(--line);border-radius:18px;text-decoration:none;color:var(--ink);display:flex;flex-direction:column;overflow:hidden}
.card .body{padding:22px;display:flex;flex-direction:column;gap:10px}
.card h3{font-size:24px}.card p{margin:0;color:var(--ink2)}
.card .go{font-weight:600;color:var(--g)}
.ill{height:190px;background:radial-gradient(circle at 50% 40%,#EAF0E6,#DDE6D8);display:flex;align-items:center;justify-content:center}
.tools{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:20px}
.tool{border-radius:18px;padding:28px;display:flex;flex-direction:column;gap:12px}
.tool.dark{background:var(--g);color:#fff}.tool.dark p{color:#D3E2DA}
.tool.light{background:#EAF0E6}
.tool .tag{font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase}
.tool.dark .tag{color:var(--lime)}.tool.light .tag{color:#3C6B57}
.tool h3{font-size:26px}.tool p{margin:0}.tool .btn{align-self:flex-start;margin-top:6px}
.come{background:#fff;border-top:1px solid var(--line);border-bottom:1px solid var(--line);margin-top:56px}
.come .wrap{padding-top:56px;padding-bottom:56px}
.come h2{font-size:30px;margin-bottom:28px}
.come .g{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:28px}
.come .n{width:40px;height:40px;border-radius:10px;background:var(--lime);color:var(--g);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:18px;display:flex;align-items:center;justify-content:center;margin-bottom:10px}
.come h3{font-size:20px;margin-bottom:6px}.come p{margin:0;color:var(--ink2)}
.grid4{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px}
.rk .meta{font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
.rk .nm{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:19px}
.rk .sp{font-size:14px;color:var(--mut)}
.nota{font-size:14px;color:var(--mut);margin-top:14px}
.marche{display:flex;flex-wrap:wrap;gap:12px}
.marche a{display:flex;flex-direction:column;gap:2px;min-width:170px;background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 20px;text-decoration:none;color:var(--ink)}
.marche b{font-family:'Space Grotesk',sans-serif;font-size:20px}.marche span{font-size:14px;color:var(--mut)}
footer{background:var(--gd);color:#C9D6CF;margin-top:64px}
footer .wrap{padding-top:48px;padding-bottom:24px;display:flex;flex-direction:column;gap:32px}
footer .cols{display:flex;flex-wrap:wrap;gap:32px 64px}
footer .cols>div{display:flex;flex-direction:column;gap:10px;font-size:15px}
footer .cols b{color:#fff}
footer a{color:#C9D6CF;text-decoration:none}
footer .wm{font-family:'Space Grotesk',sans-serif;font-size:26px;letter-spacing:-.03em;color:#fff}
footer .wm i{font-style:normal;font-weight:400;color:var(--lime)}
footer .bottom{border-top:1px solid #24503F;padding-top:20px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:12px;font-size:13px}
"""

LOGO = '<svg width="36" height="36" viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="14" width="52" height="36" rx="4" fill="none" stroke="#0F3D2E" stroke-width="4"/><line x1="19" y1="14" x2="19" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="45" y1="14" x2="45" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="19" y1="32" x2="45" y2="32" stroke="#0F3D2E" stroke-width="2"/><line x1="32" y1="9" x2="32" y2="55" stroke="#0F3D2E" stroke-width="4" stroke-linecap="round"/><circle cx="45" cy="23" r="6.5" fill="#C6F432" stroke="#0F3D2E" stroke-width="2"/></svg>'
FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F3D2E'/%3E%3Crect x='8' y='16' width='48' height='32' rx='3' fill='none' stroke='%23EAF5EC' stroke-width='4'/%3E%3Cline x1='32' y1='11' x2='32' y2='53' stroke='%23EAF5EC' stroke-width='4'/%3E%3Ccircle cx='45' cy='25' r='7' fill='%23C6F432'/%3E%3C/svg%3E"
COURT = '<svg viewBox="0 0 420 280" style="width:100%;max-width:440px;height:auto" aria-hidden="true"><rect x="10" y="10" width="400" height="260" rx="10" fill="#134A38" stroke="#C6F432" stroke-opacity="0.5" stroke-width="3"/><line x1="110" y1="10" x2="110" y2="270" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/><line x1="310" y1="10" x2="310" y2="270" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/><line x1="110" y1="140" x2="310" y2="140" stroke="#fff" stroke-opacity="0.35" stroke-width="2"/><line x1="210" y1="0" x2="210" y2="280" stroke="#fff" stroke-width="4" stroke-linecap="round"/><path d="M60 230 Q 150 30 250 190 Q 290 110 320 120" fill="none" stroke="#C6F432" stroke-width="3" stroke-linecap="round" stroke-dasharray="0 12"/><circle cx="336" cy="118" r="14" fill="#C6F432"/></svg>'
SEC_ICON = {"racchette": "diamante", "abbigliamento": None, "bambini": "rotonda"}
SHOE = '<svg viewBox="0 0 240 140" width="190" aria-hidden="true"><path d="M20 96 C20 70 40 58 62 56 L104 50 C118 48 128 38 134 26 L150 30 C152 52 168 62 190 66 C212 70 222 82 222 96 Z" fill="#0F3D2E"/><path d="M14 96 H226 V108 C226 114 222 118 216 118 H24 C18 118 14 114 14 108 Z" fill="#C6F432"/><path d="M112 58 L124 70 M124 52 L136 64 M100 62 L110 72" stroke="#FAFAF7" stroke-opacity="0.6" stroke-width="5" stroke-linecap="round"/></svg>'


def guide_box():
    g = lambda x: P("guide", x)  # noqa: E731
    voci = [(g("racchetta-padel-principianti"), L("Principianti", "Beginners", "Principiantes"), L("la prima racchetta", "your first racket", "la primera pala")),
            (g("racchetta-padel-epicondilite"), L("Gomito", "Tennis elbow", "Codo"), L("racchette confortevoli", "comfortable rackets", "palas cómodas")),
            (g("forme-racchetta-padel"), L("Forme", "Shapes", "Formas"), L("rotonda, goccia o diamante", "round, teardrop or diamond", "redonda, lágrima o diamante")),
            (P("bambini"), L("Bambini", "Kids", "Niños"), L("misure per età", "sizes by age", "medidas por edad")),
            (g("racchette-padel-economiche"), L("Economiche", "Cheap", "Baratas"), L("fino a 130 €", "up to €130", "hasta 130 €")),
            (P("confronta"), L("Confronti", "Comparisons", "Comparativas"), L("modello contro modello", "model versus model", "modelo contra modelo")),
            (g("racchette-giocatori-professionisti"), L("Professionisti", "Pro players", "Profesionales"), L("con che racchetta giocano", "which rackets they use", "con qué pala juegan")),
            (P("report", "racchette-padel-2026-2027-in-numeri"), L("Report 2026–2027", "2026–2027 report", "Informe 2026–2027"), L("il mercato in numeri", "the market in numbers", "el mercado en cifras")),
            (P("dati"), L("Dati aperti", "Open data", "Datos abiertos"), L("scarica il database", "download the database", "descarga la base de datos"))]
    return (f'<div class="head" style="margin-top:40px"><h2>{L("Guide alla scelta", "Buying guides", "Guías de compra")}</h2><a href="{P("guide")}"><b>{L("Tutte le guide", "All guides", "Todas las guías")} →</b></a></div>\n'
            + '<div class="marche">' + "".join(f'<a href="{u}"><b>{b}</b><span>{sp}</span></a>' for u, b, sp in voci) + "</div>")


def carica():
    out = {}
    for f in DATA.glob("*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        out[d["slug"]] = d
    return out


def head(lang, t):
    alts = "".join(f'<link rel="alternate" hreflang="{l}" href="{SITO}/{l}/">' for l in LINGUE)
    alts += f'<link rel="alternate" hreflang="x-default" href="{SITO}/en/">'
    return f'''<!doctype html>
<html lang="{t["html_lang"]}">
<head>
<meta charset="utf-8">
{C.head(lang)}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(t["title"])}</title>
<meta name="description" content="{e(t["desc"])}">
<link rel="canonical" href="{SITO}/{lang}/">
{alts}
<meta property="og:title" content="{e(t["title"])}">
<meta property="og:description" content="{e(t["desc"])}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITO}/{lang}/">
<meta property="og:locale" content="{S.OG_LOCALE[lang]}">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": "PadelMetrix", "url": f"{SITO}/{lang}/", "inLanguage": lang, "description": t["desc"]}, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>'''


def pagina(lang, db):
    t = T[lang]
    keys = ["racchette", "abbigliamento", "bambini", "confronta", "selettore"]
    S.set_lang(lang)
    voci_nav = [(P("guide") if k == "selettore" else url(lang, k), n) for k, n in zip(keys, t["nav"])]
    voci_nav.insert(3, (P("pickleball"), "Pickleball"))
    nav = "".join(f'<a href="{u}">{e(n)}</a>' for u, n in voci_nav)
    langs = " · ".join(f'<a{" class=\"on\"" if l == lang else ""} href="/{l}/" hreflang="{l}">{l.upper()}</a>' for l in LINGUE)
    marche = {}
    for d in db.values():
        marche[d["marca"]] = marche.get(d["marca"], 0) + 1
    conta = t["conta"].format(n=len(db), m=len(marche))

    sez = []
    for k, tit, txt, go in t["sezioni"]:
        art = SHOE if SEC_ICON[k] is None else racket_svg(SEC_ICON[k], 110 if k == "racchette" else 90, tit)
        sez.append(f'<a class="card" href="{url(lang, k)}"><div class="ill">{art}</div><div class="body"><h3>{e(tit)}</h3><p>{e(txt)}</p><span class="go">{e(go)} →</span></div></a>')

    evid = []
    for slug in IN_EVIDENZA:
        d = db.get(slug)
        if not d:
            continue
        peso = d.get("peso") or (f'{d["peso_g"][0]}–{d["peso_g"][1]} g' if d.get("peso_g") else "")
        peso = peso.split(" (")[0]
        nome = d["pagina"]["titolo"].replace(d["marca"] + " ", "")
        href = P("racchette", slug)
        evid.append(f'<a class="card rk" href="{href}"><div class="ill">{racket_svg(d["forma"], 92, d["pagina"]["titolo"])}</div><div class="body"><span class="meta">{e(d["marca"])} · {d["anno"]}</span><span class="nm">{e(nome)}</span><span class="sp">{e(t["forme"][d["forma"]])} · {e(peso)}</span></div></a>')

    mk = "".join(f'<a href="{P("marche", re.sub(r"[^a-z0-9]+", "-", m.lower()).strip("-"))}"><b>{e(m)}</b><span>{e(t["racchetta_1"] if n == 1 else t["racchette_n"].format(n=n))}</span></a>' for m, n in sorted(marche.items(), key=lambda kv: -kv[1]))
    nota = f'<p class="nota">{e(t["evid_nota"])}</p>' if t["evid_nota"] else ""
    come = "".join(f'<div><div class="n">{i}</div><h3>{e(a)}</h3><p>{e(b)}</p></div>' for i, (a, b) in enumerate(t["come"], 1))
    t1, t2 = t["t1"], t["t2"]

    return head(lang, t) + f'''
<body>
<header class="site"><div class="wrap">
<a class="brand" href="/{lang}/">{LOGO}<span><b>padel</b>metrix</span></a>
<nav class="main" aria-label="Menu">{nav}</nav>
<div class="langs" aria-label="{e(t["lingua"])}">{langs}</div>
</div></header>

<main>
<section class="hero"><div class="wrap">
<div class="txt">
<div class="claim">{e(t["claim"])}</div>
<h1>{e(t["h1"])}</h1>
<p>{e(t["intro"])}</p>
<div class="ctas"><a class="btn lime" href="{url(lang, "selettore")}">{e(t["cta1"])}</a><a class="btn out" href="{url(lang, "racchette")}">{e(t["cta2"])}</a></div>
<form class="cerca" action="{url(lang, "racchette")}" method="get" role="search">
<label for="q">{e(t["cerca_label"])}</label>
<input id="q" name="q" type="search" placeholder="{e(t["cerca_ph"])}">
<button type="submit">{e(t["cerca_btn"])}</button>
</form>
<div class="conta">{e(conta)}</div>
</div>
<div class="art">{COURT}</div>
</div></section>

<section class="block"><div class="wrap">
<div class="head"><div><h2>{e(t["sez_titolo"])}</h2><p>{e(t["sez_sub"])}</p></div></div>
<div class="grid3">{"".join(sez)}</div>
</div></section>

<section class="block"><div class="wrap">
<div class="tools">
<div class="tool dark"><span class="tag">{e(t["tool"])}</span><h3>{e(t1[0])}</h3><p>{e(t1[1])}</p><a class="btn lime" href="{url(lang, "selettore")}">{e(t1[2])}</a></div>
<div class="tool light"><span class="tag">{e(t["tool"])}</span><h3>{e(t2[0])}</h3><p>{e(t2[1])}</p><a class="btn dark" href="{url(lang, "confronta")}">{e(t2[2])}</a></div>
</div>
</div></section>

<section class="come"><div class="wrap">
<h2>{e(t["come_titolo"])}</h2>
<div class="g">{come}</div>
</div></section>

<section class="block"><div class="wrap">
<div class="head"><h2>{e(t["evid_titolo"])}</h2><a href="{url(lang, "racchette")}"><b>{e(t["evid_tutte"])} →</b></a></div>
<div class="grid4">{"".join(evid)}</div>
{nota}
</div></section>

<section class="block"><div class="wrap">
<div class="head"><h2>{e(t["marche_titolo"])}</h2></div>
<div class="marche">{mk}</div>
{guide_box()}
</div></section>
</main>

<footer><div class="wrap">
<div class="cols">
<div style="flex:1 1 240px"><span class="wm"><b>padel</b><i>metrix</i></span><span>{e(t["claim"])}</span></div>
<div><b>{e(t["footer_sez"])}</b><a href="{url(lang, "racchette")}">{e(t["nav"][0])}</a><a href="{url(lang, "abbigliamento")}">{e(t["nav"][1])}</a><a href="{url(lang, "bambini")}">{e(t["nav"][2])}</a></div>
<div><b>{e(t["footer_str"])}</b><a href="{url(lang, "confronta")}">{e(t["nav"][3])}</a><a href="{P("guide")}">{e(t["nav"][4])}</a></div>
<div><b>{e(t["footer_info"])}</b><a href="{url(lang, "chi")}">{e(t["chi"])}</a><a href="{url(lang, "privacy")}">{e(t["privacy"])}</a><a href="{url(lang, "cookie")}">{e(t["cookie"])}</a>{C.link_footer(lang)}</div>
</div>
<div class="bottom"><span style="max-width:760px">{e(t["disclosure"])}</span><span>© 2026 PadelMetrix</span></div>
</div></footer>
{C.body(lang, url(lang, "cookie"))}
</body>
</html>
'''


ROOT_INDEX = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PadelMetrix</title>
<meta http-equiv="refresh" content="0; url=/it/">
<link rel="canonical" href="https://www.padelmetrix.com/it/">
<link rel="alternate" hreflang="it" href="https://www.padelmetrix.com/it/">
<link rel="alternate" hreflang="en" href="https://www.padelmetrix.com/en/">
<link rel="alternate" hreflang="es" href="https://www.padelmetrix.com/es/">
<link rel="alternate" hreflang="x-default" href="https://www.padelmetrix.com/en/">
<script>
(function(){var l=(navigator.language||"it").slice(0,2).toLowerCase();var m={it:"/it/",en:"/en/",es:"/es/"};location.replace(m[l]||"/en/");})();
</script>
</head>
<body style="font-family:system-ui,sans-serif;padding:40px">
<p><a href="/it/">Italiano</a> · <a href="/en/">English</a> · <a href="/es/">Español</a></p>
</body>
</html>
"""

REDIRECTS = """# Vecchi indirizzi delle schede
/racchette/*  /it/racchette/:splat  301
"""


def main():
    db = carica()
    for lang in LINGUE:
        dest = ROOT / lang / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(pagina(lang, db), encoding="utf-8")
        print("ok", f"/{lang}/")
    (ROOT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    (ROOT / "_redirects").write_text(REDIRECTS, encoding="utf-8")
    print("ok / e _redirects")


if __name__ == "__main__":
    main()
