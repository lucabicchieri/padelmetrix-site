#!/usr/bin/env python3
"""Genera le schede racchetta da data/racchette/*.json in it/racchette/, en/rackets/, es/palas/.

Uso:  python3 scripts/genera_schede.py
Ogni JSON contiene i dati tecnici e un blocco "pagina" con i testi editoriali in italiano;
le versioni inglese e spagnola passano dalla memoria di traduzione (scripts/traduci.py).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from comune import racket_svg  # noqa: E402
import sito as S  # noqa: E402
from sito import (L, P, ALT, tr, e, carica, coppie, confronto_url, crumbs, pagina, SITO, FORMA, LIVN, STILEN,  # noqa: E402
                  loc, loc_html, numero, euro, data_txt, data_it_to_iso, LINGUE, set_lang)
import traduci as T  # noqa: E402
_AF = pathlib.Path(__file__).resolve().parent.parent / "data" / "articoli.json"
ARTICOLI = json.loads(_AF.read_text(encoding="utf-8")) if _AF.exists() else []

ROOT = pathlib.Path(__file__).resolve().parent.parent

AMAZON = {"it": "www.amazon.it", "en": "www.amazon.co.uk", "es": "www.amazon.es"}
# Tracking ID del Programma Affiliazione Amazon per paese (None = programma non ancora attivo)
AMAZON_TAG = {"it": "padelmetrix-21", "en": None, "es": None}


def chips(items):
    return "".join(f"<span>{e(tr(c))}</span>" for c in items)


def li(items):
    return "".join(f"<li>{e(tr(x))}</li>" for x in items)


def bars(val):
    rows = []
    for r in val["voci"]:
        pct = round(r["valore"] / val["scala"] * 100)
        rows.append(
            f'<div class="bar"><span>{e(tr(r["nome"]))}</span><div class="track"><div class="fill" style="width:{pct}%"></div></div><span class="v">{numero(r["valore"])}</span></div>'
        )
    return f'''<div class="card">
<h2>{e(tr(val["titolo"]))}</h2>
<div class="bars">
{chr(10).join(rows)}
</div>
<p class="note">{loc_html(tr(val["nota_html"]))}</p>
</div>'''


def tratti(t):
    return f'''<div class="card">
<h2>{e(tr(t["titolo"]))}</h2>
<div class="chips">{chips(t["voci"])}</div>
<p class="note">{loc_html(tr(t["nota_html"]))}</p>
</div>'''


def store(s):
    cls = "btn lime" if s.get("amazon") else "btn"
    rel = "sponsored nofollow noopener" if s.get("amazon") else "nofollow noopener"
    u = s["url"]
    if s.get("amazon"):
        u = u.replace("www.amazon.it", AMAZON[S.lang()])
        tag = AMAZON_TAG[S.lang()]
        if tag and "tag=" not in u:
            u += ("&" if "?" in u else "?") + "tag=" + tag
    return f'<div class="store"><div><strong>{e(s["nome"])}</strong><small>{e(tr(s["nota"]))}</small></div><a class="{cls}" href="{e(u)}" rel="{rel}" target="_blank">{e(tr(s["pulsante"]))}</a></div>'


NON_TRADURRE = ("Marca", "Modello", "Giocatore", "Linea")


def specs(items):
    return "\n".join(f"<div><dt>{e(tr(k))}</dt><dd>{e(v if k in NON_TRADURRE else tr(v))}</dd></div>" for k, v in items)


def rev_rows(items):
    out = []
    for r in items:
        out.append(
            f'<tr><td><a href="{e(r["url"])}" rel="nofollow noopener" target="_blank">{e(r["fonte"])}</a></td><td>{e(tr(r["voto"]))}<br><small>{e(tr(r.get("voto_dettaglio", "")))}</small></td><td>{e(tr(r["sintesi"]))}</td></tr>'
        )
    return "\n".join(out)


def sim_cards(items):
    out = []
    for s in items:
        u = loc(s["url"]) if not s["url"].startswith("http") else s["url"]
        if u.startswith("/it/") and S.lang() == "it":
            pass
        ext = u.startswith("http")
        attrs = ' rel="nofollow noopener" target="_blank"' if ext else ""
        out.append(
            f'<a href="{e(u)}"{attrs}><small>{e(tr(s["sopra"]))}</small><b>{e(s["nome"])}</b><small>{e(tr(s["testo"]))}</small></a>'
        )
    return "\n".join(out)


def short_of(d):
    return f"{d['modello']} {d['anno']}"


def art(sh):
    """Articolo davanti al nome della racchetta."""
    return L(f"la {sh}", f"the {sh}", f"la {sh}")


def faq(d, n, db):
    """Domande frequenti costruite solo dai dati della scheda."""
    sh = short_of(d)
    qa = []
    if n["peso"]:
        b = n["bilanciamento"].split(" (")[0] if isinstance(n.get("bilanciamento"), str) else None
        bil = (L(f" con bilanciamento {b}", f" with {tr(b)} balance", f" con balance {tr(b)}") if b else "")
        qa.append((L(f"Quanto pesa la {sh}?", f"How much does the {sh} weigh?", f"¿Cuánto pesa la {sh}?"),
                   L(f"La {d['marca']} {sh} pesa {n['peso']}{bil}, secondo i dati dichiarati.",
                     f"The {d['marca']} {sh} weighs {n['peso']}{bil}, according to the declared specs.",
                     f"La {d['marca']} {sh} pesa {n['peso']}{bil}, según los datos declarados.")))
    if n["livello"]:
        lv = LIVN(n["livello"]).lower()
        st = STILEN(n["stile"]).lower() if n["stile"] else None
        qa.append((L(f"Per che livello è la {sh}?", f"What level is the {sh} for?", f"¿Para qué nivel es la {sh}?"),
                   L(f"È pensata per un livello {lv}.", f"It is designed for {lv} players.", f"Está pensada para un nivel {lv}.")
                   + ((L(f" Stile di gioco: {st}.", f" Playing style: {st}.", f" Estilo de juego: {st}.")) if st else "")))
    if n["forma"]:
        spieg = {"diamante": L("Le racchette a diamante concentrano il peso in testa: più potenza nello smash, meno tolleranza in difesa.",
                               "Diamond rackets concentrate the weight in the head: more power on the smash, less forgiveness in defence.",
                               "Las palas diamante concentran el peso en la cabeza: más potencia en el remate, menos tolerancia en defensa."),
                 "rotonda": L("Le racchette rotonde hanno lo sweet spot al centro e il peso verso il manico: più controllo e maneggevolezza.",
                              "Round rackets have the sweet spot in the centre and the weight towards the handle: more control and maneuverability.",
                              "Las palas redondas tienen el punto dulce en el centro y el peso hacia el mango: más control y manejabilidad."),
                 "goccia": L("La forma a goccia sta a metà tra rotonda e diamante: un compromesso tra controllo e potenza.",
                             "The teardrop shape sits between round and diamond: a compromise between control and power.",
                             "La forma de lágrima está a medio camino entre redonda y diamante: un compromiso entre control y potencia."),
                 "ibrida": L("La forma ibrida combina caratteristiche di goccia e diamante, per un gioco versatile.",
                             "The hybrid shape combines features of teardrop and diamond, for versatile play.",
                             "La forma híbrida combina características de lágrima y diamante, para un juego versátil.")}[n["forma"]]
        fo = FORMA(n["forma"]).lower()
        qa.append((L(f"Che forma ha la {sh}?", f"What shape is the {sh}?", f"¿Qué forma tiene la {sh}?"),
                   L(f"Ha forma {fo}. ", f"It has a {fo} shape. ", f"Tiene forma {fo}. ") + spieg))
    altre = [o for o in db if o["marca"] == n["marca"] and o["modello"] == n["modello"] and o["anno"] != n["anno"]]
    if altre:
        o = altre[0]
        diffs = []
        for k, lab in (("peso", L("peso", "weight", "peso")), ("forma", L("forma", "shape", "forma")),
                       ("superficie", L("superficie", "face", "cara")), ("nucleo", L("nucleo", "core", "núcleo"))):
            a, b = n.get(k), o.get(k)
            if a and b and str(a).lower() != str(b).lower():
                if k == "forma":
                    a, b = FORMA(a), FORMA(b)
                else:
                    a, b = tr(a), tr(b)
                diffs.append(L(f"{lab} {b} nella {o['anno']} contro {a} nella {n['anno']}",
                               f"{lab} {b} on the {o['anno']} versus {a} on the {n['anno']}",
                               f"{lab} {b} en la {o['anno']} frente a {a} en la {n['anno']}"))
        txt = (L("Differenze dichiarate: ", "Declared differences: ", "Diferencias declaradas: ") + "; ".join(diffs) + ".") if diffs else \
            L("Sulla carta i dati che abbiamo coincidono; le differenze sono nei dettagli costruttivi e nel design.",
              "On paper the data we have are the same; the differences are in construction details and design.",
              "Sobre el papel los datos que tenemos coinciden; las diferencias están en los detalles de construcción y en el diseño.")
        qa.append((L(f"Che differenza c'è tra la {sh} e la {o['modello']} {o['anno']}?",
                     f"What is the difference between the {sh} and the {o['modello']} {o['anno']}?",
                     f"¿Qué diferencia hay entre la {sh} y la {o['modello']} {o['anno']}?"),
                   txt + L(" Confronto completo nella pagina dedicata.", " Full comparison on the dedicated page.", " Comparación completa en la página dedicada.")))
    if n["prezzo"]:
        pr = euro(n["prezzo"])
        qa.append((L(f"Quanto costa la {sh}?", f"How much does the {sh} cost?", f"¿Cuánto cuesta la {sh}?"),
                   L(f"Il prezzo di listino indicativo è {pr}; nei negozi online si trova spesso scontata.",
                     f"The indicative list price is {pr}; online shops often sell it at a discount.",
                     f"El precio de lista orientativo es {pr}; en las tiendas online suele encontrarse rebajada.")))
    return qa[:5]


def frase_liv(k):
    return {"principiante": L("per chi inizia", "for beginners", "para quien empieza"),
            "principiante-intermedio": L("per principianti e intermedi", "for beginners and intermediates", "para principiantes e intermedios"),
            "intermedio": L("per giocatori intermedi", "for intermediate players", "para jugadores intermedios"),
            "intermedio-avanzato": L("per intermedi e avanzati", "for intermediate and advanced players", "para intermedios y avanzados"),
            "avanzato": L("per giocatori avanzati", "for advanced players", "para jugadores avanzados"),
            "professionale": L("per giocatori avanzati e agonisti", "for advanced and competitive players", "para jugadores avanzados y de competición")}[k]


def in_breve(d, n):
    """Risposta in una frase: cosa è questa racchetta, con i dati che abbiamo."""
    l = S.lang()
    junior = n["categoria"] == "junior"
    stile = {"offensivo": L("d'attacco", "attacking", "de ataque"), "controllo": L("di controllo", "control", "de control"),
             "polivalente": L("polivalente", "all-round", "polivalente")}.get(n["stile"])
    if l == "it":
        tipo = "racchetta junior" if junior else "racchetta"
        if n["forma"]:
            tipo += " " + {"diamante": "a diamante", "rotonda": "rotonda", "goccia": "a goccia", "ibrida": "ibrida"}[n["forma"]]
        if stile:
            tipo += " " + stile
        t = f"La {d['pagina']['titolo']} è una {tipo}"
        if n["peso"]:
            t += f" da {n['peso']}"
    elif l == "en":
        bits = [stile] if stile else []
        if n["forma"]:
            bits.append(FORMA(n["forma"]).lower())
        bits.append("junior racket" if junior else "racket")
        tipo = " ".join(bits)
        if n["peso"]:
            tipo = f"{n['peso']} " + tipo
        art_ = "an" if tipo[0] in "aeiou" else "a"
        t = f"The {d['pagina']['titolo']} is {art_} {tipo}"
    else:
        tipo = "pala junior" if junior else "pala"
        if n["forma"]:
            tipo += " " + {"diamante": "diamante", "rotonda": "redonda", "goccia": "de lágrima", "ibrida": "híbrida"}[n["forma"]]
        if stile:
            tipo += " " + stile
        t = f"La {d['pagina']['titolo']} es una {tipo}"
        if n["peso"]:
            t += f" de {n['peso']}"
    if n["livello"]:
        t += f" {frase_liv(n['livello'])}"
    if n["giocatore"] and "ispirata" not in n["giocatore"]:
        t += L(f", firmata da {n['giocatore']}", f", signed by {n['giocatore']}", f", firmada por {n['giocatore']}")
    return t + "."


def render(d, n, db, pair_set):
    p = d["pagina"]
    slug = d["slug"]
    nome_completo = p["titolo"]
    sh = short_of(d)
    path = P("racchette", slug)
    alt = ALT("racchette", slug)
    title = L(f"{nome_completo}: scheda tecnica, opinioni e prezzo", f"{nome_completo}: specs, reviews and price", f"{nome_completo}: ficha técnica, opiniones y precio")
    if len(title) > 68:
        title = L(f"{nome_completo}: scheda e opinioni", f"{nome_completo}: specs and reviews", f"{nome_completo}: ficha y opiniones")
    qa = faq(d, n, db)
    cr_html, cr_ld = crumbs([S.home_crumb(), (L("Racchette", "Rackets", "Palas"), P("racchette")), (d["marca"], P("marche", n["marca_slug"])), (p["breadcrumb"], None)])
    breve = in_breve(d, n)
    prod = {"@context": "https://schema.org", "@type": "Product", "name": nome_completo, "model": d["modello"],
            "brand": {"@type": "Brand", "name": d["marca"]}, "category": L("Racchetta da padel", "Padel racket", "Pala de pádel"),
            "description": p["meta_description"] if S.lang() == "it" else breve,
            "url": SITO + path}
    props = [{"@type": "PropertyValue", "name": k, "value": v} for k, v in
             ((L("Peso", "Weight", "Peso"), n["peso"]), (L("Forma", "Shape", "Forma"), FORMA(n["forma"])), (L("Collezione", "Collection", "Colección"), str(d["anno"]))) if v]
    if props:
        prod["additionalProperty"] = props
    iso = d.get("aggiornato", "2026-10-24")
    agg = data_txt(data_it_to_iso(p["aggiornata"]))
    webpage = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITO + path,
               "dateModified": iso, "inLanguage": S.lang(), "about": {"@type": "Product", "name": nome_completo},
               "author": S.autore(), "publisher": S.editore()}
    ld = [webpage, prod, cr_ld]
    if qa:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]})
    avviso = f'<div class="card avviso">{loc_html(tr(p["avviso_html"]))}</div>' if p.get("avviso_html") else ""
    for a in ARTICOLI:
        if d["slug"] in a["racchette"] and S.lang() in a["url"]:
            avviso += (f'<div class="card avviso"><p>{L("Approfondimento", "In depth", "En profundidad")}: '
                       f'<a href="{a["url"][S.lang()]}"><b>{e(a["titolo"][S.lang()])}</b></a></p></div>')
    blocco_val = bars(p["valutazioni"]) if p.get("valutazioni") else tratti(p["tratti"])
    recensioni = ""
    if p.get("recensioni"):
        recensioni = f"""<div class="tablebox">
<table class="rev">
<thead><tr><th>{L("Fonte", "Source", "Fuente")}</th><th>{L("Valutazione", "Rating", "Valoración")}</th><th>{L("In sintesi", "In short", "En resumen")}</th></tr></thead>
<tbody>
{rev_rows(p["recensioni"])}
</tbody>
</table>
</div>"""
    per = {x["slug"]: x for x in db}
    mie = [(a if b == slug else b) for a, b in pair_set if slug in (a, b)]
    if mie:
        primo = mie[0]
        conf_btn = f'<a class="btn out" href="{confronto_url(slug, primo)}">{L("Confronta con", "Compare with", "Comparar con")} {e(per[primo]["nome"])}</a>'
        conf_list = "".join(f'<li><a href="{confronto_url(slug, o)}">{e(sh)} vs {e(per[o]["nome"])}</a></li>' for o in mie)
        conf_sec = f'<div class="card"><h3 style="font-size:17px">{L("Confronti con la", "Comparisons with the", "Comparaciones con la")} {e(sh)}</h3><ul class="clean">{conf_list}</ul></div>'
    else:
        conf_btn = f'<a class="btn out" href="{P("confronta")}">{L("Confronta con un'altra racchetta", "Compare with another racket", "Comparar con otra pala")}</a>'
        conf_sec = ""
    faq_html = ""
    if qa:
        faq_html = f'<section class="block faq"><h2>{L("Domande frequenti sulla", "Frequently asked questions about the", "Preguntas frecuentes sobre la")} ' + e(sh) + "</h2>" + "".join(
            f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</section>"
    nota_aff = L("I link verso i negozi possono essere link di affiliazione: se acquisti, PadelMetrix può ricevere una commissione senza costi per te.",
                 "Links to shops may be affiliate links: if you buy, PadelMetrix may receive a commission at no cost to you.",
                 "Los enlaces a las tiendas pueden ser enlaces de afiliado: si compras, PadelMetrix puede recibir una comisión sin coste para ti.")
    corpo = f"""{cr_html}

<div class="top">
<div class="photo">{racket_svg(d.get("forma", "goccia"), 220, nome_completo)}</div>
<div class="info">
<div>
<div class="eyebrow">{e(tr(p["eyebrow"]))}</div>
<h1>{e(nome_completo)}</h1>
<p class="note" style="margin-top:6px">{L("Aggiornata il", "Updated on", "Actualizada el")} {e(agg)} · {L("dati con fonti citate", "data with cited sources", "datos con fuentes citadas")} · <a href="{P("chi-siamo")}">{L("metodo", "method", "método")}</a></p>
</div>
<p class="lead" style="font-weight:600;color:var(--ink)">{e(breve)}</p>
<div class="chips">{chips(p["chips"])}</div>
<p class="lead">{e(tr(p["lead"]))}</p>
{avviso}
{blocco_val}

<div class="card">
<h2>{L("Dove comprare la", "Where to buy the", "Dónde comprar la")} {e(sh)}</h2>
<div class="stores">
{chr(10).join(store(s) for s in p["negozi"])}
</div>
<p class="note">{e(tr(p["nota_prezzi"]))} {nota_aff}</p>
</div>

<div style="display:flex;flex-wrap:wrap;gap:12px">
{conf_btn}
<a class="btn out" href="{P("marche", n["marca_slug"])}">{L("Tutte le racchette", "All", "Todas las palas")} {e(d["marca"])}{L("", " rackets", "")}</a>
</div>
</div>
</div>

<section class="block">
<h2>{L("Dati tecnici della", "Technical specs of the", "Datos técnicos de la")} {e(sh)}</h2>
<dl class="specs">
{specs(p["specifiche"])}
</dl>
<p class="note">{loc_html(tr(p["nota_specifiche_html"]))}</p>
</section>

<section class="block">
<h2>{e(sh)}: {L("recensioni e opinioni", "reviews and opinions", "reseñas y opiniones")}</h2>
<div class="card">
<p style="margin:0;font-size:16px">{e(tr(p["sintesi"]))}</p>
</div>
<div class="two">
<div class="card pros"><h3>{L("Punti di forza", "Strengths", "Puntos fuertes")}</h3><ul class="clean">{li(p["pro"])}</ul></div>
<div class="card cons"><h3>{L("Limiti", "Limitations", "Limitaciones")}</h3><ul class="clean">{li(p["contro"])}</ul></div>
</div>
<div class="two">
<div class="card"><h3 style="font-size:17px">{L(f"La {e(sh)} è adatta se", f"The {e(sh)} is right for you if", f"La {e(sh)} es para ti si")}</h3><ul class="clean">{li(p["adatta"])}</ul></div>
<div class="card"><h3 style="font-size:17px">{L("Meglio un'altra racchetta se", "Better choose another racket if", "Mejor otra pala si")}</h3><ul class="clean">{li(p["non_adatta"])}</ul></div>
</div>
{recensioni}
</section>

<section class="block">
<h2>{L("Racchette simili alla", "Rackets similar to the", "Palas similares a la")} {e(sh)}</h2>
<div class="sim">
{sim_cards(p["simili"])}
</div>
{conf_sec}
</section>

{faq_html}
<p class="note" style="padding-bottom:24px">{L("Scheda aggiornata il", "Page updated on", "Ficha actualizada el")} {e(agg)}.</p>"""
    meta = breve + L(" Dati tecnici, opinioni e confronti.", " Specs, reviews and comparisons.", " Datos técnicos, opiniones y comparaciones.")
    if len(meta) > 165:
        meta = breve
    return pagina(f"{title} | PadelMetrix", meta, path, corpo, on="racchette", ld=ld, alt=alt)


def main():
    db = carica()
    pair_set = coppie(db)
    for l in LINGUE:
        set_lang(l)
        for n in db:
            S.scrivi(P("racchette", n["slug"]), render(n["d"], n, db, pair_set), alt=ALT("racchette", n["slug"]))
    set_lang("it")
    (ROOT / "scripts" / "pagine_schede.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(db), "schede x", len(LINGUE), "lingue,", len(pair_set), "coppie di confronto")
    for l in ("en", "es"):
        if T.MANCANTI[l]:
            print("non tradotti", l, len(T.MANCANTI[l]), sorted(T.MANCANTI[l])[:20])


if __name__ == "__main__":
    main()
