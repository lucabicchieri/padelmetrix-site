#!/usr/bin/env python3
"""Contenuti GEO: pagina metodo, report in numeri, dataset aperto, glossario, pagine risposta, llms.txt.
Tutti i numeri sono calcolati dal database delle schede; nessun dato inventato."""
import csv
import io
import json
import pathlib
import statistics
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sito import ROOT, SITO, e, carica, crumbs, pagina, griglia, ordina, FORMA_IT, LIV_IT, STILE_IT, slugify  # noqa: E402

OGGI = "2026-10-24"
OGGI_TXT = "24 ottobre 2026"
AUTORE = {"@type": "Person", "name": "Luca Bicchieri", "url": f"{SITO}/it/chi-siamo/"}
EDITORE = {"@type": "Organization", "name": "PadelMetrix", "url": f"{SITO}/it/"}
PAGINE = []


def scrivi(path, txt):
    dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(txt, encoding="utf-8")
    PAGINE.append(path)


def euro(x):
    return f"{x:,.0f}".replace(",", ".") + " €"


def meta_art(titolo, desc, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titolo, "description": desc,
            "author": AUTORE, "publisher": EDITORE, "datePublished": OGGI, "dateModified": OGGI, "inLanguage": "it",
            "mainEntityOfPage": SITO + path}


def data_riga():
    return f'<p class="note">Aggiornato il {OGGI_TXT} · a cura di <a href="/it/chi-siamo/">Luca Bicchieri, PadelMetrix</a></p>'


def pct(a, b):
    return round(100 * a / b) if b else 0


def barre(rows, unit="%"):
    mx = max(v for _, v in rows) or 1
    return '<div class="bars" style="max-width:640px">' + "".join(
        f'<div class="bar"><span>{e(k)}</span><div class="track"><div class="fill" style="width:{round(v / mx * 100)}%"></div></div><span class="v">{v}{unit}</span></div>'
        for k, v in rows) + "</div>"


# ------------------------------------------------------------------ statistiche dal database

def statistiche(db):
    adulti = [n for n in db if n["categoria"] != "junior"]
    pesi = []
    for n in adulti:
        import re
        v = [int(x) for x in re.findall(r"\d{3}", n["peso"] or "")]
        if len(v) >= 2:
            pesi.append((v[0] + v[1]) / 2)
        elif len(v) == 1:
            pesi.append(v[0])
    forme = {f: sum(1 for n in adulti if n["forma"] == f) for f in FORMA_IT}
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
    import re
    ks = {}
    for s in sup:
        m = re.search(r"(\d+)k", s)
        if m:
            ks[m.group(1) + "K"] = ks.get(m.group(1) + "K", 0) + 1
    stili = {s: sum(1 for n in adulti if n["stile"] == s) for s in STILE_IT}
    return dict(n=len(db), adulti=len(adulti), junior=len(db) - len(adulti), anni={a: sum(1 for n in db if n["anno"] == a) for a in sorted({n["anno"] for n in db})},
                pesi=pesi, forme=forme, con_forma=con_forma, prezzi=prezzi, per_liv=per_liv, marche=marche,
                sup=len(sup), carbonio=carbonio, vetro=vetro, ks=ks, stili=stili)


# ------------------------------------------------------------------ chi siamo e metodo

def chi_siamo(db):
    s = statistiche(db)
    cr, ld = crumbs([("Home", "/it/"), ("Chi siamo e metodo", None)])
    corpo = f'''{cr}
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
<p>Il database si aggiorna quando escono nuove collezioni e quando cambiano prezzi o arrivano nuove recensioni. Ogni pagina mostra la data dell'ultimo aggiornamento. I dati sono disponibili anche come <a href="/it/dati/">dataset aperto</a>.</p>
<h2>Citare PadelMetrix</h2>
<p>Puoi riprendere dati e statistiche citando la fonte: «Fonte: PadelMetrix (padelmetrix.com), {OGGI_TXT}».</p>
</div>'''
    about = {"@context": "https://schema.org", "@type": "AboutPage", "name": "Chi siamo e metodo", "dateModified": OGGI,
             "publisher": EDITORE, "author": AUTORE}
    scrivi("/it/chi-siamo/", pagina("Chi siamo e metodo: come PadelMetrix raccoglie i dati sulle racchette | PadelMetrix",
                                    "Chi cura PadelMetrix, da dove vengono i dati sulle racchette da padel, come trattiamo punteggi e recensioni e come guadagniamo.",
                                    "/it/chi-siamo/", corpo, ld=[ld, about]))


# ------------------------------------------------------------------ report in numeri

def report(db):
    s = statistiche(db)
    med_peso = round(statistics.median(s["pesi"]))
    min_p, max_p = round(min(s["pesi"])), round(max(s["pesi"]))
    med_prezzo = statistics.median(s["prezzi"])
    forma_top = max(s["forme"], key=lambda f: s["forme"][f])
    forme_rows = [(FORMA_IT[f], pct(c, s["con_forma"])) for f, c in sorted(s["forme"].items(), key=lambda kv: -kv[1]) if c]
    liv_rows = []
    for l in ("principiante", "principiante-intermedio", "intermedio", "intermedio-avanzato", "avanzato", "professionale"):
        if l in s["per_liv"] and len(s["per_liv"][l]) >= 3:
            liv_rows.append((LIV_IT[l], round(statistics.median(s["per_liv"][l])), len(s["per_liv"][l])))
    marche_rows = sorted(s["marche"].items(), key=lambda kv: -kv[1])
    k_rows = sorted(s["ks"].items(), key=lambda kv: -kv[1])[:5]
    stili_tot = sum(s["stili"].values())
    path = "/it/report/racchette-padel-2026-2027-in-numeri/"
    titolo = "Racchette da padel 2026–2027 in numeri"
    intro = (f"Secondo il database PadelMetrix ({s['n']} racchette delle collezioni 2026 e 2027), la racchetta da padel tipica per adulti pesa circa {med_peso} g, "
             f"ha forma {FORMA_IT[forma_top].lower()} ({pct(s['forme'][forma_top], s['con_forma'])}% dei modelli con forma dichiarata) "
             f"e costa {euro(med_prezzo)} di listino (valore mediano).")
    cr, ld = crumbs([("Home", "/it/"), ("Report", None), (titolo, None)])
    corpo = f'''{cr}
<div class="intro"><h1>{titolo}</h1><p>{e(intro)}</p>{data_riga()}</div>
<div class="prose">
<h2>Le cifre principali</h2>
<table class="tab"><tbody>
<tr><td>Racchette analizzate</td><td><b>{s["n"]}</b> ({", ".join(f"{c} del {a}" for a, c in s["anni"].items())})</td></tr>
<tr><td>Marche</td><td><b>{len(s["marche"])}</b></td></tr>
<tr><td>Modelli junior</td><td><b>{s["junior"]}</b></td></tr>
<tr><td>Peso tipico (adulti, mediana)</td><td><b>{med_peso} g</b>, da {min_p} a {max_p} g su {len(s["pesi"])} modelli con peso dichiarato</td></tr>
<tr><td>Prezzo di listino (mediana)</td><td><b>{euro(med_prezzo)}</b> su {len(s["prezzi"])} modelli con prezzo rilevato</td></tr>
<tr><td>Superficie in carbonio</td><td><b>{pct(s["carbonio"], s["sup"])}%</b> dei modelli con superficie dichiarata; fibra di vetro {pct(s["vetro"], s["sup"])}%</td></tr>
</tbody></table>
<h2>Che forma hanno le racchette</h2>
<p>La forma {FORMA_IT[forma_top].lower()} è la più diffusa. Quota sui {s["con_forma"]} modelli per adulti con forma dichiarata:</p>
{barre(forme_rows)}
<h2>Attacco, controllo o polivalenti</h2>
<p>Stile di gioco indicato da produttori e rivenditori, su {stili_tot} modelli per adulti:</p>
{barre([(STILE_IT[k], pct(v, stili_tot)) for k, v in sorted(s["stili"].items(), key=lambda kv: -kv[1]) if v])}
<h2>Quanto costano, per livello</h2>
<table class="tab"><thead><tr><th>Livello</th><th>Prezzo di listino mediano</th><th>Modelli</th></tr></thead><tbody>
{"".join(f"<tr><td>{e(l)}</td><td>{euro(p)}</td><td>{c}</td></tr>" for l, p, c in liv_rows)}
</tbody></table>
<h2>Il carbonio più usato</h2>
<p>Tipi di carbonio dichiarati più frequenti nelle superfici (numero di modelli):</p>
{barre(k_rows, unit="")}
<h2>Modelli per marca</h2>
<table class="tab"><thead><tr><th>Marca</th><th>Racchette nel database</th></tr></thead><tbody>
{"".join(f'<tr><td><a href="/it/marche/{slugify(m)}/">{e(m)}</a></td><td>{c}</td></tr>' for m, c in marche_rows)}
</tbody></table>
<h2>Metodo e limiti</h2>
<p>I numeri sono calcolati sulle schede del database PadelMetrix, che copre le collezioni 2026 e 2027 delle marche principali ma non tutto il mercato. Peso e prezzo sono quelli dichiarati da produttori e rivenditori; per il peso usiamo il punto medio dell'intervallo dichiarato. Il numero di modelli per marca riflette la copertura del database, non le quote di mercato. I dati completi sono nel <a href="/it/dati/">dataset aperto</a>.</p>
<p>Citazione suggerita: «PadelMetrix, Racchette da padel 2026–2027 in numeri, {OGGI_TXT}, padelmetrix.com».</p>
</div>'''
    desc = intro[:300]
    scrivi(path, pagina(f"{titolo}: peso, forme, prezzi e materiali | PadelMetrix", desc, path, corpo, ld=[ld, meta_art(titolo, desc, path)]))
    return s, med_peso, min_p, max_p, med_prezzo, forma_top, liv_rows


# ------------------------------------------------------------------ dataset aperto

CAMPI = ["slug", "marca", "modello", "anno", "giocatore", "categoria", "forma", "peso", "bilanciamento", "nucleo", "superficie",
         "telaio", "tatto", "livello", "stile", "prezzo_listino_eur", "url", "fonti"]


def dataset(db):
    righe = []
    for n in ordina(db):
        d = n["d"]
        righe.append({"slug": n["slug"], "marca": n["marca"], "modello": n["modello"], "anno": n["anno"], "giocatore": n["giocatore"] or "",
                      "categoria": n["categoria"], "forma": n["forma"] or "", "peso": n["peso"] or "",
                      "bilanciamento": d.get("bilanciamento") if isinstance(d.get("bilanciamento"), str) else "",
                      "nucleo": n["nucleo"] if isinstance(n["nucleo"], str) else "", "superficie": n["superficie"] or "",
                      "telaio": d.get("telaio") if isinstance(d.get("telaio"), str) else "",
                      "tatto": n["sensazione"] if isinstance(n["sensazione"], str) else "", "livello": n["livello"] or "",
                      "stile": n["stile"] or "", "prezzo_listino_eur": n["prezzo"] or "", "url": SITO + n["url"],
                      "fonti": " | ".join(d.get("fonti_dati", []))})
    out = ROOT / "dati"
    out.mkdir(exist_ok=True)
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=CAMPI)
    w.writeheader()
    w.writerows(righe)
    (out / "racchette-padelmetrix.csv").write_text(buf.getvalue(), encoding="utf-8")
    (out / "racchette-padelmetrix.json").write_text(json.dumps({"fonte": "PadelMetrix (padelmetrix.com)", "licenza": "CC BY 4.0", "aggiornato": OGGI, "racchette": righe}, ensure_ascii=False, indent=1), encoding="utf-8")
    ds = {"@context": "https://schema.org", "@type": "Dataset", "name": "Racchette da padel 2026–2027 — PadelMetrix",
          "description": f"Dati tecnici di {len(righe)} racchette da padel delle collezioni 2026 e 2027: marca, modello, forma, peso, bilanciamento, materiali, livello, stile, prezzo di listino e fonti.",
          "url": SITO + "/it/dati/", "license": "https://creativecommons.org/licenses/by/4.0/", "creator": EDITORE, "dateModified": OGGI,
          "inLanguage": "it", "keywords": ["padel", "racchette da padel", "pale da padel", "padel rackets"],
          "distribution": [{"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": SITO + "/dati/racchette-padelmetrix.csv"},
                           {"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": SITO + "/dati/racchette-padelmetrix.json"}]}
    cr, ld = crumbs([("Home", "/it/"), ("Dati aperti", None)])
    corpo = f'''{cr}
<div class="intro"><h1>Dataset aperto delle racchette da padel</h1><p>Il database PadelMetrix è scaricabile gratis: {len(righe)} racchette delle collezioni 2026 e 2027 con marca, modello, forma, peso, bilanciamento, materiali, livello, stile, prezzo di listino e le fonti di ogni scheda. Licenza CC BY 4.0: puoi usarlo citando PadelMetrix.</p>{data_riga()}</div>
<div class="prose">
<p><a class="btn" href="/dati/racchette-padelmetrix.csv" download>Scarica CSV</a> &nbsp; <a class="btn out" href="/dati/racchette-padelmetrix.json" download>Scarica JSON</a></p>
<h2>Campi</h2><p>{", ".join(f"<code>{c}</code>" for c in CAMPI)}. I campi vuoti indicano dati non dichiarati dalle fonti.</p>
<h2>Licenza e citazione</h2><p>Dati rilasciati con licenza <a href="https://creativecommons.org/licenses/by/4.0/deed.it" rel="noopener" target="_blank">Creative Commons Attribuzione 4.0</a>. Citazione: «Fonte: PadelMetrix (padelmetrix.com), {OGGI_TXT}». I punteggi di siti terzi non sono inclusi: restano di proprietà delle rispettive fonti.</p>
<p>Le statistiche principali sono nel report <a href="/it/report/racchette-padel-2026-2027-in-numeri/">Racchette da padel 2026–2027 in numeri</a>.</p>
</div>'''
    scrivi("/it/dati/", pagina("Dataset aperto racchette da padel 2026–2027 (CSV e JSON) | PadelMetrix",
                               f"Scarica gratis i dati tecnici di {len(righe)} racchette da padel 2026 e 2027 in CSV e JSON, con licenza CC BY 4.0.",
                               "/it/dati/", corpo, ld=[ld, ds]))


# ------------------------------------------------------------------ glossario

GLOSSARIO = [
    ("bilanciamento", "Bilanciamento", "Il bilanciamento è la distanza del baricentro della racchetta dal fondo del manico, espressa in millimetri o centimetri.",
     "Più è alta, più il peso è spostato verso la testa: la racchetta dà più potenza nello smash ma è meno maneggevole e affatica di più il braccio. Un bilanciamento basso sposta il peso verso il manico e favorisce controllo e velocità di reazione. Per esempio, tra i modelli del database 255 mm è considerato basso e 270 mm alto.",
     "/it/guide/forme-racchetta-padel/"),
    ("swingweight", "Swingweight", "Lo swingweight misura quanto la racchetta \"pesa\" mentre la si muove, cioè la sua inerzia attorno al punto di impugnatura.",
     "Due racchette con lo stesso peso possono avere swingweight diversi se il peso è distribuito diversamente. Uno swingweight alto dà stabilità e potenza ma rende la racchetta più lenta da muovere; uno basso la rende più rapida a rete. Pochi produttori lo dichiarano: alcuni negozi lo misurano, e in quel caso lo riportiamo nelle schede.",
     "/it/racchette/"),
    ("sweet-spot", "Sweet spot", "Lo sweet spot è la zona della superficie in cui l'impatto con la palla dà la risposta migliore: più controllo, meno vibrazioni e uscita di palla più pulita.",
     "Nelle racchette rotonde è al centro e più ampio; nelle racchette a diamante è più in alto e più piccolo. Uno sweet spot ampio perdona di più i colpi decentrati ed è utile a chi inizia.",
     "/it/guide/racchetta-padel-principianti/"),
    ("eva", "Gomma EVA", "L'EVA (etilene vinil acetato) è la gomma più usata per il nucleo delle racchette da padel.",
     "Esiste in diverse densità: l'EVA morbida (soft) assorbe le vibrazioni e aiuta l'uscita di palla con poco sforzo; l'EVA dura (hard) restituisce più potenza ai colpi forti ma chiede più forza e tecnica. Molti marchi usano nuclei a più strati con densità diverse.",
     "/it/guide/racchetta-padel-epicondilite/"),
    ("foam", "Foam", "Il foam è una schiuma usata come nucleo in alternativa all'EVA, in genere più morbida e più elastica.",
     "Dà una sensazione più soffice e una buona uscita di palla anche a ritmo basso, a scapito di un po' di precisione nei colpi violenti. Head, per esempio, usa nuclei Power Foam e Control Foam.",
     "/it/marche/head/"),
    ("carbonio-3k-12k-18k", "Carbonio 3K, 12K, 18K", "La sigla K indica quante migliaia di filamenti compongono ogni fascio di fibra di carbonio usato nella superficie: 3K vuol dire 3.000 filamenti.",
     "Il numero cambia la trama del tessuto e la sensazione al tatto, ma da solo non dice se una racchetta è più rigida o più potente: contano anche resina, numero di strati e nucleo. In generale le superfici in carbonio sono più rigide e precise di quelle in fibra di vetro.",
     "/it/report/racchette-padel-2026-2027-in-numeri/"),
    ("fibra-di-vetro", "Fibra di vetro", "La fibra di vetro è un materiale per superfici e telai più flessibile ed economico del carbonio.",
     "Una superficie in fibra di vetro si deforma di più all'impatto: tatto morbido, uscita di palla facile e più comfort, a scapito di precisione e durata. È il materiale tipico delle racchette per principianti e di molte racchette junior.",
     "/it/guide/racchette-padel-economiche/"),
    ("racchetta-diamante", "Racchetta a diamante", "Una racchetta a diamante ha la testa più larga in alto e il peso spostato verso la punta.",
     "È la forma della potenza: aiuta negli smash e nelle volée d'attacco, ma ha uno sweet spot più alto e piccolo ed è meno tollerante in difesa. È adatta a giocatori con buona tecnica che giocano spesso a rete.",
     "/it/guide/racchette-padel-potenza/"),
    ("racchetta-rotonda", "Racchetta rotonda", "Una racchetta rotonda ha la testa circolare e il peso spostato verso il manico.",
     "È la forma del controllo: sweet spot centrato e ampio, grande maneggevolezza e facilità in difesa. È la forma consigliata a chi inizia e a chi costruisce il punto con pazienza.",
     "/it/guide/racchette-padel-controllo/"),
    ("racchetta-goccia", "Racchetta a goccia", "Una racchetta a goccia ha una forma intermedia tra rotonda e diamante, con il peso leggermente verso la testa.",
     "È la forma più versatile: un compromesso tra controllo e potenza adatto alla maggior parte dei giocatori, dagli intermedi agli avanzati.",
     "/it/guide/forme-racchetta-padel/"),
    ("superficie-ruvida", "Superficie ruvida", "Una superficie ruvida (sabbiata o con rilievi 3D) aumenta l'attrito tra racchetta e palla.",
     "Serve a dare più effetto ai colpi, come i tagli e le víbora. Con l'uso la ruvidità tende a consumarsi. Molti modelli di fascia alta hanno superfici ruvide, i modelli d'ingresso spesso lisce.",
     "/it/racchette/"),
    ("misure-regolamentari", "Misure regolamentari", "Il regolamento della Federazione Internazionale Padel fissa i limiti della racchetta: lunghezza massima 45,5 cm, larghezza massima 26 cm e spessore massimo 38 mm.",
     "Per questo quasi tutte le racchette da adulto hanno lo stesso spessore di 38 mm; le racchette junior sono più corte e leggere. Il peso non ha un limite regolamentare: le racchette da adulto pesano in genere tra 340 e 375 grammi.",
     "/it/bambini/"),
]


def glossario():
    for slug, nome, defin, testo, link in GLOSSARIO:
        path = f"/it/glossario/{slug}/"
        cr, ld = crumbs([("Home", "/it/"), ("Glossario", "/it/glossario/"), (nome, None)])
        term = {"@context": "https://schema.org", "@type": "DefinedTerm", "name": nome, "description": defin,
                "inDefinedTermSet": SITO + "/it/glossario/", "url": SITO + path}
        altri = "".join(f'<li><a href="/it/glossario/{s}/">{e(n)}</a></li>' for s, n, *_ in GLOSSARIO if s != slug)
        corpo = f'''{cr}
<div class="intro"><h1>{e(nome)}: cos'è nel padel</h1><p><b>{e(defin)}</b></p><p>{e(testo)}</p>{data_riga()}</div>
<div class="prose"><p><a href="{link}">Approfondisci</a></p><h2>Altri termini</h2><ul class="lista-link">{altri}</ul></div>'''
        scrivi(path, pagina(f"{nome}: cos'è e cosa significa nel padel | PadelMetrix", defin[:160], path, corpo, on="guide", ld=[ld, term]))
    cr, ld = crumbs([("Home", "/it/"), ("Glossario", None)])
    voci = "".join(f'<li><a href="/it/glossario/{s}/"><b>{e(n)}</b></a>: {e(d)}</li>' for s, n, d, *_ in GLOSSARIO)
    corpo = f'''{cr}<div class="intro"><h1>Glossario delle racchette da padel</h1><p>I termini tecnici che trovi nelle schede, spiegati in breve.</p>{data_riga()}</div><div class="prose"><ul>{voci}</ul></div>'''
    sett = {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": "Glossario delle racchette da padel", "url": SITO + "/it/glossario/"}
    scrivi("/it/glossario/", pagina("Glossario delle racchette da padel: bilanciamento, EVA, carbonio e altri termini | PadelMetrix",
                                    "Cosa significano bilanciamento, swingweight, sweet spot, EVA, foam, carbonio 12K e le forme delle racchette da padel.",
                                    "/it/glossario/", corpo, on="guide", ld=[ld, sett]))


# ------------------------------------------------------------------ pagine risposta

def faq_ld(q, a):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}]}


def domande(db, stats):
    s, med_peso, min_p, max_p, med_prezzo, forma_top, liv_rows = stats
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
        path = f"/it/domande/{slug}/"
        q = f"Con che racchetta gioca {g}?"
        anno = top["anno"]
        ult = [x for x in its if x["anno"] == anno]
        marche_g = sorted({x["marca"] for x in ult})
        nomi = [x["nome"].replace(f" {anno}", "") for x in ult]
        elenco = ", ".join(nomi[:4]) + (f" e altre {len(nomi) - 4}" if len(nomi) > 4 else "")
        if len(ult) == 1:
            dett = ", ".join(x for x in (f"forma {FORMA_IT[top['forma']].lower()}" if top["forma"] else None, top["peso"]) if x)
            ans = f"Nella collezione {anno} {g} firma la {top['titolo']}" + (f" ({dett})" if dett else "") + "."
        else:
            ans = f"Nella collezione {anno} {g} firma {len(ult)} racchette {' e '.join(marche_g)}: {elenco}."
        if len(its) > len(ult):
            ans += f" In tutto il database PadelMetrix conta {len(its)} modelli firmati tra 2026 e 2027, elencati sotto."
        nota = "I professionisti possono usare versioni personalizzate del modello in vendita."
        cr, ld = crumbs([("Home", "/it/"), ("Domande", "/it/domande/"), (g, None)])
        corpo = f'''{cr}
<div class="intro"><h1>{e(q)}</h1><p><b>{e(ans)}</b> {e(nota)}</p>{data_riga()}</div>
{griglia(its)}
<div class="prose"><p>Tutti i giocatori nella pagina <a href="/it/guide/racchette-giocatori-professionisti/">racchette dei professionisti</a>.</p></div>'''
        scrivi(path, pagina(f"Con che racchetta gioca {g}? Modelli 2026 e 2027 | PadelMetrix", ans[:300], path, corpo, on="guide", ld=[ld, faq_ld(q, ans + " " + nota)]))
        voci.append((path, q))

    # risposte calcolate dal database
    adulti = [n for n in db if n["categoria"] != "junior"]
    q1 = "Quanto pesa una racchetta da padel?"
    a1 = (f"Una racchetta da padel per adulti pesa in genere tra 340 e 375 grammi: nel database PadelMetrix il peso tipico (mediana) è {med_peso} g, "
          f"su {len(s['pesi'])} modelli 2026 e 2027 con peso dichiarato. Le racchette junior pesano meno, di solito tra 280 e 340 g.")
    leggere = sorted([n for n in adulti if n["peso_min"]], key=lambda n: n["peso_min"])[:12]
    q2 = "Quanto costa una racchetta da padel?"
    righe_l = "".join(f"<tr><td>{e(l)}</td><td>{euro(p)}</td><td>{c}</td></tr>" for l, p, c in liv_rows)
    a2 = (f"Il prezzo di listino mediano di una racchetta da padel 2026–2027 è {euro(med_prezzo)} nel database PadelMetrix; "
          f"si va da meno di 100 € per i modelli d'ingresso a oltre 350 € per quelli dei professionisti. Online i prezzi reali sono spesso più bassi del listino.")
    q3 = "Qual è la forma di racchetta da padel più diffusa?"
    a3 = (f"La forma più diffusa è la {FORMA_IT[forma_top].lower()}: {pct(s['forme'][forma_top], s['con_forma'])}% dei {s['con_forma']} modelli per adulti con forma dichiarata nel database PadelMetrix. "
          + ", ".join(f"{FORMA_IT[f].lower()} {pct(c, s['con_forma'])}%" for f, c in sorted(s["forme"].items(), key=lambda kv: -kv[1]) if f != forma_top and c) + ".")
    extra = {
        q1: ("quanto-pesa-una-racchetta-da-padel", f'<h2>Le racchette per adulti più leggere nel database</h2>{griglia(leggere)}'),
        q2: ("quanto-costa-una-racchetta-da-padel", f'<h2>Prezzo di listino mediano per livello</h2><table class="tab"><thead><tr><th>Livello</th><th>Mediana</th><th>Modelli</th></tr></thead><tbody>{righe_l}</tbody></table><p><a href="/it/guide/racchette-padel-economiche/">Racchette economiche fino a 130 €</a></p>'),
        q3: ("forma-racchetta-padel-piu-diffusa", '<p>Le differenze tra le forme sono spiegate nella <a href="/it/guide/forme-racchetta-padel/">guida alle forme</a>.</p>'),
    }
    for q, a in ((q1, a1), (q2, a2), (q3, a3)):
        slug, html_extra = extra[q]
        path = f"/it/domande/{slug}/"
        cr, ld = crumbs([("Home", "/it/"), ("Domande", "/it/domande/"), (q, None)])
        corpo = f'''{cr}<div class="intro"><h1>{e(q)}</h1><p><b>{e(a)}</b></p>{data_riga()}</div>
<div class="prose">{html_extra}<p class="note">Calcolato sul database PadelMetrix; metodo e limiti nel <a href="/it/report/racchette-padel-2026-2027-in-numeri/">report in numeri</a>.</p></div>'''
        scrivi(path, pagina(f"{q} Dati 2026–2027 | PadelMetrix", a[:300], path, corpo, on="guide", ld=[ld, faq_ld(q, a)]))
        voci.insert(0, (path, q))

    cr, ld = crumbs([("Home", "/it/"), ("Domande", None)])
    corpo = f'''{cr}<div class="intro"><h1>Domande frequenti sulle racchette da padel</h1><p>Risposte brevi, con i dati del database PadelMetrix.</p>{data_riga()}</div>
<div class="prose"><ul class="lista-link">{"".join(f'<li><a href="{p}">{e(q)}</a></li>' for p, q in voci)}</ul></div>'''
    scrivi("/it/domande/", pagina("Domande frequenti sulle racchette da padel | PadelMetrix",
                                  "Quanto pesa e quanto costa una racchetta da padel, che forma scegliere, con che racchetta giocano i professionisti: risposte con i dati.",
                                  "/it/domande/", corpo, on="guide", ld=[ld]))


# ------------------------------------------------------------------ llms.txt

def llms(db):
    s = statistiche(db)
    txt = f"""# PadelMetrix

> Database indipendente di racchette da padel: {s['n']} schede delle collezioni 2026 e 2027 di {len(s['marche'])} marche, con dati tecnici, fonti citate, confronti e guide. Sito in italiano (inglese e spagnolo in arrivo). Aggiornato il {OGGI}.

## Sezioni principali
- [Racchette](https://www.padelmetrix.com/it/racchette/): tutte le schede con filtri per marca, forma, livello, stile e prezzo
- [Marche](https://www.padelmetrix.com/it/marche/): i modelli di ogni marca
- [Confronti](https://www.padelmetrix.com/it/confronta/): confronti modello contro modello
- [Guide](https://www.padelmetrix.com/it/guide/): come scegliere la racchetta per livello, problema fisico, budget
- [Bambini](https://www.padelmetrix.com/it/bambini/): misure per età e racchette junior
- [Domande frequenti](https://www.padelmetrix.com/it/domande/): risposte brevi con dati
- [Glossario](https://www.padelmetrix.com/it/glossario/): termini tecnici

## Dati originali
- [Report Racchette da padel 2026–2027 in numeri](https://www.padelmetrix.com/it/report/racchette-padel-2026-2027-in-numeri/)
- [Dataset aperto CSV/JSON, licenza CC BY 4.0](https://www.padelmetrix.com/it/dati/)

## Metodo
- [Chi siamo e metodo](https://www.padelmetrix.com/it/chi-siamo/): fonti dei dati, indipendenza, aggiornamenti
"""
    (ROOT / "llms.txt").write_text(txt, encoding="utf-8")


def main():
    db = carica()
    chi_siamo(db)
    stats = report(db)
    dataset(db)
    glossario()
    domande(db, stats)
    llms(db)
    (ROOT / "scripts" / "pagine_geo.json").write_text(json.dumps(PAGINE, indent=0), encoding="utf-8")
    print(len(PAGINE), "pagine GEO generate")


if __name__ == "__main__":
    main()
