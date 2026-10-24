"""Traduzione IT -> EN/ES dei testi delle schede: memoria di traduzione + modelli per le frasi generate."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TMDIR = ROOT / "data" / "traduzioni"
LANGS = ("en", "es")
MANCANTI = {"en": set(), "es": set()}

_TM = {}


def tm(lang):
    if lang not in _TM:
        _TM[lang] = {}
        for f in sorted(TMDIR.glob("tm_pair_*.json")):
            for it, (en, es) in json.loads(f.read_text(encoding="utf-8")).items():
                _TM[lang][it] = en if lang == "en" else es
    return _TM[lang]


def num(s, lang):
    """Decimali: virgola in IT/ES, punto in EN."""
    if lang == "en":
        return re.sub(r"(\d),(\d)", r"\1.\2", s)
    return s


# ---------------------------------------------------------------- vocabolari fissi

VOCI = {"potenza": ("power", "potencia"), "controllo": ("control", "control"), "uscita di palla": ("ball output", "salida de bola"),
        "maneggevolezza": ("maneuverability", "manejabilidad"), "sweet spot": ("sweet spot", "punto dulce"),
        "stabilità": ("stability", "estabilidad"), "rigidità": ("stiffness", "rigidez"), "effetto": ("spin", "efecto"),
        "comfort": ("comfort", "confort"), "giocabilità": ("playability", "jugabilidad"), "rebote": ("rebound", "rebote")}
FORME = {"diamante": ("diamond", "diamante"), "rotonda": ("round", "redonda"), "goccia": ("teardrop", "lágrima"), "ibrida": ("hybrid", "híbrida"),
         "geometrica": ("geometric", "geométrica")}
LIVELLI = {"Principiante": ("Beginner", "Principiante"), "Principiante / intermedio": ("Beginner / intermediate", "Principiante / intermedio"),
           "Intermedio": ("Intermediate", "Intermedio"), "Intermedio / avanzato": ("Intermediate / advanced", "Intermedio / avanzado"),
           "Avanzato": ("Advanced", "Avanzado"), "Avanzato / professionale": ("Advanced / professional", "Avanzado / profesional"),
           "Intermedio alto / avanzato": ("Upper intermediate / advanced", "Intermedio alto / avanzado"),
           "Avanzato / professionale ": ("Advanced / professional", "Avanzado / profesional")}
STILI = {"Offensivo": ("Attacking", "Ofensivo"), "Controllo": ("Control", "Control"), "Polivalente": ("All-round", "Polivalente"),
         "Attacco": ("Attack", "Ataque")}
STILE_CHIP = {"Racchetta d'attacco": ("Attacking racket", "Pala de ataque"), "Racchetta di controllo": ("Control racket", "Pala de control"),
              "Polivalente": ("All-round", "Polivalente")}
TATTI = {"morbido": ("soft", "blando"), "medio-morbido": ("medium-soft", "medio-blando"), "medio": ("medium", "medio"),
         "medio-duro": ("medium-hard", "medio-duro"), "duro": ("hard", "duro"), "secco": ("crisp", "seco"), "fermo": ("firm", "firme"),
         "medio-secco": ("medium-crisp", "medio-seco"), "secco e fermo": ("crisp and firm", "seco y firme"), "ruvida": ("rough", "rugoso"),
         "molto morbido": ("very soft", "muy blando"), "Dura": ("Hard", "Dura"), "Medio": ("Medium", "Medio"), "Medio-duro": ("Medium-hard", "Medio-duro"),
         "Medio-morbido": ("Medium-soft", "Medio-blando"), "Morbido": ("Soft", "Blando"), "Duro": ("Hard", "Duro")}
BIL = {"alto": ("high", "alto"), "medio": ("medium", "medio"), "basso": ("low", "bajo"), "medio-alto": ("medium-high", "medio-alto"),
       "medio-basso": ("medium-low", "medio-bajo"), "neutro": ("neutral", "neutro"), "contenuto": ("moderate", "contenido")}
LIV_FRASE = {"chi inizia": ("beginners", "quien empieza"), "principianti e intermedi": ("beginners and intermediates", "principiantes e intermedios"),
             "giocatori intermedi": ("intermediate players", "jugadores intermedios"), "intermedi alti e avanzati": ("upper intermediate and advanced players", "intermedios altos y avanzados"),
             "giocatori avanzati": ("advanced players", "jugadores avanzados"), "giocatori avanzati e agonisti": ("advanced and competitive players", "jugadores avanzados y de competición")}
LIV_LOWER = {"principiante": ("beginner", "principiante"), "principiante / intermedio": ("beginner / intermediate", "principiante / intermedio"),
             "intermedio": ("intermediate", "intermedio"), "intermedio / avanzato": ("intermediate / advanced", "intermedio / avanzado"),
             "avanzato": ("advanced", "avanzado"), "avanzato / professionale": ("advanced / professional", "avanzado / profesional")}
LABELS = {"Marca": ("Brand", "Marca"), "Modello": ("Model", "Modelo"), "Collezione": ("Collection", "Colección"), "Anno": ("Year", "Año"),
          "Linea": ("Line", "Línea"), "Giocatore": ("Player", "Jugador"), "Categoria": ("Category", "Categoría"), "Forma": ("Shape", "Forma"),
          "Peso": ("Weight", "Peso"), "Bilanciamento": ("Balance", "Balance"), "Nucleo": ("Core", "Núcleo"), "Gomma": ("Core rubber", "Goma"),
          "Superficie": ("Face", "Cara"), "Telaio": ("Frame", "Marco"), "Spessore": ("Thickness", "Grosor"), "Finitura": ("Finish", "Acabado"),
          "Rigidità": ("Stiffness", "Rigidez"), "Tatto": ("Feel", "Tacto"), "Sensazione": ("Feel", "Tacto"), "Livello": ("Level", "Nivel"),
          "Livello consigliato": ("Recommended level", "Nivel recomendado"), "Stile di gioco": ("Playing style", "Estilo de juego"),
          "Personalizzazione": ("Customization", "Personalización"), "Superficie di gioco": ("Hitting surface", "Superficie de juego"),
          "Foratura": ("Hole pattern", "Taladrado"), "Tecnologie di linea": ("Line technologies", "Tecnologías de la línea"),
          "Edizioni": ("Editions", "Ediciones"), "Durezza misurata": ("Measured hardness", "Dureza medida"),
          "Swingweight misurato": ("Measured swingweight", "Swingweight medido"), "Colori": ("Colours", "Colores"),
          "Prezzo di listino": ("List price", "Precio de lista")}


def pick(d, k, lang):
    v = d.get(k)
    return v[0 if lang == "en" else 1] if v else None


# ---------------------------------------------------------------- modelli per le frasi generate

def _forma_w(w, lang):
    return pick(FORME, w.lower(), lang) or w


def _voce(w, lang):
    return pick(VOCI, w.lower(), lang) or w


def handlers(lang):
    en = lang == "en"
    H = []

    def add(pat, fn):
        H.append((re.compile(pat), fn))

    # numeri, pesi, prezzi puri
    add(r"^[\d\s–\-,\.±()+g€/]+$", lambda m: num(m.group(0), lang))
    add(r"^(\d+[–-]\d+ g) \(\+ fino a ([\d,]+) g\)$", lambda m: f"{m.group(1)} (+ up to {num(m.group(2), lang)} g)" if en else f"{m.group(1)} (+ hasta {m.group(2)} g)")
    add(r"^circa (\d+ g)$", lambda m: ("about " if en else "unos ") + m.group(1))
    add(r"^(\d+ g) \(±(\d+)\)$", lambda m: f"{m.group(1)} (±{m.group(2)})")
    add(r"^Non dichiarat[oa]$", lambda m: "Not stated" if en else "No declarado")
    add(r"^Junior$", lambda m: "Junior")
    add(r"^Modello femminile$", lambda m: "Women's model" if en else "Modelo femenino")
    add(r"^Racchetta di ([A-ZÁÉÍÓÚ][^,.;:]*)$", lambda m: (f"{m.group(1)}'s racket" if en else f"Pala de {m.group(1)}"))
    add(r"^Carbonio (\d+K)$", lambda m: (f"{m.group(1)} carbon" if en else f"Carbono {m.group(1)}"))
    add(r"^Fibra di vetro$", lambda m: "Fiberglass" if en else "Fibra de vidrio")
    add(r"^Bilanciamento (.+)$", lambda m: (f"{(pick(BIL, m.group(1), lang) or t(m.group(1), lang)).capitalize()} balance" if en else f"Balance {pick(BIL, m.group(1), lang) or t(m.group(1), lang)}"))
    add(r"^(Diamante|Rotonda|Goccia|Ibrida)$", lambda m: _forma_w(m.group(1), lang).capitalize())
    add(r"^(Diamante|Rotonda|Goccia|Ibrida) \((.+)\)$", lambda m: f"{_forma_w(m.group(1), lang).capitalize()} ({t(m.group(2), lang)})")
    add(r"^Forma (.+)$", lambda m: (f"{t(m.group(1), lang).capitalize()} shape" if en else f"Forma {t(m.group(1), lang)}"))
    add(r"^(diamante|rotonda|goccia|ibrida|geometrica)$", lambda m: _forma_w(m.group(1), lang))
    add(r"^(goccia|rotonda|diamante) / (ibrida|goccia)$", lambda m: f"{_forma_w(m.group(1), lang)} / {_forma_w(m.group(2), lang)}")
    add(r"^(ibrida) tendente alla rotonda$", lambda m: "hybrid leaning round" if en else "híbrida tirando a redonda")
    add(r"^(Alto|Medio|Basso|Medio-alto|Medio-basso|Neutro|Contenuto)( \((.+)\))?$",
        lambda m: (pick(BIL, m.group(1).lower(), lang).capitalize() + (f" ({num(m.group(3), lang).replace('circa ', 'about ' if en else 'aprox. ')})" if m.group(3) else "")))
    add(r"^(alto|medio|basso|medio-alto|medio-basso|neutro|contenuto) \((.+)\)$",
        lambda m: pick(BIL, m.group(1), lang) + f" ({num(m.group(2), lang).replace('circa ', 'about ' if en else 'aprox. ')})")
    add(r"^Livello (.+)$", lambda m: ((pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)).capitalize() + " level" if en else "Nivel " + (pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang))))
    add(r"^Tatto (.+)$", lambda m: ((pick(TATTI, m.group(1), lang) or t(m.group(1), lang)).capitalize() + " feel" if en else "Tacto " + (pick(TATTI, m.group(1), lang) or t(m.group(1), lang))))
    add(r"^Durezza misurata (\d+)$", lambda m: (f"Measured hardness {m.group(1)}" if en else f"Dureza medida {m.group(1)}"))
    add(r"^Potenza ([\d,]+)/10 secondo (.+)$", lambda m: (f"Power {num(m.group(1), lang)}/10 according to {m.group(2)}" if en else f"Potencia {m.group(1)}/10 según {m.group(2)}"))
    add(r"^(.+) · Collezione (\d{4})( · Junior| · Donna)?$",
        lambda m: f"{m.group(1)} · {m.group(2)} collection" + ({" · Junior": " · Junior", " · Donna": " · Women"}.get(m.group(3), "") if en else "")
        if en else f"{m.group(1)} · Colección {m.group(2)}" + {" · Junior": " · Junior", " · Donna": " · Mujer"}.get(m.group(3) or "", ""))
    add(r"^(.+) · Collezione (\d{4}) · (.+)$", lambda m: (f"{m.group(1)} · {m.group(2)} collection · {t(m.group(3), lang)}" if en else f"{m.group(1)} · Colección {m.group(2)} · {t(m.group(3), lang)}"))
    add(r"^([\d,]+)/10$", lambda m: num(m.group(0), lang))
    add(r"^([\d,]+)/10 \(community ([\d,]+)/10, (\d+) recensioni\)$", lambda m: (f"{num(m.group(1), lang)}/10 (community {num(m.group(2), lang)}/10, {m.group(3)} reviews)" if en else f"{m.group(1)}/10 (comunidad {m.group(2)}/10, {m.group(3)} reseñas)"))
    add(r"^potenza ([\d,]+) · controllo ([\d,]+)$", lambda m: (f"power {num(m.group(1), lang)} · control {num(m.group(2), lang)}" if en else f"potencia {m.group(1)} · control {m.group(2)}"))
    add(r"^(.+?) ([\d,]+) · (.+?) ([\d,]+)$", lambda m: f"{_voce(m.group(1), lang)} {num(m.group(2), lang)} · {_voce(m.group(3), lang)} {num(m.group(4), lang)}")
    # valutazioni e note generate
    add(r"^Valutazioni di (.+)$", lambda m: (f"{m.group(1)} ratings" if en else f"Valoraciones de {m.group(1)}"))
    add(r"^Valutazioni del produttore$", lambda m: "Manufacturer ratings" if en else "Valoraciones del fabricante")
    add(r"^Valutazioni (PadelZoom|Padelful)$", lambda m: (f"{m.group(1)} ratings" if en else f"Valoraciones de {m.group(1)}"))
    add(r"^Punteggi su 10 pubblicati da (<a [^>]+>[^<]+</a>), voto complessivo ([\d,]+)/10\. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$",
        lambda m: (f"Scores out of 10 published by {m.group(1)}, overall score {num(m.group(2), lang)}/10. The PadelMetrix score will follow with our own rating method." if en
                   else f"Puntuaciones sobre 10 publicadas por {m.group(1)}, nota global {m.group(2)}/10. La puntuación PadelMetrix llegará con nuestro método de valoración."))
    add(r"^In sintesi$", lambda m: "At a glance" if en else "En resumen")
    add(r"^Spedizione e resi Amazon$", lambda m: "Amazon shipping and returns" if en else "Envío y devoluciones de Amazon")
    add(r"^Scheda prodotto del rivenditore$", lambda m: "Retailer product page" if en else "Ficha de producto del vendedor")
    add(r"^Vedi su Amazon$", lambda m: "View on Amazon" if en else "Ver en Amazon")
    add(r"^Vedi sul sito$", lambda m: "View on site" if en else "Ver en la web")
    add(r"^Prezzo di listino indicativo ([\d\.,]+) € secondo i rivenditori consultati a ottobre 2026; i prezzi reali cambiano spesso, verifica sul negozio\.$",
        lambda m: (f"Indicative list price €{num(m.group(1), lang).replace('.', '#').replace(',', '.').replace('#', ',') if False else num(m.group(1), lang)} according to retailers checked in October 2026; actual prices change often, check the shop." if en
                   else f"Precio de lista orientativo {m.group(1)} € según las tiendas consultadas en octubre de 2026; los precios reales cambian a menudo, compruébalo en la tienda."))
    add(r"^Prezzo non ancora rilevato: verifica sul sito del negozio\.$", lambda m: "Price not yet recorded: check the shop's website." if en else "Precio aún no registrado: compruébalo en la web de la tienda.")
    add(r"^Dati raccolti da (.+)\. I campi \"non dichiarato\" non sono pubblicati dalle fonti consultate; li completeremo appena disponibili\.$",
        lambda m: (f"Data collected from {m.group(1)}. Fields marked \"not stated\" are not published by the sources consulted; we will fill them in as soon as they are available." if en
                   else f"Datos recogidos de {m.group(1)}. Los campos \"no declarado\" no los publican las fuentes consultadas; los completaremos en cuanto estén disponibles."))
    add(r"^(Caratteristiche dichiarate dal produttore e dai rivenditori\. |Caratteristiche e indice di potenza come pubblicati da (<a [^>]+>[^<]+</a>)\. )(Durezza e swingweight misurati da (<a [^>]+>[^<]+</a>)\. )?Valutazioni indipendenti in arrivo: il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$",
        lambda m: ((("Specifications as declared by the manufacturer and retailers. " if not m.group(2) else f"Specifications and power index as published by {m.group(2)}. ")
                    + (f"Hardness and swingweight measured by {m.group(4)}. " if m.group(4) else "")
                    + "Independent ratings coming soon: the PadelMetrix score will follow with our own rating method.") if en else
                   (("Características declaradas por el fabricante y las tiendas. " if not m.group(2) else f"Características e índice de potencia según {m.group(2)}. ")
                    + (f"Dureza y swingweight medidos por {m.group(4)}. " if m.group(4) else "")
                    + "Valoraciones independientes en camino: la puntuación PadelMetrix llegará con nuestro método de valoración.")))
    # sintesi generate (lotto)
    add(r"^Per Padelful ottiene ([\d,]+)/10\. In sintesi: (.+?) Il valore più alto è (.+?) \(([\d,]+)/10\), il più basso (.+?) \(([\d,]+)/10\)\. Le altre recensioni indipendenti sono ancora poche: aggiorneremo la scheda appena ne usciranno\.$",
        lambda m: (f"Padelful rates it {num(m.group(1), lang)}/10. In short: {lcfirst(t(ucfirst(m.group(2)), lang))} Its highest score is {_voce(m.group(3), lang)} ({num(m.group(4), lang)}/10), its lowest {_voce(m.group(5), lang)} ({num(m.group(6), lang)}/10). Other independent reviews are still scarce: we will update this page as they come out." if en
                   else f"Padelful le da {m.group(1)}/10. En resumen: {lcfirst(t(ucfirst(m.group(2)), lang))} Su valor más alto es {_voce(m.group(3), lang)} ({m.group(4)}/10) y el más bajo {_voce(m.group(5), lang)} ({m.group(6)}/10). Todavía hay pocas reseñas independientes: actualizaremos la ficha cuando salgan."))
    add(r"^Le recensioni indipendenti di questo modello sono ancora poche\. (.+?) la descrive così: (.+?) Aggiorneremo la sintesi appena saranno disponibili test e recensioni\.$",
        lambda m: (f"Independent reviews of this model are still scarce. {m.group(1)} describes it like this: {lcfirst(t(ucfirst(m.group(2)), lang))} We will update this summary as tests and reviews become available." if en
                   else f"Todavía hay pocas reseñas independientes de este modelo. {m.group(1)} la describe así: {lcfirst(t(ucfirst(m.group(2)), lang))} Actualizaremos el resumen cuando haya pruebas y reseñas."))
    # lead del lotto: descrizione + livello
    add(r"^(.+?) Indicata per (chi inizia|principianti e intermedi|giocatori intermedi|intermedi alti e avanzati|giocatori avanzati e agonisti|giocatori avanzati)\.$",
        lambda m: f"{t(m.group(1), lang)} " + (f"Suited to {pick(LIV_FRASE, m.group(2), lang)}." if en else f"Indicada para {pick(LIV_FRASE, m.group(2), lang)}."))
    add(r"^(.+?) Pensata per ragazzi\.$", lambda m: f"{t(m.group(1), lang)} " + ("Designed for kids." if en else "Pensada para niños."))
    # simili del lotto
    add(r"^La versione (\d{4}) dello stesso modello\.$", lambda m: (f"The {m.group(1)} version of the same model." if en else f"La versión {m.group(1)} del mismo modelo."))
    add(r"^Stessa racchetta\.$", lambda m: "Same racket." if en else "La misma pala.")
    add(r"^Stessa racchetta, cambia solo il colore(\.?)$", lambda m: "Same racket, only the colour changes." if en else "La misma pala, solo cambia el color.")
    add(r"^((Diamante|Rotonda|Goccia|Ibrida|Racchetta)( d'attacco| di controllo| polivalente)?)(, .+)?\.$", lambda m: simile_lotto(m, lang))
    # simili adidas
    add(r"^Differenze: (.+?)\. Listino (\d+) €\.$", lambda m: (("Differences: " if en else "Diferencias: ") + ", ".join(diff_item(x, lang) for x in m.group(1).split(", ")) + (f". List price €{m.group(2)}." if en else f". Precio de lista {m.group(2)} €.")))
    add(r"^Differenze: forma (diamante|rotonda|goccia)\. Listino (\d+) €\.$", lambda m: "")
    add(r"^Specifiche dichiarate uguali; per PadelZoom ha più (.+?) e meno (.+?)\. Listino (\d+) €\.$",
        lambda m: (f"Same declared specs; PadelZoom gives it more {_voce(m.group(1), lang)} and less {_voce(m.group(2), lang)}. List price €{m.group(3)}." if en
                   else f"Mismas especificaciones declaradas; según PadelZoom tiene más {_voce(m.group(1), lang)} y menos {_voce(m.group(2), lang)}. Precio de lista {m.group(3)} €."))
    add(r'^Dati dalla scheda di (<a [^>]+>PadelZoom</a>); livello consigliato stimato da PadelMetrix in base a materiali e tatto\.$',
        lambda m: (f"Data from the {m.group(1)} page; recommended level estimated by PadelMetrix from materials and feel." if en
                   else f"Datos de la ficha de {m.group(1)}; nivel recomendado estimado por PadelMetrix según materiales y tacto."))
    # adidas: sintesi a punteggi
    add(r"^PadelZoom le assegna ([\d,]+)/10 complessivo, ma senza un'analisi scritta: per ora ci sono solo i punteggi\.$",
        lambda m: (f"PadelZoom gives it {num(m.group(1), lang)}/10 overall, but without a written review: for now there are only the scores." if en
                   else f"PadelZoom le da {m.group(1)}/10 en total, pero sin un análisis escrito: por ahora solo hay puntuaciones."))
    add(r"^I valori più alti sono (.+?) \(([\d,]+)\) e (.+?) \(([\d,]+)\), il più basso è (.+?) \(([\d,]+)\)\.$",
        lambda m: (f"The highest scores are {_voce(m.group(1), lang)} ({num(m.group(2), lang)}) and {_voce(m.group(3), lang)} ({num(m.group(4), lang)}), the lowest is {_voce(m.group(5), lang)} ({num(m.group(6), lang)})." if en
                   else f"Los valores más altos son {_voce(m.group(1), lang)} ({m.group(2)}) y {_voce(m.group(3), lang)} ({m.group(4)}), el más bajo es {_voce(m.group(5), lang)} ({m.group(6)})."))
    add(r"^(Solo punteggi, senza analisi scritta|Con analisi scritta, riassunta sopra)\. Uscita di palla ([\d,]+), maneggevolezza ([\d,]+), sweet spot ([\d,]+)\.$",
        lambda m: ((("Scores only, no written review" if m.group(1).startswith("Solo") else "With a written review, summarised above") + f". Ball output {num(m.group(2), lang)}, maneuverability {num(m.group(3), lang)}, sweet spot {num(m.group(4), lang)}.") if en else
                   (("Solo puntuaciones, sin análisis escrito" if m.group(1).startswith("Solo") else "Con análisis escrito, resumido arriba") + f". Salida de bola {m.group(2)}, manejabilidad {m.group(3)}, punto dulce {m.group(4)}.")))
    add(r"^(.+) \(([\d,]+)/10 per PadelZoom\)$", lambda m: f"{t(m.group(1), lang)} ({num(m.group(2), lang)}/10 " + ("according to PadelZoom)" if en else "según PadelZoom)"))
    add(r"^(.+) \(([\d,]+)/10\)$", lambda m: f"{t(m.group(1), lang)} ({num(m.group(2), lang)}/10)")
    add(r"^Prezzo di listino alto \((\d+) €\)$", lambda m: (f"High list price (€{m.group(1)})" if en else f"Precio de lista alto ({m.group(1)} €)"))
    add(r"^Prezzo basso \(listino (\d+) €\)$", lambda m: (f"Low price (€{m.group(1)} list)" if en else f"Precio bajo (lista {m.group(1)} €)"))
    # pro/contro del lotto con variabili
    add(r"^Superficie in carbonio (\d+K)$", lambda m: (f"{m.group(1)} carbon face" if en else f"Cara de carbono {m.group(1)}"))
    add(r"^Il modello di (.+)$", lambda m: (f"{m.group(1)}'s model" if en else f"El modelo de {m.group(1)}"))
    add(r"^Collezione (\d{4}) di (.+)$", lambda m: (f"{m.group(2)} {m.group(1)} collection" if en else f"Colección {m.group(1)} de {m.group(2)}"))
    add(r"^Sei di livello (.+)$", lambda m: (f"You are at {pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)} level" if en else f"Tienes un nivel {pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)}"))
    add(r"^Cerchi un modello recente di (.+)$", lambda m: (f"You want a recent {m.group(1)} model" if en else f"Buscas un modelo reciente de {m.group(1)}"))
    # avvisi del lotto
    add(r'^<p>È uscita la versione (\d{4}): <a href="([^"]+)">(.+?)</a>\. Il modello (\d{4}) resta in vendita e spesso si trova scontato\.</p>$',
        lambda m: (f'<p>The {m.group(1)} version is out: <a href="{m.group(2)}">{m.group(3)}</a>. The {m.group(4)} model is still on sale and is often discounted.</p>' if en
                   else f'<p>Ya ha salido la versión {m.group(1)}: <a href="{m.group(2)}">{m.group(3)}</a>. El modelo {m.group(4)} sigue a la venta y a menudo con descuento.</p>'))
    add(r'^<p>Questa è la nuova versione\. Il <a href="([^"]+)">modello (\d{4})</a> resta in vendita e spesso si trova scontato\.</p>$',
        lambda m: (f'<p>This is the new version. The <a href="{m.group(1)}">{m.group(2)} model</a> is still on sale and is often discounted.</p>' if en
                   else f'<p>Esta es la nueva versión. El <a href="{m.group(1)}">modelo {m.group(2)}</a> sigue a la venta y a menudo con descuento.</p>'))
    add(r"^([A-Z][\w -]+) · (\d{4})$", lambda m: m.group(0))
    add(r"^Presso i rivenditori si trova già da circa ([\d,]+) €\.$",
        lambda m: (f"Retailers already sell it from about €{num(m.group(1), lang)}." if en else f"En las tiendas ya se encuentra desde unos {m.group(1)} €."))
    add(r"^Sito ufficiale · listino ([\d,]+) €$", lambda m: (f"Official website · list price €{num(m.group(1), lang)}" if en else f"Web oficial · precio de lista {m.group(1)} €"))
    add(r"^Sito ufficiale · prezzo consigliato ([\d,]+) €$", lambda m: (f"Official website · recommended price €{num(m.group(1), lang)}" if en else f"Web oficial · precio recomendado {m.group(1)} €"))
    add(r"^Sito ufficiale · ([\d,]+) € \(listino ([\d,]+) €\)$", lambda m: (f"Official website · €{num(m.group(1), lang)} (list price €{num(m.group(2), lang)})" if en else f"Web oficial · {m.group(1)} € (precio de lista {m.group(2)} €)"))
    add(r'^Punteggi su 10 di (<a [^>]+>PadelZoom</a>), voto complessivo ([\d,]+)/10\. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$',
        lambda m: (f"Scores out of 10 from {m.group(1)}, overall rating {num(m.group(2), lang)}/10. The PadelMetrix score will follow with our own rating method." if en
                   else f"Puntuaciones sobre 10 de {m.group(1)}, nota global {m.group(2)}/10. La puntuación PadelMetrix llegará con nuestro método de valoración."))
    add(r"^Racchetta (a diamante pensata per attaccare|a goccia polivalente|rotonda pensata per il controllo e la regolarità), della linea (.+?): (.+)\.$",
        lambda m: ({"a diamante pensata per attaccare": ("Diamond racket built for attack", "Pala diamante pensada para atacar"),
                    "a goccia polivalente": ("All-round teardrop racket", "Pala lágrima polivalente"),
                    "rotonda pensata per il controllo e la regolarità": ("Round racket built for control and consistency", "Pala redonda pensada para el control y la regularidad")}[m.group(1)][0 if en else 1]
                   + (f", from the {m.group(2)} line: " if en else f", de la línea {m.group(2)}: ") + t(m.group(3), lang) + "."))
    add(r"^Materiali di fascia alta \((.+)\) per giocatori esperti(\.?)$",
        lambda m: (f"High-end materials ({t(m.group(1), lang)}) for experienced players{m.group(2)}" if en else f"Materiales de gama alta ({t(m.group(1), lang)}) para jugadores expertos{m.group(2)}"))
    add(r"^È la stessa racchetta della (.+): cambia solo il colore(\.?)$",
        lambda m: (f"It is the same racket as the {m.group(1)}: only the colour changes{m.group(2)}" if en else f"Es la misma pala que la {m.group(1)}: solo cambia el color{m.group(2)}"))
    add(r"^Superficie in (carbonio .+?) e telaio in carbonio, per giocatori che hanno già una buona base tecnica(\.?)$",
        lambda m: (f"{ucfirst(t(m.group(1), lang))} face and carbon frame, for players who already have a good technical base{m.group(2)}" if en else f"Cara de {t(m.group(1), lang)} y marco de carbono, para jugadores que ya tienen una buena base técnica{m.group(2)}"))
    add(r"^(Potenza|Tolleranza) ([\d,]+)/(10|5)$", lambda m: f"{_voce(m.group(1), lang)} {num(m.group(2), lang)}/{m.group(3)}")
    add(r"^community ([\d,]+)/10 \((\d+) recensioni\)$", lambda m: (f"community {num(m.group(1), lang)}/10 ({m.group(2)} reviews)" if en else f"comunidad {m.group(1)}/10 ({m.group(2)} reseñas)"))
    add(r"^Media \((\d+)/100 per (.+)\)$", lambda m: (f"Medium ({m.group(1)}/100 according to {m.group(2)})" if en else f"Media ({m.group(1)}/100 según {m.group(2)})"))
    return H


_HC = {}


def _handlers(lang):
    if lang not in _HC:
        _HC[lang] = handlers(lang)
    return _HC[lang]


def ucfirst(s):
    return s[:1].upper() + s[1:]


def lcfirst(s):
    w = s.split(" ")[0]
    if w.isupper() or (len(w) > 1 and w[1:].lower() != w[1:]):
        return s
    return s[:1].lower() + s[1:]


def simile_lotto(m, lang):
    en = lang == "en"
    testa = m.group(2)
    st = m.group(3) or ""
    forma = None if testa == "Racchetta" else _forma_w(testa, lang)
    stile = {" d'attacco": ("attacking", "de ataque"), " di controllo": ("control", "de control"), " polivalente": ("all-round", "polivalente")}.get(st)
    if en:
        head = " ".join(x for x in ((stile[0] if stile else None), (forma or "racket")) if x)
        head = head[0].upper() + head[1:]
        if forma:
            head += " racket" if not stile else " racket"
    else:
        head = ("Pala " + (forma or "")).strip() + ((" " + stile[1]) if stile else "")
    parti = [head]
    for x in (m.group(4) or "").split(", ")[1:]:
        parti.append(diff_item(x, lang))
    return ", ".join(parti) + "."


def diff_item(x, lang):
    en = lang == "en"
    x = x.strip()
    r = re.match(r"^(\d+[–-]\d+ g|\d+ g)$", x)
    if r:
        return x
    r = re.match(r"^carbonio (\d+K)$", x)
    if r:
        return f"{r.group(1)} carbon" if en else f"carbono {r.group(1)}"
    if x == "fibra di vetro":
        return "fiberglass" if en else "fibra de vidrio"
    r = re.match(r"^livello (.+)$", x)
    if r:
        lv = pick(LIV_LOWER, r.group(1), lang) or t(r.group(1), lang)
        return f"{lv} level" if en else f"nivel {lv}"
    if x == "listino più alto":
        return "higher list price" if en else "precio de lista más alto"
    if x == "listino più basso":
        return "lower list price" if en else "precio de lista más bajo"
    r = re.match(r"^forma (.+)$", x)
    if r:
        return (f"{_forma_w(r.group(1), lang)} shape" if en else f"forma {_forma_w(r.group(1), lang)}")
    r = re.match(r"^superficie in (.+)$", x)
    if r:
        return (f"{t(r.group(1), lang)} face" if en else f"cara de {t(r.group(1), lang)}")
    r = re.match(r"^gomma (.+)$", x)
    if r:
        return (f"{r.group(1)} rubber" if en else f"goma {r.group(1)}")
    r = re.match(r"^tatto (.+)$", x)
    if r:
        return (f"{pick(TATTI, r.group(1), lang) or t(r.group(1), lang)} feel" if en else f"tacto {pick(TATTI, r.group(1), lang) or t(r.group(1), lang)}")
    r = re.match(r"^linea (.+)$", x)
    if r:
        return (f"{r.group(1)} line" if en else f"línea {r.group(1)}")
    return t(x, lang)


TERMINI = [
    (r"\bCarbonio alluminizzato (\d+K)\b", ("Aluminized \\1 carbon", "Carbono aluminizado \\1")),
    (r"\bCarbonio (\d+K) alluminizzato\b", ("Aluminized \\1 carbon", "Carbono \\1 aluminizado")),
    (r"\bfibra di vetro\b", ("fiberglass", "fibra de vidrio")), (r"\bFibra di vetro\b", ("Fiberglass", "Fibra de vidrio")),
    (r"\bCarbonio\b", ("Carbon", "Carbono")), (r"\bcarbonio\b", ("carbon", "carbono")),
    (r"\btexture 3D\b", ("3D texture", "textura 3D")), (r"\bfinitura sabbiata\b", ("sandy finish", "acabado arenoso")),
    (r"\bfinitura\b", ("finish", "acabado")), (r"\bruvido sabbiato\b", ("rough sandy finish", "rugoso arenoso")),
    (r"\bopaco\b", ("matte", "mate")), (r"\ba trama aperta\b", ("open weave", "de trama abierta")),
    (r"\bunidirezionale\b", ("unidirectional", "unidireccional")), (r"\bbidirezionale\b", ("bidirectional", "bidireccional")),
    (r"\bdi fascia alta\b", ("high-end", "de gama alta")), (r"\besagonale\b", ("hexagonal", "hexagonal")),
    (r"\bflessibile\b", ("flexible", "flexible")), (r"\bibrido\b", ("hybrid", "híbrido")), (r"\bmisto\b", ("mixed", "mixto")),
    (r"\bmorbid[oa]\b", ("soft", "blando")), (r"\brinforzat[oa]\b", ("reinforced", "reforzado")), (r"\btubolare\b", ("tubular", "tubular")),
    (r"\bdoppio tubo\b", ("double tube", "doble tubo")), (r"\bDoppio tubolare\b", ("Double tubular", "Doble tubular")),
    (r"\bdoppio tubolare\b", ("double tubular", "doble tubular")), (r"\bbiossido di titanio\b", ("titanium dioxide", "dióxido de titanio")),
    (r"\bdurezza intermedia\b", ("medium hardness", "dureza intermedia")), (r"\brisposta più morbida\b", ("softer response", "respuesta más blanda")),
    (r"\balta densità\b", ("high density", "alta densidad")), (r"\bdoppia densità\b", ("dual density", "doble densidad")),
    (r"\btre strati\b", ("three layers", "tres capas")), (r"\bdurezza media\b", ("medium hardness", "dureza media")),
    (r"\bgomma\b", ("rubber", "goma")), (r"\bGomma\b", ("Rubber", "Goma")), (r"\bliscia\b", ("smooth", "lisa")), (r"\bruvida\b", ("rough", "rugosa")),
    (r"\bdura\b", ("hard", "dura")), (r"\bmedia\b", ("medium", "media")), (r"\bmonoblocco\b", ("single-piece", "monobloque")),
    (r"\bmanico allungato\b", ("extended handle", "mango alargado")), (r"\bponte\b", ("bridge", "puente")),
    (r"\btunnel\b", ("tunnels", "túneles")), (r"\bcirca\b", ("about", "aprox.")), (r"\bsilver\b", ("silver", "plata")),
    (r"\bcon\b", ("with", "con")), (r"\be\b", ("and", "y")), (r"\bin\b", ("in", "en")),
]
MARKER = {"en": {"di", "della", "delle", "del", "dei", "per", "più", "che", "il", "la", "le", "gli", "è", "una", "un", "alla", "al", "dalla", "molto", "senza", "sono", "ma", "non", "da", "con", "e", "lo", "nel", "nella", "sul", "anche"},
          "es": {"di", "della", "delle", "dei", "per", "più", "che", "il", "gli", "è", "alla", "dalla", "molto", "senza", "sono", "ma", "non", "da", "e", "lo", "nel", "nella", "sul", "anche"}}
ITA_PAROLE = re.compile(r"\b(per|più|della|delle|dalla|molto|senza|gioco|giocatori|racchetta|leggera|morbid|potenza|controllo|versione|basso|bassa|chi|vuole|cerca)\b", re.I)


def termini(s, lang):
    i = 0 if lang == "en" else 1
    out = s
    for pat, rep in TERMINI:
        out = re.sub(pat, rep[i], out)
    toks = re.findall(r"[a-zàèéìòùáíóúñü]+", out.lower())
    if any(tk in MARKER[lang] for tk in toks) or ITA_PAROLE.search(out):
        return None
    return out


def t(text, lang):
    """Traduce un testo italiano. Ordine: memoria di traduzione, modelli, frasi una per una."""
    if text is None or text == "" or lang == "it" or not isinstance(text, str):
        return text
    s = text.strip()
    mem = tm(lang)
    if s in mem:
        return mem[s]
    if s + "." in mem:
        return mem[s + "."].rstrip(".")
    for pat, fn in _handlers(lang):
        m = pat.match(s)
        if m:
            out = fn(m)
            if out:
                return out
    for k, tab in ((s, LIVELLI), (s, STILI), (s, STILE_CHIP), (s, TATTI), (s, LABELS)):
        v = pick(tab, k, lang)
        if v:
            return v
    v = pick(BIL, s, lang) or pick(LIV_LOWER, s, lang)
    if v:
        return v
    if len(s) < 90 and "." not in s.rstrip(".") and re.search(r"(Carbonio|carbonio|vetro|EVA|Foam|tubolare|gomma|Gomma|finitura)", s):
        v = termini(s, lang)
        if v:
            return num(v, lang)
    # frasi multiple: traduci una per una
    parti = re.split(r"(?<=[.!?])\s+(?=[A-ZÈÀ«\"])", s)
    if len(parti) > 1 and "<" not in s:
        return " ".join(t(p, lang) for p in parti)
    MANCANTI[lang].add(s)
    return s
