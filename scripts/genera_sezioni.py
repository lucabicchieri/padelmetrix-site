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
    uno, piu = L("racchetta", "racket", "pala"), L("racchette", "rackets", "palas")
    return """<script>
(function(){
var q=new URLSearchParams(location.search);var f=document.getElementById('filtri');if(!f)return;
var cards=[].slice.call(document.querySelectorAll('.rgrid .rcard'));var out=document.getElementById('conta');
['marca','forma','livello','stile','cat','prezzo','q'].forEach(function(k){var el=f.elements[k];if(el&&q.get(k))el.value=q.get(k);});
function run(){var v={};['marca','forma','livello','stile','cat','prezzo','q'].forEach(function(k){v[k]=(f.elements[k].value||'').toLowerCase();});
var n=0;cards.forEach(function(c){var d=c.dataset,ok=true;
if(v.marca&&d.marca!==v.marca)ok=false;if(v.forma&&d.forma!==v.forma)ok=false;if(v.livello&&d.livello!==v.livello)ok=false;
if(v.stile&&d.stile!==v.stile)ok=false;if(v.cat&&d.cat!==v.cat)ok=false;
if(v.prezzo&&(!d.prezzo||parseFloat(d.prezzo)>parseFloat(v.prezzo)))ok=false;if(v.q&&d.nome.indexOf(v.q)<0)ok=false;
c.style.display=ok?'':'none';if(ok)n++;});out.textContent=n+(n===1?' %s':' %s');}
f.addEventListener('input',run);f.addEventListener('change',run);run();})();
</script>""" % (uno, piu)


def opt(vals, sel_label):
    return f'<option value="">{sel_label}</option>' + "".join(f'<option value="{v}">{e(l)}</option>' for v, l in vals)


def elenco(db):
    marche = sorted({(n["marca_slug"], n["marca"]) for n in db}, key=lambda x: x[1].lower())
    tutte, tutti = L("Tutte", "All", "Todas"), L("Tutti", "All", "Todos")
    prezzi = [(str(x), L(f"fino a {x} €", f"up to €{x}", f"hasta {x} €")) for x in (100, 150, 200, 300)]
    form = f'''<form class="filtri" id="filtri" onsubmit="return false">
<label>{L("Cerca", "Search", "Buscar")}<input name="q" type="search" placeholder="{L("Modello o giocatore", "Model or player", "Modelo o jugador")}"></label>
<label>{L("Marca", "Brand", "Marca")}<select name="marca">{opt(marche, tutte)}</select></label>
<label>{L("Forma", "Shape", "Forma")}<select name="forma">{opt(list(S.forme_d().items()), tutte)}</select></label>
<label>{L("Livello", "Level", "Nivel")}<select name="livello">{opt([(k, LIVN(k)) for k in LIV], tutti)}</select></label>
<label>{L("Stile", "Style", "Estilo")}<select name="stile">{opt(list(S.stili_d().items()), tutti)}</select></label>
<label>{L("Per chi", "For", "Para quién")}<select name="cat">{opt([("adulto", L("Adulto", "Adult", "Adulto")), ("donna", L("Modelli femminili", "Women's models", "Modelos femeninos")), ("junior", "Junior")], tutti)}</select></label>
<label>{L("Prezzo di listino", "List price", "Precio de lista")}<select name="prezzo">{opt(prezzi, L("Qualsiasi", "Any", "Cualquiera"))}</select></label>
</form>'''
    cr, ld = crumbs([H(), (L("Racchette", "Rackets", "Palas"), None)])
    nm = len(marche)
    corpo = f'''{cr}
<div class="intro"><h1>{L("Racchette da padel 2026 e 2027", "Padel rackets 2026 and 2027", "Palas de pádel 2026 y 2027")}</h1>
<p>{L(f"{len(db)} racchette di {nm} marche con dati tecnici, sintesi delle recensioni e modelli simili. Filtra per marca, forma, livello, stile e prezzo, oppure leggi le <a href=\"{P('guide')}\">guide alla scelta</a>.",
      f"{len(db)} rackets from {nm} brands with specs, review summaries and similar models. Filter by brand, shape, level, style and price, or read the <a href=\"{P('guide')}\">buying guides</a>.",
      f"{len(db)} palas de {nm} marcas con datos técnicos, resumen de reseñas y modelos similares. Filtra por marca, forma, nivel, estilo y precio, o lee las <a href=\"{P('guide')}\">guías de compra</a>.")}</p></div>
<div class="marche">{"".join(f'<a href="{P("marche", s)}">{e(m)}</a>' for s, m in marche)}</div>
{form}
<p class="conta" id="conta">{len(db)} {L("racchette", "rackets", "palas")}</p>
{griglia(ordina(db))}'''
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "numberOfItems": len(db),
                "itemListElement": [{"@type": "ListItem", "position": i, "url": SITO + url_r(n), "name": n["titolo"]} for i, n in enumerate(ordina(db), 1)]}
    path = P("racchette")
    scrivi(path, pagina(L("Racchette da padel 2026 e 2027: schede tecniche, confronti e filtri | PadelMetrix",
                          "Padel rackets 2026 and 2027: specs, comparisons and filters | PadelMetrix",
                          "Palas de pádel 2026 y 2027: fichas técnicas, comparativas y filtros | PadelMetrix"),
                        L(f"{len(db)} racchette da padel di {nm} marche: dati tecnici, opinioni e modelli simili. Filtra per livello, forma, peso, prezzo e marca.",
                          f"{len(db)} padel rackets from {nm} brands: specs, reviews and similar models. Filter by level, shape, weight, price and brand.",
                          f"{len(db)} palas de pádel de {nm} marcas: datos técnicos, opiniones y modelos similares. Filtra por nivel, forma, peso, precio y marca."),
                        path, corpo, on="racchette", ld=[ld, itemlist], extra_js=filtri_js(), alt=ALT("racchette")), ALT("racchette"))


# ---------------------------------------------------------------- Marche

def e_(a):
    return L(" e ", " and ", " y ").join(str(x) for x in a)


def marche(db, pairs):
    per_marca = {}
    for n in db:
        per_marca.setdefault((n["marca_slug"], n["marca"]), []).append(n)
    per = {n["slug"]: n for n in db}
    voci = []
    R = L("Racchette", "Rackets", "Palas")
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
            sezioni += f'<section class="block"><h2>{L(f"Racchette {e(m)} {a}", f"{e(m)} rackets {a}", f"Palas {e(m)} {a}")}</h2>{griglia(sub)}</section>'
        mp = [(x, y) for x, y in pairs if per[x]["marca"] == m or per[y]["marca"] == m]
        conf = ""
        if mp:
            conf = f'<section class="block"><h2>{L("Confronti con racchette " + e(m), "Comparisons with " + e(m) + " rackets", "Comparativas con palas " + e(m))}</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>' for x, y in mp) + "</ul></section>"
        cr, ld = crumbs([H(), (R, P("racchette")), (m, None)])
        intro = L(f"Nel database ci sono {len(items)} racchette {m} delle collezioni {anni_txt}",
                  f"The database holds {len(items)} {m} rackets from the {anni_txt} collections",
                  f"En la base de datos hay {len(items)} palas {m} de las colecciones {anni_txt}")
        intro += f": {forme_txt}." if forme_txt else "."
        if gioc:
            intro += L(" Tra i modelli dei giocatori professionisti: ", " Pro player models include: ", " Entre los modelos de jugadores profesionales: ") + ", ".join(gioc[:6]) + "."
        if junior:
            intro += " " + (L(f"{len(junior)} è un modello junior.", f"{len(junior)} is a junior model.", f"{len(junior)} es un modelo junior.") if len(junior) == 1
                            else L(f"{len(junior)} sono modelli junior.", f"{len(junior)} are junior models.", f"{len(junior)} son modelos junior."))
        h1 = L(f"Racchette {e(m)} {anni_txt}", f"{e(m)} padel rackets {anni_txt}", f"Palas {e(m)} {anni_txt}")
        corpo = f'''{cr}
<div class="intro"><h1>{h1}</h1><p>{e(intro)} {L("Ogni scheda riporta dati tecnici, a chi è adatta e le alternative più vicine.", "Each page lists the specs, who it suits and the closest alternatives.", "Cada ficha incluye datos técnicos, para quién es y las alternativas más cercanas.")}</p></div>
{sezioni}{conf}'''
        title = L(f"Racchette {m} {anni_txt}: tutti i {len(items)} modelli a confronto | PadelMetrix",
                  f"{m} padel rackets {anni_txt}: all {len(items)} models compared | PadelMetrix",
                  f"Palas {m} {anni_txt}: los {len(items)} modelos comparados | PadelMetrix")
        desc = L(f"Tutte le racchette da padel {m} {anni_txt}: {len(items)} schede con peso, forma, livello, opinioni e confronti tra modelli.",
                 f"All {m} padel rackets {anni_txt}: {len(items)} pages with weight, shape, level, reviews and model comparisons.",
                 f"Todas las palas de pádel {m} {anni_txt}: {len(items)} fichas con peso, forma, nivel, opiniones y comparativas entre modelos.")
        path = P("marche", ms)
        scrivi(path, pagina(title, desc, path, corpo, on="racchette", ld=[ld], alt=ALT("marche", ms)), ALT("marche", ms))
        voci.append((ms, m, len(items)))
    cr, ld = crumbs([H(), (L("Marche", "Brands", "Marcas"), None)])
    corpo = f'''{cr}<div class="intro"><h1>{L("Marche di racchette da padel", "Padel racket brands", "Marcas de palas de pádel")}</h1><p>{L(f"Le {len(voci)} marche presenti nel database, con tutti i modelli delle collezioni 2026 e 2027.", f"The {len(voci)} brands in the database, with all models from the 2026 and 2027 collections.", f"Las {len(voci)} marcas de la base de datos, con todos los modelos de las colecciones 2026 y 2027.")}</p></div>
<ul class="lista-link">{"".join(f'<li><a href="{P("marche", s)}">{L(f"Racchette {e(m)}", f"{e(m)} rackets", f"Palas {e(m)}")}</a> · {c}</li>' for s, m, c in voci)}</ul>'''
    path = P("marche")
    scrivi(path, pagina(L("Marche di racchette da padel: Bullpadel, Nox, Adidas, Head e altre | PadelMetrix",
                          "Padel racket brands: Bullpadel, Nox, Adidas, Head and more | PadelMetrix",
                          "Marcas de palas de pádel: Bullpadel, Nox, Adidas, Head y más | PadelMetrix"),
                        L("Tutte le marche di racchette da padel nel database PadelMetrix, con i modelli 2026 e 2027 di ciascuna.",
                          "All padel racket brands in the PadelMetrix database, with each brand's 2026 and 2027 models.",
                          "Todas las marcas de palas de pádel de la base de datos PadelMetrix, con los modelos 2026 y 2027 de cada una."),
                        path, corpo, on="racchette", ld=[ld], alt=ALT("marche")), ALT("marche"))


# ---------------------------------------------------------------- Confronti

def righe_cmp():
    return [(L("Marca", "Brand", "Marca"), lambda n: n["marca"]), (L("Collezione", "Collection", "Colección"), lambda n: str(n["anno"])),
            (L("Giocatore", "Player", "Jugador"), lambda n: n["giocatore"] if not n["giocatore"] or "ispirata" not in n["giocatore"] else tr(n["giocatore"])),
            (L("Forma", "Shape", "Forma"), lambda n: FORMA(n["forma"])), (L("Peso", "Weight", "Peso"), lambda n: n["peso"]),
            (L("Bilanciamento", "Balance", "Balance"), lambda n: tr(n["bilanciamento"]) if isinstance(n["bilanciamento"], str) else None),
            (L("Nucleo", "Core", "Núcleo"), lambda n: tr(n["nucleo"]) if isinstance(n["nucleo"], str) else None),
            (L("Superficie", "Face", "Cara"), lambda n: tr(n["superficie"])),
            (L("Tatto", "Feel", "Tacto"), lambda n: tr(n["sensazione"]) if isinstance(n["sensazione"], str) else None),
            (L("Livello", "Level", "Nivel"), lambda n: LIVN(n["livello"])),
            (L("Stile", "Style", "Estilo"), lambda n: STILEN(n["stile"])),
            (L("Prezzo di listino", "List price", "Precio de lista"), lambda n: euro(n["prezzo"]) if n["prezzo"] else None)]


def verdetto(a, b):
    an, bn = a["nome"], b["nome"]
    frasi = []
    if a["marca"] == b["marca"] and a["modello"] == b["modello"]:
        frasi.append(L(f"Sono due versioni dello stesso modello: la {an} e la {bn}.", f"These are two versions of the same model: the {an} and the {bn}.",
                       f"Son dos versiones del mismo modelo: la {an} y la {bn}."))
    comune = []
    if a["forma"] and a["forma"] == b["forma"]:
        comune.append(L(f"forma {FORMA(a['forma']).lower()}", f"{FORMA(a['forma']).lower()} shape", f"forma {FORMA(a['forma']).lower()}"))
    if a["livello"] and a["livello"] == b["livello"]:
        comune.append(L(f"livello {LIVN(a['livello']).lower()}", f"{LIVN(a['livello']).lower()} level", f"nivel {LIVN(a['livello']).lower()}"))
    if a["stile"] and a["stile"] == b["stile"]:
        comune.append(L(f"stile {STILEN(a['stile']).lower()}", f"{STILEN(a['stile']).lower()} style", f"estilo {STILEN(a['stile']).lower()}"))
    if comune:
        frasi.append(L("Hanno in comune ", "They share ", "Tienen en común ") + ", ".join(comune) + ".")
    diff = []
    if a["forma"] and b["forma"] and a["forma"] != b["forma"]:
        fa, fb = FORMA(a["forma"]).lower(), FORMA(b["forma"]).lower()
        diff.append(L(f"la {an} è {fa}, la {bn} {fb}", f"the {an} is {fa}, the {bn} {fb}", f"la {an} es {fa}, la {bn} {fb}"))
    if a["peso"] and b["peso"] and a["peso"] != b["peso"]:
        diff.append(L(f"pesano {a['peso']} contro {b['peso']}", f"they weigh {a['peso']} versus {b['peso']}", f"pesan {a['peso']} frente a {b['peso']}"))
    if a["livello"] and b["livello"] and a["livello"] != b["livello"]:
        la, lb = LIVN(a["livello"]).lower(), LIVN(b["livello"]).lower()
        diff.append(L(f"il livello indicato è {la} per la prima e {lb} per la seconda", f"the stated level is {la} for the first and {lb} for the second",
                      f"el nivel indicado es {la} para la primera y {lb} para la segunda"))
    if a["prezzo"] and b["prezzo"] and abs(a["prezzo"] - b["prezzo"]) >= 20:
        c = a if a["prezzo"] < b["prezzo"] else b
        lo, hi = euro(min(a["prezzo"], b["prezzo"])), euro(max(a["prezzo"], b["prezzo"]))
        diff.append(L(f"la {c['nome']} costa meno di listino ({lo} contro {hi})", f"the {c['nome']} has a lower list price ({lo} versus {hi})",
                      f"la {c['nome']} cuesta menos de lista ({lo} frente a {hi})"))
    if diff:
        frasi.append(L("Le differenze principali: ", "The main differences: ", "Las principales diferencias: ") + "; ".join(diff) + ".")
    elif not comune:
        frasi.append(L("I dati dichiarati sono vicini: conviene guardare le schede complete.", "The declared data are close: check the full pages.",
                       "Los datos declarados son parecidos: conviene mirar las fichas completas."))
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
    return f'''<h2>{L("Punteggi a confronto", "Scores compared", "Puntuaciones comparadas")}</h2><div class="tablebox"><table class="tab"><thead><tr><th>{e(tr(va["titolo"]))} ({L("su", "out of", "sobre")} {va["scala"]})</th><th>{e(a["nome"])}</th><th>{e(b["nome"])}</th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">{L(f"Punteggi pubblicati da fonti esterne ({e(tr(fonte))}), riportati come sono. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.",
                   f"Scores published by external sources ({e(tr(fonte))}), reported as they are. The PadelMetrix score will follow with our own rating method.",
                   f"Puntuaciones publicadas por fuentes externas ({e(tr(fonte))}), tal cual. La puntuación PadelMetrix llegará con nuestro método de valoración.")}</p>'''


def confronti(db, pairs):
    per = {n["slug"]: n for n in db}
    C = L("Confronta", "Compare", "Comparar")
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
            altri_html = f'<h2>{L("Altri confronti", "Other comparisons", "Otras comparativas")}</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(p, q)}">{e(per[p]["nome"])} vs {e(per[q]["nome"])}</a></li>' for p, q in altri) + "</ul>"
        cs = confronto_slug(x, y)
        path = P("confronta", cs)
        alt = ALT("confronta", cs)
        tit = f"{a['titolo']} vs {b['titolo']}"
        cr, ld = crumbs([H(), (C, P("confronta")), (f"{a['nome']} vs {b['nome']}", None)])

        def box(n, ad):
            nm = e(n["nome"])
            return (f'<div class="card"><h2>{L(f"Scegli la {nm} se", f"Choose the {nm} if", f"Elige la {nm} si")}</h2><ul class="clean">{"".join(f"<li>{e(tr(t))}</li>" for t in ad)}</ul>'
                    f'<p><a href="{url_r(n)}">{L(f"Scheda completa della {nm}", f"Full page of the {nm}", f"Ficha completa de la {nm}")}</a></p></div>')
        corpo = f'''{cr}
<div class="intro"><h1>{e(a["nome"])} vs {e(b["nome"])}</h1><p>{e(verdetto(a, b))}</p></div>
<div class="prose" style="max-width:none">
<h2>{L("Dati tecnici a confronto", "Specs compared", "Datos técnicos comparados")}</h2>
<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{url_r(a)}">{e(a["titolo"])}</a></th><th><a href="{url_r(b)}">{e(b["titolo"])}</a></th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">{L('Dati dalle schede PadelMetrix, che citano le fonti di ogni valore. "—" indica un dato non dichiarato.', 'Data from the PadelMetrix pages, which cite the source of every value. "—" means the value is not stated.', 'Datos de las fichas PadelMetrix, que citan la fuente de cada valor. "—" indica un dato no declarado.')}</p>
{barre_doppie(a, b)}
<h2>{L("Quale scegliere", "Which one to choose", "Cuál elegir")}</h2>
<div class="vs">
{box(a, ad_a)}
{box(b, ad_b)}
</div>
{altri_html}
</div>'''
        desc = L(f"{tit}: differenze di peso, forma, livello e prezzo, punteggi e quale scegliere in base al tuo gioco.",
                 f"{tit}: differences in weight, shape, level and price, scores and which one to choose for your game.",
                 f"{tit}: diferencias de peso, forma, nivel y precio, puntuaciones y cuál elegir según tu juego.")
        scrivi(path, pagina(L(f"{tit}: differenze e quale scegliere | PadelMetrix", f"{tit}: differences and which to choose | PadelMetrix", f"{tit}: diferencias y cuál elegir | PadelMetrix"),
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
    labels = [[L("Marca", "Brand", "Marca"), "marca"], [L("Collezione", "Collection", "Colección"), "anno"], [L("Giocatore", "Player", "Jugador"), "giocatore"],
              [L("Forma", "Shape", "Forma"), "forma"], [L("Peso", "Weight", "Peso"), "peso"], [L("Superficie", "Face", "Cara"), "superficie"],
              [L("Livello", "Level", "Nivel"), "livello"], [L("Stile", "Style", "Estilo"), "stile"], [L("Prezzo di listino", "List price", "Precio de lista"), "prezzo"]]
    base_c = P("confronta")
    tool_js = "<script>var IDX=" + json.dumps(indice, ensure_ascii=False) + ";var PAIRS=" + json.dumps(pairkeys) + ";var LAB=" + json.dumps(labels, ensure_ascii=False) + """;
(function(){var s1=document.getElementById('r1'),s2=document.getElementById('r2'),out=document.getElementById('cmp-out');
var q=new URLSearchParams(location.search).get('r');if(q){var p=q.split(',');if(p[0])s1.value=p[0];if(p[1])s2.value=p[1];}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function get(s){for(var i=0;i<IDX.length;i++)if(IDX[i].slug===s)return IDX[i];return null;}
function run(){var a=get(s1.value),b=get(s2.value);if(!a||!b||a===b){out.innerHTML='';return;}
var h='<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="'+a.url+'">'+esc(a.titolo)+'</a></th><th><a href="'+b.url+'">'+esc(b.titolo)+'</a></th></tr></thead><tbody>';
LAB.forEach(function(r){var x=a[r[1]],y=b[r[1]];if(x||y)h+='<tr><td>'+r[0]+'</td><td>'+esc(x||'—')+'</td><td>'+esc(y||'—')+'</td></tr>';});
h+='</tbody></table></div>';var k=[a.slug,b.slug].sort().join('|');if(PAIRS.indexOf(k)>=0){var u='""" + base_c + """'+[a.slug,b.slug].sort().join('-vs-')+'/';h+='<p><a class="btn" href="'+u+'">""" + L("Leggi il confronto completo", "Read the full comparison", "Lee la comparativa completa") + """</a></p>';}
out.innerHTML=h;}
s1.addEventListener('change',run);s2.addEventListener('change',run);run();})();
</script>"""
    elenco_c = '<ul class="lista-link">' + "".join(
        f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>'
        for x, y in sorted(pairs, key=lambda p: (per[p[0]]["marca"], per[p[0]]["nome"]))) + "</ul>"
    cr, ld = crumbs([H(), (C, None)])
    r1, r2 = L("Prima racchetta", "First racket", "Primera pala"), L("Seconda racchetta", "Second racket", "Segunda pala")
    corpo = f'''{cr}
<div class="intro"><h1>{L("Confronta racchette da padel", "Compare padel rackets", "Compara palas de pádel")}</h1><p>{L(f"Scegli due racchette e guarda subito dove si differenziano: peso, forma, materiali, livello e prezzo. Sotto trovi i {len(pairs)} confronti più cercati, già spiegati.",
       f"Pick two rackets and see at once where they differ: weight, shape, materials, level and price. Below are the {len(pairs)} most searched comparisons, already explained.",
       f"Elige dos palas y mira enseguida en qué se diferencian: peso, forma, materiales, nivel y precio. Debajo tienes las {len(pairs)} comparativas más buscadas, ya explicadas.")}</p></div>
<form class="cmp-tool" onsubmit="return false"><select id="r1" aria-label="{r1}"><option value="">{r1}</option>{opts}</select>
<select id="r2" aria-label="{r2}"><option value="">{r2}</option>{opts}</select></form>
<div id="cmp-out"></div>
<section class="block"><h2>{L("Confronti più cercati", "Most searched comparisons", "Comparativas más buscadas")}</h2>{elenco_c}</section>'''
    path = P("confronta")
    scrivi(path, pagina(L("Confronto racchette padel: metti a confronto due modelli | PadelMetrix", "Padel racket comparison: compare two models side by side | PadelMetrix",
                          "Comparador de palas de pádel: compara dos modelos | PadelMetrix"),
                        L(f"Confronta due racchette da padel per peso, forma, materiali, livello e prezzo. {len(pairs)} confronti già spiegati tra i modelli 2026 e 2027.",
                          f"Compare two padel rackets by weight, shape, materials, level and price. {len(pairs)} comparisons of 2026 and 2027 models already explained.",
                          f"Compara dos palas de pádel por peso, forma, materiales, nivel y precio. {len(pairs)} comparativas ya explicadas entre modelos 2026 y 2027."),
                        path, corpo, on="confronta", ld=[ld], extra_js=tool_js, alt=ALT("confronta")), ALT("confronta"))


# ---------------------------------------------------------------- Guide

def guida(slug, title, desc, h1, crumb, intro_html, corpo_html, items, on="guide", ld_extra=()):
    path, alt = P("guide", slug), ALT("guide", slug)
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías"), P("guide")), (crumb, None)])
    lista = f'<section class="block"><h2>{L("Le racchette del database adatte", "Suitable rackets in the database", "Las palas de la base de datos adecuadas")} ({len(items)})</h2>{griglia(ordina(items))}</section>' if items else ""
    corpo = f'''{cr}
<div class="intro"><h1>{e(h1)}</h1>{intro_html}{data_riga(femm=True)}</div>
<div class="prose">{corpo_html}</div>
{lista}'''
    scrivi(path, pagina(title, desc, path, corpo, on=on, ld=[ld, *ld_extra], alt=alt), alt)


def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}


def faq_html(qa):
    return f'<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes")}</h2><div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</div>"


def guide(db):
    adulti = [n for n in db if n["categoria"] != "junior"]
    G = []
    pg = lambda s: P("guide", s)  # noqa: E731

    # principianti
    items = [n for n in adulti if n["livello"] in ("principiante", "principiante-intermedio")]
    qa = [(L("Che forma deve avere una racchetta da padel per principianti?", "What shape should a beginner padel racket be?", "¿Qué forma debe tener una pala de pádel para principiantes?"),
           L("Meglio rotonda o a goccia: lo sweet spot è più centrato e la racchetta perdona di più i colpi decentrati.",
             "Round or teardrop is best: the sweet spot is more central and the racket forgives off-centre hits more.",
             "Mejor redonda o de lágrima: el punto dulce está más centrado y la pala perdona más los golpes descentrados.")),
          (L("Quanto deve pesare la prima racchetta da padel?", "How much should your first padel racket weigh?", "¿Cuánto debe pesar la primera pala de pádel?"),
           L("Per un adulto di solito tra 350 e 365 grammi; chi ha poca forza o fastidi al braccio può scendere verso i 340.",
             "For an adult usually between 350 and 365 grams; players with less strength or arm problems can go down towards 340.",
             "Para un adulto normalmente entre 350 y 365 gramos; quien tiene poca fuerza o molestias en el brazo puede bajar hacia los 340.")),
          (L("Meglio fibra di vetro o carbonio per iniziare?", "Is fiberglass or carbon better for starting out?", "¿Mejor fibra de vidrio o carbono para empezar?"),
           L("La fibra di vetro è più morbida ed economica e aiuta a far uscire la palla; il carbonio è più rigido e preciso, adatto quando la tecnica è più solida.",
             "Fiberglass is softer and cheaper and helps the ball come off the face; carbon is stiffer and more precise, suited to players whose technique is more solid.",
             "La fibra de vidrio es más blanda y económica y ayuda a sacar la bola; el carbono es más rígido y preciso, adecuado cuando la técnica es más sólida."))]
    guida("racchetta-padel-principianti",
          L("Racchetta da padel per principianti: come sceglierla e i modelli 2026 | PadelMetrix", "Padel racket for beginners: how to choose one and the 2026 models | PadelMetrix",
            "Pala de pádel para principiantes: cómo elegirla y los modelos 2026 | PadelMetrix"),
          L("Come scegliere la prima racchetta da padel: forma, peso, materiali e prezzo. Più l'elenco dei modelli 2026 e 2027 adatti a chi inizia.",
            "How to choose your first padel racket: shape, weight, materials and price. Plus the list of 2026 and 2027 models suited to beginners.",
            "Cómo elegir la primera pala de pádel: forma, peso, materiales y precio. Más la lista de modelos 2026 y 2027 adecuados para quien empieza."),
          L("Racchetta da padel per principianti", "Padel racket for beginners", "Pala de pádel para principiantes"), L("Principianti", "Beginners", "Principiantes"),
          L("<p><b>La racchetta giusta per un principiante è rotonda o a goccia, pesa 350–365 g, ha bilanciamento basso o medio e una superficie morbida in fibra di vetro o carbonio leggero; costa in genere 70–150 €.</b> Le racchette da professionisti, rigide e pesanti in testa, rendono l'apprendimento più faticoso.</p>",
            "<p><b>The right racket for a beginner is round or teardrop, weighs 350–365 g, has a low or medium balance and a soft fiberglass or light carbon face; it usually costs €70–150.</b> Pro rackets, stiff and head-heavy, make learning harder.</p>",
            "<p><b>La pala adecuada para un principiante es redonda o de lágrima, pesa 350–365 g, tiene balance bajo o medio y una cara blanda de fibra de vidrio o carbono ligero; suele costar 70–150 €.</b> Las palas de profesionales, rígidas y pesadas en cabeza, hacen el aprendizaje más difícil.</p>"),
          L(f"""<h2>I quattro criteri</h2><ol><li><b>Forma rotonda o a goccia.</b> Lo sweet spot è al centro e più ampio.</li><li><b>Peso 350–365 g.</b> Abbastanza stabile, non affatica il braccio.</li><li><b>Bilanciamento basso o medio.</b> Più maneggevole nelle volée e in difesa.</li><li><b>Fibra di vetro o carbonio morbido.</b> Tatto più confortevole e uscita di palla facile.</li></ol>
<p>Sul prezzo: per iniziare non serve spendere più di 100–150 €. Vedi anche le <a href="{pg('racchette-padel-economiche')}">racchette economiche</a> e le <a href="{pg('forme-racchetta-padel')}">differenze tra le forme</a>.</p>""",
            f"""<h2>The four criteria</h2><ol><li><b>Round or teardrop shape.</b> The sweet spot is central and larger.</li><li><b>Weight 350–365 g.</b> Stable enough, without tiring the arm.</li><li><b>Low or medium balance.</b> Easier to handle on volleys and in defence.</li><li><b>Fiberglass or soft carbon.</b> A more comfortable feel and easy ball output.</li></ol>
<p>On price: to start out you don't need to spend more than €100–150. See also the <a href="{pg('racchette-padel-economiche')}">cheap rackets</a> and the <a href="{pg('forme-racchetta-padel')}">differences between shapes</a>.</p>""",
            f"""<h2>Los cuatro criterios</h2><ol><li><b>Forma redonda o de lágrima.</b> El punto dulce está en el centro y es más amplio.</li><li><b>Peso 350–365 g.</b> Bastante estable, sin cansar el brazo.</li><li><b>Balance bajo o medio.</b> Más manejable en las voleas y en defensa.</li><li><b>Fibra de vidrio o carbono blando.</b> Tacto más cómodo y salida de bola fácil.</li></ol>
<p>Sobre el precio: para empezar no hace falta gastar más de 100–150 €. Mira también las <a href="{pg('racchette-padel-economiche')}">palas baratas</a> y las <a href="{pg('forme-racchetta-padel')}">diferencias entre formas</a>.</p>""") + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("racchetta-padel-principianti", L("Racchetta da padel per principianti", "Padel racket for beginners", "Pala de pádel para principiantes"), len(items)))

    # gomito
    items = [n for n in adulti if isinstance(n["sensazione"], str) and "morbid" in n["sensazione"].lower()
             and (n["forma"] != "diamante" or any(w in n["nome"].lower() for w in ("comfort", "soft", "cmf")))]
    qa = [(L("Quale racchetta da padel scegliere con l'epicondilite?", "Which padel racket should you choose with tennis elbow?", "¿Qué pala de pádel elegir con epicondilitis?"),
           L("In generale si consigliano racchette dal tatto morbido, non troppo pesanti e con bilanciamento basso o medio, che trasmettono meno vibrazioni al braccio. La scelta va comunque fatta con il proprio medico o fisioterapista.",
             "In general, rackets with a soft feel, not too heavy and with a low or medium balance are recommended, as they transmit less vibration to the arm. The choice should still be made with your doctor or physiotherapist.",
             "En general se recomiendan palas de tacto blando, no demasiado pesadas y con balance bajo o medio, que transmiten menos vibraciones al brazo. En todo caso, la elección debe hacerse con tu médico o fisioterapeuta.")),
          (L("Le racchette a diamante sono sconsigliate per il gomito?", "Are diamond rackets bad for the elbow?", "¿Las palas diamante están desaconsejadas para el codo?"),
           L("Le diamante rigide e pesanti in testa sollecitano di più l'avambraccio. Esistono versioni Comfort o Soft più morbide, ma per chi ha dolore conviene partire da rotonde o a goccia.",
             "Stiff, head-heavy diamonds put more strain on the forearm. There are softer Comfort or Soft versions, but if you are in pain it is better to start with round or teardrop rackets.",
             "Las diamante rígidas y pesadas en cabeza cargan más el antebrazo. Existen versiones Comfort o Soft más blandas, pero si tienes dolor conviene empezar por redondas o de lágrima.")),
          (L("Il peso conta per il gomito?", "Does weight matter for the elbow?", "¿El peso influye en el codo?"),
           L("Una racchetta troppo leggera vibra di più, una troppo pesante affatica: di solito si resta nella fascia media, intorno ai 350–365 grammi.",
             "A racket that is too light vibrates more, one that is too heavy tires you: usually it is best to stay in the middle range, around 350–365 grams.",
             "Una pala demasiado ligera vibra más, una demasiado pesada cansa: lo normal es quedarse en la franja media, alrededor de 350–365 gramos."))]
    guida("racchetta-padel-epicondilite",
          L("Racchetta da padel per epicondilite e gomito del tennista: come sceglierla | PadelMetrix", "Padel racket for tennis elbow: how to choose one | PadelMetrix",
            "Pala de pádel para epicondilitis y codo de tenista: cómo elegirla | PadelMetrix"),
          L("Racchette da padel per chi soffre di epicondilite: tatto morbido, peso e bilanciamento giusti, e i modelli 2026 e 2027 più confortevoli per il braccio.",
            "Padel rackets for players with tennis elbow: soft feel, the right weight and balance, and the most arm-friendly 2026 and 2027 models.",
            "Palas de pádel para quien sufre epicondilitis: tacto blando, peso y balance adecuados, y los modelos 2026 y 2027 más cómodos para el brazo."),
          L("Racchetta da padel per epicondilite e gomito", "Padel racket for tennis elbow", "Pala de pádel para epicondilitis y codo"), L("Epicondilite e gomito", "Tennis elbow", "Epicondilitis y codo"),
          L("<p><b>Con l'epicondilite conviene una racchetta dal tatto morbido, di 350–365 g, rotonda o a goccia e con bilanciamento basso o medio, che trasmette meno vibrazioni al braccio.</b> La racchetta non cura il gomito, ma può evitare di peggiorarlo. Questa pagina non sostituisce il parere di un medico o di un fisioterapista.</p>",
            "<p><b>With tennis elbow, choose a soft-feeling racket of 350–365 g, round or teardrop, with a low or medium balance, which transmits less vibration to the arm.</b> A racket won't cure your elbow, but it can avoid making it worse. This page is not a substitute for the advice of a doctor or physiotherapist.</p>",
            "<p><b>Con epicondilitis conviene una pala de tacto blando, de 350–365 g, redonda o de lágrima y con balance bajo o medio, que transmite menos vibraciones al brazo.</b> La pala no cura el codo, pero puede evitar que empeore. Esta página no sustituye la opinión de un médico o un fisioterapeuta.</p>"),
          L("""<h2>Cosa guardare nella scheda</h2><ul><li><b>Tatto:</b> morbido o medio-morbido. Le gomme EVA soft e le superfici in fibra di vetro assorbono più vibrazioni.</li><li><b>Forma:</b> rotonda o a goccia; le diamante concentrano il peso in testa.</li><li><b>Peso e bilanciamento:</b> 350–365 g, bilanciamento basso o medio.</li><li><b>Versioni Comfort e Soft:</b> molti marchi le propongono accanto al modello rigido, con gli stessi stampi ma materiali più morbidi.</li></ul>
<p>Nell'elenco sotto trovi le racchette del database con tatto dichiarato morbido o medio-morbido.</p>""",
            """<h2>What to look for on the spec page</h2><ul><li><b>Feel:</b> soft or medium-soft. Soft EVA rubbers and fiberglass faces absorb more vibration.</li><li><b>Shape:</b> round or teardrop; diamonds concentrate the weight in the head.</li><li><b>Weight and balance:</b> 350–365 g, low or medium balance.</li><li><b>Comfort and Soft versions:</b> many brands offer them alongside the stiff model, with the same moulds but softer materials.</li></ul>
<p>The list below shows the rackets in the database with a declared soft or medium-soft feel.</p>""",
            """<h2>Qué mirar en la ficha</h2><ul><li><b>Tacto:</b> blando o medio-blando. Las gomas EVA soft y las caras de fibra de vidrio absorben más vibraciones.</li><li><b>Forma:</b> redonda o de lágrima; las diamante concentran el peso en la cabeza.</li><li><b>Peso y balance:</b> 350–365 g, balance bajo o medio.</li><li><b>Versiones Comfort y Soft:</b> muchas marcas las ofrecen junto al modelo rígido, con los mismos moldes pero materiales más blandos.</li></ul>
<p>En la lista de abajo están las palas de la base de datos con tacto declarado blando o medio-blando.</p>""") + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("racchetta-padel-epicondilite", L("Racchetta da padel per epicondilite e gomito", "Padel racket for tennis elbow", "Pala de pádel para epicondilitis y codo"), len(items)))

    # forme
    conta = {f: [n for n in adulti if n["forma"] == f] for f in ("rotonda", "goccia", "diamante", "ibrida")}
    qa = [(L("Meglio una racchetta da padel rotonda o a diamante?", "Is a round or a diamond padel racket better?", "¿Mejor una pala de pádel redonda o diamante?"),
           L("Rotonda se cerchi controllo, tolleranza e gioco da fondo campo; diamante se giochi spesso a rete e vuoi potenza nello smash, con una tecnica già solida.",
             "Round if you want control, forgiveness and baseline play; diamond if you often play at the net and want smash power, with already solid technique.",
             "Redonda si buscas control, tolerancia y juego desde el fondo; diamante si juegas a menudo en la red y quieres potencia en el remate, con una técnica ya sólida.")),
          (L("Cos'è una racchetta a goccia?", "What is a teardrop racket?", "¿Qué es una pala de lágrima?"),
           L("Una forma intermedia: il peso è leggermente spostato verso la testa, per un compromesso tra controllo e potenza. È la scelta più versatile.",
             "An intermediate shape: the weight is shifted slightly towards the head, for a compromise between control and power. It is the most versatile choice.",
             "Una forma intermedia: el peso está algo desplazado hacia la cabeza, para un compromiso entre control y potencia. Es la opción más versátil.")),
          (L("Cosa vuol dire racchetta ibrida?", "What does hybrid racket mean?", "¿Qué significa pala híbrida?"),
           L("È il nome che molti marchi usano per stampi tra goccia e diamante, o tra goccia e rotonda: il carattere dipende dal modello.",
             "It is the name many brands use for moulds between teardrop and diamond, or between teardrop and round: the character depends on the model.",
             "Es el nombre que muchas marcas usan para moldes entre lágrima y diamante, o entre lágrima y redonda: el carácter depende del modelo."))]
    sez = ""
    testi = {"rotonda": L("Sweet spot centrato e peso verso il manico: la forma del controllo e della difesa, adatta a principianti e a chi costruisce il punto.",
                          "Centred sweet spot and weight towards the handle: the shape of control and defence, suited to beginners and players who build the point.",
                          "Punto dulce centrado y peso hacia el mango: la forma del control y la defensa, adecuada para principiantes y para quien construye el punto."),
             "goccia": L("Peso leggermente in testa e sweet spot un po' più alto: la forma polivalente, buona per la maggior parte dei giocatori.",
                         "Weight slightly towards the head and a slightly higher sweet spot: the all-round shape, good for most players.",
                         "Peso ligeramente en cabeza y punto dulce algo más alto: la forma polivalente, buena para la mayoría de jugadores."),
             "diamante": L("Testa più larga in alto e bilanciamento alto: la forma dell'attacco, per chi chiude i punti a rete e ha già una buona tecnica.",
                           "Head wider at the top and high balance: the attacking shape, for players who finish points at the net and already have good technique.",
                           "Cabeza más ancha arriba y balance alto: la forma del ataque, para quien cierra los puntos en la red y ya tiene buena técnica."),
             "ibrida": L("Stampi intermedi che ogni marca interpreta a modo suo, di solito tra goccia e diamante.",
                         "Intermediate moulds that each brand interprets in its own way, usually between teardrop and diamond.",
                         "Moldes intermedios que cada marca interpreta a su manera, normalmente entre lágrima y diamante.")}
    for f, its in conta.items():
        fo = FORMA(f).lower()
        sez += L(f'<h2>Racchette {fo} ({len(its)} nel database)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">Vedi tutte le racchette {fo}</a>.</p>',
                 f'<h2>{FORMA(f)} rackets ({len(its)} in the database)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">See all {fo} rackets</a>.</p>',
                 f'<h2>Palas {fo} ({len(its)} en la base de datos)</h2><p>{testi[f]} <a href="{P("racchette")}?forma={f}">Ver todas las palas {fo}</a>.</p>')
    guida("forme-racchetta-padel",
          L("Racchetta da padel rotonda, a goccia o a diamante: differenze e come scegliere | PadelMetrix", "Round, teardrop or diamond padel racket: differences and how to choose | PadelMetrix",
            "Pala de pádel redonda, lágrima o diamante: diferencias y cómo elegir | PadelMetrix"),
          L("Differenze tra racchetta da padel rotonda, a goccia, a diamante e ibrida: controllo, potenza, sweet spot e quale scegliere per il tuo livello.",
            "Differences between round, teardrop, diamond and hybrid padel rackets: control, power, sweet spot and which to choose for your level.",
            "Diferencias entre pala de pádel redonda, de lágrima, diamante e híbrida: control, potencia, punto dulce y cuál elegir según tu nivel."),
          L("Racchetta rotonda, a goccia o a diamante?", "Round, teardrop or diamond racket?", "¿Pala redonda, de lágrima o diamante?"), L("Forme delle racchette", "Racket shapes", "Formas de las palas"),
          L("<p><b>La racchetta rotonda dà controllo e tolleranza, quella a diamante potenza nello smash, quella a goccia sta in mezzo ed è la più versatile.</b> La forma decide dove sta lo sweet spot e come è distribuito il peso, e quindi il carattere della racchetta.</p>",
            "<p><b>A round racket gives control and forgiveness, a diamond gives smash power, and a teardrop sits in between and is the most versatile.</b> The shape decides where the sweet spot is and how the weight is distributed, and therefore the racket's character.</p>",
            "<p><b>La pala redonda da control y tolerancia, la diamante potencia en el remate y la de lágrima está en medio y es la más versátil.</b> La forma decide dónde está el punto dulce y cómo se reparte el peso, y por tanto el carácter de la pala.</p>"),
          sez + faq_html(qa), [], ld_extra=[faq_ld(qa)])
    G.append(("forme-racchetta-padel", L("Racchetta rotonda, a goccia o a diamante?", "Round, teardrop or diamond racket?", "¿Pala redonda, de lágrima o diamante?"), None))

    # donna
    items = [n for n in adulti if n["donna"]]
    guida("racchette-padel-donna",
          L("Racchette da padel da donna 2026 e 2027: i modelli femminili | PadelMetrix", "Women's padel rackets 2026 and 2027: the women's models | PadelMetrix",
            "Palas de pádel de mujer 2026 y 2027: los modelos femeninos | PadelMetrix"),
          L("Le racchette da padel da donna delle collezioni 2026 e 2027: modelli delle giocatrici professioniste, pesi, forme e livelli.",
            "Women's padel rackets from the 2026 and 2027 collections: pro players' models, weights, shapes and levels.",
            "Las palas de pádel de mujer de las colecciones 2026 y 2027: modelos de las jugadoras profesionales, pesos, formas y niveles."),
          L("Racchette da padel da donna", "Women's padel rackets", "Palas de pádel de mujer"), L("Racchette da donna", "Women's rackets", "Palas de mujer"),
          L("<p>Le racchette femminili sono in genere più leggere (spesso 340–360 g) e più maneggevoli, ma non sono obbligatorie: conta il peso che riesci a gestire senza affaticare il braccio. Qui trovi i modelli che i marchi presentano come femminili, molti firmati da giocatrici professioniste.</p>",
            "<p>Women's rackets are generally lighter (often 340–360 g) and easier to handle, but they are not compulsory: what matters is the weight you can manage without tiring your arm. Here are the models the brands present as women's rackets, many signed by professional players.</p>",
            "<p>Las palas femeninas suelen ser más ligeras (a menudo 340–360 g) y manejables, pero no son obligatorias: lo que cuenta es el peso que puedes manejar sin cansar el brazo. Aquí están los modelos que las marcas presentan como femeninos, muchos firmados por jugadoras profesionales.</p>"),
          L(f"<p>Se cerchi una racchetta leggera senza limitarti ai modelli femminili, usa il filtro per livello e forma nella <a href=\"{P('racchette')}\">pagina Racchette</a>.</p>",
            f"<p>If you want a light racket without limiting yourself to women's models, use the level and shape filters on the <a href=\"{P('racchette')}\">Rackets page</a>.</p>",
            f"<p>Si buscas una pala ligera sin limitarte a los modelos femeninos, usa el filtro por nivel y forma en la <a href=\"{P('racchette')}\">página Palas</a>.</p>"), items)
    G.append(("racchette-padel-donna", L("Racchette da padel da donna", "Women's padel rackets", "Palas de pádel de mujer"), len(items)))

    # economiche
    items = [n for n in adulti if n["prezzo"] and n["prezzo"] <= 130]
    guida("racchette-padel-economiche",
          L("Racchette da padel economiche sotto 130 euro: modelli 2026 e 2027 | PadelMetrix", "Cheap padel rackets under €130: 2026 and 2027 models | PadelMetrix",
            "Palas de pádel baratas por menos de 130 euros: modelos 2026 y 2027 | PadelMetrix"),
          L("Racchette da padel economiche con prezzo di listino fino a 130 euro: modelli per principianti e intermedi delle marche principali.",
            "Cheap padel rackets with a list price up to €130: models for beginners and intermediates from the main brands.",
            "Palas de pádel baratas con precio de lista de hasta 130 euros: modelos para principiantes e intermedios de las principales marcas."),
          L("Racchette da padel economiche (fino a 130 € di listino)", "Cheap padel rackets (list price up to €130)", "Palas de pádel baratas (hasta 130 € de precio de lista)"),
          L("Racchette economiche", "Cheap rackets", "Palas baratas"),
          L("<p>Il prezzo di listino è solo un riferimento: online molte racchette costano il 20–40% in meno, quindi anche modelli con listino più alto possono rientrare nel tuo budget. Qui trovi quelle con listino fino a 130 €.</p>",
            "<p>The list price is only a reference: online, many rackets cost 20–40% less, so models with a higher list price may also fit your budget. Here are those with a list price up to €130.</p>",
            "<p>El precio de lista es solo una referencia: online muchas palas cuestan un 20–40% menos, así que también modelos con precio de lista más alto pueden entrar en tu presupuesto. Aquí están las de hasta 130 € de lista.</p>"),
          L(f"<p>A questo prezzo prevalgono superfici in fibra di vetro e forme rotonde o a goccia: ottime per iniziare e per giocare con regolarità. Vedi anche la <a href=\"{pg('racchetta-padel-principianti')}\">guida per principianti</a>.</p>",
            f"<p>At this price fiberglass faces and round or teardrop shapes dominate: great for starting out and playing regularly. See also the <a href=\"{pg('racchetta-padel-principianti')}\">beginner's guide</a>.</p>",
            f"<p>A este precio predominan las caras de fibra de vidrio y las formas redondas o de lágrima: perfectas para empezar y jugar con regularidad. Mira también la <a href=\"{pg('racchetta-padel-principianti')}\">guía para principiantes</a>.</p>"), items)
    G.append(("racchette-padel-economiche", L("Racchette da padel economiche", "Cheap padel rackets", "Palas de pádel baratas"), len(items)))

    # controllo / potenza
    for st, slug, h1, txt in (("controllo", "racchette-padel-controllo", L("Racchette da padel di controllo", "Control padel rackets", "Palas de pádel de control"),
                               L("Le racchette di controllo privilegiano precisione, sweet spot ampio e maneggevolezza. Di solito sono rotonde o a goccia con bilanciamento basso: ideali per chi gioca da fondo campo e costruisce il punto.",
                                 "Control rackets prioritise precision, a large sweet spot and maneuverability. They are usually round or teardrop with a low balance: ideal for players who play from the back and build the point.",
                                 "Las palas de control priorizan la precisión, un punto dulce amplio y la manejabilidad. Suelen ser redondas o de lágrima con balance bajo: ideales para quien juega desde el fondo y construye el punto.")),
                              ("offensivo", "racchette-padel-potenza", L("Racchette da padel di potenza", "Power padel rackets", "Palas de pádel de potencia"),
                               L("Le racchette di potenza hanno il peso spostato in testa e una superficie più rigida: aiutano a chiudere i punti con smash e volée, ma chiedono tecnica e sono meno tolleranti in difesa.",
                                 "Power rackets have the weight shifted towards the head and a stiffer face: they help finish points with smashes and volleys, but demand technique and are less forgiving in defence.",
                                 "Las palas de potencia tienen el peso desplazado hacia la cabeza y una cara más rígida: ayudan a cerrar los puntos con remates y voleas, pero exigen técnica y son menos tolerantes en defensa."))):
        items = [n for n in adulti if n["stile"] == st]
        guida(slug, L(f"{h1} 2026 e 2027: come sceglierle e i modelli | PadelMetrix", f"{h1} 2026 and 2027: how to choose and the models | PadelMetrix", f"{h1} 2026 y 2027: cómo elegirlas y los modelos | PadelMetrix"),
              L(f"{h1}: caratteristiche, a chi sono adatte e tutti i modelli 2026 e 2027 nel database PadelMetrix.", f"{h1}: features, who they suit and all the 2026 and 2027 models in the PadelMetrix database.",
                f"{h1}: características, para quién son y todos los modelos 2026 y 2027 de la base de datos PadelMetrix."),
              h1, h1, f"<p>{txt}</p>",
              L(f'<p>Non sai quale stile fa per te? Leggi la guida alle <a href="{pg("forme-racchetta-padel")}">forme delle racchette</a>.</p>',
                f'<p>Not sure which style suits you? Read the guide to <a href="{pg("forme-racchetta-padel")}">racket shapes</a>.</p>',
                f'<p>¿No sabes qué estilo es para ti? Lee la guía de las <a href="{pg("forme-racchetta-padel")}">formas de las palas</a>.</p>'), items)
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
    t_pro = L("Le racchette dei giocatori professionisti", "The rackets of professional players", "Las palas de los jugadores profesionales")
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías"), P("guide")), (L("Racchette dei professionisti", "Pro players' rackets", "Palas de los profesionales"), None)])
    corpo = f'''{cr}<div class="intro"><h1>{t_pro}</h1><p>{L("Con che racchetta giocano Tapia, Coello, Galán, Lebrón, Chingotto e gli altri: i modelli firmati dai professionisti nelle collezioni 2026 e 2027. Le versioni in vendita sono quelle dei negozi; i professionisti possono usare racchette personalizzate.",
       "Which racket Tapia, Coello, Galán, Lebrón, Chingotto and the others play with: the models signed by professionals in the 2026 and 2027 collections. The versions on sale are the shop versions; professionals may use customised rackets.",
       "Con qué pala juegan Tapia, Coello, Galán, Lebrón, Chingotto y los demás: los modelos firmados por los profesionales en las colecciones 2026 y 2027. Las versiones a la venta son las de las tiendas; los profesionales pueden usar palas personalizadas.")}</p></div>
<div class="tablebox"><table class="tab"><thead><tr><th>{L("Giocatore", "Player", "Jugador")}</th><th>{L("Racchetta", "Racket", "Pala")}</th></tr></thead><tbody>{righe}</tbody></table></div>'''
    path, alt = P("guide", slug), ALT("guide", slug)
    scrivi(path, pagina(L("Con che racchetta giocano i professionisti del padel? Modelli 2026 e 2027 | PadelMetrix", "What rackets do padel pros use? 2026 and 2027 models | PadelMetrix",
                          "¿Con qué pala juegan los profesionales del pádel? Modelos 2026 y 2027 | PadelMetrix"),
                        L("Le racchette firmate dai giocatori professionisti di padel: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto e altri.",
                          "The rackets signed by professional padel players: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto and others.",
                          "Las palas firmadas por los jugadores profesionales de pádel: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto y otros."),
                        path, corpo, on="guide", ld=[ld], alt=alt), alt)
    G.append((slug, t_pro, None))

    # hub guide
    cr, ld = crumbs([H(), (L("Guide", "Guides", "Guías"), None)])
    n_r = L("racchette", "rackets", "palas")
    voci = "".join(f'<li><a href="{pg(s)}">{e(t)}</a>{f" · {c} {n_r}" if c else ""}</li>' for s, t, c in G)
    corpo = f'''{cr}<div class="intro"><h1>{L("Guide alla scelta della racchetta da padel", "Guides to choosing a padel racket", "Guías para elegir pala de pádel")}</h1><p>{L("Guide pratiche per trovare la racchetta giusta in base a livello, stile di gioco, budget e problemi fisici. Ogni guida rimanda alle schede dei modelli adatti.",
       "Practical guides to finding the right racket for your level, playing style, budget and physical issues. Each guide links to the pages of suitable models.",
       "Guías prácticas para encontrar la pala adecuada según tu nivel, estilo de juego, presupuesto y problemas físicos. Cada guía enlaza a las fichas de los modelos adecuados.")}</p></div>
<ul class="lista-link">{voci}<li><a href="{P("bambini")}">{L("Racchette da padel per bambini e ragazzi", "Padel rackets for kids and teenagers", "Palas de pádel para niños y jóvenes")}</a></li></ul>'''
    path = P("guide")
    scrivi(path, pagina(L("Guide alla scelta della racchetta da padel | PadelMetrix", "Padel racket buying guides | PadelMetrix", "Guías para elegir pala de pádel | PadelMetrix"),
                        L("Come scegliere la racchetta da padel: guide per principianti, epicondilite, forme, donne, bambini, budget e racchette dei professionisti.",
                          "How to choose a padel racket: guides for beginners, tennis elbow, shapes, women, kids, budget and pro players' rackets.",
                          "Cómo elegir pala de pádel: guías para principiantes, epicondilitis, formas, mujeres, niños, presupuesto y palas de los profesionales."),
                        path, corpo, on="guide", ld=[ld], alt=ALT("guide")), ALT("guide"))


# ---------------------------------------------------------------- Bambini

def bambini(db):
    items = [n for n in db if n["categoria"] == "junior"]
    qa = [(L("Che racchetta da padel per un bambino di 8 anni?", "What padel racket for an 8-year-old?", "¿Qué pala de pádel para un niño de 8 años?"),
           L("Indicativamente una racchetta junior rotonda tra 280 e 310 grammi, più corta di quella da adulto. Conta più l'altezza del bambino che l'età.",
             "Roughly a round junior racket between 280 and 310 grams, shorter than an adult one. The child's height matters more than their age.",
             "Orientativamente una pala junior redonda de entre 280 y 310 gramos, más corta que la de adulto. Cuenta más la altura del niño que la edad.")),
          (L("Da che età si passa alla racchetta da adulto?", "At what age do you move to an adult racket?", "¿A qué edad se pasa a la pala de adulto?"),
           L("In genere verso i 13–15 anni, quando il ragazzo gestisce 330–360 grammi senza fatica; prima conviene restare su modelli junior o adulti molto leggeri.",
             "Usually around 13–15, when the child can handle 330–360 grams without strain; before that it is better to stick to junior or very light adult models.",
             "Normalmente hacia los 13–15 años, cuando el chico maneja 330–360 gramos sin esfuerzo; antes conviene seguir con modelos junior o de adulto muy ligeros.")),
          (L("Meglio una racchetta junior o una da adulto leggera?", "Junior racket or light adult racket?", "¿Mejor una pala junior o una de adulto ligera?"),
           L("Sotto i 12 anni una junior: è più corta e leggera. Dopo, una racchetta da adulto leggera (340–355 g) è spesso la scelta migliore.",
             "Under 12, a junior: it is shorter and lighter. After that, a light adult racket (340–355 g) is often the best choice.",
             "Por debajo de los 12 años, una junior: es más corta y ligera. Después, una pala de adulto ligera (340–355 g) suele ser la mejor opción."))]
    rows = [(L("4–6 anni", "4–6 years", "4–6 años"), L("sotto 1,10 m", "under 1.10 m", "menos de 1,10 m"), L("sotto 280 g", "under 280 g", "menos de 280 g"), L("Rotonda", "Round", "Redonda")),
            (L("7–9 anni", "7–9 years", "7–9 años"), L("1,10–1,35 m", "1.10–1.35 m", "1,10–1,35 m"), "280–310 g", L("Rotonda", "Round", "Redonda")),
            (L("10–12 anni", "10–12 years", "10–12 años"), L("1,35–1,55 m", "1.35–1.55 m", "1,35–1,55 m"), "310–340 g", L("Rotonda o goccia", "Round or teardrop", "Redonda o lágrima")),
            (L("13–15 anni", "13–15 years", "13–15 años"), L("oltre 1,55 m", "over 1.55 m", "más de 1,55 m"), "330–360 g", L("Rotonda o goccia", "Round or teardrop", "Redonda o lágrima")),
            (L("16 anni e oltre", "16 and over", "16 años o más"), L("adulto", "adult", "adulto"), L("come un adulto", "as an adult", "como un adulto"), L("come un adulto", "as an adult", "como un adulto"))]
    tab = (f'<table class="tab"><thead><tr><th>{L("Età indicativa", "Approx. age", "Edad orientativa")}</th><th>{L("Altezza", "Height", "Altura")}</th><th>{L("Peso consigliato", "Recommended weight", "Peso recomendado")}</th><th>{L("Forma", "Shape", "Forma")}</th></tr></thead><tbody>\n'
           + "\n".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in rows) + "</tbody></table>")
    cr, ld = crumbs([H(), (L("Bambini", "Kids", "Niños"), None)])
    corpo = f'''{cr}
<div class="intro"><h1>{L("Racchette da padel per bambini e ragazzi", "Padel rackets for kids and teenagers", "Palas de pádel para niños y jóvenes")}</h1><p>{L("Una racchetta troppo pesante rovina la tecnica e affatica il braccio: per i più piccoli servono modelli junior, più corti e leggeri. Ecco come scegliere la misura giusta e i modelli junior delle collezioni 2026 e 2027.",
       "A racket that is too heavy ruins technique and tires the arm: young children need junior models, shorter and lighter. Here is how to choose the right size, plus the junior models from the 2026 and 2027 collections.",
       "Una pala demasiado pesada estropea la técnica y cansa el brazo: los más pequeños necesitan modelos junior, más cortos y ligeros. Así se elige la medida adecuada, y estos son los modelos junior de las colecciones 2026 y 2027.")}</p></div>
<div class="prose"><h2>{L("Che misura scegliere", "Which size to choose", "Qué medida elegir")}</h2><div class="tablebox">{tab}</div>
<p class="note">{L("Indicazioni orientative tratte dalla", "Indicative guidance from", "Indicaciones orientativas tomadas de la")} <a href="https://padelshop.com/en-it/collections/padel-racket-kids" rel="nofollow noopener" target="_blank">{L("guida taglie di Padelshop", "Padelshop's size guide", "guía de tallas de Padelshop")}</a>{L("; l'altezza conta più dell'età.", "; height matters more than age.", "; la altura cuenta más que la edad.")}</p>
{faq_html(qa)}</div>
<section class="block"><h2>{L("Racchette junior nel database", "Junior rackets in the database", "Palas junior en la base de datos")} ({len(items)})</h2>{griglia(ordina(items))}
<p class="note">{L(f"Per i ragazzi che passano alla racchetta da adulto vedi la <a href=\"{P('guide', 'racchetta-padel-principianti')}\">guida per principianti</a> e le <a href=\"{P('guide', 'racchette-padel-donna')}\">racchette leggere femminili</a>.",
                   f"For teenagers moving to an adult racket see the <a href=\"{P('guide', 'racchetta-padel-principianti')}\">beginner's guide</a> and the <a href=\"{P('guide', 'racchette-padel-donna')}\">light women's rackets</a>.",
                   f"Para los chicos que pasan a la pala de adulto mira la <a href=\"{P('guide', 'racchetta-padel-principianti')}\">guía para principiantes</a> y las <a href=\"{P('guide', 'racchette-padel-donna')}\">palas ligeras femeninas</a>.")}</p></section>'''
    path = P("bambini")
    scrivi(path, pagina(L("Racchetta da padel per bambini: quale scegliere in base all'età | PadelMetrix", "Padel racket for kids: which one to choose by age | PadelMetrix",
                          "Pala de pádel para niños: cuál elegir según la edad | PadelMetrix"),
                        L("Come scegliere la racchetta da padel per bambini e ragazzi: peso e misura per età e altezza, e i modelli junior 2026 e 2027.",
                          "How to choose a padel racket for kids and teenagers: weight and size by age and height, plus the 2026 and 2027 junior models.",
                          "Cómo elegir la pala de pádel para niños y jóvenes: peso y medida según edad y altura, y los modelos junior 2026 y 2027."),
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
