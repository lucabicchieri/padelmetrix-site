"""Articolo dati: le racchette 2027 in numeri rispetto al 2026, calcolato dal catalogo a ogni build.
Importato da genera_articoli."""
import collections
import json
import re
import statistics as st

import sito as S
from sito import L, P, ROOT

NU_SLUG = "tendenze-racchette-padel-2027"
S.SLUG[NU_SLUG] = ("padel-racket-trends-2027", "tendencias-palas-padel-2027")
S.SLUG_FR[NU_SLUG] = "tendances-raquettes-padel-2027"

FORME = ("goccia", "diamante", "rotonda", "ibrida")


def _peso(d):
    n = [float(x) for x in re.findall(r"\d{3}", str(d.get("peso") or d.get("peso_g") or d.get("peso_nominale_g") or ""))]
    return sum(n) / len(n) if n else None


def _carbonio(d):
    t = (str(d.get("superficie") or "") + " " + str(d.get("telaio") or "")).lower().replace(" ", "")
    for k in ("24k", "18k", "16k", "15k", "12k", "6k", "3k", "1k"):
        if k in t:
            return k.upper()
    if any(w in t for w in ("fibra", "fiber", "fibrix", "glass", "vetro")):
        return "fibra"
    return "altro" if "carbon" in t else None


def _prezzo(d):
    try:
        return float(d.get("prezzo_listino_eur")) if d.get("prezzo_listino_eur") else None
    except (TypeError, ValueError):
        return None


def statistiche():
    R = [json.loads(f.read_text(encoding="utf-8")) for f in (ROOT / "data" / "racchette").glob("*.json")]
    out = {}
    for y in ("2026", "2027"):
        X = [d for d in R if str(d.get("anno")) == y and d.get("categoria") in (None, "adulto")]
        f = collections.Counter(d.get("forma") for d in X if d.get("forma") in FORME)
        c = collections.Counter(_carbonio(d) for d in X if _carbonio(d))
        ws = [w for w in (_peso(d) for d in X) if w]
        pz = [p for p in (_prezzo(d) for d in X) if p]
        ruv = sum(1 for d in X if re.search(r"ruvid|rugos|3d|sand|spin", f"{d.get('finitura') or ''} {d.get('superficie') or ''}", re.I))
        out[y] = {"n": len(X), "marche": len({d["marca"] for d in X}), "forme": f, "nf": sum(f.values()), "carb": c, "nc": sum(c.values()),
                  "peso": round(st.median(ws)) if ws else None, "leggere": sum(1 for w in ws if w < 350), "nw": len(ws),
                  "prezzo": round(st.median(pz)) if pz else None, "np": len(pz), "firmate": sum(1 for d in X if d.get("giocatore")),
                  "ruvide": ruv, "pro": sum(1 for d in X if d.get("livello") == "professionale")}
    return out


def _pc(a, b):
    return round(a / b * 100) if b else 0


def art_numeri_2027(db, fonte, faq, scrivi_articolo, tab):
    s = statistiche()
    a, b = s["2026"], s["2027"]
    nomi_forma = {k: S.FORMA(k) for k in FORME}
    righe_f = [(nomi_forma[k], f"{_pc(a['forme'][k], a['nf'])}%", f"{_pc(b['forme'][k], b['nf'])}%") for k in FORME]
    t_forme = tab([L("Forma", "Shape", "Forma", "Forme"), "2026", "2027"], righe_f)
    cl = {"fibra": L("Fibra di vetro", "Fibreglass", "Fibra de vidrio", "Fibre de verre"), "altro": L("Carbonio (non specificato)", "Carbon (unspecified)", "Carbono (sin especificar)", "Carbone (non précisé)")}
    ordine = ("fibra", "3K", "12K", "18K", "24K")
    righe_c = [(cl.get(k, L(f"Carbonio {k}", f"{k} carbon", f"Carbono {k}", f"Carbone {k}")), f"{_pc(a['carb'][k], a['nc'])}%", f"{_pc(b['carb'][k], b['nc'])}%") for k in ordine]
    t_carb = tab([L("Materiale del piatto", "Face material", "Material de las caras", "Matériau du tamis"), "2026", "2027"], righe_c)
    righe_alt = [
        (L("Modelli nel nostro catalogo", "Models in our catalogue", "Modelos en nuestro catálogo", "Modèles dans notre catalogue"), str(a["n"]), str(b["n"])),
        (L("Marchi", "Brands", "Marcas", "Marques"), str(a["marche"]), str(b["marche"])),
        (L("Peso mediano", "Median weight", "Peso mediano", "Poids médian"), f"{a['peso']} g", f"{b['peso']} g"),
        (L("Modelli sotto i 350 g", "Models under 350 g", "Modelos de menos de 350 g", "Modèles sous 350 g"), str(a["leggere"]), str(b["leggere"])),
        (L("Prezzo di listino mediano", "Median list price", "Precio de lista mediano", "Prix catalogue médian"), f"{a['prezzo']} €", f"{b['prezzo']} €"),
        (L("Superficie ruvida", "Rough surface", "Superficie rugosa", "Surface rugueuse"), f"{_pc(a['ruvide'], a['n'])}%", f"{_pc(b['ruvide'], b['n'])}%"),
        (L("Firmate da un professionista", "Signed by a pro", "Firmadas por un profesional", "Signées par un pro"), f"{_pc(a['firmate'], a['n'])}%", f"{_pc(b['firmate'], b['n'])}%"),
    ]
    t_alt = tab([L("Indicatore", "Indicator", "Indicador", "Indicateur"), "2026", "2027"], righe_alt)
    dia_a, dia_b = _pc(a["forme"]["diamante"], a["nf"]), _pc(b["forme"]["diamante"], b["nf"])
    ibr_a, ibr_b = _pc(a["forme"]["ibrida"], a["nf"]), _pc(b["forme"]["ibrida"], b["nf"])
    k12a, k12b = _pc(a["carb"]["12K"], a["nc"]), _pc(b["carb"]["12K"], b["nc"])
    ra, rb = _pc(a["ruvide"], a["n"]), _pc(b["ruvide"], b["n"])
    cat, novita = P("racchette"), P("articoli", "racchette-padel-2027-vs-2026-cosa-cambia")
    rep = P("report", "racchette-padel-2026-2027-in-numeri")
    import datetime as _dt
    oggi = S.data_txt(_dt.date.today().isoformat())
    corpo = L(f'''<p><b>Le racchette da padel 2027 uscite finora sono più spesso ibride ({ibr_b}% contro {ibr_a}% nel 2026) e meno spesso a diamante ({dia_b}% contro {dia_a}%), usano più carbonio 12K ({k12b}% dei modelli con materiale dichiarato, contro {k12a}%) e più superfici ruvide ({rb}% contro {ra}%). Il peso mediano resta {b['peso']} g, mentre il prezzo di listino mediano sale da {a['prezzo']} a {b['prezzo']} €.</b></p>
<p>Abbiamo calcolato questi numeri sulle {a['n']} racchette 2026 e sulle {b['n']} racchette 2027 per adulti del nostro <a href="{cat}">catalogo</a>, con i dati dichiarati dai produttori. La pagina si aggiorna da sola quando aggiungiamo nuovi modelli: dati al {oggi}.</p>
<h2>Forme: meno diamante, più ibride</h2>{t_forme}
<p>La goccia resta la forma più diffusa. Le ibride, a metà tra goccia e diamante, crescono soprattutto nelle linee che hanno una versione "Hybrid" accanto a quella da attacco.</p>
<h2>Materiali: il 12K diventa il carbonio più usato</h2>{t_carb}
<p>Percentuali calcolate sui modelli con materiale del piatto dichiarato ({a['nc']} nel 2026, {b['nc']} nel 2027). La fibra di vetro resta molto presente nelle versioni "Comfort" e da donna, pensate per un tatto più morbido.</p>
<h2>Peso, prezzo e altri dati</h2>{t_alt}
<p>Il prezzo mediano è calcolato sui modelli con listino dichiarato ({a['np']} nel 2026, {b['np']} nel 2027). Nel 2027 non abbiamo ancora modelli per adulti sotto i 350 g.</p>
<h2>Come leggere questi numeri</h2>
<ul>
<li><b>La collezione 2027 non è completa.</b> I marchi presentano prima le linee per giocatori avanzati e le racchette dei professionisti: per questo le firmate e i modelli di fascia alta oggi pesano di più. Le percentuali cambieranno con le uscite di inizio 2027.</li>
<li><b>Contano i modelli, non le vendite.</b> Una racchetta che vende migliaia di pezzi pesa quanto una venduta poco.</li>
<li><b>I dati sono quelli dichiarati</b> da produttori e negozi, con le fonti citate in ogni scheda.</li>
</ul>
<p>Per i numeri complessivi del catalogo (pesi, prezzi per livello, marchi) c'è il <a href="{rep}">report racchette 2026–2027 in numeri</a>. Per le differenze modello per modello leggi <a href="{novita}">racchette 2027 contro 2026: cosa cambia</a>.</p>''',
              f'''<p><b>The 2027 padel rackets released so far are more often hybrid ({ibr_b}% against {ibr_a}% in 2026) and less often diamond-shaped ({dia_b}% against {dia_a}%), use more 12K carbon ({k12b}% of models with a stated material, against {k12a}%) and more rough surfaces ({rb}% against {ra}%). The median weight stays at {b['peso']} g, while the median list price rises from €{a['prezzo']} to €{b['prezzo']}.</b></p>
<p>We calculated these figures on the {a['n']} adult rackets from 2026 and the {b['n']} from 2027 in our <a href="{cat}">catalogue</a>, using manufacturers' stated data. The page updates itself when we add new models: data as of {oggi}.</p>
<h2>Shapes: less diamond, more hybrid</h2>{t_forme}
<p>Teardrop remains the most common shape. Hybrids, halfway between teardrop and diamond, grow mainly in lines that offer a "Hybrid" version next to the attacking one.</p>
<h2>Materials: 12K becomes the most used carbon</h2>{t_carb}
<p>Percentages of models with a stated face material ({a['nc']} in 2026, {b['nc']} in 2027). Fibreglass is still common in "Comfort" and women's versions, designed for a softer feel.</p>
<h2>Weight, price and other figures</h2>{t_alt}
<p>Median price calculated on models with a stated list price ({a['np']} in 2026, {b['np']} in 2027). We do not yet have any 2027 adult models under 350 g.</p>
<h2>How to read these figures</h2>
<ul>
<li><b>The 2027 collection is not complete.</b> Brands launch their advanced lines and pro players' rackets first, so signature and high-end models weigh more today. The percentages will change with the early-2027 releases.</li>
<li><b>Models count, not sales.</b> A racket that sells thousands of units counts the same as one that sells few.</li>
<li><b>The data is what brands and shops state,</b> with sources listed on each racket page.</li>
</ul>
<p>For the overall catalogue figures (weights, prices by level, brands) see the <a href="{rep}">2026–2027 padel rackets in numbers report</a>. For model-by-model differences read <a href="{novita}">2027 vs 2026 rackets: what changes</a>.</p>''',
              f'''<p><b>Las palas de pádel 2027 que han salido hasta ahora son más a menudo híbridas ({ibr_b}% frente al {ibr_a}% en 2026) y menos a menudo diamante ({dia_b}% frente al {dia_a}%), usan más carbono 12K ({k12b}% de los modelos con material declarado, frente al {k12a}%) y más superficies rugosas ({rb}% frente al {ra}%). El peso mediano sigue en {b['peso']} g, mientras que el precio de lista mediano sube de {a['prezzo']} a {b['prezzo']} €.</b></p>
<p>Hemos calculado estas cifras sobre las {a['n']} palas de adulto de 2026 y las {b['n']} de 2027 de nuestro <a href="{cat}">catálogo</a>, con los datos declarados por los fabricantes. La página se actualiza sola cuando añadimos modelos: datos a {oggi}.</p>
<h2>Formas: menos diamante, más híbridas</h2>{t_forme}
<p>La lágrima sigue siendo la forma más común. Las híbridas, a medio camino entre lágrima y diamante, crecen sobre todo en las líneas que tienen una versión "Hybrid" junto a la de ataque.</p>
<h2>Materiales: el 12K pasa a ser el carbono más usado</h2>{t_carb}
<p>Porcentajes sobre los modelos con material de las caras declarado ({a['nc']} en 2026, {b['nc']} en 2027). La fibra de vidrio sigue muy presente en las versiones "Comfort" y de mujer, pensadas para un tacto más blando.</p>
<h2>Peso, precio y otros datos</h2>{t_alt}
<p>Precio mediano calculado sobre los modelos con precio de lista declarado ({a['np']} en 2026, {b['np']} en 2027). En 2027 aún no tenemos palas de adulto por debajo de 350 g.</p>
<h2>Cómo leer estas cifras</h2>
<ul>
<li><b>La colección 2027 no está completa.</b> Las marcas presentan primero las líneas avanzadas y las palas de los profesionales: por eso hoy pesan más las firmadas y las de gama alta. Los porcentajes cambiarán con los lanzamientos de principios de 2027.</li>
<li><b>Cuentan los modelos, no las ventas.</b> Una pala que vende miles de unidades cuenta igual que una que vende poco.</li>
<li><b>Los datos son los declarados</b> por fabricantes y tiendas, con las fuentes en cada ficha.</li>
</ul>
<p>Para las cifras generales del catálogo (pesos, precios por nivel, marcas) está el <a href="{rep}">informe palas 2026–2027 en cifras</a>. Para las diferencias modelo a modelo lee <a href="{novita}">palas 2027 frente a 2026: qué cambia</a>.</p>''',
              f'''<p><b>Les raquettes de padel 2027 sorties jusqu'ici sont plus souvent hybrides ({ibr_b} % contre {ibr_a} % en 2026) et moins souvent en diamant ({dia_b} % contre {dia_a} %), utilisent davantage le carbone 12K ({k12b} % des modèles au matériau déclaré, contre {k12a} %) et plus de surfaces rugueuses ({rb} % contre {ra} %). Le poids médian reste de {b['peso']} g, tandis que le prix catalogue médian passe de {a['prezzo']} à {b['prezzo']} €.</b></p>
<p>Nous avons calculé ces chiffres sur les {a['n']} raquettes adultes 2026 et les {b['n']} raquettes 2027 de notre <a href="{cat}">catalogue</a>, avec les données déclarées par les fabricants. La page se met à jour seule quand nous ajoutons des modèles : données au {oggi}.</p>
<h2>Formes : moins de diamant, plus d'hybrides</h2>{t_forme}
<p>La goutte d'eau reste la forme la plus répandue. Les hybrides, entre goutte d'eau et diamant, progressent surtout dans les gammes qui proposent une version « Hybrid » à côté de la version d'attaque.</p>
<h2>Matériaux : le 12K devient le carbone le plus utilisé</h2>{t_carb}
<p>Pourcentages sur les modèles au matériau de tamis déclaré ({a['nc']} en 2026, {b['nc']} en 2027). La fibre de verre reste très présente dans les versions « Comfort » et femme, pensées pour un toucher plus doux.</p>
<h2>Poids, prix et autres données</h2>{t_alt}
<p>Prix médian calculé sur les modèles au prix catalogue déclaré ({a['np']} en 2026, {b['np']} en 2027). En 2027, nous n'avons encore aucun modèle adulte sous 350 g.</p>
<h2>Comment lire ces chiffres</h2>
<ul>
<li><b>La collection 2027 n'est pas complète.</b> Les marques présentent d'abord les gammes avancées et les raquettes des pros : c'est pourquoi les modèles signés et haut de gamme pèsent plus aujourd'hui. Les pourcentages évolueront avec les sorties de début 2027.</li>
<li><b>On compte les modèles, pas les ventes.</b> Une raquette vendue à des milliers d'exemplaires compte autant qu'une raquette peu vendue.</li>
<li><b>Les données sont celles déclarées</b> par les marques et les magasins, avec les sources sur chaque fiche.</li>
</ul>
<p>Pour les chiffres globaux du catalogue (poids, prix par niveau, marques), consultez le <a href="{rep}">rapport raquettes 2026–2027 en chiffres</a>. Pour les différences modèle par modèle, lisez <a href="{novita}">raquettes 2027 contre 2026 : ce qui change</a>.</p>''')
    qa = [(L("Quali sono le novità delle racchette da padel 2027?", "What is new in 2027 padel rackets?", "¿Qué novedades traen las palas de pádel 2027?", "Quelles sont les nouveautés des raquettes de padel 2027 ?"),
           L(f"Tra i modelli usciti finora crescono le forme ibride ({ibr_b}%), il carbonio 12K ({k12b}%) e le superfici ruvide ({rb}%); il peso mediano resta {b['peso']} g.",
             f"Among the models released so far, hybrid shapes ({ibr_b}%), 12K carbon ({k12b}%) and rough surfaces ({rb}%) are growing; the median weight stays at {b['peso']} g.",
             f"Entre los modelos lanzados hasta ahora crecen las formas híbridas ({ibr_b}%), el carbono 12K ({k12b}%) y las superficies rugosas ({rb}%); el peso mediano sigue en {b['peso']} g.",
             f"Parmi les modèles sortis jusqu'ici, les formes hybrides ({ibr_b} %), le carbone 12K ({k12b} %) et les surfaces rugueuses ({rb} %) progressent ; le poids médian reste de {b['peso']} g.")),
          (L("Le racchette 2027 costano di più?", "Do 2027 rackets cost more?", "¿Las palas 2027 cuestan más?", "Les raquettes 2027 coûtent-elles plus cher ?"),
           L(f"Il prezzo di listino mediano dei modelli 2027 usciti finora è {b['prezzo']} €, contro {a['prezzo']} € del 2026; pesa il fatto che i marchi presentano prima le linee di fascia alta.",
             f"The median list price of the 2027 models released so far is €{b['prezzo']}, against €{a['prezzo']} in 2026; partly because brands launch their high-end lines first.",
             f"El precio de lista mediano de los modelos 2027 lanzados hasta ahora es {b['prezzo']} €, frente a {a['prezzo']} € en 2026; influye que las marcas presentan antes las gamas altas.",
             f"Le prix catalogue médian des modèles 2027 sortis jusqu'ici est de {b['prezzo']} €, contre {a['prezzo']} € en 2026 ; les marques lancent d'abord leurs gammes haut de gamme."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("Racchette da padel 2027: le tendenze rispetto al 2026 (forme, carbonio, prezzi)", "Padel racket trends for 2027: what changes from 2026 (shapes, carbon, prices)",
               "Tendencias de las palas de pádel 2027 frente a 2026 (formas, carbono, precios)", "Tendances des raquettes de padel 2027 face à 2026 (formes, carbone, prix)")
    desc = L(f"Le racchette 2027 contro le 2026 nel nostro catalogo: più ibride e 12K, più superfici ruvide, peso mediano {b['peso']} g, listino mediano {b['prezzo']} €.",
             f"2027 vs 2026 padel rackets in our catalogue: more hybrids and 12K carbon, more rough faces, median weight {b['peso']} g, median list price €{b['prezzo']}.",
             f"Palas 2027 frente a 2026 en nuestro catálogo: más híbridas y 12K, más superficies rugosas, peso mediano {b['peso']} g, precio mediano {b['prezzo']} €.",
             f"Raquettes 2027 contre 2026 dans notre catalogue : plus d'hybrides et de 12K, plus de surfaces rugueuses, poids médian {b['peso']} g, prix médian {b['prezzo']} €.")
    scrivi_articolo(NU_SLUG, titolo + " | PadelMetrix", desc, titolo, L("Tendenze racchette 2027", "2027 racket trends", "Tendencias palas 2027", "Tendances raquettes 2027"), corpo + faq_htm, ld_extra=[faq_ld])
    return NU_SLUG, titolo, L("Forme, carbonio, peso e prezzi: le racchette 2027 contro le 2026, con i dati del nostro catalogo.", "Shapes, carbon, weight and prices: 2027 rackets against 2026, from our catalogue data.",
                              "Formas, carbono, peso y precios: las palas 2027 frente a las 2026, con los datos de nuestro catálogo.", "Formes, carbone, poids et prix : les raquettes 2027 face aux 2026, d'après notre catalogue.")
