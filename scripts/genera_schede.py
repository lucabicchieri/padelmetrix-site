#!/usr/bin/env python3
"""Genera le schede racchetta da data/racchette/*.json in it/racchette/<slug>/index.html.

Uso:  python3 scripts/genera_schede.py
Ogni JSON contiene i dati tecnici e un blocco "pagina" con i testi editoriali.
"""
import html
import re
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comune import racket_svg  # noqa: E402
from sito import carica, coppie, confronto_url, crumbs, pagina, SITO, FORMA_IT, LIV_IT, STILE_IT  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "racchette"
OUT = ROOT / "it" / "racchette"

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


def loc(u):
    if u.startswith("/racchette/") or u.startswith("/confronta/"):
        return "/it" + u
    return u


def sim_cards(items):
    out = []
    for s in items:
        s = dict(s, url=loc(s["url"]))
        ext = s["url"].startswith("http")
        attrs = ' rel="nofollow noopener" target="_blank"' if ext else ""
        out.append(
            f'<a href="{e(s["url"])}"{attrs}><small>{e(s["sopra"])}</small><b>{e(s["nome"])}</b><small>{e(s["testo"])}</small></a>'
        )
    return "\n".join(out)




def short_of(d):
    return f"{d['modello']} {d['anno']}"


def faq(d, n, db):
    """Domande frequenti costruite solo dai dati della scheda."""
    sh = short_of(d)
    qa = []
    if n["peso"]:
        bil = f" con bilanciamento {n['bilanciamento'].split(' (')[0]}" if isinstance(n.get("bilanciamento"), str) else ""
        qa.append((f"Quanto pesa la {sh}?", f"La {d['marca']} {sh} pesa {n['peso']}{bil}, secondo i dati dichiarati."))
    if n["livello"]:
        qa.append((f"Per che livello è la {sh}?", f"È pensata per un livello {LIV_IT[n['livello']].lower()}."
                   + (f" Stile di gioco: {STILE_IT[n['stile']].lower()}." if n["stile"] else "")))
    if n["forma"]:
        qa.append((f"Che forma ha la {sh}?", f"Ha forma {FORMA_IT[n['forma']].lower()}. "
                   + {"diamante": "Le racchette a diamante concentrano il peso in testa: più potenza nello smash, meno tolleranza in difesa.",
                      "rotonda": "Le racchette rotonde hanno lo sweet spot al centro e il peso verso il manico: più controllo e maneggevolezza.",
                      "goccia": "La forma a goccia sta a metà tra rotonda e diamante: un compromesso tra controllo e potenza.",
                      "ibrida": "La forma ibrida combina caratteristiche di goccia e diamante, per un gioco versatile."}[n["forma"]]))
    altre = [o for o in db if o["marca"] == n["marca"] and o["modello"] == n["modello"] and o["anno"] != n["anno"]]
    if altre:
        o = altre[0]
        diffs = []
        for k, lab in (("peso", "peso"), ("forma", "forma"), ("superficie", "superficie"), ("nucleo", "nucleo")):
            a, b = n.get(k), o.get(k)
            if a and b and str(a).lower() != str(b).lower():
                diffs.append(f"{lab} {b} nella {o['anno']} contro {a} nella {n['anno']}")
        txt = ("Differenze dichiarate: " + "; ".join(diffs) + ".") if diffs else \
              "Sulla carta i dati che abbiamo coincidono; le differenze sono nei dettagli costruttivi e nel design."
        qa.append((f"Che differenza c'è tra la {sh} e la {o['modello']} {o['anno']}?", txt + f" Confronto completo nella pagina dedicata."))
    if n["prezzo"]:
        pr = f"{n['prezzo']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").replace(",00", "")
        qa.append((f"Quanto costa la {sh}?", f"Il prezzo di listino indicativo è {pr} €; nei negozi online si trova spesso scontata."))
    return qa[:5]


def render(d, n, db, pair_set):
    p = d["pagina"]
    slug = d["slug"]
    nome_completo = p["titolo"]
    sh = short_of(d)
    title = f"{nome_completo}: scheda tecnica, opinioni e prezzo"
    if len(title) > 68:
        title = f"{nome_completo}: scheda e opinioni"
    qa = faq(d, n, db)
    cr_html, cr_ld = crumbs([("Home", "/it/"), ("Racchette", "/it/racchette/"), (d["marca"], f"/it/marche/{n['marca_slug']}/"), (p["breadcrumb"], None)])
    prod = {"@context": "https://schema.org", "@type": "Product", "name": nome_completo, "model": d["modello"],
            "brand": {"@type": "Brand", "name": d["marca"]}, "category": "Racchetta da padel", "description": p["meta_description"],
            "url": f"{SITO}/it/racchette/{slug}/"}
    props = [{"@type": "PropertyValue", "name": k, "value": v} for k, v in
             (("Peso", n["peso"]), ("Forma", FORMA_IT.get(n["forma"])), ("Collezione", str(d["anno"]))) if v]
    if props:
        prod["additionalProperty"] = props
    ld = [prod, cr_ld]
    if qa:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]})
    avviso = f'<div class="card avviso">{p["avviso_html"]}</div>' if p.get("avviso_html") else ""
    blocco_val = bars(p["valutazioni"]) if p.get("valutazioni") else tratti(p["tratti"])
    recensioni = ""
    if p.get("recensioni"):
        recensioni = f"""<div class="tablebox">
<table class="rev">
<thead><tr><th>Fonte</th><th>Valutazione</th><th>In sintesi</th></tr></thead>
<tbody>
{rev_rows(p["recensioni"])}
</tbody>
</table>
</div>"""
    # confronti pubblicati che coinvolgono questa racchetta
    per = {x["slug"]: x for x in db}
    mie = [(a if b == slug else b) for a, b in pair_set if slug in (a, b)]
    if mie:
        primo = mie[0]
        conf_btn = f'<a class="btn out" href="{confronto_url(slug, primo)}">Confronta con {e(per[primo]["nome"])}</a>'
        conf_list = "".join(f'<li><a href="{confronto_url(slug, o)}">{e(sh)} vs {e(per[o]["nome"])}</a></li>' for o in mie)
        conf_sec = f'<div class="card"><h3 style="font-size:17px">Confronti con la {e(sh)}</h3><ul class="clean">{conf_list}</ul></div>'
    else:
        conf_btn = f'<a class="btn out" href="/it/confronta/">Confronta con un\'altra racchetta</a>'
        conf_sec = ""
    faq_html = ""
    if qa:
        faq_html = '<section class="block faq"><h2>Domande frequenti sulla ' + e(sh) + "</h2>" + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</section>"
    corpo = f"""{cr_html}

<div class="top">
<div class="photo">{racket_svg(d.get("forma", "goccia"), 220, nome_completo)}</div>
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
<h2>Dove comprare la {e(sh)}</h2>
<div class="stores">
{chr(10).join(store(s) for s in p["negozi"])}
</div>
<p class="note">{e(p["nota_prezzi"])} I link verso i negozi possono essere link di affiliazione: se acquisti, PadelMetrix può ricevere una commissione senza costi per te.</p>
</div>

<div style="display:flex;flex-wrap:wrap;gap:12px">
{conf_btn}
<a class="btn out" href="/it/marche/{n['marca_slug']}/">Tutte le racchette {e(d["marca"])}</a>
</div>
</div>
</div>

<section class="block">
<h2>Dati tecnici della {e(sh)}</h2>
<dl class="specs">
{specs(p["specifiche"])}
</dl>
<p class="note">{p["nota_specifiche_html"]}</p>
</section>

<section class="block">
<h2>{e(sh)}: recensioni e opinioni</h2>
<div class="card">
<p style="margin:0;font-size:16px">{e(p["sintesi"])}</p>
</div>
<div class="two">
<div class="card pros"><h3>Punti di forza</h3><ul class="clean">{li(p["pro"])}</ul></div>
<div class="card cons"><h3>Limiti</h3><ul class="clean">{li(p["contro"])}</ul></div>
</div>
<div class="two">
<div class="card"><h3 style="font-size:17px">La {e(sh)} è adatta se</h3><ul class="clean">{li(p["adatta"])}</ul></div>
<div class="card"><h3 style="font-size:17px">Meglio un'altra racchetta se</h3><ul class="clean">{li(p["non_adatta"])}</ul></div>
</div>
{recensioni}
</section>

<div class="ad">Pubblicità</div>

<section class="block">
<h2>Racchette simili alla {e(sh)}</h2>
<div class="sim">
{sim_cards(p["simili"])}
</div>
{conf_sec}
</section>

{faq_html}
<p class="note" style="padding-bottom:24px">Scheda aggiornata il {e(p["aggiornata"])}.</p>"""
    return pagina(f"{title} | PadelMetrix", p["meta_description"], f"/it/racchette/{slug}/", corpo, on="racchette", ld=ld)


def main():
    db = carica()
    pair_set = coppie(db)
    for n in db:
        dest = OUT / n["slug"] / "index.html"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render(n["d"], n, db, pair_set), encoding="utf-8")
    print(len(db), "schede generate,", len(pair_set), "coppie di confronto")


if __name__ == "__main__":
    main()
