#!/usr/bin/env python3
"""Genera le pagine di sezione in it/en/es: Racchette (con filtri), marche, confronti, guide, Bambini."""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import (ROOT, SITO, e, L, P, ALT, tr, carica, coppie, confronto_url, confronto_slug, crumbs, pagina, griglia, ordina,  # noqa: E402
                  FORMA, LIVN, STILEN, LIV, euro, numero, url_r, LINGUE, set_lang, data_riga)
import traduci as T  # noqa: E402


def scrivi(path, html_txt, alt):
    S.scrivi(path, html_txt, alt)


def H():
    return S.home_crumb()


# ---------------------------------------------------------------- Racchette (elenco con filtri)

def filtri_js():
    uno, piu = L("racchetta", "racket", "pala", "raquette"), L("racchette", "rackets", "palas", "raquettes")
    return """<script>
(function(){
var q=new URLSearchParams(location.search);var f=document.getElementById('filtri');if(!f)return;
function nz(s){return (s||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();}
var cards=[].slice.call(document.querySelectorAll('.rgrid .rcard'));var out=document.getElementById('conta');
['marca','forma','tatto','livello','stile','cat','prezzo','q'].forEach(function(k){var el=f.elements[k];if(el&&q.get(k))el.value=q.get(k);});
function run(){var v={};['marca','forma','tatto','livello','stile','cat','prezzo','q'].forEach(function(k){v[k]=(f.elements[k].value||'').toLowerCase();});
var n=0;cards.forEach(function(c){var d=c.dataset,ok=true;
if(v.marca&&d.marca!==v.marca)ok=false;if(v.forma&&d.forma!==v.forma)ok=false;if(v.tatto&&d.tatto!==v.tatto)ok=false;if(v.livello&&d.livello!==v.livello)ok=false;
if(v.stile&&d.stile!==v.stile)ok=false;if(v.cat&&d.cat!==v.cat)ok=false;
if(v.prezzo&&(!d.prezzo||parseFloat(d.prezzo)>parseFloat(v.prezzo)))ok=false;if(v.q&&nz(d.nome).indexOf(nz(v.q).trim())<0)ok=false;
c.style.display=ok?'':'none';if(ok)n++;});out.textContent=n+(n===1?' %s':' %s');}
f.addEventListener('input',run);f.addEventListener('change',run);run();})();
</script>""" % (uno, piu)


def opt(vals, sel_label):
    return f'<option value="">{sel_label}</option>' + "".join(f'<option value="{v}">{e(l)}</option>' for v, l in vals)


def elenco(db):
    marche = sorted({(n["marca_slug"], n["marca"]) for n in db}, key=lambda x: x[1].lower())
    tutte, tutti = L("Tutte", "All", "Todas", "Toutes"), L("Tutti", "All", "Todos", "Tous")
    prezzi = [(str(x), L(f"fino a {x} €", f"up to €{x}", f"hasta {x} €", f"jusqu'à {x} €")) for x in (100, 150, 200, 300)]
    form = f'''<form class="filtri" id="filtri" onsubmit="return false">
<label>{L("Cerca", "Search", "Buscar", "Rechercher")}<input name="q" type="search" placeholder="{L("Modello o giocatore", "Model or player", "Modelo o jugador", "Modèle ou joueur")}"></label>
<label>{L("Marca", "Brand", "Marca", "Marque")}<select name="marca">{opt(marche, tutte)}</select></label>
<label>{L("Forma", "Shape", "Forma", "Forme")}<select name="forma">{opt(list(S.forme_d().items()), tutte)}</select></label>
<label>{L("Tatto", "Feel", "Tacto", "Toucher")}<select name="tatto">{opt(list(S.TATTI().items()), tutti)}</select></label>
<label>{L("Livello", "Level", "Nivel", "Niveau")}<select name="livello">{opt([(k, LIVN(k)) for k in LIV], tutti)}</select></label>
<label>{L("Stile", "Style", "Estilo", "Style")}<select name="stile">{opt(list(S.stili_d().items()), tutti)}</select></label>
<label>{L("Per chi", "For", "Para quién", "Pour qui")}<select name="cat">{opt([("adulto", L("Adulto", "Adult", "Adulto", "Adulte")), ("donna", L("Modelli femminili", "Women's models", "Modelos femeninos", "Modèles femme")), ("junior", "Junior")], tutti)}</select></label>
<label>{L("Prezzo di listino", "List price", "Precio de lista", "Prix public")}<select name="prezzo">{opt(prezzi, L("Qualsiasi", "Any", "Cualquiera", "Peu importe"))}</select></label>
</form>'''
    cr, ld = crumbs([H(), (L("Racchette", "Rackets", "Palas", "Raquettes"), None)])
    nm = len(marche)
    corpo = f'''{cr}
<div class="intro"><h1>{L("Racchette da padel 2026 e 2027", "Padel rackets 2026 and 2027", "Palas de pádel 2026 y 2027", "Raquettes de padel 2026 et 2027")}</h1>
<p>{L(f"{len(db)} racchette di {nm} marche con dati tecnici, sintesi delle recensioni e modelli simili. Filtra per marca, forma, tatto, livello, stile e prezzo, oppure fai il <a href=\"{P('selettore')}\">test in 2 minuti</a> o leggi le <a href=\"{P('guide')}\">guide alla scelta</a>.",
      f"{len(db)} rackets from {nm} brands with specs, review summaries and similar models. Filter by brand, shape, feel, level, style and price, or take the <a href=\"{P('selettore')}\">2-minute quiz</a> or read the <a href=\"{P('guide')}\">buying guides</a>.",
      f"{len(db)} palas de {nm} marcas con datos técnicos, resumen de reseñas y modelos similares. Filtra por marca, forma, tacto, nivel, estilo y precio, o haz el <a href=\"{P('selettore')}\">test de 2 minutos</a> o lee las <a href=\"{P('guide')}\">guías de compra</a>.", f"{len(db)} raquettes de {nm} marques avec fiches techniques, synthèse des avis et modèles similaires. Filtrez par marque, forme, toucher, niveau, style et prix, ou faites le <a href=\"{P('selettore')}\">test en 2 minutes</a> ou lisez les <a href=\"{P('guide')}\">guides d'achat</a>.")}</p></div>
<div class="marche">{"".join(f'<a href="{P("marche", s)}">{e(m)}</a>' for s, m in marche)}</div>
<p style="border:2px solid #C6F432;border-radius:12px;padding:16px 20px;background:#F4FBE3;margin:16px 0 24px">{L("<b>Nuovo al padel?</b> Prima di scegliere la racchetta leggi", "<b>New to padel?</b> Before choosing a racket, read", "<b>¿Nuevo en el pádel?</b> Antes de elegir la pala, lee", "<b>Nouveau au padel ?</b> Avant de choisir votre raquette, lisez")} <a href="{P("articoli", "regolamento-padel-regole-spiegate")}">{L("il regolamento del padel spiegato semplice", "the padel rules explained simply", "el reglamento del pádel explicado fácil", "les règles du padel expliquées simplement")}</a>: {L("servizio, pareti, punteggio e Star Point.", "serve, walls, scoring and Star Point.", "saque, paredes, tanteo y Star Point.", "service, vitres, score et Star Point.")}</p>
{form}
<p class="conta" id="conta">{len(db)} {L("racchette", "rackets", "palas", "raquettes")}</p>
{griglia(ordina(db))}'''
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "numberOfItems": len(db),
                "itemListElement": [{"@type": "ListItem", "position": i, "url": SITO + url_r(n), "name": n["titolo"]} for i, n in enumerate(ordina(db), 1)]}
    path = P("racchette")
    scrivi(path, pagina(L("Racchette da padel 2026 e 2027: schede tecniche, confronti e filtri | PadelMetrix",
                          "Padel rackets 2026 and 2027: specs, comparisons and filters | PadelMetrix",
                          "Palas de pádel 2026 y 2027: fichas técnicas, comparativas y filtros | PadelMetrix", "Raquettes de padel 2026 et 2027 : fiches techniques, comparaisons et filtres | PadelMetrix"),
                        L(f"{len(db)} racchette da padel di {nm} marche: dati tecnici, opinioni e modelli simili. Filtra per livello, forma, peso, prezzo e marca.",
                          f"{len(db)} padel rackets from {nm} brands: specs, reviews and similar models. Filter by level, shape, weight, price and brand.",
                          f"{len(db)} palas de pádel de {nm} marcas: datos técnicos, opiniones y modelos similares. Filtra por nivel, forma, peso, precio y marca.", f"{len(db)} raquettes de padel de {nm} marques : fiches techniques, avis et modèles similaires. Filtrez par niveau, forme, poids, prix et marque."),
                        path, corpo, on="racchette", ld=[ld, itemlist], extra_js=filtri_js(), alt=ALT("racchette")), ALT("racchette"))


# ---------------------------------------------------------------- Marche

def e_(a):
    a = [str(x) for x in a]
    c = L(" e ", " and ", " y ", " et ")
    return a[0] if len(a) == 1 else ", ".join(a[:-1]) + c + a[-1]


def marche(db, pairs):
    per_marca = {}
    for n in db:
        per_marca.setdefault((n["marca_slug"], n["marca"]), []).append(n)
    per = {n["slug"]: n for n in db}
    voci = []
    R = L("Racchette", "Rackets", "Palas", "Raquettes")
    for (ms, m), items in sorted(per_marca.items(), key=lambda kv: -len(kv[1])):
        anni = sorted({n["anno"] for n in items}, reverse=True)
        anni_txt = e_(sorted(anni))
        forme = {}
        for n in items:
            if n["forma"]:
                forme[n["forma"]] = forme.get(n["forma"], 0) + 1
        forme_txt = ", ".join(f"{c} {FORMA(f).lower()}" for f, c in sorted(forme.items(), key=lambda kv: -kv[1]))
        gioc = sorted({n["giocatore"] for n in items if n["giocatore"] and "ispirata" not in n["giocatore"]})
        junior = [n for n in items if n["categoria"] == "junior"]
        sezioni = ""
        for a in anni:
            sub = ordina([n for n in items if n["anno"] == a])
            sezioni += f'<section class="block"><h2>{L(f"Racchette {e(m)} {a}", f"{e(m)} rackets {a}", f"Palas {e(m)} {a}", f"Raquettes {e(m)} {a}")}</h2>{griglia(sub)}</section>'
        mp = [(x, y) for x, y in pairs if per[x]["marca"] == m or per[y]["marca"] == m]
        conf = ""
        if mp:
            conf = f'<section class="block"><h2>{L("Confronti con racchette " + e(m), "Comparisons with " + e(m) + " rackets", "Comparativas con palas " + e(m), "Comparaisons avec les raquettes " + e(m))}</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>' for x, y in mp) + "</ul></section>"
        cr, ld = crumbs([H(), (R, P("racchette")), (m, None)])
        intro = L(f"Nel database ci sono {len(items)} racchette {m} delle collezioni {anni_txt}",
                  f"The database holds {len(items)} {m} rackets from the {anni_txt} collections",
                  f"En la base de datos hay {len(items)} palas {m} de las colecciones {anni_txt}", f"La base de données compte {len(items)} raquettes {m} des collections {anni_txt}")
        intro += f": {forme_txt}." if forme_txt else "."
        if gioc:
            intro += L(" Tra i modelli dei giocatori professionisti: ", " Pro player models include: ", " Entre los modelos de jugadores profesionales: ", " Parmi les modèles des joueurs professionnels : ") + ", ".join(gioc[:6]) + "."
        if junior:
            intro += " " + (L(f"{len(junior)} è un modello junior.", f"{len(junior)} is a junior model.", f"{len(junior)} es un modelo junior.", f"{len(junior)} est un modèle junior.") if len(junior) == 1
                            else L(f"{len(junior)} sono modelli junior.", f"{len(junior)} are junior models.", f"{len(junior)} son modelos junior.", f"{len(junior)} sont des modèles junior."))
        h1 = L(f"Racchette {e(m)} {anni_txt}", f"{e(m)} padel rackets {anni_txt}", f"Palas {e(m)} {anni_txt}", f"Raquettes de padel {e(m)} {anni_txt}")
        corpo = f'''{cr}
<div class="intro"><h1>{h1}</h1><p>{e(intro)} {L("Ogni scheda riporta dati tecnici, a chi è adatta e le alternative più vicine.", "Each page lists the specs, who it suits and the closest alternatives.", "Cada ficha incluye datos técnicos, para quién es y las alternativas más cercanas.", "Chaque fiche présente les caractéristiques, le profil de joueur visé et les alternatives les plus proches.")}</p></div>
{sezioni}{conf}'''
        title = L(f"Racchette {m} {anni_txt}: tutti i {len(items)} modelli a confronto | PadelMetrix",
                  f"{m} padel rackets {anni_txt}: all {len(items)} models compared | PadelMetrix",
                  f"Palas {m} {anni_txt}: los {len(items)} modelos comparados | PadelMetrix", f"Raquettes de padel {m} {anni_txt} : les {len(items)} modèles comparés | PadelMetrix")
        desc = L(f"Tutte le racchette da padel {m} {anni_txt}: {len(items)} schede con peso, forma, livello, opinioni e confronti tra modelli.",
                 f"All {m} padel rackets {anni_txt}: {len(items)} pages with weight, shape, level, reviews and model comparisons.",
                 f"Todas las palas de pádel {m} {anni_txt}: {len(items)} fichas con peso, forma, nivel, opiniones y comparativas entre modelos.", f"Toutes les raquettes de padel {m} {anni_txt} : {len(items)} fiches avec poids, forme, niveau, avis et comparaisons entre modèles.")
        path = P("marche", ms)
        scrivi(path, pagina(title, desc, path, corpo, on="racchette", ld=[ld], alt=ALT("marche", ms)), ALT("marche", ms))
        voci.append((ms, m, len(items)))
    cr, ld = crumbs([H(), (L("Marche", "Brands", "Marcas", "Marques"), None)])
    corpo = f'''{cr}<div class="intro"><h1>{L("Marche di racchette da padel", "Padel racket brands", "Marcas de palas de pádel", "Marques de raquettes de padel")}</h1><p>{L(f"Le {len(voci)} marche presenti nel database, con tutti i modelli delle collezioni 2026 e 2027.", f"The {len(voci)} brands in the database, with all models from the 2026 and 2027 collections.", f"Las {len(voci)} marcas de la base de datos, con todos los modelos de las colecciones 2026 y 2027.", f"Les {len(voci)} marques de la base de données, avec tous les modèles des collections 2026 et 2027.")}</p></div>
<ul class="lista-link">{"".join(f'<li><a href="{P("marche", s)}">{L(f"Racchette {e(m)}", f"{e(m)} rackets", f"Palas {e(m)}", f"Raquettes {e(m)}")}</a> · {c}</li>' for s, m, c in voci)}</ul>'''
    path = P("marche")
    scrivi(path, pagina(L("Marche di racchette da padel: Bullpadel, Nox, Adidas, Head e altre | PadelMetrix",
                          "Padel racket brands: Bullpadel, Nox, Adidas, Head and more | PadelMetrix",
                          "Marcas de palas de pádel: Bullpadel, Nox, Adidas, Head y más | PadelMetrix", "Marques de raquettes de padel : Bullpadel, Nox, Adidas, Head et plus | PadelMetrix"),
                        L("Tutte le marche di racchette da padel nel database PadelMetrix, con i modelli 2026 e 2027 di ciascuna.",
                          "All padel racket brands in the PadelMetrix database, with each brand's 2026 and 2027 models.",
                          "Todas las marcas de palas de pádel de la base de datos PadelMetrix, con los modelos 2026 y 2027 de cada una.", "Toutes les marques de raquettes de padel de la base PadelMetrix, avec les modèles 2026 et 2027 de chaque marque."),
                        path, corpo, on="racchette", ld=[ld], alt=ALT("marche")), ALT("marche"))


# ---------------------------------------------------------------- Confronti

def righe_cmp():
    return [(L("Marca", "Brand", "Marca", "Marque"), lambda n: n["marca"]), (L("Collezione", "Collection", "Colección", "Collection"), lambda n: str(n["anno"])),
            (L("Giocatore", "Player", "Jugador", "Joueur"), lambda n: n["giocatore"] if not n["giocatore"] or "ispirata" not in n["giocatore"] else tr(n["giocatore"])),
            (L("Forma", "Shape", "Forma", "Forme"), lambda n: FORMA(n["forma"])), (L("Peso", "Weight", "Peso", "Poids"), lambda n: n["peso"]),
            (L("Bilanciamento", "Balance", "Balance", "Équilibre"), lambda n: tr(n["bilanciamento"]) if isinstance(n["bilanciamento"], str) else None),
            (L("Nucleo", "Core", "Núcleo", "Noyau"), lambda n: tr(n["nucleo"]) if isinstance(n["nucleo"], str) else None),
            (L("Superficie", "Face", "Cara", "Surface"), lambda n: tr(n["superficie"])),
            (L("Tatto", "Feel", "Tacto", "Toucher"), lambda n: tr(n["sensazione"]) if isinstance(n["sensazione"], str) else None),
            (L("Livello", "Level", "Nivel", "Niveau"), lambda n: LIVN(n["livello"])),
            (L("Stile", "Style", "Estilo", "Style"), lambda n: STILEN(n["stile"])),
            (L("Prezzo di listino", "List price", "Precio de lista", "Prix public"), lambda n: euro(n["prezzo"]) if n["prezzo"] else None)]


def verdetto(a, b):
    an, bn = a["nome"], b["nome"]
    frasi = []
    if a["marca"] == b["marca"] and a["modello"] == b["modello"]:
        frasi.append(L(f"Sono due versioni dello stesso modello: la {an} e la {bn}.", f"These are two versions of the same model: the {an} and the {bn}.",
                       f"Son dos versiones del mismo modelo: la {an} y la {bn}.", f"Ce sont deux versions du même modèle : la {an} et la {bn}."))
    comune = []
    if a["forma"] and a["forma"] == b["forma"]:
        comune.append(L(f"forma {FORMA(a['forma']).lower()}", f"{FORMA(a['forma']).lower()} shape", f"forma {FORMA(a['forma']).lower()}", f"forme {FORMA(a['forma']).lower()}"))
    if a["livello"] and a["livello"] == b["livello"]:
        comune.append(L(f"livello {LIVN(a['livello']).lower()}", f"{LIVN(a['livello']).lower()} level", f"nivel {LIVN(a['livello']).lower()}", f"niveau {LIVN(a['livello']).lower()}"))
    if a["stile"] and a["stile"] == b["stile"]:
        comune.append(L(f"stile {STILEN(a['stile']).lower()}", f"{STILEN(a['stile']).lower()} style", f"estilo {STILEN(a['stile']).lower()}", f"style {STILEN(a['stile']).lower()}"))
    if comune:
        frasi.append(L("Hanno in comune ", "They share ", "Tienen en común ", "Elles ont en commun : ") + ", ".join(comune) + ".")
    diff = []
    if a["forma"] and b["forma"] and a["forma"] != b["forma"]:
        fa, fb = FORMA(a["forma"]).lower(), FORMA(b["forma"]).lower()
        diff.append(L(f"la {an} è {fa}, la {bn} {fb}", f"the {an} is {fa}, the {bn} {fb}", f"la {an} es {fa}, la {bn} {fb}", f"la {an} a une forme {fa}, la {bn} {fb}"))
    if a["peso"] and b["peso"] and a["peso"] != b["peso"]:
        diff.append(L(f"pesano {a['peso']} contro {b['peso']}", f"they weigh {a['peso']} versus {b['peso']}", f"pesan {a['peso']} frente a {b['peso']}", f"elles pèsent {a['peso']} contre {b['peso']}"))
    if a["livello"] and b["livello"] and a["livello"] != b["livello"]:
        la, lb = LIVN(a["livello"]).lower(), LIVN(b["livello"]).lower()
        diff.append(L(f"il livello indicato è {la} per la prima e {lb} per la seconda", f"the stated level is {la} for the first and {lb} for the second",
                      f"el nivel indicado es {la} para la primera y {lb} para la segunda", f"le niveau indiqué est {la} pour la première et {lb} pour la seconde"))
    if a["prezzo"] and b["prezzo"] and abs(a["prezzo"] - b["prezzo"]) >= 20:
        c = a if a["prezzo"] < b["prezzo"] else b
        lo, hi = euro(min(a["prezzo"], b["prezzo"])), euro(max(a["prezzo"], b["prezzo"]))
        diff.append(L(f"la {c['nome']} costa meno di listino ({lo} contro {hi})", f"the {c['nome']} has a lower list price ({lo} versus {hi})",
                      f"la {c['nome']} cuesta menos de lista ({lo} frente a {hi})", f"la {c['nome']} est moins chère au prix public ({lo} contre {hi})"))
    if diff:
        frasi.append(L("Le differenze principali: ", "The main differences: ", "Las principales diferencias: ", "Les principales différences : ") + "; ".join(diff) + ".")
    elif not comune:
        frasi.append(L("I dati dichiarati sono vicini: conviene guardare le schede complete.", "The declared data are close: check the full pages.",
                       "Los datos declarados son parecidos: conviene mirar las fichas completas.", "Les données déclarées sont proches : consultez les fiches complètes."))
    out = " ".join(frasi)
    return out[0].upper() + out[1:] if out else out


def barre_doppie(a, b):
    va, vb = a["val"], b["val"]
    if not (va and vb and va.get("titolo") == vb.get("titolo") and va.get("scala") == vb.get("scala")):
        return ""
    nomi = [v["nome"] for v in va["voci"]]
    righe = ""
    for nm in nomi:
        x = next((v["valore"] for v in va["voci"] if v["nome"] == nm), None)
        y = next((v["valore"] for v in vb["voci"] if v["nome"] == nm), None)
        if x is None or y is None:
            continue
        righe += f'<tr><td>{e(tr(nm))}</td><td>{numero(x)}</td><td>{numero(y)}</td></tr>'
    if not righe:
        return ""
    fonte = va["titolo"].replace("Valutazioni di ", "").replace("Valutazioni del ", "").replace("Valutazioni ", "")
    return f'''<h2>{L("Punteggi a confronto", "Scores compared", "Puntuaciones comparadas", "Notes comparées")}</h2><div class="tablebox"><table class="tab"><thead><tr><th>{e(tr(va["titolo"]))} ({L("su", "out of", "sobre", "sur")} {va["scala"]})</th><th>{e(a["nome"])}</th><th>{e(b["nome"])}</th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">{L(f"Punteggi pubblicati da fonti esterne ({e(tr(fonte))}), riportati come sono. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.",
                   f"Scores published by external sources ({e(tr(fonte))}), reported as they are. The PadelMetrix score will follow with our own rating method.",
                   f"Puntuaciones publicadas por fuentes externas ({e(tr(fonte))}), tal cual. La puntuación PadelMetrix llegará con nuestro método de valoración.", f"Notes publiées par des sources externes ({e(tr(fonte))}), reprises telles quelles. La note PadelMetrix arrivera avec notre propre méthode d'évaluation.")}</p>'''


def confronti(db, pairs):
    per = {n["slug"]: n for n in db}
    C = L("Confronta", "Compare", "Comparar", "Comparer")
    for x, y in pairs:
        a, b = per[x], per[y]
        righe = ""
        for lab, fn in righe_cmp():
            va, vb = fn(a), fn(b)
            if va or vb:
                cap = (lambda v: v[0].upper() + v[1:] if v and S.lang() != "it" else v)
                righe += f"<tr><td>{lab}</td><td>{e(cap(va) or '—')}</td><td>{e(cap(vb) or '—')}</td></tr>"
        pa, pb = a["d"]["pagina"], b["d"]["pagina"]

        def scelta(p, q):
            v = [t for t in p.get("adatta", []) if t not in q.get("adatta", [])] + [t for t in p.get("pro", []) if t not in q.get("pro", [])]
            return (v or p.get("adatta", []))[:3]
        ad_a, ad_b = scelta(pa, pb), scelta(pb, pa)
        altri = [(p, q) for p, q in pairs if (p, q) != (x, y) and ({p, q} & {x, y})][:8]
        altri_html = ""
        if altri:
            altri_html = f'<h2>{L("Altri confronti", "Other comparisons", "Otras comparativas", "Autres comparaisons")}</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(p, q)}">{e(per[p]["nome"])} vs {e(per[q]["nome"])}</a></li>' for p, q in altri) + "</ul>"
        cs = confronto_slug(x, y)
        path = P("confronta", cs)
        alt = ALT("confronta", cs)
        tit = f"{a['titolo']} vs {b['titolo']}"
        cr, ld = crumbs([H(), (C, P("confronta")), (f"{a['nome']} vs {b['nome']}", None)])

        def box(n, ad):
            nm = e(n["nome"])
            return (f'<div class="card"><h2>{L(f"Scegli la {nm} se", f"Choose the {nm} if", f"Elige la {nm} si", f"Choisissez la {nm} si")}</h2><ul class="clean">{"".join(f"<li>{e(tr(t))}</li>" for t in ad)}</ul>'
                    f'<p><a href="{url_r(n)}">{L(f"Scheda completa della {nm}", f"Full page of the {nm}", f"Ficha completa de la {nm}", f"Fiche complète de la {nm}")}</a></p></div>')
        corpo = f'''{cr}
<div class="intro"><h1>{e(a["nome"])} vs {e(b["nome"])}</h1><p>{e(verdetto(a, b))}</p></div>
<div class="prose" style="max-width:none">
<h2>{L("Dati tecnici a confronto", "Specs compared", "Datos técnicos comparados", "Caractéristiques comparées")}</h2>
<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{url_r(a)}">{e(a["titolo"])}</a></th><th><a href="{url_r(b)}">{e(b["titolo"])}</a></th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">{L('Dati dalle schede PadelMetrix, che citano le fonti di ogni valore. "—" indica un dato non dichiarato.', 'Data from the PadelMetrix pages, which cite the source of every value. "—" means the value is not stated.', 'Datos de las fichas PadelMetrix, que citan la fuente de cada valor. "—" indica un dato no declarado.', 'Données issues des fiches PadelMetrix, qui citent la source de chaque valeur. « — » signifie que la valeur n\'est pas déclarée.')}</p>
{barre_doppie(a, b)}
<h2>{L("Quale scegliere", "Which one to choose", "Cuál elegir", "Laquelle choisir")}</h2>
<div class="vs">
{box(a, ad_a)}
{box(b, ad_b)}
</div>
{altri_html}
</div>'''
        desc = L(f"{tit}: differenze di peso, forma, livello e prezzo, punteggi e quale scegliere in base al tuo gioco.",
                 f"{tit}: differences in weight, shape, level and price, scores and which one to choose for your game.",
                 f"{tit}: diferencias de peso, forma, nivel y precio, puntuaciones y cuál elegir según tu juego.", f"{tit} : différences de poids, de forme, de niveau et de prix, notes et laquelle choisir selon votre jeu.")
        scrivi(path, pagina(L(f"{tit}: differenze e quale scegliere | PadelMetrix", f"{tit}: differences and which to choose | PadelMetrix", f"{tit}: diferencias y cuál elegir | PadelMetrix", f"{tit} : différences et laquelle choisir | PadelMetrix"),
                            desc[:300], path, corpo, on="confronta", ld=[ld], alt=alt), alt)

    # hub con strumento
    indice = [{k: n[k] for k in ("slug", "titolo", "nome", "marca", "anno", "peso", "livello", "stile", "forma", "prezzo", "giocatore", "superficie")} for n in ordina(db)]
    for i in indice:
        i["livello"] = LIVN(i["livello"])
        i["stile"] = STILEN(i["stile"])
        i["forma"] = FORMA(i["forma"])
        i["superficie"] = tr(i["superficie"])
        i["url"] = P("racchette", i["slug"])
        i["prezzo"] = euro(i["prezzo"]) if i["prezzo"] else None
    pairkeys = [f"{x}|{y}" for x, y in pairs]
    opts = "".join(f'<option value="{n["slug"]}">{e(n["titolo"])}</option>' for n in sorted(db, key=lambda n: n["titolo"]))
    labels = [[L("Marca", "Brand", "Marca", "Marque"), "marca"], [L("Collezione", "Collection", "Colección", "Collection"), "anno"], [L("Giocatore", "Player", "Jugador", "Joueur"), "giocatore"],
              [L("Forma", "Shape", "Forma", "Forme"), "forma"], [L("Peso", "Weight", "Peso", "Poids"), "peso"], [L("Superficie", "Face", "Cara", "Surface"), "superficie"],
              [L("Livello", "Level", "Nivel", "Niveau"), "livello"], [L("Stile", "Style", "Estilo", "Style"), "stile"], [L("Prezzo di listino", "List price", "Precio de lista", "Prix public"), "prezzo"]]
    base_c = P("confronta")
    tool_js = "<script>var IDX=" + json.dumps(indice, ensure_ascii=False) + ";var PAIRS=" + json.dumps(pairkeys) + ";var LAB=" + json.dumps(labels, ensure_ascii=False) + ";var BASE=" + json.dumps(base_c) + ";var FULL=" + json.dumps(L("Confronti completi già spiegati", "Full comparisons already explained", "Comparativas completas ya explicadas", "Comparaisons complètes déjà expliquées"), ensure_ascii=False) + ";var DIFF=" + json.dumps(L("Le righe evidenziate sono quelle in cui le racchette sono diverse.", "Highlighted rows are where the rackets differ.", "Las filas resaltadas son aquellas en las que las palas son distintas.", "Les lignes surlignées sont celles où les raquettes diffèrent."), ensure_ascii=False) + """;
(function(){var sel=[1,2,3,4].map(function(i){return document.getElementById('r'+i);}),out=document.getElementById('cmp-out');
var q=new URLSearchParams(location.search).get('r');if(q){q.split(',').slice(0,4).forEach(function(v,i){if(v)sel[i].value=v;});}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function get(s){for(var i=0;i<IDX.length;i++)if(IDX[i].slug===s)return IDX[i];return null;}
function run(){var rs=[],seen={};sel.forEach(function(x){var r=get(x.value);if(r&&!seen[r.slug]){seen[r.slug]=1;rs.push(r);}});
if(rs.length<2){out.innerHTML='';if(history.replaceState)history.replaceState(null,'',location.pathname+(rs.length?'?r='+rs[0].slug:''));return;}
if(history.replaceState)history.replaceState(null,'',location.pathname+'?r='+rs.map(function(r){return r.slug;}).join(','));
var h='<div class="tablebox"><table class="tab cmp-n'+rs.length+'"><thead><tr><th></th>';rs.forEach(function(r){h+='<th><a href="'+r.url+'">'+esc(r.titolo)+'</a></th>';});h+='</tr></thead><tbody>';
LAB.forEach(function(l){var v=rs.map(function(r){return r[l[1]];});if(!v.some(function(x){return x;}))return;var d=v.some(function(x){return String(x||'')!==String(v[0]||'');});
h+='<tr'+(d?' class="diff"':'')+'><td>'+l[0]+'</td>';v.forEach(function(x){h+='<td>'+esc(x||'—')+'</td>';});h+='</tr>';});
h+='</tbody></table></div><p class="note">'+DIFF+'</p>';var links=[];
for(var a=0;a<rs.length;a++)for(var b=a+1;b<rs.length;b++){var k=[rs[a].slug,rs[b].slug].sort();if(PAIRS.indexOf(k.join('|'))>=0)links.push('<a class="btn" href="'+BASE+k.join('-vs-')+'/">'+esc(rs[a].nome)+' vs '+esc(rs[b].nome)+'</a>');}
if(links.length)h+='<p><b>'+FULL+'</b></p><p class="cmp-links">'+links.join(' ')+'</p>';
out.innerHTML=h;}
sel.forEach(function(x){x.addEventListener('change',run);});run();})();
</script>"""
    elenco_c = '<ul class="lista-link">' + "".join(
        f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>'
        for x, y in sorted(pairs, key=lambda p: (per[p[0]]["marca"], per[p[0]]["nome"]))) + "</ul>"
    cr, ld = crumbs([H(), (C, None)])
    r1, r2 = L("Prima racchetta", "First racket", "Primera pala", "Première raquette"), L("Seconda racchetta", "Second racket", "Segunda pala", "Deuxième raquette")
    r3, r4 = L("Terza racchetta (facoltativa)", "Third racket (optional)", "Tercera pala (opcional)", "Troisième raquette (facultatif)"), L("Quarta racchetta (facoltativa)", "Fourth racket (optional)", "Cuarta pala (opcional)", "Quatrième raquette (facultatif)")
    corpo = f'''{cr}
<div class="intro"><h1>{L("Confronta racchette da padel", "Compare padel rackets", "Compara palas de pádel", "Comparer des raquettes de padel")}</h1><p>{L(f"Scegli da due a quattro racchette e guarda subito dove si differenziano: peso, forma, materiali, livello e prezzo. Sotto trovi i {len(pairs)} confronti più cercati, già spiegati.",
       f"Pick two to four rackets and see at once where they differ: weight, shape, materials, level and price. Below are the {len(pairs)} most searched comparisons, already explained.",
       f"Elige de dos a cuatro palas y mira enseguida en qué se diferencian: peso, forma, materiales, nivel y precio. Debajo tienes las {len(pairs)} comparativas más buscadas, ya explicadas.", f"Choisissez de deux à quatre raquettes et voyez tout de suite ce qui les distingue : poids, forme, matériaux, niveau et prix. Voici les {len(pairs)} comparaisons les plus recherchées, déjà expliquées.")}</p></div>
<form class="cmp-tool" onsubmit="return false"><select id="r1" aria-label="{r1}"><option value="">{r1}</option>{opts}</select>
<select id="r2" aria-label="{r2}"><option value="">{r2}</option>{opts}</select>
<select id="r3" aria-label="{r3}"><option value="">{r3}</option>{opts}</select>
<select id="r4" aria-label="{r4}"><option value="">{r4}</option>{opts}</select></form>
<div id="cmp-out"></div>
<section class="block"><h2>{L("Confronti più cercati", "Most searched comparisons", "Comparativas más buscadas", "Comparaisons les plus recherchées")}</h2>{elenco_c}</section>'''
    path = P("confronta")
    scrivi(path, pagina(L("Confronto racchette padel: metti a confronto fino a 4 modelli | PadelMetrix", "Padel racket comparison: compare up to 4 models side by side | PadelMetrix",
                          "Comparador de palas de pádel: compara hasta 4 modelos | PadelMetrix", "Comparateur de raquettes de padel : jusqu'à 4 modèles côte à côte | PadelMetrix"),
                        L(f"Confronta fino a quattro racchette da padel per peso, forma, materiali, livello e prezzo. {len(pairs)} confronti già spiegati tra i modelli 2026 e 2027.",
                          f"Compare up to four padel rackets by weight, shape, materials, level and price. {len(pairs)} comparisons of 2026 and 2027 models already explained.",
                          f"Compara hasta cuatro palas de pádel por peso, forma, materiales, nivel y precio. {len(pairs)} comparativas ya explicadas entre modelos 2026 y 2027.", f"Comparez jusqu'à quatre raquettes de padel par poids, forme, matériaux, niveau et prix. {len(pairs)} comparaisons de modèles 2026 et 2027 déjà expliquées."),
                        path, corpo, on="confronta", ld=[ld], extra_js=tool_js, alt=ALT("confronta")), ALT("confronta"))


# ---------------------------------------------------------------- Guide

def guida(slug, title, desc, h1, crumb, intro_html, corpo_html, items, on="guide", ld_extra=()):
    path, alt = P("guide", slug), ALT("guide", slug)
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías", "Guides"), P("guide")), (crumb, None)])
    lista = f'<section class="block"><h2>{L("Le racchette del database adatte", "Suitable rackets in the database", "Las palas de la base de datos adecuadas", "Raquettes adaptées dans la base de données")} ({len(items)})</h2>{griglia(ordina(items))}</section>' if items else ""
    corpo = f'''{cr}
<div class="intro"><h1>{e(h1)}</h1>{intro_html}{data_riga(femm=True)}</div>
<div class="prose">{corpo_html}</div>
{lista}'''
    scrivi(path, pagina(title, desc, path, corpo, on=on, ld=[ld, *ld_extra], alt=alt), alt)


def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}


def faq_html(qa):
    return f'<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes", "Questions fréquentes")}</h2><div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</div>"


def guide(db):
    adulti = [n for n in db if n["categoria"] != "junior"]
    G = []
    pg = lambda s: P("guide", s)  # noqa: E731

    # principianti
    items = [n for n in adulti if n["livello"] in ("principiante", "principiante-intermedio")]
    qa = [(L("Che forma deve avere una racchetta da padel per principianti?", "What shape should a beginner padel racket be?", "¿Qué forma debe tener una pala de pádel para principiantes?", "Quelle forme choisir pour une raquette de padel débutant ?"),
           L("Meglio rotonda o a goccia: lo sweet spot è più centrato e la racchetta perdona di più i colpi decentrati.",
             "Round or teardrop is best: the sweet spot is more central and the racket forgives off-centre hits more.",
             "Mejor redonda o de lágrima: el punto dulce está más centrado y la pala perdona más los golpes descentrados.", "Ronde ou goutte d'eau : le sweet spot est plus central et la raquette pardonne davantage les coups décentrés.")),
          (L("Quanto deve pesare la prima racchetta da padel?", "How much should your first padel racket weigh?", "¿Cuánto debe pesar la primera pala de pádel?", "Combien doit peser sa première raquette de padel ?"),
           L("Per un adulto di solito tra 350 e 365 grammi; chi ha poca forza o fastidi al braccio può scendere verso i 340.",
             "For an adult usually between 350 and 365 grams; players with less strength or arm problems can go down towards 340.",
             "Para un adulto normalmente entre 350 y 365 gramos; quien tiene poca fuerza o molestias en el brazo puede bajar hacia los 340.", "Pour un adulte, généralement entre 350 et 365 grammes ; les joueurs moins puissants ou avec des soucis au bras peuvent descendre vers 340.")),
          (L("Meglio fibra di vetro o carbonio per iniziare?", "Is fiberglass or carbon better for starting out?", "¿Mejor fibra de vidrio o carbono para empezar?", "Fibre de verre ou carbone pour débuter ?"),
           L("La fibra di vetro è più morbida ed economica e aiuta a far uscire la palla; il carbonio è più rigido e preciso, adatto quando la tecnica è più solida.",
             "Fiberglass is softer and cheaper and helps the ball come off the face; carbon is stiffer and more precise, suited to players whose technique is more solid.",
             "La fibra de vidrio es más blanda y económica y ayuda a sacar la bola; el carbono es más rígido y preciso, adecuado cuando la técnica es más sólida.", "La fibre de verre est plus souple et moins chère et aide la balle à sortir ; le carbone est plus rigide et plus précis, pour ceux dont la technique est déjà solide."))]
    guida("racchetta-padel-principianti",
          L("Racchetta da padel per principianti: come sceglierla e i modelli 2026 | PadelMetrix", "Padel racket for beginners: how to choose one and the 2026 models | PadelMetrix",
            "Pala de pádel para principiantes: cómo elegirla y los modelos 2026 | PadelMetrix", "Raquette de padel débutant : comment la choisir et les modèles 2026 | PadelMetrix"),
          L("Come scegliere la prima racchetta da padel: forma, peso, materiali e prezzo. Più l'elenco dei modelli 2026 e 2027 adatti a chi inizia.",
            "How to choose your first padel racket: shape, weight, materials and price. Plus the list of 2026 and 2027 models suited to beginners.",
            "Cómo elegir la primera pala de pádel: forma, peso, materiales y precio. Más la lista de modelos 2026 y 2027 adecuados para quien empieza.", "Comment choisir sa première raquette de padel : forme, poids, matériaux et prix. Avec la liste des modèles 2026 et 2027 adaptés aux débutants."),
          L("Racchetta da padel per principianti", "Padel racket for beginners", "Pala de pádel para principiantes", "Raquette de padel pour débutant"), L("Principianti", "Beginners", "Principiantes", "Débutants"),
          L("<p><b>La racchetta giusta per un principiante è rotonda o a goccia, pesa 350–365 g, ha bilanciamento basso o medio e una superficie morbida in fibra di vetro o carbonio leggero; costa in genere 70–150 €.</b> Le racchette da professionisti, rigide e pesanti in testa, rendono l'apprendimento più faticoso.</p>",
            "<p><b>The right racket for a beginner is round or teardrop, weighs 350–365 g, has a low or medium balance and a soft fiberglass or light carbon face; it usually costs €70–150.</b> Pro rackets, stiff and head-heavy, make learning harder.</p>",
            "<p><b>La pala adecuada para un principiante es redonda o de lágrima, pesa 350–365 g, tiene balance bajo o medio y una cara blanda de fibra de vidrio o carbono ligero; suele costar 70–150 €.</b> Las palas de profesionales, rígidas y pesadas en cabeza, hacen el aprendizaje más difícil.</p>", "<p><b>La bonne raquette pour débuter est ronde ou en goutte d'eau, pèse 350–365 g, a un équilibre bas ou moyen et une surface souple en fibre de verre ou en carbone léger ; elle coûte en général 70–150 €.</b> Les raquettes de pro, rigides et lourdes en tête, rendent l'apprentissage plus difficile.</p>"),
          L(f"""<h2>I quattro criteri</h2><ol><li><b>Forma rotonda o a goccia.</b> Lo sweet spot è al centro e più ampio.</li><li><b>Peso 350–365 g.</b> Abbastanza stabile, non affatica il braccio.</li><li><b>Bilanciamento basso o medio.</b> Più maneggevole nelle volée e in difesa.</li><li><b>Fibra di vetro o carbonio morbido.</b> Tatto più confortevole e uscita di palla facile.</li></ol>
<p>Sul prezzo: per iniziare non serve spendere più di 100–150 €. Vedi anche le <a href="{pg('racchette-padel-economiche')}">racchette economiche</a> e le <a href="{pg('forme-racchetta-padel')}">differenze tra le forme</a>.</p>""",
            f"""<h2>The four criteria</h2><ol><li><b>Round or teardrop shape.</b> The sweet spot is central and larger.</li><li><b>Weight 350–365 g.</b> Stable enough, without tiring the arm.</li><li><b>Low or medium balance.</b> Easier to handle on volleys and in defence.</li><li><b>Fiberglass or soft carbon.</b> A more comfortable feel and easy ball output.</li></ol>
<p>On price: to start out you don't need to spend more than €100–150. See also the <a href="{pg('racchette-padel-economiche')}">cheap rackets</a> and the <a href="{pg('forme-racchetta-padel')}">differences between shapes</a>.</p>""",
            f"""<h2>Los cuatro criterios</h2><ol><li><b>Forma redonda o de lágrima.</b> El punto dulce está en el centro y es más amplio.</li><li><b>Peso 350–365 g.</b> Bastante estable, sin cansar el brazo.</li><li><b>Balance bajo o medio.</b> Más manejable en las voleas y en defensa.</li><li><b>Fibra de vidrio o carbono blando.</b> Tacto más cómodo y salida de bola fácil.</li></ol>
<p>Sobre el precio: para empezar no hace falta gastar más de 100–150 €. Mira también las <a href="{pg('racchette-padel-economiche')}">palas baratas</a> y las <a href="{pg('forme-racchetta-padel')}">diferencias entre formas</a>.</p>""", f"""<h2>Les quatre critères</h2><ol><li><b>Forme ronde ou goutte d'eau.</b> Le sweet spot est central et plus grand.</li><li><b>Poids 350–365 g.</b> Assez stable, sans fatiguer le bras.</li><li><b>Équilibre bas ou moyen.</b> Plus maniable à la volée et en défense.</li><li><b>Fibre de verre ou carbone souple.</b> Un toucher plus confortable et une sortie de balle facile.</li></ol>\n<p>Côté prix : pour débuter, inutile de dépenser plus de 100–150 €. Voir aussi les <a href="{pg('racchette-padel-economiche')}">raquettes pas chères</a> et les <a href="{pg('forme-racchetta-padel')}">différences entre les formes</a>.</p>""") + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("racchetta-padel-principianti", L("Racchetta da padel per principianti", "Padel racket for beginners", "Pala de pádel para principiantes", "Raquette de padel pour débutant"), len(items)))

    # gomito
    items = [n for n in adulti if isinstance(n["sensazione"], str) and "morbid" in n["sensazione"].lower()
             and (n["forma"] != "diamante" or any(w in n["nome"].lower() for w in ("comfort", "soft", "cmf")))]
    qa = [(L("Quale racchetta da padel scegliere con l'epicondilite?", "Which padel racket should you choose with tennis elbow?", "¿Qué pala de pádel elegir con epicondilitis?", "Quelle raquette de padel choisir en cas de tennis elbow ?"),
           L("In generale si consigliano racchette dal tatto morbido, non troppo pesanti e con bilanciamento basso o medio, che trasmettono meno vibrazioni al braccio. La scelta va comunque fatta con il proprio medico o fisioterapista.",
             "In general, rackets with a soft feel, not too heavy and with a low or medium balance are recommended, as they transmit less vibration to the arm. The choice should still be made with your doctor or physiotherapist.",
             "En general se recomiendan palas de tacto blando, no demasiado pesadas y con balance bajo o medio, que transmiten menos vibraciones al brazo. En todo caso, la elección debe hacerse con tu médico o fisioterapeuta.", "En général, on conseille des raquettes au toucher souple, pas trop lourdes et avec un équilibre bas ou moyen, qui transmettent moins de vibrations au bras. Le choix doit tout de même se faire avec votre médecin ou kinésithérapeute.")),
          (L("Le racchette a diamante sono sconsigliate per il gomito?", "Are diamond rackets bad for the elbow?", "¿Las palas diamante están desaconsejadas para el codo?", "Les raquettes diamant sont-elles mauvaises pour le coude ?"),
           L("Le diamante rigide e pesanti in testa sollecitano di più l'avambraccio. Esistono versioni Comfort o Soft più morbide, ma per chi ha dolore conviene partire da rotonde o a goccia.",
             "Stiff, head-heavy diamonds put more strain on the forearm. There are softer Comfort or Soft versions, but if you are in pain it is better to start with round or teardrop rackets.",
             "Las diamante rígidas y pesadas en cabeza cargan más el antebrazo. Existen versiones Comfort o Soft más blandas, pero si tienes dolor conviene empezar por redondas o de lágrima.", "Les diamants rigides et lourdes en tête sollicitent davantage l'avant-bras. Il existe des versions plus souples Comfort ou Soft, mais en cas de douleur mieux vaut commencer par des raquettes rondes ou en goutte d'eau.")),
          (L("Il peso conta per il gomito?", "Does weight matter for the elbow?", "¿El peso influye en el codo?", "Le poids compte-t-il pour le coude ?"),
           L("Una racchetta troppo leggera vibra di più, una troppo pesante affatica: di solito si resta nella fascia media, intorno ai 350–365 grammi.",
             "A racket that is too light vibrates more, one that is too heavy tires you: usually it is best to stay in the middle range, around 350–365 grams.",
             "Una pala demasiado ligera vibra más, una demasiado pesada cansa: lo normal es quedarse en la franja media, alrededor de 350–365 gramos.", "Une raquette trop légère vibre davantage, une trop lourde fatigue : il vaut mieux rester dans la moyenne, autour de 350–365 grammes."))]
    guida("racchetta-padel-epicondilite",
          L("Racchetta da padel per epicondilite e gomito del tennista: come sceglierla | PadelMetrix", "Padel racket for tennis elbow: how to choose one | PadelMetrix",
            "Pala de pádel para epicondilitis y codo de tenista: cómo elegirla | PadelMetrix", "Raquette de padel et tennis elbow : comment la choisir | PadelMetrix"),
          L("Racchette da padel per chi soffre di epicondilite: tatto morbido, peso e bilanciamento giusti, e i modelli 2026 e 2027 più confortevoli per il braccio.",
            "Padel rackets for players with tennis elbow: soft feel, the right weight and balance, and the most arm-friendly 2026 and 2027 models.",
            "Palas de pádel para quien sufre epicondilitis: tacto blando, peso y balance adecuados, y los modelos 2026 y 2027 más cómodos para el brazo.", "Raquettes de padel pour les joueurs souffrant de tennis elbow : toucher souple, bon poids et bon équilibre, et les modèles 2026 et 2027 les plus doux pour le bras."),
          L("Racchetta da padel per epicondilite e gomito", "Padel racket for tennis elbow", "Pala de pádel para epicondilitis y codo", "Raquette de padel et tennis elbow"), L("Epicondilite e gomito", "Tennis elbow", "Epicondilitis y codo", "Tennis elbow"),
          L("<p><b>Con l'epicondilite conviene una racchetta dal tatto morbido, di 350–365 g, rotonda o a goccia e con bilanciamento basso o medio, che trasmette meno vibrazioni al braccio.</b> La racchetta non cura il gomito, ma può evitare di peggiorarlo. Questa pagina non sostituisce il parere di un medico o di un fisioterapista.</p>",
            "<p><b>With tennis elbow, choose a soft-feeling racket of 350–365 g, round or teardrop, with a low or medium balance, which transmits less vibration to the arm.</b> A racket won't cure your elbow, but it can avoid making it worse. This page is not a substitute for the advice of a doctor or physiotherapist.</p>",
            "<p><b>Con epicondilitis conviene una pala de tacto blando, de 350–365 g, redonda o de lágrima y con balance bajo o medio, que transmite menos vibraciones al brazo.</b> La pala no cura el codo, pero puede evitar que empeore. Esta página no sustituye la opinión de un médico o un fisioterapeuta.</p>", "<p><b>En cas de tennis elbow, choisissez une raquette au toucher souple de 350–365 g, ronde ou en goutte d'eau, avec un équilibre bas ou moyen, qui transmet moins de vibrations au bras.</b> Une raquette ne soignera pas votre coude, mais elle peut éviter de l'aggraver. Cette page ne remplace pas l'avis d'un médecin ou d'un kinésithérapeute.</p>"),
          L("""<h2>Cosa guardare nella scheda</h2><ul><li><b>Tatto:</b> morbido o medio-morbido. Le gomme EVA soft e le superfici in fibra di vetro assorbono più vibrazioni.</li><li><b>Forma:</b> rotonda o a goccia; le diamante concentrano il peso in testa.</li><li><b>Peso e bilanciamento:</b> 350–365 g, bilanciamento basso o medio.</li><li><b>Versioni Comfort e Soft:</b> molti marchi le propongono accanto al modello rigido, con gli stessi stampi ma materiali più morbidi.</li></ul>
<p>Nell'elenco sotto trovi le racchette del database con tatto dichiarato morbido o medio-morbido.</p>""",
            """<h2>What to look for on the spec page</h2><ul><li><b>Feel:</b> soft or medium-soft. Soft EVA rubbers and fiberglass faces absorb more vibration.</li><li><b>Shape:</b> round or teardrop; diamonds concentrate the weight in the head.</li><li><b>Weight and balance:</b> 350–365 g, low or medium balance.</li><li><b>Comfort and Soft versions:</b> many brands offer them alongside the stiff model, with the same moulds but softer materials.</li></ul>
<p>The list below shows the rackets in the database with a declared soft or medium-soft feel.</p>""",
            """<h2>Qué mirar en la ficha</h2><ul><li><b>Tacto:</b> blando o medio-blando. Las gomas EVA soft y las caras de fibra de vidrio absorben más vibraciones.</li><li><b>Forma:</b> redonda o de lágrima; las diamante concentran el peso en la cabeza.</li><li><b>Peso y balance:</b> 350–365 g, balance bajo o medio.</li><li><b>Versiones Comfort y Soft:</b> muchas marcas las ofrecen junto al modelo rígido, con los mismos moldes pero materiales más blandos.</li></ul>
<p>En la lista de abajo están las palas de la base de datos con tacto declarado blando o medio-blando.</p>""", """<h2>Ce qu'il faut regarder sur la fiche</h2><ul><li><b>Toucher :</b> souple ou mi-souple. Les gommes EVA souples et les surfaces en fibre de verre absorbent davantage les vibrations.</li><li><b>Forme :</b> ronde ou goutte d'eau ; les diamants concentrent le poids dans la tête.</li><li><b>Poids et équilibre :</b> 350–365 g, équilibre bas ou moyen.</li><li><b>Versions Comfort et Soft :</b> de nombreuses marques les proposent à côté du modèle rigide, avec le même moule mais des matériaux plus souples.</li></ul>\n<p>La liste ci-dessous montre les raquettes de la base au toucher déclaré souple ou mi-souple.</p>""") + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("racchetta-padel-epicondilite", L("Racchetta da padel per epicondilite e gomito", "Padel racket for tennis elbow", "Pala de pádel para epicondilitis y codo", "Raquette de padel et tennis elbow"), len(items)))

    # forme
    conta = {f: [n for n in adulti if n["forma"] == f] for f in ("rotonda", "goccia", "diamante", "ibrida")}
    qa = [(L("Meglio una racchetta da padel rotonda o a diamante?", "Is a round or a diamond padel racket better?", "¿Mejor una pala de pádel redonda o diamante?", "Raquette de padel ronde ou diamant : laquelle choisir ?"),
           L("Rotonda se cerchi controllo, tolleranza e gioco da fondo campo; diamante se giochi spesso a rete e vuoi potenza nello smash, con una tecnica già solida.",
             "Round if you want control, forgiveness and baseline play; diamond if you often play at the net and want smash power, with already solid technique.",
             "Redonda si buscas control, tolerancia y juego desde el fondo; diamante si juegas a menudo en la red y quieres potencia en el remate, con una técnica ya sólida.", "Ronde si vous voulez du contrôle, de la tolérance et un jeu de fond de court ; diamant si vous jouez souvent au filet et cherchez de la puissance au smash, avec une technique déjà solide.")),
          (L("Cos'è una racchetta a goccia?", "What is a teardrop racket?", "¿Qué es una pala de lágrima?", "Qu'est-ce qu'une raquette goutte d'eau ?"),
           L("Una forma intermedia: il peso è leggermente spostato verso la testa, per un compromesso tra controllo e potenza. È la scelta più versatile.",
             "An intermediate shape: the weight is shifted slightly towards the head, for a compromise between control and power. It is the most versatile choice.",
             "Una forma intermedia: el peso está algo desplazado hacia la cabeza, para un compromiso entre control y potencia. Es la opción más versátil.", "Une forme intermédiaire : le poids est légèrement déplacé vers la tête, pour un compromis entre contrôle et puissance. C'est le choix le plus polyvalent.")),
          (L("Cosa vuol dire racchetta ibrida?", "What does hybrid racket mean?", "¿Qué significa pala híbrida?", "Que veut dire raquette hybride ?"),
           L("È il nome che molti marchi usano per stampi tra goccia e diamante, o tra goccia e rotonda: il carattere dipende dal modello.",
             "It is the name many brands use for moulds between teardrop and diamond, or between teardrop and round: the character depends on the model.",
             "Es el nombre que muchas marcas usan para moldes entre lágrima y diamante, o entre lágrima y redonda: el carácter depende del modelo.", "C'est le nom que beaucoup de marques donnent aux moules entre goutte d'eau et diamant, ou entre goutte d'eau et ronde : le caractère dépend du modèle."))]
    sez = ""
    testi = {"rotonda": L("Sweet spot centrato e peso verso il manico: la forma del controllo e della difesa, adatta a principianti e a chi costruisce il punto.",
                          "Centred sweet spot and weight towards the handle: the shape of control and defence, suited to beginners and players who build the point.",
                          "Punto dulce centrado y peso hacia el mango: la forma del control y la defensa, adecuada para principiantes y para quien construye el punto.", "Sweet spot centré et poids vers le manche : la forme du contrôle et de la défense, adaptée aux débutants et aux joueurs qui construisent le point."),
             "goccia": L("Peso leggermente in testa e sweet spot un po' più alto: la forma polivalente, buona per la maggior parte dei giocatori.",
                         "Weight slightly towards the head and a slightly higher sweet spot: the all-round shape, good for most players.",
                         "Peso ligeramente en cabeza y punto dulce algo más alto: la forma polivalente, buena para la mayoría de jugadores.", "Poids légèrement vers la tête et sweet spot un peu plus haut : la forme polyvalente, qui convient à la plupart des joueurs."),
             "diamante": L("Testa più larga in alto e bilanciamento alto: la forma dell'attacco, per chi chiude i punti a rete e ha già una buona tecnica.",
                           "Head wider at the top and high balance: the attacking shape, for players who finish points at the net and already have good technique.",
                           "Cabeza más ancha arriba y balance alto: la forma del ataque, para quien cierra los puntos en la red y ya tiene buena técnica.", "Tête plus large en haut et équilibre haut : la forme de l'attaque, pour ceux qui finissent les points au filet et ont déjà une bonne technique."),
             "ibrida": L("Stampi intermedi che ogni marca interpreta a modo suo, di solito tra goccia e diamante.",
                         "Intermediate moulds that each brand interprets in its own way, usually between teardrop and diamond.",
                         "Moldes intermedios que cada marca interpreta a su manera, normalmente entre lágrima y diamante.", "Des moules intermédiaires que chaque marque interprète à sa façon, en général entre goutte d'eau et diamant.")}
    for f, its in conta.items():
        fo = FORMA(f).lower()
        sez += L(f'<h2>Racchette {fo} ({len(its)} nel database)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">Vedi tutte le racchette {fo}</a>.</p>',
                 f'<h2>{FORMA(f)} rackets ({len(its)} in the database)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">See all {fo} rackets</a>.</p>',
                 f'<h2>Palas {fo} ({len(its)} en la base de datos)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">Ver todas las palas {fo}</a>.</p>', f'<h2>Raquettes {FORMA(f).lower()} ({len(its)} dans la base)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">Voir toutes les raquettes de forme {fo}</a>.</p>')
    guida("forme-racchetta-padel",
          L("Racchetta da padel rotonda, a goccia o a diamante: differenze e come scegliere | PadelMetrix", "Round, teardrop or diamond padel racket: differences and how to choose | PadelMetrix",
            "Pala de pádel redonda, lágrima o diamante: diferencias y cómo elegir | PadelMetrix", "Raquette de padel ronde, goutte d'eau ou diamant : différences et comment choisir | PadelMetrix"),
          L("Differenze tra racchetta da padel rotonda, a goccia, a diamante e ibrida: controllo, potenza, sweet spot e quale scegliere per il tuo livello.",
            "Differences between round, teardrop, diamond and hybrid padel rackets: control, power, sweet spot and which to choose for your level.",
            "Diferencias entre pala de pádel redonda, de lágrima, diamante e híbrida: control, potencia, punto dulce y cuál elegir según tu nivel.", "Différences entre raquettes de padel rondes, goutte d'eau, diamant et hybrides : contrôle, puissance, sweet spot et laquelle choisir selon votre niveau."),
          L("Racchetta rotonda, a goccia o a diamante?", "Round, teardrop or diamond racket?", "¿Pala redonda, de lágrima o diamante?", "Raquette ronde, goutte d'eau ou diamant ?"), L("Forme delle racchette", "Racket shapes", "Formas de las palas", "Formes de raquette"),
          L("<p><b>La racchetta rotonda dà controllo e tolleranza, quella a diamante potenza nello smash, quella a goccia sta in mezzo ed è la più versatile.</b> La forma decide dove sta lo sweet spot e come è distribuito il peso, e quindi il carattere della racchetta.</p>",
            "<p><b>A round racket gives control and forgiveness, a diamond gives smash power, and a teardrop sits in between and is the most versatile.</b> The shape decides where the sweet spot is and how the weight is distributed, and therefore the racket's character.</p>",
            "<p><b>La pala redonda da control y tolerancia, la diamante potencia en el remate y la de lágrima está en medio y es la más versátil.</b> La forma decide dónde está el punto dulce y cómo se reparte el peso, y por tanto el carácter de la pala.</p>", "<p><b>Une raquette ronde apporte contrôle et tolérance, une diamant donne de la puissance au smash, et une goutte d'eau se place entre les deux : c'est la plus polyvalente.</b> La forme détermine où se trouve le sweet spot et comment le poids est réparti, donc le caractère de la raquette.</p>"),
          sez + faq_html(qa), [], ld_extra=[faq_ld(qa)])
    G.append(("forme-racchetta-padel", L("Racchetta rotonda, a goccia o a diamante?", "Round, teardrop or diamond racket?", "¿Pala redonda, de lágrima o diamante?", "Raquette ronde, goutte d'eau ou diamant ?"), None))

    # donna
    items = [n for n in adulti if n["donna"]]
    guida("racchette-padel-donna",
          L("Racchette da padel da donna 2026 e 2027: i modelli femminili | PadelMetrix", "Women's padel rackets 2026 and 2027: the women's models | PadelMetrix",
            "Palas de pádel de mujer 2026 y 2027: los modelos femeninos | PadelMetrix", "Raquettes de padel femme 2026 et 2027 : les modèles féminins | PadelMetrix"),
          L("Le racchette da padel da donna delle collezioni 2026 e 2027: modelli delle giocatrici professioniste, pesi, forme e livelli.",
            "Women's padel rackets from the 2026 and 2027 collections: pro players' models, weights, shapes and levels.",
            "Las palas de pádel de mujer de las colecciones 2026 y 2027: modelos de las jugadoras profesionales, pesos, formas y niveles.", "Raquettes de padel femme des collections 2026 et 2027 : modèles des joueuses professionnelles, poids, formes et niveaux."),
          L("Racchette da padel da donna", "Women's padel rackets", "Palas de pádel de mujer", "Raquettes de padel femme"), L("Racchette da donna", "Women's rackets", "Palas de mujer", "Raquettes femme"),
          L("<p>Le racchette femminili sono in genere più leggere (spesso 340–360 g) e più maneggevoli, ma non sono obbligatorie: conta il peso che riesci a gestire senza affaticare il braccio. Qui trovi i modelli che i marchi presentano come femminili, molti firmati da giocatrici professioniste.</p>",
            "<p>Women's rackets are generally lighter (often 340–360 g) and easier to handle, but they are not compulsory: what matters is the weight you can manage without tiring your arm. Here are the models the brands present as women's rackets, many signed by professional players.</p>",
            "<p>Las palas femeninas suelen ser más ligeras (a menudo 340–360 g) y manejables, pero no son obligatorias: lo que cuenta es el peso que puedes manejar sin cansar el brazo. Aquí están los modelos que las marcas presentan como femeninos, muchos firmados por jugadoras profesionales.</p>", "<p>Les raquettes femme sont en général plus légères (souvent 340–360 g) et plus maniables, mais elles ne sont pas obligatoires : ce qui compte, c'est le poids que vous pouvez manier sans fatiguer le bras. Voici les modèles que les marques présentent comme féminins, beaucoup signés par des joueuses professionnelles.</p>"),
          L(f"<p>Se cerchi una racchetta leggera senza limitarti ai modelli femminili, usa il filtro per livello e forma nella <a href=\"{P('racchette')}\">pagina Racchette</a>.</p>",
            f"<p>If you want a light racket without limiting yourself to women's models, use the level and shape filters on the <a href=\"{P('racchette')}\">Rackets page</a>.</p>",
            f"<p>Si buscas una pala ligera sin limitarte a los modelos femeninos, usa el filtro por nivel y forma en la <a href=\"{P('racchette')}\">página Palas</a>.</p>", f"<p>Si vous voulez une raquette légère sans vous limiter aux modèles femme, utilisez les filtres de niveau et de forme de la <a href=\"{P('racchette')}\">page Raquettes</a>.</p>"), items)
    G.append(("racchette-padel-donna", L("Racchette da padel da donna", "Women's padel rackets", "Palas de pádel de mujer", "Raquettes de padel femme"), len(items)))

    # economiche
    items = [n for n in adulti if n["prezzo"] and n["prezzo"] <= 130]
    guida("racchette-padel-economiche",
          L("Racchette da padel economiche sotto 130 euro: modelli 2026 e 2027 | PadelMetrix", "Cheap padel rackets under €130: 2026 and 2027 models | PadelMetrix",
            "Palas de pádel baratas por menos de 130 euros: modelos 2026 y 2027 | PadelMetrix", "Raquettes de padel pas chères à moins de 130 € : modèles 2026 et 2027 | PadelMetrix"),
          L("Racchette da padel economiche con prezzo di listino fino a 130 euro: modelli per principianti e intermedi delle marche principali.",
            "Cheap padel rackets with a list price up to €130: models for beginners and intermediates from the main brands.",
            "Palas de pádel baratas con precio de lista de hasta 130 euros: modelos para principiantes e intermedios de las principales marcas.", "Raquettes de padel pas chères avec un prix public jusqu'à 130 € : modèles pour débutants et intermédiaires des principales marques."),
          L("Racchette da padel economiche (fino a 130 € di listino)", "Cheap padel rackets (list price up to €130)", "Palas de pádel baratas (hasta 130 € de precio de lista)", "Raquettes de padel pas chères (prix public jusqu'à 130 €)"),
          L("Racchette economiche", "Cheap rackets", "Palas baratas", "Raquettes pas chères"),
          L("<p>Il prezzo di listino è solo un riferimento: online molte racchette costano il 20–40% in meno, quindi anche modelli con listino più alto possono rientrare nel tuo budget. Qui trovi quelle con listino fino a 130 €.</p>",
            "<p>The list price is only a reference: online, many rackets cost 20–40% less, so models with a higher list price may also fit your budget. Here are those with a list price up to €130.</p>",
            "<p>El precio de lista es solo una referencia: online muchas palas cuestan un 20–40% menos, así que también modelos con precio de lista más alto pueden entrar en tu presupuesto. Aquí están las de hasta 130 € de lista.</p>", "<p>Le prix public n'est qu'une référence : en ligne, beaucoup de raquettes coûtent 20 à 40 % de moins, donc des modèles au prix public plus élevé peuvent aussi entrer dans votre budget. Voici ceux dont le prix public va jusqu'à 130 €.</p>"),
          L(f"<p>A questo prezzo prevalgono superfici in fibra di vetro e forme rotonde o a goccia: ottime per iniziare e per giocare con regolarità. Vedi anche la <a href=\"{pg('racchetta-padel-principianti')}\">guida per principianti</a>.</p>",
            f"<p>At this price fiberglass faces and round or teardrop shapes dominate: great for starting out and playing regularly. See also the <a href=\"{pg('racchetta-padel-principianti')}\">beginner's guide</a>.</p>",
            f"<p>A este precio predominan las caras de fibra de vidrio y las formas redondas o de lágrima: perfectas para empezar y jugar con regularidad. Mira también la <a href=\"{pg('racchetta-padel-principianti')}\">guía para principiantes</a>.</p>", f"<p>À ce prix dominent les surfaces en fibre de verre et les formes rondes ou goutte d'eau : idéal pour débuter et jouer régulièrement. Voir aussi le <a href=\"{pg('racchetta-padel-principianti')}\">guide pour débutants</a>.</p>"), items)
    G.append(("racchette-padel-economiche", L("Racchette da padel economiche", "Cheap padel rackets", "Palas de pádel baratas", "Raquettes de padel pas chères"), len(items)))

    # controllo / potenza
    for st, slug, h1, txt in (("controllo", "racchette-padel-controllo", L("Racchette da padel di controllo", "Control padel rackets", "Palas de pádel de control", "Raquettes de padel de contrôle"),
                               L("Le racchette di controllo privilegiano precisione, sweet spot ampio e maneggevolezza. Di solito sono rotonde o a goccia con bilanciamento basso: ideali per chi gioca da fondo campo e costruisce il punto.",
                                 "Control rackets prioritise precision, a large sweet spot and maneuverability. They are usually round or teardrop with a low balance: ideal for players who play from the back and build the point.",
                                 "Las palas de control priorizan la precisión, un punto dulce amplio y la manejabilidad. Suelen ser redondas o de lágrima con balance bajo: ideales para quien juega desde el fondo y construye el punto.", "Les raquettes de contrôle privilégient la précision, un grand sweet spot et la maniabilité. Elles sont en général rondes ou en goutte d'eau avec un équilibre bas : idéales pour ceux qui jouent du fond et construisent le point.")),
                              ("offensivo", "racchette-padel-potenza", L("Racchette da padel di potenza", "Power padel rackets", "Palas de pádel de potencia", "Raquettes de padel de puissance"),
                               L("Le racchette di potenza hanno il peso spostato in testa e una superficie più rigida: aiutano a chiudere i punti con smash e volée, ma chiedono tecnica e sono meno tolleranti in difesa.",
                                 "Power rackets have the weight shifted towards the head and a stiffer face: they help finish points with smashes and volleys, but demand technique and are less forgiving in defence.",
                                 "Las palas de potencia tienen el peso desplazado hacia la cabeza y una cara más rígida: ayudan a cerrar los puntos con remates y voleas, pero exigen técnica y son menos tolerantes en defensa.", "Les raquettes de puissance ont le poids déplacé vers la tête et une surface plus rigide : elles aident à conclure les points au smash et à la volée, mais demandent de la technique et pardonnent moins en défense."))):
        items = [n for n in adulti if n["stile"] == st]
        guida(slug, L(f"{h1} 2026 e 2027: come sceglierle e i modelli | PadelMetrix", f"{h1} 2026 and 2027: how to choose and the models | PadelMetrix", f"{h1} 2026 y 2027: cómo elegirlas y los modelos | PadelMetrix", f"{h1} 2026 et 2027 : comment choisir et les modèles | PadelMetrix"),
              L(f"{h1}: caratteristiche, a chi sono adatte e tutti i modelli 2026 e 2027 nel database PadelMetrix.", f"{h1}: features, who they suit and all the 2026 and 2027 models in the PadelMetrix database.",
                f"{h1}: características, para quién son y todos los modelos 2026 y 2027 de la base de datos PadelMetrix.", f"{h1} : caractéristiques, à qui elles conviennent et tous les modèles 2026 et 2027 de la base PadelMetrix."),
              h1, h1, f"<p>{txt}</p>",
              L(f'<p>Non sai quale stile fa per te? Leggi la guida alle <a href="{pg("forme-racchetta-padel")}">forme delle racchette</a>.</p>',
                f'<p>Not sure which style suits you? Read the guide to <a href="{pg("forme-racchetta-padel")}">racket shapes</a>.</p>',
                f'<p>¿No sabes qué estilo es para ti? Lee la guía de las <a href="{pg("forme-racchetta-padel")}">formas de las palas</a>.</p>', f'<p>Vous ne savez pas quel style vous convient ? Lisez le guide des <a href="{pg("forme-racchetta-padel")}">formes de raquette</a>.</p>'), items)
        G.append((slug, h1, len(items)))

    # giocatori
    gioc = {}
    for n in db:
        g = n["giocatore"]
        if g and "ispirata" not in g:
            gioc.setdefault(g, []).append(n)
    righe = "".join(f'<tr><td>{e(g)}</td><td>{", ".join(f"<a href=\"{url_r(n)}\">{e(n["titolo"])}</a>" for n in ordina(its))}</td></tr>'
                    for g, its in sorted(gioc.items(), key=lambda kv: kv[0]))
    slug = "racchette-giocatori-professionisti"
    t_pro = L("Le racchette dei giocatori professionisti", "The rackets of professional players", "Las palas de los jugadores profesionales", "Les raquettes des joueurs professionnels")
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías", "Guides"), P("guide")), (L("Racchette dei professionisti", "Pro players' rackets", "Palas de los profesionales", "Raquettes des joueurs pro"), None)])
    corpo = f'''{cr}<div class="intro"><h1>{t_pro}</h1><p>{L("Con che racchetta giocano Tapia, Coello, Galán, Lebrón, Chingotto e gli altri: i modelli firmati dai professionisti nelle collezioni 2026 e 2027. Le versioni in vendita sono quelle dei negozi; i professionisti possono usare racchette personalizzate.",
       "Which racket Tapia, Coello, Galán, Lebrón, Chingotto and the others play with: the models signed by professionals in the 2026 and 2027 collections. The versions on sale are the shop versions; professionals may use customised rackets.",
       "Con qué pala juegan Tapia, Coello, Galán, Lebrón, Chingotto y los demás: los modelos firmados por los profesionales en las colecciones 2026 y 2027. Las versiones a la venta son las de las tiendas; los profesionales pueden usar palas personalizadas.", "Avec quelle raquette jouent Tapia, Coello, Galán, Lebrón, Chingotto et les autres : les modèles signés par les professionnels dans les collections 2026 et 2027. Les versions en vente sont celles des boutiques ; les professionnels peuvent utiliser des raquettes personnalisées.")}</p></div>
<div class="tablebox"><table class="tab"><thead><tr><th>{L("Giocatore", "Player", "Jugador", "Joueur")}</th><th>{L("Racchetta", "Racket", "Pala", "Raquette")}</th></tr></thead><tbody>{righe}</tbody></table></div>'''
    path, alt = P("guide", slug), ALT("guide", slug)
    scrivi(path, pagina(L("Con che racchetta giocano i professionisti del padel? Modelli 2026 e 2027 | PadelMetrix", "What rackets do padel pros use? 2026 and 2027 models | PadelMetrix",
                          "¿Con qué pala juegan los profesionales del pádel? Modelos 2026 y 2027 | PadelMetrix", "Quelles raquettes utilisent les pros du padel ? Modèles 2026 et 2027 | PadelMetrix"),
                        L("Le racchette firmate dai giocatori professionisti di padel: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto e altri.",
                          "The rackets signed by professional padel players: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto and others.",
                          "Las palas firmadas por los jugadores profesionales de pádel: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto y otros.", "Les raquettes signées par les joueurs professionnels de padel : Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto et d'autres."),
                        path, corpo, on="guide", ld=[ld], alt=alt), alt)
    G.append((slug, t_pro, None))

    # hub guide
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías", "Guides"), None)])
    n_r = L("racchette", "rackets", "palas", "raquettes")
    voci = "".join(f'<li><a href="{pg(s)}">{e(t)}</a>{f" · {c} {n_r}" if c else ""}</li>' for s, t, c in G)
    corpo = f'''{cr}<div class="intro"><h1>{L("Guide alla scelta della racchetta da padel", "Guides to choosing a padel racket", "Guías para elegir pala de pádel", "Guides pour choisir une raquette de padel")}</h1><p>{L("Guide pratiche per trovare la racchetta giusta in base a livello, stile di gioco, budget e problemi fisici. Ogni guida rimanda alle schede dei modelli adatti.",
       "Practical guides to finding the right racket for your level, playing style, budget and physical issues. Each guide links to the pages of suitable models.",
       "Guías prácticas para encontrar la pala adecuada según tu nivel, estilo de juego, presupuesto y problemas físicos. Cada guía enlaza a las fichas de los modelos adecuados.", "Des guides pratiques pour trouver la bonne raquette selon votre niveau, votre style de jeu, votre budget et vos soucis physiques. Chaque guide renvoie aux fiches des modèles adaptés.")}</p></div>
<ul class="lista-link">{voci}<li><a href="{P("bambini")}">{L("Racchette da padel per bambini e ragazzi", "Padel rackets for kids and teenagers", "Palas de pádel para niños y jóvenes", "Raquettes de padel pour enfants et ados")}</a></li></ul>'''
    path = P("guide")
    scrivi(path, pagina(L("Guide alla scelta della racchetta da padel | PadelMetrix", "Padel racket buying guides | PadelMetrix", "Guías para elegir pala de pádel | PadelMetrix", "Guides d'achat de raquettes de padel | PadelMetrix"),
                        L("Come scegliere la racchetta da padel: guide per principianti, epicondilite, forme, donne, bambini, budget e racchette dei professionisti.",
                          "How to choose a padel racket: guides for beginners, tennis elbow, shapes, women, kids, budget and pro players' rackets.",
                          "Cómo elegir pala de pádel: guías para principiantes, epicondilitis, formas, mujeres, niños, presupuesto y palas de los profesionales.", "Comment choisir une raquette de padel : guides pour débutants, tennis elbow, formes, femmes, enfants, budget et raquettes des joueurs pro."),
                        path, corpo, on="guide", ld=[ld], alt=ALT("guide")), ALT("guide"))


# ---------------------------------------------------------------- Bambini

def bambini(db):
    items = [n for n in db if n["categoria"] == "junior"]
    qa = [(L("Che racchetta da padel per un bambino di 8 anni?", "What padel racket for an 8-year-old?", "¿Qué pala de pádel para un niño de 8 años?", "Quelle raquette de padel pour un enfant de 8 ans ?"),
           L("Indicativamente una racchetta junior rotonda tra 280 e 310 grammi, più corta di quella da adulto. Conta più l'altezza del bambino che l'età.",
             "Roughly a round junior racket between 280 and 310 grams, shorter than an adult one. The child's height matters more than their age.",
             "Orientativamente una pala junior redonda de entre 280 y 310 gramos, más corta que la de adulto. Cuenta más la altura del niño que la edad.", "En gros, une raquette junior ronde entre 280 et 310 grammes, plus courte qu'une raquette adulte. La taille de l'enfant compte plus que son âge.")),
          (L("Da che età si passa alla racchetta da adulto?", "At what age do you move to an adult racket?", "¿A qué edad se pasa a la pala de adulto?", "À quel âge passer à une raquette adulte ?"),
           L("In genere verso i 13–15 anni, quando il ragazzo gestisce 330–360 grammi senza fatica; prima conviene restare su modelli junior o adulti molto leggeri.",
             "Usually around 13–15, when the child can handle 330–360 grams without strain; before that it is better to stick to junior or very light adult models.",
             "Normalmente hacia los 13–15 años, cuando el chico maneja 330–360 gramos sin esfuerzo; antes conviene seguir con modelos junior o de adulto muy ligeros.", "Généralement vers 13–15 ans, quand l'enfant peut manier 330–360 grammes sans effort ; avant, mieux vaut rester sur des modèles junior ou des adultes très légers.")),
          (L("Meglio una racchetta junior o una da adulto leggera?", "Junior racket or light adult racket?", "¿Mejor una pala junior o una de adulto ligera?", "Raquette junior ou raquette adulte légère ?"),
           L("Sotto i 12 anni una junior: è più corta e leggera. Dopo, una racchetta da adulto leggera (340–355 g) è spesso la scelta migliore.",
             "Under 12, a junior: it is shorter and lighter. After that, a light adult racket (340–355 g) is often the best choice.",
             "Por debajo de los 12 años, una junior: es más corta y ligera. Después, una pala de adulto ligera (340–355 g) suele ser la mejor opción.", "Avant 12 ans, une junior : elle est plus courte et plus légère. Ensuite, une raquette adulte légère (340–355 g) est souvent le meilleur choix."))]
    rows = [(L("4–6 anni", "4–6 years", "4–6 años", "4–6 ans"), L("sotto 1,10 m", "under 1.10 m", "menos de 1,10 m", "moins de 1,10 m"), L("sotto 280 g", "under 280 g", "menos de 280 g", "moins de 280 g"), L("Rotonda", "Round", "Redonda", "Ronde")),
            (L("7–9 anni", "7–9 years", "7–9 años", "7–9 ans"), L("1,10–1,35 m", "1.10–1.35 m", "1,10–1,35 m", "1,10–1,35 m"), "280–310 g", L("Rotonda", "Round", "Redonda", "Ronde")),
            (L("10–12 anni", "10–12 years", "10–12 años", "10–12 ans"), L("1,35–1,55 m", "1.35–1.55 m", "1,35–1,55 m", "1,35–1,55 m"), "310–340 g", L("Rotonda o goccia", "Round or teardrop", "Redonda o lágrima", "Ronde ou goutte d'eau")),
            (L("13–15 anni", "13–15 years", "13–15 años", "13–15 ans"), L("oltre 1,55 m", "over 1.55 m", "más de 1,55 m", "plus de 1,55 m"), "330–360 g", L("Rotonda o goccia", "Round or teardrop", "Redonda o lágrima", "Ronde ou goutte d'eau")),
            (L("16 anni e oltre", "16 and over", "16 años o más", "16 ans et plus"), L("adulto", "adult", "adulto", "adulte"), L("come un adulto", "as an adult", "como un adulto", "comme un adulte"), L("come un adulto", "as an adult", "como un adulto", "comme un adulte"))]
    tab = (f'<table class="tab"><thead><tr><th>{L("Età indicativa", "Approx. age", "Edad orientativa", "Âge indicatif")}</th><th>{L("Altezza", "Height", "Altura", "Taille")}</th><th>{L("Peso consigliato", "Recommended weight", "Peso recomendado", "Poids conseillé")}</th><th>{L("Forma", "Shape", "Forma", "Forme")}</th></tr></thead><tbody>\n'
           + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows) + "</tbody></table>")
    cr, ld = crumbs([H(), (L("Bambini", "Kids", "Niños", "Enfants"), None)])
    corpo = f'''{cr}
<div class="intro"><h1>{L("Racchette da padel per bambini e ragazzi", "Padel rackets for kids and teenagers", "Palas de pádel para niños y jóvenes", "Raquettes de padel pour enfants et ados")}</h1><p>{L("Una racchetta troppo pesante rovina la tecnica e affatica il braccio: per i più piccoli servono modelli junior, più corti e leggeri. Ecco come scegliere la misura giusta e i modelli junior in commercio, dalle collezioni più recenti a quelle precedenti ancora in vendita.",
       "A racket that is too heavy ruins technique and tires the arm: young children need junior models, shorter and lighter. Here is how to choose the right size, plus the junior models on sale, from the latest collections to earlier ones still in shops.",
       "Una pala demasiado pesada estropea la técnica y cansa el brazo: los más pequeños necesitan modelos junior, más cortos y ligeros. Así se elige la medida adecuada, y estos son los modelos junior a la venta, desde las colecciones más recientes hasta las anteriores que siguen en tienda.", "Une raquette trop lourde gâche la technique et fatigue le bras : les jeunes enfants ont besoin de modèles junior, plus courts et plus légers. Voici comment choisir la bonne taille, avec les modèles junior en vente, des collections les plus récentes aux précédentes encore en magasin.")}</p></div>
<div class="prose"><h2>{L("Che misura scegliere", "Which size to choose", "Qué medida elegir", "Quelle taille choisir")}</h2><div class="tablebox">{tab}</div>
<p class="note">{L("Indicazioni orientative tratte dalla", "Indicative guidance from", "Indicaciones orientativas tomadas de la", "Indications tirées du")} <a href="https://padelshop.com/en-it/collections/padel-racket-kids" rel="nofollow noopener" target="_blank">{L("guida taglie di Padelshop", "Padelshop's size guide", "guía de tallas de Padelshop", "guide des tailles de Padelshop")}</a>{L("; l'altezza conta più dell'età.", "; height matters more than age.", "; la altura cuenta más que la edad.", " ; la taille compte plus que l'âge.")}</p>
{faq_html(qa)}</div>
<section class="block"><h2>{L("Racchette junior nel database", "Junior rackets in the database", "Palas junior en la base de datos", "Raquettes junior dans la base")} ({len(items)})</h2>{griglia(ordina(items))}
<p class="note">{L(f"Per i ragazzi che passano alla racchetta da adulto vedi la <a href=\"{P('guide', 'racchetta-padel-principianti')}\">guida per principianti</a> e le <a href=\"{P('guide', 'racchette-padel-donna')}\">racchette leggere femminili</a>.",
                   f"For teenagers moving to an adult racket see the <a href=\"{P('guide', 'racchetta-padel-principianti')}\">beginner's guide</a> and the <a href=\"{P('guide', 'racchette-padel-donna')}\">light women's rackets</a>.",
                   f"Para los chicos que pasan a la pala de adulto mira la <a href=\"{P('guide', 'racchetta-padel-principianti')}\">guía para principiantes</a> y las <a href=\"{P('guide', 'racchette-padel-donna')}\">palas ligeras femeninas</a>.", f"Pour les ados qui passent à une raquette adulte, voir le <a href=\"{P('guide', 'racchetta-padel-principianti')}\">guide pour débutants</a> et les <a href=\"{P('guide', 'racchette-padel-donna')}\">raquettes femme légères</a>.")}</p></section>'''
    path = P("bambini")
    scrivi(path, pagina(L("Racchetta da padel per bambini: quale scegliere in base all'età | PadelMetrix", "Padel racket for kids: which one to choose by age | PadelMetrix",
                          "Pala de pádel para niños: cuál elegir según la edad | PadelMetrix", "Raquette de padel enfant : laquelle choisir selon l'âge | PadelMetrix"),
                        L("Come scegliere la racchetta da padel per bambini e ragazzi: peso e misura per età e altezza, e i modelli junior 2026 e 2027.",
                          "How to choose a padel racket for kids and teenagers: weight and size by age and height, plus the 2026 and 2027 junior models.",
                          "Cómo elegir la pala de pádel para niños y jóvenes: peso y medida según edad y altura, y los modelos junior 2026 y 2027.", "Comment choisir une raquette de padel pour enfants et ados : poids et taille selon l'âge et la taille, avec les modèles junior 2026 et 2027."),
                        path, corpo, on="bambini", ld=[ld, faq_ld(qa)], alt=ALT("bambini")), ALT("bambini"))


def main():
    db = carica()
    pairs = coppie(db)
    for l in LINGUE:
        set_lang(l)
        elenco(db)
        marche(db, pairs)
        confronti(db, pairs)
        guide(db)
        bambini(db)
    set_lang("it")
    (ROOT / "scripts" / "pagine_sezioni.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine di sezione generate")
    for l in ("en", "es"):
        if T.MANCANTI[l]:
            print("non tradotti", l, len(T.MANCANTI[l]), sorted(T.MANCANTI[l])[:20])


if __name__ == "__main__":
    main()
