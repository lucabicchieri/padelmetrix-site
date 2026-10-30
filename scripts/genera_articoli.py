#!/usr/bin/env python3
"""Genera la sezione Articoli in it/en/es: indice + articoli.

Regole come nel resto del sito: ogni dato viene dal database delle racchette o da una fonte citata;
quello che le fonti non pubblicano resta "non dichiarato". I testi sono scritti nelle tre lingue.
"""
import json
import sys
import pathlib
from collections import Counter
from urllib.parse import urlparse

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import (ROOT, SITO, e, L, P, ALT, carica, crumbs, pagina, griglia, ordina, FORMA, LIVN, euro,  # noqa: E402
                  url_r, LINGUE, set_lang, data_riga, confronto_url, coppie)

OGGI_ISO = "2026-10-30"


def T(it, en, es):
    return {"it": it, "en": en, "es": es}


def g(d):
    return d[S.lang()] if isinstance(d, dict) else d


def H():
    return S.home_crumb()


def fonte(u, nome=None):
    nome = nome or urlparse(u).netloc.replace("www.", "")
    return f'<a href="{e(u)}" rel="nofollow noopener" target="_blank">{e(nome)}</a>'


def articolo_ld(titolo, desc, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titolo, "description": desc,
            "inLanguage": S.lang(), "datePublished": OGGI_ISO, "dateModified": OGGI_ISO,
            "author": S.autore(), "publisher": S.editore(), "mainEntityOfPage": SITO + path}


def scrivi_articolo(slug, title, desc, h1, crumb, corpo_html, items=None, ld_extra=()):
    path, alt = P("articoli", slug), ALT("articoli", slug)
    cr, ld = crumbs([H(), (L("Articoli", "Articles", "Artículos"), P("articoli")), (crumb, None)])
    lista = (f'<section class="block"><h2>{L("Le racchette citate", "Rackets mentioned", "Las palas citadas")} ({len(items)})</h2>{griglia(ordina(items))}</section>'
             if items else "")
    corpo = f'''{cr}
<div class="intro"><div class="eyebrow">{L("Articolo", "Article", "Artículo")}</div><h1>{e(h1)}</h1><p class="note">{L("Pubblicato il ", "Published on ", "Publicado el ")}{S.data_txt(OGGI_ISO)} · {L("a cura di", "by", "por")} <a href="{P("chi-siamo")}">Luca Bicchieri, PadelMetrix</a></p></div>
<div class="prose">{corpo_html}</div>
{lista}'''
    S.scrivi(path, pagina(title, desc, path, corpo, on="articoli", ld=[ld, articolo_ld(h1, desc, path), *ld_extra], alt=alt), alt)


def faq(qa):
    htm = f'<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes")}</h2><div class="faq">' + "".join(
        f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</div>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    return htm, ld


# ---------------------------------------------------------------- 1. Novità 2027 per marca

def novita_2027(db):
    slug = "racchette-padel-2027-novita-per-marca"
    nuove = [n for n in db if n["anno"] == 2027 and n["categoria"] != "junior"]
    per_marca = {}
    for n in nuove:
        per_marca.setdefault(n["marca"], []).append(n)
    marche = sorted(per_marca, key=lambda m: (-len(per_marca[m]), m))
    vecchi = {(n["marca"], n["modello"]): n for n in db if n["anno"] == 2026}
    pairs = set(coppie(db))

    prezzi = [n["prezzo"] for n in nuove if n["prezzo"]]
    forme = Counter(n["forma"] for n in nuove if n["forma"])
    forma_top, forma_n = forme.most_common(1)[0] if forme else (None, 0)

    def riga(n):
        old = vecchi.get((n["marca"], n["modello"]))
        rif = ""
        if old and tuple(sorted((n["slug"], old["slug"]))) in pairs:
            rif = f'<a href="{confronto_url(old["slug"], n["slug"])}">{L("vs 2026", "vs 2026", "vs 2026")}</a>'
        celle = [f'<a href="{url_r(n)}">{e(n["nome"])}</a>', e((S.tr(n["giocatore"]) if "ispirata" in n["giocatore"] else n["giocatore"]) if n["giocatore"] else "—"), e(FORMA(n["forma"]) or L("n.d.", "n/a", "n.d.")),
                 e(n["peso"] or L("n.d.", "n/a", "n.d.")), e(LIVN(n["livello"]) or L("n.d.", "n/a", "n.d.")),
                 euro(n["prezzo"]) if n["prezzo"] else L("n.d.", "n/a", "n.d."), rif]
        return "<tr>" + "".join(f"<td>{c}</td>" for c in celle) + "</tr>"

    th = [L("Modello", "Model", "Modelo"), L("Giocatore", "Player", "Jugador"), L("Forma", "Shape", "Forma"), L("Peso", "Weight", "Peso"),
          L("Livello", "Level", "Nivel"), L("Listino", "List price", "Precio"), L("Confronto", "Comparison", "Comparativa")]
    sezioni = []
    indice = []
    for m in marche:
        items = sorted(per_marca[m], key=lambda n: (-(n["prezzo"] or 0), n["nome"]))
        pz = [n["prezzo"] for n in items if n["prezzo"]]
        fm = Counter(n["forma"] for n in items if n["forma"])
        gioc = sorted({n["giocatore"] for n in items if n["giocatore"] and "ispirata" not in n["giocatore"]})
        rinnovi = sum(1 for n in items if (n["marca"], n["modello"]) in vecchi)
        fonti = []
        for n in items:
            for u in n["d"].get("fonti_dati", []):
                if u not in fonti:
                    fonti.append(u)
        frasi = [L(f"<b>{len(items)} modelli 2027</b> nel nostro database",
                   f"<b>{len(items)} 2027 models</b> in our database",
                   f"<b>{len(items)} modelos 2027</b> en nuestra base de datos")]
        if pz:
            frasi.append(L(f"listino da {euro(min(pz))} a {euro(max(pz))}", f"list prices from {euro(min(pz))} to {euro(max(pz))}",
                           f"precio de lista de {euro(min(pz))} a {euro(max(pz))}"))
        if fm:
            fm_txt = ", ".join(f"{FORMA(k).lower()} {v}" for k, v in fm.most_common())
            frasi.append(L(f"forme: {fm_txt}", f"shapes: {fm_txt}", f"formas: {fm_txt}"))
        if rinnovi:
            frasi.append(L(f"{rinnovi} sono il rinnovo di un modello 2026", f"{rinnovi} replace a 2026 model", f"{rinnovi} renuevan un modelo 2026"))
        gtxt = ""
        if gioc:
            gtxt = L(f" Modelli firmati: {', '.join(gioc)}.", f" Signature models: {', '.join(gioc)}.", f" Modelos firmados: {', '.join(gioc)}.")
        ancora = S.slugify(m)
        indice.append(f'<a href="#{ancora}">{e(m)} ({len(items)})</a>')
        sezioni.append(f'''<h2 id="{ancora}">{e(m)}</h2>
<p>{"; ".join(frasi)}.{gtxt}</p>
<div class="tablebox"><table class="tab"><thead><tr>{"".join(f"<th>{t}</th>" for t in th)}</tr></thead><tbody>{"".join(riga(n) for n in items)}</tbody></table></div>
<p class="note">{L("Fonti dei dati", "Data sources", "Fuentes de los datos")}: {", ".join(fonte(u) for u in fonti[:6])}{" …" if len(fonti) > 6 else ""}.</p>''')

    qa = [(L("Quali marchi hanno già presentato le racchette 2027?", "Which brands have already launched their 2027 rackets?", "¿Qué marcas ya han presentado sus palas 2027?"),
           L(f"Nel database PadelMetrix al {S.data_txt(OGGI_ISO)} ci sono modelli 2027 di {', '.join(marche)}. Gli altri marchi verranno aggiunti appena pubblicano le collezioni con dati verificabili.",
             f"As of {S.data_txt(OGGI_ISO)}, the PadelMetrix database includes 2027 models from {', '.join(marche)}. Other brands will be added as soon as they publish their collections with verifiable data.",
             f"A {S.data_txt(OGGI_ISO)}, la base de datos de PadelMetrix incluye modelos 2027 de {', '.join(marche)}. Las demás marcas se añadirán en cuanto publiquen sus colecciones con datos verificables.")),
          (L("Quanto costano le racchette da padel 2027?", "How much do 2027 padel rackets cost?", "¿Cuánto cuestan las palas de pádel 2027?"),
           L(f"Tra i modelli con prezzo dichiarato il listino va da {euro(min(prezzi))} a {euro(max(prezzi))}. I prezzi reali nei negozi cambiano spesso e i modelli 2026 si trovano scontati.",
             f"Among models with a declared price, list prices range from {euro(min(prezzi))} to {euro(max(prezzi))}. Real shop prices change often and 2026 models can be found discounted.",
             f"Entre los modelos con precio declarado, el precio de lista va de {euro(min(prezzi))} a {euro(max(prezzi))}. Los precios reales cambian a menudo y los modelos 2026 se encuentran rebajados.")) if prezzi else None,
          (L("Conviene comprare il modello 2027 o il 2026 scontato?", "Should I buy the 2027 model or the discounted 2026?", "¿Conviene comprar el modelo 2027 o el 2026 rebajado?"),
           L("Dipende da quanto cambia davvero: in molti casi le schede tecniche sono quasi uguali e il 2026 costa meno. Per ogni rinnovo trovi il link al confronto tra le due versioni.",
             "It depends on how much really changes: in many cases the spec sheets are almost identical and the 2026 costs less. For each update there is a link to the comparison between the two versions.",
             "Depende de cuánto cambie realmente: en muchos casos las fichas técnicas son casi iguales y el 2026 cuesta menos. Para cada renovación tienes el enlace a la comparativa entre las dos versiones."))]
    qa = [x for x in qa if x]
    faq_htm, faq_ld = faq(qa)

    intro = L(
        f"<p><b>Le collezioni 2027 sono arrivate nei negozi: nel database PadelMetrix ci sono già {len(nuove)} racchette 2027 di {len(marche)} marchi.</b> "
        + (f"La forma più diffusa è la {FORMA(forma_top).lower()} ({forma_n} modelli) e i listini vanno da {euro(min(prezzi))} a {euro(max(prezzi))}. " if prezzi and forma_top else "")
        + "Qui sotto trovi le novità marca per marca, con i dati dichiarati da produttori e rivenditori e il link al confronto con il modello 2026 quando esiste.</p>",
        f"<p><b>The 2027 collections have reached the shops: the PadelMetrix database already lists {len(nuove)} 2027 rackets from {len(marche)} brands.</b> "
        + (f"The most common shape is {FORMA(forma_top).lower()} ({forma_n} models) and list prices range from {euro(min(prezzi))} to {euro(max(prezzi))}. " if prezzi and forma_top else "")
        + "Below are the new models brand by brand, with the data declared by manufacturers and retailers and a link to the comparison with the 2026 model where one exists.</p>",
        f"<p><b>Las colecciones 2027 ya están en las tiendas: la base de datos de PadelMetrix ya incluye {len(nuove)} palas 2027 de {len(marche)} marcas.</b> "
        + (f"La forma más común es {FORMA(forma_top).lower()} ({forma_n} modelos) y los precios de lista van de {euro(min(prezzi))} a {euro(max(prezzi))}. " if prezzi and forma_top else "")
        + "Abajo tienes las novedades marca por marca, con los datos declarados por fabricantes y tiendas y el enlace a la comparativa con el modelo 2026 cuando existe.</p>")
    metodo = L(
        f'<p class="note">Come leggere i dati: "n.d." significa che il dato non è pubblicato dalle fonti consultate. Le valutazioni indipendenti dei modelli 2027 sono ancora poche: quando escono le aggiungiamo alle schede. Vedi anche <a href="{P("guide", "racchette-padel-2026-2027-in-numeri")}">le racchette 2026 e 2027 in numeri</a>.</p>',
        f'<p class="note">How to read the data: "n/a" means the figure is not published by the sources we consulted. Independent reviews of 2027 models are still few: we add them to the spec pages as they come out. See also <a href="{P("guide", "racchette-padel-2026-2027-in-numeri")}">2026 and 2027 rackets in numbers</a>.</p>',
        f'<p class="note">Cómo leer los datos: "n.d." significa que el dato no lo publican las fuentes consultadas. Las valoraciones independientes de los modelos 2027 todavía son pocas: las añadimos a las fichas cuando salen. Mira también <a href="{P("guide", "racchette-padel-2026-2027-in-numeri")}">las palas 2026 y 2027 en cifras</a>.</p>')
    corpo = intro + f'<div class="marche">{"".join(indice)}</div>' + metodo + "".join(sezioni) + faq_htm
    titolo = L("Racchette padel 2027: tutte le novità per marca", "Padel rackets 2027: what's new from every brand", "Palas de pádel 2027: todas las novedades por marca")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L(f"Le racchette da padel 2027 di {', '.join(marche[:4])} e altri: {len(nuove)} modelli con forma, peso, giocatore, prezzo di listino e confronto con il 2026.",
                      f"2027 padel rackets from {', '.join(marche[:4])} and more: {len(nuove)} models with shape, weight, player, list price and comparison with 2026.",
                      f"Las palas de pádel 2027 de {', '.join(marche[:4])} y otras: {len(nuove)} modelos con forma, peso, jugador, precio de lista y comparativa con 2026."),
                    titolo, L("Novità 2027", "What's new in 2027", "Novedades 2027"), corpo, ld_extra=[faq_ld])
    return slug, titolo, L(f"{len(nuove)} modelli 2027 di {len(marche)} marchi, con dati e confronti.", f"{len(nuove)} 2027 models from {len(marche)} brands, with data and comparisons.",
                           f"{len(nuove)} modelos 2027 de {len(marche)} marcas, con datos y comparativas.")


# ---------------------------------------------------------------- 2. Siux Diablo Pro 2026 vs 2027

F_PM = "https://padelmarket.com/it-eu/products/siux-diablo-pro-2026-night-blue-pala"
F_RG = "https://www.racketguide.com/gb-en/padel/siux/diablo-pro-night-blue-2026/"
F_PS = "https://padelspeed.com/blogs/news/siux-2026-padel-rackets-in-depth-review"
F_PP = "https://padelproshop.com/en-dk/products/siux-padel-racket-diablo-pro-metallic-blue-2027-tino-libaak"
F_PP2 = "https://padelproshop.com/pages/siux-2027"

ND = T("Non dichiarato", "Not stated", "No declarado")

DIABLO = [  # (voce, 2026, 2027, cambia?)
    (T("Giocatore", "Player", "Jugador"), "Tino Libaak", "Tino Libaak", False),
    (T("Forma", "Shape", "Forma"), T("Goccia secondo Padel Market (Racketguide e PadelSpeed: ibrida)", "Teardrop according to Padel Market (Racketguide and PadelSpeed: hybrid)",
                                     "Lágrima según Padel Market (Racketguide y PadelSpeed: híbrida)"), T("Goccia", "Teardrop", "Lágrima"), None),
    (T("Peso", "Weight", "Peso"), "355–375 g", "355–375 g", False),
    (T("Bilanciamento", "Balance", "Balance"), T("Medio (circa 260 mm)", "Medium (about 260 mm)", "Medio (unos 260 mm)"), T("Medio", "Medium", "Medio"), False),
    (T("Nucleo", "Core", "Núcleo"), T("EVA a densità media", "Medium-density EVA", "EVA de densidad media"), "EVA Mid", False),
    (T("Faccia", "Face", "Cara"), T("Carbonio 18K TeXtreme (in un'altra sezione della stessa scheda: 24K)", "18K TeXtreme carbon (another section of the same listing says 24K)",
                                    "Carbono 18K TeXtreme (en otra sección de la misma ficha: 24K)"), T("Carbonio 3K SC Balance", "3K SC Balance carbon", "Carbono 3K SC Balance"), True),
    (T("Superficie", "Surface", "Superficie"), T("Ruvida 3D, finitura opaca", "Rough 3D, matte finish", "Rugosa 3D, acabado mate"),
     T("Texture 3D con finitura Soft Sand", "3D texture with Soft Sand finish", "Textura 3D con acabado Soft Sand"), True),
    (T("Telaio", "Frame", "Marco"), T("100% carbonio", "100% carbon", "100% carbono"), T("Fibra di carbonio", "Carbon fibre", "Fibra de carbono"), False),
    (T("Spessore", "Thickness", "Grosor"), "38 mm", ND, None),
    (T("Durezza / tatto dichiarati", "Declared hardness / feel", "Dureza / tacto declarados"), "7/10", "7/10", False),
    (T("Livello", "Level", "Nivel"), T("Avanzato / professionale", "Advanced / professional", "Avanzado / profesional"),
     T("Avanzato / professionale", "Advanced / professional", "Avanzado / profesional"), False),
    (T("Prezzo di listino", "List price", "Precio de lista"), "350,00 €", "359,95 €", True),
]


def diablo(db):
    slug = "siux-diablo-pro-2026-vs-2027-cosa-cambia"
    per = {n["slug"]: n for n in db}
    a, b = per.get("siux-diablo-pro-2026"), per.get("siux-diablo-pro-2027")
    righe = "".join(
        f'<tr><td>{e(g(v))}</td><td>{e(g(x))}</td><td>{e(g(y))}</td><td>{L("Sì", "Yes", "Sí") if c else (L("No", "No", "No") if c is False else L("Da verificare", "To be confirmed", "Por confirmar"))}</td></tr>'
        for v, x, y, c in DIABLO)
    tab = (f'<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{url_r(a)}">Diablo Pro 2026</a></th><th><a href="{url_r(b)}">Diablo Pro 2027</a></th>'
           f'<th>{L("Cambia?", "Changes?", "¿Cambia?")}</th></tr></thead><tbody>{righe}</tbody></table></div>')
    fonti = L(f'<p class="note">Dati 2026: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. Dati 2027: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "pagina collezione")}). Schede consultate a ottobre 2026.</p>',
              f'<p class="note">2026 data: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. 2027 data: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "collection page")}). Listings consulted in October 2026.</p>',
              f'<p class="note">Datos 2026: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. Datos 2027: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "página de la colección")}). Fichas consultadas en octubre de 2026.</p>')
    gloss = P("glossario", "carbonio-3k-12k-18k")
    cmp_url = confronto_url(a["slug"], b["slug"])
    corpo = L(
        f"""<p><b>Sulla carta la Siux Diablo Pro 2027 cambia soprattutto la faccia: passa dal carbonio 18K TeXtreme della 2026 al carbonio 3K SC Balance, con una nuova finitura Soft Sand.</b> Peso (355–375 g), bilanciamento medio, nucleo in EVA a media densità e durezza dichiarata 7/10 restano gli stessi. La 2026 si trova scontata: a ottobre 2026 Padel Market la vendeva a 229,95 € invece di 350 €.</p>
<h2>La scheda a confronto</h2>{tab}{fonti}
<h2>Cosa cambia davvero</h2>
<p><b>La faccia.</b> È l'unica differenza tecnica dichiarata. Il numero K indica quanti filamenti compongono ogni fascio di carbonio: cambia la trama e la sensazione, ma da solo non dice se la racchetta è più rigida o più potente (<a href="{gloss}">vedi il glossario</a>). Per sapere come cambia in campo servono test indipendenti sulla 2027, che non sono ancora pubblicati.</p>
<p><b>La superficie.</b> La 2027 aggiunge alla texture 3D una finitura Soft Sand. I rivenditori la presentano come pensata per l'effetto, ma non ci sono misure di spin.</p>
<p><b>La forma.</b> Le fonti non sono d'accordo sulla 2026: Padel Market la indica a goccia, Racketguide e PadelSpeed come ibrida. La 2027 è indicata a goccia. Finché il produttore non pubblica le misure, non si può dire se lo stampo sia cambiato.</p>
<h2>Cosa dicono di chi l'ha usata (2026)</h2>
<p>Per la 2026 PadelSpeed parla di una racchetta più ferma della versione 2025, con risposta più secca e meno rimbalzo. Su Racketguide la media delle recensioni degli utenti è 3,5 su 5 (8 recensioni): piacciono solidità, maneggevolezza e controllo; un giocatore avanzato la trova poco potente quando serve, un altro troppo morbida. Per la 2027 non ci sono ancora recensioni indipendenti.</p>
<h2>Quale scegliere</h2>
<ul><li><b>Scegli la 2026</b> se la trovi scontata: dati dichiarati quasi identici e oltre 100 € di differenza sul prezzo di listino.</li><li><b>Scegli la 2027</b> se vuoi la nuova faccia in carbonio 3K e la finitura Soft Sand, o se la 2026 non si trova più nella tua misura e colore.</li><li><b>Aspetta</b> se per te contano spin e potenza: i primi test indipendenti sulla 2027 diranno se la nuova faccia cambia qualcosa in campo.</li></ul>
<p><a class="btn" href="{cmp_url}">Confronto completo con gli altri dati del database</a></p>""",
        f"""<p><b>On paper, the Siux Diablo Pro 2027 mainly changes the face: it moves from the 2026's 18K TeXtreme carbon to 3K SC Balance carbon, with a new Soft Sand finish.</b> Weight (355–375 g), medium balance, medium-density EVA core and the declared 7/10 hardness stay the same. The 2026 can be found discounted: in October 2026 Padel Market was selling it for €229.95 instead of €350.</p>
<h2>Spec sheet comparison</h2>{tab}{fonti}
<h2>What really changes</h2>
<p><b>The face.</b> It is the only declared technical difference. The K number indicates how many filaments make up each carbon tow: it changes the weave and the feel, but on its own it doesn't tell you whether a racket is stiffer or more powerful (<a href="{gloss}">see the glossary</a>). To know how it changes on court we need independent tests of the 2027, which have not been published yet.</p>
<p><b>The surface.</b> The 2027 adds a Soft Sand finish to the 3D texture. Retailers present it as designed for spin, but there are no spin measurements.</p>
<p><b>The shape.</b> Sources disagree on the 2026: Padel Market lists it as teardrop, Racketguide and PadelSpeed as hybrid. The 2027 is listed as teardrop. Until the manufacturer publishes measurements, we can't say whether the mould has changed.</p>
<h2>What users say (2026)</h2>
<p>For the 2026, PadelSpeed describes a firmer racket than the 2025 version, with a crisper response and less rebound. On Racketguide the average user rating is 3.5 out of 5 (8 reviews): users like its solidity, manoeuvrability and control; one advanced player finds it short of power when needed, another finds it too soft. There are no independent reviews of the 2027 yet.</p>
<h2>Which to choose</h2>
<ul><li><b>Choose the 2026</b> if you find it discounted: almost identical declared specs and more than €100 difference in list price.</li><li><b>Choose the 2027</b> if you want the new 3K carbon face and Soft Sand finish, or if the 2026 is no longer available in your size and colour.</li><li><b>Wait</b> if spin and power matter to you: the first independent tests of the 2027 will show whether the new face changes anything on court.</li></ul>
<p><a class="btn" href="{cmp_url}">Full comparison with the other data in the database</a></p>""",
        f"""<p><b>Sobre el papel, la Siux Diablo Pro 2027 cambia sobre todo la cara: pasa del carbono 18K TeXtreme de la 2026 al carbono 3K SC Balance, con un nuevo acabado Soft Sand.</b> El peso (355–375 g), el balance medio, el núcleo de EVA de densidad media y la dureza declarada 7/10 se mantienen. La 2026 se encuentra rebajada: en octubre de 2026 Padel Market la vendía a 229,95 € en lugar de 350 €.</p>
<h2>Las fichas comparadas</h2>{tab}{fonti}
<h2>Qué cambia realmente</h2>
<p><b>La cara.</b> Es la única diferencia técnica declarada. El número K indica cuántos filamentos forman cada haz de carbono: cambia la trama y la sensación, pero por sí solo no dice si la pala es más rígida o más potente (<a href="{gloss}">mira el glosario</a>). Para saber cómo cambia en pista hacen falta pruebas independientes de la 2027, que todavía no se han publicado.</p>
<p><b>La superficie.</b> La 2027 añade a la textura 3D un acabado Soft Sand. Las tiendas lo presentan como pensado para el efecto, pero no hay mediciones de spin.</p>
<p><b>La forma.</b> Las fuentes no coinciden sobre la 2026: Padel Market la indica de lágrima, Racketguide y PadelSpeed como híbrida. La 2027 se indica de lágrima. Hasta que el fabricante publique las medidas, no se puede decir si el molde ha cambiado.</p>
<h2>Qué dicen quienes la han usado (2026)</h2>
<p>Sobre la 2026, PadelSpeed habla de una pala más firme que la versión 2025, con respuesta más seca y menos rebote. En Racketguide la media de las reseñas de usuarios es 3,5 sobre 5 (8 reseñas): gustan la solidez, la manejabilidad y el control; un jugador avanzado la encuentra poco potente cuando hace falta, otro demasiado blanda. De la 2027 todavía no hay reseñas independientes.</p>
<h2>Cuál elegir</h2>
<ul><li><b>Elige la 2026</b> si la encuentras rebajada: datos declarados casi idénticos y más de 100 € de diferencia en el precio de lista.</li><li><b>Elige la 2027</b> si quieres la nueva cara de carbono 3K y el acabado Soft Sand, o si la 2026 ya no está disponible en tu talla y color.</li><li><b>Espera</b> si para ti cuentan el efecto y la potencia: las primeras pruebas independientes de la 2027 dirán si la nueva cara cambia algo en pista.</li></ul>
<p><a class="btn" href="{cmp_url}">Comparativa completa con los demás datos de la base</a></p>""")
    qa = [(L("Qual è la differenza tra Siux Diablo Pro 2026 e 2027?", "What is the difference between the Siux Diablo Pro 2026 and 2027?", "¿Qué diferencia hay entre la Siux Diablo Pro 2026 y la 2027?"),
           L("Secondo le schede dei rivenditori cambia la faccia (da carbonio 18K TeXtreme a carbonio 3K SC Balance) e la finitura della superficie, che aggiunge il Soft Sand. Peso, bilanciamento, nucleo e durezza dichiarata restano uguali.",
             "According to retailer listings, the face changes (from 18K TeXtreme carbon to 3K SC Balance carbon), as does the surface finish, which adds Soft Sand. Weight, balance, core and declared hardness stay the same.",
             "Según las fichas de las tiendas cambia la cara (de carbono 18K TeXtreme a carbono 3K SC Balance) y el acabado de la superficie, que añade el Soft Sand. Peso, balance, núcleo y dureza declarada se mantienen.")),
          (L("Quanto pesa la Siux Diablo Pro 2027?", "How much does the Siux Diablo Pro 2027 weigh?", "¿Cuánto pesa la Siux Diablo Pro 2027?"),
           L("Il peso dichiarato è 355–375 g, uguale alla versione 2026.", "The declared weight is 355–375 g, the same as the 2026 version.", "El peso declarado es 355–375 g, igual que la versión 2026.")),
          (L("La Siux Diablo Pro è adatta ai principianti?", "Is the Siux Diablo Pro suitable for beginners?", "¿La Siux Diablo Pro es adecuada para principiantes?"),
           L("No: entrambe le versioni sono indicate per livello avanzato o professionale e richiedono una buona tecnica.",
             "No: both versions are aimed at advanced or professional players and require good technique.",
             "No: ambas versiones están indicadas para nivel avanzado o profesional y requieren buena técnica."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("Siux Diablo Pro 2026 vs 2027: cosa cambia davvero", "Siux Diablo Pro 2026 vs 2027: what really changes", "Siux Diablo Pro 2026 vs 2027: qué cambia realmente")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Siux Diablo Pro 2026 e 2027 (Tino Libaak) a confronto: faccia, superficie, peso, bilanciamento, prezzo e quale conviene comprare. Dati con fonti.",
                      "Siux Diablo Pro 2026 and 2027 (Tino Libaak) compared: face, surface, weight, balance, price and which one to buy. Data with sources.",
                      "Siux Diablo Pro 2026 y 2027 (Tino Libaak) comparadas: cara, superficie, peso, balance, precio y cuál conviene comprar. Datos con fuentes."),
                    titolo, "Diablo Pro 2026 vs 2027", corpo + faq_htm, items=[a, b], ld_extra=[faq_ld])
    return slug, titolo, L("La 2027 cambia la faccia e la finitura; il resto della scheda è uguale.", "The 2027 changes the face and the finish; the rest of the spec sheet is the same.",
                           "La 2027 cambia la cara y el acabado; el resto de la ficha es igual.")


# ---------------------------------------------------------------- Indice

def indice(arts):
    path, alt = P("articoli"), ALT("articoli")
    cr, ld = crumbs([H(), (L("Articoli", "Articles", "Artículos"), None)])
    lista = "".join(f'<li><a href="{P("articoli", s)}"><b>{e(t)}</b></a><br><span class="note">{e(d)}</span></li>' for s, t, d in arts)
    corpo = f'''{cr}
<div class="intro"><h1>{L("Articoli", "Articles", "Artículos")}</h1><p>{L(
        "Novità, confronti tra versioni e approfondimenti sulle racchette da padel, con i dati del database PadelMetrix e le fonti citate.",
        "New releases, comparisons between versions and in-depth articles on padel rackets, with data from the PadelMetrix database and cited sources.",
        "Novedades, comparativas entre versiones y artículos en profundidad sobre palas de pádel, con los datos de la base de PadelMetrix y las fuentes citadas.")}</p></div>
<div class="prose"><ul class="clean lista-art">{lista}</ul></div>'''
    S.scrivi(path, pagina(L("Articoli sulle racchette da padel | PadelMetrix", "Padel racket articles | PadelMetrix", "Artículos sobre palas de pádel | PadelMetrix"),
                          L("Novità 2027, confronti tra versioni e approfondimenti sulle racchette da padel, con dati e fonti.",
                            "2027 releases, comparisons between versions and in-depth articles on padel rackets, with data and sources.",
                            "Novedades 2027, comparativas entre versiones y artículos sobre palas de pádel, con datos y fuentes."),
                          path, corpo, on="articoli", ld=[ld], alt=alt), alt)


def main():
    db = carica()
    for l in LINGUE:
        set_lang(l)
        arts = [novita_2027(db), diablo(db)]
        indice(arts)
    set_lang("it")
    (ROOT / "scripts" / "pagine_articoli.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine articoli generate")


if __name__ == "__main__":
    main()
