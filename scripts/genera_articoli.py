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
DATE_ART = {"regolamento-padel-regole-spiegate": "2026-11-01", "regolamento-pickleball-regole-spiegate": "2026-11-01", "racchette-padel-2027-vs-2026-cosa-cambia": "2026-10-31", "migliori-racchette-padel-2026-classifiche-indipendenti": "2026-10-31"}


def T(it, en, es, fr=None):
    return {"it": it, "en": en, "es": es, "fr": fr if fr is not None else en}


def g(d):
    return d[S.lang()] if isinstance(d, dict) else d


def H():
    return S.home_crumb()


def fonte(u, nome=None):
    nome = nome or urlparse(u).netloc.replace("www.", "")
    return f'<a href="{e(u)}" rel="nofollow noopener" target="_blank">{e(nome)}</a>'


def articolo_ld(titolo, desc, path, data=OGGI_ISO):
    return {"@context": "https://schema.org", "@type": "Article", "headline": titolo, "description": desc,
            "inLanguage": S.lang(), "datePublished": data, "dateModified": data,
            "author": S.autore(), "publisher": S.editore(), "mainEntityOfPage": SITO + path}


def scrivi_articolo(slug, title, desc, h1, crumb, corpo_html, items=None, ld_extra=()):
    path, alt = P("articoli", slug), ALT("articoli", slug)
    cr, ld = crumbs([H(), (L("Articoli", "Articles", "Artículos", "Articles"), P("articoli")), (crumb, None)])
    lista = (f'<section class="block"><h2>{L("Le racchette citate", "Rackets mentioned", "Las palas citadas", "Raquettes citées")} ({len(items)})</h2>{griglia(ordina(items))}</section>'
             if items else "")
    corpo = f'''{cr}
<div class="intro"><div class="eyebrow">{L("Articolo", "Article", "Artículo", "Article")}</div><h1>{e(h1)}</h1><p class="note">{L("Pubblicato il ", "Published on ", "Publicado el ", "Publié le ")}{S.data_txt(DATE_ART.get(slug, OGGI_ISO))} · {L("a cura di", "by", "por", "par")} <a href="{P("chi-siamo")}">Luca Bicchieri, PadelMetrix</a></p></div>
<div class="prose">{corpo_html}<p class="note" style="margin:28px 0 56px">{L("Ti è stato utile? Seguici per i prossimi confronti:", "Found this useful? Follow us for the next comparisons:", "¿Te ha sido útil? Síguenos para las próximas comparativas:", "Cet article vous a été utile ? Suivez-nous pour les prochains comparatifs :")} {S.social_links()}</p></div>
{lista}'''
    S.scrivi(path, pagina(title, desc, path, corpo, on="articoli", ld=[ld, articolo_ld(h1, desc, path, DATE_ART.get(slug, OGGI_ISO)), *ld_extra], alt=alt), alt)


def faq(qa):
    htm = f'<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes", "Questions fréquentes")}</h2><div class="faq">' + "".join(
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
            rif = f'<a href="{confronto_url(old["slug"], n["slug"])}">{L("vs 2026", "vs 2026", "vs 2026", "vs 2026")}</a>'
        celle = [f'<a href="{url_r(n)}">{e(n["nome"])}</a>', e((S.tr(n["giocatore"]) if "ispirata" in n["giocatore"] else n["giocatore"]) if n["giocatore"] else "—"), e(FORMA(n["forma"]) or L("n.d.", "n/a", "n.d.", "n.c.")),
                 e(n["peso"] or L("n.d.", "n/a", "n.d.", "n.c.")), e(LIVN(n["livello"]) or L("n.d.", "n/a", "n.d.", "n.c.")),
                 euro(n["prezzo"]) if n["prezzo"] else L("n.d.", "n/a", "n.d.", "n.c."), rif]
        return "<tr>" + "".join(f"<td>{c}</td>" for c in celle) + "</tr>"

    th = [L("Modello", "Model", "Modelo", "Modèle"), L("Giocatore", "Player", "Jugador", "Joueur"), L("Forma", "Shape", "Forma", "Forme"), L("Peso", "Weight", "Peso", "Poids"),
          L("Livello", "Level", "Nivel", "Niveau"), L("Listino", "List price", "Precio", "Prix catalogue"), L("Confronto", "Comparison", "Comparativa", "Comparatif")]
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
                   f"<b>{len(items)} modelos 2027</b> en nuestra base de datos", f"<b>{len(items)} modèles 2027</b> dans notre base")]
        if pz:
            frasi.append(L(f"listino da {euro(min(pz))} a {euro(max(pz))}", f"list prices from {euro(min(pz))} to {euro(max(pz))}",
                           f"precio de lista de {euro(min(pz))} a {euro(max(pz))}", f"prix catalogue de {euro(min(pz))} à {euro(max(pz))}"))
        if fm:
            fm_txt = ", ".join(f"{FORMA(k).lower()} {v}" for k, v in fm.most_common())
            frasi.append(L(f"forme: {fm_txt}", f"shapes: {fm_txt}", f"formas: {fm_txt}", f"formes : {fm_txt}"))
        if rinnovi:
            frasi.append(L(f"{rinnovi} sono il rinnovo di un modello 2026", f"{rinnovi} replace a 2026 model", f"{rinnovi} renuevan un modelo 2026", f"{rinnovi} remplacent un modèle 2026"))
        gtxt = ""
        if gioc:
            gtxt = L(f" Modelli firmati: {', '.join(gioc)}.", f" Signature models: {', '.join(gioc)}.", f" Modelos firmados: {', '.join(gioc)}.", f" Modèles signature : {', '.join(gioc)}.")
        ancora = S.slugify(m)
        indice.append(f'<a href="#{ancora}">{e(m)} ({len(items)})</a>')
        sezioni.append(f'''<h2 id="{ancora}">{e(m)}</h2>
<p>{"; ".join(frasi)}.{gtxt}</p>
<div class="tablebox"><table class="tab"><thead><tr>{"".join(f"<th>{t}</th>" for t in th)}</tr></thead><tbody>{"".join(riga(n) for n in items)}</tbody></table></div>
<p class="note">{L("Fonti dei dati", "Data sources", "Fuentes de los datos", "Sources des données")}: {", ".join(fonte(u) for u in fonti[:6])}{" …" if len(fonti) > 6 else ""}.</p>''')

    qa = [(L("Quali marchi hanno già presentato le racchette 2027?", "Which brands have already launched their 2027 rackets?", "¿Qué marcas ya han presentado sus palas 2027?", "Quelles marques ont déjà lancé leurs raquettes 2027 ?"),
           L(f"Nel database PadelMetrix al {S.data_txt(OGGI_ISO)} ci sono modelli 2027 di {', '.join(marche)}. Gli altri marchi verranno aggiunti appena pubblicano le collezioni con dati verificabili.",
             f"As of {S.data_txt(OGGI_ISO)}, the PadelMetrix database includes 2027 models from {', '.join(marche)}. Other brands will be added as soon as they publish their collections with verifiable data.",
             f"A {S.data_txt(OGGI_ISO)}, la base de datos de PadelMetrix incluye modelos 2027 de {', '.join(marche)}. Las demás marcas se añadirán en cuanto publiquen sus colecciones con datos verificables.", f"Au {S.data_txt(OGGI_ISO)}, la base PadelMetrix comprend des modèles 2027 de {', '.join(marche)}. Les autres marques seront ajoutées dès qu'elles publieront leurs collections avec des données vérifiables.")),
          (L("Quanto costano le racchette da padel 2027?", "How much do 2027 padel rackets cost?", "¿Cuánto cuestan las palas de pádel 2027?", "Combien coûtent les raquettes de padel 2027 ?"),
           L(f"Tra i modelli con prezzo dichiarato il listino va da {euro(min(prezzi))} a {euro(max(prezzi))}. I prezzi reali nei negozi cambiano spesso e i modelli 2026 si trovano scontati.",
             f"Among models with a declared price, list prices range from {euro(min(prezzi))} to {euro(max(prezzi))}. Real shop prices change often and 2026 models can be found discounted.",
             f"Entre los modelos con precio declarado, el precio de lista va de {euro(min(prezzi))} a {euro(max(prezzi))}. Los precios reales cambian a menudo y los modelos 2026 se encuentran rebajados.", f"Parmi les modèles au prix déclaré, les prix catalogue vont de {euro(min(prezzi))} à {euro(max(prezzi))}. Les prix réels en boutique changent souvent et les modèles 2026 se trouvent en promotion.")) if prezzi else None,
          (L("Conviene comprare il modello 2027 o il 2026 scontato?", "Should I buy the 2027 model or the discounted 2026?", "¿Conviene comprar el modelo 2027 o el 2026 rebajado?", "Vaut-il mieux acheter le modèle 2027 ou le 2026 en promotion ?"),
           L("Dipende da quanto cambia davvero: in molti casi le schede tecniche sono quasi uguali e il 2026 costa meno. Per ogni rinnovo trovi il link al confronto tra le due versioni.",
             "It depends on how much really changes: in many cases the spec sheets are almost identical and the 2026 costs less. For each update there is a link to the comparison between the two versions.",
             "Depende de cuánto cambie realmente: en muchos casos las fichas técnicas son casi iguales y el 2026 cuesta menos. Para cada renovación tienes el enlace a la comparativa entre las dos versiones.", "Cela dépend de ce qui change vraiment : dans beaucoup de cas les fiches techniques sont presque identiques et le 2026 coûte moins cher. Pour chaque mise à jour, un lien mène au comparatif entre les deux versions."))]
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
        + "Abajo tienes las novedades marca por marca, con los datos declarados por fabricantes y tiendas y el enlace a la comparativa con el modelo 2026 cuando existe.</p>", f"<p><b>Les collections 2027 sont arrivées en boutique : la base PadelMetrix recense déjà {len(nuove)} raquettes 2027 de {len(marche)} marques.</b> "
        + (f"La forme la plus répandue est la forme {FORMA(forma_top).lower()} ({forma_n} modèles) et les prix catalogue vont de {euro(min(prezzi))} à {euro(max(prezzi))}. " if prezzi and forma_top else "")
        + "Voici les nouveaux modèles marque par marque, avec les données déclarées par les fabricants et les revendeurs et un lien vers le comparatif avec le modèle 2026 quand il existe.</p>")
    metodo = L(
        f'<p class="note">Come leggere i dati: "n.d." significa che il dato non è pubblicato dalle fonti consultate. Le valutazioni indipendenti dei modelli 2027 sono ancora poche: quando escono le aggiungiamo alle schede. Vedi anche <a href="{P("report", "racchette-padel-2026-2027-in-numeri")}">le racchette 2026 e 2027 in numeri</a>.</p>',
        f'<p class="note">How to read the data: "n/a" means the figure is not published by the sources we consulted. Independent reviews of 2027 models are still few: we add them to the spec pages as they come out. See also <a href="{P("report", "racchette-padel-2026-2027-in-numeri")}">2026 and 2027 rackets in numbers</a>.</p>',
        f'<p class="note">Cómo leer los datos: "n.d." significa que el dato no lo publican las fuentes consultadas. Las valoraciones independientes de los modelos 2027 todavía son pocas: las añadimos a las fichas cuando salen. Mira también <a href="{P("report", "racchette-padel-2026-2027-in-numeri")}">las palas 2026 y 2027 en cifras</a>.</p>', f'<p class="note">Comment lire les données : « n.c. » signifie que la donnée n\'est pas publiée par les sources consultées. Les tests indépendants des modèles 2027 sont encore rares : nous les ajoutons aux fiches au fur et à mesure de leur parution. Voir aussi <a href="{P("report", "racchette-padel-2026-2027-in-numeri")}">les raquettes 2026 et 2027 en chiffres</a>.</p>')
    corpo = intro + f'<div class="marche">{"".join(indice)}</div>' + metodo + "".join(sezioni) + faq_htm
    titolo = L("Racchette padel 2027: tutte le novità per marca", "Padel rackets 2027: what's new from every brand", "Palas de pádel 2027: todas las novedades por marca", "Raquettes de padel 2027 : les nouveautés de chaque marque")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L(f"Le racchette da padel 2027 di {', '.join(marche[:4])} e altri: {len(nuove)} modelli con forma, peso, giocatore, prezzo di listino e confronto con il 2026.",
                      f"2027 padel rackets from {', '.join(marche[:4])} and more: {len(nuove)} models with shape, weight, player, list price and comparison with 2026.",
                      f"Las palas de pádel 2027 de {', '.join(marche[:4])} y otras: {len(nuove)} modelos con forma, peso, jugador, precio de lista y comparativa con 2026.", f"Raquettes de padel 2027 de {', '.join(marche[:4])} et d'autres : {len(nuove)} modèles avec forme, poids, joueur, prix catalogue et comparatif avec le 2026."),
                    titolo, L("Novità 2027", "What's new in 2027", "Novedades 2027", "Les nouveautés 2027"), corpo, ld_extra=[faq_ld])
    return slug, titolo, L(f"{len(nuove)} modelli 2027 di {len(marche)} marchi, con dati e confronti.", f"{len(nuove)} 2027 models from {len(marche)} brands, with data and comparisons.",
                           f"{len(nuove)} modelos 2027 de {len(marche)} marcas, con datos y comparativas.", f"{len(nuove)} modèles 2027 de {len(marche)} marques, avec données et comparatifs.")


# ---------------------------------------------------------------- 2. Siux Diablo Pro 2026 vs 2027

F_PM = "https://padelmarket.com/it-eu/products/siux-diablo-pro-2026-night-blue-pala"
F_RG = "https://www.racketguide.com/gb-en/padel/siux/diablo-pro-night-blue-2026/"
F_PS = "https://padelspeed.com/blogs/news/siux-2026-padel-rackets-in-depth-review"
F_PP = "https://padelproshop.com/en-dk/products/siux-padel-racket-diablo-pro-metallic-blue-2027-tino-libaak"
F_PP2 = "https://padelproshop.com/pages/siux-2027"

ND = T("Non dichiarato", "Not stated", "No declarado", "Non communiqué")

DIABLO = [  # (voce, 2026, 2027, cambia?)
    (T("Giocatore", "Player", "Jugador", "Joueur"), "Tino Libaak", "Tino Libaak", False),
    (T("Forma", "Shape", "Forma", "Forme"), T("Goccia secondo Padel Market (Racketguide e PadelSpeed: ibrida)", "Teardrop according to Padel Market (Racketguide and PadelSpeed: hybrid)",
                                     "Lágrima según Padel Market (Racketguide y PadelSpeed: híbrida)", "Goutte d'eau selon Padel Market (Racketguide et PadelSpeed : hybride)"), T("Goccia", "Teardrop", "Lágrima", "Goutte d'eau"), None),
    (T("Peso", "Weight", "Peso", "Poids"), "355–375 g", "355–375 g", False),
    (T("Bilanciamento", "Balance", "Balance", "Équilibre"), T("Medio (circa 260 mm)", "Medium (about 260 mm)", "Medio (unos 260 mm)", "Moyen (environ 260 mm)"), T("Medio", "Medium", "Medio", "Moyen"), False),
    (T("Nucleo", "Core", "Núcleo", "Noyau"), T("EVA a densità media", "Medium-density EVA", "EVA de densidad media", "EVA de densité moyenne"), "EVA Mid", False),
    (T("Faccia", "Face", "Cara", "Tamis"), T("Carbonio 18K TeXtreme (in un'altra sezione della stessa scheda: 24K)", "18K TeXtreme carbon (another section of the same listing says 24K)",
                                    "Carbono 18K TeXtreme (en otra sección de la misma ficha: 24K)", "Carbone 18K TeXtreme (une autre partie de la même fiche indique 24K)"), T("Carbonio 3K SC Balance", "3K SC Balance carbon", "Carbono 3K SC Balance", "Carbone 3K SC Balance"), True),
    (T("Superficie", "Surface", "Superficie", "Surface"), T("Ruvida 3D, finitura opaca", "Rough 3D, matte finish", "Rugosa 3D, acabado mate", "Rugueuse 3D, finition mate"),
     T("Texture 3D con finitura Soft Sand", "3D texture with Soft Sand finish", "Textura 3D con acabado Soft Sand", "Texture 3D avec finition Soft Sand"), True),
    (T("Telaio", "Frame", "Marco", "Cadre"), T("100% carbonio", "100% carbon", "100% carbono", "100 % carbone"), T("Fibra di carbonio", "Carbon fibre", "Fibra de carbono", "Fibre de carbone"), False),
    (T("Spessore", "Thickness", "Grosor", "Épaisseur"), "38 mm", ND, None),
    (T("Durezza / tatto dichiarati", "Declared hardness / feel", "Dureza / tacto declarados", "Dureté / toucher déclaré"), "7/10", "7/10", False),
    (T("Livello", "Level", "Nivel", "Niveau"), T("Avanzato / professionale", "Advanced / professional", "Avanzado / profesional", "Avancé / professionnel"),
     T("Avanzato / professionale", "Advanced / professional", "Avanzado / profesional", "Avancé / professionnel"), False),
    (T("Prezzo di listino", "List price", "Precio de lista", "Prix catalogue"), "350,00 €", "359,95 €", True),
]


def diablo(db):
    slug = "siux-diablo-pro-2026-vs-2027-cosa-cambia"
    per = {n["slug"]: n for n in db}
    a, b = per.get("siux-diablo-pro-2026"), per.get("siux-diablo-pro-2027")
    righe = "".join(
        f'<tr><td>{e(g(v))}</td><td>{e(g(x))}</td><td>{e(g(y))}</td><td>{L("Sì", "Yes", "Sí", "Oui") if c else (L("No", "No", "No", "Non") if c is False else L("Da verificare", "To be confirmed", "Por confirmar", "À confirmer"))}</td></tr>'
        for v, x, y, c in DIABLO)
    tab = (f'<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{url_r(a)}">Diablo Pro 2026</a></th><th><a href="{url_r(b)}">Diablo Pro 2027</a></th>'
           f'<th>{L("Cambia?", "Changes?", "¿Cambia?", "Ça change ?")}</th></tr></thead><tbody>{righe}</tbody></table></div>')
    fonti = L(f'<p class="note">Dati 2026: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. Dati 2027: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "pagina collezione")}). Schede consultate a ottobre 2026.</p>',
              f'<p class="note">2026 data: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. 2027 data: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "collection page")}). Listings consulted in October 2026.</p>',
              f'<p class="note">Datos 2026: {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. Datos 2027: {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "página de la colección")}). Fichas consultadas en octubre de 2026.</p>', f'<p class="note">Données 2026 : {fonte(F_PM, "Padel Market")}, {fonte(F_RG, "Racketguide")}, {fonte(F_PS, "PadelSpeed")}. Données 2027 : {fonte(F_PP, "PadelPROShop")} ({fonte(F_PP2, "page de la collection")}). Fiches consultées en octobre 2026.</p>')
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
<p><a class="btn" href="{cmp_url}">Comparativa completa con los demás datos de la base</a></p>""", f"""<p><b>Sur le papier, la Siux Diablo Pro 2027 change surtout le tamis : elle passe du carbone 18K TeXtreme du 2026 au carbone 3K SC Balance, avec une nouvelle finition Soft Sand.</b> Poids (355–375 g), équilibre moyen, noyau EVA de densité moyenne et dureté déclarée de 7/10 restent identiques. Le 2026 se trouve en promotion : en octobre 2026, Padel Market le vendait 229,95 € au lieu de 350 €.</p>
<h2>Comparaison des fiches techniques</h2>{tab}{fonti}
<h2>Ce qui change vraiment</h2>
<p><b>Le tamis.</b> C'est la seule différence technique déclarée. Le chiffre K indique combien de filaments composent chaque mèche de carbone : il change le tissage et le toucher, mais à lui seul il ne dit pas si une raquette est plus rigide ou plus puissante (<a href="{gloss}">voir le glossaire</a>). Pour savoir ce que cela change sur le terrain, il faut des tests indépendants du 2027, qui n'ont pas encore été publiés.</p>
<p><b>La surface.</b> Le 2027 ajoute une finition Soft Sand à la texture 3D. Les revendeurs la présentent comme conçue pour l'effet, mais il n'existe pas de mesures d'effet.</p>
<p><b>La forme.</b> Les sources divergent sur le 2026 : Padel Market l'indique en goutte d'eau, Racketguide et PadelSpeed en hybride. Le 2027 est indiqué en goutte d'eau. Tant que le fabricant ne publie pas de mesures, nous ne pouvons pas dire si le moule a changé.</p>
<h2>Ce qu'en disent les utilisateurs (2026)</h2>
<p>Pour le 2026, PadelSpeed décrit une raquette plus ferme que la version 2025, avec une réponse plus sèche et moins de rebond. Sur Racketguide, la note moyenne des utilisateurs est de 3,5 sur 5 (8 avis) : ils apprécient sa solidité, sa maniabilité et son contrôle ; un joueur avancé la trouve en manque de puissance quand il le faut, un autre la trouve trop souple. Il n'existe pas encore de tests indépendants du 2027.</p>
<h2>Laquelle choisir</h2>
<ul><li><b>Choisissez le 2026</b> si vous le trouvez en promotion : fiches déclarées presque identiques et plus de 100 € d'écart de prix catalogue.</li><li><b>Choisissez le 2027</b> si vous voulez le nouveau tamis en carbone 3K et la finition Soft Sand, ou si le 2026 n'est plus disponible dans votre taille et votre couleur.</li><li><b>Attendez</b> si l'effet et la puissance comptent pour vous : les premiers tests indépendants du 2027 montreront si le nouveau tamis change quelque chose sur le terrain.</li></ul>
<p><a class="btn" href="{cmp_url}">Comparatif complet avec les autres données de la base</a></p>""")
    qa = [(L("Qual è la differenza tra Siux Diablo Pro 2026 e 2027?", "What is the difference between the Siux Diablo Pro 2026 and 2027?", "¿Qué diferencia hay entre la Siux Diablo Pro 2026 y la 2027?", "Quelle est la différence entre la Siux Diablo Pro 2026 et 2027 ?"),
           L("Secondo le schede dei rivenditori cambia la faccia (da carbonio 18K TeXtreme a carbonio 3K SC Balance) e la finitura della superficie, che aggiunge il Soft Sand. Peso, bilanciamento, nucleo e durezza dichiarata restano uguali.",
             "According to retailer listings, the face changes (from 18K TeXtreme carbon to 3K SC Balance carbon), as does the surface finish, which adds Soft Sand. Weight, balance, core and declared hardness stay the same.",
             "Según las fichas de las tiendas cambia la cara (de carbono 18K TeXtreme a carbono 3K SC Balance) y el acabado de la superficie, que añade el Soft Sand. Peso, balance, núcleo y dureza declarada se mantienen.", "D'après les fiches des revendeurs, le tamis change (du carbone 18K TeXtreme au carbone 3K SC Balance), tout comme la finition de surface, qui ajoute le Soft Sand. Poids, équilibre, noyau et dureté déclarée restent identiques.")),
          (L("Quanto pesa la Siux Diablo Pro 2027?", "How much does the Siux Diablo Pro 2027 weigh?", "¿Cuánto pesa la Siux Diablo Pro 2027?", "Combien pèse la Siux Diablo Pro 2027 ?"),
           L("Il peso dichiarato è 355–375 g, uguale alla versione 2026.", "The declared weight is 355–375 g, the same as the 2026 version.", "El peso declarado es 355–375 g, igual que la versión 2026.", "Le poids déclaré est de 355–375 g, comme la version 2026.")),
          (L("La Siux Diablo Pro è adatta ai principianti?", "Is the Siux Diablo Pro suitable for beginners?", "¿La Siux Diablo Pro es adecuada para principiantes?", "La Siux Diablo Pro convient-elle aux débutants ?"),
           L("No: entrambe le versioni sono indicate per livello avanzato o professionale e richiedono una buona tecnica.",
             "No: both versions are aimed at advanced or professional players and require good technique.",
             "No: ambas versiones están indicadas para nivel avanzado o profesional y requieren buena técnica.", "Non : les deux versions s'adressent aux joueurs avancés ou professionnels et demandent une bonne technique."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("Siux Diablo Pro 2026 vs 2027: cosa cambia davvero", "Siux Diablo Pro 2026 vs 2027: what really changes", "Siux Diablo Pro 2026 vs 2027: qué cambia realmente", "Siux Diablo Pro 2026 vs 2027 : ce qui change vraiment")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Siux Diablo Pro 2026 e 2027 (Tino Libaak) a confronto: faccia, superficie, peso, bilanciamento, prezzo e quale conviene comprare. Dati con fonti.",
                      "Siux Diablo Pro 2026 and 2027 (Tino Libaak) compared: face, surface, weight, balance, price and which one to buy. Data with sources.",
                      "Siux Diablo Pro 2026 y 2027 (Tino Libaak) comparadas: cara, superficie, peso, balance, precio y cuál conviene comprar. Datos con fuentes.", "Siux Diablo Pro 2026 et 2027 (Tino Libaak) comparées : tamis, surface, poids, équilibre, prix et laquelle acheter. Données avec sources."),
                    titolo, "Diablo Pro 2026 vs 2027", corpo + faq_htm, items=[a, b], ld_extra=[faq_ld])
    return slug, titolo, L("La 2027 cambia la faccia e la finitura; il resto della scheda è uguale.", "The 2027 changes the face and the finish; the rest of the spec sheet is the same.",
                           "La 2027 cambia la cara y el acabado; el resto de la ficha es igual.", "Le 2027 change le tamis et la finition ; le reste de la fiche est identique.")


# ---------------------------------------------------------------- 3. Ale Galán: chi è e che racchetta usa

G_WIKI = "https://en.wikipedia.org/wiki/Alejandro_Gal%C3%A1n_Romo"
G_WIKI26 = "https://en.wikipedia.org/wiki/Premier_Padel_2026"
G_STUDY = "https://www.studypadel.com/players/alejandro-galan"
G_CHINGO = "https://chingoland.es/premier-padel/top-10-ranking-premier-padel-2026/"
G_IBER = "https://www.padeliberico.es/blog-padeliberico/en/the-rackets-used-by-premier-padel-players-in-2026/"
G_RES = "https://allforpadel.com/en/blog/metalbone-reserve-edt-la-pala-exclusiva-de-ale-galan-para-dominar-el-reserve-n563"
G_PZ_HRD = "https://padelzoom.es/adidas-metalbone-hrd-2026-ale-galan/"
G_PZ = "https://padelzoom.es/adidas-metalbone-2026-ale-galan/"


def galan(db):
    slug = "ale-galan-chi-e-e-che-racchetta-usa"
    per = {n["slug"]: n for n in db}
    hrd, mb = per.get("adidas-metalbone-hrd-plus-2026"), per.get("adidas-metalbone-2026")
    righe_dati = [
        (T("Peso", "Weight", "Peso", "Poids"), "345–360 g (+11,2 g)", "345–360 g (+11,2 g)"),
        (T("Forma", "Shape", "Forma", "Forme"), T("Diamante", "Diamond", "Diamante", "Diamant"), T("Diamante", "Diamond", "Diamante", "Diamant")),
        (T("Gomma", "Core", "Goma", "Noyau"), "EVA High Memory", "EVA Soft Performance"),
        (T("Faccia", "Face", "Cara", "Tamis"), T("Carbonio alluminizzato 16K", "16K aluminised carbon", "Carbono aluminizado 16K", "Carbone aluminisé 16K"),
         T("Carbonio alluminizzato 16K", "16K aluminised carbon", "Carbono aluminizado 16K", "Carbone aluminisé 16K")),
        (T("Tatto", "Feel", "Tacto", "Toucher"), T("Medio-duro", "Medium-hard", "Medio-duro", "Moyen-dur"), T("Medio", "Medium", "Medio", "Moyen")),
        (T("Potenza (PadelZoom)", "Power (PadelZoom)", "Potencia (PadelZoom)", "Puissance (PadelZoom)"), "10/10", "9/10"),
        (T("Controllo (PadelZoom)", "Control (PadelZoom)", "Control (PadelZoom)", "Contrôle (PadelZoom)"), "9,5/10", "8,5/10"),
        (T("Uscita di palla (PadelZoom)", "Ball output (PadelZoom)", "Salida de bola (PadelZoom)", "Sortie de balle (PadelZoom)"), "8/10", "9,5/10"),
        (T("Voto complessivo (PadelZoom)", "Overall score (PadelZoom)", "Nota global (PadelZoom)", "Note globale (PadelZoom)"), "8,7/10", "8,6/10"),
        (T("Prezzo di listino", "List price", "Precio de lista", "Prix catalogue"), "390 €", "390 €"),
    ]
    num = lambda x: x.replace(",", ".") if S.lang() == "en" else x  # noqa: E731
    righe = "".join(f"<tr><td>{e(g(v))}</td><td>{e(num(g(a)))}</td><td>{e(num(g(b)))}</td></tr>" for v, a, b in righe_dati)
    tab = (f'<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{url_r(hrd)}">Metalbone HRD+ 2026</a></th>'
           f'<th><a href="{url_r(mb)}">Metalbone 2026</a></th></tr></thead><tbody>{righe}</tbody></table></div>')
    note_tab = L(f'<p class="note">Dati e punteggi: {fonte(G_PZ_HRD, "PadelZoom (HRD+)")}, {fonte(G_PZ, "PadelZoom (Metalbone)")}. Il peso si può aumentare fino a 11,2 g con il sistema Weight &amp; Balance.</p>',
                 f'<p class="note">Data and scores: {fonte(G_PZ_HRD, "PadelZoom (HRD+)")}, {fonte(G_PZ, "PadelZoom (Metalbone)")}. Weight can be increased by up to 11.2 g with the Weight &amp; Balance system.</p>',
                 f'<p class="note">Datos y puntuaciones: {fonte(G_PZ_HRD, "PadelZoom (HRD+)")}, {fonte(G_PZ, "PadelZoom (Metalbone)")}. El peso se puede aumentar hasta 11,2 g con el sistema Weight &amp; Balance.</p>', f'<p class="note">Données et notes : {fonte(G_PZ_HRD, "PadelZoom (HRD+)")}, {fonte(G_PZ, "PadelZoom (Metalbone)")}. Le poids peut être augmenté jusqu\'à 11,2 g avec le système Weight &amp; Balance.</p>')
    pro_url = P("guide", "racchette-giocatori-professionisti")
    corpo = L(
        f"""<p><b>Alejandro "Ale" Galán Romo è un giocatore di padel spagnolo, nato a Madrid il 15 maggio 1996, che gioca sul lato sinistro (revés). È stato numero 1 del mondo con Juan Lebrón e dal marzo 2024 fa coppia con l'argentino Federico Chingotto. In partita usa la Adidas Metalbone HRD+ 2026, la versione più rigida della sua linea firmata.</b></p>
<h2>Chi è Ale Galán</h2>
<ul><li><b>Nato:</b> 15 maggio 1996 a Madrid; alto 1,86 m.</li><li><b>Lato:</b> sinistro (revés), il lato che di solito chiude il punto con lo smash.</li><li><b>Compagni principali:</b> Juan Lebrón dal 2020 al marzo 2024, poi Federico Chingotto.</li><li><b>Numero 1 del mondo:</b> con Lebrón nel 2020, 2021 e 2022; hanno perso la vetta nel maggio 2023 a favore di Tapia e Coello.</li><li><b>Titoli importanti:</b> tre Master Final del World Padel Tour (2019 con Pablo Lima, 2021 e 2022 con Lebrón) e il Mondiale 2021 con la Spagna.</li></ul>
<p class="note">Fonte: {fonte(G_WIKI, "Wikipedia")}.</p>
<h2>Il 2026 con Chingotto</h2>
<p>Nel 2026 Galán e Chingotto hanno vinto sette tornei Premier Padel: Gijón P2, Miami P1, Giza P2, Asunción P2, Buenos Aires P1 (in finale contro Tapia e Coello), Pretoria P1 e Madrid P1. A fine ottobre Galán è numero 3 del ranking FIP secondo StudyPadel, che gli attribuisce 56 titoli professionali in carriera.</p>
<p class="note">Fonti: {fonte(G_WIKI26, "Wikipedia – Premier Padel 2026")}, {fonte(G_STUDY, "StudyPadel")}, {fonte(G_CHINGO, "Chingoland")}. Classifiche e titoli cambiano di settimana in settimana.</p>
<h2>Che racchetta usa Ale Galán</h2>
<p>Galán è un giocatore Adidas e la linea <b>Metalbone</b> è la sua racchetta firmata. Secondo Chingoland e Padel Ibérico, nel 2026 in partita usa la <b><a href="{url_r(hrd)}">Metalbone HRD+ 2026</a></b>: una diamante con gomma EVA High Memory e faccia in carbonio alluminizzato 16K, la più dura del catalogo Adidas. Accanto c'è la <a href="{url_r(mb)}">Metalbone 2026</a>, stessa forma e stessi materiali della faccia ma con una gomma più morbida.</p>
{tab}{note_tab}
<p>Per PadelZoom la HRD+ è la Metalbone più potente (10/10) e con più controllo nei colpi d'attacco, ma con un'uscita di palla moderata: in difesa bisogna accompagnare il colpo e lo sweet spot è più piccolo. La Metalbone "normale" perdona di più e ha un'uscita di palla molto alta per una diamante.</p>
<p>A gennaio 2026 Adidas ha annunciato anche la <b>Metalbone Reserve</b>, un'edizione limitata con la firma di Galán per la Reserve Cup ({fonte(G_RES, "All for Padel")}). La fonte non dice che la usi in torneo.</p>
<h2>La racchetta di Galán fa per te?</h2>
<ul><li><b>Sì, la HRD+</b>, se sei un giocatore avanzato, giochi a sinistra, chiudi molto il punto di smash e hai un braccio allenato: è rigida ed esigente.</li><li><b>Meglio la Metalbone</b> se vuoi lo stesso stile di gioco con più tolleranza e più aiuto in difesa.</li><li><b>Nessuna delle due</b> se sei principiante o hai fastidi al gomito: guarda le <a href="{P("guide", "racchetta-padel-principianti")}">racchette per principianti</a> o quelle <a href="{P("guide", "racchetta-padel-epicondilite")}">per l'epicondilite</a>.</li></ul>
<p>Le racchette degli altri professionisti sono nella guida <a href="{pro_url}">con che racchetta giocano i professionisti</a>.</p>""",
        f"""<p><b>Alejandro "Ale" Galán Romo is a Spanish padel player, born in Madrid on 15 May 1996, who plays on the left side (backhand). He was world number 1 with Juan Lebrón and since March 2024 has partnered Argentina's Federico Chingotto. In matches he uses the Adidas Metalbone HRD+ 2026, the stiffest version of his signature line.</b></p>
<h2>Who is Ale Galán</h2>
<ul><li><b>Born:</b> 15 May 1996 in Madrid; 1.86 m tall.</li><li><b>Side:</b> left (backhand), the side that usually finishes points with the smash.</li><li><b>Main partners:</b> Juan Lebrón from 2020 to March 2024, then Federico Chingotto.</li><li><b>World number 1:</b> with Lebrón in 2020, 2021 and 2022; they lost the top spot in May 2023 to Tapia and Coello.</li><li><b>Major titles:</b> three World Padel Tour Master Finals (2019 with Pablo Lima, 2021 and 2022 with Lebrón) and the 2021 World Championship with Spain.</li></ul>
<p class="note">Source: {fonte(G_WIKI, "Wikipedia")}.</p>
<h2>2026 with Chingotto</h2>
<p>In 2026 Galán and Chingotto won seven Premier Padel tournaments: Gijón P2, Miami P1, Giza P2, Asunción P2, Buenos Aires P1 (beating Tapia and Coello in the final), Pretoria P1 and Madrid P1. At the end of October Galán is number 3 in the FIP ranking according to StudyPadel, which credits him with 56 professional titles.</p>
<p class="note">Sources: {fonte(G_WIKI26, "Wikipedia – Premier Padel 2026")}, {fonte(G_STUDY, "StudyPadel")}, {fonte(G_CHINGO, "Chingoland")}. Rankings and titles change week by week.</p>
<h2>Which racket does Ale Galán use</h2>
<p>Galán is an Adidas player and the <b>Metalbone</b> line is his signature racket. According to Chingoland and Padel Ibérico, in 2026 he plays matches with the <b><a href="{url_r(hrd)}">Metalbone HRD+ 2026</a></b>: a diamond with an EVA High Memory core and a 16K aluminised carbon face, the hardest racket in the Adidas range. Alongside it is the <a href="{url_r(mb)}">Metalbone 2026</a>, with the same shape and face materials but a softer core.</p>
{tab}{note_tab}
<p>According to PadelZoom, the HRD+ is the most powerful Metalbone (10/10) and the one with the most control on attacking shots, but with moderate ball output: in defence you have to follow through more and the sweet spot is smaller. The standard Metalbone is more forgiving and has very high ball output for a diamond.</p>
<p>In January 2026 Adidas also announced the <b>Metalbone Reserve</b>, a limited edition signed by Galán for the Reserve Cup ({fonte(G_RES, "All for Padel")}). The source does not say he uses it in tournaments.</p>
<h2>Is Galán's racket right for you?</h2>
<ul><li><b>Yes, the HRD+</b>, if you are an advanced player, play on the left, finish many points with the smash and have a trained arm: it is stiff and demanding.</li><li><b>The Metalbone is better</b> if you want the same style of play with more forgiveness and more help in defence.</li><li><b>Neither</b> if you are a beginner or have elbow problems: look at <a href="{P("guide", "racchetta-padel-principianti")}">rackets for beginners</a> or those <a href="{P("guide", "racchetta-padel-epicondilite")}">for tennis elbow</a>.</li></ul>
<p>The rackets of the other pros are in the guide <a href="{pro_url}">which rackets the pros use</a>.</p>""",
        f"""<p><b>Alejandro "Ale" Galán Romo es un jugador de pádel español, nacido en Madrid el 15 de mayo de 1996, que juega en el lado izquierdo (revés). Fue número 1 del mundo con Juan Lebrón y desde marzo de 2024 forma pareja con el argentino Federico Chingotto. En partido usa la Adidas Metalbone HRD+ 2026, la versión más rígida de su línea firmada.</b></p>
<h2>Quién es Ale Galán</h2>
<ul><li><b>Nacido:</b> el 15 de mayo de 1996 en Madrid; mide 1,86 m.</li><li><b>Lado:</b> izquierdo (revés), el lado que suele cerrar el punto con el remate.</li><li><b>Compañeros principales:</b> Juan Lebrón de 2020 a marzo de 2024, después Federico Chingotto.</li><li><b>Número 1 del mundo:</b> con Lebrón en 2020, 2021 y 2022; perdieron el primer puesto en mayo de 2023 frente a Tapia y Coello.</li><li><b>Títulos importantes:</b> tres Master Final del World Padel Tour (2019 con Pablo Lima, 2021 y 2022 con Lebrón) y el Mundial 2021 con España.</li></ul>
<p class="note">Fuente: {fonte(G_WIKI, "Wikipedia")}.</p>
<h2>El 2026 con Chingotto</h2>
<p>En 2026 Galán y Chingotto ganaron siete torneos de Premier Padel: Gijón P2, Miami P1, Giza P2, Asunción P2, Buenos Aires P1 (en la final contra Tapia y Coello), Pretoria P1 y Madrid P1. A finales de octubre Galán es número 3 del ranking FIP según StudyPadel, que le atribuye 56 títulos profesionales.</p>
<p class="note">Fuentes: {fonte(G_WIKI26, "Wikipedia – Premier Padel 2026")}, {fonte(G_STUDY, "StudyPadel")}, {fonte(G_CHINGO, "Chingoland")}. Los rankings y los títulos cambian cada semana.</p>
<h2>Qué pala usa Ale Galán</h2>
<p>Galán es jugador de Adidas y la línea <b>Metalbone</b> es su pala firmada. Según Chingoland y Padel Ibérico, en 2026 juega los partidos con la <b><a href="{url_r(hrd)}">Metalbone HRD+ 2026</a></b>: una diamante con goma EVA High Memory y cara de carbono aluminizado 16K, la más dura del catálogo de Adidas. A su lado está la <a href="{url_r(mb)}">Metalbone 2026</a>, con la misma forma y los mismos materiales en la cara pero una goma más blanda.</p>
{tab}{note_tab}
<p>Para PadelZoom la HRD+ es la Metalbone más potente (10/10) y la de más control en los golpes de ataque, pero con una salida de bola moderada: en defensa hay que acompañar más el golpe y el punto dulce es más pequeño. La Metalbone "normal" perdona más y tiene una salida de bola muy alta para una diamante.</p>
<p>En enero de 2026 Adidas anunció también la <b>Metalbone Reserve</b>, una edición limitada con la firma de Galán para la Reserve Cup ({fonte(G_RES, "All for Padel")}). La fuente no dice que la use en torneo.</p>
<h2>¿La pala de Galán es para ti?</h2>
<ul><li><b>Sí, la HRD+</b>, si eres un jugador avanzado, juegas en el lado izquierdo, cierras muchos puntos de remate y tienes el brazo entrenado: es rígida y exigente.</li><li><b>Mejor la Metalbone</b> si quieres el mismo estilo de juego con más tolerancia y más ayuda en defensa.</li><li><b>Ninguna de las dos</b> si eres principiante o tienes molestias en el codo: mira las <a href="{P("guide", "racchetta-padel-principianti")}">palas para principiantes</a> o las <a href="{P("guide", "racchetta-padel-epicondilite")}">palas para la epicondilitis</a>.</li></ul>
<p>Las palas de los demás profesionales están en la guía <a href="{pro_url}">con qué pala juegan los profesionales</a>.</p>""", f"""<p><b>Alejandro « Ale » Galán Romo est un joueur de padel espagnol, né à Madrid le 15 mai 1996, qui joue à gauche (côté revers). Il a été numéro 1 mondial avec Juan Lebrón et, depuis mars 2024, il fait équipe avec l'Argentin Federico Chingotto. En match, il utilise l'Adidas Metalbone HRD+ 2026, la version la plus rigide de sa ligne signature.</b></p>
<h2>Qui est Ale Galán</h2>
<ul><li><b>Naissance :</b> 15 mai 1996 à Madrid ; 1,86 m.</li><li><b>Côté :</b> gauche (revers), le côté qui conclut généralement les points au smash.</li><li><b>Principaux partenaires :</b> Juan Lebrón de 2020 à mars 2024, puis Federico Chingotto.</li><li><b>Numéro 1 mondial :</b> avec Lebrón en 2020, 2021 et 2022 ; ils ont perdu la première place en mai 2023 au profit de Tapia et Coello.</li><li><b>Principaux titres :</b> trois Master Finals du World Padel Tour (2019 avec Pablo Lima, 2021 et 2022 avec Lebrón) et le Championnat du monde 2021 avec l'Espagne.</li></ul>
<p class="note">Source : {fonte(G_WIKI, "Wikipedia")}.</p>
<h2>2026 avec Chingotto</h2>
<p>En 2026, Galán et Chingotto ont remporté sept tournois Premier Padel : Gijón P2, Miami P1, Gizeh P2, Asunción P2, Buenos Aires P1 (en battant Tapia et Coello en finale), Pretoria P1 et Madrid P1. Fin octobre, Galán est numéro 3 du classement FIP selon StudyPadel, qui lui attribue 56 titres professionnels.</p>
<p class="note">Sources : {fonte(G_WIKI26, "Wikipedia – Premier Padel 2026")}, {fonte(G_STUDY, "StudyPadel")}, {fonte(G_CHINGO, "Chingoland")}. Classements et titres changent chaque semaine.</p>
<h2>Avec quelle raquette joue Ale Galán</h2>
<p>Galán est un joueur Adidas et la ligne <b>Metalbone</b> est sa raquette signature. Selon Chingoland et Padel Ibérico, en 2026 il joue ses matchs avec la <b><a href="{url_r(hrd)}">Metalbone HRD+ 2026</a></b> : une diamant avec noyau EVA High Memory et tamis en carbone aluminisé 16K, la raquette la plus dure de la gamme Adidas. À ses côtés, il y a la <a href="{url_r(mb)}">Metalbone 2026</a>, avec la même forme et les mêmes matériaux de tamis mais un noyau plus souple.</p>
{tab}{note_tab}
<p>Selon PadelZoom, la HRD+ est la Metalbone la plus puissante (10/10) et celle qui offre le plus de contrôle sur les frappes d'attaque, mais avec une sortie de balle modérée : en défense, il faut davantage accompagner et le sweet spot est plus petit. La Metalbone standard est plus tolérante et a une sortie de balle très élevée pour une diamant.</p>
<p>En janvier 2026, Adidas a aussi annoncé la <b>Metalbone Reserve</b>, une édition limitée signée Galán pour la Reserve Cup ({fonte(G_RES, "All for Padel")}). La source ne dit pas qu'il l'utilise en tournoi.</p>
<h2>La raquette de Galán est-elle faite pour vous ?</h2>
<ul><li><b>Oui, la HRD+</b>, si vous êtes un joueur avancé, jouez à gauche, concluez beaucoup de points au smash et avez un bras entraîné : elle est rigide et exigeante.</li><li><b>La Metalbone est meilleure</b> si vous voulez le même style de jeu avec plus de tolérance et plus d'aide en défense.</li><li><b>Aucune des deux</b> si vous débutez ou avez des problèmes de coude : regardez les <a href="{P("guide", "racchetta-padel-principianti")}">raquettes pour débutants</a> ou celles <a href="{P("guide", "racchetta-padel-epicondilite")}">pour l'épicondylite</a>.</li></ul>
<p>Les raquettes des autres pros sont dans le guide <a href="{pro_url}">quelles raquettes utilisent les pros</a>.</p>""")
    qa = [(L("Che racchetta usa Ale Galán?", "Which racket does Ale Galán use?", "¿Qué pala usa Ale Galán?", "Quelle raquette utilise Ale Galán ?"),
           L("Nel 2026 usa la Adidas Metalbone HRD+ 2026, una diamante rigida con gomma EVA High Memory e faccia in carbonio alluminizzato 16K.",
             "In 2026 he uses the Adidas Metalbone HRD+ 2026, a stiff diamond with an EVA High Memory core and a 16K aluminised carbon face.",
             "En 2026 usa la Adidas Metalbone HRD+ 2026, una diamante rígida con goma EVA High Memory y cara de carbono aluminizado 16K.", "En 2026, il utilise l'Adidas Metalbone HRD+ 2026, une diamant rigide avec noyau EVA High Memory et tamis en carbone aluminisé 16K.")),
          (L("Con chi gioca Ale Galán?", "Who does Ale Galán play with?", "¿Con quién juega Ale Galán?", "Avec qui joue Ale Galán ?"),
           L("Dal marzo 2024 gioca con l'argentino Federico Chingotto; prima, dal 2020, con Juan Lebrón.",
             "Since March 2024 he has played with Argentina's Federico Chingotto; before that, from 2020, with Juan Lebrón.",
             "Desde marzo de 2024 juega con el argentino Federico Chingotto; antes, desde 2020, con Juan Lebrón.", "Depuis mars 2024, il joue avec l'Argentin Federico Chingotto ; avant cela, à partir de 2020, avec Juan Lebrón.")),
          (L("Quanto costa la racchetta di Galán?", "How much does Galán's racket cost?", "¿Cuánto cuesta la pala de Galán?", "Combien coûte la raquette de Galán ?"),
           L("Il prezzo di listino della Metalbone HRD+ 2026 è 390 €; nei negozi si trova spesso scontata.",
             "The list price of the Metalbone HRD+ 2026 is €390; shops often sell it at a discount.",
             "El precio de lista de la Metalbone HRD+ 2026 es de 390 €; en las tiendas suele encontrarse rebajada.", "Le prix catalogue de la Metalbone HRD+ 2026 est de 390 € ; les boutiques la vendent souvent en promotion."))]
    faq_htm, faq_ld = faq(qa)
    persona = {"@context": "https://schema.org", "@type": "Person", "name": "Alejandro Galán Romo", "alternateName": "Ale Galán",
               "birthDate": "1996-05-15", "birthPlace": "Madrid", "nationality": "Spain", "sameAs": [G_WIKI]}
    titolo = L("Ale Galán: chi è e che racchetta usa nel 2026", "Ale Galán: who he is and which racket he uses in 2026", "Ale Galán: quién es y qué pala usa en 2026", "Ale Galán : qui il est et quelle raquette il utilise en 2026")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Chi è Ale Galán (Madrid, 1996), con chi gioca, i suoi titoli e la racchetta che usa nel 2026: Adidas Metalbone HRD+, con dati tecnici e alternative.",
                      "Who Ale Galán is (Madrid, 1996), who he plays with, his titles and the racket he uses in 2026: Adidas Metalbone HRD+, with specs and alternatives.",
                      "Quién es Ale Galán (Madrid, 1996), con quién juega, sus títulos y la pala que usa en 2026: Adidas Metalbone HRD+, con datos técnicos y alternativas.", "Qui est Ale Galán (Madrid, 1996), avec qui il joue, ses titres et la raquette qu'il utilise en 2026 : Adidas Metalbone HRD+, avec caractéristiques et alternatives."),
                    titolo, "Ale Galán", corpo + faq_htm, items=[hrd, mb], ld_extra=[faq_ld, persona])
    return slug, titolo, L("Il campione madrileno, i titoli con Lebrón e Chingotto e la sua Adidas Metalbone HRD+.",
                           "The Madrid champion, his titles with Lebrón and Chingotto and his Adidas Metalbone HRD+.",
                           "El campeón madrileño, sus títulos con Lebrón y Chingotto y su Adidas Metalbone HRD+.", "Le champion madrilène, ses titres avec Lebrón et Chingotto et son Adidas Metalbone HRD+.")


# ---------------------------------------------------------------- 4. Giocatori (Chingotto, Coello, Tapia, Lebrón)

import re as _re  # noqa: E402
from dati_giocatori import GIOCATORI, F as FG, TITOLI_TC, TITOLI_GC  # noqa: E402

for _g in GIOCATORI:
    S.SLUG[_g["slug"]] = (_g["slug_en"], _g["slug_es"])
    S.SLUG_FR[_g["slug"]] = _g["slug"].replace("-chi-e-e-che-racchetta-usa", "-qui-est-il-et-quelle-raquette-utilise-t-il")


def _link_r(txt, per):
    def rep(m):
        n = per.get(m.group(1))
        return f'<a href="{url_r(n)}">{e(n["titolo"])}</a>' if n else e(m.group(1))
    return _re.sub(r"\{r:([a-z0-9-]+)\}", rep, txt)


def _fonti(keys):
    return ", ".join(fonte(FG[k][1], FG[k][0]) for k in keys)


def giocatore(db, G):
    per = {n["slug"]: n for n in db}
    nd = L("n.d.", "n/a", "n.d.", "n.c.")
    tab_r = [per[s] for s in G["tabella"] if s in per]
    righe_def = [(L("Forma", "Shape", "Forma", "Forme"), lambda n: FORMA(n["forma"])), (L("Peso", "Weight", "Peso", "Poids"), lambda n: n["peso"]),
                 (L("Bilanciamento", "Balance", "Balance", "Équilibre"), lambda n: S.tr(n["bilanciamento"]) if isinstance(n["bilanciamento"], str) else None),
                 (L("Gomma", "Core", "Goma", "Noyau"), lambda n: S.tr(n["nucleo"]) if isinstance(n["nucleo"], str) else None),
                 (L("Faccia", "Face", "Cara", "Tamis"), lambda n: S.tr(n["superficie"]) if isinstance(n["superficie"], str) else None),
                 (L("Tatto", "Feel", "Tacto", "Toucher"), lambda n: S.tr(n["sensazione"]) if isinstance(n["sensazione"], str) else None),
                 (L("Livello", "Level", "Nivel", "Niveau"), lambda n: LIVN(n["livello"])),
                 (L("Prezzo di listino", "List price", "Precio de lista", "Prix catalogue"), lambda n: euro(n["prezzo"]) if n["prezzo"] else None)]
    righe = "".join("<tr><td>" + e(lab) + "</td>" + "".join(f"<td>{e(f(n) or nd)}</td>" for n in tab_r) + "</tr>" for lab, f in righe_def)
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th></th>' + "".join(f'<th><a href="{url_r(n)}">{e(n["titolo"])}</a></th>' for n in tab_r)
           + f"</tr></thead><tbody>{righe}</tbody></table></div>")
    fonti_tab = []
    for n in tab_r:
        for u in n["d"].get("fonti_dati", []):
            if u not in fonti_tab:
                fonti_tab.append(u)
    note_tab = (f'<p class="note">{L("Dati tecnici dalle schede PadelMetrix; fonti", "Specs from the PadelMetrix spec pages; sources", "Datos técnicos de las fichas de PadelMetrix; fuentes", "Caractéristiques issues des fiches PadelMetrix ; sources")}: '
                + ", ".join(fonte(u) for u in fonti_tab) + f'. {L("n.d. = non dichiarato dalle fonti.", "n/a = not stated by the sources.", "n.d. = no declarado por las fuentes.", "n.c. = non communiqué par les sources.")}</p>')
    bio = "".join(f"<li><b>{e(g(k))}:</b> {e(g(v))}</li>" for k, v in G["bio"])
    stagione = g(G["stagione"]).format(tc=g(TITOLI_TC), gc=g(TITOLI_GC))
    nome, breve = G["nome"], G["breve"]
    pro_url = P("guide", "racchette-giocatori-professionisti")
    corpo = f"""<p><b>{e(g(G["lead"]))}</b></p>
<h2>{L(f"Chi è {nome}", f"Who is {nome}", f"Quién es {nome}", f"Qui est {nome}")}</h2>
<ul>{bio}</ul>
<p class="note">{L("Fonte", "Source", "Fuente", "Source")}: {_fonti(G["fonti_bio"])}.</p>
<h2>{L(f"{breve} nel 2026", f"{breve} in 2026", f"{breve} en 2026", f"{breve} en 2026")}</h2>
<p>{e(stagione)}</p>
<p class="note">{L("Fonti", "Sources", "Fuentes", "Sources")}: {_fonti(G["fonti_stagione"])}. {L("Classifiche e titoli cambiano di settimana in settimana.", "Rankings and titles change week by week.", "Los rankings y los títulos cambian cada semana.", "Classements et titres changent chaque semaine.")}</p>
<h2>{L(f"Che racchetta usa {breve}", f"Which racket does {breve} use", f"Qué pala usa {breve}", f"Avec quelle raquette joue {breve}")}</h2>
<p>{_link_r(e(g(G["racchetta"])), per)}</p>
<p class="note">{L("Fonti sul modello usato", "Sources on the model used", "Fuentes sobre el modelo usado", "Sources sur le modèle utilisé")}: {_fonti(G["fonti_racchetta"])}.</p>
{tab}{note_tab}
<h2>{L(f"La racchetta di {breve} fa per te?", f"Is {breve}'s racket right for you?", f"¿La pala de {breve} es para ti?", f"La raquette de {breve} est-elle faite pour vous ?")}</h2>
<ul>{"".join(f"<li>{g(x)}</li>" for x in G["adatta"])}<li>{L(f'<b>Nessuna delle sue racchette da torneo</b> se sei principiante o hai fastidi al gomito: guarda le <a href="{P("guide", "racchetta-padel-principianti")}">racchette per principianti</a> o quelle <a href="{P("guide", "racchetta-padel-epicondilite")}">per l\'epicondilite</a>.',
        f'<b>None of his tournament rackets</b> if you are a beginner or have elbow problems: look at <a href="{P("guide", "racchetta-padel-principianti")}">rackets for beginners</a> or those <a href="{P("guide", "racchetta-padel-epicondilite")}">for tennis elbow</a>.',
        f'<b>Ninguna de sus palas de torneo</b> si eres principiante o tienes molestias en el codo: mira las <a href="{P("guide", "racchetta-padel-principianti")}">palas para principiantes</a> o las <a href="{P("guide", "racchetta-padel-epicondilite")}">palas para la epicondilitis</a>.', f'<b>Aucune de ses raquettes de tournoi</b> si vous débutez ou avez des problèmes de coude : regardez les <a href="{P("guide", "racchetta-padel-principianti")}">raquettes pour débutants</a> ou celles <a href="{P("guide", "racchetta-padel-epicondilite")}">pour l\'épicondylite</a>.')}</li></ul>
<p>{L(f'Le racchette degli altri professionisti sono nella guida <a href="{pro_url}">con che racchetta giocano i professionisti</a>.', f'The rackets of the other pros are in the guide <a href="{pro_url}">which rackets the pros use</a>.', f'Las palas de los demás profesionales están en la guía <a href="{pro_url}">con qué pala juegan los profesionales</a>.', f'Les raquettes des autres pros sont dans le guide <a href="{pro_url}">quelles raquettes utilisent les pros</a>.')}</p>"""
    qa = [(g(q), g(a)) for q, a in G["faq"]]
    faq_htm, faq_ld = faq(qa)
    persona = {"@context": "https://schema.org", "@type": "Person", **G["persona"]}
    titolo = g(G["titolo"])
    items = [per[s] for s in G["racchette"] if s in per]
    scrivi_articolo(G["slug"], titolo + " | PadelMetrix", g(G["desc"]), titolo, nome, corpo + faq_htm, items=items, ld_extra=[faq_ld, persona])
    return G["slug"], titolo, g(G["sommario"])


# ---------------------------------------------------------------- 9. 2027 vs 2026, modello per modello

S.SLUG["racchette-padel-2027-vs-2026-cosa-cambia"] = ("padel-rackets-2027-vs-2026-what-changes", "palas-padel-2027-vs-2026-que-cambia")
S.SLUG["migliori-racchette-padel-2026-classifiche-indipendenti"] = ("best-padel-rackets-2026-independent-rankings", "mejores-palas-padel-2026-rankings-independientes")

VOCI = [("giocatore", T("Giocatore", "Player", "Jugador", "Joueur")), ("forma", T("Forma", "Shape", "Forma", "Forme")), ("peso", T("Peso", "Weight", "Peso", "Poids")),
        ("bilanciamento", T("Bilanciamento", "Balance", "Balance", "Équilibre")), ("superficie", T("Faccia", "Face", "Cara", "Tamis")), ("telaio", T("Telaio", "Frame", "Marco", "Cadre")),
        ("sensazione", T("Sensazione", "Feel", "Tacto", "Toucher")), ("livello", T("Livello", "Level", "Nivel", "Niveau")), ("prezzo_listino_eur", T("Listino", "List price", "Precio de lista", "Prix catalogue"))]


def _val(k, v):
    if v in (None, ""):
        return None
    if k == "forma":
        return FORMA(v)
    if k == "livello":
        return LIVN(v)
    if k == "prezzo_listino_eur":
        return euro(v)
    return S.tr(v)


def _norm(v):
    """Confronta il valore senza i dettagli tra parentesi: "alto" e "alto (26,3 cm)" sono lo stesso dato."""
    return str(v).split("(")[0].strip().lower().replace("dura", "duro") if v is not None else None


def confronti_2027(db):
    slug = "racchette-padel-2027-vs-2026-cosa-cambia"
    gruppi = {}
    for n in db:
        if n["categoria"] != "junior":
            gruppi.setdefault((n["marca"], n["modello"]), {})[n["anno"]] = n
    coppie_ok = set(coppie(db))
    pairs = sorted(((k, v[2026], v[2027]) for k, v in gruppi.items() if 2026 in v and 2027 in v), key=lambda x: x[0])
    sezioni, cambi_forma, cambi_prezzo, tot_diff = [], [], [], 0
    nd = L("non dichiarato", "not stated", "no declarado", "non communiqué")
    for (marca, modello), a, b in pairs:
        da, dbb = a["d"], b["d"]
        righe, n_diff, n_ug, n_manca = [], 0, 0, 0
        for k, nome in VOCI:
            va, vb = da.get(k), dbb.get(k)
            if va in (None, "") and vb in (None, ""):
                continue
            if va in (None, "") or vb in (None, ""):
                stato, n_manca = L("non confrontabile", "not comparable", "no comparable", "non comparable"), n_manca + 1
                cls = "nd"
            elif _norm(va) == _norm(vb):
                stato, n_ug, cls = L("uguale", "same", "igual", "identique"), n_ug + 1, "ok"
            else:
                stato, n_diff, cls = f"<b>{L('cambia', 'changes', 'cambia', "change")}</b>", n_diff + 1, "diff"
                if k == "forma":
                    cambi_forma.append((marca, modello + (L(", fonti 2026 discordanti", ", 2026 sources disagree", ", fuentes 2026 discrepantes", ", les sources 2026 divergent") if (marca, modello) == ("Siux", "Diablo Pro") else ""), FORMA(va), FORMA(vb)))
                if k == "prezzo_listino_eur":
                    cambi_prezzo.append((marca, modello, va, vb))
            righe.append(f'<tr class="{cls}"><td>{g(nome)}</td><td>{e(_val(k, va) or nd)}</td><td>{e(_val(k, vb) or nd)}</td><td>{stato}</td></tr>')
        tot_diff += n_diff
        if slug_art := ("siux-diablo-pro-2026-vs-2027-cosa-cambia" if (marca, modello) == ("Siux", "Diablo Pro") else None):
            extra = f'<a href="{P("articoli", slug_art)}">{L("Articolo dedicato", "Dedicated article", "Artículo dedicado", "Article dédié")}</a>'
        elif tuple(sorted((a["slug"], b["slug"]))) in coppie_ok:
            extra = f'<a href="{confronto_url(a["slug"], b["slug"])}">{L("Confronto completo", "Full comparison", "Comparativa completa", "Comparatif complet")}</a>'
        else:
            extra = ""
        sint = L(f"Cambiano: {n_diff} · uguali: {n_ug} · non confrontabili (manca il dato di una delle due versioni): {n_manca}.",
                 f"Changed: {n_diff} · same: {n_ug} · not comparable (one version does not state the figure): {n_manca}.",
                 f"Cambian: {n_diff} · iguales: {n_ug} · no comparables (falta el dato de una de las dos versiones): {n_manca}.", f"Changé : {n_diff} · identique : {n_ug} · non comparable (une version ne communique pas la donnée) : {n_manca}.")
        ancora = S.slugify(f"{marca} {modello}")
        sezioni.append(f'''<h3 id="{ancora}">{e(marca)} {e(modello)}: 2026 vs 2027</h3>
<p>{sint} <a href="{url_r(a)}">{L("Scheda 2026", "2026 page", "Ficha 2026", "Fiche 2026")}</a> · <a href="{url_r(b)}">{L("Scheda 2027", "2027 page", "Ficha 2027", "Fiche 2027")}</a>{" · " + extra if extra else ""}</p>
<div class="tablebox"><table class="tab"><thead><tr><th>{L("Voce", "Item", "Dato", "Critère")}</th><th>2026</th><th>2027</th><th>{L("Esito", "Result", "Resultado", "Résultat")}</th></tr></thead><tbody>{"".join(righe)}</tbody></table></div>''')
    indice_htm = '<div class="marche">' + "".join(f'<a href="#{S.slugify(m + " " + mo)}">{e(m)} {e(mo)}</a>' for (m, mo), _, _ in pairs) + "</div>"
    forma_txt = "; ".join(f"{e(m)} {e(mo)} ({e(x)} → {e(y)})" for m, mo, x, y in cambi_forma)
    aum = [x for x in cambi_prezzo if x[3] > x[2]]
    prezzo_txt = "; ".join(f"{e(m)} {e(mo)} ({euro(x)} → {euro(y)})" for m, mo, x, y in cambi_prezzo)
    marche = sorted({m for (m, _), _, _ in pairs})
    intro = L(
        f"<p><b>Abbiamo messo a confronto, voce per voce, le {len(pairs)} racchette che nel database PadelMetrix esistono sia in versione 2026 sia in versione 2027</b> ({', '.join(marche)}). Per ogni modello trovi cosa cambia, cosa resta uguale e cosa non si può confrontare perché il produttore o i rivenditori non lo dichiarano.</p>"
        f"<p>In sintesi: la forma cambia in {len(cambi_forma)} modelli ({forma_txt}). Il listino è dichiarato per entrambe le versioni solo in {len(cambi_prezzo)} casi ({prezzo_txt}){', sempre in aumento' if cambi_prezzo and len(aum) == len(cambi_prezzo) else ''}. Molte voci delle versioni 2026 non sono mai state pubblicate, quindi per diversi modelli non si può dire se il 2027 sia davvero diverso.</p>",
        f"<p><b>We compared, item by item, the {len(pairs)} rackets that exist in the PadelMetrix database in both a 2026 and a 2027 version</b> ({', '.join(marche)}). For each model you can see what changes, what stays the same and what cannot be compared because the manufacturer or retailers do not state it.</p>"
        f"<p>In short: the shape changes in {len(cambi_forma)} models ({forma_txt}). The list price is stated for both versions in only {len(cambi_prezzo)} cases ({prezzo_txt}){', always going up' if cambi_prezzo and len(aum) == len(cambi_prezzo) else ''}. Many 2026 figures were never published, so for several models it is impossible to say whether the 2027 is really different.</p>",
        f"<p><b>Hemos comparado, dato por dato, las {len(pairs)} palas que en la base de datos de PadelMetrix existen tanto en versión 2026 como en versión 2027</b> ({', '.join(marche)}). Para cada modelo verás qué cambia, qué se mantiene y qué no se puede comparar porque el fabricante o las tiendas no lo declaran.</p>"
        f"<p>En resumen: la forma cambia en {len(cambi_forma)} modelos ({forma_txt}). El precio de lista está declarado para ambas versiones solo en {len(cambi_prezzo)} casos ({prezzo_txt}){', siempre al alza' if cambi_prezzo and len(aum) == len(cambi_prezzo) else ''}. Muchos datos de las versiones 2026 nunca se publicaron, así que en varios modelos no se puede decir si la 2027 es realmente distinta.</p>", f"<p><b>Nous avons comparé, critère par critère, les {len(pairs)} raquettes qui existent dans la base PadelMetrix en version 2026 et 2027</b> ({', '.join(marche)}). Pour chaque modèle, vous voyez ce qui change, ce qui reste identique et ce qui ne peut pas être comparé parce que le fabricant ou les revendeurs ne le communiquent pas.</p>"
        f"<p>En bref : la forme change sur {len(cambi_forma)} modèles ({forma_txt}). Le prix catalogue n'est indiqué pour les deux versions que dans {len(cambi_prezzo)} cas ({prezzo_txt}){', toujours à la hausse' if cambi_prezzo and len(aum) == len(cambi_prezzo) else ''}. Beaucoup de données 2026 n'ont jamais été publiées : pour plusieurs modèles, il est donc impossible de dire si le 2027 est vraiment différent.</p>")
    metodo = L(
        '<p class="note">Come leggere le tabelle: "cambia" significa che le fonti dichiarano valori diversi per le due versioni. A volte la differenza dipende anche da come rivenditori diversi descrivono la stessa racchetta (per esempio il livello di gioco): prima di decidere guarda le fonti nelle schede. "Non confrontabile" significa che una delle due versioni non dichiara il dato.</p>',
        '<p class="note">How to read the tables: "changes" means the sources state different values for the two versions. Sometimes the difference also depends on how different retailers describe the same racket (for example the playing level): check the sources on each spec page before deciding. "Not comparable" means one of the two versions does not state the figure.</p>',
        '<p class="note">Cómo leer las tablas: "cambia" significa que las fuentes declaran valores distintos para las dos versiones. A veces la diferencia depende también de cómo tiendas distintas describen la misma pala (por ejemplo el nivel de juego): antes de decidir mira las fuentes en cada ficha. "No comparable" significa que una de las dos versiones no declara el dato.</p>', "<p class=\"note\">Comment lire les tableaux : « change » signifie que les sources indiquent des valeurs différentes pour les deux versions. Parfois la différence dépend aussi de la façon dont différents revendeurs décrivent la même raquette (par exemple le niveau de jeu) : vérifiez les sources sur chaque fiche avant de décider. « Non comparable » signifie qu'une des deux versions ne communique pas la donnée.</p>")
    qa = [(L("Le racchette 2027 sono molto diverse dalle 2026?", "Are 2027 rackets very different from the 2026 ones?", "¿Las palas 2027 son muy distintas de las 2026?", "Les raquettes 2027 sont-elles très différentes des 2026 ?"),
           L(f"Dipende dal modello. Su {len(pairs)} rinnovi confrontati la forma cambia in {len(cambi_forma)} casi; negli altri le differenze dichiarate riguardano soprattutto materiali della faccia, finitura e prezzo.",
             f"It depends on the model. Across {len(pairs)} updates compared, the shape changes in {len(cambi_forma)} cases; in the others the stated differences are mostly about face materials, finish and price.",
             f"Depende del modelo. En {len(pairs)} renovaciones comparadas la forma cambia en {len(cambi_forma)} casos; en las demás las diferencias declaradas son sobre todo de materiales de la cara, acabado y precio.", f"Cela dépend du modèle. Sur {len(pairs)} mises à jour comparées, la forme change dans {len(cambi_forma)} cas ; dans les autres, les différences déclarées portent surtout sur les matériaux du tamis, la finition et le prix.")),
          (L("Conviene comprare la 2026 scontata?", "Is the discounted 2026 worth buying?", "¿Conviene comprar la 2026 rebajada?", "Le 2026 en promotion vaut-il le coup ?"),
           L("Se forma, peso e bilanciamento restano uguali e la 2026 si trova scontata, spesso sì. Se cambia la forma, la racchetta si comporta in modo diverso e conviene provarle entrambe.",
             "If shape, weight and balance stay the same and the 2026 is discounted, often yes. If the shape changes, the racket behaves differently and it is worth trying both.",
             "Si forma, peso y balance se mantienen y la 2026 está rebajada, muchas veces sí. Si cambia la forma, la pala se comporta distinto y conviene probar las dos.", "Si la forme, le poids et l'équilibre restent identiques et que le 2026 est en promotion, souvent oui. Si la forme change, la raquette se comporte différemment et il vaut la peine d'essayer les deux."))]
    faq_htm, faq_ld = faq(qa)
    corpo = intro + indice_htm + metodo + "".join(sezioni) + faq_htm
    titolo = L("Racchette padel 2027 vs 2026: cosa cambia modello per modello", "Padel rackets 2027 vs 2026: what changes, model by model",
               "Palas de pádel 2027 vs 2026: qué cambia modelo por modelo", "Raquettes de padel 2027 vs 2026 : ce qui change, modèle par modèle")
    items = [x for _, a, b in pairs for x in (b,)]
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L(f"{len(pairs)} racchette da padel confrontate voce per voce tra versione 2026 e 2027: forma, peso, bilanciamento, faccia, livello e prezzo.",
                      f"{len(pairs)} padel rackets compared item by item between the 2026 and 2027 versions: shape, weight, balance, face, level and price.",
                      f"{len(pairs)} palas de pádel comparadas dato por dato entre la versión 2026 y la 2027: forma, peso, balance, cara, nivel y precio.", f"{len(pairs)} raquettes de padel comparées critère par critère entre les versions 2026 et 2027 : forme, poids, équilibre, tamis, niveau et prix."),
                    titolo, L("2027 vs 2026", "2027 vs 2026", "2027 vs 2026", "2027 vs 2026"), corpo, items=items, ld_extra=[faq_ld])
    RACCHETTE_ARTICOLO[slug] = [x["slug"] for _, a, b in pairs for x in (a, b)]
    return slug, titolo, L(f"{len(pairs)} rinnovi confrontati voce per voce: cosa cambia davvero.", f"{len(pairs)} updates compared item by item: what really changes.",
                           f"{len(pairs)} renovaciones comparadas dato por dato: qué cambia de verdad.", f"{len(pairs)} mises à jour comparées critère par critère : ce qui change vraiment.")


# ---------------------------------------------------------------- 10. Migliori racchette 2026 secondo le classifiche indipendenti

PF = "https://www.padelful.com/es/mejores-palas-padel"
PF_M = "https://www.padelful.com/es/como-puntuamos"
PV = "https://padelverdict.com/es/guias/mejores-palas-padel-2026/"

# (nome come lo pubblica la fonte, slug nel database se è lo stesso modello, voto, potenza, controllo, rebote, manejo, punto dulce)
PADELFUL = [
    ("Nox AT10 Luxury Genius 18K 2026 (Agustín Tapia)", None, 87, 79, 87, 85, 96, 90),
    ("Bullpadel Vertex 05 2026 (Juan Tello)", "bullpadel-vertex-05-2026", 87, 85, 88, 85, 83, 92),
    ("Bullpadel Hack 04 2026 (Paquito Navarro)", "bullpadel-hack-04-2026", 87, 100, 90, 80, 83, 82),
    ("Head Extreme Pro 2026", "head-extreme-pro-2026", 87, 100, 96, 80, 81, 80),
    ("StarVie Raptor 2026 Plus", None, 86, 80, 89, 89, 80, 90),
    ("Bullpadel Neuron 02 2026 (Fede Chingotto)", "bullpadel-neuron-02-2026", 86, 80, 94, 78, 85, 92),
    ("Nox AT10 Genius Attack 18K 2026", "nox-at10-genius-attack-18k-alum-2026", 87, 96, 91, 85, 81, 82),
    ("StarVie Black Titan 2026", "starvie-black-titan-2026", 86, 94, 97, 81, 78, 81),
    ("Babolat Viper 3.0 2026 (Juan Lebrón)", "babolat-viper-juan-lebron-3-0-2026", 87, 98, 94, 82, 76, 86),
    ("Adidas Metalbone HRD+ 2026 (Ale Galán)", "adidas-metalbone-hrd-plus-2026", 87, 99, 94, 80, 80, 81),
]
# (sezione, nome della fonte, slug, verdict, punteggio di profilo)
VERDICT = [
    ("gen", "NOX EA10 Ventus Attack 12K Xtrem 2026", "nox-ea10-ventus-attack-12k-xtrem-2026", 9.0, 8.72),
    ("gen", "StarVie BlackTitan 2026", "starvie-black-titan-2026", 9.0, 8.73),
    ("gen", "Adidas Metalbone HRD 2026", None, 8.8, 8.52),
    ("gen", "Babolat Technical Viper 3.0 2026", "babolat-technical-viper-3-0-2026", 8.8, 8.55),
    ("gen", "HEAD Coello Pro 2026", "head-coello-pro-2026", 8.8, 8.48),
    ("hyb", "NOX Ventus Hybrid 12K Lite 2026", "nox-ventus-hybrid-12k-lite-2026", 8.7, 8.39),
    ("hyb", "StarVie Astrum+ 2026", None, 8.6, 8.39),
    ("hyb", "Babolat Air Viper 2026", None, 8.6, 8.39),
    ("hyb", "NOX AT10 12K Lite 2026", None, 8.6, 8.35),
    ("hyb", "Siux Diablo Pro 2026", "siux-diablo-pro-2026", 8.5, 8.33),
    ("def", "NOX ML10 Ventus Control 3K 2026", "nox-ml10-ventus-control-3k-2026", 8.8, 8.59),
    ("def", "NOX VK10 Ventus Control 12K 2026", "nox-vk10-ventus-control-12k-2026", 8.7, 8.49),
    ("def", "Adidas Arrow Hit Carbon CTRL 2026", "adidas-arrow-hit-carbon-ctrl-2026", 8.6, 8.41),
    ("def", "Adidas Metalbone Carbon CTRL 2026", "adidas-metalbone-carbon-ctrl-2026", 8.6, 8.37),
    ("def", "Oxdog Pure Pro Plus 2026", "oxdog-pure-pro-plus-2026", 8.6, 8.37),
]


def migliori_2026(db):
    slug = "migliori-racchette-padel-2026-classifiche-indipendenti"
    per = {n["slug"]: n for n in db}

    def nome(txt, s):
        return f'<a href="{url_r(per[s])}">{e(txt)}</a>' if s in per else e(txt)

    th_pf = [L("#", "#", "#", "#"), L("Racchetta (come la chiama la fonte)", "Racket (as named by the source)", "Pala (como la llama la fuente)", "Raquette (nom donné par la source)"), L("Voto", "Score", "Nota", "Note"),
             L("Potenza", "Power", "Potencia", "Puissance"), L("Controllo", "Control", "Control", "Contrôle"), L("Uscita palla", "Ball exit", "Salida de bola", "Sortie de balle"),
             L("Maneggevolezza", "Handling", "Manejabilidad", "Maniabilité"), L("Punto dolce", "Sweet spot", "Punto dulce", "Sweet spot")]
    pf_rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in (i, nome(n, s), f"<b>{v}</b>", *sub)) + "</tr>" for i, (n, s, v, *sub) in enumerate(PADELFUL, 1))
    tab_pf = f'<div class="tablebox"><table class="tab"><thead><tr>{"".join(f"<th>{t}</th>" for t in th_pf)}</tr></thead><tbody>{pf_rows}</tbody></table></div>'

    sez = {"gen": L("Classifica generale", "Overall ranking", "Ranking general", "Classement général"), "hyb": L("Migliori polivalenti", "Best all-round", "Mejores polivalentes", "Meilleures polyvalentes"),
           "def": L("Migliori per il controllo", "Best for control", "Mejores para control", "Meilleures pour le contrôle")}
    prof = {"gen": L("Attacco", "Attack", "Ataque", "Attaque"), "hyb": L("Polivalente", "All-round", "Polivalente", "Polyvalente"), "def": L("Controllo", "Control", "Control", "Contrôle")}
    blocchi = []
    for k in ("gen", "hyb", "def"):
        rr = "".join(f"<tr><td>{i}</td><td>{nome(n, s)}</td><td><b>{v:.1f}</b></td><td>{p:.2f}</td></tr>"
                     for i, (_, n, s, v, p) in enumerate([x for x in VERDICT if x[0] == k], 1))
        blocchi.append(f'<h3>{sez[k]}</h3><div class="tablebox"><table class="tab"><thead><tr><th>#</th><th>{L("Racchetta (come la chiama la fonte)", "Racket (as named by the source)", "Pala (como la llama la fuente)", "Raquette (nom donné par la source)")}</th><th>Verdict Score</th><th>{L("Punteggio", "Profile score", "Puntuación", "Note du profil")} {prof[k]}</th></tr></thead><tbody>{rr}</tbody></table></div>')

    pz = sorted([n for n in db if n["d"].get("valutazioni_padelzoom") and n["anno"] == 2026], key=lambda n: -n["d"]["valutazioni_padelzoom"]["globale"])[:5]
    pz_rows = "".join(f'<tr><td><a href="{url_r(n)}">{e(n["nome"])}</a></td><td><b>{n["d"]["valutazioni_padelzoom"]["globale"]}</b></td><td>{n["d"]["valutazioni_padelzoom"]["potenza"]}</td><td>{n["d"]["valutazioni_padelzoom"]["controllo"]}</td></tr>' for n in pz)

    entrambe = sorted({s for _, _, s, _, _ in VERDICT if s} & {s for _, s, *_ in PADELFUL if s})
    ent_txt = ", ".join(nome(per[s]["nome"], s) for s in entrambe)
    corpo = L(
        f"""<p><b>Quali sono le migliori racchette da padel del 2026? Invece di stilare l'ennesima classifica abbiamo messo insieme quelle di due siti di recensioni che non vendono racchette: Padelful e PadelVerdict.</b> L'unica racchetta presente in tutte e due le classifiche è {ent_txt}: 8ª su Padelful con 86/100 e 2ª su PadelVerdict con 9,0 (1ª tra le racchette d'attacco). Le altre posizioni cambiano molto da una fonte all'altra, quindi una classifica unica sarebbe un'invenzione.</p>
<p>Attenzione ai nomi: le marche fanno più versioni dello stesso modello (per esempio la Metalbone HRD e la HRD+, o la Viper Juan Lebrón e la Technical Viper). Le abbiamo tenute separate e abbiamo messo il link alla scheda PadelMetrix solo quando il modello è esattamente lo stesso.</p>
<h2>La classifica di Padelful</h2>
<p>Padelful dà un voto da 0 a 100 su cinque aspetti: potenza, controllo, uscita palla, maneggevolezza e punto dolce. Il voto viene da dati del produttore, recensioni di analisti e opinioni di giocatori verificati; il sito dichiara di non provare ogni racchetta in laboratorio ({fonte(PF_M, "metodo Padelful")}). Classifica aggiornata a luglio 2026.</p>
{tab_pf}
<p class="note">Fonte: {fonte(PF, "Padelful, Mejores palas de pádel")}. Nel testo dell'articolo Padelful riporta anche voti da 1 a 10 che non sempre coincidono con quelli dei badge: qui usiamo i badge.</p>
<h2>La classifica di PadelVerdict</h2>
<p>PadelVerdict valuta otto parametri (potenza, effetto, controllo, stabilità, comfort, maneggevolezza, punto dolce, giocabilità) e li combina nel Verdict Score, con penalità se comfort o punto dolce sono sotto soglia e un correttivo basato sul confronto tra più fonti. Pubblica anche un punteggio per profilo di gioco. Non spiega se le prove sono in laboratorio o in campo. Classifica aggiornata ad aprile 2026.</p>
{"".join(blocchi)}
<p class="note">Fonte: {fonte(PV, "PadelVerdict, Mejores palas de pádel 2026")}.</p>
<h2>E le Adidas? I voti di PadelZoom</h2>
<p>Per le Adidas 2026 il nostro database contiene anche i voti di PadelZoom (scala da 1 a 10). Queste sono le cinque con il voto globale più alto:</p>
<div class="tablebox"><table class="tab"><thead><tr><th>Racchetta</th><th>Globale</th><th>Potenza</th><th>Controllo</th></tr></thead><tbody>{pz_rows}</tbody></table></div>
<p class="note">Fonte: padelzoom.es, voti riportati in ciascuna scheda.</p>
<h2>Come usare queste classifiche</h2>
<p>Quasi tutte le racchette in cima sono modelli per giocatori avanzati, con forma a diamante o goccia e voti di potenza alti. Se sei agli inizi o giochi soprattutto in difesa, guarda la sezione "controllo" di PadelVerdict o usa il nostro <a href="{P("selettore")}">selettore Trova la tua racchetta</a>.</p>
<p class="note">Entrambi i siti dichiarano di non accettare posizionamenti a pagamento e di usare link di affiliazione. PadelMetrix non ha rapporti con nessuno dei due.</p>""",
        f"""<p><b>Which are the best padel rackets of 2026? Instead of making yet another ranking, we combined those of two review sites that don't sell rackets: Padelful and PadelVerdict.</b> The only racket in both rankings is {ent_txt}: 8th on Padelful with 86/100 and 2nd on PadelVerdict with 9.0 (1st among attacking rackets). The other positions vary a lot from one source to the other, so a single ranking would be made up.</p>
<p>Watch the names: brands make several versions of the same model (for example the Metalbone HRD and HRD+, or the Viper Juan Lebrón and the Technical Viper). We kept them separate and linked to the PadelMetrix page only when the model is exactly the same.</p>
<h2>Padelful's ranking</h2>
<p>Padelful scores rackets from 0 to 100 on five aspects: power, control, ball exit, handling and sweet spot. Scores come from manufacturer data, analyst reviews and verified player opinions; the site says it does not test every racket in a lab ({fonte(PF_M, "Padelful method")}). Ranking updated July 2026.</p>
{tab_pf}
<p class="note">Source: {fonte(PF, "Padelful, Mejores palas de pádel")}. In the article text Padelful also gives 1–10 scores that don't always match the badges: we use the badges.</p>
<h2>PadelVerdict's ranking</h2>
<p>PadelVerdict rates eight parameters (power, spin, control, stability, comfort, handling, sweet spot, playability) and combines them into the Verdict Score, with penalties when comfort or sweet spot fall below a threshold and a correction based on cross-checking several sources. It also publishes a score per playing profile. It does not say whether tests are done in a lab or on court. Ranking updated April 2026.</p>
{"".join(blocchi)}
<p class="note">Source: {fonte(PV, "PadelVerdict, Mejores palas de pádel 2026")}.</p>
<h2>What about Adidas? PadelZoom's scores</h2>
<p>For 2026 Adidas rackets our database also holds PadelZoom's scores (1–10 scale). These are the five with the highest overall score:</p>
<div class="tablebox"><table class="tab"><thead><tr><th>Racket</th><th>Overall</th><th>Power</th><th>Control</th></tr></thead><tbody>{pz_rows}</tbody></table></div>
<p class="note">Source: padelzoom.es, scores listed on each spec page.</p>
<h2>How to use these rankings</h2>
<p>Almost all the top rackets are models for advanced players, diamond or teardrop shaped, with high power scores. If you are a beginner or mostly play defence, look at PadelVerdict's "control" section or use our <a href="{P("selettore")}">Find your racket selector</a>.</p>
<p class="note">Both sites state that they accept no paid placements and that they use affiliate links. PadelMetrix has no relationship with either.</p>""",
        f"""<p><b>¿Cuáles son las mejores palas de pádel de 2026? En vez de hacer otro ranking más, hemos juntado los de dos webs de análisis que no venden palas: Padelful y PadelVerdict.</b> La única pala presente en los dos rankings es {ent_txt}: 8ª en Padelful con 86/100 y 2ª en PadelVerdict con 9,0 (1ª entre las palas de ataque). Las demás posiciones cambian mucho de una fuente a otra, así que un ranking único sería inventado.</p>
<p>Ojo con los nombres: las marcas sacan varias versiones del mismo modelo (por ejemplo la Metalbone HRD y la HRD+, o la Viper Juan Lebrón y la Technical Viper). Las hemos mantenido separadas y enlazamos la ficha de PadelMetrix solo cuando el modelo es exactamente el mismo.</p>
<h2>El ranking de Padelful</h2>
<p>Padelful puntúa de 0 a 100 cinco aspectos: potencia, control, salida de bola, manejabilidad y punto dulce. La nota sale de datos del fabricante, análisis de expertos y opiniones de jugadores verificados; la web declara que no prueba cada pala en laboratorio ({fonte(PF_M, "método Padelful")}). Ranking actualizado en julio de 2026.</p>
{tab_pf}
<p class="note">Fuente: {fonte(PF, "Padelful, Mejores palas de pádel")}. En el texto del artículo Padelful da también notas de 1 a 10 que no siempre coinciden con las de las insignias: aquí usamos las insignias.</p>
<h2>El ranking de PadelVerdict</h2>
<p>PadelVerdict valora ocho parámetros (potencia, efecto, control, estabilidad, comodidad, manejabilidad, punto dulce, jugabilidad) y los combina en el Verdict Score, con penalizaciones si la comodidad o el punto dulce quedan por debajo de un umbral y un ajuste basado en el cruce de varias fuentes. También publica una puntuación por perfil de juego. No explica si las pruebas son en laboratorio o en pista. Ranking actualizado en abril de 2026.</p>
{"".join(blocchi)}
<p class="note">Fuente: {fonte(PV, "PadelVerdict, Mejores palas de pádel 2026")}.</p>
<h2>¿Y las Adidas? Las notas de PadelZoom</h2>
<p>Para las Adidas 2026 nuestra base de datos incluye también las notas de PadelZoom (escala de 1 a 10). Estas son las cinco con la nota global más alta:</p>
<div class="tablebox"><table class="tab"><thead><tr><th>Pala</th><th>Global</th><th>Potencia</th><th>Control</th></tr></thead><tbody>{pz_rows}</tbody></table></div>
<p class="note">Fuente: padelzoom.es, notas indicadas en cada ficha.</p>
<h2>Cómo usar estos rankings</h2>
<p>Casi todas las palas de arriba son modelos para jugadores avanzados, con forma diamante o lágrima y notas altas de potencia. Si estás empezando o juegas sobre todo en defensa, mira la sección "control" de PadelVerdict o usa nuestro <a href="{P("selettore")}">selector Encuentra tu pala</a>.</p>
<p class="note">Las dos webs declaran que no aceptan posiciones pagadas y que usan enlaces de afiliación. PadelMetrix no tiene relación con ninguna de ellas.</p>""", f"""<p><b>Quelles sont les meilleures raquettes de padel de 2026 ? Plutôt que de faire un énième classement, nous avons croisé ceux de deux sites de tests qui ne vendent pas de raquettes : Padelful et PadelVerdict.</b> La seule raquette présente dans les deux classements est la {ent_txt} : 8e sur Padelful avec 86/100 et 2e sur PadelVerdict avec 9,0 (1re parmi les raquettes d'attaque). Les autres positions varient beaucoup d'une source à l'autre : un classement unique serait donc inventé.</p>
<p>Attention aux noms : les marques font plusieurs versions du même modèle (par exemple la Metalbone HRD et HRD+, ou la Viper Juan Lebrón et la Technical Viper). Nous les avons gardées séparées et n'avons mis un lien vers la fiche PadelMetrix que quand le modèle est exactement le même.</p>
<h2>Le classement de Padelful</h2>
<p>Padelful note les raquettes de 0 à 100 sur cinq aspects : puissance, contrôle, sortie de balle, maniabilité et sweet spot. Les notes viennent des données des fabricants, des avis d'analystes et d'avis de joueurs vérifiés ; le site précise qu'il ne teste pas chaque raquette en laboratoire ({fonte(PF_M, "méthode Padelful")}). Classement mis à jour en juillet 2026.</p>
{tab_pf}
<p class="note">Source : {fonte(PF, "Padelful, Mejores palas de pádel")}. Dans le texte de l'article, Padelful donne aussi des notes de 1 à 10 qui ne correspondent pas toujours aux badges : nous utilisons les badges.</p>
<h2>Le classement de PadelVerdict</h2>
<p>PadelVerdict évalue huit paramètres (puissance, effet, contrôle, stabilité, confort, maniabilité, sweet spot, jouabilité) et les combine dans le Verdict Score, avec des pénalités quand le confort ou le sweet spot passent sous un seuil et une correction basée sur le recoupement de plusieurs sources. Il publie aussi une note par profil de jeu. Il ne précise pas si les tests sont faits en laboratoire ou sur le terrain. Classement mis à jour en avril 2026.</p>
{"".join(blocchi)}
<p class="note">Source : {fonte(PV, "PadelVerdict, Mejores palas de pádel 2026")}.</p>
<h2>Et Adidas ? Les notes de PadelZoom</h2>
<p>Pour les raquettes Adidas 2026, notre base contient aussi les notes de PadelZoom (échelle de 1 à 10). Voici les cinq avec la meilleure note globale :</p>
<div class="tablebox"><table class="tab"><thead><tr><th>Raquette</th><th>Globale</th><th>Puissance</th><th>Contrôle</th></tr></thead><tbody>{pz_rows}</tbody></table></div>
<p class="note">Source : padelzoom.es, notes indiquées sur chaque fiche.</p>
<h2>Comment utiliser ces classements</h2>
<p>Presque toutes les raquettes en tête sont des modèles pour joueurs avancés, en forme diamant ou goutte d'eau, avec des notes de puissance élevées. Si vous débutez ou jouez surtout en défense, regardez la section « contrôle » de PadelVerdict ou utilisez notre outil <a href="{P("selettore")}">Trouve ta raquette</a>.</p>
<p class="note">Les deux sites déclarent n'accepter aucun placement payant et utiliser des liens affiliés. PadelMetrix n'a aucun lien avec l'un ou l'autre.</p>""")
    qa = [(L("Qual è la migliore racchetta da padel del 2026?", "What is the best padel racket of 2026?", "¿Cuál es la mejor pala de pádel de 2026?", "Quelle est la meilleure raquette de padel de 2026 ?"),
           L("Non esiste una risposta unica: le classifiche indipendenti non concordano. L'unica racchetta presente sia nella top 10 di Padelful sia nella classifica generale di PadelVerdict è la StarVie Black Titan 2026, una racchetta d'attacco per giocatori avanzati.",
             "There is no single answer: independent rankings disagree. The only racket in both Padelful's top 10 and PadelVerdict's overall ranking is the StarVie Black Titan 2026, an attacking racket for advanced players.",
             "No hay una única respuesta: los rankings independientes no coinciden. La única pala presente tanto en el top 10 de Padelful como en el ranking general de PadelVerdict es la StarVie Black Titan 2026, una pala de ataque para jugadores avanzados.", "Il n'y a pas de réponse unique : les classements indépendants ne sont pas d'accord. La seule raquette présente à la fois dans le top 10 de Padelful et dans le classement général de PadelVerdict est la StarVie Black Titan 2026, une raquette d'attaque pour joueurs avancés.")),
          (L("Queste classifiche si basano su test di laboratorio?", "Are these rankings based on lab tests?", "¿Estos rankings se basan en pruebas de laboratorio?", "Ces classements reposent-ils sur des tests en laboratoire ?"),
           L("No. Padelful dichiara di combinare dati dei produttori, recensioni di esperti e opinioni di giocatori, senza prove di laboratorio; PadelVerdict non specifica come vengono fatte le prove.",
             "No. Padelful says it combines manufacturer data, expert reviews and player opinions, without lab tests; PadelVerdict does not specify how tests are done.",
             "No. Padelful declara que combina datos de fabricantes, análisis de expertos y opiniones de jugadores, sin pruebas de laboratorio; PadelVerdict no especifica cómo se hacen las pruebas.", "Non. Padelful indique combiner données des fabricants, avis d'experts et avis de joueurs, sans tests en laboratoire ; PadelVerdict ne précise pas comment les tests sont réalisés.")),
          (L("Qual è la migliore racchetta 2026 per il controllo?", "What is the best 2026 racket for control?", "¿Cuál es la mejor pala 2026 para control?", "Quelle est la meilleure raquette 2026 pour le contrôle ?"),
           L("Nella classifica per giocatori difensivi di PadelVerdict il primo posto va alla Nox ML10 Ventus Control 3K 2026 (8,8), seguita dalla Nox VK10 Ventus Control 12K 2026.",
             "In PadelVerdict's ranking for defensive players first place goes to the Nox ML10 Ventus Control 3K 2026 (8.8), followed by the Nox VK10 Ventus Control 12K 2026.",
             "En el ranking de PadelVerdict para jugadores defensivos el primer puesto es para la Nox ML10 Ventus Control 3K 2026 (8,8), seguida de la Nox VK10 Ventus Control 12K 2026.", "Dans le classement de PadelVerdict pour les joueurs défensifs, la première place revient à la Nox ML10 Ventus Control 3K 2026 (8,8), suivie de la Nox VK10 Ventus Control 12K 2026."))]
    faq_htm, faq_ld = faq(qa)
    corpo += faq_htm
    titolo = L("Le migliori racchette da padel 2026 secondo le classifiche indipendenti", "The best padel rackets of 2026 according to independent rankings",
               "Las mejores palas de pádel 2026 según los rankings independientes", "Les meilleures raquettes de padel de 2026 selon les classements indépendants")
    slugs = list(dict.fromkeys([s for _, s, *_ in PADELFUL if s] + [s for _, _, s, _, _ in VERDICT if s]))
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Le classifiche 2026 di Padelful e PadelVerdict a confronto, con voti, metodo e l'unica racchetta presente in entrambe.",
                      "Padelful's and PadelVerdict's 2026 rankings side by side, with scores, method and the only racket that appears in both.",
                      "Los rankings 2026 de Padelful y PadelVerdict comparados, con notas, método y la única pala presente en los dos.", "Les classements 2026 de Padelful et PadelVerdict côte à côte, avec notes, méthode et la seule raquette présente dans les deux."),
                    titolo, L("Migliori 2026", "Best of 2026", "Mejores 2026", "Meilleures de 2026"), corpo, items=[per[s] for s in slugs if s in per], ld_extra=[faq_ld])
    RACCHETTE_ARTICOLO[slug] = slugs
    return slug, titolo, L("Padelful e PadelVerdict a confronto: voti, metodo e l'unica racchetta in entrambe.", "Padelful and PadelVerdict side by side: scores, method and the one racket in both.",
                           "Padelful y PadelVerdict comparados: notas, método y la única pala en los dos.", "Padelful et PadelVerdict côte à côte : notes, méthode et la seule raquette présente dans les deux.")



# ---------------------------------------------------------------- 11. Regolamento del pickleball

PB_REG = "https://europeanpickleballfederation.org/wp-content/uploads/2026/04/2026-USAP-Official-Rulebook-–-EPF-Edition-–-Italian-Version.pdf"
PB_CHG = "https://pickleballcanada.org/wp-content/uploads/2026/04/2026-Rulebook-Change-Document-EN.pdf"


def pickleball_regole(db):
    import dati_pickleball as DP
    slug = "regolamento-pickleball-regole-spiegate"
    pad = DP.P
    approvate = [p for p in pad if p.get("approvazioni") and "USAP" in p["approvazioni"]]
    inizio = [p for p in pad if p["livello"] in ("principiante", "principiante-intermedio")]
    url_pb = P("pickleball")

    def pl(p):
        import genera_pickleball as GP
        return f'<a href="{P("pickleball", p["slug"])}">{e(GP.titolo(p))}</a>'

    inizio_txt = ", ".join(pl(p) for p in inizio[:5])
    reg, chg = fonte(PB_REG, L("Regolamento USA Pickleball 2026, edizione EPF in italiano", "2026 USA Pickleball Rulebook, EPF edition", "Reglamento USA Pickleball 2026, edición EPF", "USA Pickleball Rulebook 2026, édition EPF")), fonte(PB_CHG, L("documento delle modifiche 2026 (Pickleball Canada)", "2026 rule change document (Pickleball Canada)", "documento de cambios 2026 (Pickleball Canada)", "Document des changements de règles 2026 (Pickleball Canada)"))
    cta = L(f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Hai capito le regole e ti serve la racchetta?</b><br>Nella nostra sezione pickleball trovi {len(pad)} racchette di {len({p["marca"] for p in pad})} marche, con peso, spessore, forma, omologazioni e opinioni delle recensioni indipendenti.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_pb}">Vedi le racchette da pickleball →</a></div>''',
            f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Got the rules and need a paddle?</b><br>Our pickleball section lists {len(pad)} paddles from {len({p["marca"] for p in pad})} brands, with weight, thickness, shape, approvals and summaries of independent reviews.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_pb}">See the pickleball paddles →</a></div>''',
            f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>¿Ya conoces las reglas y necesitas pala?</b><br>En nuestra sección de pickleball tienes {len(pad)} palas de {len({p["marca"] for p in pad})} marcas, con peso, grosor, forma, homologaciones y resumen de las reseñas independientes.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_pb}">Ver las palas de pickleball →</a></div>''', f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Vous connaissez les règles et il vous faut une raquette ?</b><br>Notre section pickleball recense {len(pad)} raquettes de {len({p["marca"] for p in pad})} marques, avec poids, épaisseur, forme, homologations et résumés de tests indépendants.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_pb}">Voir les raquettes de pickleball →</a></div>''')
    corpo = L(f'''<p><b>Il pickleball si gioca su un campo da 13,41 × 6,10 m, con una rete più bassa al centro, una racchetta piatta e una pallina di plastica forata.</b> Le regole sono poche, ma tre sono diverse da tutti gli altri sport di racchetta: il servizio dal basso, la regola dei due rimbalzi e la "kitchen", la zona vicino alla rete in cui non si può colpire al volo. Questa guida le spiega una per una, seguendo il regolamento ufficiale USA Pickleball 2026, quello adottato anche dalla Federazione Europea (EPF).</p>
<h2>Le regole in breve</h2>
<ol>
<li>Si serve dal basso, in diagonale, e la palla deve superare la kitchen avversaria.</li>
<li>Servizio e risposta devono rimbalzare prima di essere colpiti: è la regola dei due rimbalzi.</li>
<li>Nella kitchen (2,13 m dalla rete) non si può colpire la palla al volo.</li>
<li>Con il punteggio tradizionale fa punto solo chi serve; si gioca a 11, con 2 punti di scarto.</li>
<li>Una palla che tocca la linea è buona, tranne il servizio che cade sulla linea della kitchen.</li>
</ol>
{cta}
<h2>Il campo e la rete</h2>
<p>Il campo misura <b>6,10 m di larghezza per 13,41 m di lunghezza</b> (20 × 44 piedi), uguale per singolare e doppio (regola 3.A.1). Vicino alla rete, su ciascun lato, c'è la <b>zona di non volée</b>, detta kitchen, profonda <b>2,13 m</b> (7 piedi). La rete è alta <b>91,44 cm ai lati e 86,36 cm al centro</b> (regole 3.B.6 e 3.B.7): più bassa del tennis, e infatti a rete si gioca molto.</p>
<h2>Il servizio</h2>
<p>Esistono due modi di servire.</p>
<ul>
<li><b>Servizio al volo</b> (regola 7.C): al momento del contatto la racchetta deve muoversi chiaramente dal basso verso l'alto, la testa della racchetta non può essere sopra il polso e la palla va colpita non più in alto della vita. Si può servire di dritto o di rovescio.</li>
<li><b>Servizio a rimbalzo</b> (regola 7.D): si lascia cadere la palla da un'altezza naturale, senza spingerla, e la si colpisce dopo il rimbalzo. In questo caso non contano né il movimento del braccio né l'altezza del contatto.</li>
</ul>
<p>Al momento del colpo almeno un piede deve essere a terra dietro la linea di fondo, dentro l'area di battuta (7.A). La palla va servita <b>in diagonale</b> e deve superare la kitchen avversaria (7.E). Dal 2026 la rotazione si può dare solo con la racchetta al momento del contatto, non con la mano mentre si lascia la palla (7.B.2).</p>
<h2>La regola dei due rimbalzi</h2>
<p>Il servizio deve rimbalzare nel campo di chi risponde, e la risposta deve rimbalzare nel campo di chi ha servito. Solo dopo questi due rimbalzi si può colpire al volo (regola 10.A). Serve a evitare che chi serve corra subito a rete e chiuda il punto: per questo i primi colpi di ogni scambio sono quasi sempre da fondo campo.</p>
<h2>La kitchen, o zona di non volée</h2>
<p>Dentro la kitchen non si può colpire la palla al volo (regola 11.A). Si può entrare quando si vuole, per esempio per giocare una palla che ha già rimbalzato. Sono fallo:</p>
<ul>
<li>toccare la kitchen, linea compresa, mentre si colpisce al volo;</li>
<li>finirci dentro per lo slancio dopo un colpo al volo, anche se la palla è già morta;</li>
<li>colpire al volo prima di essere usciti dalla kitchen con entrambi i piedi.</li>
</ul>
<h2>Il punteggio</h2>
<p>Con il punteggio tradizionale <b>fa punto solo la squadra che serve</b> (regola 4.A). La partita, o game, va a 11 punti con almeno 2 di scarto (4.B). Nel doppio il punteggio si chiama con <b>tre numeri</b>: punti di chi serve, punti di chi riceve e numero del battitore, 1 o 2. La partita inizia con <b>"zero – zero – due"</b> perché la squadra che serve per prima ha a disposizione un solo battitore (6.B.2). Negli scambi successivi servono entrambi i giocatori: quando la squadra perde lo scambio con il primo battitore, serve il compagno; quando perde anche con il secondo, il servizio passa agli avversari (5.B).</p>
<p>Nel 2026 il regolamento prevede anche, in via provvisoria, il <b>rally scoring</b>: chi vince lo scambio fa punto, anche se stava rispondendo (14.A.2). Lo decide l'organizzatore del torneo.</p>
<h2>Palla dentro o fuori</h2>
<p>La palla che tocca una linea è <b>buona</b>, con un'eccezione: il servizio che cade sulla linea della kitchen è fuori (8.C). Per chiamare "fuori" si deve vedere spazio tra palla e linea (8.E), e la chiamata va fatta subito, a voce o con un gesto (8.F). Se due compagni non sono d'accordo, la palla è considerata dentro (8.H). Gli spettatori non possono essere consultati (8.J).</p>
<h2>I falli più comuni</h2>
<ul>
<li>la palla esce dal campo o non supera la rete (10.C);</li>
<li>la palla colpisce un giocatore o i suoi vestiti; la mano sotto il polso conta come racchetta (10.C.3);</li>
<li>colpire la palla due volte, o colpirla con entrambi i giocatori della stessa squadra (10.D);</li>
<li>toccare la rete o i pali mentre la palla è in gioco (13.G);</li>
<li>colpire al volo nella kitchen (11.A).</li>
</ul>
<h2>La racchetta: cosa dice il regolamento</h2>
<p>La racchetta da pickleball, chiamata anche paddle, è piatta e senza fori. Il regolamento fissa poche misure (regola 3.D):</p>
<ul>
<li>lunghezza massima <b>43,18 cm</b> (17 pollici);</li>
<li>lunghezza più larghezza, bordo e tappo del manico compresi, al massimo <b>60,96 cm</b> (24 pollici);</li>
<li>nessun limite di peso né di spessore;</li>
<li>superficie liscia e non riflettente: niente fori, gomma o superfici ruvide che aumentino l'effetto (3.D.5);</li>
<li>nei tornei serve un modello omologato "USA Pickleball Approved", con il marchio visibile (3.D.1).</li>
</ul>
<p>Per giocare con gli amici l'omologazione non serve. Delle {len(pad)} racchette nella <a href="{url_pb}">nostra sezione pickleball</a>, {len(approvate)} risultano omologate USA Pickleball. Se sei agli inizi, guarda quelle pensate per chi comincia: {inizio_txt}.</p>
<p class="note">Fonti: {reg}; {chg}. Il regolamento completo prevede anche regole per arbitri, tornei, wheelchair e giocatori con disabilità, che qui non trattiamo.</p>''',
              f'''<p><b>Pickleball is played on a 44 × 20 ft court, with a net that dips in the middle, a flat paddle and a perforated plastic ball.</b> The rules are few, but three are unlike any other racket sport: the underhand serve, the two-bounce rule and the "kitchen", the area near the net where you cannot volley. This guide explains them one by one, following the official 2026 USA Pickleball Rulebook, also adopted by the European Pickleball Federation (EPF).</p>
<h2>The rules in short</h2>
<ol>
<li>Serve underhand, diagonally, and clear the opponents' kitchen.</li>
<li>The serve and the return must bounce before being hit: the two-bounce rule.</li>
<li>You cannot volley inside the kitchen (7 ft from the net).</li>
<li>With traditional scoring only the serving side scores; games go to 11, win by 2.</li>
<li>A ball touching a line is in, except a serve landing on the kitchen line.</li>
</ol>
{cta}
<h2>The court and the net</h2>
<p>The court is <b>20 ft wide and 44 ft long</b> (6.10 × 13.41 m), the same for singles and doubles (rule 3.A.1). Next to the net on each side is the <b>non-volley zone</b>, or kitchen, <b>7 ft</b> deep. The net is <b>36 in high at the sidelines and 34 in at the centre</b> (rules 3.B.6 and 3.B.7): lower than tennis, which is why so much of the game is played at the net.</p>
<h2>The serve</h2>
<p>There are two ways to serve.</p>
<ul>
<li><b>Volley serve</b> (rule 7.C): at contact the paddle must move in a clear upward arc, the paddle head cannot be above the wrist and the ball must be hit no higher than the waist. Forehand or backhand are both allowed.</li>
<li><b>Drop serve</b> (rule 7.D): drop the ball from a natural height, without pushing it, and hit it after the bounce. Arm motion and contact height do not matter in this case.</li>
</ul>
<p>At contact at least one foot must be on the ground behind the baseline, inside the serving area (7.A). The serve goes <b>diagonally</b> and must clear the opponents' kitchen (7.E). From 2026 spin may only be added by the paddle at contact, not by the hand when releasing the ball (7.B.2).</p>
<h2>The two-bounce rule</h2>
<p>The serve must bounce in the receiver's court, and the return must bounce in the server's court. Only after these two bounces can players volley (rule 10.A). It stops the server from rushing the net and ending the point at once, which is why the first shots of every rally are almost always from the baseline.</p>
<h2>The kitchen, or non-volley zone</h2>
<p>You cannot volley inside the kitchen (rule 11.A). You can step in whenever you like, for example to play a ball that has already bounced. These are faults:</p>
<ul>
<li>touching the kitchen, line included, while volleying;</li>
<li>being carried into it by momentum after a volley, even if the ball is already dead;</li>
<li>volleying before both feet are back out of the kitchen.</li>
</ul>
<h2>Scoring</h2>
<p>With traditional scoring <b>only the serving side scores</b> (rule 4.A). A game goes to 11 points, win by 2 (4.B). In doubles the score is called with <b>three numbers</b>: server's score, receiver's score and server number, 1 or 2. A game starts at <b>"zero – zero – two"</b> because the first serving side gets only one server (6.B.2). After that both players serve: when the side loses a rally with the first server, the partner serves; when it loses with the second server too, the serve passes to the opponents (5.B).</p>
<p>In 2026 the rulebook also includes provisional <b>rally scoring</b>: whoever wins the rally scores, even when receiving (14.A.2). The tournament director decides whether to use it.</p>
<h2>In or out</h2>
<p>A ball touching a line is <b>in</b>, with one exception: a serve landing on the kitchen line is out (8.C). To call "out" there must be visible space between ball and line (8.E), and the call must be made promptly, by voice or hand signal (8.F). If partners disagree, the ball is in (8.H). Spectators cannot be consulted (8.J).</p>
<h2>The most common faults</h2>
<ul>
<li>the ball lands out or fails to clear the net (10.C);</li>
<li>the ball hits a player or their clothing; the hand below the wrist counts as the paddle (10.C.3);</li>
<li>hitting the ball twice, or both partners hitting it (10.D);</li>
<li>touching the net or posts while the ball is in play (13.G);</li>
<li>volleying inside the kitchen (11.A).</li>
</ul>
<h2>The paddle: what the rules say</h2>
<p>A pickleball paddle is flat and has no holes. The rules set only a few limits (rule 3.D):</p>
<ul>
<li>maximum length <b>17 in</b> (43.18 cm);</li>
<li>length plus width, edge guard and butt cap included, no more than <b>24 in</b> (60.96 cm);</li>
<li>no limit on weight or thickness;</li>
<li>a smooth, non-reflective surface: no holes, rubber or rough textures that add spin (3.D.5);</li>
<li>tournaments require a "USA Pickleball Approved" model with visible markings (3.D.1).</li>
</ul>
<p>For casual play approval is not needed. Of the {len(pad)} paddles in <a href="{url_pb}">our pickleball section</a>, {len(approvate)} are USA Pickleball approved. If you are just starting, look at the beginner-friendly ones: {inizio_txt}.</p>
<p class="note">Sources: {reg}; {chg}. The full rulebook also covers referees, tournaments, wheelchair and adaptive play, which are not covered here.</p>''',
              f'''<p><b>El pickleball se juega en una pista de 13,41 × 6,10 m, con una red más baja en el centro, una pala plana y una pelota de plástico perforada.</b> Las reglas son pocas, pero tres son distintas de cualquier otro deporte de raqueta: el saque por abajo, la regla de los dos botes y la "kitchen", la zona junto a la red donde no se puede volear. Esta guía las explica una a una, siguiendo el reglamento oficial USA Pickleball 2026, adoptado también por la Federación Europea (EPF).</p>
<h2>Las reglas en breve</h2>
<ol>
<li>Se saca por abajo, en diagonal, y la pelota debe superar la kitchen rival.</li>
<li>El saque y el resto deben botar antes de golpearse: es la regla de los dos botes.</li>
<li>Dentro de la kitchen (2,13 m desde la red) no se puede volear.</li>
<li>Con el tanteo tradicional solo puntúa quien saca; se juega a 11, con 2 de diferencia.</li>
<li>La pelota que toca la línea es buena, salvo el saque que cae en la línea de la kitchen.</li>
</ol>
{cta}
<h2>La pista y la red</h2>
<p>La pista mide <b>6,10 m de ancho por 13,41 m de largo</b> (20 × 44 pies), igual para individuales y dobles (regla 3.A.1). Junto a la red, a cada lado, está la <b>zona de no volea</b> o kitchen, de <b>2,13 m</b> (7 pies) de profundidad. La red mide <b>91,44 cm en los laterales y 86,36 cm en el centro</b> (reglas 3.B.6 y 3.B.7): más baja que en el tenis, y por eso se juega tanto en la red.</p>
<h2>El saque</h2>
<p>Hay dos formas de sacar.</p>
<ul>
<li><b>Saque de volea</b> (regla 7.C): en el contacto la pala debe moverse claramente de abajo arriba, la cabeza de la pala no puede estar por encima de la muñeca y la pelota se golpea como máximo a la altura de la cintura. Se puede sacar de derecha o de revés.</li>
<li><b>Saque con bote</b> (regla 7.D): se deja caer la pelota desde una altura natural, sin impulsarla, y se golpea tras el bote. En este caso no cuentan ni el movimiento del brazo ni la altura del contacto.</li>
</ul>
<p>En el contacto al menos un pie debe estar en el suelo detrás de la línea de fondo, dentro de la zona de saque (7.A). El saque va <b>en diagonal</b> y debe superar la kitchen rival (7.E). Desde 2026 el efecto solo puede darse con la pala en el contacto, no con la mano al soltar la pelota (7.B.2).</p>
<h2>La regla de los dos botes</h2>
<p>El saque debe botar en el campo de quien resta, y el resto debe botar en el campo de quien sacó. Solo después de esos dos botes se puede volear (regla 10.A). Evita que quien saca suba a la red y cierre el punto enseguida: por eso los primeros golpes de cada punto casi siempre son desde el fondo.</p>
<h2>La kitchen, o zona de no volea</h2>
<p>Dentro de la kitchen no se puede volear (regla 11.A). Se puede entrar cuando se quiera, por ejemplo para jugar una pelota que ya ha botado. Son falta:</p>
<ul>
<li>tocar la kitchen, línea incluida, mientras se volea;</li>
<li>entrar en ella por la inercia tras una volea, aunque la pelota ya esté muerta;</li>
<li>volear antes de haber salido de la kitchen con los dos pies.</li>
</ul>
<h2>El tanteo</h2>
<p>Con el tanteo tradicional <b>solo puntúa el equipo que saca</b> (regla 4.A). El juego va a 11 puntos con al menos 2 de diferencia (4.B). En dobles el tanteo se canta con <b>tres números</b>: puntos de quien saca, puntos de quien resta y número del sacador, 1 o 2. El juego empieza con <b>"cero – cero – dos"</b> porque el primer equipo que saca solo tiene un sacador (6.B.2). Después sacan los dos jugadores: cuando el equipo pierde el punto con el primer sacador, saca el compañero; cuando lo pierde también con el segundo, el saque pasa a los rivales (5.B).</p>
<p>En 2026 el reglamento incluye también, de forma provisional, el <b>rally scoring</b>: quien gana el punto suma, aunque estuviera restando (14.A.2). Lo decide el organizador del torneo.</p>
<h2>Pelota dentro o fuera</h2>
<p>La pelota que toca una línea es <b>buena</b>, con una excepción: el saque que cae en la línea de la kitchen es fuera (8.C). Para cantar "fuera" debe verse espacio entre la pelota y la línea (8.E), y hay que cantarlo enseguida, de viva voz o con un gesto (8.F). Si los compañeros no están de acuerdo, la pelota es buena (8.H). No se puede consultar al público (8.J).</p>
<h2>Las faltas más comunes</h2>
<ul>
<li>la pelota sale de la pista o no pasa la red (10.C);</li>
<li>la pelota golpea a un jugador o su ropa; la mano por debajo de la muñeca cuenta como pala (10.C.3);</li>
<li>golpear la pelota dos veces, o que la golpeen los dos jugadores del mismo equipo (10.D);</li>
<li>tocar la red o los postes con la pelota en juego (13.G);</li>
<li>volear dentro de la kitchen (11.A).</li>
</ul>
<h2>La pala: qué dice el reglamento</h2>
<p>La pala de pickleball, también llamada paddle, es plana y sin agujeros. El reglamento fija pocas medidas (regla 3.D):</p>
<ul>
<li>longitud máxima <b>43,18 cm</b> (17 pulgadas);</li>
<li>longitud más anchura, protector y tapón incluidos, como máximo <b>60,96 cm</b> (24 pulgadas);</li>
<li>sin límite de peso ni de grosor;</li>
<li>superficie lisa y no reflectante: sin agujeros, goma ni texturas rugosas que aumenten el efecto (3.D.5);</li>
<li>en torneos se exige un modelo homologado "USA Pickleball Approved", con la marca visible (3.D.1).</li>
</ul>
<p>Para jugar con amigos la homologación no hace falta. De las {len(pad)} palas de <a href="{url_pb}">nuestra sección de pickleball</a>, {len(approvate)} están homologadas por USA Pickleball. Si estás empezando, mira las pensadas para principiantes: {inizio_txt}.</p>
<p class="note">Fuentes: {reg}; {chg}. El reglamento completo incluye también normas para árbitros, torneos, silla de ruedas y jugadores con discapacidad, que aquí no tratamos.</p>''', f'''<p><b>Le pickleball se joue sur un terrain de 44 × 20 pieds (13,41 × 6,10 m), avec un filet qui s'abaisse au centre, une raquette pleine et une balle en plastique perforée.</b> Les règles sont peu nombreuses, mais trois ne ressemblent à aucun autre sport de raquette : le service à la cuillère, la règle des deux rebonds et la « kitchen », la zone près du filet où l'on ne peut pas jouer de volée. Ce guide les explique une par une, d'après le règlement officiel USA Pickleball 2026, adopté aussi par la Fédération européenne de pickleball (EPF).</p>
<h2>Les règles en bref</h2>
<ol>
<li>Servez à la cuillère, en diagonale, en dépassant la kitchen adverse.</li>
<li>Le service et le retour doivent rebondir avant d'être frappés : c'est la règle des deux rebonds.</li>
<li>On ne peut pas jouer de volée dans la kitchen (7 pieds, soit 2,13 m, depuis le filet).</li>
<li>Avec le comptage traditionnel, seule l'équipe au service marque ; les jeux se jouent en 11 points, avec 2 points d'écart.</li>
<li>Une balle qui touche une ligne est bonne, sauf un service qui tombe sur la ligne de la kitchen.</li>
</ol>
{cta}
<h2>Le terrain et le filet</h2>
<p>Le terrain mesure <b>20 pieds de large et 44 pieds de long</b> (6,10 × 13,41 m), le même en simple et en double (règle 3.A.1). Contre le filet, de chaque côté, se trouve la <b>zone de non-volée</b>, ou kitchen, profonde de <b>7 pieds</b> (2,13 m). Le filet mesure <b>36 pouces aux poteaux et 34 pouces au centre</b> (91,4 et 86,4 cm, règles 3.B.6 et 3.B.7) : plus bas qu'au tennis, c'est pourquoi une si grande partie du jeu se déroule au filet.</p>
<h2>Le service</h2>
<p>Il existe deux façons de servir.</p>
<ul>
<li><b>Service de volée</b> (règle 7.C) : à l'impact, la raquette doit suivre un arc clairement ascendant, la tête de la raquette ne peut pas être au-dessus du poignet et la balle doit être frappée au plus à hauteur de la taille. Coup droit ou revers sont tous deux autorisés.</li>
<li><b>Service après rebond</b> (drop serve, règle 7.D) : lâchez la balle d'une hauteur naturelle, sans la pousser, et frappez-la après le rebond. Dans ce cas, le mouvement du bras et la hauteur d'impact n'ont pas d'importance.</li>
</ul>
<p>À l'impact, au moins un pied doit être au sol derrière la ligne de fond, dans la zone de service (7.A). Le service se joue <b>en diagonale</b> et doit dépasser la kitchen adverse (7.E). Depuis 2026, l'effet ne peut être donné que par la raquette à l'impact, pas par la main au moment de lâcher la balle (7.B.2).</p>
<h2>La règle des deux rebonds</h2>
<p>Le service doit rebondir dans le camp du relanceur, et le retour doit rebondir dans le camp du serveur. Ce n'est qu'après ces deux rebonds que les joueurs peuvent jouer de volée (règle 10.A). Cela empêche le serveur de monter au filet et de conclure le point aussitôt : c'est pourquoi les premiers coups de chaque échange se jouent presque toujours du fond.</p>
<h2>La kitchen, ou zone de non-volée</h2>
<p>On ne peut pas jouer de volée dans la kitchen (règle 11.A). On peut y entrer quand on veut, par exemple pour jouer une balle qui a déjà rebondi. Sont des fautes :</p>
<ul>
<li>toucher la kitchen, ligne comprise, en jouant une volée ;</li>
<li>y être emporté par l'élan après une volée, même si la balle est déjà morte ;</li>
<li>jouer une volée avant d'avoir les deux pieds ressortis de la kitchen.</li>
</ul>
<h2>Le comptage des points</h2>
<p>Avec le comptage traditionnel, <b>seule l'équipe au service marque</b> (règle 4.A). Un jeu se joue en 11 points, avec 2 points d'écart (4.B). En double, le score s'annonce avec <b>trois nombres</b> : score du serveur, score du relanceur et numéro du serveur, 1 ou 2. Un jeu commence à <b>« zéro – zéro – deux »</b> car la première équipe au service n'a qu'un seul serveur (6.B.2). Ensuite, les deux joueurs servent : quand l'équipe perd un échange avec le premier serveur, c'est le partenaire qui sert ; quand elle le perd aussi avec le second serveur, le service passe aux adversaires (5.B).</p>
<p>En 2026, le règlement prévoit aussi, à titre provisoire, le <b>rally scoring</b> : celui qui gagne l'échange marque, même en retour (14.A.2). C'est le directeur du tournoi qui décide de l'utiliser.</p>
<h2>Bonne ou faute</h2>
<p>Une balle qui touche une ligne est <b>bonne</b>, avec une exception : un service qui tombe sur la ligne de la kitchen est faute (8.C). Pour annoncer « out », il faut un espace visible entre la balle et la ligne (8.E), et l'annonce doit être faite rapidement, de la voix ou d'un signe de la main (8.F). Si les partenaires ne sont pas d'accord, la balle est bonne (8.H). Les spectateurs ne peuvent pas être consultés (8.J).</p>
<h2>Les fautes les plus courantes</h2>
<ul>
<li>la balle tombe dehors ou ne passe pas le filet (10.C) ;</li>
<li>la balle touche un joueur ou ses vêtements ; la main sous le poignet compte comme la raquette (10.C.3) ;</li>
<li>frapper la balle deux fois, ou que les deux partenaires la frappent (10.D) ;</li>
<li>toucher le filet ou les poteaux pendant que la balle est en jeu (13.G) ;</li>
<li>jouer une volée dans la kitchen (11.A).</li>
</ul>
<h2>La raquette : ce que dit le règlement</h2>
<p>Une raquette de pickleball est pleine et n'a pas de trous. Le règlement ne fixe que quelques limites (règle 3.D) :</p>
<ul>
<li>longueur maximale <b>17 pouces</b> (43,18 cm) ;</li>
<li>longueur plus largeur, protège-cadre et embout compris, pas plus de <b>24 pouces</b> (60,96 cm) ;</li>
<li>aucune limite de poids ni d'épaisseur ;</li>
<li>une surface lisse et non réfléchissante : pas de trous, de caoutchouc ni de textures rugueuses qui ajoutent de l'effet (3.D.5) ;</li>
<li>les tournois exigent un modèle « USA Pickleball Approved » avec marquages visibles (3.D.1).</li>
</ul>
<p>Pour jouer en loisir, l'homologation n'est pas nécessaire. Sur les {len(pad)} raquettes de <a href="{url_pb}">notre section pickleball</a>, {len(approvate)} sont homologuées USA Pickleball. Si vous débutez, regardez celles adaptées aux débutants : {inizio_txt}.</p>
<p class="note">Sources : {reg} ; {chg}. Le règlement complet traite aussi de l'arbitrage, des tournois, du jeu en fauteuil et du jeu adapté, qui ne sont pas abordés ici.</p>''')
    corpo += cta
    qa = [(L("Il servizio nel pickleball si fa dal basso?", "Is the pickleball serve underhand?", "¿El saque de pickleball es por abajo?", "Le service au pickleball se fait-il à la cuillère ?"),
           L("Sì. Nel servizio al volo la racchetta deve salire dal basso verso l'alto, la sua testa non può superare il polso e la palla va colpita sotto la vita. In alternativa si può fare il servizio a rimbalzo, lasciando cadere la palla e colpendola dopo il rimbalzo.",
             "Yes. On a volley serve the paddle must move upward, its head cannot be above the wrist and the ball must be hit below the waist. Alternatively you can use the drop serve, letting the ball bounce before hitting it.",
             "Sí. En el saque de volea la pala debe subir de abajo arriba, su cabeza no puede superar la muñeca y la pelota se golpea por debajo de la cintura. También se puede hacer el saque con bote, dejando caer la pelota y golpeándola tras el bote.", "Oui. Pour un service de volée, la raquette doit monter, sa tête ne peut pas être au-dessus du poignet et la balle doit être frappée sous la taille. Sinon, on peut utiliser le service après rebond, en laissant la balle rebondir avant de la frapper.")),
          (L("Cos'è la kitchen nel pickleball?", "What is the kitchen in pickleball?", "¿Qué es la kitchen en el pickleball?", "Qu'est-ce que la kitchen au pickleball ?"),
           L("È la zona di non volée: 2,13 metri di campo su ciascun lato della rete in cui non si può colpire la palla al volo. Ci si può entrare per giocare palle che hanno già rimbalzato.",
             "It is the non-volley zone: 7 feet of court on each side of the net where you cannot volley. You may step in to play balls that have already bounced.",
             "Es la zona de no volea: 2,13 metros de pista a cada lado de la red donde no se puede volear. Se puede entrar para jugar pelotas que ya han botado.", "C'est la zone de non-volée : 7 pieds (2,13 m) de terrain de chaque côté du filet où l'on ne peut pas jouer de volée. On peut y entrer pour jouer des balles qui ont déjà rebondi.")),
          (L("A quanti punti si gioca a pickleball?", "How many points is a pickleball game?", "¿A cuántos puntos se juega al pickleball?", "En combien de points se joue un jeu de pickleball ?"),
           L("Di solito a 11, con almeno 2 punti di scarto. Con il punteggio tradizionale fa punto solo chi serve; alcuni tornei usano il rally scoring, in cui ogni scambio vale un punto.",
             "Usually to 11, win by 2. With traditional scoring only the serving side scores; some tournaments use rally scoring, where every rally is worth a point.",
             "Normalmente a 11, con al menos 2 puntos de diferencia. Con el tanteo tradicional solo puntúa quien saca; algunos torneos usan el rally scoring, en el que cada punto cuenta.", "En général en 11 points, avec 2 points d'écart. Avec le comptage traditionnel, seule l'équipe au service marque ; certains tournois utilisent le rally scoring, où chaque échange vaut un point.")),
          (L("Quanto è grande un campo da pickleball?", "How big is a pickleball court?", "¿Cuánto mide una pista de pickleball?", "Quelles sont les dimensions d'un terrain de pickleball ?"),
           L("13,41 metri per 6,10 (44 × 20 piedi), sia per il singolare sia per il doppio. La rete è alta 91,44 cm ai lati e 86,36 cm al centro.",
             "44 by 20 feet (13.41 × 6.10 m), for both singles and doubles. The net is 36 inches high at the sidelines and 34 inches at the centre.",
             "13,41 por 6,10 metros (44 × 20 pies), tanto en individuales como en dobles. La red mide 91,44 cm en los laterales y 86,36 cm en el centro.", "44 pieds sur 20 (13,41 × 6,10 m), en simple comme en double. Le filet mesure 36 pouces (91,4 cm) aux poteaux et 34 pouces (86,4 cm) au centre.")),
          (L("Serve una racchetta omologata per giocare?", "Do I need an approved paddle to play?", "¿Hace falta una pala homologada para jugar?", "Faut-il une raquette homologuée pour jouer ?"),
           L("Solo nei tornei ufficiali, dove serve un modello USA Pickleball Approved. Per giocare per divertimento va bene qualsiasi racchetta da pickleball.",
             "Only in official tournaments, which require a USA Pickleball Approved model. For casual play any pickleball paddle will do.",
             "Solo en torneos oficiales, donde se exige un modelo USA Pickleball Approved. Para jugar por diversión vale cualquier pala de pickleball.", "Seulement dans les tournois officiels, qui exigent un modèle USA Pickleball Approved. Pour jouer en loisir, n'importe quelle raquette de pickleball convient."))]
    faq_htm, faq_ld = faq(qa)
    corpo += faq_htm
    titolo = L("Regolamento del pickleball 2026: le regole spiegate semplici", "Pickleball rules 2026: the rules explained simply", "Reglamento del pickleball 2026: las reglas explicadas fácil", "Règles du pickleball 2026 : les règles expliquées simplement")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Le regole del pickleball secondo il regolamento ufficiale 2026: campo, servizio dal basso, regola dei due rimbalzi, kitchen, punteggio, falli e misure della racchetta.",
                      "Pickleball rules from the official 2026 rulebook: court, underhand serve, two-bounce rule, kitchen, scoring, faults and paddle limits.",
                      "Las reglas del pickleball según el reglamento oficial 2026: pista, saque por abajo, regla de los dos botes, kitchen, tanteo, faltas y medidas de la pala.", "Les règles du pickleball d'après le règlement officiel 2026 : terrain, service à la cuillère, règle des deux rebonds, kitchen, comptage des points, fautes et limites de la raquette."),
                    titolo, L("Regolamento pickleball", "Pickleball rules", "Reglamento pickleball", "Règles du pickleball"), corpo, ld_extra=[faq_ld])
    return slug, titolo, L("Campo, servizio, due rimbalzi, kitchen e punteggio, secondo il regolamento 2026.", "Court, serve, two bounces, kitchen and scoring, per the 2026 rulebook.",
                           "Pista, saque, dos botes, kitchen y tanteo, según el reglamento 2026.", "Terrain, service, deux rebonds, kitchen et comptage des points, d'après le règlement 2026.")



# ---------------------------------------------------------------- 12. Regolamento del padel

PD_REG = "https://www.padelfip.com/wp-content/uploads/2025/12/FIP_Reglas-del-Padel.pdf"
PD_STAR = "https://www.padelfip.com/wp-content/uploads/2025/12/18-diciembre_Star-Point_ESP.pdf"


def padel_regole(db):
    slug = "regolamento-padel-regole-spiegate"
    adulti = [n for n in db if n["categoria"] != "junior"]
    inizio = [n for n in adulti if n["livello"] in ("principiante", "principiante-intermedio")]
    url_r_all, url_sel = P("racchette"), P("selettore")
    reg = fonte(PD_REG, L("Regolamento del padel FIP, revisione in vigore dal 1° gennaio 2026", "FIP Padel Rules, revision in force from 1 January 2026", "Reglas del Pádel FIP, revisión en vigor desde el 1 de enero de 2026", "Règlement du padel FIP, révision en vigueur depuis le 1er janvier 2026"))
    star = fonte(PD_STAR, L("comunicato FIP sullo Star Point", "FIP Star Point announcement", "comunicado FIP sobre el Star Point", "Annonce du Star Point par la FIP"))
    box = lambda: L(f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Regole chiare? Ora scegli la racchetta giusta.</b><br>Nel nostro database ci sono {len(adulti)} racchette da padel 2026 e 2027, con forma, peso, bilanciamento e voti delle recensioni indipendenti. Se non sai da dove partire, il test ti consiglia in 2 minuti.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_sel}">Fai il test</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{url_r_all}">Vedi tutte le racchette →</a></div>''',
                    f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Rules clear? Now pick the right racket.</b><br>Our database has {len(adulti)} 2026 and 2027 padel rackets, with shape, weight, balance and independent review scores. Not sure where to start? The quiz gives you a recommendation in 2 minutes.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_sel}">Take the quiz</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{url_r_all}">See all rackets →</a></div>''',
                    f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>¿Reglas claras? Ahora elige la pala adecuada.</b><br>En nuestra base de datos hay {len(adulti)} palas de pádel 2026 y 2027, con forma, peso, balance y notas de las reseñas independientes. Si no sabes por dónde empezar, el test te recomienda en 2 minutos.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_sel}">Haz el test</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{url_r_all}">Ver todas las palas →</a></div>''', f'''<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Les règles sont claires ? Choisissez maintenant la bonne raquette.</b><br>Notre base contient {len(adulti)} raquettes de padel 2026 et 2027, avec forme, poids, équilibre et notes de tests indépendants. Vous ne savez pas par où commencer ? Le quiz vous donne une recommandation en 2 minutes.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{url_sel}">Faire le quiz</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{url_r_all}">Voir toutes les raquettes →</a></div>''')
    corpo = L(f'''<p><b>Il padel si gioca in doppio su un campo di 20 × 10 metri chiuso da pareti, con una rete alta 88 cm al centro e una pallina simile a quella del tennis.</b> Le pareti sono la vera differenza: la palla può rimbalzarci contro e restare in gioco. Questa guida spiega le regole una per una seguendo il regolamento ufficiale della Federazione Internazionale (FIP), nella revisione in vigore dal 1° gennaio 2026, con le novità di quest'anno come lo Star Point.</p>
<h2>Le regole in breve</h2>
<ol>
<li>Si serve dal basso: la palla rimbalza a terra e va colpita all'altezza della vita o più in basso, in diagonale.</li>
<li>Per ogni punto hai due servizi, come nel tennis.</li>
<li>La palla deve rimbalzare prima nel campo avversario; dopo può toccare pareti e rete metallica.</li>
<li>Si risponde prima del secondo rimbalzo a terra, anche dopo che la palla ha toccato le pareti del proprio campo.</li>
<li>Punteggio come nel tennis: 15, 30, 40, gioco; set a 6 giochi, partita al meglio dei 3 set.</li>
</ol>
{box()}
<h2>Il campo, la rete e la pallina</h2>
<p>Il campo misura <b>20 metri di lunghezza per 10 di larghezza</b>. Sul fondo ci sono pareti alte 3 metri sormontate da 1 metro di rete metallica, per un totale di 4 metri; ai lati pareti e rete metallica seguono uno schema a gradini. La rete è alta <b>88 cm al centro e fino a 92 cm alle estremità</b>. La pallina ha un diametro tra 6,35 e 6,77 cm e pesa tra 56 e 59,4 grammi, con un rimbalzo un po' più basso di quella da tennis.</p>
<h2>Il servizio</h2>
<p>Il servizio è la regola che crea più dubbi (regola 6):</p>
<ul>
<li>chi serve ha almeno un piede sulla linea di servizio o dietro, nella metà campo tra la linea centrale e la parete laterale;</li>
<li>lascia rimbalzare la palla a terra dietro la linea, poi la colpisce;</li>
<li>al momento del colpo la palla deve essere <b>all'altezza della vita o più in basso</b>, con almeno un piede a terra;</li>
<li>la palla deve passare la rete <b>in diagonale</b> e rimbalzare nel riquadro di servizio avversario;</li>
<li>se il primo servizio è sbagliato, c'è il <b>secondo</b>.</li>
</ul>
<p>Dopo il rimbalzo nel riquadro giusto la palla può toccare la parete di vetro, ma se tocca la rete metallica (la "griglia") prima del secondo rimbalzo il servizio è fallo. Se la palla tocca il nastro della rete e poi entra nel riquadro senza toccare la griglia, il servizio si ripete (net).</p>
<h2>Come si usano le pareti</h2>
<p>È la parte che rende unico il padel (regole 12 e 14).</p>
<ul>
<li>Il colpo è buono se la palla <b>rimbalza prima nel campo avversario</b>; dopo può toccare pareti, griglia o rete.</li>
<li>Puoi anche colpire la palla contro una <b>parete del tuo campo</b>: se poi passa la rete e rimbalza nel campo avversario, il colpo è valido.</li>
<li>Quando la palla arriva nel tuo campo, la puoi colpire al volo, oppure dopo un rimbalzo a terra, anche dopo che ha toccato le pareti: conta solo che <b>non rimbalzi due volte a terra</b>.</li>
<li>Uscire dal campo per riprendere la palla è permesso solo nei campi che hanno lo spazio di sicurezza previsto (regola 16).</li>
</ul>
<h2>Il punteggio e lo Star Point</h2>
<p>Il punteggio è quello del tennis (regola 1): <b>15, 30, 40, gioco</b>. Sul 40 pari si gioca il vantaggio. Il set va a 6 giochi con 2 di scarto; sul 6–6 si gioca il <b>tie-break a 7 punti</b>, sempre con 2 di scarto. La partita è al meglio dei <b>3 set</b>. Si cambia campo quando la somma dei giochi del set è dispari, e nel tie-break ogni 6 punti.</p>
<p><b>Novità 2026: lo Star Point.</b> Dal 2026 nei circuiti Premier Padel, CUPRA FIP Tour, FIP Promises e FIP Beyond, sul 40 pari si giocano al massimo due vantaggi. Se chi ha il vantaggio perde anche il secondo, si gioca un unico punto decisivo, lo Star Point, che assegna il gioco. Nei circoli molti usano invece il <b>punto d'oro</b>: sul 40 pari si gioca subito un solo punto decisivo. Il regolamento li prevede entrambi come formule alternative.</p>
<h2>I falli più comuni</h2>
<ul>
<li>toccare la rete, i pali o il campo avversario con il corpo, la racchetta o il laccetto mentre la palla è in gioco;</li>
<li>lasciare rimbalzare la palla due volte a terra;</li>
<li>colpire la palla in modo che tocchi la griglia o la parete avversaria <b>prima</b> di rimbalzare a terra;</li>
<li>colpire la palla due volte, o colpirla con entrambi i giocatori della coppia;</li>
<li>essere toccati dalla palla, sul corpo o sui vestiti;</li>
<li>sbagliare anche il secondo servizio.</li>
</ul>
<h2>Le altre novità del 2026</h2>
<ul>
<li>al servizio basta avere un piede <b>sulla linea</b> o dietro, e la palla resta comunque sotto la vita;</li>
<li>il riscaldamento prima della partita scende da 5 a 3 minuti;</li>
<li>se il laccetto di sicurezza si rompe durante un punto, quel punto è perso;</li>
<li>nella racchetta, i fori lungo il bordo possono avere forme non rotonde, fino a 20 mm.</li>
</ul>
<h2>La racchetta: cosa dice il regolamento</h2>
<p>Il regolamento FIP fissa le misure massime della racchetta:</p>
<ul>
<li>lunghezza totale, testa più manico, al massimo <b>45,5 cm</b>;</li>
<li>testa larga al massimo <b>26 cm</b> e spessa al massimo <b>38 mm</b>;</li>
<li>fori cilindrici da 9 a 13 mm, in numero libero;</li>
<li>laccetto da polso obbligatorio, non elastico, lungo al massimo 35 cm;</li>
<li>nessun limite di peso.</li>
</ul>
<p>Tutte le racchette che trovi nei negozi rispettano queste misure: la scelta dipende da forma, peso e bilanciamento. Nel nostro database ci sono {len(adulti)} racchette 2026 e 2027, di cui {len(inizio)} pensate per chi inizia o è a livello principiante-intermedio. Puoi filtrarle nella <a href="{url_r_all}">pagina delle racchette</a> o farti consigliare dal <a href="{url_sel}">test "Trova la tua racchetta"</a>. Se vuoi capire cosa cambia tra le forme, leggi le <a href="{P("guide")}">guide</a>.</p>
<p class="note">Fonti: {reg}; {star}. Il regolamento completo comprende anche le norme su arbitri, comportamento e tornei, che qui non trattiamo.</p>''',
              f'''<p><b>Padel is played in doubles on a 20 × 10 m court enclosed by walls, with a net 88 cm high at the centre and a ball similar to a tennis ball.</b> The walls are the real difference: the ball can bounce off them and stay in play. This guide explains the rules one by one, following the official rules of the International Padel Federation (FIP), in the revision in force from 1 January 2026, including this year's changes such as the Star Point.</p>
<h2>The rules in short</h2>
<ol>
<li>Serve underhand: bounce the ball and hit it at or below waist height, diagonally.</li>
<li>You get two serves per point, as in tennis.</li>
<li>The ball must bounce first in the opponents' court; after that it may hit the walls and the wire fence.</li>
<li>Return the ball before its second bounce on the ground, even after it has hit the walls on your side.</li>
<li>Scoring as in tennis: 15, 30, 40, game; sets to 6 games, best of 3 sets.</li>
</ol>
{box()}
<h2>The court, the net and the ball</h2>
<p>The court is <b>20 metres long and 10 metres wide</b>. At each end there are 3 m walls topped by 1 m of wire mesh, 4 m in total; the sides combine walls and mesh in a stepped layout. The net is <b>88 cm high at the centre and up to 92 cm at the ends</b>. The ball is 6.35–6.77 cm in diameter and weighs 56–59.4 grams, with a slightly lower bounce than a tennis ball.</p>
<h2>The serve</h2>
<p>The serve causes the most doubts (rule 6):</p>
<ul>
<li>the server has at least one foot on or behind the service line, in the half between the centre line and the side wall;</li>
<li>bounces the ball on the ground behind the line, then hits it;</li>
<li>at contact the ball must be <b>at or below waist height</b>, with at least one foot on the ground;</li>
<li>the ball must cross the net <b>diagonally</b> and bounce in the opponents' service box;</li>
<li>if the first serve is a fault, there is a <b>second serve</b>.</li>
</ul>
<p>After bouncing in the correct box the ball may hit the glass wall, but if it hits the wire fence before the second bounce the serve is a fault. If the ball clips the net and lands in the box without touching the fence, the serve is replayed (let).</p>
<h2>How the walls work</h2>
<p>This is what makes padel unique (rules 12 and 14).</p>
<ul>
<li>A shot is good if the ball <b>bounces first in the opponents' court</b>; after that it may hit walls, fence or net.</li>
<li>You may also hit the ball against a <b>wall on your own side</b>: if it then clears the net and bounces in the opponents' court, the shot is good.</li>
<li>When the ball comes to your side you can volley it, or play it after one bounce, even after it has hit the walls: what matters is that it <b>does not bounce twice on the ground</b>.</li>
<li>Leaving the court to play the ball is only allowed on courts with the required safety area (rule 16).</li>
</ul>
<h2>Scoring and the Star Point</h2>
<p>Scoring is the same as tennis (rule 1): <b>15, 30, 40, game</b>. At 40–40 advantage is played. A set goes to 6 games with a 2-game margin; at 6–6 a <b>tie-break to 7 points</b> is played, again with a 2-point margin. Matches are best of <b>3 sets</b>. Players change ends when the total number of games in the set is odd, and every 6 points in the tie-break.</p>
<p><b>New in 2026: the Star Point.</b> From 2026 on the Premier Padel, CUPRA FIP Tour, FIP Promises and FIP Beyond circuits, at 40–40 a maximum of two advantages are played. If the team with advantage loses the second one too, a single deciding point, the Star Point, wins the game. Many clubs instead use the <b>golden point</b>: at 40–40 a single deciding point is played straight away. The rules include both as alternative formats.</p>
<h2>The most common faults</h2>
<ul>
<li>touching the net, posts or the opponents' court with body, racket or wrist strap while the ball is in play;</li>
<li>letting the ball bounce twice on the ground;</li>
<li>hitting the ball so that it hits the opponents' fence or wall <b>before</b> bouncing on the ground;</li>
<li>hitting the ball twice, or both partners hitting it;</li>
<li>being hit by the ball, on the body or clothing;</li>
<li>missing the second serve too.</li>
</ul>
<h2>Other changes in 2026</h2>
<ul>
<li>on the serve, one foot <b>on the line</b> or behind it is enough, and the ball must still be below the waist;</li>
<li>the pre-match warm-up drops from 5 to 3 minutes;</li>
<li>if the safety strap breaks during a point, that point is lost;</li>
<li>on the racket, holes along the edge may be non-round, up to 20 mm.</li>
</ul>
<h2>The racket: what the rules say</h2>
<p>The FIP rules set the maximum racket dimensions:</p>
<ul>
<li>total length, head plus handle, no more than <b>45.5 cm</b>;</li>
<li>head no wider than <b>26 cm</b> and no thicker than <b>38 mm</b>;</li>
<li>cylindrical holes of 9–13 mm, in any number;</li>
<li>a mandatory, non-elastic wrist strap no longer than 35 cm;</li>
<li>no weight limit.</li>
</ul>
<p>All rackets sold in shops meet these limits: the choice comes down to shape, weight and balance. Our database has {len(adulti)} 2026 and 2027 rackets, {len(inizio)} of them aimed at beginner or beginner-intermediate players. You can filter them on the <a href="{url_r_all}">rackets page</a> or get a recommendation from the <a href="{url_sel}">racket finder quiz</a>. To understand how shapes differ, read the <a href="{P("guide")}">guides</a>.</p>
<p class="note">Sources: {reg}; {star}. The full rules also cover referees, conduct and tournaments, which are not covered here.</p>''',
              f'''<p><b>El pádel se juega por parejas en una pista de 20 × 10 metros cerrada por paredes, con una red de 88 cm en el centro y una pelota parecida a la de tenis.</b> Las paredes son la verdadera diferencia: la pelota puede rebotar en ellas y seguir en juego. Esta guía explica las reglas una a una siguiendo el reglamento oficial de la Federación Internacional (FIP), en la revisión vigente desde el 1 de enero de 2026, con las novedades de este año como el Star Point.</p>
<h2>Las reglas en breve</h2>
<ol>
<li>Se saca por abajo: la pelota bota en el suelo y se golpea a la altura de la cintura o por debajo, en diagonal.</li>
<li>En cada punto hay dos saques, como en el tenis.</li>
<li>La pelota debe botar primero en el campo rival; después puede tocar paredes y malla metálica.</li>
<li>Se devuelve antes del segundo bote en el suelo, aunque la pelota haya tocado las paredes del propio campo.</li>
<li>Tanteo como en el tenis: 15, 30, 40, juego; sets a 6 juegos, partido al mejor de 3 sets.</li>
</ol>
{box()}
<h2>La pista, la red y la pelota</h2>
<p>La pista mide <b>20 metros de largo por 10 de ancho</b>. En los fondos hay paredes de 3 metros coronadas por 1 metro de malla metálica, 4 metros en total; en los laterales paredes y malla siguen un esquema escalonado. La red mide <b>88 cm en el centro y hasta 92 cm en los extremos</b>. La pelota tiene un diámetro de 6,35 a 6,77 cm y pesa de 56 a 59,4 gramos, con un bote algo más bajo que la de tenis.</p>
<h2>El saque</h2>
<p>El saque es la regla que genera más dudas (regla 6):</p>
<ul>
<li>quien saca tiene al menos un pie sobre la línea de saque o detrás, en la mitad entre la línea central y la pared lateral;</li>
<li>bota la pelota en el suelo detrás de la línea y después la golpea;</li>
<li>en el impacto la pelota debe estar <b>a la altura de la cintura o por debajo</b>, con al menos un pie en el suelo;</li>
<li>la pelota debe pasar la red <b>en diagonal</b> y botar en el recuadro de saque rival;</li>
<li>si el primer saque es falta, hay <b>segundo saque</b>.</li>
</ul>
<p>Tras botar en el recuadro correcto la pelota puede tocar el cristal, pero si toca la malla metálica antes del segundo bote el saque es falta. Si la pelota toca la red y entra en el recuadro sin tocar la malla, el saque se repite (net).</p>
<h2>Cómo se usan las paredes</h2>
<p>Es lo que hace único al pádel (reglas 12 y 14).</p>
<ul>
<li>El golpe es bueno si la pelota <b>bota primero en el campo rival</b>; después puede tocar paredes, malla o red.</li>
<li>También puedes golpear la pelota contra una <b>pared de tu campo</b>: si después pasa la red y bota en el campo rival, el golpe es válido.</li>
<li>Cuando la pelota llega a tu campo puedes volearla o jugarla tras un bote, aunque haya tocado las paredes: solo cuenta que <b>no bote dos veces en el suelo</b>.</li>
<li>Salir de la pista para jugar la pelota solo está permitido en pistas con la zona de seguridad prevista (regla 16).</li>
</ul>
<h2>El tanteo y el Star Point</h2>
<p>El tanteo es el del tenis (regla 1): <b>15, 30, 40, juego</b>. Con 40 iguales se juega la ventaja. El set va a 6 juegos con 2 de diferencia; con 6–6 se juega el <b>tie-break a 7 puntos</b>, también con 2 de diferencia. El partido es al mejor de <b>3 sets</b>. Se cambia de lado cuando la suma de juegos del set es impar, y en el tie-break cada 6 puntos.</p>
<p><b>Novedad 2026: el Star Point.</b> Desde 2026 en los circuitos Premier Padel, CUPRA FIP Tour, FIP Promises y FIP Beyond, con 40 iguales se juegan como máximo dos ventajas. Si quien tiene la ventaja pierde también la segunda, se juega un único punto decisivo, el Star Point, que da el juego. En los clubes muchos usan en cambio el <b>punto de oro</b>: con 40 iguales se juega directamente un solo punto decisivo. El reglamento recoge ambos como fórmulas alternativas.</p>
<h2>Las faltas más comunes</h2>
<ul>
<li>tocar la red, los postes o el campo rival con el cuerpo, la pala o el cordón con la pelota en juego;</li>
<li>dejar que la pelota bote dos veces en el suelo;</li>
<li>golpear la pelota de forma que toque la malla o la pared rival <b>antes</b> de botar en el suelo;</li>
<li>golpear la pelota dos veces, o que la golpeen los dos jugadores de la pareja;</li>
<li>que la pelota te toque en el cuerpo o la ropa;</li>
<li>fallar también el segundo saque.</li>
</ul>
<h2>Las otras novedades de 2026</h2>
<ul>
<li>en el saque basta con tener un pie <b>sobre la línea</b> o detrás, y la pelota sigue por debajo de la cintura;</li>
<li>el calentamiento antes del partido baja de 5 a 3 minutos;</li>
<li>si el cordón de seguridad se rompe durante un punto, ese punto se pierde;</li>
<li>en la pala, los agujeros del borde pueden no ser redondos, hasta 20 mm.</li>
</ul>
<h2>La pala: qué dice el reglamento</h2>
<p>El reglamento FIP fija las medidas máximas de la pala:</p>
<ul>
<li>longitud total, cabeza más puño, como máximo <b>45,5 cm</b>;</li>
<li>cabeza de <b>26 cm</b> de ancho y <b>38 mm</b> de grosor como máximo;</li>
<li>agujeros cilíndricos de 9 a 13 mm, en número libre;</li>
<li>cordón de muñeca obligatorio, no elástico, de 35 cm como máximo;</li>
<li>sin límite de peso.</li>
</ul>
<p>Todas las palas que encuentras en las tiendas cumplen estas medidas: la elección depende de forma, peso y balance. En nuestra base de datos hay {len(adulti)} palas 2026 y 2027, {len(inizio)} de ellas pensadas para quien empieza o tiene nivel principiante-intermedio. Puedes filtrarlas en la <a href="{url_r_all}">página de palas</a> o pedir consejo al <a href="{url_sel}">test "Encuentra tu pala"</a>. Para entender qué cambia entre formas, lee las <a href="{P("guide")}">guías</a>.</p>
<p class="note">Fuentes: {reg}; {star}. El reglamento completo incluye también normas sobre árbitros, conducta y torneos, que aquí no tratamos.</p>''', f'''<p><b>Le padel se joue en double sur un terrain de 20 × 10 m entouré de murs, avec un filet de 88 cm au centre et une balle semblable à une balle de tennis.</b> Les murs sont la vraie différence : la balle peut rebondir dessus et rester en jeu. Ce guide explique les règles une par une, d'après le règlement officiel de la Fédération internationale de padel (FIP), dans la révision en vigueur depuis le 1er janvier 2026, y compris les nouveautés de cette année comme le Star Point.</p>
<h2>Les règles en bref</h2>
<ol>
<li>Servez à la cuillère : faites rebondir la balle et frappez-la à hauteur de la taille ou en dessous, en diagonale.</li>
<li>Vous avez deux services par point, comme au tennis.</li>
<li>La balle doit d'abord rebondir dans le camp adverse ; ensuite, elle peut toucher les murs et le grillage.</li>
<li>Renvoyez la balle avant son deuxième rebond au sol, même après qu'elle a touché les murs de votre côté.</li>
<li>Comptage comme au tennis : 15, 30, 40, jeu ; sets en 6 jeux, au meilleur des 3 sets.</li>
</ol>
{box()}
<h2>Le terrain, le filet et la balle</h2>
<p>Le terrain mesure <b>20 mètres de long et 10 mètres de large</b>. À chaque extrémité se trouvent des murs de 3 m surmontés d'1 m de grillage, soit 4 m au total ; les côtés combinent murs et grillage en escalier. Le filet mesure <b>88 cm au centre et jusqu'à 92 cm aux extrémités</b>. La balle fait 6,35–6,77 cm de diamètre et pèse 56–59,4 grammes, avec un rebond légèrement plus bas qu'une balle de tennis.</p>
<h2>Le service</h2>
<p>C'est le service qui suscite le plus de doutes (règle 6) :</p>
<ul>
<li>le serveur a au moins un pied sur la ligne de service ou derrière, dans la moitié comprise entre la ligne centrale et le mur latéral ;</li>
<li>il fait rebondir la balle au sol derrière la ligne, puis la frappe ;</li>
<li>à l'impact, la balle doit être <b>à hauteur de la taille ou en dessous</b>, avec au moins un pied au sol ;</li>
<li>la balle doit passer le filet <b>en diagonale</b> et rebondir dans le carré de service adverse ;</li>
<li>si le premier service est faute, il y a un <b>second service</b>.</li>
</ul>
<p>Après avoir rebondi dans le bon carré, la balle peut toucher la vitre, mais si elle touche le grillage avant le deuxième rebond, le service est faute. Si la balle touche le filet et tombe dans le carré sans toucher le grillage, le service est rejoué (let).</p>
<h2>Comment fonctionnent les murs</h2>
<p>C'est ce qui rend le padel unique (règles 12 et 14).</p>
<ul>
<li>Un coup est bon si la balle <b>rebondit d'abord dans le camp adverse</b> ; ensuite, elle peut toucher murs, grillage ou filet.</li>
<li>Vous pouvez aussi frapper la balle contre un <b>mur de votre côté</b> : si elle passe ensuite le filet et rebondit dans le camp adverse, le coup est bon.</li>
<li>Quand la balle arrive de votre côté, vous pouvez la jouer de volée, ou après un rebond, même après qu'elle a touché les murs : l'important est qu'elle <b>ne rebondisse pas deux fois au sol</b>.</li>
<li>Sortir du terrain pour jouer la balle n'est autorisé que sur les terrains disposant de la zone de sécurité requise (règle 16).</li>
</ul>
<h2>Le comptage et le Star Point</h2>
<p>Le comptage est le même qu'au tennis (règle 1) : <b>15, 30, 40, jeu</b>. À 40–40, on joue l'avantage. Un set se joue en 6 jeux avec 2 jeux d'écart ; à 6–6, on joue un <b>tie-break en 7 points</b>, là encore avec 2 points d'écart. Les matchs se jouent au meilleur des <b>3 sets</b>. Les joueurs changent de côté quand le nombre total de jeux du set est impair, et tous les 6 points dans le tie-break.</p>
<p><b>Nouveauté 2026 : le Star Point.</b> Depuis 2026, sur les circuits Premier Padel, CUPRA FIP Tour, FIP Promises et FIP Beyond, à 40–40 on joue au maximum deux avantages. Si l'équipe qui a l'avantage perd aussi le second, un seul point décisif, le Star Point, attribue le jeu. Beaucoup de clubs utilisent plutôt le <b>point en or</b> : à 40–40, on joue directement un seul point décisif. Le règlement prévoit les deux comme formats alternatifs.</p>
<h2>Les fautes les plus courantes</h2>
<ul>
<li>toucher le filet, les poteaux ou le camp adverse avec le corps, la raquette ou la dragonne pendant que la balle est en jeu ;</li>
<li>laisser la balle rebondir deux fois au sol ;</li>
<li>frapper la balle de façon qu'elle touche le grillage ou le mur adverse <b>avant</b> de rebondir au sol ;</li>
<li>frapper la balle deux fois, ou que les deux partenaires la frappent ;</li>
<li>être touché par la balle, sur le corps ou les vêtements ;</li>
<li>rater aussi le second service.</li>
</ul>
<h2>Les autres nouveautés 2026</h2>
<ul>
<li>au service, un pied <b>sur la ligne</b> ou derrière suffit, et la balle doit toujours être sous la taille ;</li>
<li>l'échauffement avant le match passe de 5 à 3 minutes ;</li>
<li>si la dragonne casse pendant un point, ce point est perdu ;</li>
<li>sur la raquette, les trous le long du bord peuvent être non ronds, jusqu'à 20 mm.</li>
</ul>
<h2>La raquette : ce que dit le règlement</h2>
<p>Le règlement FIP fixe les dimensions maximales de la raquette :</p>
<ul>
<li>longueur totale, tête plus manche, pas plus de <b>45,5 cm</b> ;</li>
<li>tête pas plus large que <b>26 cm</b> ni plus épaisse que <b>38 mm</b> ;</li>
<li>trous cylindriques de 9–13 mm, en nombre libre ;</li>
<li>une dragonne obligatoire, non élastique, de 35 cm au maximum ;</li>
<li>aucune limite de poids.</li>
</ul>
<p>Toutes les raquettes vendues en magasin respectent ces limites : le choix se fait sur la forme, le poids et l'équilibre. Notre base contient {len(adulti)} raquettes 2026 et 2027, dont {len(inizio)} destinées aux débutants ou aux joueurs débutants-intermédiaires. Vous pouvez les filtrer sur la <a href="{url_r_all}">page des raquettes</a> ou obtenir une recommandation avec le <a href="{url_sel}">quiz Trouve ta raquette</a>. Pour comprendre les différences entre les formes, lisez les <a href="{P("guide")}">guides</a>.</p>
<p class="note">Sources : {reg} ; {star}. Le règlement complet traite aussi de l'arbitrage, du comportement et des tournois, qui ne sont pas abordés ici.</p>''')
    corpo += box()
    qa = [(L("Nel padel il servizio si fa dal basso?", "Is the padel serve underhand?", "¿En el pádel se saca por abajo?", "Le service au padel se fait-il à la cuillère ?"),
           L("Sì. Si lascia rimbalzare la palla a terra dietro la linea di servizio e la si colpisce all'altezza della vita o più in basso, in diagonale. Ci sono due servizi per punto.",
             "Yes. You bounce the ball behind the service line and hit it at or below waist height, diagonally. There are two serves per point.",
             "Sí. Se bota la pelota detrás de la línea de saque y se golpea a la altura de la cintura o por debajo, en diagonal. Hay dos saques por punto.", "Oui. On fait rebondir la balle derrière la ligne de service et on la frappe à hauteur de la taille ou en dessous, en diagonale. Il y a deux services par point.")),
          (L("La palla può toccare le pareti?", "Can the ball hit the walls?", "¿La pelota puede tocar las paredes?", "La balle peut-elle toucher les murs ?"),
           L("Sì, ma deve rimbalzare prima a terra nel campo avversario. Puoi anche giocarla contro una parete del tuo campo, purché poi passi la rete e rimbalzi nel campo avversario.",
             "Yes, but it must bounce on the ground in the opponents' court first. You can also play it off a wall on your side, as long as it then clears the net and bounces in the opponents' court.",
             "Sí, pero debe botar primero en el suelo del campo rival. También puedes jugarla contra una pared de tu campo, siempre que después pase la red y bote en el campo rival.", "Oui, mais elle doit d'abord rebondir au sol dans le camp adverse. Vous pouvez aussi la jouer contre un mur de votre côté, à condition qu'elle passe ensuite le filet et rebondisse dans le camp adverse.")),
          (L("Cos'è lo Star Point nel padel?", "What is the Star Point in padel?", "¿Qué es el Star Point en el pádel?", "Qu'est-ce que le Star Point au padel ?"),
           L("È la regola introdotta nel 2026 nei circuiti professionistici: sul 40 pari si giocano al massimo due vantaggi, poi un punto decisivo che assegna il gioco.",
             "It is the rule introduced in 2026 on the pro circuits: at 40–40 a maximum of two advantages are played, then a single deciding point wins the game.",
             "Es la regla introducida en 2026 en los circuitos profesionales: con 40 iguales se juegan como máximo dos ventajas y después un punto decisivo que da el juego.", "C'est la règle introduite en 2026 sur les circuits professionnels : à 40–40, on joue au maximum deux avantages, puis un seul point décisif attribue le jeu.")),
          (L("Quanto è grande un campo da padel?", "How big is a padel court?", "¿Cuánto mide una pista de pádel?", "Quelles sont les dimensions d'un terrain de padel ?"),
           L("20 metri per 10, con pareti di fondo alte 3 metri più 1 metro di rete metallica. La rete è alta 88 cm al centro.",
             "20 by 10 metres, with 3 m back walls plus 1 m of wire mesh. The net is 88 cm high at the centre.",
             "20 por 10 metros, con paredes de fondo de 3 metros más 1 metro de malla metálica. La red mide 88 cm en el centro.", "20 mètres sur 10, avec des murs de fond de 3 m plus 1 m de grillage. Le filet mesure 88 cm au centre.")),
          (L("Quali sono le misure massime della racchetta da padel?", "What are the maximum padel racket dimensions?", "¿Cuáles son las medidas máximas de la pala de pádel?", "Quelles sont les dimensions maximales d'une raquette de padel ?"),
           L("Lunghezza totale 45,5 cm, testa larga 26 cm e spessa 38 mm al massimo. Non c'è un limite di peso e il laccetto da polso è obbligatorio.",
             "Total length 45.5 cm, head up to 26 cm wide and 38 mm thick. There is no weight limit and the wrist strap is mandatory.",
             "Longitud total 45,5 cm, cabeza de hasta 26 cm de ancho y 38 mm de grosor. No hay límite de peso y el cordón de muñeca es obligatorio.", "Longueur totale de 45,5 cm, tête jusqu'à 26 cm de large et 38 mm d'épaisseur. Il n'y a pas de limite de poids et la dragonne est obligatoire."))]
    faq_htm, faq_ld = faq(qa)
    corpo += faq_htm
    titolo = L("Regolamento del padel 2026: le regole spiegate semplici", "Padel rules 2026: the rules explained simply", "Reglamento del pádel 2026: las reglas explicadas fácil", "Règles du padel 2026 : les règles expliquées simplement")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Le regole del padel secondo il regolamento FIP 2026: campo, servizio, uso delle pareti, punteggio, Star Point, falli e misure della racchetta.",
                      "Padel rules from the 2026 FIP rulebook: court, serve, playing off the walls, scoring, Star Point, faults and racket limits.",
                      "Las reglas del pádel según el reglamento FIP 2026: pista, saque, uso de las paredes, tanteo, Star Point, faltas y medidas de la pala.", "Les règles du padel d'après le règlement FIP 2026 : terrain, service, jeu avec les murs, comptage des points, Star Point, fautes et limites de la raquette."),
                    titolo, L("Regolamento padel", "Padel rules", "Reglamento pádel", "Règles du padel"), corpo, ld_extra=[faq_ld])
    return slug, titolo, L("Servizio, pareti, punteggio e Star Point, secondo il regolamento FIP 2026.", "Serve, walls, scoring and Star Point, per the 2026 FIP rules.",
                           "Saque, paredes, tanteo y Star Point, según el reglamento FIP 2026.", "Service, murs, comptage et Star Point, d'après le règlement FIP 2026.")



FITP_SOLE = "https://en.ilsole24ore.com/art/tennis-has-overtaken-football-in-terms-of-the-number-of-registered-members-whilst-the-football-federation-recorded-revenue-of-280-million-AJMhseuB"
FITP_POST = "https://www.ilpost.it/2026/10/27/federtennis-fitp-superato-tesserati-figc-federcalcio-come-ha-fatto-rapporto-coni-2024/"
FITP_FQ = "https://www.ilfattoquotidiano.it/2026/10/27/tennis-sorpasso-calcio-tesserati-padel-fitp-figc-buonfiglio-binaghi/8551561/"
FITP_NOME = "https://www.oasport.it/2022/10/tennis-la-fit-cambia-nome-diventa-fitp-e-include-il-padel/"
FITP_FIP = "https://www.padelfip.com/?p=161358"
FITP_AGI = "https://www.agi.it/sport/news/2026-07-12/campi-da-padel-italia-37986662/"
S.SLUG["fitp-supera-figc-tesserati-tennis-padel"] = ("fitp-overtakes-figc-registered-members-tennis-padel", "fitp-supera-figc-federados-tenis-padel")
S.SLUG_FR["fitp-supera-figc-tesserati-tennis-padel"] = "fitp-depasse-figc-licencies-tennis-padel"
DATE_ART["fitp-supera-figc-tesserati-tennis-padel"] = "2026-11-02"


def fitp_sorpasso(db):
    slug = "fitp-supera-figc-tesserati-tennis-padel"
    adulti = [n for n in db if n["categoria"] != "junior"]
    sole, post, fq = fonte(FITP_SOLE, "Il Sole 24 Ore"), fonte(FITP_POST, "Il Post"), fonte(FITP_FQ, "Il Fatto Quotidiano")
    nome_src, fip, agi = fonte(FITP_NOME, "OA Sport"), fonte(FITP_FIP, "FIP"), fonte(FITP_AGI, "AGI")
    reg, sel, rac = P("articoli", "regolamento-padel-regole-spiegate"), P("selettore"), P("racchette")
    num = (lambda x: x) if S.lang() != "en" else (lambda x: x.replace(".", ","))
    righe = [("FITP (tennis e padel)", "FITP (tennis and padel)", "FITP (tenis y pádel)", "FITP (tennis et padel)", "1.162.477", "20,2"),
             ("FIGC (calcio)", "FIGC (football)", "FIGC (fútbol)", "FIGC (football)", "1.123.054", "19,5"),
             ("Pallavolo", "Volleyball", "Voleibol", "Volley-ball", "359.797", ""), ("Pallacanestro", "Basketball", "Baloncesto", "Basket-ball", "320.769", ""),
             ("Atletica leggera", "Athletics", "Atletismo", "Athlétisme", "292.599", "")]
    def fmt(v):
        if S.lang() == "en":
            return v.replace(".", "§").replace(",", ".").replace("§", ",")
        if S.lang() == "fr":
            return v.replace(".", " ")
        return v
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th>' + L("Federazione", "Federation", "Federación", "Fédération") + '</th><th>'
           + L("Tesserati 2024", "Registered members 2024", "Federados 2024", "Licenciés 2024") + '</th><th>' + L("Quota sul totale", "Share of total", "Cuota del total", "Part du total") + '</th></tr></thead><tbody>'
           + "".join(f'<tr><td>{L(a, b, c, d)}</td><td>{fmt(n)}</td><td>{(fmt(q) + " %") if q and S.lang() == "fr" else ((fmt(q) + "%") if q else "—")}</td></tr>' for a, b, c, d, n, q in righe)
           + '</tbody></table></div>')
    box = L(f'<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Sei tra i nuovi giocatori di padel?</b><br>Parti dalle <a href="{reg}">regole spiegate semplici</a>, poi scegli la racchetta tra le {len(adulti)} del nostro database.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{sel}">Trova la tua racchetta</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{rac}">Vedi tutte le racchette →</a></div>',
            f'<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>New to padel?</b><br>Start with the <a href="{reg}">rules explained simply</a>, then pick your racket from the {len(adulti)} in our database.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{sel}">Find your racket</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{rac}">See all rackets →</a></div>',
            f'<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>¿Acabas de empezar con el pádel?</b><br>Empieza por las <a href="{reg}">reglas explicadas fácil</a> y luego elige pala entre las {len(adulti)} de nuestra base de datos.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{sel}">Encuentra tu pala</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{rac}">Ver todas las palas →</a></div>',
            f'<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>Vous débutez au padel ?</b><br>Commencez par les <a href="{reg}">règles expliquées simplement</a>, puis choisissez votre raquette parmi les {len(adulti)} de notre base.<br><a class="btn" style="margin-top:12px;display:inline-block" href="{sel}">Trouve ta raquette</a> <a class="btn out" style="margin-top:12px;display:inline-block" href="{rac}">Voir toutes les raquettes →</a></div>')
    corpo = L(f'''<p><b>Per la prima volta in Italia la Federazione Italiana Tennis e Padel (FITP) ha più tesserati della Federcalcio (FIGC): secondo il monitoraggio del CONI sul 2024, 1.162.477 contro 1.123.054.</b> È un sorpasso storico, che ha più di una spiegazione. Una di queste è il padel, che dal 2023 fa parte anche del nome della federazione.</p>
<h2>Cos'è la FITP</h2>
<p>La FITP è la federazione sportiva nazionale, riconosciuta dal CONI, che governa in Italia il tennis e il padel: affilia i circoli, rilascia le tessere, forma maestri e arbitri e organizza campionati e tornei. Fino al 2022 si chiamava FIT, Federazione Italiana Tennis. Il 16 ottobre 2022 l'assemblea straordinaria riunita a Firenze ha approvato all'unanimità il nuovo nome, Federazione Italiana Tennis e Padel, con la nuova federazione costituita dal 1° gennaio 2023 dopo il via libera del CONI ({nome_src}). Il padel era già una disciplina della federazione dal 2008 ({post}).</p>
<p>La guida dal 2001 Angelo Binaghi: quando è diventato presidente i tesserati erano circa 130.000 ({fq}). Oggi la FITP conta oltre 4.000 circoli affiliati, più di 2.500 scuole di tennis e padel, circa 14.000 tecnici e 10.000 ufficiali di gara, e organizza grandi eventi come le ATP Finals di Torino e gli Internazionali d'Italia ({sole}).</p>
<h2>I numeri del sorpasso</h2>
<p>I dati vengono dal "Monitoraggio CONI-FSN-DSA", il censimento di società e tesserati di 48 federazioni, 15 discipline associate e 14 enti di promozione, anticipato da Il Sole 24 Ore. Nel 2024 i tesserati in Italia sono stati 6.069.891, il dato più alto di sempre (+7,7% sul 2023).</p>
{tab}
<p>Nel 2025 la FITP è salita a 1.254.153 tesserati ({sole}). La crescita è soprattutto dell'ultimo decennio: nel rapporto CONI sul 2014 la federazione aveva meno di 300.000 tesserati ed era dietro a pallavolo e pallacanestro; da allora è cresciuta di oltre il 300%, mentre la FIGC di circa il 5% ({post}).</p>
<p>Il sorpasso riguarda anche i conti. Nel 2024 il valore della produzione era di 209 milioni per la FITP e 224 per la FIGC; nel 2025 la FITP ha superato i 240 milioni contro i 214 della Federcalcio, e per il 2026 prevede oltre 280 milioni. Più del 70% dei ricavi arriva dall'organizzazione di eventi internazionali ({sole}).</p>
<h2>Perché tennis e padel crescono così</h2>
<ul>
<li><b>Il padel.</b> Si impara in fretta e basta essere in quattro invece che in dieci: per molti ha preso il posto della partita di calcetto ({sole}).</li>
<li><b>I campioni.</b> Sinner, Paolini ed Errani hanno avvicinato tante persone al tennis, ma soprattutto negli ultimi anni: Il Sole 24 Ore considera i successi più una conseguenza che la causa della crescita ({post}).</li>
<li><b>Le donne.</b> Il tennis è storicamente più aperto alle donne: gli uomini sono il 59% dei tesserati FITP e il 96% di quelli FIGC ({post}).</li>
<li><b>Il modello economico.</b> I ricavi dei grandi eventi vengono reinvestiti in scuole, formazione dei tecnici e tornei: i tornei internazionali in Italia sono passati da meno di 30 a circa 90 in 25 anni ({post}).</li>
</ul>
<h2>Quanto pesa il padel</h2>
<p>La FITP non pubblica nel rapporto un dato separato per il padel, ma alcuni numeri danno l'idea della crescita. A fine 2023 i tesserati padel erano quasi 74.000 e i circoli affiliati 1.682 ({fip}). Secondo i dati 2025 del centro studi della Federazione Internazionale Padel riportati da AGI, i campi affiliati FITP sono 5.321, con il Lazio in testa (2.014), e l'Italia è il secondo Paese al mondo per diffusione del padel ({agi}).</p>
<h2>Da leggere con attenzione</h2>
<ul>
<li><b>Tesserati non vuol dire praticanti.</b> Il calcio non è diventato meno popolare: si gioca moltissimo anche senza tessera federale.</li>
<li>Il rapporto CONI non conta il CSI, il Centro Sportivo Italiano, che raccoglie molta attività calcistica amatoriale e degli oratori ({post}).</li>
<li>La FIGC resta la federazione più diffusa sul territorio, con oltre 10.000 società affiliate, ed è ancora prima per tesserati in 11 regioni ({post}, {sole}).</li>
</ul>
<p class="note">Fonti: {sole} (27 ottobre 2026), {post}, {fq}, {nome_src}, {fip}, {agi}.</p>''',
              f'''<p><b>For the first time in Italy, the Italian Tennis and Padel Federation (FITP) has more registered members than the football federation (FIGC): according to CONI's monitoring report for 2024, 1,162,477 against 1,123,054.</b> It is a historic overtaking with more than one explanation. One of them is padel, which since 2023 has also been part of the federation's name.</p>
<h2>What the FITP is</h2>
<p>The FITP is the national sports federation, recognised by the Italian Olympic Committee (CONI), that governs tennis and padel in Italy: it affiliates clubs, issues memberships, trains coaches and referees and organises championships and tournaments. Until 2022 it was called FIT, the Italian Tennis Federation. On 16 October 2022 an extraordinary assembly in Florence unanimously approved the new name, Italian Tennis and Padel Federation, with the new federation established from 1 January 2023 after CONI's approval ({nome_src}). Padel had already been one of the federation's disciplines since 2008 ({post}).</p>
<p>It has been led since 2001 by Angelo Binaghi: when he became president it had around 130,000 members ({fq}). Today the FITP has more than 4,000 affiliated clubs, over 2,500 tennis and padel schools, about 14,000 coaches and 10,000 officials, and it organises major events such as the ATP Finals in Turin and the Internazionali d'Italia in Rome ({sole}).</p>
<h2>The numbers behind the overtaking</h2>
<p>The data come from the "CONI-FSN-DSA Monitoring", a census of clubs and members of 48 federations, 15 associated disciplines and 14 sports promotion bodies, previewed by Il Sole 24 Ore. In 2024 Italy had 6,069,891 registered members, the highest figure ever (+7.7% on 2023).</p>
{tab}
<p>In 2025 the FITP rose to 1,254,153 members ({sole}). The growth came mostly in the last decade: in CONI's report for 2014 the federation had fewer than 300,000 members and was behind volleyball and basketball; since then it has grown by more than 300%, while the FIGC grew by about 5% ({post}).</p>
<p>The overtaking also shows in the accounts. In 2024 production value was 209 million euros for the FITP and 224 million for the FIGC; in 2025 the FITP passed 240 million against the football federation's 214, and for 2026 it forecasts more than 280 million. Over 70% of its revenue comes from organising international events ({sole}).</p>
<h2>Why tennis and padel are growing so fast</h2>
<ul>
<li><b>Padel.</b> It is quick to learn and you only need four people instead of ten: for many it has replaced the five-a-side football game ({sole}).</li>
<li><b>The champions.</b> Sinner, Paolini and Errani have drawn many people to tennis, but mostly in recent years: Il Sole 24 Ore sees their success more as a consequence than the cause of the growth ({post}).</li>
<li><b>Women.</b> Tennis has historically been more open to women: men make up 59% of FITP members and 96% of FIGC members ({post}).</li>
<li><b>The business model.</b> Revenue from major events is reinvested in schools, coach training and tournaments: international tournaments in Italy have gone from fewer than 30 to about 90 in 25 years ({post}).</li>
</ul>
<h2>How big is padel's share</h2>
<p>The report does not give a separate figure for padel, but some numbers show its growth. At the end of 2023 there were almost 74,000 padel members and 1,682 affiliated clubs ({fip}). According to 2025 data from the International Padel Federation's research department reported by AGI, there are 5,321 FITP-affiliated courts, with Lazio in the lead (2,014), and Italy is the second country in the world for padel ({agi}).</p>
<h2>Read with care</h2>
<ul>
<li><b>Registered members are not players.</b> Football has not become less popular: a lot of it is played without a federal membership.</li>
<li>CONI's report does not count the CSI (Centro Sportivo Italiano), which covers much amateur and parish football ({post}).</li>
<li>The FIGC is still the most widespread federation, with more than 10,000 affiliated clubs, and still has the most members in 11 regions ({post}, {sole}).</li>
</ul>
<p class="note">Sources: {sole} (27 October 2026), {post}, {fq}, {nome_src}, {fip}, {agi}.</p>''',
              f'''<p><b>Por primera vez en Italia, la Federación Italiana de Tenis y Pádel (FITP) tiene más federados que la federación de fútbol (FIGC): según el informe de seguimiento del CONI sobre 2024, 1.162.477 frente a 1.123.054.</b> Es un adelantamiento histórico con más de una explicación. Una de ellas es el pádel, que desde 2023 forma parte también del nombre de la federación.</p>
<h2>Qué es la FITP</h2>
<p>La FITP es la federación deportiva nacional, reconocida por el Comité Olímpico Italiano (CONI), que gobierna el tenis y el pádel en Italia: afilia a los clubes, expide las licencias, forma a entrenadores y árbitros y organiza campeonatos y torneos. Hasta 2022 se llamaba FIT, Federación Italiana de Tenis. El 16 de octubre de 2022, una asamblea extraordinaria en Florencia aprobó por unanimidad el nuevo nombre, Federación Italiana de Tenis y Pádel, con la nueva federación constituida desde el 1 de enero de 2023 tras el visto bueno del CONI ({nome_src}). El pádel ya era una disciplina de la federación desde 2008 ({post}).</p>
<p>La preside desde 2001 Angelo Binaghi: cuando llegó a la presidencia tenía unos 130.000 federados ({fq}). Hoy la FITP cuenta con más de 4.000 clubes afiliados, más de 2.500 escuelas de tenis y pádel, unos 14.000 técnicos y 10.000 jueces, y organiza grandes eventos como las ATP Finals de Turín y los Internazionali d'Italia de Roma ({sole}).</p>
<h2>Las cifras del adelantamiento</h2>
<p>Los datos proceden del "Monitoraggio CONI-FSN-DSA", el censo de clubes y federados de 48 federaciones, 15 disciplinas asociadas y 14 entes de promoción, adelantado por Il Sole 24 Ore. En 2024 Italia tuvo 6.069.891 federados, la cifra más alta de la historia (+7,7% respecto a 2023).</p>
{tab}
<p>En 2025 la FITP subió a 1.254.153 federados ({sole}). El crecimiento se concentra en la última década: en el informe del CONI sobre 2014 la federación tenía menos de 300.000 federados y estaba por detrás del voleibol y el baloncesto; desde entonces ha crecido más de un 300%, mientras que la FIGC lo ha hecho en torno a un 5% ({post}).</p>
<p>El adelantamiento también se ve en las cuentas. En 2024 el valor de la producción fue de 209 millones de euros para la FITP y 224 para la FIGC; en 2025 la FITP superó los 240 millones frente a los 214 de la federación de fútbol, y para 2026 prevé más de 280 millones. Más del 70% de sus ingresos procede de la organización de eventos internacionales ({sole}).</p>
<h2>Por qué crecen tanto el tenis y el pádel</h2>
<ul>
<li><b>El pádel.</b> Se aprende rápido y basta con ser cuatro en lugar de diez: para muchos ha sustituido al partido de fútbol sala ({sole}).</li>
<li><b>Los campeones.</b> Sinner, Paolini y Errani han acercado a mucha gente al tenis, pero sobre todo en los últimos años: Il Sole 24 Ore considera sus éxitos más una consecuencia que la causa del crecimiento ({post}).</li>
<li><b>Las mujeres.</b> El tenis ha sido históricamente más abierto a las mujeres: los hombres son el 59% de los federados de la FITP y el 96% de los de la FIGC ({post}).</li>
<li><b>El modelo económico.</b> Los ingresos de los grandes eventos se reinvierten en escuelas, formación de técnicos y torneos: los torneos internacionales en Italia han pasado de menos de 30 a unos 90 en 25 años ({post}).</li>
</ul>
<h2>Cuánto pesa el pádel</h2>
<p>El informe no da una cifra separada para el pádel, pero algunos datos muestran su crecimiento. A finales de 2023 había casi 74.000 federados de pádel y 1.682 clubes afiliados ({fip}). Según datos de 2025 del departamento de estudios de la Federación Internacional de Pádel recogidos por AGI, hay 5.321 pistas afiliadas a la FITP, con el Lacio en cabeza (2.014), e Italia es el segundo país del mundo en difusión del pádel ({agi}).</p>
<h2>Para leer con atención</h2>
<ul>
<li><b>Federados no significa practicantes.</b> El fútbol no ha perdido popularidad: se juega muchísimo también sin licencia federativa.</li>
<li>El informe del CONI no incluye al CSI (Centro Sportivo Italiano), que agrupa mucho fútbol aficionado y de parroquia ({post}).</li>
<li>La FIGC sigue siendo la federación más extendida, con más de 10.000 clubes afiliados, y sigue siendo la primera en federados en 11 regiones ({post}, {sole}).</li>
</ul>
<p class="note">Fuentes: {sole} (27 de octubre de 2026), {post}, {fq}, {nome_src}, {fip}, {agi}.</p>''',
              f'''<p><b>Pour la première fois en Italie, la Fédération italienne de tennis et de padel (FITP) compte plus de licenciés que la fédération de football (FIGC) : selon le rapport de suivi du CONI sur 2024, 1 162 477 contre 1 123 054.</b> C'est un dépassement historique qui a plusieurs explications. L'une d'elles est le padel, qui fait aussi partie du nom de la fédération depuis 2023.</p>
<h2>Qu'est-ce que la FITP</h2>
<p>La FITP est la fédération sportive nationale, reconnue par le Comité olympique italien (CONI), qui gère le tennis et le padel en Italie : elle affilie les clubs, délivre les licences, forme les enseignants et les arbitres et organise championnats et tournois. Jusqu'en 2022, elle s'appelait FIT, Fédération italienne de tennis. Le 16 octobre 2022, une assemblée extraordinaire réunie à Florence a approuvé à l'unanimité le nouveau nom, Fédération italienne de tennis et de padel, la nouvelle fédération étant constituée au 1er janvier 2023 après l'accord du CONI ({nome_src}). Le padel était déjà une discipline de la fédération depuis 2008 ({post}).</p>
<p>Elle est présidée depuis 2001 par Angelo Binaghi : à son arrivée, elle comptait environ 130 000 licenciés ({fq}). Aujourd'hui, la FITP réunit plus de 4 000 clubs affiliés, plus de 2 500 écoles de tennis et de padel, environ 14 000 enseignants et 10 000 officiels, et organise de grands événements comme les ATP Finals de Turin et les Internazionali d'Italia à Rome ({sole}).</p>
<h2>Les chiffres du dépassement</h2>
<p>Les données viennent du « Monitoraggio CONI-FSN-DSA », le recensement des clubs et licenciés de 48 fédérations, 15 disciplines associées et 14 organismes de promotion, dévoilé en avant-première par Il Sole 24 Ore. En 2024, l'Italie comptait 6 069 891 licenciés, un record (+7,7 % par rapport à 2023).</p>
{tab}
<p>En 2025, la FITP est montée à 1 254 153 licenciés ({sole}). La croissance s'est surtout faite au cours de la dernière décennie : dans le rapport du CONI sur 2014, la fédération comptait moins de 300 000 licenciés et se trouvait derrière le volley-ball et le basket-ball ; depuis, elle a progressé de plus de 300 %, contre environ 5 % pour la FIGC ({post}).</p>
<p>Le dépassement se voit aussi dans les comptes. En 2024, la valeur de la production était de 209 millions d'euros pour la FITP et de 224 millions pour la FIGC ; en 2025, la FITP a dépassé les 240 millions contre 214 pour la fédération de football, et elle prévoit plus de 280 millions pour 2026. Plus de 70 % de ses recettes proviennent de l'organisation d'événements internationaux ({sole}).</p>
<h2>Pourquoi le tennis et le padel progressent autant</h2>
<ul>
<li><b>Le padel.</b> Il s'apprend vite et il suffit d'être quatre au lieu de dix : pour beaucoup, il a remplacé le match de foot à cinq ({sole}).</li>
<li><b>Les champions.</b> Sinner, Paolini et Errani ont attiré beaucoup de monde vers le tennis, mais surtout ces dernières années : Il Sole 24 Ore voit leurs succès davantage comme une conséquence que comme la cause de la croissance ({post}).</li>
<li><b>Les femmes.</b> Le tennis a toujours été plus ouvert aux femmes : les hommes représentent 59 % des licenciés de la FITP et 96 % de ceux de la FIGC ({post}).</li>
<li><b>Le modèle économique.</b> Les recettes des grands événements sont réinvesties dans les écoles, la formation des enseignants et les tournois : les tournois internationaux en Italie sont passés de moins de 30 à environ 90 en 25 ans ({post}).</li>
</ul>
<h2>Quel poids pour le padel</h2>
<p>Le rapport ne donne pas de chiffre séparé pour le padel, mais quelques données montrent sa croissance. Fin 2023, on comptait près de 74 000 licenciés de padel et 1 682 clubs affiliés ({fip}). Selon les données 2025 du service d'études de la Fédération internationale de padel reprises par AGI, il y a 5 321 terrains affiliés à la FITP, le Latium en tête (2 014), et l'Italie est le deuxième pays au monde pour la diffusion du padel ({agi}).</p>
<h2>À lire avec prudence</h2>
<ul>
<li><b>Licenciés ne veut pas dire pratiquants.</b> Le football n'est pas devenu moins populaire : on y joue énormément sans licence fédérale.</li>
<li>Le rapport du CONI ne compte pas le CSI (Centro Sportivo Italiano), qui regroupe une grande partie du football amateur et paroissial ({post}).</li>
<li>La FIGC reste la fédération la plus implantée, avec plus de 10 000 clubs affiliés, et reste la première en nombre de licenciés dans 11 régions ({post}, {sole}).</li>
</ul>
<p class="note">Sources : {sole} (27 octobre 2026), {post}, {fq}, {nome_src}, {fip}, {agi}.</p>''')
    corpo += box
    qa = [(L("Cos'è la FITP?", "What is the FITP?", "¿Qué es la FITP?", "Qu'est-ce que la FITP ?"),
           L("È la Federazione Italiana Tennis e Padel, la federazione sportiva nazionale riconosciuta dal CONI che governa tennis e padel in Italia. Fino al 2022 si chiamava FIT; il nuovo nome è in vigore dal 2023.",
             "It is the Italian Tennis and Padel Federation, the national sports federation recognised by CONI that governs tennis and padel in Italy. Until 2022 it was called FIT; the new name has applied since 2023.",
             "Es la Federación Italiana de Tenis y Pádel, la federación deportiva nacional reconocida por el CONI que gobierna el tenis y el pádel en Italia. Hasta 2022 se llamaba FIT; el nuevo nombre está en vigor desde 2023.",
             "C'est la Fédération italienne de tennis et de padel, la fédération sportive nationale reconnue par le CONI qui gère le tennis et le padel en Italie. Jusqu'en 2022, elle s'appelait FIT ; le nouveau nom s'applique depuis 2023.")),
          (L("Quanti tesserati ha la FITP?", "How many members does the FITP have?", "¿Cuántos federados tiene la FITP?", "Combien de licenciés compte la FITP ?"),
           L("1.162.477 nel 2024 secondo il monitoraggio CONI, più dei 1.123.054 della FIGC; nel 2025 è salita a 1.254.153.",
             "1,162,477 in 2024 according to CONI's monitoring report, more than the FIGC's 1,123,054; in 2025 it rose to 1,254,153.",
             "1.162.477 en 2024 según el informe del CONI, más que los 1.123.054 de la FIGC; en 2025 subió a 1.254.153.",
             "1 162 477 en 2024 selon le rapport du CONI, plus que les 1 123 054 de la FIGC ; en 2025, elle est montée à 1 254 153.")),
          (L("Il padel fa parte della FITP?", "Is padel part of the FITP?", "¿El pádel forma parte de la FITP?", "Le padel fait-il partie de la FITP ?"),
           L("Sì: è una disciplina della federazione dal 2008 e dal 2023 è anche nel nome. I tesserati padel non sono indicati separatamente nel rapporto CONI.",
             "Yes: it has been one of the federation's disciplines since 2008 and has been in its name since 2023. Padel members are not shown separately in CONI's report.",
             "Sí: es una disciplina de la federación desde 2008 y desde 2023 también forma parte de su nombre. Los federados de pádel no aparecen por separado en el informe del CONI.",
             "Oui : c'est une discipline de la fédération depuis 2008 et elle figure dans son nom depuis 2023. Les licenciés de padel n'apparaissent pas séparément dans le rapport du CONI.")),
          (L("In Italia si gioca più a tennis e padel che a calcio?", "Do more people in Italy play tennis and padel than football?", "¿En Italia se juega más al tenis y al pádel que al fútbol?", "En Italie, joue-t-on plus au tennis et au padel qu'au football ?"),
           L("Non necessariamente: il dato riguarda i tesserati delle federazioni. Il calcio si gioca molto anche senza tessera e il rapporto non conta il CSI, che raccoglie tanta attività amatoriale.",
             "Not necessarily: the figure concerns federation members. A lot of football is played without a membership, and the report does not count the CSI, which covers much amateur activity.",
             "No necesariamente: la cifra se refiere a los federados. El fútbol se juega mucho sin licencia y el informe no incluye al CSI, que agrupa mucha actividad aficionada.",
             "Pas forcément : le chiffre concerne les licenciés des fédérations. On joue beaucoup au football sans licence et le rapport ne compte pas le CSI, qui regroupe une grande partie de l'activité amateur."))]
    faq_htm, faq_ld = faq(qa)
    corpo += faq_htm
    titolo = L("La FITP supera la FIGC: tennis e padel hanno più tesserati del calcio", "The FITP overtakes the FIGC: tennis and padel now have more members than football",
               "La FITP supera a la FIGC: tenis y pádel ya tienen más federados que el fútbol", "La FITP dépasse la FIGC : le tennis et le padel comptent plus de licenciés que le football")
    scrivi_articolo(slug, titolo + " | PadelMetrix",
                    L("Cos'è la FITP, la Federazione Italiana Tennis e Padel, e come ha superato la Federcalcio per tesserati: numeri CONI 2024, ricavi, ruolo del padel e limiti del confronto.",
                      "What the FITP, the Italian Tennis and Padel Federation, is and how it overtook the football federation in members: CONI 2024 figures, revenue, padel's role and the limits of the comparison.",
                      "Qué es la FITP, la Federación Italiana de Tenis y Pádel, y cómo superó a la federación de fútbol en federados: cifras CONI 2024, ingresos, papel del pádel y límites de la comparación.",
                      "Ce qu'est la FITP, la Fédération italienne de tennis et de padel, et comment elle a dépassé la fédération de football en licenciés : chiffres CONI 2024, recettes, rôle du padel et limites de la comparaison."),
                    titolo, L("FITP e FIGC", "FITP and FIGC", "FITP y FIGC", "FITP et FIGC"), corpo, ld_extra=[faq_ld])
    return slug, titolo, L("Cos'è la FITP e i numeri del sorpasso sulla Federcalcio, con il ruolo del padel.", "What the FITP is and the numbers behind overtaking football, including padel's role.",
                           "Qué es la FITP y las cifras del adelantamiento a la federación de fútbol, con el papel del pádel.", "Ce qu'est la FITP et les chiffres du dépassement du football, avec le rôle du padel.")


# ---------------------------------------------------------------- Cinque guide pratiche (novembre 2026)
G5 = {
    "durata": ("quanto-dura-racchetta-padel-quando-cambiarla", "how-long-does-a-padel-racket-last", "cuanto-dura-una-pala-de-padel", "combien-de-temps-dure-une-raquette-de-padel"),
    "carbonio": ("carbonio-3k-12k-18k-racchetta-padel", "padel-racket-carbon-3k-12k-18k-explained", "carbono-3k-12k-18k-pala-padel", "carbone-3k-12k-18k-raquette-padel"),
    "peso": ("peso-racchetta-padel-quale-scegliere", "padel-racket-weight-how-heavy", "peso-pala-padel-cual-elegir", "poids-raquette-padel-lequel-choisir"),
    "over50": ("padel-over-50-racchetta-consigli", "padel-over-50-racket-and-tips", "padel-mayores-de-50-pala-consejos", "padel-apres-50-ans-raquette-conseils"),
    "scarpe": ("scarpe-padel-come-sceglierle", "padel-shoes-how-to-choose", "zapatillas-padel-como-elegirlas", "chaussures-padel-comment-choisir"),
}
for _k, (_it, _en, _es, _fr) in G5.items():
    S.SLUG[_it] = (_en, _es)
    S.SLUG_FR[_it] = _fr
    DATE_ART[_it] = "2026-11-06"

F5 = {
    "speed": ("PadelSpeed", "https://padelspeed.com/blogs/news/how-often-should-i-change-my-padel-racket"),
    "fyi": ("padel.fyi", "https://www.padel.fyi/articles/how-long-do-padel-rackets-last/"),
    "pps_k": ("PadelPROShop", "https://padelproshop.com/en/blogs/blog/tipos-palas-carbono-3k-12k-18k"),
    "pps_w": ("PadelPROShop", "https://padelproshop.com/en/blogs/blog/how-to-choose-the-ideal-weight-of-a-padel-racket"),
    "castillo": ("Castillo-Lozano, Rev. Andal. Med. Deporte 2015", "https://www.elsevier.es/es-revista-revista-andaluza-medicina-del-deporte-284-articulo-epidemiology-prevention-strategies-for-musculoskeletal-S1888754615000969"),
    "sadok": ("Sadok et al., Quality in Sport 2026", "https://apcz.umk.pl/QS/article/view/69884"),
    "shop": ("Padelshop", "https://padelshop.com/blogs/padel-tips/which-sole-should-you-choose-for-padel-shoes"),
}


def _f5(k):
    return fonte(F5[k][1], F5[k][0])


def _pmid(p):
    n = [float(x.replace(",", ".")) for x in _re.findall(r"\d{3}(?:[.,]\d)?", p or "")]
    n = [x for x in n if 250 <= x <= 400][:2]
    return sum(n) / len(n) if n else None


def _g(x):
    return f"{x:.0f}".replace(".", ",")


def _elenco_r(rs):
    out = []
    for r in rs:
        bits = [r["peso"] or "", FORMA(r["forma"]).lower() if r.get("forma") else "", LIVN(r["livello"]).lower() if r.get("livello") else ""]
        if r.get("prezzo"):
            bits.append(euro(r["prezzo"]))
        out.append(f'<li><a href="{url_r(r)}">{e(r["titolo"])}</a> — {e(" · ".join(b for b in bits if b))}</li>')
    return "<ul>" + "".join(out) + "</ul>"


def _box5(titolo, testo, btn, href):
    return (f'<div class="box" style="border:2px solid #C6F432;border-radius:12px;padding:20px 24px;margin:28px 0;background:#F4FBE3"><b>{titolo}</b><br>{testo}'
            f'<br><a class="btn" style="margin-top:12px;display:inline-block" href="{href}">{btn}</a></div>')


def _pubblica5(chiave, titolo, desc, crumb, corpo, qa, card, items=None):
    slug = G5[chiave][0]
    faq_htm, faq_ld = faq(qa)
    if items:
        RACCHETTE_ARTICOLO[slug] = [r["slug"] for r in items]
    scrivi_articolo(slug, titolo + " | PadelMetrix", desc, titolo, crumb, corpo + faq_htm, items=items, ld_extra=[faq_ld])
    return slug, titolo, card


def art_durata(db):
    epi, sel = P("guide", "racchetta-padel-epicondilite"), P("selettore")
    sp, fy = _f5("speed"), _f5("fyi")
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th>' + L("Quanto giochi", "How often you play", "Cuánto juegas", "Fréquence de jeu") + '</th><th>'
           + L("Durata indicativa", "Rough lifespan", "Duración orientativa", "Durée indicative") + '</th></tr></thead><tbody>'
           + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in [
               (L("Una volta a settimana o meno", "Once a week or less", "Una vez por semana o menos", "Une fois par semaine ou moins"), L("2–3 anni", "2–3 years", "2–3 años", "2 à 3 ans")),
               (L("2–3 volte a settimana", "2–3 times a week", "2–3 veces por semana", "2 à 3 fois par semaine"), L("12–18 mesi", "12–18 months", "12–18 meses", "12 à 18 mois")),
               (L("Agonisti o quasi tutti i giorni", "Competitive or almost daily", "Competición o casi a diario", "Compétition ou presque tous les jours"), L("6–12 mesi", "6–12 months", "6–12 meses", "6 à 12 mois"))])
           + "</tbody></table></div>")
    box = _box5(L("Hai deciso di cambiarla?", "Decided to replace it?", "¿Has decidido cambiarla?", "Vous avez décidé de la changer ?"),
                L("Il quiz ti propone le 3 racchette più adatte al tuo livello e al tuo gioco.", "The quiz suggests the 3 rackets that best fit your level and game.", "El test te propone las 3 palas más adecuadas a tu nivel y tu juego.", "Le quiz vous propose les 3 raquettes les plus adaptées à votre niveau et à votre jeu."),
                L("Trova la tua racchetta", "Find your racket", "Encuentra tu pala", "Trouve ta raquette"), sel)
    corpo = L(f'''<p><b>Una racchetta da padel dura in media da 6 mesi a 3 anni: dipende soprattutto da quanto giochi.</b> Prima di rompersi, perde le sue qualità: la gomma interna si comprime, la palla esce meno e il braccio riceve più vibrazioni. Ecco come capire quando è il momento di cambiarla.</p>
<h2>Quanto dura, in base a quanto giochi</h2>{tab}
<p>Sono indicazioni orientative, non scadenze ({sp}). Un'altra stima diffusa parla di circa 100 partite per chi gioca 2–3 volte a settimana ({fy}). Chi colpisce forte, soprattutto con racchette dalla gomma morbida, la consuma prima.</p>
<h2>I segnali che è ora di cambiarla</h2>
<ul><li><b>La palla "muore":</b> meno potenza e meno controllo, un tocco sordo all'impatto. È il primo segnale, e arriva prima dei danni visibili.</li>
<li><b>Zone morbide o irregolari</b> sul piatto: premendo con il pollice in punti diversi, alcune cedono più di altre.</li>
<li><b>Crepe sul telaio o sulla faccia:</b> una racchetta con il telaio incrinato si comporta in modo imprevedibile.</li>
<li><b>Più vibrazioni del solito</b> o rumori strani all'impatto.</li>
<li><b>Dolore nuovo a gomito, polso o spalla</b> senza altri motivi: una racchetta usurata trasmette più vibrazioni ({sp}).</li></ul>
<p>Un trucco: se puoi, confronta la tua racchetta con una nuova dello stesso modello. La differenza di rimbalzo si sente subito ({fy}).</p>
<h2>Cosa la fa invecchiare prima</h2>
<ul><li><b>Il caldo:</b> mai lasciarla in macchina d'estate. Meglio evitare temperature sopra i 40 °C ({fy}).</li>
<li><b>L'umidità:</b> la gomma assorbe acqua, si gonfia e poi si ritira asciugandosi.</li>
<li><b>I colpi contro pareti, suolo e racchetta del compagno</b>, e gli sfoghi di rabbia.</li>
<li><b>Il peso sopra:</b> nel borsone, non appoggiarci oggetti pesanti.</li></ul>
<h2>Come farla durare di più</h2>
<ul><li>Tienila in una custodia imbottita o termica, in un luogo asciutto.</li>
<li>Usa il paracolpi sul bordo, se ti aiuta a proteggere il telaio.</li>
<li>Cambia spesso l'overgrip: non allunga la vita della racchetta, ma mantiene presa e sensazioni.</li>
<li>Le crepe superficiali si possono riparare, ma la racchetta non tornerà come nuova.</li></ul>
<p>Se hai già dolore al gomito, non aspettare che la racchetta sia distrutta: leggi la guida alle <a href="{epi}">racchette per l'epicondilite</a>.</p>{box}
<p class="note">Fonti: {sp}, {fy}. I tempi sono indicativi e cambiano con materiali, stile di gioco e cura.</p>''',
              f'''<p><b>A padel racket lasts on average from 6 months to 3 years, depending mostly on how much you play.</b> Before it breaks, it loses its qualities: the inner rubber compresses, the ball comes off the face less and your arm takes more vibration. Here is how to tell when it is time to replace it.</p>
<h2>How long it lasts, by how much you play</h2>{tab}
<p>These are guidelines, not expiry dates ({sp}). Another common estimate is about 100 sessions for someone playing 2–3 times a week ({fy}). Hard hitters, especially with soft-core rackets, wear them out sooner.</p>
<h2>Signs it is time for a new one</h2>
<ul><li><b>The ball feels "dead":</b> less power and control, a dull feel at impact. It is the first sign, and it comes before any visible damage.</li>
<li><b>Soft or uneven spots</b> on the face: pressing with your thumb in different places, some give more than others.</li>
<li><b>Cracks in the frame or face:</b> a racket with a cracked frame behaves unpredictably.</li>
<li><b>More vibration than usual</b> or strange sounds at impact.</li>
<li><b>New pain in the elbow, wrist or shoulder</b> with no other cause: a worn racket passes on more vibration ({sp}).</li></ul>
<p>A tip: if you can, compare your racket with a new one of the same model. The difference in bounce is obvious straight away ({fy}).</p>
<h2>What ages it faster</h2>
<ul><li><b>Heat:</b> never leave it in the car in summer. Avoid temperatures above 40 °C ({fy}).</li>
<li><b>Humidity:</b> the rubber absorbs water, swells and then shrinks as it dries.</li>
<li><b>Hitting walls, the floor or your partner's racket</b>, and taking your frustration out on it.</li>
<li><b>Weight on top:</b> don't put heavy objects on it in your bag.</li></ul>
<h2>How to make it last longer</h2>
<ul><li>Keep it in a padded or thermal cover, somewhere dry.</li>
<li>Use an edge protector if it helps protect the frame.</li>
<li>Change the overgrip often: it won't extend the racket's life, but it keeps grip and feel.</li>
<li>Surface cracks can be repaired, but the racket won't play like new.</li></ul>
<p>If you already have elbow pain, don't wait for the racket to fall apart: read the guide to <a href="{epi}">rackets for tennis elbow</a>.</p>{box}
<p class="note">Sources: {sp}, {fy}. Timings are guidelines and vary with materials, playing style and care.</p>''',
              f'''<p><b>Una pala de pádel dura de media entre 6 meses y 3 años: depende sobre todo de cuánto juegues.</b> Antes de romperse, pierde sus cualidades: la goma interior se comprime, la bola sale menos y el brazo recibe más vibraciones. Así puedes saber cuándo toca cambiarla.</p>
<h2>Cuánto dura, según cuánto juegues</h2>{tab}
<p>Son orientaciones, no fechas de caducidad ({sp}). Otra estimación habitual habla de unos 100 partidos para quien juega 2–3 veces por semana ({fy}). Quien pega fuerte, sobre todo con palas de goma blanda, la desgasta antes.</p>
<h2>Las señales de que hay que cambiarla</h2>
<ul><li><b>La bola "muere":</b> menos potencia y control, un tacto sordo al impactar. Es la primera señal, y llega antes que los daños visibles.</li>
<li><b>Zonas blandas o irregulares</b> en la cara: al presionar con el pulgar en distintos puntos, algunos ceden más que otros.</li>
<li><b>Grietas en el marco o en la cara:</b> una pala con el marco agrietado se comporta de forma imprevisible.</li>
<li><b>Más vibraciones de lo normal</b> o ruidos extraños al golpear.</li>
<li><b>Dolor nuevo en codo, muñeca u hombro</b> sin otra causa: una pala desgastada transmite más vibraciones ({sp}).</li></ul>
<p>Un truco: si puedes, compara tu pala con una nueva del mismo modelo. La diferencia de rebote se nota enseguida ({fy}).</p>
<h2>Qué la hace envejecer antes</h2>
<ul><li><b>El calor:</b> nunca la dejes en el coche en verano. Mejor evitar temperaturas por encima de 40 °C ({fy}).</li>
<li><b>La humedad:</b> la goma absorbe agua, se hincha y luego se contrae al secarse.</li>
<li><b>Los golpes contra paredes, suelo y la pala del compañero</b>, y los arrebatos de rabia.</li>
<li><b>El peso encima:</b> en el paletero, no le pongas objetos pesados.</li></ul>
<h2>Cómo hacer que dure más</h2>
<ul><li>Guárdala en una funda acolchada o térmica, en un lugar seco.</li>
<li>Usa protector en el marco si te ayuda a protegerlo.</li>
<li>Cambia a menudo el overgrip: no alarga la vida de la pala, pero mantiene agarre y sensaciones.</li>
<li>Las grietas superficiales se pueden reparar, pero la pala no volverá a ser nueva.</li></ul>
<p>Si ya tienes dolor de codo, no esperes a que la pala esté destrozada: lee la guía de <a href="{epi}">palas para la epicondilitis</a>.</p>{box}
<p class="note">Fuentes: {sp}, {fy}. Los plazos son orientativos y cambian con materiales, estilo de juego y cuidado.</p>''',
              f'''<p><b>Une raquette de padel dure en moyenne de 6 mois à 3 ans : cela dépend surtout de la fréquence à laquelle vous jouez.</b> Avant de casser, elle perd ses qualités : la gomme intérieure se tasse, la balle sort moins et le bras reçoit plus de vibrations. Voici comment savoir quand la changer.</p>
<h2>Combien de temps elle dure, selon votre fréquence de jeu</h2>{tab}
<p>Ce sont des repères, pas des dates de péremption ({sp}). Une autre estimation courante parle d'environ 100 parties pour qui joue 2 à 3 fois par semaine ({fy}). Les gros frappeurs, surtout avec des raquettes à gomme souple, l'usent plus vite.</p>
<h2>Les signes qu'il est temps de la changer</h2>
<ul><li><b>La balle « meurt » :</b> moins de puissance et de contrôle, un toucher sourd à l'impact. C'est le premier signe, et il arrive avant les dégâts visibles.</li>
<li><b>Des zones molles ou irrégulières</b> sur le tamis : en appuyant avec le pouce à différents endroits, certains cèdent plus que d'autres.</li>
<li><b>Des fissures sur le cadre ou le tamis :</b> une raquette au cadre fissuré se comporte de façon imprévisible.</li>
<li><b>Plus de vibrations que d'habitude</b> ou des bruits étranges à l'impact.</li>
<li><b>Une nouvelle douleur au coude, au poignet ou à l'épaule</b> sans autre cause : une raquette usée transmet plus de vibrations ({sp}).</li></ul>
<p>Une astuce : si possible, comparez votre raquette avec une neuve du même modèle. La différence de rebond se sent tout de suite ({fy}).</p>
<h2>Ce qui la fait vieillir plus vite</h2>
<ul><li><b>La chaleur :</b> ne la laissez jamais dans la voiture en été. Évitez les températures au-dessus de 40 °C ({fy}).</li>
<li><b>L'humidité :</b> la gomme absorbe l'eau, gonfle puis se rétracte en séchant.</li>
<li><b>Les chocs contre les murs, le sol et la raquette du partenaire</b>, et les accès de colère.</li>
<li><b>Le poids posé dessus :</b> dans le sac, n'y posez pas d'objets lourds.</li></ul>
<h2>Comment la faire durer plus longtemps</h2>
<ul><li>Rangez-la dans une housse rembourrée ou isotherme, dans un endroit sec.</li>
<li>Utilisez une protection de cadre si elle vous aide à le protéger.</li>
<li>Changez souvent le surgrip : cela n'allonge pas la vie de la raquette, mais garde l'adhérence et les sensations.</li>
<li>Les fissures superficielles se réparent, mais la raquette ne redeviendra pas neuve.</li></ul>
<p>Si vous avez déjà mal au coude, n'attendez pas que la raquette soit cassée : lisez le guide des <a href="{epi}">raquettes pour l'épicondylite</a>.</p>{box}
<p class="note">Sources : {sp}, {fy}. Les durées sont indicatives et varient selon les matériaux, le style de jeu et l'entretien.</p>''')
    qa = [(L("Quanto dura una racchetta da padel?", "How long does a padel racket last?", "¿Cuánto dura una pala de pádel?", "Combien de temps dure une raquette de padel ?"),
           L("Da 6 mesi a 3 anni: circa 2–3 anni giocando una volta a settimana, 12–18 mesi giocando 2–3 volte a settimana, 6–12 mesi per chi gioca quasi tutti i giorni.",
             "From 6 months to 3 years: about 2–3 years playing once a week, 12–18 months playing 2–3 times a week, 6–12 months for those who play almost every day.",
             "De 6 meses a 3 años: unos 2–3 años jugando una vez por semana, 12–18 meses jugando 2–3 veces por semana y 6–12 meses para quien juega casi a diario.",
             "De 6 mois à 3 ans : environ 2 à 3 ans en jouant une fois par semaine, 12 à 18 mois en jouant 2 à 3 fois par semaine, 6 à 12 mois pour qui joue presque tous les jours.")),
          (L("Come capisco se la racchetta è da cambiare?", "How do I know if my racket needs replacing?", "¿Cómo sé si tengo que cambiar la pala?", "Comment savoir si ma raquette est à changer ?"),
           L("La palla esce meno e il tocco è sordo, ci sono zone morbide sul piatto, crepe, più vibrazioni o un nuovo dolore al braccio.",
             "The ball comes off the face less and feels dull, there are soft spots on the face, cracks, more vibration or new arm pain.",
             "La bola sale menos y el tacto es sordo, hay zonas blandas en la cara, grietas, más vibraciones o un dolor nuevo en el brazo.",
             "La balle sort moins et le toucher est sourd, il y a des zones molles sur le tamis, des fissures, plus de vibrations ou une nouvelle douleur au bras.")),
          (L("Il caldo rovina la racchetta?", "Does heat damage a racket?", "¿El calor estropea la pala?", "La chaleur abîme-t-elle la raquette ?"),
           L("Sì: le alte temperature, per esempio in auto d'estate, accelerano il degrado della gomma interna.",
             "Yes: high temperatures, such as in a car in summer, speed up the breakdown of the inner rubber.",
             "Sí: las altas temperaturas, por ejemplo en el coche en verano, aceleran el deterioro de la goma interior.",
             "Oui : les fortes chaleurs, par exemple dans une voiture en été, accélèrent la dégradation de la gomme intérieure."))]
    titolo = L("Quanto dura una racchetta da padel e quando cambiarla", "How long does a padel racket last and when to replace it",
               "Cuánto dura una pala de pádel y cuándo cambiarla", "Combien de temps dure une raquette de padel et quand la changer")
    return _pubblica5("durata", titolo,
                      L("Quanto dura una racchetta da padel in base a quanto giochi, i segnali che è da cambiare e come farla durare di più.",
                        "How long a padel racket lasts depending on how much you play, the signs it needs replacing and how to make it last longer.",
                        "Cuánto dura una pala de pádel según cuánto juegues, las señales de que hay que cambiarla y cómo hacer que dure más.",
                        "Combien de temps dure une raquette de padel selon votre fréquence de jeu, les signes qu'elle est à changer et comment la faire durer."),
                      L("Durata racchetta", "Racket lifespan", "Duración de la pala", "Durée de la raquette"), corpo, qa,
                      L("Da 6 mesi a 3 anni: i segnali che è ora di cambiarla.", "From 6 months to 3 years: the signs it's time for a new one.",
                        "De 6 meses a 3 años: las señales de que toca cambiarla.", "De 6 mois à 3 ans : les signes qu'il faut la changer."))


def art_carbonio(db):
    ad = [r for r in db if r["categoria"] != "junior"]
    gruppi = {}
    for r in ad:
        sup = r.get("superficie") or ""
        ks = set(_re.findall(r"(\d{1,2})\s?K\b", sup, _re.I))
        for k in ks:
            gruppi.setdefault(k + "K", []).append(r)
        if not ks and _re.search(r"vetro|glass", sup, _re.I):
            gruppi.setdefault("vetro", []).append(r)
    righe = []
    for k in ("3K", "12K", "18K", "24K", "vetro"):
        rs = gruppi.get(k, [])
        pz = sorted(r["prezzo"] for r in rs if r.get("prezzo"))
        med = euro(pz[len(pz) // 2]) if pz else "—"
        avz = sum(1 for r in rs if r.get("livello") in ("avanzato", "professionale"))
        nome = L("Fibra di vetro (senza carbonio dichiarato)", "Fiberglass (no carbon stated)", "Fibra de vidrio (sin carbono declarado)", "Fibre de verre (sans carbone déclaré)") if k == "vetro" else L(f"Carbonio {k}", f"{k} carbon", f"Carbono {k}", f"Carbone {k}")
        righe.append((nome, len(rs), med, f"{round(100 * avz / len(rs))} %" if (rs and S.lang() == "fr") else (f"{round(100 * avz / len(rs))}%" if rs else "—")))
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th>' + L("Faccia", "Face", "Cara", "Tamis") + '</th><th>' + L("Modelli", "Models", "Modelos", "Modèles") + '</th><th>'
           + L("Prezzo di listino mediano", "Median list price", "Precio de catálogo mediano", "Prix catalogue médian") + '</th><th>' + L("Per avanzati o pro", "For advanced or pro", "Para avanzados o pro", "Pour avancés ou pros") + '</th></tr></thead><tbody>'
           + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in righe) + "</tbody></table></div>")
    n3, n12, n18 = (len(gruppi.get(k, [])) for k in ("3K", "12K", "18K"))
    pk, gl = _f5("pps_k"), P("glossario", "carbonio-3k-12k-18k")
    cmp = P("confronta")
    box = _box5(L("Confronta i materiali sul campo", "Compare materials side by side", "Compara los materiales", "Comparez les matériaux"),
                L("Metti fianco a fianco fino a 4 racchette e guarda subito faccia, gomma e prezzo.", "Put up to 4 rackets side by side and see face, core and price at a glance.", "Pon hasta 4 palas una al lado de otra y mira de un vistazo cara, goma y precio.", "Mettez jusqu'à 4 raquettes côte à côte et voyez d'un coup d'œil tamis, gomme et prix."),
                L("Confronta le racchette", "Compare rackets", "Comparar palas", "Comparer les raquettes"), cmp)
    corpo = L(f'''<p><b>3K, 12K, 18K indicano quanti filamenti di carbonio compongono ogni fascio del tessuto: 3.000, 12.000, 18.000. Non è una classifica di qualità: un numero più alto non vuol dire racchetta migliore, né più cara.</b> Il tocco di una racchetta dipende anche da gomma, numero di strati, resina e telaio.</p>
<h2>Cosa significa la K</h2>
<p>Le facce in carbonio sono fatte di un tessuto di fasci di filamenti. La K indica le migliaia di filamenti per fascio: con 3K i fasci sono sottili e il tessuto è fitto, con 12K e 18K i fasci sono più grossi ({pk}). Cambia la trama, e con essa un po' la rigidità e le sensazioni, ma il valore da solo non dice come si comporterà la racchetta (vedi anche il <a href="{gl}">glossario</a>).</p>
<h2>Le differenze che si leggono di solito</h2>
<ul><li><b>3K:</b> tocco più secco e diretto, molto controllo; la potenza dipende di più dal tuo braccio.</li>
<li><b>12K:</b> compromesso tra fermezza e comfort, adatto a giocatori polivalenti.</li>
<li><b>18K:</b> risposta più solida ed esplosiva quando acceleri, più vibrazioni fuori dal punto dolce.</li></ul>
<p>Sono descrizioni qualitative dei negozi, senza misure di laboratorio: lo stesso articolo che le propone ricorda che "più filamenti" non significa "migliore" e che conta molto la costruzione complessiva ({pk}).</p>
<h2>Cosa dicono i dati del nostro database</h2>
<p>Abbiamo contato il tipo di carbonio dichiarato sulle {len(ad)} racchette adulte del database. Il 3K è il più diffuso ({n3} modelli), seguito da 12K ({n12}) e 18K ({n18}).</p>
{tab}
<p>Due cose saltano all'occhio. Primo, i prezzi mediani di 3K, 12K e 18K sono molto vicini: il tipo di carbonio non spiega il prezzo. Secondo, la vera differenza è tra carbonio e fibra di vetro: le facce in vetro costano molto meno e sono pensate soprattutto per chi inizia.</p>
<h2>Quale scegliere</h2>
<ul><li><b>Inizi o hai problemi al braccio:</b> fibra di vetro o carbonio con gomma morbida; il tipo di K conta poco.</li>
<li><b>Giochi di controllo e piazzamento:</b> spesso ti troverai bene con un 3K.</li>
<li><b>Giochi polivalente o d'attacco:</b> guarda 12K e 18K, ma prova sempre forma, peso e bilanciamento prima del numero.</li></ul>{box}
<p class="note">Dati: database PadelMetrix, materiali dichiarati da produttori e rivenditori; prezzi di listino dove indicati. Le caratteristiche qualitative vengono da {pk}.</p>''',
              f'''<p><b>3K, 12K and 18K tell you how many carbon filaments make up each bundle of the weave: 3,000, 12,000, 18,000. It is not a quality ranking: a higher number doesn't mean a better racket, or a more expensive one.</b> How a racket feels also depends on the core, the number of layers, the resin and the frame.</p>
<h2>What the K means</h2>
<p>Carbon faces are made of a fabric woven from bundles of filaments. The K is the thousands of filaments per bundle: with 3K the bundles are thin and the weave is tight, with 12K and 18K the bundles are thicker ({pk}). It changes the weave, and with it some of the stiffness and feel, but the number alone doesn't tell you how the racket will play (see also the <a href="{gl}">glossary</a>).</p>
<h2>The differences you usually read about</h2>
<ul><li><b>3K:</b> drier, more direct feel, lots of control; power depends more on your arm.</li>
<li><b>12K:</b> a compromise between firmness and comfort, suited to all-round players.</li>
<li><b>18K:</b> a more solid, explosive response when you accelerate, more vibration outside the sweet spot.</li></ul>
<p>These are retailers' qualitative descriptions, without lab measurements: the same article that offers them reminds readers that "more filaments" doesn't mean "better" and that the overall construction matters a lot ({pk}).</p>
<h2>What our database shows</h2>
<p>We counted the type of carbon stated for the {len(ad)} adult rackets in the database. 3K is the most common ({n3} models), followed by 12K ({n12}) and 18K ({n18}).</p>
{tab}
<p>Two things stand out. First, the median prices of 3K, 12K and 18K are very close: the type of carbon doesn't explain the price. Second, the real difference is between carbon and fiberglass: fiberglass faces cost much less and are aimed mostly at beginners.</p>
<h2>Which to choose</h2>
<ul><li><b>You're starting out or have arm problems:</b> fiberglass or carbon with a soft core; the K matters little.</li>
<li><b>You play a control and placement game:</b> you'll often get on well with 3K.</li>
<li><b>You play all-round or attacking padel:</b> look at 12K and 18K, but always check shape, weight and balance before the number.</li></ul>{box}
<p class="note">Data: PadelMetrix database, materials stated by manufacturers and retailers; list prices where given. Qualitative characteristics from {pk}.</p>''',
              f'''<p><b>3K, 12K y 18K indican cuántos filamentos de carbono forman cada haz del tejido: 3.000, 12.000, 18.000. No es una clasificación de calidad: un número más alto no significa una pala mejor ni más cara.</b> El tacto de una pala depende también de la goma, el número de capas, la resina y el marco.</p>
<h2>Qué significa la K</h2>
<p>Las caras de carbono están hechas de un tejido de haces de filamentos. La K indica los miles de filamentos por haz: con 3K los haces son finos y el tejido es tupido; con 12K y 18K los haces son más gruesos ({pk}). Cambia la trama y, con ella, algo de la rigidez y las sensaciones, pero el número por sí solo no dice cómo se comportará la pala (ver también el <a href="{gl}">glosario</a>).</p>
<h2>Las diferencias que se suelen leer</h2>
<ul><li><b>3K:</b> tacto más seco y directo, mucho control; la potencia depende más de tu brazo.</li>
<li><b>12K:</b> equilibrio entre firmeza y comodidad, adecuado para jugadores polivalentes.</li>
<li><b>18K:</b> respuesta más sólida y explosiva al acelerar, más vibración fuera del punto dulce.</li></ul>
<p>Son descripciones cualitativas de tiendas, sin mediciones de laboratorio: el mismo artículo que las propone recuerda que "más filamentos" no significa "mejor" y que la construcción global cuenta mucho ({pk}).</p>
<h2>Qué dicen los datos de nuestra base</h2>
<p>Hemos contado el tipo de carbono declarado en las {len(ad)} palas de adulto de la base de datos. El 3K es el más frecuente ({n3} modelos), seguido del 12K ({n12}) y el 18K ({n18}).</p>
{tab}
<p>Llaman la atención dos cosas. Primero, los precios medianos de 3K, 12K y 18K son muy parecidos: el tipo de carbono no explica el precio. Segundo, la verdadera diferencia está entre carbono y fibra de vidrio: las caras de vidrio cuestan mucho menos y están pensadas sobre todo para quien empieza.</p>
<h2>Cuál elegir</h2>
<ul><li><b>Empiezas o tienes problemas en el brazo:</b> fibra de vidrio o carbono con goma blanda; el tipo de K importa poco.</li>
<li><b>Juegas de control y colocación:</b> a menudo te irá bien un 3K.</li>
<li><b>Juegas polivalente o de ataque:</b> mira 12K y 18K, pero comprueba siempre forma, peso y balance antes que el número.</li></ul>{box}
<p class="note">Datos: base de datos PadelMetrix, materiales declarados por fabricantes y tiendas; precios de catálogo donde se indican. Las características cualitativas proceden de {pk}.</p>''',
              f'''<p><b>3K, 12K et 18K indiquent combien de filaments de carbone composent chaque mèche du tissu : 3 000, 12 000, 18 000. Ce n'est pas un classement de qualité : un chiffre plus élevé ne signifie pas une meilleure raquette, ni une raquette plus chère.</b> Le toucher d'une raquette dépend aussi de la gomme, du nombre de couches, de la résine et du cadre.</p>
<h2>Ce que signifie le K</h2>
<p>Les tamis en carbone sont faits d'un tissu de mèches de filaments. Le K indique les milliers de filaments par mèche : en 3K les mèches sont fines et le tissage serré, en 12K et 18K elles sont plus épaisses ({pk}). Cela change le tissage, et avec lui un peu la rigidité et les sensations, mais le chiffre seul ne dit pas comment la raquette se comportera (voir aussi le <a href="{gl}">glossaire</a>).</p>
<h2>Les différences qu'on lit en général</h2>
<ul><li><b>3K :</b> toucher plus sec et direct, beaucoup de contrôle ; la puissance dépend davantage de votre bras.</li>
<li><b>12K :</b> compromis entre fermeté et confort, adapté aux joueurs polyvalents.</li>
<li><b>18K :</b> réponse plus solide et explosive quand vous accélérez, plus de vibrations hors du sweet spot.</li></ul>
<p>Ce sont des descriptions qualitatives de revendeurs, sans mesures en laboratoire : l'article même qui les propose rappelle que « plus de filaments » ne veut pas dire « meilleur » et que la construction globale compte beaucoup ({pk}).</p>
<h2>Ce que disent les données de notre base</h2>
<p>Nous avons compté le type de carbone déclaré pour les {len(ad)} raquettes adultes de la base. Le 3K est le plus répandu ({n3} modèles), suivi du 12K ({n12}) et du 18K ({n18}).</p>
{tab}
<p>Deux choses ressortent. D'abord, les prix médians du 3K, du 12K et du 18K sont très proches : le type de carbone n'explique pas le prix. Ensuite, la vraie différence se fait entre carbone et fibre de verre : les tamis en verre coûtent bien moins cher et visent surtout les débutants.</p>
<h2>Lequel choisir</h2>
<ul><li><b>Vous débutez ou avez des problèmes au bras :</b> fibre de verre ou carbone avec gomme souple ; le K compte peu.</li>
<li><b>Vous jouez contrôle et placement :</b> vous vous sentirez souvent bien avec un 3K.</li>
<li><b>Vous jouez polyvalent ou en attaque :</b> regardez le 12K et le 18K, mais vérifiez toujours forme, poids et équilibre avant le chiffre.</li></ul>{box}
<p class="note">Données : base PadelMetrix, matériaux déclarés par les fabricants et les revendeurs ; prix catalogue quand ils sont indiqués. Caractéristiques qualitatives tirées de {pk}.</p>''')
    qa = [(L("Cosa vuol dire 3K, 12K, 18K in una racchetta da padel?", "What do 3K, 12K and 18K mean on a padel racket?", "¿Qué significa 3K, 12K, 18K en una pala de pádel?", "Que signifient 3K, 12K et 18K sur une raquette de padel ?"),
           L("Il numero di migliaia di filamenti per fascio del tessuto di carbonio: 3.000, 12.000 o 18.000.", "The thousands of filaments per bundle of the carbon weave: 3,000, 12,000 or 18,000.",
             "Los miles de filamentos por haz del tejido de carbono: 3.000, 12.000 o 18.000.", "Le nombre de milliers de filaments par mèche du tissu de carbone : 3 000, 12 000 ou 18 000.")),
          (L("Il carbonio 18K è migliore del 3K?", "Is 18K carbon better than 3K?", "¿El carbono 18K es mejor que el 3K?", "Le carbone 18K est-il meilleur que le 3K ?"),
           L("No: cambia il tocco, non la qualità. Il comportamento dipende anche da gomma, strati e telaio.", "No: it changes the feel, not the quality. How a racket plays also depends on the core, layers and frame.",
             "No: cambia el tacto, no la calidad. El comportamiento depende también de la goma, las capas y el marco.", "Non : cela change le toucher, pas la qualité. Le comportement dépend aussi de la gomme, des couches et du cadre.")),
          (L("Le racchette 18K costano di più?", "Do 18K rackets cost more?", "¿Las palas 18K cuestan más?", "Les raquettes 18K coûtent-elles plus cher ?"),
           L("Nel nostro database no: i prezzi di listino mediani di 3K, 12K e 18K sono molto vicini. La differenza di prezzo vera è tra carbonio e fibra di vetro.",
             "Not in our database: the median list prices of 3K, 12K and 18K are very close. The real price gap is between carbon and fiberglass.",
             "En nuestra base no: los precios de catálogo medianos de 3K, 12K y 18K son muy parecidos. La diferencia real de precio está entre carbono y fibra de vidrio.",
             "Pas dans notre base : les prix catalogue médians du 3K, du 12K et du 18K sont très proches. Le vrai écart de prix se fait entre carbone et fibre de verre."))]
    titolo = L("Carbonio 3K, 12K, 18K nelle racchette da padel: cosa cambia davvero", "3K, 12K and 18K carbon in padel rackets: what really changes",
               "Carbono 3K, 12K y 18K en las palas de pádel: qué cambia de verdad", "Carbone 3K, 12K et 18K dans les raquettes de padel : ce qui change vraiment")
    return _pubblica5("carbonio", titolo,
                      L("Cosa significa la K del carbonio nelle racchette da padel, le differenze tra 3K, 12K e 18K e cosa dicono prezzi e livelli del nostro database.",
                        "What the K in padel racket carbon means, the differences between 3K, 12K and 18K and what prices and levels in our database show.",
                        "Qué significa la K del carbono en las palas de pádel, las diferencias entre 3K, 12K y 18K y qué dicen precios y niveles de nuestra base.",
                        "Ce que signifie le K du carbone dans les raquettes de padel, les différences entre 3K, 12K et 18K et ce que montrent prix et niveaux de notre base."),
                      L("Carbonio 3K, 12K, 18K", "3K, 12K, 18K carbon", "Carbono 3K, 12K, 18K", "Carbone 3K, 12K, 18K"), corpo, qa,
                      L("Cosa significa la K e perché non è una classifica di qualità.", "What the K means and why it isn't a quality ranking.",
                        "Qué significa la K y por qué no es una clasificación de calidad.", "Ce que signifie le K et pourquoi ce n'est pas un classement de qualité."))


def art_peso(db):
    ad = [r for r in db if r["categoria"] != "junior"]
    pesi = [(r, _pmid(r["peso"])) for r in ad]
    pesi = [(r, w) for r, w in pesi if w]
    med_all = sorted(w for _, w in pesi)[len(pesi) // 2]
    livelli = [("principiante", ("principiante", "principiante-intermedio")), ("intermedio", ("intermedio", "intermedio-avanzato")), ("avanzato", ("avanzato", "professionale"))]
    righe = []
    for nome, keys in livelli:
        ws = sorted(w for r, w in pesi if r.get("livello") in keys)
        if ws:
            righe.append((LIVN(nome), len(ws), _g(ws[len(ws) // 2]), f"{_g(ws[0])}–{_g(ws[-1])}"))
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th>' + L("Livello", "Level", "Nivel", "Niveau") + '</th><th>' + L("Modelli", "Models", "Modelos", "Modèles") + '</th><th>'
           + L("Peso tipico (g)", "Typical weight (g)", "Peso típico (g)", "Poids type (g)") + '</th><th>' + L("Da – a (g)", "Range (g)", "De – a (g)", "De – à (g)") + '</th></tr></thead><tbody>'
           + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in righe) + "</tbody></table></div>")
    leggere = [r for r, w in sorted(pesi, key=lambda x: x[1]) if w <= 352.5][:8]
    pw = _f5("pps_w")
    epi, don, bimbi = P("guide", "racchetta-padel-epicondilite"), P("guide", "racchette-padel-donna"), P("bambini")
    box = _box5(L("Vuoi un consiglio su misura?", "Want a tailored suggestion?", "¿Quieres un consejo a medida?", "Vous voulez un conseil sur mesure ?"),
                L("Nel quiz indichi il peso che preferisci e se hai problemi al braccio.", "In the quiz you choose your preferred weight and say whether you have arm problems.", "En el test indicas el peso que prefieres y si tienes problemas en el brazo.", "Dans le quiz, vous indiquez le poids préféré et si vous avez des problèmes au bras."),
                L("Trova la tua racchetta", "Find your racket", "Encuentra tu pala", "Trouve ta raquette"), P("selettore"))
    corpo = L(f'''<p><b>Per la maggior parte dei giocatori adulti il peso giusto è tra 350 e 370 grammi. Chi inizia, chi ha problemi al braccio e molte donne stanno bene sotto i 360 g; chi gioca d'attacco e ha il braccio allenato può salire a 370 g e oltre.</b> Conta però anche il bilanciamento: due racchette dello stesso peso possono sembrare molto diverse.</p>
<h2>Il peso consigliato</h2>
<ul><li><b>Principianti:</b> sotto i 360 g.</li>
<li><b>Intermedi:</b> 360–370 g.</li>
<li><b>Avanzati e agonisti:</b> 370–390 g, solo con un braccio allenato.</li>
<li><b>Donne:</b> 330–355 g per comfort e controllo, fino a 360–370 g con livello e forza maggiori.</li>
<li><b>Epicondilite:</b> meglio non superare i 370 g, con bilanciamento basso e tocco morbido.</li>
<li><b>Ragazzi:</b> non più di 330 g; per i più piccoli vedi la <a href="{bimbi}">guida per bambini</a>.</li></ul>
<p class="note">Indicazioni di {pw}. Il peso corporeo e la preparazione fisica contano quanto il livello.</p>
<h2>Quanto pesano davvero le racchette in vendita</h2>
<p>Nel nostro database il peso tipico (mediana) di una racchetta adulta è di {_g(med_all)} g, calcolato su {len(pesi)} modelli con peso dichiarato. Per livello:</p>
{tab}
<p>La differenza tra livelli è piccola: i produttori fanno racchette da principiante solo poco più leggere di quelle da avanzato. Per questo, se cerchi leggerezza, conviene guardare le versioni "Light" o "Lite" dei modelli.</p>
<h2>Il bilanciamento conta quanto il peso</h2>
<ul><li><b>Basso</b> (peso verso il manico): più controllo e maneggevolezza, meno fatica.</li>
<li><b>Medio:</b> un compromesso tra controllo e potenza.</li>
<li><b>Alto</b> (peso verso la testa): più potenza nello smash, ma serve un braccio allenato. Una racchetta da 360 g con bilanciamento alto può sembrare più pesante di una da 370 g bilanciata bassa.</li></ul>
<h2>Come capire se è troppo pesante</h2>
<p>Se a fine partita il braccio è stanco, se arrivi in ritardo sui colpi a rete o se compare un fastidio a gomito o spalla, scendi di qualche grammo o scegli un bilanciamento più basso ({pw}). Leggi anche le guide alle <a href="{epi}">racchette per l'epicondilite</a> e alle <a href="{don}">racchette da donna</a>.</p>
<h2>Le racchette adulte più leggere del database</h2>{_elenco_r(leggere)}{box}''',
              f'''<p><b>For most adult players the right weight is between 350 and 370 grams. Beginners, players with arm problems and many women do well under 360 g; attacking players with a trained arm can go to 370 g and above.</b> Balance matters too: two rackets with the same weight can feel very different.</p>
<h2>Recommended weight</h2>
<ul><li><b>Beginners:</b> under 360 g.</li>
<li><b>Intermediate:</b> 360–370 g.</li>
<li><b>Advanced and competitive:</b> 370–390 g, only with a trained arm.</li>
<li><b>Women:</b> 330–355 g for comfort and control, up to 360–370 g with more level and strength.</li>
<li><b>Tennis elbow:</b> best not to go over 370 g, with a low balance and soft feel.</li>
<li><b>Juniors:</b> no more than 330 g; for younger children see the <a href="{bimbi}">kids' guide</a>.</li></ul>
<p class="note">Guidance from {pw}. Body weight and fitness matter as much as level.</p>
<h2>How much the rackets on sale really weigh</h2>
<p>In our database the typical (median) weight of an adult racket is {_g(med_all)} g, based on {len(pesi)} models with a stated weight. By level:</p>
{tab}
<p>The difference between levels is small: manufacturers make beginner rackets only slightly lighter than advanced ones. So if you want something light, look at the "Light" or "Lite" versions of models.</p>
<h2>Balance matters as much as weight</h2>
<ul><li><b>Low</b> (weight towards the handle): more control and manoeuvrability, less fatigue.</li>
<li><b>Medium:</b> a compromise between control and power.</li>
<li><b>High</b> (weight towards the head): more power on the smash, but you need a trained arm. A 360 g racket with a high balance can feel heavier than a 370 g one with a low balance.</li></ul>
<h2>How to tell if it's too heavy</h2>
<p>If your arm is tired at the end of a match, you're late on shots at the net or you feel discomfort in your elbow or shoulder, drop a few grams or choose a lower balance ({pw}). See also the guides to <a href="{epi}">rackets for tennis elbow</a> and <a href="{don}">women's rackets</a>.</p>
<h2>The lightest adult rackets in the database</h2>{_elenco_r(leggere)}{box}''',
              f'''<p><b>Para la mayoría de los jugadores adultos el peso adecuado está entre 350 y 370 gramos. Quien empieza, quien tiene problemas en el brazo y muchas mujeres van bien por debajo de 360 g; quien juega al ataque y tiene el brazo entrenado puede subir a 370 g o más.</b> Pero también cuenta el balance: dos palas del mismo peso pueden sentirse muy distintas.</p>
<h2>El peso recomendado</h2>
<ul><li><b>Principiantes:</b> por debajo de 360 g.</li>
<li><b>Intermedios:</b> 360–370 g.</li>
<li><b>Avanzados y competición:</b> 370–390 g, solo con el brazo entrenado.</li>
<li><b>Mujeres:</b> 330–355 g para comodidad y control, hasta 360–370 g con más nivel y fuerza.</li>
<li><b>Epicondilitis:</b> mejor no pasar de 370 g, con balance bajo y tacto blando.</li>
<li><b>Jóvenes:</b> no más de 330 g; para los más pequeños, mira la <a href="{bimbi}">guía para niños</a>.</li></ul>
<p class="note">Indicaciones de {pw}. El peso corporal y la forma física cuentan tanto como el nivel.</p>
<h2>Cuánto pesan de verdad las palas a la venta</h2>
<p>En nuestra base el peso típico (mediana) de una pala de adulto es de {_g(med_all)} g, calculado sobre {len(pesi)} modelos con peso declarado. Por nivel:</p>
{tab}
<p>La diferencia entre niveles es pequeña: los fabricantes hacen palas de iniciación solo un poco más ligeras que las de avanzado. Por eso, si buscas ligereza, conviene mirar las versiones "Light" o "Lite" de los modelos.</p>
<h2>El balance cuenta tanto como el peso</h2>
<ul><li><b>Bajo</b> (peso hacia el mango): más control y manejabilidad, menos cansancio.</li>
<li><b>Medio:</b> un equilibrio entre control y potencia.</li>
<li><b>Alto</b> (peso hacia la cabeza): más potencia en el remate, pero hace falta un brazo entrenado. Una pala de 360 g con balance alto puede parecer más pesada que una de 370 g con balance bajo.</li></ul>
<h2>Cómo saber si es demasiado pesada</h2>
<p>Si al final del partido el brazo está cansado, llegas tarde a los golpes en la red o aparece una molestia en codo u hombro, baja unos gramos o elige un balance más bajo ({pw}). Lee también las guías de <a href="{epi}">palas para la epicondilitis</a> y de <a href="{don}">palas de mujer</a>.</p>
<h2>Las palas de adulto más ligeras de la base</h2>{_elenco_r(leggere)}{box}''',
              f'''<p><b>Pour la plupart des joueurs adultes, le bon poids se situe entre 350 et 370 grammes. Les débutants, les joueurs qui ont des problèmes au bras et beaucoup de femmes sont bien sous les 360 g ; les attaquants au bras entraîné peuvent monter à 370 g et plus.</b> L'équilibre compte aussi : deux raquettes du même poids peuvent donner des sensations très différentes.</p>
<h2>Le poids conseillé</h2>
<ul><li><b>Débutants :</b> moins de 360 g.</li>
<li><b>Intermédiaires :</b> 360 à 370 g.</li>
<li><b>Avancés et compétiteurs :</b> 370 à 390 g, seulement avec un bras entraîné.</li>
<li><b>Femmes :</b> 330 à 355 g pour le confort et le contrôle, jusqu'à 360–370 g avec plus de niveau et de force.</li>
<li><b>Épicondylite :</b> mieux vaut ne pas dépasser 370 g, avec un équilibre bas et un toucher souple.</li>
<li><b>Jeunes :</b> pas plus de 330 g ; pour les plus petits, voir le <a href="{bimbi}">guide enfants</a>.</li></ul>
<p class="note">Repères de {pw}. Le poids du corps et la condition physique comptent autant que le niveau.</p>
<h2>Combien pèsent vraiment les raquettes en vente</h2>
<p>Dans notre base, le poids type (médiane) d'une raquette adulte est de {_g(med_all)} g, calculé sur {len(pesi)} modèles à poids déclaré. Par niveau :</p>
{tab}
<p>L'écart entre niveaux est faible : les fabricants font des raquettes débutant à peine plus légères que les raquettes avancées. Si vous cherchez de la légèreté, regardez donc les versions « Light » ou « Lite » des modèles.</p>
<h2>L'équilibre compte autant que le poids</h2>
<ul><li><b>Bas</b> (poids vers le manche) : plus de contrôle et de maniabilité, moins de fatigue.</li>
<li><b>Moyen :</b> un compromis entre contrôle et puissance.</li>
<li><b>Haut</b> (poids vers la tête) : plus de puissance au smash, mais il faut un bras entraîné. Une raquette de 360 g à équilibre haut peut sembler plus lourde qu'une raquette de 370 g à équilibre bas.</li></ul>
<h2>Comment savoir si elle est trop lourde</h2>
<p>Si votre bras est fatigué en fin de match, si vous êtes en retard sur les frappes au filet ou si une gêne apparaît au coude ou à l'épaule, descendez de quelques grammes ou choisissez un équilibre plus bas ({pw}). Lisez aussi les guides des <a href="{epi}">raquettes pour l'épicondylite</a> et des <a href="{don}">raquettes pour femmes</a>.</p>
<h2>Les raquettes adultes les plus légères de la base</h2>{_elenco_r(leggere)}{box}''')
    qa = [(L("Quanto deve pesare una racchetta da padel?", "How heavy should a padel racket be?", "¿Cuánto debe pesar una pala de pádel?", "Combien doit peser une raquette de padel ?"),
           L("Per la maggior parte degli adulti tra 350 e 370 g: sotto i 360 g per principianti, chi ha problemi al braccio e molte donne; 370 g e oltre per avanzati con il braccio allenato.",
             "For most adults between 350 and 370 g: under 360 g for beginners, players with arm problems and many women; 370 g and above for advanced players with a trained arm.",
             "Para la mayoría de los adultos entre 350 y 370 g: por debajo de 360 g para principiantes, quien tiene problemas de brazo y muchas mujeres; 370 g o más para avanzados con el brazo entrenado.",
             "Pour la plupart des adultes entre 350 et 370 g : moins de 360 g pour les débutants, les joueurs ayant des problèmes au bras et beaucoup de femmes ; 370 g et plus pour les avancés au bras entraîné.")),
          (L("Una racchetta più pesante dà più potenza?", "Does a heavier racket give more power?", "¿Una pala más pesada da más potencia?", "Une raquette plus lourde donne-t-elle plus de puissance ?"),
           L("Sì, ma solo se riesci a muoverla in fretta. Se ti rallenta, perdi potenza e controllo e affatichi il braccio.",
             "Yes, but only if you can swing it fast. If it slows you down, you lose power and control and tire your arm.",
             "Sí, pero solo si puedes moverla rápido. Si te frena, pierdes potencia y control y cansas el brazo.",
             "Oui, mais seulement si vous la déplacez vite. Si elle vous ralentit, vous perdez puissance et contrôle et fatiguez le bras.")),
          (L("Che peso scegliere con l'epicondilite?", "What weight should I choose with tennis elbow?", "¿Qué peso elegir con epicondilitis?", "Quel poids choisir avec une épicondylite ?"),
           L("Meglio non superare i 370 g, con bilanciamento basso e tocco morbido.", "Best not to go over 370 g, with a low balance and soft feel.",
             "Mejor no pasar de 370 g, con balance bajo y tacto blando.", "Mieux vaut ne pas dépasser 370 g, avec un équilibre bas et un toucher souple."))]
    titolo = L("Quanto deve pesare la racchetta da padel: il peso giusto per te", "How heavy should your padel racket be: the right weight for you",
               "Cuánto debe pesar la pala de pádel: el peso adecuado para ti", "Combien doit peser votre raquette de padel : le bon poids pour vous")
    return _pubblica5("peso", titolo,
                      L("Il peso giusto della racchetta da padel per livello, sesso e problemi al braccio, con i pesi reali delle racchette in vendita e il ruolo del bilanciamento.",
                        "The right padel racket weight by level, gender and arm problems, with the real weights of rackets on sale and the role of balance.",
                        "El peso adecuado de la pala de pádel según nivel, sexo y problemas de brazo, con los pesos reales de las palas a la venta y el papel del balance.",
                        "Le bon poids de raquette de padel selon le niveau, le sexe et les problèmes au bras, avec les poids réels des raquettes en vente et le rôle de l'équilibre."),
                      L("Peso della racchetta", "Racket weight", "Peso de la pala", "Poids de la raquette"), corpo, qa,
                      L("Il peso giusto per livello e i pesi reali delle racchette in vendita.", "The right weight by level and the real weights of rackets on sale.",
                        "El peso adecuado por nivel y los pesos reales de las palas a la venta.", "Le bon poids par niveau et les poids réels des raquettes en vente."), items=leggere)


def art_over50(db):
    ad = [r for r in db if r["categoria"] != "junior"]
    cand = [(r, _pmid(r["peso"])) for r in ad if r.get("forma") in ("rotonda", "goccia") and r.get("livello") in ("principiante", "principiante-intermedio", "intermedio")]
    scelte = [r for r, w in sorted(cand, key=lambda x: (x[1] or 999)) if w and w <= 355][:8]
    ca, sa = _f5("castillo"), _f5("sadok")
    epi, peso, forme, reg = P("guide", "racchetta-padel-epicondilite"), P("articoli", G5["peso"][0]), P("guide", "forme-racchetta-padel"), P("articoli", "regolamento-padel-regole-spiegate")
    scarpe = P("articoli", G5["scarpe"][0])
    box = _box5(L("Trova la racchetta giusta per te", "Find the right racket for you", "Encuentra la pala adecuada para ti", "Trouvez la bonne raquette"),
                L("Nel quiz puoi indicare problemi a gomito o spalla: ti proponiamo modelli leggeri e dal tocco morbido.", "In the quiz you can mention elbow or shoulder problems: we'll suggest light, soft-feeling models.", "En el test puedes indicar problemas de codo u hombro: te proponemos modelos ligeros y de tacto blando.", "Dans le quiz, vous pouvez signaler des problèmes de coude ou d'épaule : nous vous proposons des modèles légers au toucher souple."),
                L("Trova la tua racchetta", "Find your racket", "Encuentra tu pala", "Trouve ta raquette"), P("selettore"))
    corpo = L(f'''<p><b>Il padel è uno degli sport più adatti a chi ha superato i 50 anni: si gioca in quattro, il campo è piccolo, la palla rallenta sulle pareti e gli scambi si costruiscono più con la testa che con la forza. Per giocare a lungo senza farsi male contano tre cose: una racchetta leggera e morbida, le scarpe giuste e un buon riscaldamento.</b></p>
<h2>Gli infortuni più frequenti dopo i 50 anni</h2>
<p>Uno studio spagnolo su 131 giocatori tra 50 e 66 anni (età media 57) ha rilevato i problemi più comuni: gomito nel 29,8% dei giocatori, zona lombare nel 27,5%, ginocchio nel 22,9%, polpaccio ("tennis leg") nel 22,1% e spalla nel 20,6% ({ca}). Agli arti superiori prevalgono i problemi da sovraccarico, come l'epicondilite; alle gambe quelli acuti, come le distorsioni.</p>
<p>Una revisione del 2026 indica come strategie di prevenzione un riscaldamento adeguato, un aumento graduale del carico, esercizi di stabilità e propriocezione e un'attrezzatura adatta ({sa}).</p>
<h2>La racchetta giusta</h2>
<ul><li><b>Leggera:</b> 340–355 g è un buon punto di partenza; leggi la guida sul <a href="{peso}">peso della racchetta</a>.</li>
<li><b>Rotonda o a goccia:</b> perdonano di più i colpi decentrati e richiedono meno forza (vedi <a href="{forme}">le forme</a>).</li>
<li><b>Bilanciamento basso e gomma morbida:</b> meno vibrazioni su gomito e spalla. Se hai già avuto l'epicondilite, leggi la <a href="{epi}">guida dedicata</a>.</li>
<li><b>Niente racchette "da pro":</b> diamanti rigide e pesanti mettono sotto sforzo il braccio senza dare vantaggi a chi non colpisce fortissimo.</li></ul>
<h2>Racchette leggere e tolleranti dal nostro database</h2>{_elenco_r(scelte)}
<h2>Consigli per giocare senza farsi male</h2>
<ul><li><b>Riscaldati 10 minuti</b> prima di entrare in campo: spalle, polsi, polpacci e qualche spostamento laterale.</li>
<li><b>Aumenta gradualmente:</b> meglio due partite a settimana con continuità che tante partite in pochi giorni.</li>
<li><b>Scarpe da padel, non da corsa:</b> servono suola adatta al campo e sostegno laterale (vedi la <a href="{scarpe}">guida alle scarpe</a>).</li>
<li><b>Lascia lavorare le pareti:</b> nel padel non serve correre su ogni palla, spesso basta aspettarla dopo il rimbalzo sul vetro.</li>
<li><b>Ascolta i segnali:</b> un fastidio al gomito o al polpaccio che torna a ogni partita va fatto vedere a un medico o a un fisioterapista.</li></ul>
<p>Se sei agli inizi, parti dalle <a href="{reg}">regole spiegate semplici</a>.</p>{box}
<p class="note">Fonti: {ca}; {sa}. Questo articolo non sostituisce il parere di un medico.</p>''',
              f'''<p><b>Padel is one of the best sports for people over 50: it's played in fours, the court is small, the ball slows down off the walls and rallies are built more with your head than with strength. To keep playing for years without getting hurt, three things matter: a light, soft racket, the right shoes and a proper warm-up.</b></p>
<h2>The most common injuries after 50</h2>
<p>A Spanish study of 131 players aged 50 to 66 (average age 57) recorded the most common problems: elbow in 29.8% of players, lower back in 27.5%, knee in 22.9%, calf ("tennis leg") in 22.1% and shoulder in 20.6% ({ca}). In the upper limbs overuse problems such as tennis elbow prevail; in the legs, acute ones such as sprains.</p>
<p>A 2026 review lists as prevention strategies a proper warm-up, a gradual increase in load, stability and proprioception exercises and suitable equipment ({sa}).</p>
<h2>The right racket</h2>
<ul><li><b>Light:</b> 340–355 g is a good starting point; read the guide to <a href="{peso}">racket weight</a>.</li>
<li><b>Round or teardrop:</b> more forgiving on off-centre hits and less demanding on strength (see <a href="{forme}">shapes</a>).</li>
<li><b>Low balance and soft core:</b> less vibration on elbow and shoulder. If you've already had tennis elbow, read the <a href="{epi}">dedicated guide</a>.</li>
<li><b>No "pro" rackets:</b> stiff, heavy diamonds strain the arm without any benefit if you don't hit very hard.</li></ul>
<h2>Light, forgiving rackets from our database</h2>{_elenco_r(scelte)}
<h2>Tips for playing without getting hurt</h2>
<ul><li><b>Warm up for 10 minutes</b> before going on court: shoulders, wrists, calves and some side-to-side movement.</li>
<li><b>Build up gradually:</b> two matches a week consistently is better than many matches in a few days.</li>
<li><b>Padel shoes, not running shoes:</b> you need a sole suited to the court and lateral support (see the <a href="{scarpe}">shoe guide</a>).</li>
<li><b>Let the walls do the work:</b> in padel you don't need to chase every ball; often you can wait for it after it bounces off the glass.</li>
<li><b>Listen to your body:</b> elbow or calf discomfort that comes back every match should be seen by a doctor or physiotherapist.</li></ul>
<p>If you're just starting out, begin with the <a href="{reg}">rules explained simply</a>.</p>{box}
<p class="note">Sources: {ca}; {sa}. This article is not a substitute for medical advice.</p>''',
              f'''<p><b>El pádel es uno de los deportes más adecuados para quien ha pasado de los 50: se juega de cuatro en cuatro, la pista es pequeña, la bola se frena en las paredes y los puntos se construyen más con la cabeza que con la fuerza. Para jugar muchos años sin lesionarse cuentan tres cosas: una pala ligera y blanda, las zapatillas adecuadas y un buen calentamiento.</b></p>
<h2>Las lesiones más frecuentes a partir de los 50</h2>
<p>Un estudio español con 131 jugadores de entre 50 y 66 años (edad media 57) registró los problemas más comunes: codo en el 29,8% de los jugadores, zona lumbar en el 27,5%, rodilla en el 22,9%, gemelo ("pierna de tenista") en el 22,1% y hombro en el 20,6% ({ca}). En las extremidades superiores predominan las lesiones por sobrecarga, como la epicondilitis; en las piernas, las agudas, como los esguinces.</p>
<p>Una revisión de 2026 señala como estrategias de prevención un calentamiento adecuado, un aumento progresivo de la carga, ejercicios de estabilidad y propiocepción y un material adecuado ({sa}).</p>
<h2>La pala adecuada</h2>
<ul><li><b>Ligera:</b> 340–355 g es un buen punto de partida; lee la guía sobre el <a href="{peso}">peso de la pala</a>.</li>
<li><b>Redonda o lágrima:</b> perdonan más los golpes descentrados y exigen menos fuerza (ver <a href="{forme}">las formas</a>).</li>
<li><b>Balance bajo y goma blanda:</b> menos vibraciones en codo y hombro. Si ya has tenido epicondilitis, lee la <a href="{epi}">guía específica</a>.</li>
<li><b>Nada de palas "de pro":</b> los diamantes rígidos y pesados cargan el brazo sin aportar ventajas si no golpeas muy fuerte.</li></ul>
<h2>Palas ligeras y tolerantes de nuestra base</h2>{_elenco_r(scelte)}
<h2>Consejos para jugar sin lesionarse</h2>
<ul><li><b>Calienta 10 minutos</b> antes de entrar en pista: hombros, muñecas, gemelos y algunos desplazamientos laterales.</li>
<li><b>Aumenta poco a poco:</b> mejor dos partidos a la semana con regularidad que muchos partidos en pocos días.</li>
<li><b>Zapatillas de pádel, no de running:</b> hace falta una suela adecuada a la pista y sujeción lateral (ver la <a href="{scarpe}">guía de zapatillas</a>).</li>
<li><b>Deja trabajar a las paredes:</b> en pádel no hace falta correr a por todas las bolas; a menudo basta esperarla tras el rebote en el cristal.</li>
<li><b>Escucha las señales:</b> una molestia en el codo o el gemelo que vuelve en cada partido debe verla un médico o un fisioterapeuta.</li></ul>
<p>Si estás empezando, arranca por las <a href="{reg}">reglas explicadas fácil</a>.</p>{box}
<p class="note">Fuentes: {ca}; {sa}. Este artículo no sustituye la opinión de un médico.</p>''',
              f'''<p><b>Le padel est l'un des sports les plus adaptés après 50 ans : on joue à quatre, le terrain est petit, la balle ralentit sur les vitres et les échanges se construisent plus avec la tête qu'avec la force. Pour jouer longtemps sans se blesser, trois choses comptent : une raquette légère et souple, les bonnes chaussures et un bon échauffement.</b></p>
<h2>Les blessures les plus fréquentes après 50 ans</h2>
<p>Une étude espagnole sur 131 joueurs de 50 à 66 ans (âge moyen 57 ans) a relevé les problèmes les plus courants : coude chez 29,8 % des joueurs, bas du dos chez 27,5 %, genou chez 22,9 %, mollet (« tennis leg ») chez 22,1 % et épaule chez 20,6 % ({ca}). Aux membres supérieurs dominent les problèmes de surmenage comme l'épicondylite ; aux jambes, les blessures aiguës comme les entorses.</p>
<p>Une revue de 2026 cite comme stratégies de prévention un échauffement adapté, une augmentation progressive de la charge, des exercices de stabilité et de proprioception et un équipement adapté ({sa}).</p>
<h2>La bonne raquette</h2>
<ul><li><b>Légère :</b> 340 à 355 g est un bon point de départ ; lisez le guide sur le <a href="{peso}">poids de la raquette</a>.</li>
<li><b>Ronde ou goutte d'eau :</b> elles pardonnent davantage les frappes décentrées et demandent moins de force (voir <a href="{forme}">les formes</a>).</li>
<li><b>Équilibre bas et gomme souple :</b> moins de vibrations pour le coude et l'épaule. Si vous avez déjà eu une épicondylite, lisez le <a href="{epi}">guide dédié</a>.</li>
<li><b>Pas de raquettes « de pro » :</b> les diamants rigides et lourds sollicitent le bras sans avantage si vous ne frappez pas très fort.</li></ul>
<h2>Raquettes légères et tolérantes de notre base</h2>{_elenco_r(scelte)}
<h2>Conseils pour jouer sans se blesser</h2>
<ul><li><b>Échauffez-vous 10 minutes</b> avant d'entrer sur le terrain : épaules, poignets, mollets et quelques déplacements latéraux.</li>
<li><b>Progressez en douceur :</b> mieux vaut deux matchs par semaine avec régularité que beaucoup de matchs en peu de jours.</li>
<li><b>Des chaussures de padel, pas de running :</b> il faut une semelle adaptée au terrain et un bon maintien latéral (voir le <a href="{scarpe}">guide des chaussures</a>).</li>
<li><b>Laissez travailler les vitres :</b> au padel, inutile de courir sur chaque balle ; souvent, il suffit de l'attendre après le rebond sur la vitre.</li>
<li><b>Écoutez les signaux :</b> une gêne au coude ou au mollet qui revient à chaque match doit être montrée à un médecin ou à un kinésithérapeute.</li></ul>
<p>Si vous débutez, commencez par les <a href="{reg}">règles expliquées simplement</a>.</p>{box}
<p class="note">Sources : {ca} ; {sa}. Cet article ne remplace pas l'avis d'un médecin.</p>''')
    qa = [(L("Si può iniziare a giocare a padel dopo i 50 anni?", "Can you start playing padel after 50?", "¿Se puede empezar a jugar al pádel después de los 50?", "Peut-on commencer le padel après 50 ans ?"),
           L("Sì: si gioca in quattro, il campo è piccolo e gli scambi richiedono più tecnica che forza. Conviene partire con una racchetta leggera e aumentare il carico poco a poco.",
             "Yes: it's played in fours, the court is small and rallies need more technique than strength. Start with a light racket and build up gradually.",
             "Sí: se juega de cuatro en cuatro, la pista es pequeña y los puntos exigen más técnica que fuerza. Conviene empezar con una pala ligera e ir aumentando poco a poco.",
             "Oui : on joue à quatre, le terrain est petit et les échanges demandent plus de technique que de force. Mieux vaut commencer avec une raquette légère et progresser petit à petit.")),
          (L("Qual è l'infortunio più comune nei giocatori over 50?", "What's the most common injury in players over 50?", "¿Cuál es la lesión más común en jugadores mayores de 50?", "Quelle est la blessure la plus fréquente chez les joueurs de plus de 50 ans ?"),
           L("In uno studio su 131 giocatori tra 50 e 66 anni, il gomito (29,8%), seguito da zona lombare, ginocchio, polpaccio e spalla.",
             "In a study of 131 players aged 50 to 66, the elbow (29.8%), followed by lower back, knee, calf and shoulder.",
             "En un estudio con 131 jugadores de 50 a 66 años, el codo (29,8%), seguido de zona lumbar, rodilla, gemelo y hombro.",
             "Dans une étude sur 131 joueurs de 50 à 66 ans, le coude (29,8 %), suivi du bas du dos, du genou, du mollet et de l'épaule.")),
          (L("Che racchetta usare dopo i 50 anni?", "Which racket should I use after 50?", "¿Qué pala usar después de los 50?", "Quelle raquette utiliser après 50 ans ?"),
           L("Leggera (340–355 g), rotonda o a goccia, con bilanciamento basso e gomma morbida.", "Light (340–355 g), round or teardrop, with a low balance and soft core.",
             "Ligera (340–355 g), redonda o de lágrima, con balance bajo y goma blanda.", "Légère (340 à 355 g), ronde ou goutte d'eau, avec un équilibre bas et une gomme souple."))]
    titolo = L("Padel dopo i 50 anni: racchetta, scarpe e consigli per non farsi male", "Padel after 50: racket, shoes and tips to avoid injury",
               "Pádel a partir de los 50: pala, zapatillas y consejos para no lesionarse", "Le padel après 50 ans : raquette, chaussures et conseils pour ne pas se blesser")
    return _pubblica5("over50", titolo,
                      L("Come giocare a padel dopo i 50 anni: gli infortuni più frequenti secondo gli studi, la racchetta giusta e i consigli per prevenirli.",
                        "How to play padel after 50: the most common injuries according to studies, the right racket and tips to prevent them.",
                        "Cómo jugar al pádel a partir de los 50: las lesiones más frecuentes según los estudios, la pala adecuada y consejos para prevenirlas.",
                        "Comment jouer au padel après 50 ans : les blessures les plus fréquentes selon les études, la bonne raquette et des conseils pour les prévenir."),
                      L("Padel over 50", "Padel over 50", "Pádel mayores de 50", "Padel après 50 ans"), corpo, qa,
                      L("Infortuni più comuni, racchetta giusta e consigli pratici.", "Most common injuries, the right racket and practical tips.",
                        "Lesiones más comunes, la pala adecuada y consejos prácticos.", "Blessures les plus fréquentes, la bonne raquette et conseils pratiques."), items=scelte)


def art_scarpe(db):
    sh = _f5("shop")
    o50, reg = P("articoli", G5["over50"][0]), P("articoli", "regolamento-padel-regole-spiegate")
    tab = ('<div class="tablebox"><table class="tab"><thead><tr><th>' + L("Suola", "Sole", "Suela", "Semelle") + '</th><th>' + L("Campo ideale", "Best court", "Pista ideal", "Terrain idéal") + '</th><th>'
           + L("Pro", "Pros", "Ventajas", "Atouts") + '</th><th>' + L("Contro", "Cons", "Inconvenientes", "Limites") + '</th></tr></thead><tbody>'
           + "".join(f"<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in [
               (L("Spina di pesce (herringbone, clay)", "Herringbone (clay)", "Espiga (clay)", "Chevrons (clay)"),
                L("Erba sintetica con sabbia, terra", "Sand-filled artificial grass, clay", "Césped artificial con arena, tierra", "Gazon synthétique sablé, terre battue"),
                L("Ottima presa sulla sabbia, buon sostegno laterale, durevole", "Great grip on sand, good lateral support, durable", "Gran agarre en arena, buena sujeción lateral, duradera", "Excellente adhérence sur le sable, bon maintien latéral, durable"),
                L("Troppa presa sui campi duri", "Too grippy on hard courts", "Demasiado agarre en pistas duras", "Trop d'adhérence sur terrain dur")),
               (L("Omni (puntini)", "Omni (studs)", "Omni (tacos)", "Omni (picots)"),
                L("Campi con poca sabbia, indoor, cemento", "Courts with little sand, indoor, hard", "Pistas con poca arena, indoor, cemento", "Terrains peu sablés, indoor, dur"),
                L("Movimenti rapidi in tutte le direzioni", "Quick movement in every direction", "Movimientos rápidos en todas las direcciones", "Déplacements rapides dans toutes les directions"),
                L("Meno presa sulla sabbia, si consuma prima", "Less grip on sand, wears out faster", "Menos agarre en arena, se desgasta antes", "Moins d'adhérence sur le sable, s'use plus vite")),
               (L("Ibrida", "Hybrid", "Híbrida", "Hybride"),
                L("Chi gioca su campi diversi", "Players who use different courts", "Quien juega en pistas distintas", "Ceux qui jouent sur des terrains différents"),
                L("Equilibrio tra presa e mobilità", "Balance of grip and mobility", "Equilibrio entre agarre y movilidad", "Équilibre entre adhérence et mobilité"),
                L("Meno presa della spina di pesce sui campi molto sabbiosi", "Less grip than herringbone on very sandy courts", "Menos agarre que la espiga en pistas muy arenosas", "Moins d'adhérence que les chevrons sur terrain très sablé"))])
           + "</tbody></table></div>")
    corpo = L(f'''<p><b>Per giocare a padel servono scarpe da padel, non da corsa: la suola deve fare presa sulla sabbia del campo e la tomaia deve sostenere il piede negli spostamenti laterali. La scelta più importante è il tipo di suola, che dipende dal campo su cui giochi.</b></p>
<h2>I tre tipi di suola</h2>{tab}
<p class="note">Fonte: {sh}.</p>
<h2>Quale scegliere in Italia</h2>
<p>La maggior parte dei campi da padel in Italia è in erba sintetica con sabbia: per questi la suola a <b>spina di pesce</b> è la scelta più sicura. Se giochi spesso indoor o su campi con poca sabbia, valuta una <b>omni</b>; se cambi spesso circolo, una <b>ibrida</b> è il compromesso più comodo.</p>
<h2>Perché non usare scarpe da corsa</h2>
<ul><li><b>Poco sostegno laterale:</b> sono fatte per correre in avanti, non per frenare e cambiare direzione di lato. Il rischio di distorsioni alla caviglia aumenta.</li>
<li><b>Suola sbagliata:</b> sulla sabbia scivola troppo, e la suola morbida si consuma in fretta sull'erba sintetica.</li>
<li><b>Ammortizzazione alta e instabile:</b> va bene nella corsa, ma negli scatti brevi rende il piede meno stabile.</li></ul>
<h2>Cosa guardare oltre alla suola</h2>
<ul><li><b>Sostegno laterale e tallone stabile:</b> il piede non deve "uscire" dalla scarpa nei cambi di direzione.</li>
<li><b>Ammortizzazione nel tallone:</b> utile per chi gioca spesso o ha qualche anno in più (vedi <a href="{o50}">padel dopo i 50 anni</a>).</li>
<li><b>Punta rinforzata:</b> nel padel si striscia spesso la punta, soprattutto chi gioca a destra.</li>
<li><b>Misura:</b> provala con le calze da gioco; tra la punta del piede e la scarpa ci vuole circa un dito.</li></ul>
<h2>Quando cambiarle</h2>
<p>Quando il disegno della suola è consumato nella zona dell'avampiede, la presa cala molto e aumenta il rischio di scivolare: a quel punto conviene cambiarle, anche se la tomaia sembra ancora buona.</p>
<p>Se sei agli inizi, leggi anche le <a href="{reg}">regole del padel spiegate semplici</a>.</p>
<p class="note">Fonte sulle suole: {sh}. Gli altri consigli sono indicazioni generali di PadelMetrix.</p>''',
              f'''<p><b>To play padel you need padel shoes, not running shoes: the sole must grip the sand on the court and the upper must support your foot when you move sideways. The most important choice is the type of sole, which depends on the court you play on.</b></p>
<h2>The three types of sole</h2>{tab}
<p class="note">Source: {sh}.</p>
<h2>Which to choose</h2>
<p>Most padel courts are sand-filled artificial grass: for these a <b>herringbone</b> sole is the safest choice. If you often play indoors or on courts with little sand, consider an <b>omni</b> sole; if you switch clubs a lot, a <b>hybrid</b> is the most convenient compromise.</p>
<h2>Why not to use running shoes</h2>
<ul><li><b>Little lateral support:</b> they're made for running forwards, not for braking and changing direction sideways. The risk of ankle sprains goes up.</li>
<li><b>Wrong sole:</b> it slips too much on sand, and a soft sole wears out fast on artificial grass.</li>
<li><b>High, unstable cushioning:</b> fine for running, but on short bursts it makes the foot less stable.</li></ul>
<h2>What to look at besides the sole</h2>
<ul><li><b>Lateral support and a stable heel:</b> your foot shouldn't "roll out" of the shoe when you change direction.</li>
<li><b>Heel cushioning:</b> useful for frequent players or those a little older (see <a href="{o50}">padel after 50</a>).</li>
<li><b>Reinforced toe:</b> in padel you often drag the toe, especially if you play on the right.</li>
<li><b>Size:</b> try them with your playing socks; leave about a finger's width between your toes and the end of the shoe.</li></ul>
<h2>When to replace them</h2>
<p>When the tread pattern is worn under the forefoot, grip drops a lot and the risk of slipping goes up: that's the time to replace them, even if the upper still looks fine.</p>
<p>If you're just starting out, read the <a href="{reg}">padel rules explained simply</a> too.</p>
<p class="note">Source on soles: {sh}. The other tips are general PadelMetrix guidance.</p>''',
              f'''<p><b>Para jugar al pádel hacen falta zapatillas de pádel, no de running: la suela tiene que agarrar en la arena de la pista y el empeine tiene que sujetar el pie en los desplazamientos laterales. La elección más importante es el tipo de suela, que depende de la pista en la que juegues.</b></p>
<h2>Los tres tipos de suela</h2>{tab}
<p class="note">Fuente: {sh}.</p>
<h2>Cuál elegir</h2>
<p>La mayoría de las pistas de pádel son de césped artificial con arena: para estas, la suela de <b>espiga</b> es la opción más segura. Si juegas a menudo en indoor o en pistas con poca arena, valora una <b>omni</b>; si cambias mucho de club, una <b>híbrida</b> es el compromiso más cómodo.</p>
<h2>Por qué no usar zapatillas de running</h2>
<ul><li><b>Poca sujeción lateral:</b> están hechas para correr hacia delante, no para frenar y cambiar de dirección de lado. Aumenta el riesgo de esguince de tobillo.</li>
<li><b>Suela equivocada:</b> en la arena resbala demasiado y la suela blanda se desgasta rápido en el césped artificial.</li>
<li><b>Amortiguación alta e inestable:</b> va bien para correr, pero en los arranques cortos hace el pie menos estable.</li></ul>
<h2>Qué mirar además de la suela</h2>
<ul><li><b>Sujeción lateral y talón estable:</b> el pie no debe "salirse" de la zapatilla en los cambios de dirección.</li>
<li><b>Amortiguación en el talón:</b> útil para quien juega a menudo o tiene algunos años más (ver <a href="{o50}">pádel a partir de los 50</a>).</li>
<li><b>Puntera reforzada:</b> en pádel se arrastra a menudo la puntera, sobre todo quien juega en el lado derecho.</li>
<li><b>Talla:</b> pruébatelas con los calcetines de juego; entre los dedos y la punta debe quedar más o menos un dedo.</li></ul>
<h2>Cuándo cambiarlas</h2>
<p>Cuando el dibujo de la suela está gastado en la zona del antepié, el agarre baja mucho y aumenta el riesgo de resbalar: en ese momento conviene cambiarlas, aunque el empeine parezca todavía bueno.</p>
<p>Si estás empezando, lee también las <a href="{reg}">reglas del pádel explicadas fácil</a>.</p>
<p class="note">Fuente sobre las suelas: {sh}. Los demás consejos son indicaciones generales de PadelMetrix.</p>''',
              f'''<p><b>Pour jouer au padel, il faut des chaussures de padel, pas de running : la semelle doit accrocher sur le sable du terrain et la tige doit maintenir le pied dans les déplacements latéraux. Le choix le plus important est le type de semelle, qui dépend du terrain sur lequel vous jouez.</b></p>
<h2>Les trois types de semelle</h2>{tab}
<p class="note">Source : {sh}.</p>
<h2>Laquelle choisir</h2>
<p>La plupart des terrains de padel sont en gazon synthétique sablé : pour ceux-ci, la semelle à <b>chevrons</b> est le choix le plus sûr. Si vous jouez souvent en salle ou sur des terrains peu sablés, pensez à une <b>omni</b> ; si vous changez souvent de club, une <b>hybride</b> est le compromis le plus pratique.</p>
<h2>Pourquoi ne pas jouer en chaussures de running</h2>
<ul><li><b>Peu de maintien latéral :</b> elles sont faites pour courir vers l'avant, pas pour freiner et changer de direction sur le côté. Le risque d'entorse de la cheville augmente.</li>
<li><b>Mauvaise semelle :</b> elle glisse trop sur le sable, et une semelle souple s'use vite sur le gazon synthétique.</li>
<li><b>Amorti haut et instable :</b> parfait pour courir, mais sur les démarrages courts il rend le pied moins stable.</li></ul>
<h2>Ce qu'il faut regarder en plus de la semelle</h2>
<ul><li><b>Maintien latéral et talon stable :</b> le pied ne doit pas « sortir » de la chaussure dans les changements de direction.</li>
<li><b>Amorti au talon :</b> utile si vous jouez souvent ou si vous avez quelques années de plus (voir <a href="{o50}">le padel après 50 ans</a>).</li>
<li><b>Bout renforcé :</b> au padel, on traîne souvent la pointe du pied, surtout à droite.</li>
<li><b>Pointure :</b> essayez-les avec vos chaussettes de jeu ; il faut environ un doigt entre les orteils et le bout de la chaussure.</li></ul>
<h2>Quand les changer</h2>
<p>Quand les reliefs de la semelle sont usés sous l'avant-pied, l'adhérence baisse beaucoup et le risque de glisser augmente : c'est le moment de les changer, même si la tige semble encore en bon état.</p>
<p>Si vous débutez, lisez aussi les <a href="{reg}">règles du padel expliquées simplement</a>.</p>
<p class="note">Source sur les semelles : {sh}. Les autres conseils sont des repères généraux de PadelMetrix.</p>''')
    qa = [(L("Si può giocare a padel con le scarpe da corsa?", "Can you play padel in running shoes?", "¿Se puede jugar al pádel con zapatillas de running?", "Peut-on jouer au padel en chaussures de running ?"),
           L("È sconsigliato: hanno poco sostegno laterale e una suola che scivola sulla sabbia, quindi aumentano il rischio di distorsioni.",
             "It's not recommended: they have little lateral support and a sole that slips on sand, which raises the risk of sprains.",
             "No es recomendable: tienen poca sujeción lateral y una suela que resbala en la arena, por lo que aumentan el riesgo de esguinces.",
             "C'est déconseillé : elles offrent peu de maintien latéral et une semelle qui glisse sur le sable, ce qui augmente le risque d'entorse.")),
          (L("Che suola serve per i campi in erba sintetica?", "Which sole is best for artificial grass courts?", "¿Qué suela hace falta para pistas de césped artificial?", "Quelle semelle pour les terrains en gazon synthétique ?"),
           L("Sui campi in erba sintetica con sabbia la più indicata è la suola a spina di pesce (herringbone).", "On sand-filled artificial grass the best choice is a herringbone sole.",
             "En pistas de césped artificial con arena, la más indicada es la suela de espiga (herringbone).", "Sur gazon synthétique sablé, la plus indiquée est la semelle à chevrons (herringbone).")),
          (L("Quando vanno cambiate le scarpe da padel?", "When should padel shoes be replaced?", "¿Cuándo hay que cambiar las zapatillas de pádel?", "Quand faut-il changer ses chaussures de padel ?"),
           L("Quando il disegno della suola è consumato sotto l'avampiede: la presa cala e si rischia di scivolare.", "When the tread is worn under the forefoot: grip drops and you risk slipping.",
             "Cuando el dibujo de la suela está gastado bajo el antepié: el agarre baja y se corre el riesgo de resbalar.", "Quand les reliefs de la semelle sont usés sous l'avant-pied : l'adhérence baisse et on risque de glisser."))]
    titolo = L("Scarpe da padel: come sceglierle (suola, campo e misura)", "Padel shoes: how to choose them (sole, court and fit)",
               "Zapatillas de pádel: cómo elegirlas (suela, pista y talla)", "Chaussures de padel : comment les choisir (semelle, terrain et pointure)")
    return _pubblica5("scarpe", titolo,
                      L("Come scegliere le scarpe da padel: suola a spina di pesce, omni o ibrida in base al campo, perché non usare scarpe da corsa e quando cambiarle.",
                        "How to choose padel shoes: herringbone, omni or hybrid sole by court type, why not to use running shoes and when to replace them.",
                        "Cómo elegir zapatillas de pádel: suela de espiga, omni o híbrida según la pista, por qué no usar zapatillas de running y cuándo cambiarlas.",
                        "Comment choisir ses chaussures de padel : semelle à chevrons, omni ou hybride selon le terrain, pourquoi éviter les chaussures de running et quand les changer."),
                      L("Scarpe da padel", "Padel shoes", "Zapatillas de pádel", "Chaussures de padel"), corpo, qa,
                      L("Spina di pesce, omni o ibrida: la suola giusta per il tuo campo.", "Herringbone, omni or hybrid: the right sole for your court.",
                        "Espiga, omni o híbrida: la suela adecuada para tu pista.", "Chevrons, omni ou hybride : la bonne semelle pour votre terrain."))


# ---------------------------------------------------------------- QUAD, la marca portoghese (novembre 2026)
QUAD_SLUG = "quad-racchette-padel-portoghesi-modelli"
S.SLUG[QUAD_SLUG] = ("quad-portuguese-padel-rackets-models", "quad-palas-padel-portuguesas-modelos")
S.SLUG_FR[QUAD_SLUG] = "quad-raquettes-padel-portugaises-modeles"
DATE_ART[QUAD_SLUG] = "2026-11-07"
QUAD_U = "https://www.quad-sports.com/"


def art_quad(db):
    qs = [r for r in db if r["marca"] == "QUAD"]
    RACCHETTE_ARTICOLO[QUAD_SLUG] = [r["slug"] for r in qs]
    by = {r["slug"]: r for r in qs}
    ad = [r["prezzo"] for r in db if r.get("prezzo") and r["categoria"] != "junior"]
    med = sorted(ad)[len(ad) // 2]
    base = ["quad-shark-2026", "quad-naja-2026", "quad-rhino-2024", "quad-tiger-2026", "quad-fox-2026", "quad-leopard-2026", "quad-wolf-2026", "quad-t-rex-junior-2026"]
    spec = ["quad-fpf-edition-2026", "quad-dragon-ii-fc-porto-edition-2026", "quad-euro-padel-cup-edition-2026", "quad-chinese-new-year-edition-2026", "quad-garuda-2025", "quad-garuda-ii-2026",
            "quad-siza-vieira-2024", "quad-diogo-dalot-2026", "quad-muklay-2026", "quad-guel-do-it-2026"]
    nd = L("n.d.", "n/a", "n.d.", "n.c.")

    def carb(r):
        m = _re.search(r"(\d+)K(?:, (\d) strati)?", r.get("superficie") or "")
        return (m.group(1) + "K" + (f" ×{m.group(2)}" if m.group(2) else "")) if m else nd

    def riga(s):
        r = by[s]
        return (f'<tr><td><a href="{url_r(r)}">{e(r["modello"])}</a></td><td>{FORMA(r["forma"]) if r.get("forma") else nd}</td>'
                f'<td>{e(S.tr(r["peso"])) if r.get("peso") else nd}</td><td>{carb(r)}</td><td>{euro(r["prezzo"])}</td></tr>')

    th = ("<thead><tr><th>" + L("Modello", "Model", "Modelo", "Modèle") + "</th><th>" + L("Forma", "Shape", "Forma", "Forme") + "</th><th>" + L("Peso", "Weight", "Peso", "Poids")
          + "</th><th>" + L("Carbonio (strati)", "Carbon (layers)", "Carbono (capas)", "Carbone (couches)") + "</th><th>" + L("Listino", "List price", "Precio", "Prix") + "</th></tr></thead>")
    tab_b = f'<div class="tablebox"><table class="tab">{th}<tbody>{"".join(riga(s) for s in base if s in by)}</tbody></table></div>'
    tab_s = f'<div class="tablebox"><table class="tab">{th}<tbody>{"".join(riga(s) for s in spec if s in by)}</tbody></table></div>'
    qf, qe = fonte(QUAD_U + "collections/padel-rackets", "QUAD"), fonte(QUAD_U + "collections/special-editions", "QUAD")
    eb = fonte("https://echoboomer.pt/marca-portuguesa-quad-abre-loja-padel-norteshopping/", "Echo Boomer")
    pa = fonte("https://www.padeladdict.com/quad-padel-es-la-nueva-marca-de-tito-allemandi/", "Padel Addict")
    fb = fonte("https://www.forbespt.com/popularidade-do-padel-coloca-empresa-portuguesa-em-alta-voltagem", "Forbes Portugal")
    mk = P("marche", "quad")
    u = lambda s: url_r(by[s])
    box = _box5(L("Tutte le schede QUAD", "All QUAD racket pages", "Todas las fichas QUAD", "Toutes les fiches QUAD"),
                L(f"{len(qs)} racchette con dati tecnici, fonti e alternative simili di altri marchi.", f"{len(qs)} rackets with specs, sources and similar alternatives from other brands.",
                  f"{len(qs)} palas con datos técnicos, fuentes y alternativas similares de otras marcas.", f"{len(qs)} raquettes avec données techniques, sources et alternatives d'autres marques."),
                L("Vai alla pagina QUAD", "Go to the QUAD page", "Ir a la página QUAD", "Voir la page QUAD"), mk)
    corpo = L(f'''<p><b>QUAD è un piccolo marchio portoghese che produce le sue racchette in carbonio in una fabbrica propria in Portogallo. In Italia è un marchio di nicchia: non si trova nei grandi negozi di padel, ma si compra dal sito ufficiale. La gamma ha 7 modelli base tra 190 e 390 euro, più una serie di edizioni limitate e d'autore che arrivano a 1.900 euro.</b></p>
<h2>Chi è QUAD</h2>
<p>QUAD vende racchette da padel, articoli da pickleball e abbigliamento sportivo. La sua caratteristica principale è la produzione: le racchette nascono nella QUAD Factory, che il marchio presenta come l'unica fabbrica del suo genere in Portogallo ({eb}). Non è scontato: un'altra marca portoghese, Volt, ha dichiarato a Forbes di progettare in casa e produrre in Asia ({fb}).</p>
<p>Sul sito si può creare una racchetta da zero o cambiare i colori di un modello esistente; QUAD ha aperto il primo negozio monomarca al NorteShopping di Matosinhos, vicino a Porto ({eb}). Nel 2022 ha sponsorizzato l'argentino Tito Allemandi, allora tra i primi dieci dell'APT Padel Tour ({pa}). Il motto è "Play like an animal": quasi tutti i modelli portano il nome di un animale.</p>
<h2>È un marchio di nicchia?</h2>
<p>Sì. QUAD è conosciuto soprattutto in Portogallo, non ha giocatori del circuito Premier Padel e le recensioni indipendenti sono poche: per questo nelle nostre schede non trovi ancora valutazioni, solo i dati dichiarati. I prezzi però sono in linea con il mercato: il modello base più caro costa 390 €, contro un prezzo di listino mediano di {euro(med)} per le racchette adulte del nostro database.</p>
<h2>La gamma base</h2>{tab_b}
<ul><li><b>Per chi attacca:</b> la <a href="{u("quad-naja-2026")}">Naja</a> (diamante, bilanciamento extra alto, 12K ×3) e la <a href="{u("quad-shark-2026")}">Shark</a>, che QUAD indica per giocatori molto avanzati.</li>
<li><b>Per chi cerca equilibrio:</b> la <a href="{u("quad-rhino-2024")}">Rhino</a>, una goccia in carbonio 24K, e la <a href="{u("quad-tiger-2026")}">Tiger</a>, la più leggera (340 g) con superficie ruvida per l'effetto.</li>
<li><b>Per spendere meno:</b> <a href="{u("quad-leopard-2026")}">Leopard</a> e <a href="{u("quad-wolf-2026")}">Wolf</a> a 190 €, ibride in carbonio 3K con gomma morbida.</li>
<li><b>Per i ragazzi:</b> la <a href="{u("quad-t-rex-junior-2026")}">T-Rex Junior</a>, rotonda da 330 g.</li></ul>
<h2>Edizioni speciali e linea Creators</h2>
<p>Una buona parte del catalogo QUAD sono edizioni limitate, spesso numerate e con certificato ({qe}):</p>{tab_s}
<ul><li>La <a href="{u("quad-fpf-edition-2026")}">FPF Edition</a> con la Federazione portoghese di calcio: nera opaca con dettagli dorati, 500 pezzi numerati.</li>
<li>La <a href="{u("quad-dragon-ii-fc-porto-edition-2026")}">Dragon II</a> per il Porto, in blu e bianco.</li>
<li>La <a href="{u("quad-siza-vieira-2024")}">racchetta di Álvaro Siza Vieira</a>, disegnata dall'architetto per i suoi 90 anni in 90 esemplari, con carbonio riciclato.</li>
<li>Le collaborazioni con Diogo Dalot, difensore del Manchester United, e con gli artisti Muklay e Guel Do It.</li></ul>
<p>Sotto la grafica, molte di queste edizioni usano le stesse basi tecniche della gamma: carbonio 3K a due o quattro strati e gomma EVA 990Q o Hyper Soft Foam.</p>
<h2>Dove si comprano</h2>
<p>Il canale principale è il sito ufficiale, che spedisce in Portogallo e Spagna con CTT e nel resto del mondo con DHL Express ({qf}). Alcuni modelli si trovano anche sul marketplace Decathlon in Portogallo e in Francia e in negozi portoghesi di padel. Prima di comprare conviene controllare la disponibilità: diverse edizioni speciali sono già esaurite.</p>{box}
<p class="note">Fonti: schede ufficiali {qf}; {eb}; {pa}; {fb}. Prezzi di listino del sito QUAD a novembre 2026.</p>''',
              f'''<p><b>QUAD is a small Portuguese brand that makes its carbon rackets in its own factory in Portugal. Outside Portugal it is a niche brand: you won't find it in the big padel shops, you buy it from the official website. The range has 7 core models between 190 and 390 euros, plus a series of limited and artist editions that go up to 1,900 euros.</b></p>
<h2>Who QUAD is</h2>
<p>QUAD sells padel rackets, pickleball gear and sportswear. Its main distinguishing feature is manufacturing: the rackets are made at the QUAD Factory, which the brand describes as the only factory of its kind in Portugal ({eb}). That is not a given: another Portuguese brand, Volt, told Forbes it designs in-house and manufactures in Asia ({fb}).</p>
<p>On the website you can design a racket from scratch or change the colours of an existing model; QUAD has opened its first own-brand shop at NorteShopping in Matosinhos, near Porto ({eb}). In 2022 it sponsored Argentine player Tito Allemandi, then in the top ten of the APT Padel Tour ({pa}). Its motto is "Play like an animal": almost every model is named after an animal.</p>
<h2>Is it a niche brand?</h2>
<p>Yes. QUAD is known mainly in Portugal, has no players on the Premier Padel tour and independent reviews are scarce: that's why our pages don't have ratings yet, only the stated specs. Prices, though, are in line with the market: the most expensive core model costs €390, against a median list price of {euro(med)} for the adult rackets in our database.</p>
<h2>The core range</h2>{tab_b}
<ul><li><b>For attacking players:</b> the <a href="{u("quad-naja-2026")}">Naja</a> (diamond, extra-high balance, 12K ×3) and the <a href="{u("quad-shark-2026")}">Shark</a>, which QUAD recommends for very advanced players.</li>
<li><b>For balance:</b> the <a href="{u("quad-rhino-2024")}">Rhino</a>, a 24K carbon teardrop, and the <a href="{u("quad-tiger-2026")}">Tiger</a>, the lightest (340 g) with a rough surface for spin.</li>
<li><b>To spend less:</b> the <a href="{u("quad-leopard-2026")}">Leopard</a> and <a href="{u("quad-wolf-2026")}">Wolf</a> at €190, 3K carbon hybrids with a soft core.</li>
<li><b>For juniors:</b> the <a href="{u("quad-t-rex-junior-2026")}">T-Rex Junior</a>, a 330 g round racket.</li></ul>
<h2>Special editions and the Creators line</h2>
<p>A good part of the QUAD catalogue is limited editions, often numbered and with a certificate ({qe}):</p>{tab_s}
<ul><li>The <a href="{u("quad-fpf-edition-2026")}">FPF Edition</a> with the Portuguese Football Federation: matte black with gold details, 500 numbered pieces.</li>
<li>The <a href="{u("quad-dragon-ii-fc-porto-edition-2026")}">Dragon II</a> for FC Porto, in blue and white.</li>
<li>The <a href="{u("quad-siza-vieira-2024")}">Álvaro Siza Vieira racket</a>, designed by the architect for his 90th birthday in 90 pieces, with recycled carbon.</li>
<li>Collaborations with Manchester United defender Diogo Dalot and with artists Muklay and Guel Do It.</li></ul>
<p>Under the artwork, many of these editions share the technical bases of the range: two or four layers of 3K carbon and an EVA 990Q or Hyper Soft Foam core.</p>
<h2>Where to buy</h2>
<p>The main channel is the official website, which ships within Portugal and Spain with CTT and worldwide with DHL Express ({qf}). Some models are also on the Decathlon marketplace in Portugal and France and in Portuguese padel shops. Check availability before buying: several special editions are already sold out.</p>{box}
<p class="note">Sources: official QUAD pages {qf}; {eb}; {pa}; {fb}. List prices from the QUAD website in November 2026.</p>''',
              f'''<p><b>QUAD es una pequeña marca portuguesa que fabrica sus palas de carbono en una fábrica propia en Portugal. Fuera de Portugal es una marca de nicho: no está en las grandes tiendas de pádel y se compra en la web oficial. La gama tiene 7 modelos base entre 190 y 390 euros, más una serie de ediciones limitadas y de autor que llegan a 1.900 euros.</b></p>
<h2>Quién es QUAD</h2>
<p>QUAD vende palas de pádel, material de pickleball y ropa deportiva. Su rasgo principal es la producción: las palas salen de la QUAD Factory, que la marca presenta como la única fábrica de su tipo en Portugal ({eb}). No es lo habitual: otra marca portuguesa, Volt, contó a Forbes que diseña en casa y fabrica en Asia ({fb}).</p>
<p>En la web se puede crear una pala desde cero o cambiar los colores de un modelo existente; QUAD ha abierto su primera tienda propia en el NorteShopping de Matosinhos, cerca de Oporto ({eb}). En 2022 patrocinó al argentino Tito Allemandi, entonces entre los diez primeros del APT Padel Tour ({pa}). Su lema es "Play like an animal": casi todos los modelos llevan nombre de animal.</p>
<h2>¿Es una marca de nicho?</h2>
<p>Sí. QUAD es conocida sobre todo en Portugal, no tiene jugadores en el circuito Premier Padel y las opiniones independientes son pocas: por eso en nuestras fichas aún no hay valoraciones, solo los datos declarados. Los precios, en cambio, están en línea con el mercado: el modelo base más caro cuesta 390 €, frente a un precio de catálogo mediano de {euro(med)} para las palas de adulto de nuestra base.</p>
<h2>La gama base</h2>{tab_b}
<ul><li><b>Para atacar:</b> la <a href="{u("quad-naja-2026")}">Naja</a> (diamante, balance extra alto, 12K ×3) y la <a href="{u("quad-shark-2026")}">Shark</a>, que QUAD recomienda para jugadores muy avanzados.</li>
<li><b>Para buscar equilibrio:</b> la <a href="{u("quad-rhino-2024")}">Rhino</a>, una lágrima de carbono 24K, y la <a href="{u("quad-tiger-2026")}">Tiger</a>, la más ligera (340 g), con superficie rugosa para el efecto.</li>
<li><b>Para gastar menos:</b> la <a href="{u("quad-leopard-2026")}">Leopard</a> y la <a href="{u("quad-wolf-2026")}">Wolf</a> a 190 €, híbridas de carbono 3K con goma blanda.</li>
<li><b>Para los jóvenes:</b> la <a href="{u("quad-t-rex-junior-2026")}">T-Rex Junior</a>, redonda de 330 g.</li></ul>
<h2>Ediciones especiales y línea Creators</h2>
<p>Buena parte del catálogo QUAD son ediciones limitadas, a menudo numeradas y con certificado ({qe}):</p>{tab_s}
<ul><li>La <a href="{u("quad-fpf-edition-2026")}">FPF Edition</a> con la Federación Portuguesa de Fútbol: negra mate con detalles dorados, 500 unidades numeradas.</li>
<li>La <a href="{u("quad-dragon-ii-fc-porto-edition-2026")}">Dragon II</a> para el Oporto, en azul y blanco.</li>
<li>La <a href="{u("quad-siza-vieira-2024")}">pala de Álvaro Siza Vieira</a>, diseñada por el arquitecto por sus 90 años en 90 unidades, con carbono reciclado.</li>
<li>Las colaboraciones con Diogo Dalot, defensa del Manchester United, y con los artistas Muklay y Guel Do It.</li></ul>
<p>Bajo el diseño, muchas de estas ediciones usan las mismas bases técnicas de la gama: carbono 3K de dos o cuatro capas y goma EVA 990Q o Hyper Soft Foam.</p>
<h2>Dónde se compran</h2>
<p>El canal principal es la web oficial, que envía a Portugal y España con CTT y al resto del mundo con DHL Express ({qf}). Algunos modelos están también en el marketplace de Decathlon en Portugal y Francia y en tiendas portuguesas de pádel. Antes de comprar conviene comprobar la disponibilidad: varias ediciones especiales ya están agotadas.</p>{box}
<p class="note">Fuentes: fichas oficiales {qf}; {eb}; {pa}; {fb}. Precios de catálogo de la web de QUAD en noviembre de 2026.</p>''',
              f'''<p><b>QUAD est une petite marque portugaise qui fabrique ses raquettes en carbone dans sa propre usine au Portugal. Hors du Portugal, c'est une marque de niche : on ne la trouve pas dans les grands magasins de padel, on l'achète sur le site officiel. La gamme compte 7 modèles de base entre 190 et 390 euros, plus une série d'éditions limitées et d'artistes qui montent jusqu'à 1 900 euros.</b></p>
<h2>Qui est QUAD</h2>
<p>QUAD vend des raquettes de padel, du matériel de pickleball et des vêtements de sport. Sa particularité principale, c'est la fabrication : les raquettes sortent de la QUAD Factory, que la marque présente comme la seule usine de ce type au Portugal ({eb}). Ce n'est pas la norme : une autre marque portugaise, Volt, a expliqué à Forbes qu'elle conçoit en interne et fabrique en Asie ({fb}).</p>
<p>Sur le site, on peut créer une raquette de zéro ou changer les couleurs d'un modèle existant ; QUAD a ouvert sa première boutique en propre au NorteShopping de Matosinhos, près de Porto ({eb}). En 2022, elle a sponsorisé l'Argentin Tito Allemandi, alors dans le top 10 de l'APT Padel Tour ({pa}). Sa devise est « Play like an animal » : presque tous les modèles portent un nom d'animal.</p>
<h2>Est-ce une marque de niche ?</h2>
<p>Oui. QUAD est surtout connue au Portugal, n'a pas de joueurs sur le circuit Premier Padel et les avis indépendants sont rares : c'est pourquoi nos fiches n'ont pas encore de notes, seulement les données déclarées. Les prix, eux, sont dans la moyenne : le modèle de base le plus cher coûte 390 €, contre un prix catalogue médian de {euro(med)} pour les raquettes adultes de notre base.</p>
<h2>La gamme de base</h2>{tab_b}
<ul><li><b>Pour attaquer :</b> la <a href="{u("quad-naja-2026")}">Naja</a> (diamant, équilibre très haut, 12K ×3) et la <a href="{u("quad-shark-2026")}">Shark</a>, que QUAD destine aux joueurs très avancés.</li>
<li><b>Pour l'équilibre :</b> la <a href="{u("quad-rhino-2024")}">Rhino</a>, une goutte d'eau en carbone 24K, et la <a href="{u("quad-tiger-2026")}">Tiger</a>, la plus légère (340 g), avec surface rugueuse pour l'effet.</li>
<li><b>Pour dépenser moins :</b> la <a href="{u("quad-leopard-2026")}">Leopard</a> et la <a href="{u("quad-wolf-2026")}">Wolf</a> à 190 €, hybrides en carbone 3K à gomme souple.</li>
<li><b>Pour les jeunes :</b> la <a href="{u("quad-t-rex-junior-2026")}">T-Rex Junior</a>, ronde de 330 g.</li></ul>
<h2>Éditions spéciales et ligne Creators</h2>
<p>Une bonne partie du catalogue QUAD est faite d'éditions limitées, souvent numérotées et avec certificat ({qe}) :</p>{tab_s}
<ul><li>La <a href="{u("quad-fpf-edition-2026")}">FPF Edition</a> avec la Fédération portugaise de football : noire mate avec détails dorés, 500 exemplaires numérotés.</li>
<li>La <a href="{u("quad-dragon-ii-fc-porto-edition-2026")}">Dragon II</a> pour le FC Porto, en bleu et blanc.</li>
<li>La <a href="{u("quad-siza-vieira-2024")}">raquette d'Álvaro Siza Vieira</a>, dessinée par l'architecte pour ses 90 ans en 90 exemplaires, en carbone recyclé.</li>
<li>Les collaborations avec Diogo Dalot, défenseur de Manchester United, et avec les artistes Muklay et Guel Do It.</li></ul>
<p>Sous le graphisme, beaucoup de ces éditions reprennent les bases techniques de la gamme : carbone 3K à deux ou quatre couches et gomme EVA 990Q ou Hyper Soft Foam.</p>
<h2>Où les acheter</h2>
<p>Le canal principal est le site officiel, qui livre au Portugal et en Espagne avec CTT et dans le reste du monde avec DHL Express ({qf}). Certains modèles sont aussi sur la marketplace Decathlon au Portugal et en France et dans des magasins de padel portugais. Vérifiez la disponibilité avant d'acheter : plusieurs éditions spéciales sont déjà épuisées.</p>{box}
<p class="note">Sources : fiches officielles {qf} ; {eb} ; {pa} ; {fb}. Prix catalogue du site QUAD en novembre 2026.</p>''')
    qa = [(L("Che marca è QUAD?", "What brand is QUAD?", "¿Qué marca es QUAD?", "Quelle marque est QUAD ?"),
           L("Un marchio portoghese di articoli sportivi che produce racchette da padel in carbonio nella propria fabbrica in Portogallo.", "A Portuguese sports brand that makes carbon padel rackets in its own factory in Portugal.",
             "Una marca portuguesa de material deportivo que fabrica palas de pádel de carbono en su propia fábrica en Portugal.", "Une marque portugaise d'articles de sport qui fabrique des raquettes de padel en carbone dans sa propre usine au Portugal.")),
          (L("Quanto costano le racchette QUAD?", "How much do QUAD rackets cost?", "¿Cuánto cuestan las palas QUAD?", "Combien coûtent les raquettes QUAD ?"),
           L("I modelli base vanno da 190 a 390 euro di listino, la junior costa 140 euro; le edizioni limitate arrivano a 1.900 euro.", "Core models list at 190 to 390 euros and the junior costs 140 euros; limited editions go up to 1,900 euros.",
             "Los modelos base van de 190 a 390 euros de catálogo y la junior cuesta 140 euros; las ediciones limitadas llegan a 1.900 euros.", "Les modèles de base vont de 190 à 390 euros en prix catalogue, la junior coûte 140 euros ; les éditions limitées montent jusqu'à 1 900 euros.")),
          (L("Dove si comprano le racchette QUAD?", "Where can I buy QUAD rackets?", "¿Dónde se compran las palas QUAD?", "Où acheter les raquettes QUAD ?"),
           L("Soprattutto sul sito ufficiale quad-sports.com, che spedisce anche all'estero; alcuni modelli sono sul marketplace Decathlon in Portogallo e Francia.", "Mainly on the official website quad-sports.com, which ships abroad; some models are on the Decathlon marketplace in Portugal and France.",
             "Sobre todo en la web oficial quad-sports.com, que envía también al extranjero; algunos modelos están en el marketplace de Decathlon en Portugal y Francia.", "Surtout sur le site officiel quad-sports.com, qui livre aussi à l'étranger ; certains modèles sont sur la marketplace Decathlon au Portugal et en France."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("QUAD, le racchette da padel fatte in Portogallo: tutti i modelli", "QUAD, the padel rackets made in Portugal: every model",
               "QUAD, las palas de pádel hechas en Portugal: todos los modelos", "QUAD, les raquettes de padel fabriquées au Portugal : tous les modèles")
    desc = L("Chi è QUAD, il marchio portoghese che produce le racchette in casa: gamma base, edizioni limitate, prezzi e dove comprarle.",
             "Who QUAD is, the Portuguese brand that makes its own rackets: core range, limited editions, prices and where to buy.",
             "Quién es QUAD, la marca portuguesa que fabrica sus propias palas: gama base, ediciones limitadas, precios y dónde comprarlas.",
             "Qui est QUAD, la marque portugaise qui fabrique ses propres raquettes : gamme de base, éditions limitées, prix et où les acheter.")
    scrivi_articolo(QUAD_SLUG, titolo + " | PadelMetrix", desc, titolo, "QUAD", corpo + faq_htm, items=qs, ld_extra=[faq_ld])
    return QUAD_SLUG, titolo, L("Il marchio portoghese di nicchia che produce in casa: gamma, edizioni limitate e prezzi.", "The niche Portuguese brand that makes its own rackets: range, limited editions and prices.",
                                "La marca portuguesa de nicho que fabrica en casa: gama, ediciones limitadas y precios.", "La marque portugaise de niche qui fabrique elle-même : gamme, éditions limitées et prix.")


# ---------------------------------------------------------------- Indice

def indice(arts):
    path, alt = P("articoli"), ALT("articoli")
    cr, ld = crumbs([H(), (L("Articoli", "Articles", "Artículos", "Articles"), None)])
    lista = "".join(f'<li><a href="{P("articoli", s)}"><b>{e(t)}</b></a><br><span class="note">{e(d)}</span></li>' for s, t, d in arts)
    corpo = f'''{cr}
<div class="intro"><h1>{L("Articoli", "Articles", "Artículos", "Articles")}</h1><p>{L(
        "Novità, confronti tra versioni e approfondimenti sulle racchette da padel, con i dati del database PadelMetrix e le fonti citate.",
        "New releases, comparisons between versions and in-depth articles on padel rackets, with data from the PadelMetrix database and cited sources.",
        "Novedades, comparativas entre versiones y artículos en profundidad sobre palas de pádel, con los datos de la base de PadelMetrix y las fuentes citadas.", "Nouveautés, comparatifs entre versions et articles de fond sur les raquettes de padel, avec les données de la base PadelMetrix et des sources citées.")}</p></div>
<div class="prose"><ul class="clean lista-art">{lista}</ul></div>'''
    S.scrivi(path, pagina(L("Articoli sulle racchette da padel | PadelMetrix", "Padel racket articles | PadelMetrix", "Artículos sobre palas de pádel | PadelMetrix", "Articles sur les raquettes de padel | PadelMetrix"),
                          L("Novità 2027, confronti tra versioni e approfondimenti sulle racchette da padel, con dati e fonti.",
                            "2027 releases, comparisons between versions and in-depth articles on padel rackets, with data and sources.",
                            "Novedades 2027, comparativas entre versiones y artículos sobre palas de pádel, con datos y fuentes.", "Nouveautés 2027, comparatifs entre versions et articles de fond sur les raquettes de padel, avec données et sources."),
                          path, corpo, on="articoli", ld=[ld], alt=alt), alt)


RACCHETTE_ARTICOLO = {"siux-diablo-pro-2026-vs-2027-cosa-cambia": ["siux-diablo-pro-2026", "siux-diablo-pro-2027"],
                      "ale-galan-chi-e-e-che-racchetta-usa": ["adidas-metalbone-hrd-plus-2026", "adidas-metalbone-2026"],
                      **{_g["slug"]: _g["racchette"] for _g in GIOCATORI}}


def main():
    db = carica()
    elenco = {}
    for l in LINGUE:
        set_lang(l)
        arts = [art_quad(db), art_durata(db), art_carbonio(db), art_peso(db), art_over50(db), art_scarpe(db), fitp_sorpasso(db), padel_regole(db), pickleball_regole(db), migliori_2026(db), confronti_2027(db), novita_2027(db), *(giocatore(db, G) for G in reversed(GIOCATORI)), galan(db), diablo(db)]  # più recenti in alto
        indice(arts)
        for slug, titolo, desc in arts:
            x = elenco.setdefault(slug, {"slug": slug, "data": DATE_ART.get(slug, OGGI_ISO), "racchette": RACCHETTE_ARTICOLO.get(slug, []), "titolo": {}, "desc": {}, "url": {}})
            x["titolo"][l], x["desc"][l], x["url"][l] = titolo, desc, P("articoli", slug)
    (ROOT / "data" / "articoli.json").write_text(json.dumps(list(elenco.values()), ensure_ascii=False, indent=1), encoding="utf-8")
    set_lang("it")
    (ROOT / "scripts" / "pagine_articoli.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine articoli generate")


if __name__ == "__main__":
    main()
