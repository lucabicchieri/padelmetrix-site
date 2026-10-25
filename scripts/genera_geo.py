#!/usr/bin/env python3
"""Contenuti GEO in it/en/es: pagina metodo, report in numeri, dataset aperto, glossario, pagine risposta, llms.txt.
Tutti i numeri sono calcolati dal database delle schede; nessun dato inventato."""
import csv
import io
import json
import pathlib
import re
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import (ROOT, SITO, e, L, P, ALT, carica, crumbs, pagina, griglia, ordina, FORMA, LIVN, STILEN, slugify,  # noqa: E402
                  euro, data_txt, data_riga, LINGUE, set_lang, url_r, OGGI)

FORME = ("diamante", "rotonda", "goccia", "ibrida")
STILI = ("offensivo", "controllo", "polivalente")


def scrivi(path, txt, alt):
    S.scrivi(path, txt, alt)


def eur(x):
    return euro(round(x), dec=False)


def meta_art(titolo, desc, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titolo, "description": desc,
            "author": S.autore(), "publisher": S.editore(), "datePublished": OGGI, "dateModified": OGGI, "inLanguage": S.lang(),
            "mainEntityOfPage": SITO + path}


def pct(a, b):
    return round(100 * a / b) if b else 0


def barre(rows, unit="%"):
    mx = max(v for _, v in rows) or 1
    return '<div class="bars" style="max-width:640px">' + "".join(
        f'<div class="bar"><span>{e(k)}</span><div class="track"><div class="fill" style="width:{round(v / mx * 100)}%"></div></div><span class="v">{v}{unit}</span></div>'
        for k, v in rows) + "</div>"


def H():
    return S.home_crumb()


# ------------------------------------------------------------------ statistiche dal database

def statistiche(db):
    adulti = [n for n in db if n["categoria"] != "junior"]
    pesi = []
    for n in adulti:
        v = [int(x) for x in re.findall(r"\d{3}", n["peso"] or "")]
        if len(v) >= 2:
            pesi.append((v[0] + v[1]) / 2)
        elif len(v) == 1:
            pesi.append(v[0])
    forme = {f: sum(1 for n in adulti if n["forma"] == f) for f in FORME}
    con_forma = sum(forme.values())
    prezzi = [n["prezzo"] for n in adulti if n["prezzo"]]
    per_liv = {}
    for n in adulti:
        if n["prezzo"] and n["livello"]:
            per_liv.setdefault(n["livello"], []).append(n["prezzo"])
    marche = {}
    for n in db:
        marche[n["marca"]] = marche.get(n["marca"], 0) + 1
    sup = [str(n["superficie"] or "").lower() for n in adulti if n["superficie"]]
    carbonio = sum(1 for s in sup if "carbon" in s)
    vetro = sum(1 for s in sup if "vetro" in s and "carbon" not in s)
    ks = {}
    for s in sup:
        m = re.search(r"(\d+)k", s)
        if m:
            ks[m.group(1) + "K"] = ks.get(m.group(1) + "K", 0) + 1
    stili = {s: sum(1 for n in adulti if n["stile"] == s) for s in STILI}
    return dict(n=len(db), adulti=len(adulti), junior=len(db) - len(adulti), anni={a: sum(1 for n in db if n["anno"] == a) for a in sorted({n["anno"] for n in db})},
                pesi=pesi, forme=forme, con_forma=con_forma, prezzi=prezzi, per_liv=per_liv, marche=marche,
                sup=len(sup), carbonio=carbonio, vetro=vetro, ks=ks, stili=stili)


# ------------------------------------------------------------------ chi siamo e metodo

def chi_siamo(db):
    s = statistiche(db)
    cr, ld = crumbs([H(), (L("Chi siamo e metodo", "About and method", "Quiénes somos y método"), None)])
    cit = L(f"«Fonte: PadelMetrix (padelmetrix.com), {data_txt()}»", f"\"Source: PadelMetrix (padelmetrix.com), {data_txt()}\"", f"«Fuente: PadelMetrix (padelmetrix.com), {data_txt()}»")
    corpo = L(f'''{cr}
<div class="intro"><h1>Chi siamo e come lavoriamo</h1>
<p>PadelMetrix è un database indipendente di racchette da padel: {s["n"]} schede delle collezioni 2026 e 2027 di {len(s["marche"])} marche, con dati tecnici, fonti citate e confronti. Lo cura Luca Bicchieri.</p>{data_riga()}</div>
<div class="prose">
<h2>Da dove vengono i dati</h2>
<p>Ogni dato tecnico (peso, forma, bilanciamento, materiali, livello) viene dai siti dei produttori, dalle schede dei rivenditori specializzati o da test pubblicati. Ogni scheda elenca le sue fonti con il link. Quando due fonti non coincidono riportiamo quella della scheda prodotto; quando un dato non è pubblicato scriviamo "non dichiarato" invece di stimarlo.</p>
<h2>Punteggi e recensioni</h2>
<p>Dove esistono test indipendenti riportiamo i punteggi così come li ha pubblicati la fonte (per esempio Padelful o PadelZoom), sempre con il nome e il link. Non inventiamo voti. L'indice PadelMetrix, un punteggio unico calcolato con un metodo pubblico, è in preparazione: questa pagina ne descriverà la formula prima della pubblicazione.</p>
<h2>Indipendenza e guadagni</h2>
<p>PadelMetrix non vende racchette e non riceve compensi dai marchi per le schede. Alcuni link verso i negozi sono link di affiliazione: se acquisti, il sito può ricevere una piccola commissione senza costi per te. Le commissioni non influenzano dati, confronti e consigli.</p>
<h2>Ogni quanto aggiorniamo</h2>
<p>Il database si aggiorna quando escono nuove collezioni e quando cambiano prezzi o arrivano nuove recensioni. Ogni pagina mostra la data dell'ultimo aggiornamento. I dati sono disponibili anche come <a href="{P("dati")}">dataset aperto</a>.</p>
<h2>Citare PadelMetrix</h2>
<p>Puoi riprendere dati e statistiche citando la fonte: {cit}.</p>
</div>''', f'''{cr}
<div class="intro"><h1>About us and how we work</h1>
<p>PadelMetrix is an independent padel racket database: {s["n"]} pages from the 2026 and 2027 collections of {len(s["marche"])} brands, with specs, cited sources and comparisons. It is run by Luca Bicchieri.</p>{data_riga()}</div>
<div class="prose">
<h2>Where the data comes from</h2>
<p>Every technical value (weight, shape, balance, materials, level) comes from manufacturers' websites, specialist retailers' product pages or published tests. Each page lists its sources with a link. When two sources disagree we report the product page's value; when a value is not published we write "not stated" instead of estimating it.</p>
<h2>Scores and reviews</h2>
<p>Where independent tests exist we report the scores exactly as the source published them (for example Padelful or PadelZoom), always with its name and a link. We do not invent ratings. The PadelMetrix index, a single score calculated with a public method, is in preparation: this page will describe its formula before it is published.</p>
<h2>Independence and income</h2>
<p>PadelMetrix does not sell rackets and receives no payment from brands for its pages. Some links to shops are affiliate links: if you buy, the site may receive a small commission at no cost to you. Commissions do not influence data, comparisons or advice.</p>
<h2>How often we update</h2>
<p>The database is updated when new collections come out and when prices change or new reviews appear. Every page shows the date of its last update. The data is also available as an <a href="{P("dati")}">open dataset</a>.</p>
<h2>Citing PadelMetrix</h2>
<p>You may reuse data and statistics by citing the source: {cit}.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Quiénes somos y cómo trabajamos</h1>
<p>PadelMetrix es una base de datos independiente de palas de pádel: {s["n"]} fichas de las colecciones 2026 y 2027 de {len(s["marche"])} marcas, con datos técnicos, fuentes citadas y comparativas. La lleva Luca Bicchieri.</p>{data_riga()}</div>
<div class="prose">
<h2>De dónde vienen los datos</h2>
<p>Cada dato técnico (peso, forma, balance, materiales, nivel) procede de las webs de los fabricantes, de las fichas de tiendas especializadas o de pruebas publicadas. Cada ficha enumera sus fuentes con el enlace. Cuando dos fuentes no coinciden indicamos la de la ficha de producto; cuando un dato no está publicado escribimos "no declarado" en lugar de estimarlo.</p>
<h2>Puntuaciones y reseñas</h2>
<p>Donde existen pruebas independientes indicamos las puntuaciones tal como las publicó la fuente (por ejemplo Padelful o PadelZoom), siempre con su nombre y enlace. No inventamos notas. El índice PadelMetrix, una puntuación única calculada con un método público, está en preparación: esta página describirá su fórmula antes de la publicación.</p>
<h2>Independencia e ingresos</h2>
<p>PadelMetrix no vende palas y no recibe pagos de las marcas por las fichas. Algunos enlaces a tiendas son enlaces de afiliado: si compras, la web puede recibir una pequeña comisión sin coste para ti. Las comisiones no influyen en los datos, las comparativas ni los consejos.</p>
<h2>Cada cuánto actualizamos</h2>
<p>La base de datos se actualiza cuando salen nuevas colecciones y cuando cambian los precios o llegan nuevas reseñas. Cada página muestra la fecha de su última actualización. Los datos también están disponibles como <a href="{P("dati")}">dataset abierto</a>.</p>
<h2>Citar PadelMetrix</h2>
<p>Puedes reutilizar datos y estadísticas citando la fuente: {cit}.</p>
</div>''')
    about = {"@context": "https://schema.org", "@type": "AboutPage", "name": L("Chi siamo e metodo", "About and method", "Quiénes somos y método"), "dateModified": OGGI,
             "publisher": S.editore(), "author": S.autore()}
    path, alt = P("chi-siamo"), ALT("chi-siamo")
    scrivi(path, pagina(L("Chi siamo e metodo: come PadelMetrix raccoglie i dati sulle racchette | PadelMetrix", "About and method: how PadelMetrix collects padel racket data | PadelMetrix",
                          "Quiénes somos y método: cómo PadelMetrix recoge los datos de las palas | PadelMetrix"),
                        L("Chi cura PadelMetrix, da dove vengono i dati sulle racchette da padel, come trattiamo punteggi e recensioni e come guadagniamo.",
                          "Who runs PadelMetrix, where the padel racket data comes from, how we handle scores and reviews and how we earn money.",
                          "Quién lleva PadelMetrix, de dónde vienen los datos de las palas de pádel, cómo tratamos puntuaciones y reseñas y cómo ganamos dinero."),
                        path, corpo, ld=[ld, about], alt=alt), alt)


# ------------------------------------------------------------------ report in numeri

REPORT = "racchette-padel-2026-2027-in-numeri"


def report(db):
    s = statistiche(db)
    med_peso = round(statistics.median(s["pesi"]))
    min_p, max_p = round(min(s["pesi"])), round(max(s["pesi"]))
    med_prezzo = statistics.median(s["prezzi"])
    forma_top = max(s["forme"], key=lambda f: s["forme"][f])
    forme_rows = [(FORMA(f), pct(c, s["con_forma"])) for f, c in sorted(s["forme"].items(), key=lambda kv: -kv[1]) if c]
    liv_rows = []
    for lv in S.LIV:
        if lv in s["per_liv"] and len(s["per_liv"][lv]) >= 3:
            liv_rows.append((LIVN(lv), round(statistics.median(s["per_liv"][lv])), len(s["per_liv"][lv])))
    marche_rows = sorted(s["marche"].items(), key=lambda kv: -kv[1])
    k_rows = sorted(s["ks"].items(), key=lambda kv: -kv[1])[:5]
    stili_tot = sum(s["stili"].values())
    path, alt = P("report", REPORT), ALT("report", REPORT)
    titolo = L("Racchette da padel 2026–2027 in numeri", "Padel rackets 2026–2027 in numbers", "Palas de pádel 2026–2027 en cifras")
    ft = FORMA(forma_top).lower()
    pf = pct(s['forme'][forma_top], s['con_forma'])
    intro = L(f"Secondo il database PadelMetrix ({s['n']} racchette delle collezioni 2026 e 2027), la racchetta da padel tipica per adulti pesa circa {med_peso} g, ha forma {ft} ({pf}% dei modelli con forma dichiarata) e costa {eur(med_prezzo)} di listino (valore mediano).",
              f"According to the PadelMetrix database ({s['n']} rackets from the 2026 and 2027 collections), the typical adult padel racket weighs about {med_peso} g, has a {ft} shape ({pf}% of models with a declared shape) and has a list price of {eur(med_prezzo)} (median).",
              f"Según la base de datos PadelMetrix ({s['n']} palas de las colecciones 2026 y 2027), la pala de pádel típica para adultos pesa unos {med_peso} g, tiene forma {ft} ({pf}% de los modelos con forma declarada) y cuesta {eur(med_prezzo)} de precio de lista (valor mediano).")
    cr, ld = crumbs([H(), (L("Report", "Report", "Informe"), None), (titolo, None)])
    anni = ", ".join(L(f"{c} del {a}", f"{c} from {a}", f"{c} de {a}") for a, c in s["anni"].items())
    citaz = L(f"«PadelMetrix, Racchette da padel 2026–2027 in numeri, {data_txt()}, padelmetrix.com»",
              f"\"PadelMetrix, Padel rackets 2026–2027 in numbers, {data_txt()}, padelmetrix.com\"",
              f"«PadelMetrix, Palas de pádel 2026–2027 en cifras, {data_txt()}, padelmetrix.com»")
    corpo = f'''{cr}
<div class="intro"><h1>{titolo}</h1><p>{e(intro)}</p>{data_riga()}</div>
<div class="prose">
<h2>{L("Le cifre principali", "Key figures", "Las cifras principales")}</h2>
<table class="tab"><tbody>
<tr><td>{L("Racchette analizzate", "Rackets analysed", "Palas analizadas")}</td><td><b>{s["n"]}</b> ({anni})</td></tr>
<tr><td>{L("Marche", "Brands", "Marcas")}</td><td><b>{len(s["marche"])}</b></td></tr>
<tr><td>{L("Modelli junior", "Junior models", "Modelos junior")}</td><td><b>{s["junior"]}</b></td></tr>
<tr><td>{L("Peso tipico (adulti, mediana)", "Typical weight (adults, median)", "Peso típico (adultos, mediana)")}</td><td><b>{med_peso} g</b>, {L(f"da {min_p} a {max_p} g su {len(s['pesi'])} modelli con peso dichiarato", f"from {min_p} to {max_p} g across {len(s['pesi'])} models with a declared weight", f"de {min_p} a {max_p} g en {len(s['pesi'])} modelos con peso declarado")}</td></tr>
<tr><td>{L("Prezzo di listino (mediana)", "List price (median)", "Precio de lista (mediana)")}</td><td><b>{eur(med_prezzo)}</b> {L(f"su {len(s['prezzi'])} modelli con prezzo rilevato", f"across {len(s['prezzi'])} models with a recorded price", f"en {len(s['prezzi'])} modelos con precio registrado")}</td></tr>
<tr><td>{L("Superficie in carbonio", "Carbon face", "Cara de carbono")}</td><td><b>{pct(s["carbonio"], s["sup"])}%</b> {L(f"dei modelli con superficie dichiarata; fibra di vetro {pct(s['vetro'], s['sup'])}%", f"of models with a declared face; fiberglass {pct(s['vetro'], s['sup'])}%", f"de los modelos con cara declarada; fibra de vidrio {pct(s['vetro'], s['sup'])}%")}</td></tr>
</tbody></table>
<h2>{L("Che forma hanno le racchette", "What shape the rackets are", "Qué forma tienen las palas")}</h2>
<p>{L(f"La forma {ft} è la più diffusa. Quota sui {s['con_forma']} modelli per adulti con forma dichiarata:", f"The {ft} shape is the most common. Share across the {s['con_forma']} adult models with a declared shape:", f"La forma {ft} es la más común. Cuota sobre los {s['con_forma']} modelos para adultos con forma declarada:")}</p>
{barre(forme_rows)}
<h2>{L("Attacco, controllo o polivalenti", "Attack, control or all-round", "Ataque, control o polivalentes")}</h2>
<p>{L(f"Stile di gioco indicato da produttori e rivenditori, su {stili_tot} modelli per adulti:", f"Playing style stated by manufacturers and retailers, across {stili_tot} adult models:", f"Estilo de juego indicado por fabricantes y tiendas, sobre {stili_tot} modelos para adultos:")}</p>
{barre([(STILEN(k), pct(v, stili_tot)) for k, v in sorted(s["stili"].items(), key=lambda kv: -kv[1]) if v])}
<h2>{L("Quanto costano, per livello", "How much they cost, by level", "Cuánto cuestan, por nivel")}</h2>
<table class="tab"><thead><tr><th>{L("Livello", "Level", "Nivel")}</th><th>{L("Prezzo di listino mediano", "Median list price", "Precio de lista mediano")}</th><th>{L("Modelli", "Models", "Modelos")}</th></tr></thead><tbody>
{"".join(f"<tr><td>{e(lv)}</td><td>{eur(p)}</td><td>{c}</td></tr>" for lv, p, c in liv_rows)}
</tbody></table>
<h2>{L("Il carbonio più usato", "The most used carbon", "El carbono más usado")}</h2>
<p>{L("Tipi di carbonio dichiarati più frequenti nelle superfici (numero di modelli):", "Most frequently declared carbon types in the faces (number of models):", "Tipos de carbono declarados más frecuentes en las caras (número de modelos):")}</p>
{barre(k_rows, unit="")}
<h2>{L("Modelli per marca", "Models by brand", "Modelos por marca")}</h2>
<table class="tab"><thead><tr><th>{L("Marca", "Brand", "Marca")}</th><th>{L("Racchette nel database", "Rackets in the database", "Palas en la base de datos")}</th></tr></thead><tbody>
{"".join(f'<tr><td><a href="{P("marche", slugify(m))}">{e(m)}</a></td><td>{c}</td></tr>' for m, c in marche_rows)}
</tbody></table>
<h2>{L("Metodo e limiti", "Method and limitations", "Método y limitaciones")}</h2>
<p>{L(f'I numeri sono calcolati sulle schede del database PadelMetrix, che copre le collezioni 2026 e 2027 delle marche principali ma non tutto il mercato. Peso e prezzo sono quelli dichiarati da produttori e rivenditori; per il peso usiamo il punto medio dell\'intervallo dichiarato. Il numero di modelli per marca riflette la copertura del database, non le quote di mercato. I dati completi sono nel <a href="{P("dati")}">dataset aperto</a>.',
      f'The figures are calculated from the pages in the PadelMetrix database, which covers the 2026 and 2027 collections of the main brands but not the whole market. Weight and price are those declared by manufacturers and retailers; for weight we use the midpoint of the declared range. The number of models per brand reflects the database coverage, not market share. The full data is in the <a href="{P("dati")}">open dataset</a>.',
      f'Las cifras se calculan sobre las fichas de la base de datos PadelMetrix, que cubre las colecciones 2026 y 2027 de las principales marcas pero no todo el mercado. Peso y precio son los declarados por fabricantes y tiendas; para el peso usamos el punto medio del intervalo declarado. El número de modelos por marca refleja la cobertura de la base de datos, no las cuotas de mercado. Los datos completos están en el <a href="{P("dati")}">dataset abierto</a>.')}</p>
<p>{L("Citazione suggerita:", "Suggested citation:", "Cita sugerida:")} {citaz}.</p>
</div>'''
    desc = intro[:300]
    scrivi(path, pagina(L(f"{titolo}: peso, forme, prezzi e materiali | PadelMetrix", f"{titolo}: weight, shapes, prices and materials | PadelMetrix", f"{titolo}: peso, formas, precios y materiales | PadelMetrix"),
                        desc, path, corpo, ld=[ld, meta_art(titolo, desc, path)], alt=alt), alt)
    return s, med_peso, min_p, max_p, med_prezzo, forma_top, liv_rows


# ------------------------------------------------------------------ dataset aperto

CAMPI = ["slug", "marca", "modello", "anno", "giocatore", "categoria", "forma", "peso", "bilanciamento", "nucleo", "superficie",
         "telaio", "tatto", "livello", "stile", "prezzo_listino_eur", "url", "fonti"]


def file_dataset(db):
    """Il dataset resta unico (valori in italiano, URL delle schede italiane)."""
    righe = []
    for n in ordina(db):
        d = n["d"]
        righe.append({"slug": n["slug"], "marca": n["marca"], "modello": n["modello"], "anno": n["anno"], "giocatore": n["giocatore"] or "",
                      "categoria": n["categoria"], "forma": n["forma"] or "", "peso": n["peso"] or "",
                      "bilanciamento": d.get("bilanciamento") if isinstance(d.get("bilanciamento"), str) else "",
                      "nucleo": n["nucleo"] if isinstance(n["nucleo"], str) else "", "superficie": n["superficie"] or "",
                      "telaio": d.get("telaio") if isinstance(d.get("telaio"), str) else "",
                      "tatto": n["sensazione"] if isinstance(n["sensazione"], str) else "", "livello": n["livello"] or "",
                      "stile": n["stile"] or "", "prezzo_listino_eur": n["prezzo"] or "", "url": SITO + P("racchette", n["slug"], "it"),
                      "fonti": " | ".join(d.get("fonti_dati", []))})
    out = ROOT / "dati"
    out.mkdir(exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPI)
    w.writeheader()
    w.writerows(righe)
    (out / "racchette-padelmetrix.csv").write_text(buf.getvalue(), encoding="utf-8")
    (out / "racchette-padelmetrix.json").write_text(json.dumps({"fonte": "PadelMetrix (padelmetrix.com)", "licenza": "CC BY 4.0", "aggiornato": OGGI, "racchette": righe}, ensure_ascii=False, indent=1), encoding="utf-8")
    return len(righe)


def dataset(nr):
    ds = {"@context": "https://schema.org", "@type": "Dataset",
          "name": L("Racchette da padel 2026–2027 — PadelMetrix", "Padel rackets 2026–2027 — PadelMetrix", "Palas de pádel 2026–2027 — PadelMetrix"),
          "description": L(f"Dati tecnici di {nr} racchette da padel delle collezioni 2026 e 2027: marca, modello, forma, peso, bilanciamento, materiali, livello, stile, prezzo di listino e fonti.",
                           f"Technical data for {nr} padel rackets from the 2026 and 2027 collections: brand, model, shape, weight, balance, materials, level, style, list price and sources.",
                           f"Datos técnicos de {nr} palas de pádel de las colecciones 2026 y 2027: marca, modelo, forma, peso, balance, materiales, nivel, estilo, precio de lista y fuentes."),
          "url": SITO + P("dati"), "license": "https://creativecommons.org/licenses/by/4.0/", "creator": S.editore(), "dateModified": OGGI,
          "inLanguage": S.lang(), "keywords": ["padel", "racchette da padel", "pale da padel", "padel rackets", "palas de pádel"],
          "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITO + "/dati/racchette-padelmetrix.csv"},
                           {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": SITO + "/dati/racchette-padelmetrix.json"}]}
    cr, ld = crumbs([H(), (L("Dati aperti", "Open data", "Datos abiertos"), None)])
    cit = L(f"«Fonte: PadelMetrix (padelmetrix.com), {data_txt()}»", f"\"Source: PadelMetrix (padelmetrix.com), {data_txt()}\"", f"«Fuente: PadelMetrix (padelmetrix.com), {data_txt()}»")
    rep = P("report", REPORT)
    corpo = f'''{cr}
<div class="intro"><h1>{L("Dataset aperto delle racchette da padel", "Open padel racket dataset", "Dataset abierto de palas de pádel")}</h1><p>{L(f"Il database PadelMetrix è scaricabile gratis: {nr} racchette delle collezioni 2026 e 2027 con marca, modello, forma, peso, bilanciamento, materiali, livello, stile, prezzo di listino e le fonti di ogni scheda. Licenza CC BY 4.0: puoi usarlo citando PadelMetrix.",
       f"The PadelMetrix database can be downloaded for free: {nr} rackets from the 2026 and 2027 collections with brand, model, shape, weight, balance, materials, level, style, list price and the sources for each page. CC BY 4.0 licence: you can use it by crediting PadelMetrix.",
       f"La base de datos PadelMetrix se puede descargar gratis: {nr} palas de las colecciones 2026 y 2027 con marca, modelo, forma, peso, balance, materiales, nivel, estilo, precio de lista y las fuentes de cada ficha. Licencia CC BY 4.0: puedes usarla citando PadelMetrix.")}</p>{data_riga()}</div>
<div class="prose">
<p><a class="btn" href="/dati/racchette-padelmetrix.csv" download>{L("Scarica CSV", "Download CSV", "Descargar CSV")}</a> &nbsp; <a class="btn out" href="/dati/racchette-padelmetrix.json" download>{L("Scarica JSON", "Download JSON", "Descargar JSON")}</a></p>
<h2>{L("Campi", "Fields", "Campos")}</h2><p>{", ".join(f"<code>{c}</code>" for c in CAMPI)}. {L("I campi vuoti indicano dati non dichiarati dalle fonti.", "Empty fields mean data not stated by the sources. Field names and values are in Italian.", "Los campos vacíos indican datos no declarados por las fuentes. Los nombres y valores de los campos están en italiano.")}</p>
<h2>{L("Licenza e citazione", "Licence and citation", "Licencia y cita")}</h2><p>{L("Dati rilasciati con licenza", "Data released under the", "Datos publicados con licencia")} <a href="https://creativecommons.org/licenses/by/4.0/{L("deed.it", "", "deed.es")}" rel="noopener" target="_blank">{L("Creative Commons Attribuzione 4.0", "Creative Commons Attribution 4.0 licence", "Creative Commons Atribución 4.0")}</a>. {L("Citazione:", "Citation:", "Cita:")} {cit}. {L("I punteggi di siti terzi non sono inclusi: restano di proprietà delle rispettive fonti.", "Third-party scores are not included: they remain the property of their sources.", "Las puntuaciones de webs de terceros no están incluidas: siguen siendo propiedad de sus fuentes.")}</p>
<p>{L(f'Le statistiche principali sono nel report <a href="{rep}">Racchette da padel 2026–2027 in numeri</a>.', f'The main statistics are in the report <a href="{rep}">Padel rackets 2026–2027 in numbers</a>.', f'Las estadísticas principales están en el informe <a href="{rep}">Palas de pádel 2026–2027 en cifras</a>.')}</p>
</div>'''
    path, alt = P("dati"), ALT("dati")
    scrivi(path, pagina(L("Dataset aperto racchette da padel 2026–2027 (CSV e JSON) | PadelMetrix", "Open padel racket dataset 2026–2027 (CSV and JSON) | PadelMetrix",
                          "Dataset abierto de palas de pádel 2026–2027 (CSV y JSON) | PadelMetrix"),
                        L(f"Scarica gratis i dati tecnici di {nr} racchette da padel 2026 e 2027 in CSV e JSON, con licenza CC BY 4.0.",
                          f"Download for free the technical data of {nr} padel rackets from 2026 and 2027 in CSV and JSON, under a CC BY 4.0 licence.",
                          f"Descarga gratis los datos técnicos de {nr} palas de pádel 2026 y 2027 en CSV y JSON, con licencia CC BY 4.0."),
                        path, corpo, ld=[ld, ds], alt=alt), alt)


# ------------------------------------------------------------------ glossario
# (slug italiano, (nome it, en, es), (definizione it, en, es), (testo it, en, es), (sezione, slug) del link)

GLOSSARIO = [
    ("bilanciamento", ("Bilanciamento", "Balance", "Balance"),
     ("Il bilanciamento è la distanza del baricentro della racchetta dal fondo del manico, espressa in millimetri o centimetri.",
      "Balance is the distance of the racket's centre of gravity from the end of the handle, expressed in millimetres or centimetres.",
      "El balance es la distancia del centro de gravedad de la pala al final del mango, expresada en milímetros o centímetros."),
     ("Più è alta, più il peso è spostato verso la testa: la racchetta dà più potenza nello smash ma è meno maneggevole e affatica di più il braccio. Un bilanciamento basso sposta il peso verso il manico e favorisce controllo e velocità di reazione. Per esempio, tra i modelli del database 255 mm è considerato basso e 270 mm alto.",
      "The higher it is, the more the weight shifts towards the head: the racket gives more smash power but is less maneuverable and tires the arm more. A low balance shifts the weight towards the handle and favours control and reaction speed. For example, among the models in the database 255 mm is considered low and 270 mm high.",
      "Cuanto más alto, más peso hay hacia la cabeza: la pala da más potencia en el remate pero es menos manejable y cansa más el brazo. Un balance bajo desplaza el peso hacia el mango y favorece el control y la velocidad de reacción. Por ejemplo, entre los modelos de la base de datos 255 mm se considera bajo y 270 mm alto."),
     ("guide", "forme-racchetta-padel")),
    ("swingweight", ("Swingweight", "Swingweight", "Swingweight"),
     ("Lo swingweight misura quanto la racchetta \"pesa\" mentre la si muove, cioè la sua inerzia attorno al punto di impugnatura.",
      "Swingweight measures how \"heavy\" the racket feels while you swing it, that is, its inertia around the grip point.",
      "El swingweight mide cuánto \"pesa\" la pala mientras se mueve, es decir, su inercia alrededor del punto de empuñadura."),
     ("Due racchette con lo stesso peso possono avere swingweight diversi se il peso è distribuito diversamente. Uno swingweight alto dà stabilità e potenza ma rende la racchetta più lenta da muovere; uno basso la rende più rapida a rete. Pochi produttori lo dichiarano: alcuni negozi lo misurano, e in quel caso lo riportiamo nelle schede.",
      "Two rackets with the same weight can have different swingweights if the weight is distributed differently. A high swingweight gives stability and power but makes the racket slower to move; a low one makes it quicker at the net. Few manufacturers declare it: some shops measure it, and in that case we report it on the pages.",
      "Dos palas con el mismo peso pueden tener swingweights distintos si el peso está repartido de otra forma. Un swingweight alto da estabilidad y potencia pero hace la pala más lenta de mover; uno bajo la hace más rápida en la red. Pocos fabricantes lo declaran: algunas tiendas lo miden, y en ese caso lo indicamos en las fichas."),
     ("racchette", None)),
    ("sweet-spot", ("Sweet spot", "Sweet spot", "Punto dulce"),
     ("Lo sweet spot è la zona della superficie in cui l'impatto con la palla dà la risposta migliore: più controllo, meno vibrazioni e uscita di palla più pulita.",
      "The sweet spot is the area of the face where contact with the ball gives the best response: more control, less vibration and cleaner ball output.",
      "El punto dulce es la zona de la cara en la que el impacto con la bola da la mejor respuesta: más control, menos vibraciones y una salida de bola más limpia."),
     ("Nelle racchette rotonde è al centro e più ampio; nelle racchette a diamante è più in alto e più piccolo. Uno sweet spot ampio perdona di più i colpi decentrati ed è utile a chi inizia.",
      "On round rackets it is central and larger; on diamond rackets it is higher and smaller. A large sweet spot forgives off-centre hits more and is useful for beginners.",
      "En las palas redondas está en el centro y es más amplio; en las palas diamante está más arriba y es más pequeño. Un punto dulce amplio perdona más los golpes descentrados y es útil para quien empieza."),
     ("guide", "racchetta-padel-principianti")),
    ("eva", ("Gomma EVA", "EVA rubber", "Goma EVA"),
     ("L'EVA (etilene vinil acetato) è la gomma più usata per il nucleo delle racchette da padel.",
      "EVA (ethylene-vinyl acetate) is the most widely used rubber for padel racket cores.",
      "La EVA (etileno vinil acetato) es la goma más usada para el núcleo de las palas de pádel."),
     ("Esiste in diverse densità: l'EVA morbida (soft) assorbe le vibrazioni e aiuta l'uscita di palla con poco sforzo; l'EVA dura (hard) restituisce più potenza ai colpi forti ma chiede più forza e tecnica. Molti marchi usano nuclei a più strati con densità diverse.",
      "It comes in different densities: soft EVA absorbs vibration and helps ball output with little effort; hard EVA returns more power on hard shots but demands more strength and technique. Many brands use multi-layer cores with different densities.",
      "Existe en distintas densidades: la EVA blanda (soft) absorbe las vibraciones y ayuda a la salida de bola con poco esfuerzo; la EVA dura (hard) devuelve más potencia en los golpes fuertes pero exige más fuerza y técnica. Muchas marcas usan núcleos de varias capas con densidades distintas."),
     ("guide", "racchetta-padel-epicondilite")),
    ("foam", ("Foam", "Foam", "Foam"),
     ("Il foam è una schiuma usata come nucleo in alternativa all'EVA, in genere più morbida e più elastica.",
      "Foam is a material used as a core instead of EVA, generally softer and more elastic.",
      "El foam es una espuma usada como núcleo en lugar de la EVA, en general más blanda y elástica."),
     ("Dà una sensazione più soffice e una buona uscita di palla anche a ritmo basso, a scapito di un po' di precisione nei colpi violenti. Head, per esempio, usa nuclei Power Foam e Control Foam.",
      "It gives a softer feel and good ball output even at low pace, at the expense of some precision on violent shots. Head, for example, uses Power Foam and Control Foam cores.",
      "Da una sensación más suave y una buena salida de bola incluso a ritmo bajo, a costa de algo de precisión en los golpes violentos. Head, por ejemplo, usa núcleos Power Foam y Control Foam."),
     ("marche", "head")),
    ("carbonio-3k-12k-18k", ("Carbonio 3K, 12K, 18K", "3K, 12K, 18K carbon", "Carbono 3K, 12K, 18K"),
     ("La sigla K indica quante migliaia di filamenti compongono ogni fascio di fibra di carbonio usato nella superficie: 3K vuol dire 3.000 filamenti.",
      "The K figure indicates how many thousand filaments make up each carbon fibre tow used in the face: 3K means 3,000 filaments.",
      "La sigla K indica cuántos miles de filamentos forman cada haz de fibra de carbono usado en la cara: 3K significa 3.000 filamentos."),
     ("Il numero cambia la trama del tessuto e la sensazione al tatto, ma da solo non dice se una racchetta è più rigida o più potente: contano anche resina, numero di strati e nucleo. In generale le superfici in carbonio sono più rigide e precise di quelle in fibra di vetro.",
      "The number changes the weave of the fabric and the feel, but on its own it doesn't tell you whether a racket is stiffer or more powerful: resin, number of layers and core matter too. In general, carbon faces are stiffer and more precise than fiberglass ones.",
      "El número cambia la trama del tejido y la sensación al tacto, pero por sí solo no dice si una pala es más rígida o más potente: también cuentan la resina, el número de capas y el núcleo. En general las caras de carbono son más rígidas y precisas que las de fibra de vidrio."),
     ("report", REPORT)),
    ("fibra-di-vetro", ("Fibra di vetro", "Fiberglass", "Fibra de vidrio"),
     ("La fibra di vetro è un materiale per superfici e telai più flessibile ed economico del carbonio.",
      "Fiberglass is a face and frame material that is more flexible and cheaper than carbon.",
      "La fibra de vidrio es un material para caras y marcos más flexible y económico que el carbono."),
     ("Una superficie in fibra di vetro si deforma di più all'impatto: tatto morbido, uscita di palla facile e più comfort, a scapito di precisione e durata. È il materiale tipico delle racchette per principianti e di molte racchette junior.",
      "A fiberglass face deforms more on impact: soft feel, easy ball output and more comfort, at the expense of precision and durability. It is the typical material of beginner rackets and many junior rackets.",
      "Una cara de fibra de vidrio se deforma más en el impacto: tacto blando, salida de bola fácil y más confort, a costa de precisión y durabilidad. Es el material típico de las palas para principiantes y de muchas palas junior."),
     ("guide", "racchette-padel-economiche")),
    ("racchetta-diamante", ("Racchetta a diamante", "Diamond racket", "Pala diamante"),
     ("Una racchetta a diamante ha la testa più larga in alto e il peso spostato verso la punta.",
      "A diamond racket has a head that is wider at the top and weight shifted towards the tip.",
      "Una pala diamante tiene la cabeza más ancha arriba y el peso desplazado hacia la punta."),
     ("È la forma della potenza: aiuta negli smash e nelle volée d'attacco, ma ha uno sweet spot più alto e piccolo ed è meno tollerante in difesa. È adatta a giocatori con buona tecnica che giocano spesso a rete.",
      "It is the power shape: it helps on smashes and attacking volleys, but has a higher, smaller sweet spot and is less forgiving in defence. It suits players with good technique who often play at the net.",
      "Es la forma de la potencia: ayuda en los remates y las voleas de ataque, pero tiene un punto dulce más alto y pequeño y es menos tolerante en defensa. Es adecuada para jugadores con buena técnica que juegan a menudo en la red."),
     ("guide", "racchette-padel-potenza")),
    ("racchetta-rotonda", ("Racchetta rotonda", "Round racket", "Pala redonda"),
     ("Una racchetta rotonda ha la testa circolare e il peso spostato verso il manico.",
      "A round racket has a circular head and weight shifted towards the handle.",
      "Una pala redonda tiene la cabeza circular y el peso desplazado hacia el mango."),
     ("È la forma del controllo: sweet spot centrato e ampio, grande maneggevolezza e facilità in difesa. È la forma consigliata a chi inizia e a chi costruisce il punto con pazienza.",
      "It is the control shape: a central, large sweet spot, great maneuverability and ease in defence. It is the shape recommended for beginners and for players who build the point patiently.",
      "Es la forma del control: punto dulce centrado y amplio, gran manejabilidad y facilidad en defensa. Es la forma recomendada para quien empieza y para quien construye el punto con paciencia."),
     ("guide", "racchette-padel-controllo")),
    ("racchetta-goccia", ("Racchetta a goccia", "Teardrop racket", "Pala de lágrima"),
     ("Una racchetta a goccia ha una forma intermedia tra rotonda e diamante, con il peso leggermente verso la testa.",
      "A teardrop racket has a shape between round and diamond, with the weight slightly towards the head.",
      "Una pala de lágrima tiene una forma intermedia entre redonda y diamante, con el peso ligeramente hacia la cabeza."),
     ("È la forma più versatile: un compromesso tra controllo e potenza adatto alla maggior parte dei giocatori, dagli intermedi agli avanzati.",
      "It is the most versatile shape: a compromise between control and power that suits most players, from intermediate to advanced.",
      "Es la forma más versátil: un compromiso entre control y potencia adecuado para la mayoría de jugadores, de intermedios a avanzados."),
     ("guide", "forme-racchetta-padel")),
    ("superficie-ruvida", ("Superficie ruvida", "Rough face", "Superficie rugosa"),
     ("Una superficie ruvida (sabbiata o con rilievi 3D) aumenta l'attrito tra racchetta e palla.",
      "A rough face (sanded or with 3D relief) increases friction between racket and ball.",
      "Una superficie rugosa (arenada o con relieves 3D) aumenta la fricción entre pala y bola."),
     ("Serve a dare più effetto ai colpi, come i tagli e le víbora. Con l'uso la ruvidità tende a consumarsi. Molti modelli di fascia alta hanno superfici ruvide, i modelli d'ingresso spesso lisce.",
      "It is used to put more spin on shots, such as slices and víboras. With use the roughness tends to wear off. Many high-end models have rough faces, entry models often smooth ones.",
      "Sirve para dar más efecto a los golpes, como los cortados y las víboras. Con el uso la rugosidad tiende a desgastarse. Muchos modelos de gama alta tienen superficies rugosas, los de iniciación a menudo lisas."),
     ("racchette", None)),
    ("misure-regolamentari", ("Misure regolamentari", "Official dimensions", "Medidas reglamentarias"),
     ("Il regolamento della Federazione Internazionale Padel fissa i limiti della racchetta: lunghezza massima 45,5 cm, larghezza massima 26 cm e spessore massimo 38 mm.",
      "The International Padel Federation rules set the racket limits: maximum length 45.5 cm, maximum width 26 cm and maximum thickness 38 mm.",
      "El reglamento de la Federación Internacional de Pádel fija los límites de la pala: longitud máxima 45,5 cm, anchura máxima 26 cm y grosor máximo 38 mm."),
     ("Per questo quasi tutte le racchette da adulto hanno lo stesso spessore di 38 mm; le racchette junior sono più corte e leggere. Il peso non ha un limite regolamentare: le racchette da adulto pesano in genere tra 340 e 375 grammi.",
      "That is why almost all adult rackets have the same 38 mm thickness; junior rackets are shorter and lighter. Weight has no regulatory limit: adult rackets generally weigh between 340 and 375 grams.",
      "Por eso casi todas las palas de adulto tienen el mismo grosor de 38 mm; las palas junior son más cortas y ligeras. El peso no tiene límite reglamentario: las palas de adulto pesan en general entre 340 y 375 gramos."),
     ("bambini", None)),
]


def _g(t):
    return t[S.LINGUE.index(S.lang())]


def glossario():
    G = L("Glossario", "Glossary", "Glosario")
    for slug, nome, defin, testo, link in GLOSSARIO:
        nome, defin, testo = _g(nome), _g(defin), _g(testo)
        path, alt = P("glossario", slug), ALT("glossario", slug)
        cr, ld = crumbs([H(), (G, P("glossario")), (nome, None)])
        term = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": nome, "description": defin,
                "inDefinedTermSet": SITO + P("glossario"), "url": SITO + path}
        altri = "".join(f'<li><a href="{P("glossario", s)}">{e(_g(n))}</a></li>' for s, n, *_ in GLOSSARIO if s != slug)
        h1 = L(f"{e(nome)}: cos'è nel padel", f"{e(nome)}: what it means in padel", f"{e(nome)}: qué es en el pádel")
        corpo = f'''{cr}
<div class="intro"><h1>{h1}</h1><p><b>{e(defin)}</b></p><p>{e(testo)}</p>{data_riga()}</div>
<div class="prose"><p><a href="{P(*link)}">{L("Approfondisci", "Learn more", "Saber más")}</a></p><h2>{L("Altri termini", "Other terms", "Otros términos")}</h2><ul class="lista-link">{altri}</ul></div>'''
        scrivi(path, pagina(L(f"{nome}: cos'è e cosa significa nel padel | PadelMetrix", f"{nome}: what it is and what it means in padel | PadelMetrix",
                              f"{nome}: qué es y qué significa en el pádel | PadelMetrix"), defin[:160], path, corpo, on="guide", ld=[ld, term], alt=alt), alt)
    cr, ld = crumbs([H(), (G, None)])
    voci = "".join(f'<li><a href="{P("glossario", s)}"><b>{e(_g(n))}</b></a>: {e(_g(d))}</li>' for s, n, d, *_ in GLOSSARIO)
    t_g = L("Glossario delle racchette da padel", "Padel racket glossary", "Glosario de las palas de pádel")
    corpo = f'''{cr}<div class="intro"><h1>{t_g}</h1><p>{L("I termini tecnici che trovi nelle schede, spiegati in breve.", "The technical terms you will find on the racket pages, briefly explained.", "Los términos técnicos que encontrarás en las fichas, explicados en breve.")}</p>{data_riga()}</div><div class="prose"><ul>{voci}</ul></div>'''
    sett = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": t_g, "url": SITO + P("glossario")}
    path, alt = P("glossario"), ALT("glossario")
    scrivi(path, pagina(L("Glossario delle racchette da padel: bilanciamento, EVA, carbonio e altri termini | PadelMetrix", "Padel racket glossary: balance, EVA, carbon and other terms | PadelMetrix",
                          "Glosario de palas de pádel: balance, EVA, carbono y otros términos | PadelMetrix"),
                        L("Cosa significano bilanciamento, swingweight, sweet spot, EVA, foam, carbonio 12K e le forme delle racchette da padel.",
                          "What balance, swingweight, sweet spot, EVA, foam, 12K carbon and the padel racket shapes mean.",
                          "Qué significan balance, swingweight, punto dulce, EVA, foam, carbono 12K y las formas de las palas de pádel."),
                        path, corpo, on="guide", ld=[ld, sett], alt=alt), alt)


# ------------------------------------------------------------------ pagine risposta

def faq_ld(q, a):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}]}


def domande(db, stats):
    s, med_peso, min_p, max_p, med_prezzo, forma_top, liv_rows = stats
    D = L("Domande", "Questions", "Preguntas")
    voci = []
    gioc = {}
    for n in db:
        g = n["giocatore"]
        if g and "ispirata" not in g:
            gioc.setdefault(g, []).append(n)
    for g, its in sorted(gioc.items()):
        its = ordina(its)
        top = its[0]
        slug = "racchetta-" + slugify(g)
        path, alt = P("domande", slug), ALT("domande", slug)
        q = L(f"Con che racchetta gioca {g}?", f"What racket does {g} use?", f"¿Con qué pala juega {g}?")
        anno = top["anno"]
        ult = [x for x in its if x["anno"] == anno]
        marche_g = sorted({x["marca"] for x in ult})
        nomi = [x["nome"].replace(f" {anno}", "") for x in ult]
        resto = len(nomi) - 4
        elenco = ", ".join(nomi[:4]) + (L(f" e altre {resto}", f" and {resto} more", f" y {resto} más") if resto > 0 else "")
        if len(ult) == 1:
            dett = ", ".join(x for x in (L(f"forma {FORMA(top['forma']).lower()}", f"{FORMA(top['forma']).lower()} shape", f"forma {FORMA(top['forma']).lower()}") if top["forma"] else None, top["peso"]) if x)
            ans = L(f"Nella collezione {anno} {g} firma la {top['titolo']}", f"In the {anno} collection {g} signs the {top['titolo']}", f"En la colección {anno} {g} firma la {top['titolo']}") + (f" ({dett})" if dett else "") + "."
        else:
            mg = L(" e ", " and ", " y ").join(marche_g)
            ans = L(f"Nella collezione {anno} {g} firma {len(ult)} racchette {mg}: {elenco}.", f"In the {anno} collection {g} signs {len(ult)} {mg} rackets: {elenco}.",
                    f"En la colección {anno} {g} firma {len(ult)} palas {mg}: {elenco}.")
        if len(its) > len(ult):
            ans += L(f" In tutto il database PadelMetrix conta {len(its)} modelli firmati tra 2026 e 2027, elencati sotto.",
                     f" In total the PadelMetrix database lists {len(its)} signature models across 2026 and 2027, shown below.",
                     f" En total la base de datos PadelMetrix recoge {len(its)} modelos firmados entre 2026 y 2027, listados abajo.")
        nota = L("I professionisti possono usare versioni personalizzate del modello in vendita.", "Professionals may use customised versions of the model on sale.",
                 "Los profesionales pueden usar versiones personalizadas del modelo a la venta.")
        cr, ld = crumbs([H(), (D, P("domande")), (g, None)])
        pro = P("guide", "racchette-giocatori-professionisti")
        corpo = f'''{cr}
<div class="intro"><h1>{e(q)}</h1><p><b>{e(ans)}</b> {e(nota)}</p>{data_riga()}</div>
{griglia(its)}
<div class="prose"><p>{L(f'Tutti i giocatori nella pagina <a href="{pro}">racchette dei professionisti</a>.', f'All players on the <a href="{pro}">pro players\' rackets</a> page.', f'Todos los jugadores en la página <a href="{pro}">palas de los profesionales</a>.')}</p></div>'''
        scrivi(path, pagina(L(f"Con che racchetta gioca {g}? Modelli 2026 e 2027 | PadelMetrix", f"What racket does {g} use? 2026 and 2027 models | PadelMetrix",
                              f"¿Con qué pala juega {g}? Modelos 2026 y 2027 | PadelMetrix"), ans[:300], path, corpo, on="guide", ld=[ld, faq_ld(q, ans + " " + nota)], alt=alt), alt)
        voci.append((path, q))

    # risposte calcolate dal database
    adulti = [n for n in db if n["categoria"] != "junior"]
    q1 = L("Quanto pesa una racchetta da padel?", "How much does a padel racket weigh?", "¿Cuánto pesa una pala de pádel?")
    a1 = L(f"Una racchetta da padel per adulti pesa in genere tra 340 e 375 grammi: nel database PadelMetrix il peso tipico (mediana) è {med_peso} g, su {len(s['pesi'])} modelli 2026 e 2027 con peso dichiarato. Le racchette junior pesano meno, di solito tra 280 e 340 g.",
           f"An adult padel racket usually weighs between 340 and 375 grams: in the PadelMetrix database the typical (median) weight is {med_peso} g, across {len(s['pesi'])} 2026 and 2027 models with a declared weight. Junior rackets weigh less, usually between 280 and 340 g.",
           f"Una pala de pádel para adultos pesa en general entre 340 y 375 gramos: en la base de datos PadelMetrix el peso típico (mediana) es {med_peso} g, sobre {len(s['pesi'])} modelos 2026 y 2027 con peso declarado. Las palas junior pesan menos, normalmente entre 280 y 340 g.")
    leggere = sorted([n for n in adulti if n["peso_min"]], key=lambda n: n["peso_min"])[:12]
    q2 = L("Quanto costa una racchetta da padel?", "How much does a padel racket cost?", "¿Cuánto cuesta una pala de pádel?")
    righe_l = "".join(f"<tr><td>{e(lv)}</td><td>{eur(p)}</td><td>{c}</td></tr>" for lv, p, c in liv_rows)
    a2 = L(f"Il prezzo di listino mediano di una racchetta da padel 2026–2027 è {eur(med_prezzo)} nel database PadelMetrix; si va da meno di 100 € per i modelli d'ingresso a oltre 350 € per quelli dei professionisti. Online i prezzi reali sono spesso più bassi del listino.",
           f"The median list price of a 2026–2027 padel racket is {eur(med_prezzo)} in the PadelMetrix database; it ranges from under €100 for entry models to over €350 for pro models. Online, actual prices are often lower than the list price.",
           f"El precio de lista mediano de una pala de pádel 2026–2027 es {eur(med_prezzo)} en la base de datos PadelMetrix; va de menos de 100 € en los modelos de iniciación a más de 350 € en los de los profesionales. Online los precios reales suelen ser más bajos que el de lista.")
    q3 = L("Qual è la forma di racchetta da padel più diffusa?", "What is the most common padel racket shape?", "¿Cuál es la forma de pala de pádel más común?")
    ft = FORMA(forma_top).lower()
    resto = ", ".join(f"{FORMA(f).lower()} {pct(c, s['con_forma'])}%" for f, c in sorted(s["forme"].items(), key=lambda kv: -kv[1]) if f != forma_top and c)
    pf = pct(s['forme'][forma_top], s['con_forma'])
    a3 = L(f"La forma più diffusa è la {ft}: {pf}% dei {s['con_forma']} modelli per adulti con forma dichiarata nel database PadelMetrix. {resto}.",
           f"The most common shape is {ft}: {pf}% of the {s['con_forma']} adult models with a declared shape in the PadelMetrix database. {resto[0].upper() + resto[1:]}.",
           f"La forma más común es la {ft}: {pf}% de los {s['con_forma']} modelos para adultos con forma declarada en la base de datos PadelMetrix. {resto[0].upper() + resto[1:]}.")
    if S.lang() == "it":
        a3 = a3.replace(f"PadelMetrix. {resto}", f"PadelMetrix. {resto[0].upper() + resto[1:]}")
    eco, forme_g = P("guide", "racchette-padel-economiche"), P("guide", "forme-racchetta-padel")
    extra = [
        ("quanto-pesa-una-racchetta-da-padel", q1, a1, f'<h2>{L("Le racchette per adulti più leggere nel database", "The lightest adult rackets in the database", "Las palas de adulto más ligeras de la base de datos")}</h2>{griglia(leggere)}'),
        ("quanto-costa-una-racchetta-da-padel", q2, a2, f'<h2>{L("Prezzo di listino mediano per livello", "Median list price by level", "Precio de lista mediano por nivel")}</h2><table class="tab"><thead><tr><th>{L("Livello", "Level", "Nivel")}</th><th>{L("Mediana", "Median", "Mediana")}</th><th>{L("Modelli", "Models", "Modelos")}</th></tr></thead><tbody>{righe_l}</tbody></table><p><a href="{eco}">{L("Racchette economiche fino a 130 €", "Cheap rackets up to €130", "Palas baratas hasta 130 €")}</a></p>'),
        ("forma-racchetta-padel-piu-diffusa", q3, a3, L(f'<p>Le differenze tra le forme sono spiegate nella <a href="{forme_g}">guida alle forme</a>.</p>', f'<p>The differences between shapes are explained in the <a href="{forme_g}">shapes guide</a>.</p>', f'<p>Las diferencias entre formas se explican en la <a href="{forme_g}">guía de las formas</a>.</p>')),
    ]
    rep = P("report", REPORT)
    for slug, q, a, html_extra in extra:
        path, alt = P("domande", slug), ALT("domande", slug)
        cr, ld = crumbs([H(), (D, P("domande")), (q, None)])
        corpo = f'''{cr}<div class="intro"><h1>{e(q)}</h1><p><b>{e(a)}</b></p>{data_riga()}</div>
<div class="prose">{html_extra}<p class="note">{L(f'Calcolato sul database PadelMetrix; metodo e limiti nel <a href="{rep}">report in numeri</a>.', f'Calculated on the PadelMetrix database; method and limitations in the <a href="{rep}">report in numbers</a>.', f'Calculado sobre la base de datos PadelMetrix; método y limitaciones en el <a href="{rep}">informe en cifras</a>.')}</p></div>'''
        scrivi(path, pagina(L(f"{q} Dati 2026–2027 | PadelMetrix", f"{q} 2026–2027 data | PadelMetrix", f"{q} Datos 2026–2027 | PadelMetrix"), a[:300], path, corpo, on="guide", ld=[ld, faq_ld(q, a)], alt=alt), alt)
        voci.insert(0, (path, q))

    cr, ld = crumbs([H(), (D, None)])
    corpo = f'''{cr}<div class="intro"><h1>{L("Domande frequenti sulle racchette da padel", "Frequently asked questions about padel rackets", "Preguntas frecuentes sobre las palas de pádel")}</h1><p>{L("Risposte brevi, con i dati del database PadelMetrix.", "Short answers, with data from the PadelMetrix database.", "Respuestas breves, con los datos de la base de datos PadelMetrix.")}</p>{data_riga()}</div>
<div class="prose"><ul class="lista-link">{"".join(f'<li><a href="{p}">{e(q)}</a></li>' for p, q in voci)}</ul></div>'''
    path, alt = P("domande"), ALT("domande")
    scrivi(path, pagina(L("Domande frequenti sulle racchette da padel | PadelMetrix", "Padel racket FAQ | PadelMetrix", "Preguntas frecuentes sobre palas de pádel | PadelMetrix"),
                        L("Quanto pesa e quanto costa una racchetta da padel, che forma scegliere, con che racchetta giocano i professionisti: risposte con i dati.",
                          "How much a padel racket weighs and costs, which shape to choose, which rackets the pros use: answers backed by data.",
                          "Cuánto pesa y cuánto cuesta una pala de pádel, qué forma elegir, con qué pala juegan los profesionales: respuestas con datos."),
                        path, corpo, on="guide", ld=[ld], alt=alt), alt)


# ------------------------------------------------------------------ llms.txt

def llms(db):
    s = statistiche(db)
    righe = []
    for l, nome in (("it", "Italiano"), ("en", "English"), ("es", "Español")):
        set_lang(l)
        righe.append(f"""

## {nome}
- [{L("Racchette", "Rackets", "Palas")}]({SITO}{P("racchette")}): {L("tutte le schede con filtri per marca, forma, livello, stile e prezzo", "all racket pages with filters by brand, shape, level, style and price", "todas las fichas con filtros por marca, forma, nivel, estilo y precio")}
- [{L("Marche", "Brands", "Marcas")}]({SITO}{P("marche")}): {L("i modelli di ogni marca", "each brand's models", "los modelos de cada marca")}
- [{L("Confronti", "Comparisons", "Comparativas")}]({SITO}{P("confronta")}): {L("confronti modello contro modello", "model-versus-model comparisons", "comparativas modelo contra modelo")}
- [{L("Guide", "Guides", "Guías")}]({SITO}{P("guide")}): {L("come scegliere la racchetta per livello, problema fisico, budget", "how to choose a racket by level, physical issue, budget", "cómo elegir la pala según nivel, problema físico, presupuesto")}
- [{L("Bambini", "Kids", "Niños")}]({SITO}{P("bambini")}): {L("misure per età e racchette junior", "sizes by age and junior rackets", "medidas por edad y palas junior")}
- [{L("Domande frequenti", "FAQ", "Preguntas frecuentes")}]({SITO}{P("domande")}): {L("risposte brevi con dati", "short answers with data", "respuestas breves con datos")}
- [{L("Glossario", "Glossary", "Glosario")}]({SITO}{P("glossario")}): {L("termini tecnici", "technical terms", "términos técnicos")}
- [Pickleball]({SITO}{P("pickleball")}): {L("schede delle racchette da pickleball HEAD, JOOLA e VICLION", "HEAD, JOOLA and VICLION pickleball paddle pages", "fichas de las palas de pickleball HEAD, JOOLA y VICLION")}
- [{L("Report Racchette da padel 2026–2027 in numeri", "Report: Padel rackets 2026–2027 in numbers", "Informe Palas de pádel 2026–2027 en cifras")}]({SITO}{P("report", REPORT)})
- [{L("Dataset aperto CSV/JSON, licenza CC BY 4.0", "Open dataset CSV/JSON, CC BY 4.0 licence", "Dataset abierto CSV/JSON, licencia CC BY 4.0")}]({SITO}{P("dati")})
- [{L("Chi siamo e metodo", "About and method", "Quiénes somos y método")}]({SITO}{P("chi-siamo")}): {L("fonti dei dati, indipendenza, aggiornamenti", "data sources, independence, updates", "fuentes de los datos, independencia, actualizaciones")}""")
    set_lang("it")
    txt = f"""# PadelMetrix

> Independent padel racket database / Database indipendente di racchette da padel / Base de datos independiente de palas de pádel: {s['n']} racket pages from the 2026 and 2027 collections of {len(s['marche'])} brands, with specs, cited sources, comparisons and guides. Available in Italian, English and Spanish. Updated {OGGI}.
{"".join(righe)}
"""
    (ROOT / "llms.txt").write_text(txt, encoding="utf-8")


def main():
    db = carica()
    nr = file_dataset(db)
    for l in LINGUE:
        set_lang(l)
        chi_siamo(db)
        stats = report(db)
        dataset(nr)
        glossario()
        domande(db, stats)
    set_lang("it")
    llms(db)
    (ROOT / "scripts" / "pagine_geo.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine GEO generate")


if __name__ == "__main__":
    main()
