"""Traduzione IT -> EN/ES dei testi delle schede: memoria di traduzione + modelli per le frasi generate."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
TMDIR = ROOT / "data" / "traduzioni"
LANGS = ("en", "es", "fr")
MANCANTI = {"en": set(), "es": set(), "fr": set()}

_TM = {}


def tm(lang):
    if lang not in _TM:
        _TM[lang] = {}
        if lang == "fr":
            for f in sorted(TMDIR.glob("tm_fr_*.json")):
                _TM[lang].update(json.loads(f.read_text(encoding="utf-8")))
            return _TM[lang]
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

VOCI = {"potenza": ("power", "potencia", "puissance"), "controllo": ("control", "control", "contrôle"), "uscita di palla": ("ball output", "salida de bola", "sortie de balle"),
        "maneggevolezza": ("maneuverability", "manejabilidad", "maniabilité"), "sweet spot": ("sweet spot", "punto dulce", "sweet spot"),
        "stabilità": ("stability", "estabilidad", "stabilité"), "rigidità": ("stiffness", "rigidez", "rigidité"), "effetto": ("spin", "efecto", "effet"),
        "comfort": ("comfort", "confort", "confort"), "giocabilità": ("playability", "jugabilidad", "jouabilité"), "rebote": ("rebound", "rebote", "rebond"),
        "difesa": ("defence", "defensa", "défense"), "precisione": ("precision", "precisión", "précision"), "tolleranza": ("forgiveness", "tolerancia", "tolérance")}
FORME = {"diamante": ("diamond", "diamante", "diamant"), "rotonda": ("round", "redonda", "ronde"), "goccia": ("teardrop", "lágrima", "goutte d'eau"), "ibrida": ("hybrid", "híbrida", "hybride"),
         "geometrica": ("geometric", "geométrica", "géométrique")}
LIVELLI = {"Principiante": ("Beginner", "Principiante", "Débutant"), "Principiante / intermedio": ("Beginner / intermediate", "Principiante / intermedio", "Débutant / intermédiaire"),
           "Intermedio": ("Intermediate", "Intermedio", "Intermédiaire"), "Intermedio / avanzato": ("Intermediate / advanced", "Intermedio / avanzado", "Intermédiaire / confirmé"),
           "Avanzato": ("Advanced", "Avanzado", "Confirmé"), "Avanzato / professionale": ("Advanced / professional", "Avanzado / profesional", "Confirmé / expert"),
           "Intermedio alto / avanzato": ("Upper intermediate / advanced", "Intermedio alto / avanzado", "Intermédiaire avancé / confirmé"),
           "Avanzato / professionale ": ("Advanced / professional", "Avanzado / profesional", "Confirmé / expert")}
STILI = {"Offensivo": ("Attacking", "Ofensivo", "Offensif"), "Controllo": ("Control", "Control", "Contrôle"), "Polivalente": ("All-round", "Polivalente", "Polyvalent"),
         "Attacco": ("Attack", "Ataque", "Attaque")}
STILE_CHIP = {"Racchetta d'attacco": ("Attacking racket", "Pala de ataque", "Raquette d'attaque"), "Racchetta di controllo": ("Control racket", "Pala de control", "Raquette de contrôle"),
              "Polivalente": ("All-round", "Polivalente", "Polyvalente")}
TATTI = {"morbido": ("soft", "blando", "souple"), "medio-morbido": ("medium-soft", "medio-blando", "mi-souple"), "medio": ("medium", "medio", "moyen"),
         "medio-duro": ("medium-hard", "medio-duro", "mi-dur"), "duro": ("hard", "duro", "dur"), "secco": ("crisp", "seco", "sec"), "fermo": ("firm", "firme", "ferme"),
         "medio-secco": ("medium-crisp", "medio-seco", "mi-sec"), "secco e fermo": ("crisp and firm", "seco y firme", "sec et ferme"), "ruvida": ("rough", "rugoso", "rugueux"),
         "molto morbido": ("very soft", "muy blando", "très souple"), "Dura": ("Hard", "Dura", "Dur"), "Medio": ("Medium", "Medio", "Moyen"), "Medio-duro": ("Medium-hard", "Medio-duro", "Mi-dur"),
         "Medio-morbido": ("Medium-soft", "Medio-blando", "Mi-souple"), "Morbido": ("Soft", "Blando", "Souple"), "Duro": ("Hard", "Duro", "Dur")}
BIL = {"alto": ("high", "alto", "haut"), "medio": ("medium", "medio", "moyen"), "basso": ("low", "bajo", "bas"), "medio-alto": ("medium-high", "medio-alto", "moyen-haut"),
       "medio-basso": ("medium-low", "medio-bajo", "moyen-bas"), "neutro": ("neutral", "neutro", "neutre"), "contenuto": ("moderate", "contenido", "modéré")}
LIV_FRASE = {"chi inizia": ("beginners", "quien empieza", "les débutants"), "principianti e intermedi": ("beginners and intermediates", "principiantes e intermedios", "les débutants et intermédiaires"),
             "giocatori intermedi": ("intermediate players", "jugadores intermedios", "les joueurs intermédiaires"), "intermedi alti e avanzati": ("upper intermediate and advanced players", "intermedios altos y avanzados", "les joueurs intermédiaires avancés et confirmés"),
             "giocatori avanzati": ("advanced players", "jugadores avanzados", "les joueurs confirmés"), "giocatori avanzati e agonisti": ("advanced and competitive players", "jugadores avanzados y de competición", "les joueurs confirmés et compétiteurs")}
LIV_LOWER = {"principiante": ("beginner", "principiante", "débutant"), "principiante / intermedio": ("beginner / intermediate", "principiante / intermedio", "débutant / intermédiaire"),
             "intermedio": ("intermediate", "intermedio", "intermédiaire"), "intermedio / avanzato": ("intermediate / advanced", "intermedio / avanzado", "intermédiaire / confirmé"),
             "avanzato": ("advanced", "avanzado", "confirmé"), "avanzato / professionale": ("advanced / professional", "avanzado / profesional", "confirmé / expert")}
LABELS = {"Marca": ("Brand", "Marca", "Marque"), "Modello": ("Model", "Modelo", "Modèle"), "Collezione": ("Collection", "Colección", "Collection"), "Anno": ("Year", "Año", "Année"),
          "Linea": ("Line", "Línea", "Gamme"), "Giocatore": ("Player", "Jugador", "Joueur"), "Categoria": ("Category", "Categoría", "Catégorie"), "Forma": ("Shape", "Forma", "Forme"),
          "Peso": ("Weight", "Peso", "Poids"), "Bilanciamento": ("Balance", "Balance", "Équilibre"), "Nucleo": ("Core", "Núcleo", "Noyau"), "Gomma": ("Core rubber", "Goma", "Gomme"),
          "Superficie": ("Face", "Cara", "Surface"), "Telaio": ("Frame", "Marco", "Cadre"), "Spessore": ("Thickness", "Grosor", "Épaisseur"), "Finitura": ("Finish", "Acabado", "Finition"),
          "Rigidità": ("Stiffness", "Rigidez", "Rigidité"), "Tatto": ("Feel", "Tacto", "Toucher"), "Sensazione": ("Feel", "Tacto", "Toucher"), "Livello": ("Level", "Nivel", "Niveau"),
          "Livello consigliato": ("Recommended level", "Nivel recomendado", "Niveau conseillé"), "Stile di gioco": ("Playing style", "Estilo de juego", "Style de jeu"),
          "Personalizzazione": ("Customization", "Personalización", "Personnalisation"), "Superficie di gioco": ("Hitting surface", "Superficie de juego", "Surface de frappe"),
          "Foratura": ("Hole pattern", "Taladrado", "Perçage"), "Tecnologie di linea": ("Line technologies", "Tecnologías de la línea", "Technologies de la gamme"),
          "Edizioni": ("Editions", "Ediciones", "Éditions"), "Durezza misurata": ("Measured hardness", "Dureza medida", "Dureté mesurée"),
          "Swingweight misurato": ("Measured swingweight", "Swingweight medido", "Swingweight mesuré"), "Colori": ("Colours", "Colores", "Couleurs"),
          "Prezzo di listino": ("List price", "Precio de lista", "Prix public")}


IDX = {"en": 0, "es": 1, "fr": 2}


def pick(d, k, lang):
    v = d.get(k)
    return v[IDX[lang]] if v else None


# ---------------------------------------------------------------- modelli per le frasi generate

def _forma_w(w, lang):
    return pick(FORME, w.lower(), lang) or w


def _voce(w, lang):
    return pick(VOCI, w.lower(), lang) or w


def handlers(lang):
    en = lang == "en"

    def X(a, b, c):
        return a if lang == "en" else (b if lang == "es" else c)
    H = []

    def add(pat, fn):
        H.append((re.compile(pat), fn))

    # numeri, pesi, prezzi puri
    add(r"^[\d\s–\-,\.±()+g€/]+$", lambda m: num(m.group(0), lang))
    add(r"^(\d+[–-]\d+ g) \(\+ fino a ([\d,]+) g\)$", lambda m: X(f"{m.group(1)} (+ up to {num(m.group(2), lang)} g)", f"{m.group(1)} (+ hasta {m.group(2)} g)", f"{m.group(1)} (+ jusqu'à {m.group(2)} g)"))
    add(r"^circa (\d+ g)$", lambda m: X("about ", "unos ", "environ ") + m.group(1))
    add(r"^(\d+ g) \(±(\d+)\)$", lambda m: f"{m.group(1)} (±{m.group(2)})")
    add(r"^Non dichiarat[oa]$", lambda m: X("Not stated", "No declarado", "Non déclaré"))
    add(r"^Junior$", lambda m: "Junior")
    add(r"^Modello femminile$", lambda m: X("Women's model", "Modelo femenino", "Modèle femme"))
    add(r"^Racchetta di ([A-ZÁÉÍÓÚ][^,.;:]*)$", lambda m: X(f"{m.group(1)}'s racket", f"Pala de {m.group(1)}", ("Raquette d'" if m.group(1)[0] in "AEIOUYÁÉÍÓÚH" else "Raquette de ") + m.group(1)))
    add(r"^Carbonio (\d+K)$", lambda m: X(f"{m.group(1)} carbon", f"Carbono {m.group(1)}", f"Carbone {m.group(1)}"))
    add(r"^Fibra di vetro$", lambda m: X("Fiberglass", "Fibra de vidrio", "Fibre de verre"))
    add(r"^Bilanciamento (.+)$", lambda m: X(f"{(pick(BIL, m.group(1), lang) or t(m.group(1), lang)).capitalize()} balance", f"Balance {pick(BIL, m.group(1), lang) or t(m.group(1), lang)}", f"Équilibre {pick(BIL, m.group(1), lang) or t(m.group(1), lang)}"))
    add(r"^(Diamante|Rotonda|Goccia|Ibrida)$", lambda m: ucfirst(_forma_w(m.group(1), lang)))
    add(r"^(Diamante|Rotonda|Goccia|Ibrida) \((.+)\)$", lambda m: f"{ucfirst(_forma_w(m.group(1), lang))} ({t(m.group(2), lang)})")
    add(r"^Forma (.+)$", lambda m: X(f"{t(m.group(1), lang).capitalize()} shape", f"Forma {t(m.group(1), lang)}", f"Forme {t(m.group(1), lang)}"))
    add(r"^(diamante|rotonda|goccia|ibrida|geometrica)$", lambda m: _forma_w(m.group(1), lang))
    add(r"^(goccia|rotonda|diamante) / (ibrida|goccia)$", lambda m: f"{_forma_w(m.group(1), lang)} / {_forma_w(m.group(2), lang)}")
    add(r"^(ibrida) tendente alla rotonda$", lambda m: X("hybrid leaning round", "híbrida tirando a redonda", "hybride tirant vers la ronde"))
    add(r"^(Alto|Medio|Basso|Medio-alto|Medio-basso|Neutro|Contenuto)( \((.+)\))?$",
        lambda m: (ucfirst(pick(BIL, m.group(1).lower(), lang)) + (f" ({num(m.group(3), lang).replace('circa ', X('about ', 'aprox. ', 'env. '))})" if m.group(3) else "")))
    add(r"^(alto|medio|basso|medio-alto|medio-basso|neutro|contenuto) \((.+)\)$",
        lambda m: pick(BIL, m.group(1), lang) + f" ({num(m.group(2), lang).replace('circa ', X('about ', 'aprox. ', 'env. '))})")
    add(r"^Livello (.+)$", lambda m: X((pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)).capitalize() + " level", "Nivel " + (pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)), "Niveau " + (pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang))))
    add(r"^Tatto (.+)$", lambda m: X((pick(TATTI, m.group(1), lang) or t(m.group(1), lang)).capitalize() + " feel", "Tacto " + (pick(TATTI, m.group(1), lang) or t(m.group(1), lang)), "Toucher " + (pick(TATTI, m.group(1), lang) or t(m.group(1), lang))))
    add(r"^Durezza misurata (\d+)$", lambda m: X(f"Measured hardness {m.group(1)}", f"Dureza medida {m.group(1)}", f"Dureté mesurée {m.group(1)}"))
    add(r"^Potenza ([\d,]+)/10 secondo (.+)$", lambda m: X(f"Power {num(m.group(1), lang)}/10 according to {m.group(2)}", f"Potencia {m.group(1)}/10 según {m.group(2)}", f"Puissance {m.group(1)}/10 selon {m.group(2)}"))
    add(r"^(.+) · Collezione (\d{4})( · Junior| · Donna)?$",
        lambda m: X(f"{m.group(1)} · {m.group(2)} collection" + {" · Junior": " · Junior", " · Donna": " · Women"}.get(m.group(3) or "", ""),
                    f"{m.group(1)} · Colección {m.group(2)}" + {" · Junior": " · Junior", " · Donna": " · Mujer"}.get(m.group(3) or "", ""),
                    f"{m.group(1)} · Collection {m.group(2)}" + {" · Junior": " · Junior", " · Donna": " · Femme"}.get(m.group(3) or "", "")))
    add(r"^(.+) · Collezione (\d{4}) · (.+)$", lambda m: X(f"{m.group(1)} · {m.group(2)} collection · {t(m.group(3), lang)}", f"{m.group(1)} · Colección {m.group(2)} · {t(m.group(3), lang)}", f"{m.group(1)} · Collection {m.group(2)} · {t(m.group(3), lang)}"))
    add(r"^([\d,]+)/10$", lambda m: num(m.group(0), lang))
    add(r"^([\d,]+)/10 \(community ([\d,]+)/10, (\d+) recensioni\)$", lambda m: X(f"{num(m.group(1), lang)}/10 (community {num(m.group(2), lang)}/10, {m.group(3)} reviews)", f"{m.group(1)}/10 (comunidad {m.group(2)}/10, {m.group(3)} reseñas)", f"{m.group(1)}/10 (communauté {m.group(2)}/10, {m.group(3)} avis)"))
    add(r"^potenza ([\d,]+) · controllo ([\d,]+)$", lambda m: X(f"power {num(m.group(1), lang)} · control {num(m.group(2), lang)}", f"potencia {m.group(1)} · control {m.group(2)}", f"puissance {m.group(1)} · contrôle {m.group(2)}"))
    add(r"^(.+?) ([\d,]+) · (.+?) ([\d,]+)$", lambda m: f"{_voce(m.group(1), lang)} {num(m.group(2), lang)} · {_voce(m.group(3), lang)} {num(m.group(4), lang)}")
    # valutazioni e note generate
    add(r"^Valutazioni di (.+)$", lambda m: X(f"{m.group(1)} ratings", f"Valoraciones de {m.group(1)}", f"Notes de {m.group(1)}"))
    add(r"^Valutazioni del produttore$", lambda m: X("Manufacturer ratings", "Valoraciones del fabricante", "Notes du fabricant"))
    add(r"^Valutazioni (PadelZoom|Padelful)$", lambda m: X(f"{m.group(1)} ratings", f"Valoraciones de {m.group(1)}", f"Notes de {m.group(1)}"))
    add(r"^Punteggi su 10 pubblicati da (<a [^>]+>[^<]+</a>), voto complessivo ([\d,]+)/10\. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$",
        lambda m: X(f"Scores out of 10 published by {m.group(1)}, overall score {num(m.group(2), lang)}/10. The PadelMetrix score will follow with our own rating method.",
                    f"Puntuaciones sobre 10 publicadas por {m.group(1)}, nota global {m.group(2)}/10. La puntuación PadelMetrix llegará con nuestro método de valoración.",
                    f"Notes sur 10 publiées par {m.group(1)}, note globale {m.group(2)}/10. La note PadelMetrix arrivera avec notre propre méthode d'évaluation."))
    add(r"^In sintesi$", lambda m: X("At a glance", "En resumen", "En bref"))
    add(r"^Spedizione e resi Amazon$", lambda m: X("Amazon shipping and returns", "Envío y devoluciones de Amazon", "Livraison et retours Amazon"))
    add(r"^Scheda prodotto del rivenditore$", lambda m: X("Retailer product page", "Ficha de producto del vendedor", "Fiche produit du revendeur"))
    add(r"^Vedi su Amazon$", lambda m: X("View on Amazon", "Ver en Amazon", "Voir sur Amazon"))
    add(r"^Vedi sul sito$", lambda m: X("View on site", "Ver en la web", "Voir sur le site"))
    add(r"^Prezzo di listino indicativo ([\d\.,]+) € secondo i rivenditori consultati a ottobre 2026; i prezzi reali cambiano spesso, verifica sul negozio\.$",
        lambda m: X(f"Indicative list price €{num(m.group(1), lang)} according to retailers checked in October 2026; actual prices change often, check the shop.",
                    f"Precio de lista orientativo {m.group(1)} € según las tiendas consultadas en octubre de 2026; los precios reales cambian a menudo, compruébalo en la tienda.",
                    f"Prix public indicatif {m.group(1)} € selon les revendeurs consultés en octobre 2026 ; les prix réels changent souvent, vérifiez sur la boutique."))
    add(r"^Prezzo non ancora rilevato: verifica sul sito del negozio\.$", lambda m: X("Price not yet recorded: check the shop's website.", "Precio aún no registrado: compruébalo en la web de la tienda.", "Prix pas encore relevé : vérifiez sur le site de la boutique."))
    add(r"^Dati raccolti da (.+)\. I campi \"non dichiarato\" non sono pubblicati dalle fonti consultate; li completeremo appena disponibili\.$",
        lambda m: X(f"Data collected from {m.group(1)}. Fields marked \"not stated\" are not published by the sources consulted; we will fill them in as soon as they are available.",
                    f"Datos recogidos de {m.group(1)}. Los campos \"no declarado\" no los publican las fuentes consultadas; los completaremos en cuanto estén disponibles.",
                    f"Données recueillies auprès de {m.group(1)}. Les champs « non déclaré » ne sont pas publiés par les sources consultées ; nous les compléterons dès qu'ils seront disponibles."))
    add(r"^(Caratteristiche dichiarate dal produttore e dai rivenditori\. |Caratteristiche e indice di potenza come pubblicati da (<a [^>]+>[^<]+</a>)\. )(Durezza e swingweight misurati da (<a [^>]+>[^<]+</a>)\. )?Valutazioni indipendenti in arrivo: il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$",
        lambda m: X((("Specifications as declared by the manufacturer and retailers. " if not m.group(2) else f"Specifications and power index as published by {m.group(2)}. ")
                     + (f"Hardness and swingweight measured by {m.group(4)}. " if m.group(4) else "")
                     + "Independent ratings coming soon: the PadelMetrix score will follow with our own rating method."),
                    (("Características declaradas por el fabricante y las tiendas. " if not m.group(2) else f"Características e índice de potencia según {m.group(2)}. ")
                     + (f"Dureza y swingweight medidos por {m.group(4)}. " if m.group(4) else "")
                     + "Valoraciones independientes en camino: la puntuación PadelMetrix llegará con nuestro método de valoración."),
                    (("Caractéristiques déclarées par le fabricant et les revendeurs. " if not m.group(2) else f"Caractéristiques et indice de puissance publiés par {m.group(2)}. ")
                     + (f"Dureté et swingweight mesurés par {m.group(4)}. " if m.group(4) else "")
                     + "Évaluations indépendantes à venir : la note PadelMetrix arrivera avec notre propre méthode d'évaluation.")))
    # sintesi generate (lotto)
    add(r"^Per Padelful ottiene ([\d,]+)/10\. In sintesi: (.+?) Il valore più alto è (.+?) \(([\d,]+)/10\), il più basso (.+?) \(([\d,]+)/10\)\. Le altre recensioni indipendenti sono ancora poche: aggiorneremo la scheda appena ne usciranno\.$",
        lambda m: X(f"Padelful rates it {num(m.group(1), lang)}/10. In short: {lcfirst(t(ucfirst(m.group(2)), lang))} Its highest score is {_voce(m.group(3), lang)} ({num(m.group(4), lang)}/10), its lowest {_voce(m.group(5), lang)} ({num(m.group(6), lang)}/10). Other independent reviews are still scarce: we will update this page as they come out.",
                    f"Padelful le da {m.group(1)}/10. En resumen: {lcfirst(t(ucfirst(m.group(2)), lang))} Su valor más alto es {_voce(m.group(3), lang)} ({m.group(4)}/10) y el más bajo {_voce(m.group(5), lang)} ({m.group(6)}/10). Todavía hay pocas reseñas independientes: actualizaremos la ficha cuando salgan.",
                    f"Padelful lui donne {m.group(1)}/10. En bref : {lcfirst(t(ucfirst(m.group(2)), lang))} Sa meilleure note concerne la {_voce(m.group(3), lang)} ({m.group(4)}/10), la plus basse la {_voce(m.group(5), lang)} ({m.group(6)}/10). Les autres tests indépendants sont encore rares : nous mettrons la fiche à jour dès leur parution."))
    add(r"^Le recensioni indipendenti di questo modello sono ancora poche\. (.+?) la descrive così: (.+?) Aggiorneremo la sintesi appena saranno disponibili test e recensioni\.$",
        lambda m: X(f"Independent reviews of this model are still scarce. {m.group(1)} describes it like this: {lcfirst(t(ucfirst(m.group(2)), lang))} We will update this summary as tests and reviews become available.",
                    f"Todavía hay pocas reseñas independientes de este modelo. {m.group(1)} la describe así: {lcfirst(t(ucfirst(m.group(2)), lang))} Actualizaremos el resumen cuando haya pruebas y reseñas.",
                    f"Les tests indépendants de ce modèle sont encore rares. {m.group(1)} la décrit ainsi : {lcfirst(t(ucfirst(m.group(2)), lang))} Nous mettrons cette synthèse à jour dès que des tests et avis seront disponibles."))
    # lead del lotto: descrizione + livello
    add(r"^(.+?) Indicata per (chi inizia|principianti e intermedi|giocatori intermedi|intermedi alti e avanzati|giocatori avanzati e agonisti|giocatori avanzati)\.$",
        lambda m: f"{t(m.group(1), lang)} " + X(f"Suited to {pick(LIV_FRASE, m.group(2), lang)}.", f"Indicada para {pick(LIV_FRASE, m.group(2), lang)}.", f"Conseillée pour {pick(LIV_FRASE, m.group(2), lang)}."))
    add(r"^(.+?) Pensata per ragazzi\.$", lambda m: f"{t(m.group(1), lang)} " + X("Designed for kids.", "Pensada para niños.", "Pensée pour les enfants."))
    # simili del lotto
    add(r"^La versione (\d{4}) dello stesso modello\.$", lambda m: X(f"The {m.group(1)} version of the same model.", f"La versión {m.group(1)} del mismo modelo.", f"La version {m.group(1)} du même modèle."))
    add(r"^Stessa racchetta\.$", lambda m: X("Same racket.", "La misma pala.", "Même raquette."))
    add(r"^Stessa racchetta, cambia solo il colore(\.?)$", lambda m: X("Same racket, only the colour changes.", "La misma pala, solo cambia el color.", "Même raquette, seule la couleur change."))
    add(r"^((Diamante|Rotonda|Goccia|Ibrida|Racchetta)( d'attacco| di controllo| polivalente)?)(, .+)?\.$", lambda m: simile_lotto(m, lang))
    # simili adidas
    add(r"^Differenze: (.+?)\. Listino (\d+) €\.$", lambda m: (X("Differences: ", "Diferencias: ", "Différences : ") + ", ".join(diff_item(x, lang) for x in m.group(1).split(", ")) + X(f". List price €{m.group(2)}.", f". Precio de lista {m.group(2)} €.", f". Prix public {m.group(2)} €.")))
    add(r"^Differenze: forma (diamante|rotonda|goccia)\. Listino (\d+) €\.$", lambda m: "")
    add(r"^Specifiche dichiarate uguali; per PadelZoom ha più (.+?) e meno (.+?)\. Listino (\d+) €\.$",
        lambda m: X(f"Same declared specs; PadelZoom gives it more {_voce(m.group(1), lang)} and less {_voce(m.group(2), lang)}. List price €{m.group(3)}.",
                    f"Mismas especificaciones declaradas; según PadelZoom tiene más {_voce(m.group(1), lang)} y menos {_voce(m.group(2), lang)}. Precio de lista {m.group(3)} €.",
                    f"Mêmes caractéristiques déclarées ; selon PadelZoom elle a plus de {_voce(m.group(1), lang)} et moins de {_voce(m.group(2), lang)}. Prix public {m.group(3)} €."))
    add(r'^Dati dalla scheda di (<a [^>]+>PadelZoom</a>); livello consigliato stimato da PadelMetrix in base a materiali e tatto\.$',
        lambda m: X(f"Data from the {m.group(1)} page; recommended level estimated by PadelMetrix from materials and feel.",
                    f"Datos de la ficha de {m.group(1)}; nivel recomendado estimado por PadelMetrix según materiales y tacto.",
                    f"Données de la fiche {m.group(1)} ; niveau conseillé estimé par PadelMetrix d'après les matériaux et le toucher."))
    # adidas: sintesi a punteggi
    add(r"^PadelZoom le assegna ([\d,]+)/10 complessivo, ma senza un'analisi scritta: per ora ci sono solo i punteggi\.$",
        lambda m: X(f"PadelZoom gives it {num(m.group(1), lang)}/10 overall, but without a written review: for now there are only the scores.",
                    f"PadelZoom le da {m.group(1)}/10 en total, pero sin un análisis escrito: por ahora solo hay puntuaciones.",
                    f"PadelZoom lui attribue {m.group(1)}/10 au global, mais sans analyse écrite : pour l'instant il n'y a que les notes."))
    add(r"^I valori più alti sono (.+?) \(([\d,]+)\) e (.+?) \(([\d,]+)\), il più basso è (.+?) \(([\d,]+)\)\.$",
        lambda m: X(f"The highest scores are {_voce(m.group(1), lang)} ({num(m.group(2), lang)}) and {_voce(m.group(3), lang)} ({num(m.group(4), lang)}), the lowest is {_voce(m.group(5), lang)} ({num(m.group(6), lang)}).",
                    f"Los valores más altos son {_voce(m.group(1), lang)} ({m.group(2)}) y {_voce(m.group(3), lang)} ({m.group(4)}), el más bajo es {_voce(m.group(5), lang)} ({m.group(6)}).",
                    f"Les meilleures notes concernent {_voce(m.group(1), lang)} ({m.group(2)}) et {_voce(m.group(3), lang)} ({m.group(4)}), la plus basse {_voce(m.group(5), lang)} ({m.group(6)})."))
    add(r"^(Solo punteggi, senza analisi scritta|Con analisi scritta, riassunta sopra)\. Uscita di palla ([\d,]+), maneggevolezza ([\d,]+), sweet spot ([\d,]+)\.$",
        lambda m: X((("Scores only, no written review" if m.group(1).startswith("Solo") else "With a written review, summarised above") + f". Ball output {num(m.group(2), lang)}, maneuverability {num(m.group(3), lang)}, sweet spot {num(m.group(4), lang)}."),
                    (("Solo puntuaciones, sin análisis escrito" if m.group(1).startswith("Solo") else "Con análisis escrito, resumido arriba") + f". Salida de bola {m.group(2)}, manejabilidad {m.group(3)}, punto dulce {m.group(4)}."),
                    (("Notes seules, sans analyse écrite" if m.group(1).startswith("Solo") else "Avec une analyse écrite, résumée plus haut") + f". Sortie de balle {m.group(2)}, maniabilité {m.group(3)}, sweet spot {m.group(4)}.")))
    add(r"^(.+) \(([\d,]+)/10 per PadelZoom\)$", lambda m: f"{t(m.group(1), lang)} ({num(m.group(2), lang)}/10 " + X("according to PadelZoom)", "según PadelZoom)", "selon PadelZoom)"))
    add(r"^(.+) \(([\d,]+)/10\)$", lambda m: f"{t(m.group(1), lang)} ({num(m.group(2), lang)}/10)")
    add(r"^Prezzo di listino alto \((\d+) €\)$", lambda m: X(f"High list price (€{m.group(1)})", f"Precio de lista alto ({m.group(1)} €)", f"Prix public élevé ({m.group(1)} €)"))
    add(r"^Prezzo basso \(listino (\d+) €\)$", lambda m: X(f"Low price (€{m.group(1)} list)", f"Precio bajo (lista {m.group(1)} €)", f"Prix bas ({m.group(1)} € prix public)"))
    # pro/contro del lotto con variabili
    add(r"^Superficie in carbonio (\d+K)$", lambda m: X(f"{m.group(1)} carbon face", f"Cara de carbono {m.group(1)}", f"Surface en carbone {m.group(1)}"))
    add(r"^Il modello di (.+)$", lambda m: X(f"{m.group(1)}'s model", f"El modelo de {m.group(1)}", f"Le modèle de {m.group(1)}"))
    add(r"^Collezione (\d{4}) di (.+)$", lambda m: X(f"{m.group(2)} {m.group(1)} collection", f"Colección {m.group(1)} de {m.group(2)}", f"Collection {m.group(1)} de {m.group(2)}"))
    add(r"^Sei di livello (.+)$", lambda m: X(f"You are at {pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)} level", f"Tienes un nivel {pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)}", f"Vous avez un niveau {pick(LIV_LOWER, m.group(1), lang) or t(m.group(1), lang)}"))
    add(r"^Cerchi un modello recente di (.+)$", lambda m: X(f"You want a recent {m.group(1)} model", f"Buscas un modelo reciente de {m.group(1)}", f"Vous cherchez un modèle récent de {m.group(1)}"))
    # avvisi del lotto
    add(r'^<p>È uscita la versione (\d{4}): <a href="([^"]+)">(.+?)</a>\. Il modello (\d{4}) resta in vendita e spesso si trova scontato\.</p>$',
        lambda m: X(f'<p>The {m.group(1)} version is out: <a href="{m.group(2)}">{m.group(3)}</a>. The {m.group(4)} model is still on sale and is often discounted.</p>',
                    f'<p>Ya ha salido la versión {m.group(1)}: <a href="{m.group(2)}">{m.group(3)}</a>. El modelo {m.group(4)} sigue a la venta y a menudo con descuento.</p>',
                    f'<p>La version {m.group(1)} est sortie : <a href="{m.group(2)}">{m.group(3)}</a>. Le modèle {m.group(4)} reste en vente et se trouve souvent en promotion.</p>'))
    add(r'^<p>Questa è la nuova versione\. Il <a href="([^"]+)">modello (\d{4})</a> resta in vendita e spesso si trova scontato\.</p>$',
        lambda m: X(f'<p>This is the new version. The <a href="{m.group(1)}">{m.group(2)} model</a> is still on sale and is often discounted.</p>',
                    f'<p>Esta es la nueva versión. El <a href="{m.group(1)}">modelo {m.group(2)}</a> sigue a la venta y a menudo con descuento.</p>',
                    f'<p>Voici la nouvelle version. Le <a href="{m.group(1)}">modèle {m.group(2)}</a> reste en vente et se trouve souvent en promotion.</p>'))
    add(r"^([A-Z][\w -]+) · (\d{4})$", lambda m: m.group(0))
    add(r"^Presso i rivenditori si trova già da circa ([\d,]+) €\.$",
        lambda m: X(f"Retailers already sell it from about €{num(m.group(1), lang)}.", f"En las tiendas ya se encuentra desde unos {m.group(1)} €.", f"Chez les revendeurs, on la trouve déjà à partir d'environ {m.group(1)} €."))
    add(r"^Sito ufficiale · listino ([\d,]+) €$", lambda m: X(f"Official website · list price €{num(m.group(1), lang)}", f"Web oficial · precio de lista {m.group(1)} €", f"Site officiel · prix public {m.group(1)} €"))
    add(r"^Sito ufficiale · prezzo consigliato ([\d,]+) €$", lambda m: X(f"Official website · recommended price €{num(m.group(1), lang)}", f"Web oficial · precio recomendado {m.group(1)} €", f"Site officiel · prix conseillé {m.group(1)} €"))
    add(r"^Sito ufficiale · ([\d,]+) € \(listino ([\d,]+) €\)$", lambda m: X(f"Official website · €{num(m.group(1), lang)} (list price €{num(m.group(2), lang)})", f"Web oficial · {m.group(1)} € (precio de lista {m.group(2)} €)", f"Site officiel · {m.group(1)} € (prix public {m.group(2)} €)"))
    add(r'^Punteggi su 10 di (<a [^>]+>PadelZoom</a>), voto complessivo ([\d,]+)/10\. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione\.$',
        lambda m: X(f"Scores out of 10 from {m.group(1)}, overall rating {num(m.group(2), lang)}/10. The PadelMetrix score will follow with our own rating method.",
                    f"Puntuaciones sobre 10 de {m.group(1)}, nota global {m.group(2)}/10. La puntuación PadelMetrix llegará con nuestro método de valoración.",
                    f"Notes sur 10 de {m.group(1)}, note globale {m.group(2)}/10. La note PadelMetrix arrivera avec notre propre méthode d'évaluation."))
    add(r"^Racchetta (a diamante pensata per attaccare|a goccia polivalente|rotonda pensata per il controllo e la regolarità), della linea (.+?): (.+)\.$",
        lambda m: ({"a diamante pensata per attaccare": ("Diamond racket built for attack", "Pala diamante pensada para atacar", "Raquette diamant pensée pour attaquer"),
                    "a goccia polivalente": ("All-round teardrop racket", "Pala lágrima polivalente", "Raquette goutte d'eau polyvalente"),
                    "rotonda pensata per il controllo e la regolarità": ("Round racket built for control and consistency", "Pala redonda pensada para el control y la regularidad", "Raquette ronde pensée pour le contrôle et la régularité")}[m.group(1)][IDX[lang]]
                   + X(f", from the {m.group(2)} line: ", f", de la línea {m.group(2)}: ", f", de la gamme {m.group(2)} : ") + t(m.group(3), lang) + "."))
    add(r"^Materiali di fascia alta \((.+)\) per giocatori esperti(\.?)$",
        lambda m: X(f"High-end materials ({t(m.group(1), lang)}) for experienced players{m.group(2)}", f"Materiales de gama alta ({t(m.group(1), lang)}) para jugadores expertos{m.group(2)}", f"Matériaux haut de gamme ({t(m.group(1), lang)}) pour joueurs expérimentés{m.group(2)}"))
    add(r"^È la stessa racchetta della (.+): cambia solo il colore(\.?)$",
        lambda m: X(f"It is the same racket as the {m.group(1)}: only the colour changes{m.group(2)}", f"Es la misma pala que la {m.group(1)}: solo cambia el color{m.group(2)}", f"C'est la même raquette que la {m.group(1)} : seule la couleur change{m.group(2)}"))
    add(r"^Superficie in (carbonio .+?) e telaio in carbonio, per giocatori che hanno già una buona base tecnica(\.?)$",
        lambda m: X(f"{ucfirst(t(m.group(1), lang))} face and carbon frame, for players who already have a good technical base{m.group(2)}", f"Cara de {t(m.group(1), lang)} y marco de carbono, para jugadores que ya tienen una buena base técnica{m.group(2)}", f"Surface en {t(m.group(1), lang)} et cadre en carbone, pour des joueurs qui ont déjà une bonne base technique{m.group(2)}"))
    add(r"^(Potenza|Tolleranza) ([\d,]+)/(10|5)$", lambda m: f"{ucfirst(_voce(m.group(1), lang)) if m.group(1) == 'Potenza' else X('Forgiveness', 'Tolerancia', 'Tolérance')} {num(m.group(2), lang)}/{m.group(3)}")
    add(r"^community ([\d,]+)/10 \((\d+) recensioni\)$", lambda m: X(f"community {num(m.group(1), lang)}/10 ({m.group(2)} reviews)", f"comunidad {m.group(1)}/10 ({m.group(2)} reseñas)", f"communauté {m.group(1)}/10 ({m.group(2)} avis)"))
    add(r"^Media \((\d+)/100 per (.+)\)$", lambda m: X(f"Medium ({m.group(1)}/100 according to {m.group(2)})", f"Media ({m.group(1)}/100 según {m.group(2)})", f"Moyenne ({m.group(1)}/100 selon {m.group(2)})"))
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
    stile = {" d'attacco": ("attacking", "de ataque", "d'attaque"), " di controllo": ("control", "de control", "de contrôle"), " polivalente": ("all-round", "polivalente", "polyvalente")}.get(st)
    if en:
        head = " ".join(x for x in ((stile[0] if stile else None), (forma or "racket")) if x)
        head = head[0].upper() + head[1:]
        if forma:
            head += " racket"
    elif lang == "fr":
        head = "Raquette" + ((" " + ("en goutte d'eau" if testa == "Goccia" else forma)) if forma else "") + ((" " + stile[2]) if stile else "")
    else:
        head = ("Pala " + (forma or "")).strip() + ((" " + stile[1]) if stile else "")
    parti = [head]
    for x in (m.group(4) or "").split(", ")[1:]:
        parti.append(diff_item(x, lang))
    return ", ".join(parti) + "."


def diff_item(x, lang):
    en = lang == "en"

    def X(a, b, c):
        return a if lang == "en" else (b if lang == "es" else c)
    x = x.strip()
    r = re.match(r"^(\d+[–-]\d+ g|\d+ g)$", x)
    if r:
        return x
    r = re.match(r"^carbonio (\d+K)$", x)
    if r:
        return X(f"{r.group(1)} carbon", f"carbono {r.group(1)}", f"carbone {r.group(1)}")
    if x == "fibra di vetro":
        return X("fiberglass", "fibra de vidrio", "fibre de verre")
    r = re.match(r"^livello (.+)$", x)
    if r:
        lv = pick(LIV_LOWER, r.group(1), lang) or t(r.group(1), lang)
        return X(f"{lv} level", f"nivel {lv}", f"niveau {lv}")
    if x == "listino più alto":
        return X("higher list price", "precio de lista más alto", "prix public plus élevé")
    if x == "listino più basso":
        return X("lower list price", "precio de lista más bajo", "prix public plus bas")
    r = re.match(r"^forma (.+)$", x)
    if r:
        return X(f"{_forma_w(r.group(1), lang)} shape", f"forma {_forma_w(r.group(1), lang)}", f"forme {_forma_w(r.group(1), lang)}")
    r = re.match(r"^superficie in (.+)$", x)
    if r:
        return X(f"{t(r.group(1), lang)} face", f"cara de {t(r.group(1), lang)}", f"surface en {t(r.group(1), lang)}")
    r = re.match(r"^gomma (.+)$", x)
    if r:
        return X(f"{r.group(1)} rubber", f"goma {r.group(1)}", f"gomme {r.group(1)}")
    r = re.match(r"^tatto (.+)$", x)
    if r:
        tt = pick(TATTI, r.group(1), lang) or t(r.group(1), lang)
        return X(f"{tt} feel", f"tacto {tt}", f"toucher {tt}")
    r = re.match(r"^linea (.+)$", x)
    if r:
        return X(f"{r.group(1)} line", f"línea {r.group(1)}", f"gamme {r.group(1)}")
    return t(x, lang)


TERMINI = [
    (r"\bCarbonio alluminizzato (\d+K)\b", ("Aluminized \\1 carbon", "Carbono aluminizado \\1", "Carbone \\1 aluminisé")),
    (r"\bCarbonio (\d+K) alluminizzato\b", ("Aluminized \\1 carbon", "Carbono \\1 aluminizado", "Carbone \\1 aluminisé")),
    (r"\bfibra di vetro\b", ("fiberglass", "fibra de vidrio", "fibre de verre")), (r"\bFibra di vetro\b", ("Fiberglass", "Fibra de vidrio", "Fibre de verre")),
    (r"\bCarbonio\b", ("Carbon", "Carbono", "Carbone")), (r"\bcarbonio\b", ("carbon", "carbono", "carbone")),
    (r"\btexture 3D\b", ("3D texture", "textura 3D", "texture 3D")), (r"\bfinitura sabbiata\b", ("sandy finish", "acabado arenoso", "finition sablée")),
    (r"\bfinitura\b", ("finish", "acabado", "finition")), (r"\bruvido sabbiato\b", ("rough sandy finish", "rugoso arenoso", "rugueux sablé")),
    (r"\bopaco\b", ("matte", "mate", "mat")), (r"\ba trama aperta\b", ("open weave", "de trama abierta", "à trame ouverte")),
    (r"\bunidirezionale\b", ("unidirectional", "unidireccional", "unidirectionnel")), (r"\bbidirezionale\b", ("bidirectional", "bidireccional", "bidirectionnel")),
    (r"\bdi fascia alta\b", ("high-end", "de gama alta", "haut de gamme")), (r"\besagonale\b", ("hexagonal", "hexagonal", "hexagonal")),
    (r"\bflessibile\b", ("flexible", "flexible", "flexible")), (r"\bibrido\b", ("hybrid", "híbrido", "hybride")), (r"\bmisto\b", ("mixed", "mixto", "mixte")),
    (r"\bmorbid[oa]\b", ("soft", "blando", "souple")), (r"\brinforzat[oa]\b", ("reinforced", "reforzado", "renforcé")), (r"\btubolare\b", ("tubular", "tubular", "tubulaire")),
    (r"\bdoppio tubo\b", ("double tube", "doble tubo", "double tube")), (r"\bDoppio tubolare\b", ("Double tubular", "Doble tubular", "Double tubulaire")),
    (r"\bdoppio tubolare\b", ("double tubular", "doble tubular", "double tubulaire")), (r"\bbiossido di titanio\b", ("titanium dioxide", "dióxido de titanio", "dioxyde de titane")),
    (r"\bdurezza intermedia\b", ("medium hardness", "dureza intermedia", "dureté intermédiaire")), (r"\brisposta più morbida\b", ("softer response", "respuesta más blanda", "réponse plus souple")),
    (r"\balta densità\b", ("high density", "alta densidad", "haute densité")), (r"\bdoppia densità\b", ("dual density", "doble densidad", "double densité")),
    (r"\btre strati\b", ("three layers", "tres capas", "trois couches")), (r"\bdurezza media\b", ("medium hardness", "dureza media", "dureté moyenne")),
    (r"\bgomma\b", ("rubber", "goma", "gomme")), (r"\bGomma\b", ("Rubber", "Goma", "Gomme")), (r"\bliscia\b", ("smooth", "lisa", "lisse")), (r"\bruvida\b", ("rough", "rugosa", "rugueuse")),
    (r"\bdura\b", ("hard", "dura", "dure")), (r"\bmedia\b", ("medium", "media", "moyenne")), (r"\bmonoblocco\b", ("single-piece", "monobloque", "monobloc")),
    (r"\bmanico allungato\b", ("extended handle", "mango alargado", "manche allongé")), (r"\bponte\b", ("bridge", "puente", "pont")),
    (r"\btunnel\b", ("tunnels", "túneles", "tunnels")), (r"\bcirca\b", ("about", "aprox.", "environ")), (r"\bsilver\b", ("silver", "plata", "argent")),
    (r"\bcon\b", ("with", "con", "avec")), (r"\be\b", ("and", "y", "et")), (r"\bin\b", ("in", "en", "en")),
]
MARKER = {"en": {"di", "della", "delle", "del", "dei", "per", "più", "che", "il", "la", "le", "gli", "è", "una", "un", "alla", "al", "dalla", "molto", "senza", "sono", "ma", "non", "da", "con", "e", "lo", "nel", "nella", "sul", "anche"},
          "es": {"di", "della", "delle", "dei", "per", "più", "che", "il", "gli", "è", "alla", "dalla", "molto", "senza", "sono", "ma", "non", "da", "e", "lo", "nel", "nella", "sul", "anche"},
          "fr": {"di", "della", "delle", "dei", "per", "più", "che", "il", "gli", "è", "alla", "dalla", "molto", "senza", "sono", "ma", "non", "da", "e", "lo", "nel", "nella", "sul", "anche", "con"}}
ITA_PAROLE = re.compile(r"\b(per|più|della|delle|dalla|molto|senza|gioco|giocatori|racchetta|leggera|morbid|potenza|controllo|versione|basso|bassa|chi|vuole|cerca)\b", re.I)


def termini(s, lang):
    i = IDX[lang]
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
