#!/usr/bin/env python3
"""Sezione Pickleball in it/en/es: elenco con filtri e guida rapida + una scheda per racchetta (paddle).

Dati e testi in scripts/dati_pickleball.py. Stesso formato delle schede padel."""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import ROOT, SITO, e, L, P, ALT, crumbs, pagina, LINGUE, set_lang, LIVN, STILEN, euro, data_txt, OGGI  # noqa: E402
from dati_pickleball import P as PADDLE, F, FORME  # noqa: E402

AMAZON = {"it": "www.amazon.it", "en": "www.amazon.co.uk", "es": "www.amazon.es"}
AMAZON_TAG = {"it": "padelmetrix-21", "en": None, "es": None}
OZ, IN = 28.3495, 2.54


def g(d):
    """Testo nella lingua corrente da un dict {it, en, es}."""
    return d[S.lang()] if isinstance(d, dict) else d


def num(v, dec=1):
    s = f"{v:.{dec}f}".rstrip("0").rstrip(".") if dec else f"{v:.0f}"
    return s if S.lang() == "en" else s.replace(".", ",")


def numtxt(s):
    """Valori scritti in formato italiano ('6,26', '2.060') nel formato della lingua."""
    if S.lang() != "en":
        return s
    return s.replace(".", "§").replace(",", ".").replace("§", ",")


def peso(p):
    if p.get("peso_oz"):
        a, b = p["peso_oz"]
        return f"{num(a)}–{num(b)} oz ({round(a * OZ)}–{round(b * OZ)} g)"
    if p.get("peso_g"):
        return f"{p['peso_g']} g ({num(p['peso_g'] / OZ)} oz)"
    if p.get("peso_test_oz"):
        return f"{num(p['peso_test_oz'], 2)} oz ({round(p['peso_test_oz'] * OZ)} g) " + L("misurati", "measured", "medidos")
    return None


def peso_breve(p):
    if p.get("peso_oz"):
        a, b = p["peso_oz"]
        return f"{round(a * OZ)}–{round(b * OZ)} g"
    if p.get("peso_g"):
        return f"{p['peso_g']} g"
    if p.get("peso_test_oz"):
        return f"~{round(p['peso_test_oz'] * OZ)} g"
    return None


def misura(p, k):
    if p.get(k + "_in"):
        v = p[k + "_in"]
        return f"{num(v * IN)} cm ({num(v, 3)}\")"
    if p.get(k + "_cm"):
        v = p[k + "_cm"]
        return f"{num(v, 2)} cm ({num(v / IN)}\")"
    return None


def prezzo(p):
    if p.get("prezzo_eur"):
        return euro(p["prezzo_eur"])
    if p.get("prezzo_usd"):
        s = f"${p['prezzo_usd']:.2f}"
        return s + L(" (listino USA)", " (US list price)", " (precio de lista EE. UU.)")
    return None


def forma(p):
    return g(FORME[p["forma"]])


def titolo(p):
    return f"{p['marca']} {p['modello']}" if p["marca"] != "VICLION" else f"VICLION {g(nome_set(p))}"


def nome_set(p):
    return {"viclion-set-2-racchette-carbonio": {"it": "Set 2 racchette in carbonio (V2)", "en": "Set of 2 carbon fiber paddles (V2)", "es": "Set de 2 palas de carbono (V2)"},
            "viclion-set-2-racchette-fibra-di-vetro": {"it": "Set 2 racchette in fibra di vetro", "en": "Set of 2 fiberglass paddles", "es": "Set de 2 palas de fibra de vidrio"}}.get(p["slug"], p["modello"])


def nome(p):
    return g(nome_set(p)) if p["marca"] == "VICLION" else p["modello"]


def paddle_svg(f, width=150, label=""):
    """Illustrazione di una racchetta da pickleball: allungata, larga o standard."""
    w, h = {"allungata": (96, 150), "larga": (110, 140), "standard": (104, 140)}[f]
    x = (200 - w) / 2
    y = 14
    fori = "".join(f'<circle cx="{cx}" cy="{cy}" r="3" fill="#FAFAF7" fill-opacity="0.18"/>' for cx in (80, 100, 120) for cy in (60, 85, 110))
    return (f'<svg viewBox="0 0 200 300" width="{width}" role="img" aria-label="{e(label)}"><title>{e(label)}</title>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.32:.0f}" fill="#0F3D2E"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * 0.32:.0f}" fill="none" stroke="#C6F432" stroke-width="5" stroke-opacity="0.9"/>'
            f'{fori}<rect x="88" y="{y + h - 4}" width="24" height="{286 - y - h + 4}" rx="7" fill="#0F3D2E"/>'
            f'<rect x="88" y="{y + h + 40}" width="24" height="5" fill="#C6F432" fill-opacity="0.8"/><rect x="88" y="{y + h + 60}" width="24" height="5" fill="#C6F432" fill-opacity="0.8"/>'
            '<circle cx="158" cy="250" r="14" fill="#C6F432"/><circle cx="153" cy="246" r="2" fill="#0F3D2E"/><circle cx="163" cy="252" r="2" fill="#0F3D2E"/><circle cx="156" cy="256" r="2" fill="#0F3D2E"/></svg>')


def url_p(p):
    return P("pickleball", p["slug"])


def amazon_url(p):
    q = p["amazon"].replace(" ", "+")
    u = f"https://{AMAZON[S.lang()]}/s?k={q}"
    tag = AMAZON_TAG[S.lang()]
    return u + (f"&tag={tag}" if tag else "")


def fonte_link(k):
    n, u = F[k]
    return f'<a href="{e(u)}" rel="nofollow noopener" target="_blank">{e(n)}</a>'


LAB = {"swing": ("Swing weight", "Swing weight", "Swing weight"), "twist": ("Twist weight", "Twist weight", "Twist weight"),
       "bilanciamento": ("Punto di bilanciamento", "Balance point", "Punto de balance"),
       "potenza": ("Velocità al servizio/drive", "Serve/drive speed", "Velocidad de saque/drive"),
       "pop": ("Velocità in volée (pop)", "Punch volley speed (pop)", "Velocidad en volea (pop)"),
       "spin": ("Spin", "Spin", "Efecto (spin)"), "peso": ("Peso misurato", "Measured weight", "Peso medido"),
       "controllo": ("Controllo", "Control", "Control"), "tolleranza": ("Tolleranza", "Forgiveness", "Tolerancia")}


def lab_lab(k):
    return LAB[k][LINGUE.index(S.lang())]


def frase_liv(k):
    return {"principiante": L("per chi inizia", "for beginners", "para quien empieza"),
            "principiante-intermedio": L("per principianti e intermedi", "for beginners and intermediates", "para principiantes e intermedios"),
            "intermedio": L("per giocatori intermedi", "for intermediate players", "para jugadores intermedios"),
            "intermedio-avanzato": L("per intermedi e avanzati", "for intermediate and advanced players", "para intermedios y avanzados"),
            "avanzato": L("per giocatori avanzati", "for advanced players", "para jugadores avanzados")}[k]


def in_breve(p):
    f = forma(p).lower().split(" (")[0]
    sp = f"{p['spessore_mm']} mm" if p.get("spessore_mm") else None
    pb = peso_breve(p)
    if p.get("set"):
        base = L(f"Il {titolo(p)} è un set da pickleball con racchette di forma {f}", f"The {titolo(p)} is a pickleball set with {f}-shape paddles",
                 f"El {titolo(p)} es un set de pickleball con palas de forma {f}")
    else:
        base = L(f"La {titolo(p)} è una racchetta da pickleball {f}", f"The {titolo(p)} is {'an' if f[0] in 'aeiou' else 'a'} {f} pickleball paddle",
                 f"La {titolo(p)} es una pala de pickleball {f}")
    extra = []
    if sp:
        extra.append(L(f"nucleo da {sp}", f"{sp} core", f"núcleo de {sp}"))
    if pb:
        extra.append(pb)
    t = base + (L(" con ", " with ", " con ") + L(" e ", " and ", " y ").join(extra) if extra else "")
    t += " " + frase_liv(p["livello"])
    if p.get("giocatore"):
        t += L(f", firmata da {p['giocatore']}", f", signed by {p['giocatore']}", f", firmada por {p['giocatore']}")
    return t + "."


def specifiche(p):
    righe = [(L("Marca", "Brand", "Marca"), p["marca"]), (L("Modello", "Model", "Modelo"), nome(p)),
             (L("Giocatore", "Player", "Jugador"), p.get("giocatore")),
             (L("Forma", "Shape", "Forma"), forma(p)),
             (L("Peso", "Weight", "Peso"), peso(p))]
    if p.get("peso_swift_oz"):
        righe.append((L("Versione leggera (Swift)", "Light version (Swift)", "Versión ligera (Swift)"), f"{num(p['peso_swift_oz'])} oz ({round(p['peso_swift_oz'] * OZ)} g)"))
    righe += [(L("Lunghezza", "Length", "Longitud"), misura(p, "lunghezza")), (L("Larghezza", "Width", "Anchura"), misura(p, "larghezza")),
              (L("Lunghezza manico", "Handle length", "Longitud del mango"), misura(p, "manico")),
              (L("Circonferenza grip", "Grip circumference", "Circunferencia del grip"), misura(p, "grip")),
              (L("Spessore nucleo", "Core thickness", "Grosor del núcleo"), f"{p['spessore_mm']} mm" if p.get("spessore_mm") else None),
              (L("Nucleo", "Core", "Núcleo"), g(p["nucleo"])), (L("Faccia", "Face", "Cara"), g(p["faccia"])),
              (L("Omologazioni", "Approvals", "Homologaciones"), p.get("approvazioni"))]
    if p.get("set"):
        righe.append((L("Contenuto", "Contents", "Contenido"), g(p["set"])))
    righe += [(L("Livello (stima PadelMetrix)", "Level (PadelMetrix estimate)", "Nivel (estimación PadelMetrix)"), LIVN(p["livello"])),
              (L("Stile", "Style", "Estilo"), STILEN(p["stile"])),
              (L("Prezzo di listino", "List price", "Precio de lista"), prezzo(p))]
    nd = L("Non dichiarato", "Not stated", "No declarado")
    return [(k, v or nd) for k, v in righe if not (k == L("Giocatore", "Player", "Jugador") and not v)]


def simili(p):
    def score(o):
        s = 0
        s += 3 if o["forma"] == p["forma"] else 0
        s += 2 if o["livello"] == p["livello"] else 0
        s += 2 if o.get("spessore_mm") == p.get("spessore_mm") else 0
        s += 1 if o["stile"] == p["stile"] else 0
        s += 1 if o["marca"] == p["marca"] else 0
        return s
    altri = sorted((o for o in PADDLE if o is not p), key=lambda o: (-score(o), o["slug"]))
    return altri[:3]


def chips(p):
    c = [forma(p)]
    if p.get("spessore_mm"):
        c.append(f"{p['spessore_mm']} mm")
    if peso_breve(p):
        c.append(peso_breve(p))
    c.append(LIVN(p["livello"]))
    if p.get("approvazioni"):
        c.append(p["approvazioni"])
    return c


def faq(p):
    t = titolo(p)
    qa = []
    if peso(p):
        qa.append((L(f"Quanto pesa la {t}?", f"How much does the {t} weigh?", f"¿Cuánto pesa la {t}?"),
                   L(f"Secondo i dati pubblicati pesa {peso(p)}.", f"According to published data it weighs {peso(p)}.", f"Según los datos publicados pesa {peso(p)}.")))
    if p.get("spessore_mm"):
        sp = p["spessore_mm"]
        spieg = (L("Un nucleo sottile dà più spinta immediata e meno controllo nel gioco morbido.", "A thin core gives more immediate pop and less control in the soft game.", "Un núcleo fino da más empuje inmediato y menos control en el juego suave.")
                 if sp <= 14 else L("Un nucleo spesso aumenta controllo, stabilità e tempo di permanenza della palla.", "A thick core adds control, stability and dwell time.", "Un núcleo grueso aumenta el control, la estabilidad y el tiempo de permanencia de la bola."))
        qa.append((L(f"Che spessore ha la {t}?", f"How thick is the {t}?", f"¿Qué grosor tiene la {t}?"),
                   L(f"Il nucleo è da {sp} mm. ", f"The core is {sp} mm. ", f"El núcleo es de {sp} mm. ") + spieg))
    if p.get("approvazioni"):
        qa.append((L(f"La {t} è omologata per i tornei?", f"Is the {t} approved for tournaments?", f"¿La {t} está homologada para torneos?"),
                   L(f"Sì: risulta omologata {p['approvazioni']}.", f"Yes: it is listed as {p['approvazioni']} approved.", f"Sí: figura como homologada {p['approvazioni']}.")))
    qa.append((L(f"Per che livello è la {t}?", f"What level is the {t} for?", f"¿Para qué nivel es la {t}?"),
               L(f"Secondo la nostra stima, basata su materiali, peso e recensioni: livello {LIVN(p['livello']).lower()}.",
                 f"In our estimate, based on materials, weight and reviews: {LIVN(p['livello']).lower()} level.",
                 f"Según nuestra estimación, basada en materiales, peso y reseñas: nivel {LIVN(p['livello']).lower()}.")))
    return qa


def scheda(p):
    t = titolo(p)
    path, alt = url_p(p), ALT("pickleball", p["slug"])
    tx = {k: (g(v) if isinstance(v, dict) else [g(x) for x in v]) for k, v in p["t"].items()}
    breve = in_breve(p)
    qa = faq(p)
    cr, cr_ld = crumbs([S.home_crumb(), ("Pickleball", P("pickleball")), (nome(p), None)])
    blocco = ""
    if p.get("valutazioni"):
        v = p["valutazioni"]
        rows = "".join(f'<div class="bar"><span>{lab_lab(k)}</span><div class="track"><div class="fill" style="width:{round(x / v["scala"] * 100)}%"></div></div><span class="v">{num(x)}{"%" if v["scala"] == 100 else ""}</span></div>' for k, x in v["voci"])
        blocco = (f'<div class="card"><h2>{L("Valutazioni di", "Ratings from", "Valoraciones de")} {e(F[v["fonte"]][0])}</h2><div class="bars">{rows}</div>'
                  f'<p class="note">{L("Punteggi pubblicati da", "Scores published by", "Puntuaciones publicadas por")} {fonte_link(v["fonte"])}{L(" su ", " out of ", " sobre ")}{v["scala"]}. {L("Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.", "The PadelMetrix score will follow with our own rating method.", "La puntuación PadelMetrix llegará con nuestro método de valoración.")}</p></div>')
    if p.get("lab"):
        def tab(lab, fk):
            return (f'<dl class="specs">' + "".join(f"<div><dt>{lab_lab(k)}</dt><dd>{e(numtxt(v))}</dd></div>" for k, v in lab) + "</dl>"
                    f'<p class="note">{L("Misure di laboratorio di", "Lab measurements by", "Medidas de laboratorio de")} {fonte_link(fk)}.</p>')
        blocco += f'<div class="card"><h2>{L("Dati di laboratorio", "Lab data", "Datos de laboratorio")}</h2>{tab(p["lab"], p["lab_fonte"])}'
        if p.get("lab2"):
            blocco += tab(p["lab2"], p["lab2_fonte"])
        blocco += "</div>"
    nota_lab = L("Swing weight: quanto pesa la racchetta in movimento (più alto = più stabile, più lenta). Twist weight: resistenza alla torsione sui colpi decentrati (più alto = più tollerante).",
                 "Swing weight: how heavy the paddle feels in motion (higher = more stable, slower). Twist weight: resistance to twisting on off-centre hits (higher = more forgiving).",
                 "Swing weight: cuánto pesa la pala en movimiento (más alto = más estable, más lenta). Twist weight: resistencia a la torsión en golpes descentrados (más alto = más tolerante).") if p.get("lab") else ""
    nota_aff = L("Il link verso Amazon è un link di affiliazione: se acquisti, PadelMetrix può ricevere una commissione senza costi per te.",
                 "The Amazon link is an affiliate link: if you buy, PadelMetrix may receive a commission at no cost to you.",
                 "El enlace a Amazon es un enlace de afiliado: si compras, PadelMetrix puede recibir una comisión sin coste para ti.")
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)  # noqa: E731
    sim = "".join(f'<a href="{url_p(o)}"><small>{e(o["marca"])}</small><b>{e(nome(o))}</b><small>{e(forma(o))}{", " + str(o["spessore_mm"]) + " mm" if o.get("spessore_mm") else ""}, {e(LIVN(o["livello"]).lower())}</small></a>' for o in simili(p))
    fonti = " · ".join(fonte_link(k) for k in p["fonti"])
    corpo = f"""{cr}
<div class="top">
<div class="photo">{paddle_svg(p["forma"], 200, t)}</div>
<div class="info">
<div>
<div class="eyebrow">{e(p["marca"])} · Pickleball{" · " + str(p["anno"]) if p.get("anno") else ""}</div>
<h1>{e(t)}</h1>
<p class="note" style="margin-top:6px">{L("Aggiornata il", "Updated on", "Actualizada el")} {data_txt()} · {L("dati con fonti citate", "data with cited sources", "datos con fuentes citadas")} · <a href="{P("chi-siamo")}">{L("metodo", "method", "método")}</a></p>
</div>
<p class="lead" style="font-weight:600;color:var(--ink)">{e(breve)}</p>
<div class="chips">{"".join(f"<span>{e(c)}</span>" for c in chips(p))}</div>
<p class="lead">{e(tx["lead"])}</p>
{blocco}
<div class="card">
<h2>{L("Dove comprare la", "Where to buy the", "Dónde comprar la")} {e(nome(p))}</h2>
<div class="stores"><div class="store"><div><strong>Amazon</strong><small>{L("Spedizione e resi Amazon", "Amazon shipping and returns", "Envío y devoluciones de Amazon")}</small></div><a class="btn lime" href="{e(amazon_url(p))}" rel="sponsored nofollow noopener" target="_blank">{L("Vedi su Amazon", "View on Amazon", "Ver en Amazon")}</a></div></div>
<p class="note">{L("I prezzi su Amazon cambiano spesso: quello in scheda è il listino indicato dalla fonte.", "Amazon prices change often: the one on this page is the list price given by the source.", "Los precios en Amazon cambian a menudo: el de la ficha es el precio de lista indicado por la fuente.")} {nota_aff}</p>
</div>
</div>
</div>

<section class="block">
<h2>{L("Dati tecnici della", "Technical specs of the", "Datos técnicos de la")} {e(nome(p))}</h2>
<dl class="specs">{"".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in specifiche(p))}</dl>
<p class="note">{L("Fonti", "Sources", "Fuentes")}: {fonti}. {e(nota_lab)}</p>
</section>

<section class="block">
<h2>{e(nome(p))}: {L("recensioni e opinioni", "reviews and opinions", "reseñas y opiniones")}</h2>
<div class="card"><p style="margin:0;font-size:16px">{e(tx["sintesi"])}</p></div>
<div class="two">
<div class="card pros"><h3>{L("Punti di forza", "Strengths", "Puntos fuertes")}</h3><ul class="clean">{li(tx["pro"])}</ul></div>
<div class="card cons"><h3>{L("Limiti", "Limitations", "Limitaciones")}</h3><ul class="clean">{li(tx["contro"])}</ul></div>
</div>
<div class="two">
<div class="card"><h3 style="font-size:17px">{L("È adatta se", "It suits you if", "Es para ti si")}</h3><ul class="clean">{li(tx["adatta"])}</ul></div>
<div class="card"><h3 style="font-size:17px">{L("Meglio un'altra racchetta se", "Better choose another paddle if", "Mejor otra pala si")}</h3><ul class="clean">{li(tx["non_adatta"])}</ul></div>
</div>
</section>

<section class="block">
<h2>{L("Racchette da pickleball simili", "Similar pickleball paddles", "Palas de pickleball similares")}</h2>
<div class="sim">{sim}</div>
<p><a class="btn out" href="{P("pickleball")}">{L("Tutte le racchette da pickleball", "All pickleball paddles", "Todas las palas de pickleball")}</a></p>
</section>

<section class="block faq"><h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes")}</h2>{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa)}</section>
<p class="note" style="padding-bottom:24px">{L("Scheda aggiornata il", "Page updated on", "Ficha actualizada el")} {data_txt()}.</p>"""
    title = L(f"{t}: scheda tecnica e opinioni (pickleball)", f"{t}: specs and reviews (pickleball)", f"{t}: ficha técnica y opiniones (pickleball)")
    prod = {"@context": "https://schema.org", "@type": "Product", "name": t, "brand": {"@type": "Brand", "name": p["marca"]},
            "category": L("Racchetta da pickleball", "Pickleball paddle", "Pala de pickleball"), "description": breve, "url": SITO + path}
    web = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "url": SITO + path, "dateModified": OGGI, "inLanguage": S.lang(),
           "author": S.autore(), "publisher": S.editore()}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    S.scrivi(path, pagina(f"{title} | PadelMetrix", breve[:165], path, corpo, on="pickleball", ld=[web, prod, cr_ld, faqld], alt=alt), alt)


FILTRI_JS = """<script>(function(){var f=document.getElementById('filtri');if(!f)return;var cards=[].slice.call(document.querySelectorAll('.rgrid .rcard'));var out=document.getElementById('conta');
function run(){var v={};['marca','forma','livello'].forEach(function(k){v[k]=f.elements[k].value;});var n=0;cards.forEach(function(c){var d=c.dataset,ok=(!v.marca||d.marca===v.marca)&&(!v.forma||d.forma===v.forma)&&(!v.livello||d.livello===v.livello);c.style.display=ok?'':'none';if(ok)n++;});out.textContent=n+' %s';}
f.addEventListener('change',run);run();})();</script>"""


def elenco():
    path, alt = P("pickleball"), ALT("pickleball")
    cr, cr_ld = crumbs([S.home_crumb(), ("Pickleball", None)])
    marche = sorted({p["marca"] for p in PADDLE})
    livs = [k for k in S.LIV if any(p["livello"] == k for p in PADDLE)]
    opt = lambda vals, lab: f'<option value="">{lab}</option>' + "".join(f'<option value="{v}">{e(t)}</option>' for v, t in vals)  # noqa: E731
    tutte, tutti = L("Tutte", "All", "Todas"), L("Tutti", "All", "Todos")
    form = (f'<form class="filtri" id="filtri" onsubmit="return false">'
            f'<label>{L("Marca", "Brand", "Marca")}<select name="marca">{opt([(m, m) for m in marche], tutte)}</select></label>'
            f'<label>{L("Forma", "Shape", "Forma")}<select name="forma">{opt([(k, g(v)) for k, v in FORME.items()], tutte)}</select></label>'
            f'<label>{L("Livello", "Level", "Nivel")}<select name="livello">{opt([(k, LIVN(k)) for k in livs], tutti)}</select></label></form>')
    cards = "".join(
        f'<a class="rcard" href="{url_p(p)}" data-marca="{p["marca"]}" data-forma="{p["forma"]}" data-livello="{p["livello"]}"><div class="ill">{paddle_svg(p["forma"], 60, titolo(p))}</div>'
        f'<div><small>{e(p["marca"])}{" · " + str(p["anno"]) if p.get("anno") else ""}</small><b>{e(nome(p))}</b><small>{e(" · ".join(x for x in (forma(p), str(p["spessore_mm"]) + " mm" if p.get("spessore_mm") else None, LIVN(p["livello"])) if x))}</small></div></a>'
        for p in PADDLE)
    qa = [(L("Che differenza c'è tra pickleball e padel?", "What is the difference between pickleball and padel?", "¿Qué diferencia hay entre pickleball y pádel?"),
           L("Il pickleball si gioca su un campo più piccolo, senza pareti, con una pallina di plastica forata e una racchetta piatta senza fori (paddle). Il padel ha le pareti, una pallina pressurizzata e racchette forate più spesse e pesanti.",
             "Pickleball is played on a smaller court without walls, with a perforated plastic ball and a flat paddle without holes. Padel has walls, a pressurised ball and thicker, heavier perforated rackets.",
             "El pickleball se juega en una pista más pequeña, sin paredes, con una pelota de plástico perforada y una pala plana sin agujeros (paddle). El pádel tiene paredes, una pelota presurizada y palas perforadas más gruesas y pesadas.")),
          (L("Meglio un nucleo da 14 o da 16 mm?", "Is a 14 mm or 16 mm core better?", "¿Mejor un núcleo de 14 o de 16 mm?"),
           L("Il 16 mm dà più controllo e stabilità nel gioco morbido; il 14 mm è più reattivo e veloce, con più spinta immediata. Chi inizia di solito si trova meglio con 16 mm o con racchette d'ingresso da 12–14 mm in fibra di vetro.",
             "16 mm gives more control and stability in the soft game; 14 mm is more responsive and faster, with more immediate pop. Beginners usually do better with 16 mm or with 12–14 mm fiberglass entry paddles.",
             "El de 16 mm da más control y estabilidad en el juego suave; el de 14 mm es más reactivo y rápido, con más empuje inmediato. Quien empieza suele ir mejor con 16 mm o con palas de iniciación de 12–14 mm de fibra de vidrio.")),
          (L("Cosa vuol dire omologata USAP o UPA-A?", "What does USAP or UPA-A approved mean?", "¿Qué significa homologada USAP o UPA-A?"),
           L("Che la racchetta rispetta le regole delle due principali federazioni statunitensi (USA Pickleball e United Pickleball Association) ed è ammessa nei loro tornei. Per giocare per divertimento non serve.",
             "That the paddle meets the rules of the two main US bodies (USA Pickleball and the United Pickleball Association) and is allowed in their tournaments. It is not needed for recreational play.",
             "Que la pala cumple las reglas de las dos principales federaciones estadounidenses (USA Pickleball y United Pickleball Association) y está admitida en sus torneos. Para jugar por diversión no hace falta.")),
          (L("Quanto deve pesare una racchetta da pickleball?", "How much should a pickleball paddle weigh?", "¿Cuánto debe pesar una pala de pickleball?"),
           L("Tra le racchette in questa pagina il peso va da circa 220 a 245 grammi (7,6–8,6 oz). Le più pesanti sono più stabili e potenti, le più leggere più rapide a rete e meno faticose per il braccio.",
             "Among the paddles on this page, weight ranges from about 220 to 245 grams (7.6–8.6 oz). Heavier paddles are more stable and powerful, lighter ones quicker at the net and easier on the arm.",
             "Entre las palas de esta página el peso va de unos 220 a 245 gramos (7,6–8,6 oz). Las más pesadas son más estables y potentes, las más ligeras más rápidas en la red y menos cansadas para el brazo."))]
    corpo = f"""{cr}
<div class="intro"><h1>{L("Racchette da pickleball: schede e opinioni", "Pickleball paddles: specs and reviews", "Palas de pickleball: fichas y opiniones")}</h1>
<p><b>{L(f"{len(PADDLE)} racchette da pickleball (paddle) di JOOLA e VICLION, tutte acquistabili su Amazon, con dati tecnici, misure di laboratorio dove esistono e sintesi delle recensioni indipendenti.", f"{len(PADDLE)} pickleball paddles from JOOLA and VICLION, all available on Amazon, with specs, lab measurements where available and summaries of independent reviews.", f"{len(PADDLE)} palas de pickleball (paddle) de JOOLA y VICLION, todas disponibles en Amazon, con datos técnicos, medidas de laboratorio cuando existen y resumen de las reseñas independientes.")}</b> {L("Per chi inizia vanno bene le racchette in fibra di vetro da 12–14 mm o i set da due; chi gioca già con regolarità guarda al carbonio e allo spessore del nucleo.", "Beginners do well with 12–14 mm fiberglass paddles or two-paddle sets; regular players should look at carbon faces and core thickness.", "Para quien empieza van bien las palas de fibra de vidrio de 12–14 mm o los sets de dos; quien ya juega con regularidad debe fijarse en el carbono y el grosor del núcleo.")}</p>{S.data_riga()}</div>
{form}
<p class="conta" id="conta">{len(PADDLE)} {L("racchette", "paddles", "palas")}</p>
<div class="rgrid">{cards}</div>
<div class="prose">
<h2>{L("Come scegliere la racchetta da pickleball", "How to choose a pickleball paddle", "Cómo elegir la pala de pickleball")}</h2>
<ul>
<li><b>{L("Forma", "Shape", "Forma")}:</b> {L("allungata (circa 42 × 19 cm) per portata e potenza; larga (circa 41 × 20 cm) per stabilità e uno sweet spot più ampio.", "elongated (about 16.5 × 7.5 in) for reach and power; widebody (about 16 × 8 in) for stability and a larger sweet spot.", "alargada (unos 42 × 19 cm) para alcance y potencia; ancha (unos 41 × 20 cm) para estabilidad y un punto dulce más amplio.")}</li>
<li><b>{L("Spessore", "Thickness", "Grosor")}:</b> {L("16 mm per controllo, 14 mm per reattività, 12 mm nelle racchette d'ingresso.", "16 mm for control, 14 mm for responsiveness, 12 mm on entry paddles.", "16 mm para control, 14 mm para reactividad, 12 mm en las palas de iniciación.")}</li>
<li><b>{L("Faccia", "Face", "Cara")}:</b> {L("la fibra di vetro è più morbida ed economica; il carbonio testurizzato dà più controllo ed effetto.", "fiberglass is softer and cheaper; textured carbon gives more control and spin.", "la fibra de vidrio es más blanda y económica; el carbono texturizado da más control y efecto.")}</li>
<li><b>{L("Manico", "Handle", "Mango")}:</b> {L("un manico lungo (circa 14 cm) aiuta chi gioca il rovescio a due mani.", "a long handle (about 5.5 in) helps two-handed backhands.", "un mango largo (unos 14 cm) ayuda a quien juega el revés a dos manos.")}</li>
</ul>
<h2>{L("Domande frequenti", "Frequently asked questions", "Preguntas frecuentes")}</h2><div class="faq">{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in qa)}</div>
</div>"""
    il = {"@context": "https://schema.org", "@type": "ItemList", "numberOfItems": len(PADDLE),
          "itemListElement": [{"@type": "ListItem", "position": i, "url": SITO + url_p(p), "name": titolo(p)} for i, p in enumerate(PADDLE, 1)]}
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    S.scrivi(path, pagina(L("Racchette da pickleball JOOLA e VICLION: schede, opinioni e prezzi | PadelMetrix", "JOOLA and VICLION pickleball paddles: specs, reviews and prices | PadelMetrix",
                            "Palas de pickleball JOOLA y VICLION: fichas, opiniones y precios | PadelMetrix"),
                          L("Racchette da pickleball JOOLA e VICLION su Amazon: peso, spessore, forma, dati di laboratorio e opinioni, e come scegliere quella giusta.",
                            "JOOLA and VICLION pickleball paddles on Amazon: weight, thickness, shape, lab data and reviews, and how to choose the right one.",
                            "Palas de pickleball JOOLA y VICLION en Amazon: peso, grosor, forma, datos de laboratorio y opiniones, y cómo elegir la adecuada."),
                          path, corpo, on="pickleball", ld=[cr_ld, il, faqld], extra_js=FILTRI_JS % L("racchette", "paddles", "palas"), alt=alt), alt)


def main():
    for l in LINGUE:
        set_lang(l)
        elenco()
        for p in PADDLE:
            scheda(p)
    set_lang("it")
    (ROOT / "scripts" / "pagine_pickleball.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine pickleball generate")


if __name__ == "__main__":
    main()
