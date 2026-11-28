#!/usr/bin/env python3
"""Pagina "Offerte" in it/en/es/fr: le racchette e gli accessori del database oggi in sconto su Amazon.

I prezzi non sono scritti nella pagina: il browser li legge da /amazon/immagini.json, aggiornato due volte
al giorno dalla Creators API (prezzo, prezzo precedente e sconto dichiarati da Amazon). Se i dati hanno più
di 24 ore non vengono mostrati, come chiede la licenza Amazon. Lo stesso blocco è usato in home page."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import ROOT, e, L, P, ALT, crumbs, pagina, LINGUE, set_lang, url_r, ordina  # noqa: E402

BF = "27 novembre 2026"

CSS = """<style>
.of-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:16px;margin:18px 0 10px}
.of{position:relative;display:flex;flex-direction:column;background:#fff;border:1px solid var(--line);border-radius:16px;overflow:hidden}
.of .bd{position:absolute;left:10px;top:10px;z-index:2;background:var(--lime);color:var(--green);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:18px;padding:4px 10px;border-radius:999px}
[data-of="r"]:not(.ok){min-height:640px}[data-of]:not(.ok){min-height:330px}.of .im{height:190px;display:flex;align-items:center;justify-content:center;background:#fff;border-bottom:1px solid var(--line)}
.of .im img{max-width:86%;max-height:170px;width:auto;height:auto;object-fit:contain}
.of .tx{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1}
.of .nm{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px;line-height:1.25;color:var(--ink);text-decoration:none}
.of .nm:hover{text-decoration:underline}
.of .pz{margin-top:8px;font-size:15px}.of .pz b{font-family:'Space Grotesk',sans-serif;font-size:24px;color:var(--green)}.of .pz s{color:var(--muted);margin-left:6px}
.of small{color:var(--muted);font-size:12px;line-height:1.3;margin-top:2px}.of small.lv{color:var(--ink2);font-weight:600}
.of .bt{margin-top:auto;padding-top:12px;display:flex;flex-wrap:wrap;gap:8px 12px;align-items:center}
.of .bt .btn{font-size:14px;padding:9px 14px}.of .bt .sc{font-size:14px;color:var(--green);font-weight:600}
.of-chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
.of-chips button{font:inherit;font-size:14px;font-weight:600;padding:7px 14px;border-radius:999px;border:1.5px solid var(--line);background:#fff;color:var(--ink2);cursor:pointer}
.of-chips button.on{background:var(--green);border-color:var(--green);color:#fff}
.of-agg{color:var(--muted);font-size:14px;margin:6px 0 0}
.of-vuoto{background:var(--soft);border-radius:14px;padding:18px;color:var(--ink2)}
.of-tutti{columns:2 320px;column-gap:28px;margin:14px 0;padding:0;list-style:none;font-size:15px}
.of-tutti li{break-inside:avoid;display:flex;justify-content:space-between;gap:10px;padding:7px 0;border-bottom:1px solid var(--line)}
.of-tutti li span{white-space:nowrap;font-weight:600;color:var(--green)}
.of-more{display:block;margin:6px auto 0;cursor:pointer;font:inherit;font-weight:600}
.of-det summary{cursor:pointer;font-weight:600;color:var(--green);padding:8px 0}
@media (max-width:560px){.of-grid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.of .im{height:130px}.of .im img{max-height:116px}.of .tx{padding:10px}.of .nm{font-size:14px}.of .pz b{font-size:19px}.of .pz s{display:block;margin:0}.of .bd{font-size:15px;left:6px;top:6px}.of .bt .btn{width:100%;text-align:center;padding:9px 6px}.of-hero{padding:22px 18px}}
.of-hero{background:var(--green);color:#fff;border-radius:20px;padding:28px 26px;margin:6px 0 8px}
.of-hero h1{color:#fff;margin:0 0 10px}.of-hero p{color:#EAF5EC;margin:0;max-width:760px}.of-hero .k{color:var(--lime);font-family:'Space Grotesk',sans-serif;font-weight:700;letter-spacing:.08em;text-transform:uppercase;font-size:13px;margin-bottom:8px}
</style>"""


def indice(db):
    """ASIN -> dati minimi per le card: nome, link alla scheda, listino, tipo (r racchetta, p pickleball, a accessorio)."""
    out = {}
    for n in db:
        d = json.loads((S.DATA / f'{n["slug"]}.json').read_text(encoding="utf-8"))
        asin = next((s.get("asin") for s in d["pagina"].get("negozi", []) if isinstance(s, dict) and s.get("amazon") and s.get("asin")), None)
        if asin:
            out[asin] = {"k": "r", "t": n["titolo"], "u": url_r(n), "pl": n["prezzo"] or 0, "lv": S.LIVN(n["livello"]) or "", "an": n["anno"]}
    from dati_pickleball import P as PADDLE
    for p in PADDLE:
        if p.get("asin"):
            out[p["asin"]] = {"k": "p", "t": f'{p["marca"]} {p["modello"]}', "u": P("pickleball", p["slug"]), "pl": 0}
    from dati_regali_prodotti import P as REGALI
    for a, r in REGALI.items():
        out.setdefault(a, {"k": "a", "t": r["n"], "u": "", "pl": 0})
    return out


def testi_js():
    return {"am": L("Vedi su Amazon", "View on Amazon", "Ver en Amazon", "Voir sur Amazon"),
            "sc": L("Scheda tecnica →", "Full specs →", "Ficha técnica →", "Fiche technique →"),
            "pa": L("prezzo precedente indicato da Amazon", "previous price shown by Amazon", "precio anterior indicado por Amazon", "prix précédent indiqué par Amazon"),
            "pl": L("rispetto al listino del produttore", "compared with the maker's list price", "respecto al PVP del fabricante", "par rapport au prix catalogue du fabricant"),
            "agg": L("Prezzi Amazon.it aggiornati il {g} alle {h}. Possono cambiare in qualsiasi momento: fa fede il prezzo che vedi su Amazon.",
                     "Amazon.it prices updated on {g} at {h}. They can change at any time: the price you see on Amazon is the one that counts.",
                     "Precios de Amazon.it actualizados el {g} a las {h}. Pueden cambiar en cualquier momento: vale el precio que ves en Amazon.",
                     "Prix Amazon.it mis à jour le {g} à {h}. Ils peuvent changer à tout moment : le prix affiché sur Amazon fait foi."),
            "no": L("In questo momento non riusciamo a mostrare i prezzi aggiornati. Riprova tra qualche ora.",
                    "We can't show up-to-date prices right now. Please try again in a few hours.",
                    "Ahora mismo no podemos mostrar los precios actualizados. Vuelve a intentarlo en unas horas.",
                    "Nous ne pouvons pas afficher les prix à jour pour le moment. Réessayez dans quelques heures."),
            "zero": L("Oggi non ci sono sconti in questa fascia.", "No discounts in this range today.", "Hoy no hay descuentos en este rango.", "Aucune remise dans cette tranche aujourd'hui."),
            "fino": L("fino a −{n}%", "up to −{n}%", "hasta −{n}%", "jusqu'à −{n} %"),
            "more": L("Mostra tutte le {n} offerte", "Show all {n} deals", "Ver las {n} ofertas", "Voir les {n} offres"),
            "lv": L("Livello", "Level", "Nivel", "Niveau"),
            "en": S.lang() == "en"}


# Motore comune a pagina offerte e home: legge i prezzi e disegna le card.
JS = r"""<script>(function(){
var I=window.OF_IDX||{},T=window.OF_TX||{};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fm(x){var s=x.toFixed(2).replace('.',',').replace(/,00$/,'');s=s.replace(/\B(?=(\d{3})+(?!\d))/g,'.');return T.en?'€'+x.toFixed(2).replace(/\.00$/,''):s+' €'}
function card(o){var am='https://www.amazon.it/dp/'+o.a+'?tag=padelmetrix-21',r='rel="sponsored nofollow noopener" target="_blank"';
return '<div class="of"><span class="bd">−'+o.s+'%</span><a class="im" href="'+am+'" '+r+' title="Amazon"><img src="'+o.img+'" alt="'+esc(o.t)+'" width="500" height="500" loading="lazy"></a><div class="tx">'
+(o.u?'<a class="nm" href="'+o.u+'">'+esc(o.t)+'</a>':'<span class="nm">'+esc(o.t)+'</span>')
+(o.lv?'<small class="lv">'+T.lv+': '+esc(o.lv)+'</small>':'')
+'<div class="pz"><b>'+esc(o.pz)+'</b><s>'+esc(o.pr)+'</s></div><small>'+(o.src=='l'?T.pl:T.pa)+'</small>'
+'<div class="bt"><a class="btn lime" href="'+am+'" '+r+'>'+T.am+'</a>'+(o.u?'<a class="sc" href="'+o.u+'">'+T.sc+'</a>':'')+'</div></div></div>'}
fetch('/amazon/immagini.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(j){
var t=Date.parse(j.aggiornato||''),ok=t&&Date.now()-t<864e5,P=j.prodotti||{},all=[],tutti=[];
if(ok)for(var a in I){var x=P[a],i=I[a];if(!x||!x.euro||!x.img)continue;
 var s=x.sconto||0,pr=(x.prima||'').replace(/ /g,' '),src='a';
 if(!s&&i.pl&&x.euro<=i.pl*0.9){s=Math.round((1-x.euro/i.pl)*100);pr=fm(i.pl);src='l'}
 var o={a:a,k:i.k,t:i.t,u:i.u,lv:i.lv,img:x.img,e:x.euro,pz:x.prezzo.replace(/ /g,' '),s:s,pr:pr,src:src};
 if(i.k=='r')tutti.push(o);if(s>=10)all.push(o)}
all.sort(function(p,q){return q.s-p.s||p.e-q.e});
var d=new Date(t),hh=('0'+d.getHours()).slice(-2)+':'+('0'+d.getMinutes()).slice(-2),gg=d.getDate()+'/'+(d.getMonth()+1);
document.querySelectorAll('[data-of-agg]').forEach(function(el){el.textContent=ok?T.agg.replace('{g}',gg).replace('{h}',hh):''});
var mx=0;all.forEach(function(o){if(o.k=='r'&&o.s>mx)mx=o.s});
document.querySelectorAll('[data-of-max]').forEach(function(el){if(mx)el.textContent=T.fino.replace('{n}',mx)});
document.querySelectorAll('[data-of]').forEach(function(box){
 var k=box.getAttribute('data-of'),n=+box.getAttribute('data-n')||999,sec=box.closest('[data-of-sec]');
 var more=box.hasAttribute('data-more');
 function draw(lo,hi){var f=all.filter(function(o){return o.k==k&&o.e>=lo&&o.e<hi}),v=f.slice(0,n);
  box.innerHTML=v.length?v.map(card).join(''):'';box.className=(v.length?'of-grid':'')+' ok';
  var nx=box.nextElementSibling;if(nx&&nx.classList.contains('of-more'))nx.remove();
  if(more&&f.length>v.length){var b=document.createElement('button');b.type='button';b.className='btn out of-more';b.textContent=T.more.replace('{n}',f.length);
   b.onclick=function(){n=999;draw(lo,hi)};box.after(b)}
  if(!v.length&&box.hasAttribute('data-msg'))box.innerHTML='<p class="of-vuoto">'+(ok?T.zero:T.no)+'</p>';return v.length}
 var c=draw(0,1e9);if(sec&&!c&&!box.hasAttribute('data-msg'))sec.style.display='none';else if(sec)sec.style.display='';
 var ch=sec&&sec.querySelector('.of-chips');if(ch)ch.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b)return;
  ch.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});draw(+b.getAttribute('data-lo'),+b.getAttribute('data-hi'))})});
var ul=document.querySelector('[data-of-tutti]');if(ul&&ok){tutti.sort(function(p,q){return p.e-q.e});
 ul.innerHTML=tutti.map(function(o){return '<li><a href="'+o.u+'">'+esc(o.t)+'</a><span>'+esc(o.pz)+'</span></li>'}).join('')}
}).catch(function(){document.querySelectorAll('[data-of][data-msg]').forEach(function(b){b.innerHTML='<p class="of-vuoto">'+T.no+'</p>'});document.querySelectorAll('[data-of]').forEach(function(b){b.classList.add('ok')})})})();</script>"""


def dati_js(db, solo=None):
    idx = indice(db)
    if solo:
        idx = {a: v for a, v in idx.items() if v["k"] in solo}
    return "<script>window.OF_IDX=" + json.dumps(idx, ensure_ascii=False) + ";window.OF_TX=" + json.dumps(testi_js(), ensure_ascii=False) + ";</script>"


def FASE():
    """'cyber' fino a lunedì 30 novembre 2026 (ora di Roma), poi 'dopo': la pagina Black Friday resta online
    con lo stesso indirizzo (si riusa ogni anno) ma cambia messaggio e spariscono i banner."""
    import datetime as dt
    import zoneinfo
    oggi = dt.datetime.now(zoneinfo.ZoneInfo("Europe/Rome")).date()
    return "cyber" if oggi <= dt.date(2026, 11, 30) else "dopo"


def blocco_home(db):
    """Sezione per la home: le 4 racchette più scontate oggi. Resta nascosta se non ci sono dati aggiornati."""
    return (CSS + f'''<section class="of-home" data-of-sec style="display:none"><div class="wrap">
<h2>{L("Le offerte di oggi su Amazon", "Today's deals on Amazon", "Las ofertas de hoy en Amazon", "Les offres du jour sur Amazon")}</h2>
<p class="of-agg" data-of-agg></p>
<div data-of="r" data-n="4"></div>
<p style="margin-top:16px;display:flex;flex-wrap:wrap;gap:10px">{_bottone_home()}<a class="btn ln" href="{P("offerte")}">{L("Tutte le offerte padel →", "All padel deals →", "Todas las ofertas de pádel →", "Toutes les offres padel →")}</a></p>
</div></section>''', dati_js(db, solo="r") + JS)


def _bottone_home():
    if FASE() == "dopo":
        return ""
    return f'<a class="btn lime" href="{P("blackfriday")}">{L("Cyber Monday: le 15 più scontate →", "Cyber Monday: the 15 biggest discounts →", "Cyber Monday: las 15 más rebajadas →", "Cyber Monday : les 15 plus remisées →")}</a>'


def striscia_home():
    """Barra sopra l'hero della home (solo fino al Cyber Monday)."""
    if FASE() == "dopo":
        return ""
    return (f'<a class="promo-bar" href="{P("blackfriday")}"><b>Cyber Monday</b> '
            f'{L("Ultimi giorni di offerte sulle racchette da padel", "Last days of padel racket deals", "Últimos días de ofertas en palas de pádel", "Derniers jours de promos sur les raquettes de padel")} '
            f'<span data-of-max></span> · <u>{L("Guarda le offerte", "See the deals", "Ver las ofertas", "Voir les offres")} →</u></a>')
    return (f'<a class="promo-bar" href="{P("blackfriday")}"><b>Black Friday</b> '
            f'{L("Racchette da padel in offerta su Amazon", "Padel rackets on sale at Amazon", "Palas de pádel en oferta en Amazon", "Raquettes de padel en promo sur Amazon")} '
            f'<span data-of-max></span> · <u>{L("Guarda le offerte", "See the deals", "Ver las ofertas", "Voir les offres")} →</u></a>')


def pagina_offerte(db):
    path, alt = P("offerte"), ALT("offerte")
    cr, ld = crumbs([S.home_crumb(), (L("Offerte", "Deals", "Ofertas", "Offres"), None)])
    chips = "".join(f'<button type="button"{" class=\"on\"" if i == 0 else ""} data-lo="{lo}" data-hi="{hi}">{t}</button>' for i, (lo, hi, t) in enumerate([
        (0, 1000000000, L("Tutte", "All", "Todas", "Toutes")), (0, 100, L("Fino a 100 €", "Up to €100", "Hasta 100 €", "Jusqu'à 100 €")),
        (100, 200, L("Da 100 a 200 €", "€100 to €200", "De 100 a 200 €", "De 100 à 200 €")), (200, 1000000000, L("Oltre 200 €", "Over €200", "Más de 200 €", "Plus de 200 €"))]))
    con_asin = [n for n in db if n["slug"] in {v["u"].strip("/").split("/")[-1] for v in indice(db).values() if v["k"] == "r"}]
    qa = [((L("Quando sarà il Black Friday 2027?", "When is Black Friday 2027?", "¿Cuándo será el Black Friday 2027?", "Quand aura lieu le Black Friday 2027 ?"),
           L("Venerdì 26 novembre 2027, con il Cyber Monday lunedì 29 novembre. Su Amazon le offerte di solito iniziano già nei giorni precedenti: questa pagina tornerà con gli sconti del 2027.",
             "Friday 26 November 2027, with Cyber Monday on Monday 29 November. Amazon deals usually start in the days before: this page will come back with the 2027 discounts.",
             "El viernes 26 de noviembre de 2027, con el Cyber Monday el lunes 29 de noviembre. Las ofertas de Amazon suelen empezar unos días antes: esta página volverá con los descuentos de 2027.",
             "Le vendredi 26 novembre 2027, avec le Cyber Monday le lundi 29 novembre. Les offres Amazon commencent généralement quelques jours avant : cette page reviendra avec les remises 2027.")) if FASE() == "dopo" else (L("Quando è il Black Friday 2026?", "When is Black Friday 2026?", "¿Cuándo es el Black Friday 2026?", "Quand a lieu le Black Friday 2026 ?"),
           L("Venerdì 27 novembre 2026. Le offerte su Amazon di solito iniziano già nei giorni precedenti e proseguono fino al Cyber Monday, lunedì 30 novembre.",
             "Friday 27 November 2026. Amazon deals usually start in the days before and run until Cyber Monday, 30 November.",
             "El viernes 27 de noviembre de 2026. Las ofertas de Amazon suelen empezar unos días antes y siguen hasta el Cyber Monday, el lunes 30 de noviembre.",
             "Le vendredi 27 novembre 2026. Les offres Amazon commencent généralement quelques jours avant et durent jusqu'au Cyber Monday, le lundi 30 novembre."))),
          (L("Ogni quanto aggiornate i prezzi?", "How often do you update prices?", "¿Cada cuánto actualizáis los precios?", "À quelle fréquence mettez-vous les prix à jour ?"),
           L("Due volte al giorno, direttamente da Amazon. In pagina trovi sempre il giorno e l'ora dell'ultimo aggiornamento. Il prezzo può cambiare in qualsiasi momento: fa fede quello che vedi su Amazon.",
             "Twice a day, straight from Amazon. The page always shows the day and time of the last update. Prices can change at any time: the one you see on Amazon is the one that counts.",
             "Dos veces al día, directamente desde Amazon. En la página ves siempre el día y la hora de la última actualización. El precio puede cambiar en cualquier momento: vale el que ves en Amazon.",
             "Deux fois par jour, directement depuis Amazon. La page indique toujours le jour et l'heure de la dernière mise à jour. Le prix peut changer à tout moment : celui affiché sur Amazon fait foi.")),
          (L("Come calcolate lo sconto?", "How do you calculate the discount?", "¿Cómo calculáis el descuento?", "Comment calculez-vous la remise ?"),
           L("Usiamo lo sconto e il prezzo precedente dichiarati da Amazon. Quando Amazon non li indica, confrontiamo il prezzo di oggi con il listino del produttore e lo scriviamo sotto il prezzo. Mostriamo solo gli sconti di almeno il 10%.",
             "We use the discount and previous price stated by Amazon. When Amazon doesn't give them, we compare today's price with the maker's list price and say so under the price. We only show discounts of at least 10%.",
             "Usamos el descuento y el precio anterior que indica Amazon. Cuando Amazon no los da, comparamos el precio de hoy con el PVP del fabricante y lo indicamos bajo el precio. Solo mostramos descuentos de al menos el 10 %.",
             "Nous utilisons la remise et le prix précédent indiqués par Amazon. Quand Amazon ne les donne pas, nous comparons le prix du jour au prix catalogue du fabricant et nous le précisons sous le prix. Nous n'affichons que les remises d'au moins 10 %.")),
          (L("Conviene comprare un modello dell'anno scorso?", "Is last year's model worth buying?", "¿Merece la pena comprar un modelo del año pasado?", "Vaut-il la peine d'acheter un modèle de l'an dernier ?"),
           L("Spesso sì: tra un anno e l'altro cambiano soprattutto i colori e pochi dettagli, mentre il prezzo del modello precedente scende molto. Nelle nostre schede trovi il confronto tra le versioni.",
             "Often yes: from one year to the next it's mostly colours and small details that change, while the previous model's price drops a lot. Our racket pages compare the versions.",
             "A menudo sí: de un año a otro cambian sobre todo los colores y pocos detalles, mientras que el precio del modelo anterior baja mucho. En nuestras fichas encuentras la comparación entre versiones.",
             "Souvent oui : d'une année à l'autre, ce sont surtout les couleurs et quelques détails qui changent, alors que le prix du modèle précédent baisse beaucoup. Nos fiches comparent les versions."))]
    faq_h = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in qa)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": S.lang(),
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    elenco = "".join(f'<li><a href="{url_r(n)}">{e(n["titolo"])}</a><span></span></li>' for n in con_asin)
    corpo = f'''{CSS}{cr}
<div class="of-hero"><div class="k">{"Black Friday & Cyber Monday 2026 · " if FASE() == "cyber" else ""}{L("aggiornate ogni giorno", "updated daily", "actualizadas cada día", "mises à jour chaque jour")}</div>
<h1>{L("Offerte padel su Amazon: le racchette in sconto oggi", "Padel deals on Amazon: rackets on sale today", "Ofertas de pádel en Amazon: las palas rebajadas hoy", "Offres padel sur Amazon : les raquettes en promo aujourd'hui")}</h1>
<p>{L(f"Controlliamo due volte al giorno il prezzo Amazon di {len(con_asin)} racchette del nostro database e ti mostriamo solo quelle davvero scontate, dalla più conveniente. Per ogni racchetta trovi anche la scheda tecnica, così sai cosa stai comprando.",
       f"Twice a day we check the Amazon price of {len(con_asin)} rackets in our database and show only the ones that are really discounted, best deal first. Each one links to its full spec page, so you know what you're buying.",
       f"Comprobamos dos veces al día el precio en Amazon de {len(con_asin)} palas de nuestra base de datos y te mostramos solo las que están rebajadas de verdad, de la mejor oferta en adelante. Cada pala tiene su ficha técnica, para que sepas qué compras.",
       f"Deux fois par jour, nous vérifions le prix Amazon de {len(con_asin)} raquettes de notre base et n'affichons que celles réellement remisées, de la meilleure offre à la moins forte. Chaque raquette a sa fiche technique, pour savoir ce que vous achetez.")}</p></div>
{banner_bf()}
<p class="of-agg" data-of-agg></p>
<section data-of-sec><h2>{L("Racchette da padel in offerta", "Padel rackets on sale", "Palas de pádel en oferta", "Raquettes de padel en promo")}</h2>
<div class="of-chips">{chips}</div>
<div data-of="r" data-n="20" data-more data-msg><p class="of-vuoto">{L("Carico i prezzi di oggi…", "Loading today's prices…", "Cargando los precios de hoy…", "Chargement des prix du jour…")}</p></div></section>
<section data-of-sec><h2>{L("Accessori e idee regalo in offerta", "Accessories and gift ideas on sale", "Accesorios e ideas de regalo en oferta", "Accessoires et idées cadeaux en promo")}</h2>
<p>{L(f'Palline, borse, overgrip e gli altri prodotti delle nostre <a href="{P("articoli", "idee-regalo-natale-padel")}">idee regalo di Natale</a> che oggi costano meno.',
       f'Balls, bags, overgrips and the other products from our <a href="{P("articoli", "idee-regalo-natale-padel")}">Christmas gift ideas</a> that cost less today.',
       f'Pelotas, paleteros, overgrips y los demás productos de nuestras <a href="{P("articoli", "idee-regalo-natale-padel")}">ideas de regalo de Navidad</a> que hoy cuestan menos.',
       f'Balles, sacs, surgrips et les autres produits de nos <a href="{P("articoli", "idee-regalo-natale-padel")}">idées cadeaux de Noël</a> qui coûtent moins cher aujourd\'hui.')}</p>
<div data-of="a" data-n="12" data-more></div></section>
<section data-of-sec><h2>{L("Racchette da pickleball in offerta", "Pickleball paddles on sale", "Palas de pickleball en oferta", "Raquettes de pickleball en promo")}</h2>
<div data-of="p"></div></section>
<div class="prose" style="margin-top:30px">
<h2>{L("Come riconoscere una vera offerta", "How to spot a real deal", "Cómo reconocer una oferta de verdad", "Comment reconnaître une vraie bonne affaire")}</h2>
<ul>
<li>{L("<b>Guarda il prezzo finale, non la percentuale.</b> Il prezzo «prima» a volte è un listino che nessuno ha mai pagato. Per questo, quando possiamo, indichiamo da dove arriva il confronto.",
       "<b>Look at the final price, not the percentage.</b> The “before” price is sometimes a list price nobody ever paid. That's why, whenever we can, we say where the comparison comes from.",
       "<b>Mira el precio final, no el porcentaje.</b> El precio «antes» a veces es un PVP que nadie ha pagado nunca. Por eso, cuando podemos, indicamos de dónde sale la comparación.",
       "<b>Regardez le prix final, pas le pourcentage.</b> Le prix « avant » est parfois un prix catalogue que personne n'a jamais payé. C'est pourquoi nous indiquons, quand c'est possible, d'où vient la comparaison.")}</li>
<li>{L("<b>Controlla l'anno del modello.</b> Gli sconti più forti sono sulle collezioni 2025 e 2026, ora che sono uscite le 2027: per la maggior parte dei giocatori vanno benissimo.",
       "<b>Check the model year.</b> The biggest discounts are on the 2025 and 2026 collections now that the 2027 ones are out: for most players they're perfectly fine.",
       "<b>Comprueba el año del modelo.</b> Los mayores descuentos están en las colecciones 2025 y 2026, ahora que han salido las 2027: para la mayoría de jugadores van perfectas.",
       "<b>Vérifiez l'année du modèle.</b> Les plus fortes remises concernent les collections 2025 et 2026, maintenant que les 2027 sont sorties : elles conviennent très bien à la plupart des joueurs.")}</li>
<li>{L(f'<b>Scegli prima la racchetta, poi lo sconto.</b> Una racchetta sbagliata resta sbagliata anche a metà prezzo. Se non sai quale fa per te, prova il <a href="{P("selettore")}">test in 2 minuti</a>.',
       f'<b>Choose the racket first, then the discount.</b> The wrong racket is still wrong at half price. If you don\'t know which suits you, try the <a href="{P("selettore")}">2-minute quiz</a>.',
       f'<b>Elige primero la pala y luego el descuento.</b> Una pala equivocada sigue siéndolo a mitad de precio. Si no sabes cuál te va, prueba el <a href="{P("selettore")}">test de 2 minutos</a>.',
       f'<b>Choisissez d\'abord la raquette, ensuite la remise.</b> Une mauvaise raquette reste mauvaise à moitié prix. Si vous ne savez pas laquelle vous convient, essayez le <a href="{P("selettore")}">quiz de 2 minutes</a>.')}</li>
</ul>
<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes", "Questions fréquentes")}</h2>
{faq_h}
<h2>{L("Tutte le racchette con il prezzo Amazon di oggi", "Every racket with today's Amazon price", "Todas las palas con el precio de Amazon de hoy", "Toutes les raquettes avec le prix Amazon du jour")}</h2>
<details class="of-det"><summary>{L("Apri l'elenco completo", "Open the full list", "Abrir la lista completa", "Ouvrir la liste complète")}</summary>
<p>{L("Dalla meno cara alla più cara. Tocca il nome per aprire la scheda tecnica.", "From cheapest to most expensive. Tap a name to open its spec page.", "De la más barata a la más cara. Toca el nombre para abrir la ficha técnica.", "De la moins chère à la plus chère. Touchez le nom pour ouvrir la fiche technique.")}</p>
<ul class="of-tutti" data-of-tutti>{elenco}</ul>
</details>
<p class="note">{L("In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Questo non cambia il prezzo che paghi né l'ordine delle offerte, che dipende solo dallo sconto.",
                    "As an Amazon Associate, PadelMetrix earns from qualifying purchases. This doesn't change the price you pay or the order of the deals, which depends only on the discount.",
                    "Como Afiliado de Amazon, PadelMetrix obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Esto no cambia el precio que pagas ni el orden de las ofertas, que depende solo del descuento.",
                    "En tant que Partenaire Amazon, PadelMetrix est rémunéré pour les achats éligibles. Cela ne change ni le prix que vous payez ni l'ordre des offres, qui dépend uniquement de la remise.")}</p>
</div>'''
    if FASE() == "cyber":
        tit = L("Offerte padel Amazon oggi: racchette in sconto per Black Friday e Cyber Monday | PadelMetrix", "Padel deals on Amazon today: rackets on sale for Black Friday and Cyber Monday | PadelMetrix",
                "Ofertas de pádel en Amazon hoy: palas rebajadas por Black Friday y Cyber Monday | PadelMetrix", "Offres padel Amazon aujourd'hui : raquettes en promo pour le Black Friday et le Cyber Monday | PadelMetrix")
    else:
        tit = L("Offerte padel Amazon oggi: racchette in sconto | PadelMetrix", "Padel deals on Amazon today: rackets on sale | PadelMetrix",
                "Ofertas de pádel en Amazon hoy: palas rebajadas | PadelMetrix", "Offres padel Amazon aujourd'hui : raquettes en promo | PadelMetrix")
    desc = L(f"Le racchette da padel oggi in offerta su Amazon, ordinate per sconto: prezzi di {len(con_asin)} modelli controllati due volte al giorno, con scheda tecnica.",
             f"Padel rackets on sale at Amazon today, sorted by discount: prices of {len(con_asin)} models checked twice a day, each with full specs.",
             f"Las palas de pádel hoy en oferta en Amazon, ordenadas por descuento: precios de {len(con_asin)} modelos comprobados dos veces al día, con ficha técnica.",
             f"Les raquettes de padel en promo sur Amazon aujourd'hui, classées par remise : prix de {len(con_asin)} modèles vérifiés deux fois par jour, avec fiche technique.")
    S.scrivi(path, pagina(tit, desc, path, corpo, on="offerte", ld=[ld, faq_ld], extra_js=dati_js(db) + JS, alt=alt), alt)


def banner_bf():
    if FASE() == "dopo":
        return ""
    return (f'<a class="promo-bar" style="border-radius:14px;margin:4px 0 14px" href="{P("blackfriday")}"><b>Cyber Monday</b> '
            f'{L("Ultimi giorni: le 15 racchette più scontate di oggi, con livello di gioco", "Last days: today\'s 15 most discounted rackets, with playing level", "Últimos días: las 15 palas más rebajadas de hoy, con nivel de juego", "Derniers jours : les 15 raquettes les plus remisées du jour, avec niveau de jeu")} '
            f'· <u>{L("Vai alla pagina", "Go to the page", "Ir a la página", "Voir la page")} →</u></a>')


def _top_statico(db, n=15):
    """Ordine di partenza (senza prezzi) per chi non esegue JavaScript: le racchette più scontate all'ultimo aggiornamento."""
    import datetime as dt
    idx = indice(db)
    try:
        j = json.loads((ROOT / "amazon" / "immagini.json").read_text(encoding="utf-8"))
        t = dt.datetime.fromisoformat(j["aggiornato"].replace("Z", "+00:00"))
        fresco = (dt.datetime.now(dt.timezone.utc) - t).total_seconds() < 86400 * 3
        prod = j.get("prodotti", {}) if fresco else {}
    except Exception:  # noqa: BLE001
        prod = {}
    righe = []
    for a, i in idx.items():
        x = prod.get(a)
        if i["k"] != "r" or not x or not x.get("euro"):
            continue
        sc = x.get("sconto") or 0
        if not sc and i["pl"] and x["euro"] <= i["pl"] * 0.9:
            sc = round((1 - x["euro"] / i["pl"]) * 100)
        if sc >= 10:
            righe.append((sc, i))
    righe.sort(key=lambda r: -r[0])
    return [i for _, i in righe[:n]]


def _intro_bf(dopo):
    regali = P("articoli", "idee-regalo-natale-padel")
    if dopo:
        return "<p><b>" + L(f'Le offerte del Black Friday e del Cyber Monday 2026 su Amazon si sono chiuse lunedì 30 novembre. Qui sotto trovi le racchette che oggi sono ancora scontate di almeno il 10%. Più in basso trovi anche le idee per i regali di Natale.',
                            f'The Black Friday and Cyber Monday 2026 deals on Amazon ended on Monday 30 November. Below are the rackets still at least 10% off today. Further down you will also find Christmas gift ideas.',
                            f'Las ofertas del Black Friday y del Cyber Monday 2026 en Amazon terminaron el lunes 30 de noviembre. Aquí abajo tienes las palas que hoy siguen con al menos un 10 % de descuento. Más abajo encontrarás también ideas de regalo de Navidad.',
                            f'Les offres du Black Friday et du Cyber Monday 2026 sur Amazon se sont terminées le lundi 30 novembre. Ci-dessous, les raquettes encore remisées d\'au moins 10 % aujourd\'hui. Plus bas, vous trouverez aussi des idées cadeaux de Noël.') + "</b></p>"
    return "<p><b>" + L("Il Cyber Monday, lunedì 30 novembre, è l'ultimo giorno delle offerte Black Friday su Amazon.it: dopo, molti prezzi tornano su. Se hai una racchetta in mente, è il momento di controllare.",
                        "Cyber Monday, Monday 30 November, is the last day of the Black Friday deals on Amazon.it: after that, many prices go back up. If you have a racket in mind, now is the time to check.",
                        "El Cyber Monday, lunes 30 de noviembre, es el último día de las ofertas del Black Friday en Amazon.it: después, muchos precios vuelven a subir. Si tienes una pala en mente, es el momento de mirarla.",
                        "Le Cyber Monday, lundi 30 novembre, est le dernier jour des offres Black Friday sur Amazon.it : ensuite, beaucoup de prix remontent. Si vous avez une raquette en tête, c'est le moment de vérifier.") + "</b></p>"


def pagina_bf(db):
    path, alt = P("blackfriday"), ALT("blackfriday")
    dopo = FASE() == "dopo"
    if dopo:
        tit_h = L("Black Friday racchette padel: il 2026 è finito, ecco cosa resta in offerta", "Black Friday padel rackets: 2026 is over, here's what is still on sale",
                  "Black Friday palas de pádel: el de 2026 terminó, esto sigue en oferta", "Black Friday raquettes de padel : l'édition 2026 est finie, voici ce qui reste en promo")
    else:
        tit_h = L("Black Friday e Cyber Monday racchette padel 2026: i veri sconti su Amazon", "Black Friday and Cyber Monday padel rackets 2026: the real Amazon discounts",
                  "Black Friday y Cyber Monday palas de pádel 2026: los descuentos reales en Amazon", "Black Friday et Cyber Monday raquettes de padel 2026 : les vraies remises sur Amazon")
    cr, ld = crumbs([S.home_crumb(), (L("Offerte", "Deals", "Ofertas", "Offres"), P("offerte")), ("Black Friday", None)])
    stat = _top_statico(db)
    fallback = ('<ol class="of-tutti">' + "".join(f'<li><a href="{i["u"]}">{e(i["t"])}</a><span>{e(i["lv"])}</span></li>' for i in stat) + "</ol>") if stat else ""
    regali = P("articoli", "idee-regalo-natale-padel")
    qa = [((L("Quando sarà il Black Friday 2027?", "When is Black Friday 2027?", "¿Cuándo será el Black Friday 2027?", "Quand aura lieu le Black Friday 2027 ?"),
           L("Venerdì 26 novembre 2027, con il Cyber Monday lunedì 29 novembre. Su Amazon le offerte di solito iniziano già nei giorni precedenti: questa pagina tornerà con gli sconti del 2027.",
             "Friday 26 November 2027, with Cyber Monday on Monday 29 November. Amazon deals usually start in the days before: this page will come back with the 2027 discounts.",
             "El viernes 26 de noviembre de 2027, con el Cyber Monday el lunes 29 de noviembre. Las ofertas de Amazon suelen empezar unos días antes: esta página volverá con los descuentos de 2027.",
             "Le vendredi 26 novembre 2027, avec le Cyber Monday le lundi 29 novembre. Les offres Amazon commencent généralement quelques jours avant : cette page reviendra avec les remises 2027.")) if dopo else (L("Quando inizia il Black Friday 2026 su Amazon?", "When does Black Friday 2026 start on Amazon?", "¿Cuándo empieza el Black Friday 2026 en Amazon?", "Quand commence le Black Friday 2026 sur Amazon ?"),
           L("Su Amazon.it le offerte del Black Friday 2026 sono iniziate giovedì 19 novembre e durano fino a lunedì 30 novembre, il Cyber Monday. Il Black Friday vero e proprio è venerdì 27 novembre. Per gli acquisti dal 1° novembre al 25 dicembre il reso è possibile fino al 31 gennaio 2027.",
             "On Amazon.it the Black Friday 2026 deals started on Thursday 19 November and run until Monday 30 November, Cyber Monday. Black Friday itself is Friday 27 November. Purchases made from 1 November to 25 December can be returned until 31 January 2027.",
             "En Amazon.it las ofertas del Black Friday 2026 empezaron el jueves 19 de noviembre y duran hasta el lunes 30 de noviembre, el Cyber Monday. El Black Friday propiamente dicho es el viernes 27 de noviembre. Las compras del 1 de noviembre al 25 de diciembre se pueden devolver hasta el 31 de enero de 2027.",
             "Sur Amazon.it, les offres du Black Friday 2026 ont commencé le jeudi 19 novembre et durent jusqu'au lundi 30 novembre, le Cyber Monday. Le Black Friday proprement dit tombe le vendredi 27 novembre. Les achats faits du 1er novembre au 25 décembre peuvent être retournés jusqu'au 31 janvier 2027."))),
          (L("Conviene comprare la racchetta 2026 o la 2027?", "Should I buy the 2026 or the 2027 racket?", "¿Conviene comprar la pala 2026 o la 2027?", "Vaut-il mieux acheter la raquette 2026 ou la 2027 ?"),
           L("Per la maggior parte dei giocatori conviene la 2026 in offerta. Tra un anno e l'altro cambiano soprattutto grafica e piccoli dettagli di materiali o bilanciamento, mentre la 2026 adesso costa spesso il 20–40% in meno. La 2027 ha senso se cerchi proprio una novità tecnica di quel modello o se la 2026 non si trova più nella tua misura di peso. Nelle schede trovi il confronto tra le due versioni.",
             "For most players the discounted 2026 is the better buy. From one year to the next it's mostly the graphics and small details of materials or balance that change, while the 2026 now often costs 20–40% less. The 2027 makes sense if you want a specific technical change in that model or if the 2026 is no longer available in your weight. Our spec pages compare the two versions.",
             "Para la mayoría de jugadores conviene la 2026 en oferta. De un año a otro cambian sobre todo el diseño y pequeños detalles de materiales o balance, mientras que la 2026 ahora suele costar un 20–40 % menos. La 2027 tiene sentido si buscas justo una novedad técnica de ese modelo o si la 2026 ya no está en tu peso. En las fichas encuentras la comparación entre las dos versiones.",
             "Pour la plupart des joueurs, la 2026 en promo est le meilleur choix. D'une année à l'autre, ce sont surtout le design et de petits détails de matériaux ou d'équilibre qui changent, alors que la 2026 coûte souvent 20 à 40 % de moins. La 2027 a du sens si vous voulez précisément une nouveauté technique de ce modèle ou si la 2026 n'existe plus dans votre poids. Nos fiches comparent les deux versions.")),
          (L("Gli sconti sono veri?", "Are the discounts real?", "¿Los descuentos son reales?", "Les remises sont-elles réelles ?"),
           L("Mostriamo lo sconto e il prezzo precedente dichiarati da Amazon; quando Amazon non li indica confrontiamo il prezzo con il listino del produttore e lo scriviamo sotto il prezzo. Teniamo solo sconti di almeno il 10% e aggiorniamo i prezzi due volte al giorno.",
             "We show the discount and previous price stated by Amazon; when Amazon doesn't give them we compare the price with the maker's list price and say so under the price. We keep only discounts of at least 10% and update prices twice a day.",
             "Mostramos el descuento y el precio anterior que indica Amazon; cuando Amazon no los da, comparamos el precio con el PVP del fabricante y lo indicamos bajo el precio. Solo incluimos descuentos de al menos el 10 % y actualizamos los precios dos veces al día.",
             "Nous affichons la remise et le prix précédent indiqués par Amazon ; quand Amazon ne les donne pas, nous comparons le prix au prix catalogue du fabricant et le précisons sous le prix. Nous ne gardons que les remises d'au moins 10 % et mettons les prix à jour deux fois par jour.")),
          (L("Quale livello di gioco scegliere?", "Which playing level should I choose?", "¿Qué nivel de juego elegir?", "Quel niveau de jeu choisir ?"),
           L("Se giochi da meno di un anno o una volta a settimana scegli una racchetta da principiante o intermedio: perdona di più gli errori e affatica meno il braccio. Le racchette da avanzato sono più rigide e precise, ma vanno bene solo se colpisci già con buona tecnica.",
             "If you've played for less than a year or once a week, pick a beginner or intermediate racket: it forgives mistakes more and is easier on the arm. Advanced rackets are stiffer and more precise, but only suit players who already hit with good technique.",
             "Si juegas desde hace menos de un año o una vez por semana, elige una pala de principiante o intermedio: perdona más los errores y cansa menos el brazo. Las palas de avanzado son más rígidas y precisas, pero solo van bien si ya golpeas con buena técnica.",
             "Si vous jouez depuis moins d'un an ou une fois par semaine, choisissez une raquette débutant ou intermédiaire : elle pardonne davantage et fatigue moins le bras. Les raquettes confirmé sont plus rigides et précises, mais ne conviennent qu'aux joueurs ayant déjà une bonne technique."))]
    faq_h = "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in qa)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": S.lang(),
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    corpo = f'''{CSS}{cr}
<div class="of-hero"><div class="k">{L("Black Friday 2026 concluso · il prossimo: 26 novembre 2027", "Black Friday 2026 is over · next one: 26 November 2027", "Black Friday 2026 terminado · el próximo: 26 de noviembre de 2027", "Black Friday 2026 terminé · le prochain : 26 novembre 2027") if dopo else "Black Friday & Cyber Monday 2026 · " + L("19–30 novembre", "19–30 November", "19–30 de noviembre", "19–30 novembre") + " · " + L("aggiornato ogni giorno", "updated daily", "actualizado cada día", "mis à jour chaque jour")}</div>
<h1>{tit_h}</h1>
{_intro_bf(dopo)}
<p>{L("Le 15 racchette da padel più scontate di oggi su Amazon, scelte tra le centinaia del nostro database: per ognuna trovi prezzo prima e dopo, percentuale di sconto, livello di gioco consigliato e la scheda tecnica completa.",
       "Today's 15 most discounted padel rackets on Amazon, picked from the hundreds in our database: for each one you get the before and after price, the discount, the recommended playing level and the full spec page.",
       "Las 15 palas de pádel más rebajadas de hoy en Amazon, elegidas entre los cientos de nuestra base de datos: para cada una tienes el precio antes y después, el porcentaje de descuento, el nivel de juego recomendado y la ficha técnica completa.",
       "Les 15 raquettes de padel les plus remisées du jour sur Amazon, choisies parmi les centaines de notre base : pour chacune, le prix avant et après, la remise, le niveau de jeu conseillé et la fiche technique complète.")}</p></div>
<p class="of-agg" data-of-agg></p>
<section data-of-sec><h2>{L("Le 15 racchette più scontate di oggi", "Today's 15 most discounted rackets", "Las 15 palas más rebajadas de hoy", "Les 15 raquettes les plus remisées du jour")}</h2>
<div data-of="r" data-n="15" data-msg>{fallback or '<p class="of-vuoto">' + L("Carico i prezzi di oggi…", "Loading today's prices…", "Cargando los precios de hoy…", "Chargement des prix du jour…") + '</p>'}</div>
<p style="margin-top:14px"><a class="btn ln" href="{P("offerte")}">{L("Tutte le offerte, anche accessori e pickleball →", "All deals, including accessories and pickleball →", "Todas las ofertas, también accesorios y pickleball →", "Toutes les offres, accessoires et pickleball compris →")}</a></p></section>
<div class="prose" style="margin-top:30px">
<h2>{L("Le date del Black Friday 2026 su Amazon", "Black Friday 2026 dates on Amazon", "Las fechas del Black Friday 2026 en Amazon", "Les dates du Black Friday 2026 sur Amazon")}</h2>
<ul><li>{L("<b>Inizio offerte:</b> giovedì 19 novembre", "<b>Deals start:</b> Thursday 19 November", "<b>Inicio de las ofertas:</b> jueves 19 de noviembre", "<b>Début des offres :</b> jeudi 19 novembre")}</li>
<li>{L("<b>Black Friday:</b> venerdì 27 novembre", "<b>Black Friday:</b> Friday 27 November", "<b>Black Friday:</b> viernes 27 de noviembre", "<b>Black Friday :</b> vendredi 27 novembre")}</li>
<li>{L("<b>Fine offerte (Cyber Monday):</b> lunedì 30 novembre", "<b>Deals end (Cyber Monday):</b> Monday 30 November", "<b>Fin de las ofertas (Cyber Monday):</b> lunes 30 de noviembre", "<b>Fin des offres (Cyber Monday) :</b> lundi 30 novembre")}</li>
<li>{L("<b>Reso esteso:</b> per gli acquisti fino al 25 dicembre, fino al 31 gennaio 2027", "<b>Extended returns:</b> for purchases up to 25 December, until 31 January 2027", "<b>Devolución ampliada:</b> para compras hasta el 25 de diciembre, hasta el 31 de enero de 2027", "<b>Retour prolongé :</b> pour les achats jusqu'au 25 décembre, jusqu'au 31 janvier 2027")}</li></ul>
<h2>{L("Come scegliere bene una racchetta in offerta", "How to choose a discounted racket well", "Cómo elegir bien una pala en oferta", "Bien choisir une raquette en promo") if dopo else L("Come scegliere bene durante il Black Friday", "How to choose well during Black Friday", "Cómo elegir bien durante el Black Friday", "Bien choisir pendant le Black Friday")}</h2>
<ul>
<li>{L(f'<b>Prima il livello, poi lo sconto.</b> Una racchetta da avanzato a metà prezzo resta difficile da usare per chi inizia. Se hai dubbi fai il <a href="{P("selettore")}">test in 2 minuti</a>.',
       f'<b>Level first, discount second.</b> An advanced racket at half price is still hard to use for a beginner. If in doubt, take the <a href="{P("selettore")}">2-minute quiz</a>.',
       f'<b>Primero el nivel, luego el descuento.</b> Una pala de avanzado a mitad de precio sigue siendo difícil para quien empieza. Si dudas, haz el <a href="{P("selettore")}">test de 2 minutos</a>.',
       f'<b>D\'abord le niveau, ensuite la remise.</b> Une raquette confirmé à moitié prix reste difficile pour un débutant. En cas de doute, faites le <a href="{P("selettore")}">quiz de 2 minutes</a>.')}</li>
<li>{L("<b>Guarda il prezzo finale.</b> Il prezzo «prima» a volte è un listino che nessuno ha mai pagato: per questo sotto ogni prezzo indichiamo da dove viene il confronto.",
       "<b>Look at the final price.</b> The “before” price is sometimes a list price nobody ever paid: that's why under each price we say where the comparison comes from.",
       "<b>Mira el precio final.</b> El precio «antes» a veces es un PVP que nadie ha pagado nunca: por eso bajo cada precio indicamos de dónde sale la comparación.",
       "<b>Regardez le prix final.</b> Le prix « avant » est parfois un prix catalogue que personne n'a payé : c'est pourquoi nous indiquons sous chaque prix d'où vient la comparaison.")}</li>
<li>{L(f'<b>Pensi a un regalo?</b> Con il reso esteso fino al 31 gennaio puoi comprare adesso. Altre idee nella nostra <a href="{regali}">guida ai regali di Natale per chi gioca a padel</a>.',
       f'<b>Buying a gift?</b> With returns extended to 31 January you can buy now. More ideas in our <a href="{regali}">Christmas gift guide for padel players</a>.',
       f'<b>¿Es un regalo?</b> Con la devolución ampliada hasta el 31 de enero puedes comprar ya. Más ideas en nuestra <a href="{regali}">guía de regalos de Navidad para jugadores de pádel</a>.',
       f'<b>C\'est un cadeau ?</b> Avec le retour prolongé jusqu\'au 31 janvier, vous pouvez acheter dès maintenant. D\'autres idées dans notre <a href="{regali}">guide des cadeaux de Noël pour joueurs de padel</a>.')}</li>
</ul>
<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes", "Questions fréquentes")}</h2>
{faq_h}
<p class="note">{L("In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei. Questo non cambia il prezzo che paghi né l'ordine delle racchette, che dipende solo dallo sconto. I prezzi arrivano da Amazon.it e non vengono mostrati se hanno più di 24 ore.",
                    "As an Amazon Associate, PadelMetrix earns from qualifying purchases. This doesn't change the price you pay or the order of the rackets, which depends only on the discount. Prices come from Amazon.it and are not shown if they are more than 24 hours old.",
                    "Como Afiliado de Amazon, PadelMetrix obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables. Esto no cambia el precio que pagas ni el orden de las palas, que depende solo del descuento. Los precios vienen de Amazon.it y no se muestran si tienen más de 24 horas.",
                    "En tant que Partenaire Amazon, PadelMetrix est rémunéré pour les achats éligibles. Cela ne change ni le prix que vous payez ni l'ordre des raquettes, qui dépend uniquement de la remise. Les prix viennent d'Amazon.it et ne sont pas affichés s'ils datent de plus de 24 heures.")}</p>
</div>'''
    if dopo:
        tit = L("Black Friday racchette padel: le offerte ancora attive e la data del 2027", "Black Friday padel rackets: deals still running and the 2027 date",
                "Black Friday palas de pádel: ofertas que siguen activas y la fecha de 2027", "Black Friday raquettes de padel : les promos encore actives et la date 2027")
    else:
        tit = L("Black Friday e Cyber Monday racchette padel 2026: i veri sconti su Amazon", "Black Friday & Cyber Monday padel rackets 2026: the real Amazon discounts",
                "Black Friday y Cyber Monday palas de pádel 2026: descuentos reales en Amazon", "Black Friday et Cyber Monday raquettes de padel 2026 : les vraies remises Amazon")
    desc_dopo = L("Il Black Friday 2026 è finito: le racchette da padel ancora scontate di almeno il 10% su Amazon, con prezzo e livello di gioco, e le date del Black Friday 2027.",
                  "Black Friday 2026 is over: the padel rackets still at least 10% off on Amazon, with price and playing level, plus the Black Friday 2027 dates.",
                  "El Black Friday 2026 terminó: las palas de pádel que siguen con al menos un 10 % de descuento en Amazon, con precio y nivel, y las fechas del Black Friday 2027.",
                  "Le Black Friday 2026 est terminé : les raquettes de padel encore remisées d'au moins 10 % sur Amazon, avec prix et niveau, et les dates du Black Friday 2027.")
    desc = L("Le 15 racchette da padel più scontate su Amazon per il Black Friday e il Cyber Monday 2026 (19–30 novembre): prezzo prima e dopo, % di sconto e livello di gioco, aggiornati due volte al giorno.",
             "The 15 most discounted padel rackets on Amazon for Black Friday and Cyber Monday 2026 (19–30 November): before and after price, % off and playing level, updated twice a day.",
             "Las 15 palas de pádel más rebajadas en Amazon por el Black Friday y el Cyber Monday 2026 (19–30 de noviembre): precio antes y después, % de descuento y nivel de juego, actualizados dos veces al día.",
             "Les 15 raquettes de padel les plus remisées sur Amazon pour le Black Friday et le Cyber Monday 2026 (19–30 novembre) : prix avant et après, % de remise et niveau de jeu, mis à jour deux fois par jour.")
    S.scrivi(path, pagina(tit, desc_dopo if dopo else desc, path, corpo, on="offerte", ld=[ld, faq_ld], extra_js=dati_js(db, solo="r") + JS, alt=alt), alt)


def main():
    db = ordina(S.carica())
    for l in LINGUE:
        set_lang(l)
        pagina_offerte(db)
        pagina_bf(db)
    set_lang("it")
    (ROOT / "scripts" / "pagine_offerte.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine offerte generate")


if __name__ == "__main__":
    main()
