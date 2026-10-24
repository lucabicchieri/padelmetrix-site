#!/usr/bin/env python3
"""Genera le pagine italiane di sezione: Racchette (con filtri), marche, confronti, guide, Bambini, giocatori."""
import json
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from sito import (ROOT, SITO, e, carica, coppie, confronto_url, crumbs, pagina, griglia, ordina,  # noqa: E402
                  FORMA_IT, LIV_IT, STILE_IT, LIV, slugify)

IT = ROOT / "it"
PAGINE = []  # (path, lastmod) per la sitemap


def scrivi(path, html_txt):
    dest = ROOT / path.strip("/") / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html_txt, encoding="utf-8")
    PAGINE.append(path)


def euro(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".").replace(",00", "") + " €"


# ---------------------------------------------------------------- Racchette (elenco con filtri)

FILTRI_JS = """<script>
(function(){
var q=new URLSearchParams(location.search);var f=document.getElementById('filtri');if(!f)return;
var cards=[].slice.call(document.querySelectorAll('.rgrid .rcard'));var out=document.getElementById('conta');
['marca','forma','livello','stile','cat','prezzo','q'].forEach(function(k){var el=f.elements[k];if(el&&q.get(k))el.value=q.get(k);});
function run(){var v={};['marca','forma','livello','stile','cat','prezzo','q'].forEach(function(k){v[k]=(f.elements[k].value||'').toLowerCase();});
var n=0;cards.forEach(function(c){var d=c.dataset,ok=true;
if(v.marca&&d.marca!==v.marca)ok=false;if(v.forma&&d.forma!==v.forma)ok=false;if(v.livello&&d.livello!==v.livello)ok=false;
if(v.stile&&d.stile!==v.stile)ok=false;if(v.cat&&d.cat!==v.cat)ok=false;
if(v.prezzo&&(!d.prezzo||parseFloat(d.prezzo)>parseFloat(v.prezzo)))ok=false;if(v.q&&d.nome.indexOf(v.q)<0)ok=false;
c.style.display=ok?'':'none';if(ok)n++;});out.textContent=n+(n===1?' racchetta':' racchette');}
f.addEventListener('input',run);f.addEventListener('change',run);run();})();
</script>"""


def opt(vals, sel_label):
    return f'<option value="">{sel_label}</option>' + "".join(f'<option value="{v}">{e(l)}</option>' for v, l in vals)


def elenco(db):
    marche = sorted({(n["marca_slug"], n["marca"]) for n in db}, key=lambda x: x[1].lower())
    form = f'''<form class="filtri" id="filtri" onsubmit="return false">
<label>Cerca<input name="q" type="search" placeholder="Modello o giocatore"></label>
<label>Marca<select name="marca">{opt(marche, "Tutte")}</select></label>
<label>Forma<select name="forma">{opt([(k, v) for k, v in FORMA_IT.items()], "Tutte")}</select></label>
<label>Livello<select name="livello">{opt([(k, LIV_IT[k]) for k in LIV], "Tutti")}</select></label>
<label>Stile<select name="stile">{opt([(k, v) for k, v in STILE_IT.items()], "Tutti")}</select></label>
<label>Per chi<select name="cat">{opt([("adulto", "Adulto"), ("donna", "Modelli femminili"), ("junior", "Junior")], "Tutti")}</select></label>
<label>Prezzo di listino<select name="prezzo">{opt([("100", "fino a 100 €"), ("150", "fino a 150 €"), ("200", "fino a 200 €"), ("300", "fino a 300 €")], "Qualsiasi")}</select></label>
</form>'''
    cr, ld = crumbs([("Home", "/it/"), ("Racchette", None)])
    nm = len(marche)
    corpo = f'''{cr}
<div class="intro"><h1>Racchette da padel 2026 e 2027</h1>
<p>{len(db)} racchette di {nm} marche con dati tecnici, sintesi delle recensioni e modelli simili. Filtra per marca, forma, livello, stile e prezzo, oppure leggi le <a href="/it/guide/">guide alla scelta</a>.</p></div>
<div class="marche">{"".join(f'<a href="/it/marche/{s}/">{e(m)}</a>' for s, m in marche)}</div>
{form}
<p class="conta" id="conta">{len(db)} racchette</p>
{griglia(ordina(db))}'''
    itemlist = {"@context": "https://schema.org", "@type": "ItemList", "numberOfItems": len(db),
                "itemListElement": [{"@type": "ListItem", "position": i, "url": SITO + n["url"], "name": n["titolo"]} for i, n in enumerate(ordina(db), 1)]}
    scrivi("/it/racchette/", pagina("Racchette da padel 2026 e 2027: schede tecniche, confronti e filtri | PadelMetrix",
                                    f"{len(db)} racchette da padel di {nm} marche: dati tecnici, opinioni e modelli simili. Filtra per livello, forma, peso, prezzo e marca.",
                                    "/it/racchette/", corpo, on="racchette", ld=[ld, itemlist], extra_js=FILTRI_JS))


# ---------------------------------------------------------------- Marche

def marche(db, pairs):
    per_marca = {}
    for n in db:
        per_marca.setdefault((n["marca_slug"], n["marca"]), []).append(n)
    per = {n["slug"]: n for n in db}
    voci = []
    for (ms, m), items in sorted(per_marca.items(), key=lambda kv: -len(kv[1])):
        anni = sorted({n["anno"] for n in items}, reverse=True)
        anni_txt = " e ".join(str(a) for a in sorted(anni))
        forme = {}
        for n in items:
            if n["forma"]:
                forme[n["forma"]] = forme.get(n["forma"], 0) + 1
        forme_txt = ", ".join(f"{c} {FORMA_IT[f].lower()}" for f, c in sorted(forme.items(), key=lambda kv: -kv[1]))
        gioc = sorted({n["giocatore"] for n in items if n["giocatore"] and "ispirata" not in n["giocatore"]})
        junior = [n for n in items if n["categoria"] == "junior"]
        sezioni = ""
        for a in anni:
            sub = ordina([n for n in items if n["anno"] == a])
            sezioni += f'<section class="block"><h2>Racchette {e(m)} {a}</h2>{griglia(sub)}</section>'
        mp = [(x, y) for x, y in pairs if per[x]["marca"] == m or per[y]["marca"] == m]
        conf = ""
        if mp:
            conf = '<section class="block"><h2>Confronti con racchette ' + e(m) + '</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>' for x, y in mp) + "</ul></section>"
        cr, ld = crumbs([("Home", "/it/"), ("Racchette", "/it/racchette/"), (m, None)])
        intro = f"Nel database ci sono {len(items)} racchette {m} delle collezioni {anni_txt}"
        intro += f": {forme_txt}." if forme_txt else "."
        if gioc:
            intro += " Tra i modelli dei giocatori professionisti: " + ", ".join(gioc[:6]) + "."
        if junior:
            intro += f" {len(junior)} {'è un modello junior' if len(junior) == 1 else 'sono modelli junior'}."
        corpo = f'''{cr}
<div class="intro"><h1>Racchette {e(m)} {anni_txt}</h1><p>{e(intro)} Ogni scheda riporta dati tecnici, a chi è adatta e le alternative più vicine.</p></div>
{sezioni}{conf}'''
        title = f"Racchette {m} {anni_txt}: tutti i {len(items)} modelli a confronto | PadelMetrix"
        desc = f"Tutte le racchette da padel {m} {anni_txt}: {len(items)} schede con peso, forma, livello, opinioni e confronti tra modelli."
        scrivi(f"/it/marche/{ms}/", pagina(title, desc, f"/it/marche/{ms}/", corpo, on="racchette", ld=[ld]))
        voci.append((ms, m, len(items)))
    cr, ld = crumbs([("Home", "/it/"), ("Marche", None)])
    corpo = f'''{cr}<div class="intro"><h1>Marche di racchette da padel</h1><p>Le {len(voci)} marche presenti nel database, con tutti i modelli delle collezioni 2026 e 2027.</p></div>
<ul class="lista-link">{"".join(f'<li><a href="/it/marche/{s}/">Racchette {e(m)}</a> · {c}</li>' for s, m, c in voci)}</ul>'''
    scrivi("/it/marche/", pagina("Marche di racchette da padel: Bullpadel, Nox, Adidas, Head e altre | PadelMetrix",
                                 "Tutte le marche di racchette da padel nel database PadelMetrix, con i modelli 2026 e 2027 di ciascuna.",
                                 "/it/marche/", corpo, on="racchette", ld=[ld]))


# ---------------------------------------------------------------- Confronti

RIGHE = [("Marca", lambda n: n["marca"]), ("Collezione", lambda n: str(n["anno"])), ("Giocatore", lambda n: n["giocatore"]),
         ("Forma", lambda n: FORMA_IT.get(n["forma"])), ("Peso", lambda n: n["peso"]),
         ("Bilanciamento", lambda n: n["bilanciamento"] if isinstance(n["bilanciamento"], str) else None),
         ("Nucleo", lambda n: n["nucleo"] if isinstance(n["nucleo"], str) else None), ("Superficie", lambda n: n["superficie"]),
         ("Tatto", lambda n: n["sensazione"] if isinstance(n["sensazione"], str) else None), ("Livello", lambda n: LIV_IT.get(n["livello"])),
         ("Stile", lambda n: STILE_IT.get(n["stile"])), ("Prezzo di listino", lambda n: euro(n["prezzo"]) if n["prezzo"] else None)]


def verdetto(a, b):
    an, bn = a["nome"], b["nome"]
    frasi = []
    if a["marca"] == b["marca"] and a["modello"] == b["modello"]:
        frasi.append(f"Sono due versioni dello stesso modello: la {an} e la {bn}.")
    comune = []
    if a["forma"] and a["forma"] == b["forma"]:
        comune.append(f"forma {FORMA_IT[a['forma']].lower()}")
    if a["livello"] and a["livello"] == b["livello"]:
        comune.append(f"livello {LIV_IT[a['livello']].lower()}")
    if a["stile"] and a["stile"] == b["stile"]:
        comune.append(f"stile {STILE_IT[a['stile']].lower()}")
    if comune:
        frasi.append("Hanno in comune " + ", ".join(comune) + ".")
    diff = []
    if a["forma"] and b["forma"] and a["forma"] != b["forma"]:
        diff.append(f"la {an} è {FORMA_IT[a['forma']].lower()}, la {bn} {FORMA_IT[b['forma']].lower()}")
    if a["peso"] and b["peso"] and a["peso"] != b["peso"]:
        diff.append(f"pesano {a['peso']} contro {b['peso']}")
    if a["livello"] and b["livello"] and a["livello"] != b["livello"]:
        diff.append(f"il livello indicato è {LIV_IT[a['livello']].lower()} per la prima e {LIV_IT[b['livello']].lower()} per la seconda")
    if a["prezzo"] and b["prezzo"] and abs(a["prezzo"] - b["prezzo"]) >= 20:
        c = a if a["prezzo"] < b["prezzo"] else b
        diff.append(f"la {c['nome']} costa meno di listino ({euro(min(a['prezzo'], b['prezzo']))} contro {euro(max(a['prezzo'], b['prezzo']))})")
    if diff:
        frasi.append("Le differenze principali: " + "; ".join(diff) + ".")
    elif not comune:
        frasi.append("I dati dichiarati sono vicini: conviene guardare le schede complete.")
    return " ".join(frasi)


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
        righe += f'<tr><td>{e(nm)}</td><td>{str(x).replace(".", ",")}</td><td>{str(y).replace(".", ",")}</td></tr>'
    if not righe:
        return ""
    fonte = va["titolo"].replace("Valutazioni di ", "").replace("Valutazioni del ", "")
    return f'''<h2>Punteggi a confronto</h2><div class="tablebox"><table class="tab"><thead><tr><th>{e(va["titolo"])} (su {va["scala"]})</th><th>{e(a["nome"])}</th><th>{e(b["nome"])}</th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">Punteggi pubblicati da fonti esterne ({e(fonte)}), riportati come sono. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.</p>'''


def confronti(db, pairs):
    per = {n["slug"]: n for n in db}
    for x, y in pairs:
        a, b = per[x], per[y]
        righe = ""
        for lab, fn in RIGHE:
            va, vb = fn(a), fn(b)
            if va or vb:
                righe += f"<tr><td>{lab}</td><td>{e(va or '—')}</td><td>{e(vb or '—')}</td></tr>"
        pa, pb = a["d"]["pagina"], b["d"]["pagina"]
        def scelta(p, q):
            v = [t for t in p.get("adatta", []) if t not in q.get("adatta", [])] + [t for t in p.get("pro", []) if t not in q.get("pro", [])]
            return (v or p.get("adatta", []))[:3]
        ad_a, ad_b = scelta(pa, pb), scelta(pb, pa)
        altri = [(p, q) for p, q in pairs if (p, q) != (x, y) and ({p, q} & {x, y})][:8]
        altri_html = ""
        if altri:
            altri_html = '<h2>Altri confronti</h2><ul class="lista-link">' + "".join(
                f'<li><a href="{confronto_url(p, q)}">{e(per[p]["nome"])} vs {e(per[q]["nome"])}</a></li>' for p, q in altri) + "</ul>"
        path = confronto_url(x, y)
        tit = f"{a['titolo']} vs {b['titolo']}"
        cr, ld = crumbs([("Home", "/it/"), ("Confronta", "/it/confronta/"), (f"{a['nome']} vs {b['nome']}", None)])
        corpo = f'''{cr}
<div class="intro"><h1>{e(a["nome"])} vs {e(b["nome"])}</h1><p>{e(verdetto(a, b))}</p></div>
<div class="prose" style="max-width:none">
<h2>Dati tecnici a confronto</h2>
<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="{a["url"]}">{e(a["titolo"])}</a></th><th><a href="{b["url"]}">{e(b["titolo"])}</a></th></tr></thead><tbody>{righe}</tbody></table></div>
<p class="note">Dati dalle schede PadelMetrix, che citano le fonti di ogni valore. "—" indica un dato non dichiarato.</p>
{barre_doppie(a, b)}
<h2>Quale scegliere</h2>
<div class="vs">
<div class="card"><h2>Scegli la {e(a["nome"])} se</h2><ul class="clean">{"".join(f"<li>{e(t)}</li>" for t in ad_a)}</ul><p><a href="{a["url"]}">Scheda completa della {e(a["nome"])}</a></p></div>
<div class="card"><h2>Scegli la {e(b["nome"])} se</h2><ul class="clean">{"".join(f"<li>{e(t)}</li>" for t in ad_b)}</ul><p><a href="{b["url"]}">Scheda completa della {e(b["nome"])}</a></p></div>
</div>
{altri_html}
</div>'''
        desc = f"{tit}: differenze di peso, forma, livello e prezzo, punteggi e quale scegliere in base al tuo gioco."
        scrivi(path, pagina(f"{tit}: differenze e quale scegliere | PadelMetrix", desc[:300], path, corpo, on="confronta", ld=[ld]))

    # hub con strumento
    indice = [{k: n[k] for k in ("slug", "titolo", "nome", "marca", "anno", "peso", "livello", "stile", "forma", "prezzo", "giocatore", "superficie")} for n in ordina(db)]
    for i in indice:
        i["livello"] = LIV_IT.get(i["livello"])
        i["stile"] = STILE_IT.get(i["stile"])
        i["forma"] = FORMA_IT.get(i["forma"])
    pairkeys = [f"{x}|{y}" for x, y in pairs]
    opts = "".join(f'<option value="{n["slug"]}">{e(n["titolo"])}</option>' for n in sorted(db, key=lambda n: n["titolo"]))
    tool_js = "<script>var IDX=" + json.dumps(indice, ensure_ascii=False) + ";var PAIRS=" + json.dumps(pairkeys) + """;
(function(){var s1=document.getElementById('r1'),s2=document.getElementById('r2'),out=document.getElementById('cmp-out');
var q=new URLSearchParams(location.search).get('r');if(q){var p=q.split(',');if(p[0])s1.value=p[0];if(p[1])s2.value=p[1];}
var L=[['Marca','marca'],['Collezione','anno'],['Giocatore','giocatore'],['Forma','forma'],['Peso','peso'],['Superficie','superficie'],['Livello','livello'],['Stile','stile'],['Prezzo di listino','prezzo']];
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function get(s){for(var i=0;i<IDX.length;i++)if(IDX[i].slug===s)return IDX[i];return null;}
function run(){var a=get(s1.value),b=get(s2.value);if(!a||!b||a===b){out.innerHTML='';return;}
var h='<div class="tablebox"><table class="tab"><thead><tr><th></th><th><a href="/it/racchette/'+a.slug+'/">'+esc(a.titolo)+'</a></th><th><a href="/it/racchette/'+b.slug+'/">'+esc(b.titolo)+'</a></th></tr></thead><tbody>';
L.forEach(function(r){var x=a[r[1]],y=b[r[1]];if(r[1]==='prezzo'){x=x?x+' €':null;y=y?y+' €':null;}if(x||y)h+='<tr><td>'+r[0]+'</td><td>'+esc(x||'—')+'</td><td>'+esc(y||'—')+'</td></tr>';});
h+='</tbody></table></div>';var k=[a.slug,b.slug].sort().join('|');if(PAIRS.indexOf(k)>=0){var u='/it/confronta/'+[a.slug,b.slug].sort().join('-vs-')+'/';h+='<p><a class="btn" href="'+u+'">Leggi il confronto completo</a></p>';}
out.innerHTML=h;}
s1.addEventListener('change',run);s2.addEventListener('change',run);run();})();
</script>"""
    elenco_c = '<ul class="lista-link">' + "".join(
        f'<li><a href="{confronto_url(x, y)}">{e(per[x]["nome"])} vs {e(per[y]["nome"])}</a></li>'
        for x, y in sorted(pairs, key=lambda p: (per[p[0]]["marca"], per[p[0]]["nome"]))) + "</ul>"
    cr, ld = crumbs([("Home", "/it/"), ("Confronta", None)])
    corpo = f'''{cr}
<div class="intro"><h1>Confronta racchette da padel</h1><p>Scegli due racchette e guarda subito dove si differenziano: peso, forma, materiali, livello e prezzo. Sotto trovi i {len(pairs)} confronti più cercati, già spiegati.</p></div>
<form class="cmp-tool" onsubmit="return false"><select id="r1" aria-label="Prima racchetta"><option value="">Prima racchetta</option>{opts}</select>
<select id="r2" aria-label="Seconda racchetta"><option value="">Seconda racchetta</option>{opts}</select></form>
<div id="cmp-out"></div>
<section class="block"><h2>Confronti più cercati</h2>{elenco_c}</section>'''
    scrivi("/it/confronta/", pagina("Confronto racchette padel: metti a confronto due modelli | PadelMetrix",
                                    f"Confronta due racchette da padel per peso, forma, materiali, livello e prezzo. {len(pairs)} confronti già spiegati tra i modelli 2026 e 2027.",
                                    "/it/confronta/", corpo, on="confronta", ld=[ld], extra_js=tool_js))


# ---------------------------------------------------------------- Guide

def guida(path, title, desc, h1, crumb, intro_html, corpo_html, items, on="guide", ld_extra=()):
    cr, ld = crumbs([("Home", "/it/"), ("Guide", "/it/guide/"), (crumb, None)])
    lista = f'<section class="block"><h2>Le racchette del database adatte ({len(items)})</h2>{griglia(ordina(items))}</section>' if items else ""
    corpo = f'''{cr}
<div class="intro"><h1>{e(h1)}</h1>{intro_html}<p class="note">Aggiornata il 24 ottobre 2026 · a cura di <a href="/it/chi-siamo/">Luca Bicchieri, PadelMetrix</a></p></div>
<div class="prose">{corpo_html}</div>
{lista}'''
    scrivi(path, pagina(title, desc, path, corpo, on=on, ld=[ld, *ld_extra]))


def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}


def faq_html(qa):
    return '<h2>Domande frequenti</h2><div class="faq">' + "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa) + "</div>"


def guide(db):
    adulti = [n for n in db if n["categoria"] != "junior"]
    G = []

    # principianti
    items = [n for n in adulti if n["livello"] in ("principiante", "principiante-intermedio")]
    qa = [("Che forma deve avere una racchetta da padel per principianti?", "Meglio rotonda o a goccia: lo sweet spot è più centrato e la racchetta perdona di più i colpi decentrati."),
          ("Quanto deve pesare la prima racchetta da padel?", "Per un adulto di solito tra 350 e 365 grammi; chi ha poca forza o fastidi al braccio può scendere verso i 340."),
          ("Meglio fibra di vetro o carbonio per iniziare?", "La fibra di vetro è più morbida ed economica e aiuta a far uscire la palla; il carbonio è più rigido e preciso, adatto quando la tecnica è più solida.")]
    guida("/it/guide/racchetta-padel-principianti/", "Racchetta da padel per principianti: come sceglierla e i modelli 2026 | PadelMetrix",
          "Come scegliere la prima racchetta da padel: forma, peso, materiali e prezzo. Più l'elenco dei modelli 2026 e 2027 adatti a chi inizia.",
          "Racchetta da padel per principianti", "Principianti",
          "<p><b>La racchetta giusta per un principiante è rotonda o a goccia, pesa 350–365 g, ha bilanciamento basso o medio e una superficie morbida in fibra di vetro o carbonio leggero; costa in genere 70–150 €.</b> Le racchette da professionisti, rigide e pesanti in testa, rendono l'apprendimento più faticoso.</p>",
          """<h2>I quattro criteri</h2><ol><li><b>Forma rotonda o a goccia.</b> Lo sweet spot è al centro e più ampio.</li><li><b>Peso 350–365 g.</b> Abbastanza stabile, non affatica il braccio.</li><li><b>Bilanciamento basso o medio.</b> Più maneggevole nelle volée e in difesa.</li><li><b>Fibra di vetro o carbonio morbido.</b> Tatto più confortevole e uscita di palla facile.</li></ol>
<p>Sul prezzo: per iniziare non serve spendere più di 100–150 €. Vedi anche le <a href="/it/guide/racchette-padel-economiche/">racchette economiche</a> e le <a href="/it/guide/forme-racchetta-padel/">differenze tra le forme</a>.</p>""" + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("/it/guide/racchetta-padel-principianti/", "Racchetta da padel per principianti", len(items)))

    # gomito
    items = [n for n in adulti if isinstance(n["sensazione"], str) and "morbid" in n["sensazione"].lower()
             and (n["forma"] != "diamante" or any(w in n["nome"].lower() for w in ("comfort", "soft", "cmf")))]
    qa = [("Quale racchetta da padel scegliere con l'epicondilite?", "In generale si consigliano racchette dal tatto morbido, non troppo pesanti e con bilanciamento basso o medio, che trasmettono meno vibrazioni al braccio. La scelta va comunque fatta con il proprio medico o fisioterapista."),
          ("Le racchette a diamante sono sconsigliate per il gomito?", "Le diamante rigide e pesanti in testa sollecitano di più l'avambraccio. Esistono versioni Comfort o Soft più morbide, ma per chi ha dolore conviene partire da rotonde o a goccia."),
          ("Il peso conta per il gomito?", "Una racchetta troppo leggera vibra di più, una troppo pesante affatica: di solito si resta nella fascia media, intorno ai 350–365 grammi.")]
    guida("/it/guide/racchetta-padel-epicondilite/", "Racchetta da padel per epicondilite e gomito del tennista: come sceglierla | PadelMetrix",
          "Racchette da padel per chi soffre di epicondilite: tatto morbido, peso e bilanciamento giusti, e i modelli 2026 e 2027 più confortevoli per il braccio.",
          "Racchetta da padel per epicondilite e gomito", "Epicondilite e gomito",
          "<p><b>Con l'epicondilite conviene una racchetta dal tatto morbido, di 350–365 g, rotonda o a goccia e con bilanciamento basso o medio, che trasmette meno vibrazioni al braccio.</b> La racchetta non cura il gomito, ma può evitare di peggiorarlo. Questa pagina non sostituisce il parere di un medico o di un fisioterapista.</p>",
          """<h2>Cosa guardare nella scheda</h2><ul><li><b>Tatto:</b> morbido o medio-morbido. Le gomme EVA soft e le superfici in fibra di vetro assorbono più vibrazioni.</li><li><b>Forma:</b> rotonda o a goccia; le diamante concentrano il peso in testa.</li><li><b>Peso e bilanciamento:</b> 350–365 g, bilanciamento basso o medio.</li><li><b>Versioni Comfort e Soft:</b> molti marchi le propongono accanto al modello rigido, con gli stessi stampi ma materiali più morbidi.</li></ul>
<p>Nell'elenco sotto trovi le racchette del database con tatto dichiarato morbido o medio-morbido.</p>""" + faq_html(qa),
          items, ld_extra=[faq_ld(qa)])
    G.append(("/it/guide/racchetta-padel-epicondilite/", "Racchetta da padel per epicondilite e gomito", len(items)))

    # forme
    conta = {f: [n for n in adulti if n["forma"] == f] for f in ("rotonda", "goccia", "diamante", "ibrida")}
    qa = [("Meglio una racchetta da padel rotonda o a diamante?", "Rotonda se cerchi controllo, tolleranza e gioco da fondo campo; diamante se giochi spesso a rete e vuoi potenza nello smash, con una tecnica già solida."),
          ("Cos'è una racchetta a goccia?", "Una forma intermedia: il peso è leggermente spostato verso la testa, per un compromesso tra controllo e potenza. È la scelta più versatile."),
          ("Cosa vuol dire racchetta ibrida?", "È il nome che molti marchi usano per stampi tra goccia e diamante, o tra goccia e rotonda: il carattere dipende dal modello.")]
    sez = ""
    testi = {"rotonda": "Sweet spot centrato e peso verso il manico: la forma del controllo e della difesa, adatta a principianti e a chi costruisce il punto.",
             "goccia": "Peso leggermente in testa e sweet spot un po' più alto: la forma polivalente, buona per la maggior parte dei giocatori.",
             "diamante": "Testa più larga in alto e bilanciamento alto: la forma dell'attacco, per chi chiude i punti a rete e ha già una buona tecnica.",
             "ibrida": "Stampi intermedi che ogni marca interpreta a modo suo, di solito tra goccia e diamante."}
    for f, its in conta.items():
        sez += f'<h2>Racchette {FORMA_IT[f].lower()} ({len(its)} nel database)</h2><p>{testi[f]} <a href="/it/racchette/?forma={f}">Vedi tutte le racchette {FORMA_IT[f].lower()}</a>.</p>'
    guida("/it/guide/forme-racchetta-padel/", "Racchetta da padel rotonda, a goccia o a diamante: differenze e come scegliere | PadelMetrix",
          "Differenze tra racchetta da padel rotonda, a goccia, a diamante e ibrida: controllo, potenza, sweet spot e quale scegliere per il tuo livello.",
          "Racchetta rotonda, a goccia o a diamante?", "Forme delle racchette",
          "<p><b>La racchetta rotonda dà controllo e tolleranza, quella a diamante potenza nello smash, quella a goccia sta in mezzo ed è la più versatile.</b> La forma decide dove sta lo sweet spot e come è distribuito il peso, e quindi il carattere della racchetta.</p>",
          sez + faq_html(qa), [], ld_extra=[faq_ld(qa)])
    G.append(("/it/guide/forme-racchetta-padel/", "Racchetta rotonda, a goccia o a diamante?", None))

    # donna
    items = [n for n in adulti if n["donna"]]
    guida("/it/guide/racchette-padel-donna/", "Racchette da padel da donna 2026 e 2027: i modelli femminili | PadelMetrix",
          "Le racchette da padel da donna delle collezioni 2026 e 2027: modelli delle giocatrici professioniste, pesi, forme e livelli.",
          "Racchette da padel da donna", "Racchette da donna",
          "<p>Le racchette femminili sono in genere più leggere (spesso 340–360 g) e più maneggevoli, ma non sono obbligatorie: conta il peso che riesci a gestire senza affaticare il braccio. Qui trovi i modelli che i marchi presentano come femminili, molti firmati da giocatrici professioniste.</p>",
          "<p>Se cerchi una racchetta leggera senza limitarti ai modelli femminili, usa il filtro per livello e forma nella <a href=\"/it/racchette/\">pagina Racchette</a>.</p>", items)
    G.append(("/it/guide/racchette-padel-donna/", "Racchette da padel da donna", len(items)))

    # economiche
    items = [n for n in adulti if n["prezzo"] and n["prezzo"] <= 130]
    guida("/it/guide/racchette-padel-economiche/", "Racchette da padel economiche sotto 130 euro: modelli 2026 e 2027 | PadelMetrix",
          "Racchette da padel economiche con prezzo di listino fino a 130 euro: modelli per principianti e intermedi delle marche principali.",
          "Racchette da padel economiche (fino a 130 € di listino)", "Racchette economiche",
          "<p>Il prezzo di listino è solo un riferimento: online molte racchette costano il 20–40% in meno, quindi anche modelli con listino più alto possono rientrare nel tuo budget. Qui trovi quelle con listino fino a 130 €.</p>",
          "<p>A questo prezzo prevalgono superfici in fibra di vetro e forme rotonde o a goccia: ottime per iniziare e per giocare con regolarità. Vedi anche la <a href=\"/it/guide/racchetta-padel-principianti/\">guida per principianti</a>.</p>", items)
    G.append(("/it/guide/racchette-padel-economiche/", "Racchette da padel economiche", len(items)))

    # controllo / potenza
    for st, slug, h1, txt in (("controllo", "racchette-padel-controllo", "Racchette da padel di controllo",
                               "Le racchette di controllo privilegiano precisione, sweet spot ampio e maneggevolezza. Di solito sono rotonde o a goccia con bilanciamento basso: ideali per chi gioca da fondo campo e costruisce il punto."),
                              ("offensivo", "racchette-padel-potenza", "Racchette da padel di potenza",
                               "Le racchette di potenza hanno il peso spostato in testa e una superficie più rigida: aiutano a chiudere i punti con smash e volée, ma chiedono tecnica e sono meno tolleranti in difesa.")):
        items = [n for n in adulti if n["stile"] == st]
        guida(f"/it/guide/{slug}/", f"{h1} 2026 e 2027: come sceglierle e i modelli | PadelMetrix",
              f"{h1}: caratteristiche, a chi sono adatte e tutti i modelli 2026 e 2027 nel database PadelMetrix.",
              h1, h1, f"<p>{txt}</p>", f'<p>Non sai quale stile fa per te? Leggi la guida alle <a href="/it/guide/forme-racchetta-padel/">forme delle racchette</a>.</p>', items)
        G.append((f"/it/guide/{slug}/", h1, len(items)))

    # giocatori
    gioc = {}
    for n in db:
        g = n["giocatore"]
        if g and "ispirata" not in g:
            gioc.setdefault(g, []).append(n)
    righe = "".join(f'<tr><td>{e(g)}</td><td>{", ".join(f"<a href=\"{n["url"]}\">{e(n["titolo"])}</a>" for n in ordina(its))}</td></tr>'
                    for g, its in sorted(gioc.items(), key=lambda kv: kv[0]))
    cr, ld = crumbs([("Home", "/it/"), ("Guide", "/it/guide/"), ("Racchette dei professionisti", None)])
    corpo = f'''{cr}<div class="intro"><h1>Le racchette dei giocatori professionisti</h1><p>Con che racchetta giocano Tapia, Coello, Galán, Lebrón, Chingotto e gli altri: i modelli firmati dai professionisti nelle collezioni 2026 e 2027. Le versioni in vendita sono quelle dei negozi; i professionisti possono usare racchette personalizzate.</p></div>
<div class="tablebox"><table class="tab"><thead><tr><th>Giocatore</th><th>Racchetta</th></tr></thead><tbody>{righe}</tbody></table></div>'''
    scrivi("/it/guide/racchette-giocatori-professionisti/", pagina("Con che racchetta giocano i professionisti del padel? Modelli 2026 e 2027 | PadelMetrix",
           "Le racchette firmate dai giocatori professionisti di padel: Agustín Tapia, Arturo Coello, Ale Galán, Juan Lebrón, Fede Chingotto e altri.",
           "/it/guide/racchette-giocatori-professionisti/", corpo, on="guide", ld=[ld]))
    G.append(("/it/guide/racchette-giocatori-professionisti/", "Le racchette dei giocatori professionisti", None))

    # hub guide
    cr, ld = crumbs([("Home", "/it/"), ("Guide", None)])
    voci = "".join(f'<li><a href="{p}">{e(t)}</a>{f" · {c} racchette" if c else ""}</li>' for p, t, c in G)
    corpo = f'''{cr}<div class="intro"><h1>Guide alla scelta della racchetta da padel</h1><p>Guide pratiche per trovare la racchetta giusta in base a livello, stile di gioco, budget e problemi fisici. Ogni guida rimanda alle schede dei modelli adatti.</p></div>
<ul class="lista-link">{voci}<li><a href="/it/bambini/">Racchette da padel per bambini e ragazzi</a></li></ul>'''
    scrivi("/it/guide/", pagina("Guide alla scelta della racchetta da padel | PadelMetrix",
                                "Come scegliere la racchetta da padel: guide per principianti, epicondilite, forme, donne, bambini, budget e racchette dei professionisti.",
                                "/it/guide/", corpo, on="guide", ld=[ld]))


# ---------------------------------------------------------------- Bambini

def bambini(db):
    items = [n for n in db if n["categoria"] == "junior"]
    qa = [("Che racchetta da padel per un bambino di 8 anni?", "Indicativamente una racchetta junior rotonda tra 280 e 310 grammi, più corta di quella da adulto. Conta più l'altezza del bambino che l'età."),
          ("Da che età si passa alla racchetta da adulto?", "In genere verso i 13–15 anni, quando il ragazzo gestisce 330–360 grammi senza fatica; prima conviene restare su modelli junior o adulti molto leggeri."),
          ("Meglio una racchetta junior o una da adulto leggera?", "Sotto i 12 anni una junior: è più corta e leggera. Dopo, una racchetta da adulto leggera (340–355 g) è spesso la scelta migliore.")]
    tab = """<table class="tab"><thead><tr><th>Età indicativa</th><th>Altezza</th><th>Peso consigliato</th><th>Forma</th></tr></thead><tbody>
<tr><td>4–6 anni</td><td>sotto 1,10 m</td><td>sotto 280 g</td><td>Rotonda</td></tr>
<tr><td>7–9 anni</td><td>1,10–1,35 m</td><td>280–310 g</td><td>Rotonda</td></tr>
<tr><td>10–12 anni</td><td>1,35–1,55 m</td><td>310–340 g</td><td>Rotonda o goccia</td></tr>
<tr><td>13–15 anni</td><td>oltre 1,55 m</td><td>330–360 g</td><td>Rotonda o goccia</td></tr>
<tr><td>16 anni e oltre</td><td>adulto</td><td>come un adulto</td><td>come un adulto</td></tr></tbody></table>"""
    cr, ld = crumbs([("Home", "/it/"), ("Bambini", None)])
    corpo = f'''{cr}
<div class="intro"><h1>Racchette da padel per bambini e ragazzi</h1><p>Una racchetta troppo pesante rovina la tecnica e affatica il braccio: per i più piccoli servono modelli junior, più corti e leggeri. Ecco come scegliere la misura giusta e i modelli junior delle collezioni 2026 e 2027.</p></div>
<div class="prose"><h2>Che misura scegliere</h2><div class="tablebox">{tab}</div>
<p class="note">Indicazioni orientative tratte dalla <a href="https://padelshop.com/en-it/collections/padel-racket-kids" rel="nofollow noopener" target="_blank">guida taglie di Padelshop</a>; l'altezza conta più dell'età.</p>
{faq_html(qa)}</div>
<section class="block"><h2>Racchette junior nel database ({len(items)})</h2>{griglia(ordina(items))}
<p class="note">Per i ragazzi che passano alla racchetta da adulto vedi la <a href="/it/guide/racchetta-padel-principianti/">guida per principianti</a> e le <a href="/it/guide/racchette-padel-donna/">racchette leggere femminili</a>.</p></section>'''
    scrivi("/it/bambini/", pagina("Racchetta da padel per bambini: quale scegliere in base all'età | PadelMetrix",
                                  "Come scegliere la racchetta da padel per bambini e ragazzi: peso e misura per età e altezza, e i modelli junior 2026 e 2027.",
                                  "/it/bambini/", corpo, on="bambini", ld=[ld, faq_ld(qa)]))


def main():
    db = carica()
    pairs = coppie(db)
    elenco(db)
    marche(db, pairs)
    confronti(db, pairs)
    guide(db)
    bambini(db)
    (ROOT / "scripts" / "pagine_sezioni.json").write_text(json.dumps(PAGINE, indent=0), encoding="utf-8")
    print(len(PAGINE), "pagine di sezione generate")


if __name__ == "__main__":
    main()
