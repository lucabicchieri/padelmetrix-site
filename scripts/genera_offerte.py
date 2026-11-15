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
.of .im{height:190px;display:flex;align-items:center;justify-content:center;background:#fff;border-bottom:1px solid var(--line)}
.of .im img{max-width:86%;max-height:170px;object-fit:contain}
.of .tx{padding:12px 14px 14px;display:flex;flex-direction:column;flex:1}
.of .nm{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px;line-height:1.25;color:var(--ink);text-decoration:none}
.of .nm:hover{text-decoration:underline}
.of .pz{margin-top:8px;font-size:15px}.of .pz b{font-family:'Space Grotesk',sans-serif;font-size:24px;color:var(--green)}.of .pz s{color:var(--muted);margin-left:6px}
.of small{color:var(--muted);font-size:12px;line-height:1.3;margin-top:2px}
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
            out[asin] = {"k": "r", "t": n["titolo"], "u": url_r(n), "pl": n["prezzo"] or 0}
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
            "en": S.lang() == "en"}


# Motore comune a pagina offerte e home: legge i prezzi e disegna le card.
JS = r"""<script>(function(){
var I=window.OF_IDX||{},T=window.OF_TX||{};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
function fm(x){var s=x.toFixed(2).replace('.',',').replace(/,00$/,'');s=s.replace(/\B(?=(\d{3})+(?!\d))/g,'.');return T.en?'€'+x.toFixed(2).replace(/\.00$/,''):s+' €'}
function card(o){var am='https://www.amazon.it/dp/'+o.a+'?tag=padelmetrix-21',r='rel="sponsored nofollow noopener" target="_blank"';
return '<div class="of"><span class="bd">−'+o.s+'%</span><a class="im" href="'+am+'" '+r+' title="Amazon"><img src="'+o.img+'" alt="'+esc(o.t)+'" loading="lazy"></a><div class="tx">'
+(o.u?'<a class="nm" href="'+o.u+'">'+esc(o.t)+'</a>':'<span class="nm">'+esc(o.t)+'</span>')
+'<div class="pz"><b>'+esc(o.pz)+'</b><s>'+esc(o.pr)+'</s></div><small>'+(o.src=='l'?T.pl:T.pa)+'</small>'
+'<div class="bt"><a class="btn lime" href="'+am+'" '+r+'>'+T.am+'</a>'+(o.u?'<a class="sc" href="'+o.u+'">'+T.sc+'</a>':'')+'</div></div></div>'}
fetch('/amazon/immagini.json',{cache:'no-cache'}).then(function(r){return r.json()}).then(function(j){
var t=Date.parse(j.aggiornato||''),ok=t&&Date.now()-t<864e5,P=j.prodotti||{},all=[],tutti=[];
if(ok)for(var a in I){var x=P[a],i=I[a];if(!x||!x.euro||!x.img)continue;
 var s=x.sconto||0,pr=(x.prima||'').replace(/ /g,' '),src='a';
 if(!s&&i.pl&&x.euro<=i.pl*0.9){s=Math.round((1-x.euro/i.pl)*100);pr=fm(i.pl);src='l'}
 var o={a:a,k:i.k,t:i.t,u:i.u,img:x.img,e:x.euro,pz:x.prezzo.replace(/ /g,' '),s:s,pr:pr,src:src};
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
  box.innerHTML=v.length?v.map(card).join(''):'';box.className=v.length?'of-grid':'';
  var nx=box.nextElementSibling;if(nx&&nx.classList.contains('of-more'))nx.remove();
  if(more&&f.length>v.length){var b=document.createElement('button');b.type='button';b.className='btn out of-more';b.textContent=T.more.replace('{n}',f.length);
   b.onclick=function(){n=999;draw(lo,hi)};box.after(b)}
  if(!v.length&&box.hasAttribute('data-msg'))box.innerHTML='<p class="of-vuoto">'+(ok?T.zero:T.no)+'</p>';return v.length}
 var c=draw(0,1e9);if(sec&&!c&&!box.hasAttribute('data-msg'))sec.style.display='none';else if(sec)sec.style.display='';
 var ch=sec&&sec.querySelector('.of-chips');if(ch)ch.addEventListener('click',function(ev){var b=ev.target.closest('button');if(!b)return;
  ch.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x===b)});draw(+b.getAttribute('data-lo'),+b.getAttribute('data-hi'))})});
var ul=document.querySelector('[data-of-tutti]');if(ul&&ok){tutti.sort(function(p,q){return p.e-q.e});
 ul.innerHTML=tutti.map(function(o){return '<li><a href="'+o.u+'">'+esc(o.t)+'</a><span>'+esc(o.pz)+'</span></li>'}).join('')}
}).catch(function(){document.querySelectorAll('[data-of][data-msg]').forEach(function(b){b.innerHTML='<p class="of-vuoto">'+T.no+'</p>'})})})();</script>"""


def dati_js(db, solo=None):
    idx = indice(db)
    if solo:
        idx = {a: v for a, v in idx.items() if v["k"] in solo}
    return "<script>window.OF_IDX=" + json.dumps(idx, ensure_ascii=False) + ";window.OF_TX=" + json.dumps(testi_js(), ensure_ascii=False) + ";</script>"


def blocco_home(db):
    """Sezione per la home: le 4 racchette più scontate oggi. Resta nascosta se non ci sono dati aggiornati."""
    return (CSS + f'''<section class="of-home" data-of-sec style="display:none"><div class="wrap">
<h2>{L("Le offerte di oggi su Amazon", "Today's deals on Amazon", "Las ofertas de hoy en Amazon", "Les offres du jour sur Amazon")}</h2>
<p class="of-agg" data-of-agg></p>
<div data-of="r" data-n="4"></div>
<p style="margin-top:16px"><a class="btn lime" href="{P("offerte")}">{L("Tutte le offerte padel →", "All padel deals →", "Todas las ofertas de pádel →", "Toutes les offres padel →")}</a></p>
</div></section>''', dati_js(db, solo="r") + JS)


def striscia_home():
    """Barra sopra l'hero della home."""
    return (f'<a class="promo-bar" href="{P("offerte")}"><b>Black Friday</b> '
            f'{L("Racchette da padel in offerta su Amazon", "Padel rackets on sale at Amazon", "Palas de pádel en oferta en Amazon", "Raquettes de padel en promo sur Amazon")} '
            f'<span data-of-max></span> · <u>{L("Guarda le offerte", "See the deals", "Ver las ofertas", "Voir les offres")} →</u></a>')


def pagina_offerte(db):
    path, alt = P("offerte"), ALT("offerte")
    cr, ld = crumbs([S.home_crumb(), (L("Offerte", "Deals", "Ofertas", "Offres"), None)])
    chips = "".join(f'<button type="button"{" class=\"on\"" if i == 0 else ""} data-lo="{lo}" data-hi="{hi}">{t}</button>' for i, (lo, hi, t) in enumerate([
        (0, 1000000000, L("Tutte", "All", "Todas", "Toutes")), (0, 100, L("Fino a 100 €", "Up to €100", "Hasta 100 €", "Jusqu'à 100 €")),
        (100, 200, L("Da 100 a 200 €", "€100 to €200", "De 100 a 200 €", "De 100 à 200 €")), (200, 1000000000, L("Oltre 200 €", "Over €200", "Más de 200 €", "Plus de 200 €"))]))
    con_asin = [n for n in db if n["slug"] in {v["u"].strip("/").split("/")[-1] for v in indice(db).values() if v["k"] == "r"}]
    qa = [(L("Quando è il Black Friday 2026?", "When is Black Friday 2026?", "¿Cuándo es el Black Friday 2026?", "Quand a lieu le Black Friday 2026 ?"),
           L("Venerdì 27 novembre 2026. Le offerte su Amazon di solito iniziano già nei giorni precedenti e proseguono fino al Cyber Monday, lunedì 30 novembre.",
             "Friday 27 November 2026. Amazon deals usually start in the days before and run until Cyber Monday, 30 November.",
             "El viernes 27 de noviembre de 2026. Las ofertas de Amazon suelen empezar unos días antes y siguen hasta el Cyber Monday, el lunes 30 de noviembre.",
             "Le vendredi 27 novembre 2026. Les offres Amazon commencent généralement quelques jours avant et durent jusqu'au Cyber Monday, le lundi 30 novembre.")),
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
<div class="of-hero"><div class="k">Black Friday 2026 · {L("aggiornate ogni giorno", "updated daily", "actualizadas cada día", "mises à jour chaque jour")}</div>
<h1>{L("Offerte padel su Amazon: le racchette in sconto oggi", "Padel deals on Amazon: rackets on sale today", "Ofertas de pádel en Amazon: las palas rebajadas hoy", "Offres padel sur Amazon : les raquettes en promo aujourd'hui")}</h1>
<p>{L(f"Controlliamo due volte al giorno il prezzo Amazon di {len(con_asin)} racchette del nostro database e ti mostriamo solo quelle davvero scontate, dalla più conveniente. Per ogni racchetta trovi anche la scheda tecnica, così sai cosa stai comprando.",
       f"Twice a day we check the Amazon price of {len(con_asin)} rackets in our database and show only the ones that are really discounted, best deal first. Each one links to its full spec page, so you know what you're buying.",
       f"Comprobamos dos veces al día el precio en Amazon de {len(con_asin)} palas de nuestra base de datos y te mostramos solo las que están rebajadas de verdad, de la mejor oferta en adelante. Cada pala tiene su ficha técnica, para que sepas qué compras.",
       f"Deux fois par jour, nous vérifions le prix Amazon de {len(con_asin)} raquettes de notre base et n'affichons que celles réellement remisées, de la meilleure offre à la moins forte. Chaque raquette a sa fiche technique, pour savoir ce que vous achetez.")}</p></div>
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
    tit = L("Offerte padel Amazon oggi: racchette in sconto e Black Friday 2026 | PadelMetrix", "Padel deals on Amazon today: rackets on sale and Black Friday 2026 | PadelMetrix",
            "Ofertas de pádel en Amazon hoy: palas rebajadas y Black Friday 2026 | PadelMetrix", "Offres padel Amazon aujourd'hui : raquettes en promo et Black Friday 2026 | PadelMetrix")
    desc = L(f"Le racchette da padel oggi in offerta su Amazon, ordinate per sconto: prezzi di {len(con_asin)} modelli controllati due volte al giorno, con scheda tecnica. Pronti per il Black Friday 2026.",
             f"Padel rackets on sale at Amazon today, sorted by discount: prices of {len(con_asin)} models checked twice a day, each with full specs. Ready for Black Friday 2026.",
             f"Las palas de pádel hoy en oferta en Amazon, ordenadas por descuento: precios de {len(con_asin)} modelos comprobados dos veces al día, con ficha técnica. Listos para el Black Friday 2026.",
             f"Les raquettes de padel en promo sur Amazon aujourd'hui, classées par remise : prix de {len(con_asin)} modèles vérifiés deux fois par jour, avec fiche technique. Prêts pour le Black Friday 2026.")
    S.scrivi(path, pagina(tit, desc, path, corpo, on="offerte", ld=[ld, faq_ld], extra_js=dati_js(db) + JS, alt=alt), alt)


def main():
    db = ordina(S.carica())
    for l in LINGUE:
        set_lang(l)
        pagina_offerte(db)
    set_lang("it")
    (ROOT / "scripts" / "pagine_offerte.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine offerte generate")


if __name__ == "__main__":
    main()
