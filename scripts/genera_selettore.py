#!/usr/bin/env python3
"""Pagina "Trova la tua racchetta in 2 minuti" in it/en/es: 7 domande e le 3 racchette più adatte dal database.

Il punteggio usa solo i dati delle schede (livello, stile, forma, peso, tatto, prezzo di listino, categoria, marca)
ed è spiegato in pagina. Tutto gira nel browser: nessun dato viene inviato."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import ROOT, e, L, P, ALT, crumbs, pagina, LINGUE, set_lang, LIV, FORMA, LIVN, euro, url_r, ordina  # noqa: E402
from comune import racket_svg  # noqa: E402

LIVNUM = {k: i for i, k in enumerate(LIV)}


def tatto(n):
    s = str(n["sensazione"] or "").lower()
    if "morbid" in s:
        return 1
    if any(w in s for w in ("dur", "rigid", "secc", "ferm")):
        return -1
    return 0


def indice(db):
    out = []
    for n in db:
        out.append({"s": n["slug"], "t": n["titolo"], "m": n["marca"], "ms": n["marca_slug"], "f": n["forma"] or "", "fl": FORMA(n["forma"]) or "",
                    "l": LIVNUM.get(n["livello"], -1), "ll": LIVN(n["livello"]) or "", "st": n["stile"] or "", "p": n["peso_min"] or 0,
                    "pz": n["prezzo"] or 0, "pzt": euro(n["prezzo"]) if n["prezzo"] else "", "tt": tatto(n),
                    "c": "junior" if n["categoria"] == "junior" else ("donna" if n["donna"] else "adulto"), "a": n["anno"], "u": url_r(n),
                    "svg": n["forma"] or "goccia"})
    return out


SVGS = {f: racket_svg(f, 72, "") for f in ("diamante", "rotonda", "goccia")}


def domande(marche):
    q = [
        ("l", L("Che livello hai?", "What is your level?", "¿Qué nivel tienes?"),
         [("0", L("Ho appena iniziato", "I've just started", "Acabo de empezar")), ("2", L("Gioco con regolarità", "I play regularly", "Juego con regularidad")),
          ("4", L("Sono avanzato", "I'm advanced", "Soy avanzado")), ("5", L("Gioco tornei", "I play tournaments", "Juego torneos"))]),
        ("s", L("Come giochi?", "How do you play?", "¿Cómo juegas?"),
         [("controllo", L("Difendo e costruisco il punto", "I defend and build the point", "Defiendo y construyo el punto")),
          ("polivalente", L("Un po' di tutto", "A bit of everything", "Un poco de todo")),
          ("offensivo", L("Attacco e chiudo a rete", "I attack and finish at the net", "Ataco y cierro en la red"))]),
        ("b", L("Hai fastidi a gomito o spalla?", "Do you have elbow or shoulder problems?", "¿Tienes molestias en el codo o el hombro?"),
         [("si", L("Sì", "Yes", "Sí")), ("no", L("No", "No", "No"))]),
        ("w", L("Che peso preferisci?", "What weight do you prefer?", "¿Qué peso prefieres?"),
         [("leggera", L("Leggera (sotto 355 g)", "Light (under 355 g)", "Ligera (menos de 355 g)")), ("media", L("Media (355–365 g)", "Medium (355–365 g)", "Media (355–365 g)")),
          ("pesante", L("Pesante (oltre 365 g)", "Heavy (over 365 g)", "Pesada (más de 365 g)")), ("", L("Non so", "Not sure", "No sé"))]),
        ("p", L("Quanto vuoi spendere (prezzo di listino)?", "How much do you want to spend (list price)?", "¿Cuánto quieres gastar (precio de lista)?"),
         [("100", L("Fino a 100 €", "Up to €100", "Hasta 100 €")), ("200", L("Fino a 200 €", "Up to €200", "Hasta 200 €")),
          ("300", L("Fino a 300 €", "Up to €300", "Hasta 300 €")), ("", L("Indifferente", "Doesn't matter", "Me da igual"))]),
        ("c", L("Per chi è?", "Who is it for?", "¿Para quién es?"),
         [("adulto", L("Adulto", "Adult", "Adulto")), ("donna", L("Donna (anche modelli femminili)", "Woman (women's models too)", "Mujer (también modelos femeninos)")),
          ("junior", L("Bambino o ragazzo", "Child or teenager", "Niño o joven"))]),
        ("m", L("Hai una marca preferita?", "Do you have a favourite brand?", "¿Tienes una marca preferida?"),
         [("", L("Nessuna", "None", "Ninguna"))] + [(s, m) for s, m in marche]),
    ]
    return q


def testi_js():
    return {
        "liv": L("adatta al tuo livello", "suits your level", "adecuada a tu nivel"),
        "stile": L("stile di gioco in linea con il tuo", "playing style matches yours", "estilo de juego como el tuyo"),
        "forma": L("forma adatta a come giochi", "shape suits how you play", "forma adecuada a cómo juegas"),
        "soft": L("tatto morbido, più comodo per il braccio", "soft feel, easier on the arm", "tacto blando, más cómodo para el brazo"),
        "peso": L("peso come lo preferisci", "weight as you prefer", "peso como lo prefieres"),
        "budget": L("nel tuo budget", "within your budget", "dentro de tu presupuesto"),
        "donna": L("modello femminile", "women's model", "modelo femenino"),
        "nuova": L("collezione 2027", "2027 collection", "colección 2027"),
        "scheda": L("Leggi la scheda", "Read the page", "Lee la ficha"),
        "titolo": L("Le 3 racchette più adatte a te", "The 3 rackets that suit you best", "Las 3 palas que mejor te encajan"),
        "vuoto": L("Nessuna racchetta corrisponde a tutti i criteri: prova ad allargare budget o marca.", "No racket matches all the criteria: try widening budget or brand.",
                   "Ninguna pala cumple todos los criterios: prueba a ampliar el presupuesto o la marca."),
        "manca": L("Rispondi a tutte le domande per vedere il risultato.", "Answer all the questions to see the result.", "Responde a todas las preguntas para ver el resultado."),
        "confronta": L("Confronta queste racchette", "Compare these rackets", "Compara estas palas"),
        "prezzo": L("Listino", "List price", "Precio de lista"),
        "cmp": P("confronta"),
    }


JS = r"""<script>
(function(){
var f=document.getElementById('finder'),out=document.getElementById('risultato');
var q=new URLSearchParams(location.search);['l','s','b','w','p','c','m'].forEach(function(k){var v=q.get(k);if(v===null)return;var el=f.querySelector('input[name="'+k+'"][value="'+v+'"]');if(el)el.checked=true;});
function val(k){var el=f.querySelector('input[name="'+k+'"]:checked');return el?el.value:null;}
function esc(t){return String(t).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function score(r,a){
 var s=0,why=[];
 if(a.c==='junior'){if(r.c!=='junior')return null;}else if(r.c==='junior')return null;
 if(a.m&&r.ms!==a.m)return null;
 var lv=parseInt(a.l,10);
 if(r.l>=0){var d=Math.abs(r.l-lv);s-=d*3;if(d<=1)why.push(TX.liv);if(lv<=1&&r.l>=4)s-=6;}
 var forma={controllo:'rotonda',polivalente:'goccia',offensivo:'diamante'}[a.s];
 if(r.st===a.s){s+=4;why.push(TX.stile);}
 if(r.f===forma||(a.s==='polivalente'&&r.f==='ibrida')){s+=3;why.push(TX.forma);}else if(a.s==='controllo'&&r.f==='diamante')s-=3;
 if(a.b==='si'){if(r.tt===1){s+=5;why.push(TX.soft);}else if(r.tt===-1)s-=5;if(r.f==='diamante'&&r.tt!==1)s-=3;}
 if(a.w&&r.p){var w=r.p<355?'leggera':(r.p<=365?'media':'pesante');if(w===a.w){s+=2;why.push(TX.peso);}else s-=1;}
 if(a.p){var b=parseFloat(a.p);if(r.pz){if(r.pz<=b){s+=2;why.push(TX.budget);}else s-=6+(r.pz-b)/25;}else s-=1.5;}
 if(a.c==='donna'&&r.c==='donna'){s+=2;why.push(TX.donna);}
 if(r.a===2027){s+=0.5;if(why.length<4)why.push(TX.nuova);}
 return {s:s,why:why};
}
function run(show){
 var a={};var ok=true;['l','s','b','w','p','c','m'].forEach(function(k){var v=val(k);if(v===null)ok=false;a[k]=v;});
 if(!ok){if(show)out.innerHTML='<p class="note">'+TX.manca+'</p>';return;}
 var p=new URLSearchParams(a);history.replaceState(null,'','?'+p.toString());
 var res=[];IDX.forEach(function(r){var x=score(r,a);if(x)res.push({r:r,s:x.s,why:x.why});});
 res.sort(function(x,y){return y.s-x.s||y.r.a-x.r.a;});
 var top=res.slice(0,3);
 if(!top.length){out.innerHTML='<p class="note">'+TX.vuoto+'</p>';return;}
 var h='<h2>'+TX.titolo+'</h2><div class="fres">';
 top.forEach(function(x,i){var r=x.r;h+='<a class="fcard" href="'+r.u+'"><span class="n">'+(i+1)+'</span><div class="ill">'+SVG[r.svg]+'</div><div><small>'+esc(r.m)+' · '+r.a+'</small><b>'+esc(r.t)+'</b><small>'+esc([r.fl,r.ll,r.pzt?TX.prezzo+' '+r.pzt:''].filter(Boolean).join(' · '))+'</small><ul>'+x.why.slice(0,4).map(function(w){return '<li>'+w+'</li>';}).join('')+'</ul><span class="go">'+TX.scheda+' →</span></div></a>';});
 h+='</div>';
 if(top.length>=2)h+='<p><a class="btn out" href="'+TX.cmp+'?r='+top[0].r.s+','+top[1].r.s+'">'+TX.confronta+'</a></p>';
 out.innerHTML=h;out.scrollIntoView({behavior:'smooth',block:'start'});
}
f.addEventListener('submit',function(ev){ev.preventDefault();run(true);});
if(q.get('l')!==null)run(false);
})();
</script>"""

CSS = """<style>
.finder{display:flex;flex-direction:column;gap:18px;max-width:860px}
.finder fieldset{border:1px solid var(--line,#E1E5DF);border-radius:16px;background:#fff;padding:16px 18px;margin:0}
.finder legend{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:18px;padding:0 6px}
.finder .opts{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.finder label{cursor:pointer}
.finder input{position:absolute;opacity:0;pointer-events:none}
.finder label span{display:inline-block;padding:9px 14px;border:1.5px solid #CFD8D1;border-radius:999px;font-size:15px;background:#FAFAF7}
.finder input:checked+span{background:#0F3D2E;color:#fff;border-color:#0F3D2E}
.finder input:focus-visible+span{outline:2px solid #C6F432;outline-offset:2px}
.finder button{align-self:flex-start;font:600 17px 'IBM Plex Sans',sans-serif;padding:14px 24px;border-radius:12px;border:none;background:#C6F432;color:#0F3D2E;cursor:pointer}
#risultato{scroll-margin-top:20px;margin-top:28px}
.fres{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}
.fcard{position:relative;display:flex;gap:12px;background:#fff;border:1px solid var(--line,#E1E5DF);border-radius:16px;padding:16px;text-decoration:none;color:inherit}
.fcard .n{position:absolute;top:10px;right:12px;width:28px;height:28px;border-radius:8px;background:#C6F432;color:#0F3D2E;font-weight:700;display:flex;align-items:center;justify-content:center}
.fcard .ill{flex:0 0 72px}.fcard small{display:block;color:#5B6B63;font-size:13px}.fcard b{display:block;font-size:17px;margin:2px 0 4px;padding-right:30px}
.fcard ul{margin:8px 0;padding-left:18px;font-size:14px;color:#3D4D45}.fcard .go{font-weight:600;color:#0F3D2E;font-size:14px}
</style>"""


def pagina_selettore(db):
    marche = sorted({(n["marca_slug"], n["marca"]) for n in db}, key=lambda x: x[1].lower())
    path, alt = P("selettore"), ALT("selettore")
    form = "".join(
        f'<fieldset><legend>{i}. {e(t)}</legend><div class="opts">' + "".join(
            f'<label><input type="radio" name="{k}" value="{v}"{" required" if j == 0 else ""}><span>{e(lab)}</span></label>' for j, (v, lab) in enumerate(opts)) + "</div></fieldset>"
        for i, (k, t, opts) in enumerate(domande(marche), 1))
    cr, ld = crumbs([S.home_crumb(), (L("Trova la tua racchetta", "Racket finder", "Encuentra tu pala"), None)])
    corpo = f'''{CSS}{cr}
<div class="intro"><h1>{L("Trova la tua racchetta da padel in 2 minuti", "Find your padel racket in 2 minutes", "Encuentra tu pala de pádel en 2 minutos")}</h1>
<p><b>{L(f"Rispondi a 7 domande su livello, stile, braccio, peso, budget e marca: ti proponiamo le 3 racchette più adatte tra le {len(db)} del database PadelMetrix.", f"Answer 7 questions about level, style, arm, weight, budget and brand: we suggest the 3 best-suited rackets out of the {len(db)} in the PadelMetrix database.", f"Responde a 7 preguntas sobre nivel, estilo, brazo, peso, presupuesto y marca: te proponemos las 3 palas más adecuadas entre las {len(db)} de la base de datos PadelMetrix.")}</b> {L("Il test gira nel tuo browser: le risposte non vengono inviate a nessuno.", "The quiz runs in your browser: your answers are not sent anywhere.", "El test funciona en tu navegador: las respuestas no se envían a nadie.")}</p></div>
<form class="finder" id="finder">{form}<button type="submit">{L("Mostra le mie racchette", "Show my rackets", "Mostrar mis palas")}</button></form>
<div id="risultato" aria-live="polite"></div>
<div class="prose" style="margin-top:36px">
<h2>{L("Come scegliamo", "How we choose", "Cómo elegimos")}</h2>
<p>{L("Ogni racchetta riceve un punteggio in base ai dati della sua scheda: quanto il livello consigliato è vicino al tuo, se stile e forma corrispondono a come giochi (rotonda per il controllo, goccia o ibrida per il gioco completo, diamante per l'attacco), il tatto se hai fastidi al braccio, il peso, il prezzo di listino rispetto al budget e la categoria. Le racchette troppo avanzate per chi inizia vengono penalizzate. Non ci sono posizioni a pagamento.",
       "Each racket gets a score based on its page data: how close the recommended level is to yours, whether style and shape match how you play (round for control, teardrop or hybrid for an all-round game, diamond for attack), the feel if you have arm problems, the weight, the list price against your budget and the category. Rackets that are too advanced for beginners are penalised. There are no paid placements.",
       "Cada pala recibe una puntuación según los datos de su ficha: lo cerca que está el nivel recomendado del tuyo, si estilo y forma coinciden con tu juego (redonda para el control, lágrima o híbrida para un juego completo, diamante para el ataque), el tacto si tienes molestias en el brazo, el peso, el precio de lista frente al presupuesto y la categoría. Las palas demasiado avanzadas para quien empieza se penalizan. No hay posiciones de pago.")}</p>
<p>{L(f'Vuoi capire meglio? Leggi le guide <a href="{P("guide", "racchetta-padel-principianti")}">per principianti</a>, <a href="{P("guide", "racchetta-padel-epicondilite")}">per il gomito</a> e <a href="{P("guide", "forme-racchetta-padel")}">sulle forme</a>, oppure cerca nell\'<a href="{P("racchette")}">elenco completo</a>.',
       f'Want to know more? Read the guides <a href="{P("guide", "racchetta-padel-principianti")}">for beginners</a>, <a href="{P("guide", "racchetta-padel-epicondilite")}">for tennis elbow</a> and <a href="{P("guide", "forme-racchetta-padel")}">on shapes</a>, or search the <a href="{P("racchette")}">full list</a>.',
       f'¿Quieres saber más? Lee las guías <a href="{P("guide", "racchetta-padel-principianti")}">para principiantes</a>, <a href="{P("guide", "racchetta-padel-epicondilite")}">para el codo</a> y <a href="{P("guide", "forme-racchetta-padel")}">sobre las formas</a>, o busca en la <a href="{P("racchette")}">lista completa</a>.')}</p>
</div>'''
    js = ("<script>var IDX=" + json.dumps(indice(db), ensure_ascii=False) + ";var TX=" + json.dumps(testi_js(), ensure_ascii=False)
          + ";var SVG=" + json.dumps(SVGS) + ";</script>" + JS)
    app = {"@context": "https://schema.org", "@type": "WebApplication", "name": L("Trova la tua racchetta da padel", "Padel racket finder", "Encuentra tu pala de pádel"),
           "applicationCategory": "SportsApplication", "operatingSystem": "Web", "url": S.SITO + path, "inLanguage": S.lang(),
           "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}, "publisher": S.editore()}
    S.scrivi(path, pagina(L("Trova la tua racchetta da padel in 2 minuti: test con 7 domande | PadelMetrix", "Find your padel racket in 2 minutes: 7-question quiz | PadelMetrix",
                            "Encuentra tu pala de pádel en 2 minutos: test de 7 preguntas | PadelMetrix"),
                          L(f"Test gratuito: 7 domande su livello, stile, braccio, peso e budget e le 3 racchette da padel più adatte tra {len(db)} modelli 2026 e 2027.",
                            f"Free quiz: 7 questions on level, style, arm, weight and budget, and the 3 best-suited padel rackets among {len(db)} 2026 and 2027 models.",
                            f"Test gratuito: 7 preguntas sobre nivel, estilo, brazo, peso y presupuesto y las 3 palas de pádel más adecuadas entre {len(db)} modelos 2026 y 2027."),
                          path, corpo, on="racchette", ld=[ld, app], extra_js=js, alt=alt), alt)


def main():
    db = ordina(S.carica())
    for l in LINGUE:
        set_lang(l)
        pagina_selettore(db)
    set_lang("it")
    (ROOT / "scripts" / "pagine_selettore.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine selettore generate")


if __name__ == "__main__":
    main()
