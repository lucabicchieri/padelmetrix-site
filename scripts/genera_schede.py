#!/usr/bin/env python3
"""Genera le schede racchetta da data/racchette/*.json in racchette/<slug>/index.html.

Uso:  python3 scripts/genera_schede.py
Ogni JSON contiene i dati tecnici e un blocco "pagina" con i testi editoriali.
"""
import html
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "racchette"
OUT = ROOT / "racchette"

e = html.escape


def chips(items):
    return "".join(f"<span>{e(c)}</span>" for c in items)


def li(items):
    return "".join(f"<li>{e(x)}</li>" for x in items)


def num(v):
    s = f"{v:g}"
    return s.replace(".", ",")


def bars(val):
    rows = []
    for r in val["voci"]:
        pct = round(r["valore"] / val["scala"] * 100)
        rows.append(
            f'<div class="bar"><span>{e(r["nome"])}</span><div class="track"><div class="fill" style="width:{pct}%"></div></div><span class="v">{num(r["valore"])}</span></div>'
        )
    return f'''<div class="card">
<h2>{e(val["titolo"])}</h2>
<div class="bars">
{chr(10).join(rows)}
</div>
<p class="note">{val["nota_html"]}</p>
</div>'''


def tratti(t):
    return f'''<div class="card">
<h2>{e(t["titolo"])}</h2>
<div class="chips">{chips(t["voci"])}</div>
<p class="note">{t["nota_html"]}</p>
</div>'''


def store(s):
    cls = "btn lime" if s.get("amazon") else "btn"
    rel = "sponsored nofollow noopener" if s.get("amazon") else "nofollow noopener"
    return f'<div class="store"><div><strong>{e(s["nome"])}</strong><small>{e(s["nota"])}</small></div><a class="{cls}" href="{e(s["url"])}" rel="{rel}" target="_blank">{e(s["pulsante"])}</a></div>'


def specs(items):
    return "\n".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in items)


def rev_rows(items):
    out = []
    for r in items:
        out.append(
            f'<tr><td><a href="{e(r["url"])}" rel="nofollow noopener" target="_blank">{e(r["fonte"])}</a></td><td>{e(r["voto"])}<br><small>{e(r.get("voto_dettaglio", ""))}</small></td><td>{e(r["sintesi"])}</td></tr>'
        )
    return "\n".join(out)


def sim_cards(items):
    out = []
    for s in items:
        ext = s["url"].startswith("http")
        attrs = ' rel="nofollow noopener" target="_blank"' if ext else ""
        out.append(
            f'<a href="{e(s["url"])}"{attrs}><small>{e(s["sopra"])}</small><b>{e(s["nome"])}</b><small>{e(s["testo"])}</small></a>'
        )
    return "\n".join(out)


CSS = open(ROOT / "scripts" / "scheda.css", encoding="utf-8").read()

NAV = [("Racchette", "/racchette/"), ("Abbigliamento", "/abbigliamento/"), ("Bambini", "/bambini/"),
       ("Confronta", "/confronta/"), ("Trova la tua racchetta", "/trova-la-tua-racchetta/")]

LOGO = '<svg width="36" height="36" viewBox="0 0 64 64" aria-hidden="true"><rect x="6" y="14" width="52" height="36" rx="4" fill="none" stroke="#0F3D2E" stroke-width="4"/><line x1="19" y1="14" x2="19" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="45" y1="14" x2="45" y2="50" stroke="#0F3D2E" stroke-width="2"/><line x1="19" y1="32" x2="45" y2="32" stroke="#0F3D2E" stroke-width="2"/><line x1="32" y1="9" x2="32" y2="55" stroke="#0F3D2E" stroke-width="4" stroke-linecap="round"/><circle cx="45" cy="23" r="6.5" fill="#C6F432" stroke="#0F3D2E" stroke-width="2"/></svg>'

FAVICON = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230F3D2E'/%3E%3Crect x='8' y='16' width='48' height='32' rx='3' fill='none' stroke='%23EAF5EC' stroke-width='4'/%3E%3Cline x1='32' y1='11' x2='32' y2='53' stroke='%23EAF5EC' stroke-width='4'/%3E%3Ccircle cx='45' cy='25' r='7' fill='%23C6F432'/%3E%3C/svg%3E"


def render(d):
    p = d["pagina"]
    slug = d["slug"]
    nome_completo = p["titolo"]
    ld = {
        "@context": "https://schema.org", "@type": "Product", "name": nome_completo,
        "brand": {"@type": "Brand", "name": d["marca"]}, "category": "Racchetta da padel",
        "description": p["meta_description"],
    }
    nav = "\n".join(
        f'<a{" class=\"on\"" if lbl == "Racchette" else ""} href="{href}">{lbl}</a>' for lbl, href in NAV)
    marca_slug = d["marca"].lower()
    avviso = f'<div class="card avviso">{p["avviso_html"]}</div>' if p.get("avviso_html") else ""
    blocco_val = bars(p["valutazioni"]) if p.get("valutazioni") else tratti(p["tratti"])
    recensioni = ""
    if p.get("recensioni"):
        recensioni = f'''<div class="tablebox">
<table class="rev">
<thead><tr><th>Fonte</th><th>Valutazione</th><th>In sintesi</th></tr></thead>
<tbody>
{rev_rows(p["recensioni"])}
</tbody>
</table>
</div>'''
    return f'''<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(p["title_tag"])} | PadelMetrix</title>
<meta name="description" content="{e(p["meta_description"])}">
<link rel="canonical" href="https://www.padelmetrix.com/racchette/{slug}/">
<link rel="icon" href="{FAVICON}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False)}
</script>
<style>
{CSS}
</style>
</head>
<body>

<header class="site"><div class="wrap">
<a class="brand" href="/">{LOGO}<b>padel</b><span>metrix</span></a>
<nav class="main" aria-label="Principale">
{nav}
</nav>
</div></header>

<main class="wrap">
<nav class="crumbs" aria-label="Percorso"><a href="/">Home</a><span>›</span><a href="/racchette/">Racchette</a><span>›</span><a href="/racchette/?marca={marca_slug}">{e(d["marca"])}</a><span>›</span><span>{e(p["breadcrumb"])}</span></nav>

<div class="top">
<div class="photo">Foto della racchetta<br>(in arrivo dal programma di affiliazione)</div>
<div class="info">
<div>
<div class="eyebrow">{e(p["eyebrow"])}</div>
<h1>{e(nome_completo)}</h1>
</div>
<div class="chips">{chips(p["chips"])}</div>
<p class="lead">{e(p["lead"])}</p>
{avviso}
{blocco_val}

<div class="card">
<h2>Dove comprarla</h2>
<div class="stores">
{chr(10).join(store(s) for s in p["negozi"])}
</div>
<p class="note">{e(p["nota_prezzi"])} I link verso i negozi possono essere link di affiliazione: se acquisti, PadelMetrix può ricevere una commissione senza costi per te.</p>
</div>

<div style="display:flex;flex-wrap:wrap;gap:12px">
<a class="btn out" href="{e(p["confronta"]["url"])}">{e(p["confronta"]["testo"])}</a>
</div>
</div>
</div>

<section class="block">
<h2>Dati tecnici</h2>
<dl class="specs">
{specs(p["specifiche"])}
</dl>
<p class="note">{p["nota_specifiche_html"]}</p>
</section>

<section class="block">
<h2>Cosa dicono le recensioni</h2>
<div class="card">
<p style="margin:0;font-size:16px">{e(p["sintesi"])}</p>
</div>
<div class="two">
<div class="card pros"><h3>Punti di forza</h3><ul class="clean">{li(p["pro"])}</ul></div>
<div class="card cons"><h3>Limiti</h3><ul class="clean">{li(p["contro"])}</ul></div>
</div>
<div class="two">
<div class="card"><h3 style="font-size:17px">È adatta se</h3><ul class="clean">{li(p["adatta"])}</ul></div>
<div class="card"><h3 style="font-size:17px">Meglio un'altra se</h3><ul class="clean">{li(p["non_adatta"])}</ul></div>
</div>
{recensioni}
</section>

<div class="ad">Pubblicità</div>

<section class="block">
<h2>Racchette simili</h2>
<div class="sim">
{sim_cards(p["simili"])}
</div>
<p class="note">Altre alternative compariranno qui man mano che aggiungiamo racchette al database.</p>
</section>
</main>

<footer><div class="wrap">
<span style="max-width:760px">In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Alcuni link verso altri negozi sono link di affiliazione. Scheda aggiornata il {e(p["aggiornata"])}.</span>
<span>© 2026 PadelMetrix</span>
</div></footer>

</body>
</html>
'''


def main():
    n = 0
    for f in sorted(DATA.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if "pagina" not in d:
            print("salto (manca blocco pagina):", f.name)
            continue
        dest = OUT / d["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(d), encoding="utf-8")
        n += 1
        print("ok", d["slug"])
    print(n, "schede generate")


if __name__ == "__main__":
    main()
