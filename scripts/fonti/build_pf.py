"""Trasforma i dati estratti da Padelful in un lotto di schede PadelMetrix e nelle traduzioni dei testi generati.

Uso: python3 build_pf.py pf_dati.jsonl nome_lotto [anno_min]
Scrive scripts/dati_lotto/<nome_lotto>.py e aggiorna data/traduzioni/tm_pair_pf.json e tm_fr_pf.json.
Regole: solo dati pubblicati da Padelful; nessun testo copiato dalle recensioni; livello e stile stimati da forma, tatto,
materiali e punteggi (lo dichiara la nota della scheda); varianti di colore unite in una sola scheda."""
import glob
import json
import pathlib
import re
import sys
import unicodedata

ROOT = pathlib.Path("/home/claude/padelmetrix-site")
BRAND = {"adidas": "Adidas", "alkemia": "Alkemia", "babolat": "Babolat", "black-crown": "Black Crown", "bullpadel": "Bullpadel",
         "drop-shot": "Drop Shot", "dunlop": "Dunlop", "enebe": "Enebe", "head": "Head", "hirostar": "Hirostar", "joma": "Joma",
         "kombat": "Kombat", "kuikma": "Kuikma", "level": "Level", "lok": "Lok", "middle-moon": "Middle Moon", "munich": "Munich",
         "neuronpadel": "NeuronPadel", "nox": "Nox", "osaka": "Osaka", "oxdog": "Oxdog", "padelsmith": "Padelsmith", "pallap": "Pallap",
         "royal-padel": "Royal Padel", "sane": "Sane", "set": "SET Padel", "siux": "Siux", "softee": "Softee", "star-vie": "StarVie",
         "tactical": "Tactical Padel", "tecnifibre": "Tecnifibre", "vibora": "Vibor-A", "wilson": "Wilson", "akkeron": "Akkeron",
         "puma": "Puma", "varlion": "Varlion", "xcalion": "Xcalion", "ocho": "Ocho Padel", "just-ten": "Just Ten", "kelme": "Kelme",
         "cork": "Cork", "grandcow": "Grandcow", "artengo": "Artengo"}
PLAYER_FIX = {"Agustin Tapia": "Agustín Tapia", "Juan Lebron": "Juan Lebrón", "Ale Galan": "Ale Galán", "Martin Di Nenno": "Martín Di Nenno",
              "Bea Gonzalez": "Bea González", "Paquito Navarro": "Paquito Navarro", "Leo Augsburger": "Leo Augsburger",
              "Franco Stupaczuk": "Franco Stupaczuk", "Miguel Lamperti": "Miguel Lamperti", "Aranzazu Osoro": "Aranzazu Osoro",
              "Ari Sanchez": "Ari Sánchez", "Martita Ortega": "Martita Ortega", "Gemma Triay": "Gemma Triay", "Delfi Brea": "Delfi Brea",
              "Raul Marcos": "Raúl Marcos", "Coki Nieto": "Coki Nieto", "Lucas Bergamini": "Lucas Bergamini", "Javi Ruiz": "Javi Ruiz",
              "Vero Virseda": "Vero Virseda", "Patty Llaguno": "Patty Llaguno", "Manu Martin": "Manu Martín", "Arturo Coello": "Arturo Coello",
              "Fede Chingotto": "Fede Chingotto", "Juan Tello": "Juan Tello", "Paula Josemaria": "Paula Josemaría", "Ariana Sanchez": "Ariana Sánchez",
              "Alejandra Salazar": "Alejandra Salazar", "Marta Ortega": "Marta Ortega", "Sanyo Gutierrez": "Sanyo Gutiérrez",
              "Momo Gonzalez": "Momo González", "Maxi Sanchez": "Maxi Sánchez", "Pablo Lima": "Pablo Lima", "Fernando Belasteguin": "Fernando Belasteguín",
              "Lucia Sainz": "Lucía Sainz", "Claudia Fernandez": "Claudia Fernández", "Jon Sanz": "Jon Sanz", "Mike Yanguas": "Mike Yanguas",
              "Javi Garrido": "Javi Garrido", "Tolito Aguirre": "Tolito Aguirre", "Alex Ruiz": "Álex Ruiz", "Juani Mieres": "Juani Mieres",
              "Agustin Gutierrez": "Agustín Gutiérrez", "Lucas Campagnolo": "Lucas Campagnolo", "Martin Sanchez": "Martín Sánchez",
              "Edu Alonso": "Edu Alonso", "Jessica Castello": "Jessica Castelló", "Bea Caldera": "Bea Caldera", "Tamara Icardo": "Tamara Icardo"}
COLORI = {"blue": ("blu", "blue", "azul", "bleu"), "red": ("rosso", "red", "rojo", "rouge"), "white": ("bianco", "white", "blanco", "blanc"),
          "black": ("nero", "black", "negro", "noir"), "silver": ("argento", "silver", "plata", "argent"), "gold": ("oro", "gold", "oro", "or"),
          "green": ("verde", "green", "verde", "vert"), "pink": ("rosa", "pink", "rosa", "rose"), "yellow": ("giallo", "yellow", "amarillo", "jaune"),
          "violet": ("viola", "violet", "violeta", "violet"), "purple": ("viola", "purple", "morado", "violet"), "grey": ("grigio", "grey", "gris", "gris"),
          "gray": ("grigio", "grey", "gris", "gris"), "orange": ("arancione", "orange", "naranja", "orange"), "bronze": ("bronzo", "bronze", "bronce", "bronze"),
          "navy": ("blu navy", "navy", "azul marino", "bleu marine"), "coral": ("corallo", "coral", "coral", "corail"), "mint": ("menta", "mint", "menta", "menthe"),
          "turquoise": ("turchese", "turquoise", "turquesa", "turquoise"), "lime": ("lime", "lime", "lima", "citron vert")}
FORMA = {"tear": "goccia", "diamond": "diamante", "round": "rotonda", "teardrop": "goccia", "tear drop": "goccia", "hybrid": "ibrida", "drop": "goccia"}
TATTO = {"soft": "morbido", "medium": "medio", "hard": "duro", "medium-soft": "medio-morbido", "medium soft": "medio-morbido",
         "soft-medium": "medio-morbido", "medium-hard": "medio-duro", "medium hard": "medio-duro", "hard-medium": "medio-duro",
         "very soft": "morbido", "very hard": "duro", "semi-hard": "medio-duro", "semi-soft": "medio-morbido"}
# parole dei materiali: EN -> (IT, ES, FR)
W = [(r"\bfiberglass\b|\bfibreglass\b|\bglass ?fib(?:er|re)\b|\bfiber ?glass\b", ("fibra di vetro", "fibra de vidrio", "fibre de verre")),
     (r"\baluminized\b|\baluminised\b|\baluminum\b|\baluminium\b|\balum\b", ("alluminizzato", "aluminizado", "aluminisé")),
     (r"\bcarbon fib(?:er|re)\b", ("fibra di carbonio", "fibra de carbono", "fibre de carbone")),
     (r"\bcarbon\b", ("carbonio", "carbono", "carbone")), (r"\bgraphene\b", ("grafene", "grafeno", "graphène")),
     (r"\bkevlar\b", ("kevlar", "kevlar", "kevlar")), (r"\btitanium\b", ("titanio", "titanio", "titane")),
     (r"\bbasalt\b", ("basalto", "basalto", "basalte")), (r"\bpolyethylene\b", ("polietilene", "polietileno", "polyéthylène")),
     (r"\bfoam\b", ("foam", "foam", "mousse")), (r"\btubular\b", ("tubolare", "tubular", "tubulaire")),
     (r"\breinforced\b", ("rinforzato", "reforzado", "renforcé")), (r"\bhybrid\b", ("ibrido", "híbrido", "hybride")),
     (r"\band\b", ("e", "y", "et")), (r"\bwith\b", ("con", "con", "avec")), (r"\bsilver\b", ("argento", "plata", "argent")),
     (r"\bgold\b", ("oro", "oro", "or")), (r"\bblack\b", ("nero", "negro", "noir")), (r"\bwhite\b", ("bianco", "blanco", "blanc")),
     (r"\bframe\b", ("telaio", "marco", "cadre")), (r"\bfaces?\b", ("piatti", "caras", "faces")), (r"\bcore\b", ("nucleo", "núcleo", "noyau")),
     (r"\bbidirectional\b", ("bidirezionale", "bidireccional", "bidirectionnel")), (r"\bdouble\b|\bdual\b", ("doppio", "doble", "double")),
     (r"\b100% full\b", ("100%", "100%", "100%")), (r"\bfull\b", ("", "", "")), (r"\bsoft\b", ("morbido", "blando", "souple")),
     (r"\bfiber\b|\bfibre\b", ("fibra", "fibra", "fibre"))]
EVA = [(r"^soft eva$", ("EVA morbida", "soft EVA", "EVA blanda", "EVA souple")), (r"^medium eva$", ("EVA media", "medium EVA", "EVA media", "EVA medium")),
       (r"^hard eva$", ("EVA dura", "hard EVA", "EVA dura", "EVA dure")), (r"^eva$", ("EVA", "EVA", "EVA", "EVA")),
       (r"^eva soft$", ("EVA morbida", "soft EVA", "EVA blanda", "EVA souple")), (r"^eva hard$", ("EVA dura", "hard EVA", "EVA dura", "EVA dure")),
       (r"^eva medium$", ("EVA media", "medium EVA", "EVA media", "EVA medium")), (r"^foam$", ("foam", "foam", "foam", "mousse")),
       (r"^multieva$|^multi eva$|^multi-eva$", ("MultiEVA", "MultiEVA", "MultiEVA", "MultiEVA")), (r"^polyethylene$", ("polietilene", "polyethylene", "polietileno", "polyéthylène")),
       (r"^ultra soft eva$|^eva ultra soft$", ("EVA molto morbida", "ultra-soft EVA", "EVA muy blanda", "EVA très souple")),
       (r"^super soft eva$|^eva super soft$", ("EVA molto morbida", "super-soft EVA", "EVA muy blanda", "EVA très souple")),
       (r"^black eva$|^eva black$", ("EVA Black", "Black EVA", "EVA Black", "EVA Black")), (r"^pro eva$|^eva pro$", ("EVA Pro", "Pro EVA", "EVA Pro", "EVA Pro"))]

# esclusioni: modelli già in catalogo con nome diverso, edizioni città, colori nel mezzo del nome
SKIP = [r"^Siux\|(Diablo Pro|Electra Pro|Fenix Pro|Pegasus Pro|Trilogy Pro) (Night|Royal|Fire|Shadow|Glow|Lava|Storm|Ash|Noir Fog|Black)$",
        r"^Siux\|(Electra|Fenix|Trilogy|Diablo|Pegasus) Elite 6$", r"^Softee\|Freezer Carbon 3K (Petrol|Verde)$",
        r"^Nox\|AT10 Genius .*(Riyadh|London|Buenos Aires)$", r"^Kombat\|.* 2\.5 by Manu Martin$",
        r"^Babolat\|(Technical )?(Veron|Viper|Viper Soft) 3\.[01]$", r"^Babolat\|(Air|Counter) (Veron|Vertuo|Viper)$",
        r"^Bullpadel\|Pearl Bea Gonzalez$", r"^Bullpadel\|Elite 02 Woman$", r"^Hirostar\|Alien (Core|Pro)$", r"^Adidas\|Metalbone Reserve$"]
MERGE = {("Lok", "Be Flow Gen 2 Pink-Green"): ("Be Flow Gen 2", "pink"), ("Lok", "Be Flow Gen 2 Yellow-Blue"): ("Be Flow Gen 2", "yellow"),
         ("Enebe", "Suburban Green 12K"): ("Suburban 12K", "green"), ("Enebe", "Suburban Red 12K"): ("Suburban 12K", "red"),
         ("Enebe", "Mustang Esmerald 15K"): ("Mustang 15K", "green"), ("Enebe", "Mustang Gold 15K"): ("Mustang 15K", "gold"),
         ("Enebe", "Suburban Silver 3K"): ("Suburban 3K", None), ("Nox", "Nextgen Pro Attack 12K"): ("NextGen Pro Attack 12K", None),
         ("Nox", "Nextgen Pro Hybrid 12K"): ("NextGen Pro Hybrid 12K", None)}

PERSISTENTI = {"Wilson", "Varlion", "Royal Padel", "Black Crown", "Enebe", "Lok", "Tecnifibre", "Kombat", "Kuikma", "Softee", "Vibor-A", "Dunlop", "Oxdog", "Joma"}
COLORI_ES = r"\s+(?:Gris|Negro|Turquesa|Azul|Rojo|Verde|Blanco|Amarillo|Naranja|Rosa|Morado)(?:-(?:Gris|Negro|Turquesa|Azul|Rojo|Verde|Blanco|Amarillo|Naranja|Rosa|Morado))*$"
GIOC_NOME = {"Jon Sanz": "Jon Sanz", "Pablo Lima": "Pablo Lima", "Stupa": "Franco Stupaczuk", "Juan Lebron": "Juan Lebrón"}


def mat(en):
    """Valore di materiale in EN -> (IT, EN, ES, FR). I nomi commerciali restano invariati."""
    s = re.sub(r"\s+", " ", en.strip())
    low = s.lower()
    for pat, v in EVA:
        if re.fullmatch(pat, low):
            return v
    m = re.fullmatch(r"(.+?) \((.+)\)", s)
    if m:
        a, b = mat(m.group(1)), mat(m.group(2))
        return tuple(f"{a[i]} ({b[i]})" for i in range(4))
    out = []
    for i in range(3):
        x = s
        for pat, v in W:
            x = re.sub(pat, v[i], x, flags=re.I)
        out.append(x)
    it, es, fr = out
    # ordine "12K carbonio" -> "carbonio 12K"
    def kord(x, w):
        return re.sub(r"\b(\d+K) " + w + r"\b", w + r" \1", x)
    it, es, fr = kord(it, "carbonio"), kord(es, "carbono"), kord(fr, "carbone")
    it = re.sub(r"carbonio alluminizzato|alluminizzato carbonio", "carbonio alluminizzato", it)
    es = re.sub(r"aluminizado carbono", "carbono aluminizado", es)
    fr = re.sub(r"aluminisé carbone", "carbone aluminisé", fr)
    ENG = r"\b(layers?|blown|twin|tube|reinforced frame|shaped|structure|system|technology|inside|of|the|for|by)\b"
    if any(re.search(ENG, x, re.I) for x in (it, es, fr)):
        has = [w for w in ("carbon", "kevlar", "fiberglass", "glass", "graphene", "aluminum") if w in low]
        parti = {"carbon": ("carbonio", "carbon", "carbono", "carbone"), "kevlar": ("kevlar", "Kevlar", "kevlar", "kevlar"),
                 "fiberglass": ("fibra di vetro", "fiberglass", "fibra de vidrio", "fibre de verre"), "glass": ("fibra di vetro", "fiberglass", "fibra de vidrio", "fibre de verre"),
                 "graphene": ("grafene", "graphene", "grafeno", "graphène"), "aluminum": ("alluminio", "aluminium", "aluminio", "aluminium")}
        has = list(dict.fromkeys(parti[w] for w in has))
        if not has:
            return None
        j = (" e ", " and ", " y ", " et ")
        v = tuple(j[i].join(h[i] for h in has) for i in range(4))
        return tuple(x[0].upper() + x[1:] for x in v)
    def riordina(x, nome):
        return re.sub(r"^([A-Z][\w\-]*(?: [A-Z][\w\-]*)?) (" + nome + r")$", r"\2 \1", x)
    it, es, fr = riordina(it, "carbonio"), riordina(es, "carbono"), riordina(fr, "carbone")
    it, es, fr = (re.sub(r"\s{2,}", " ", x).strip() for x in (it, es, fr))
    en2 = re.sub(r"\bfibreglass\b", "fiberglass", s, flags=re.I)
    cap = lambda x: x[0].upper() + x[1:] if x else x  # noqa: E731
    return cap(it), cap(en2), cap(es), cap(fr)


def _k(low):
    m = re.search(r"\b(\d{1,2})\s?k\b", low)
    return f" {m.group(1)}K" if m else ""


def piatti_std(en):
    low = en.lower()
    carb = "carbon" in low or "carbono" in low or re.search(r"\b\d{1,2}k\b", low)
    vetro = any(w in low for w in ("fiberglass", "fibreglass", "glass", "polyglass", "fibrix", "vidrio"))
    alu = any(w in low for w in ("alum", "silver"))
    graf = "graphene" in low or "glaphite" in low or "graphite" in low
    kev = "kevlar" in low or "aramid" in low
    if carb and vetro:
        v = ("Carbonio e fibra di vetro", "Carbon and fiberglass", "Carbono y fibra de vidrio", "Carbone et fibre de verre")
    elif carb:
        k = _k(low)
        if alu:
            v = ("Carbonio alluminizzato" + k, k.strip() + " aluminised carbon" if k else "Aluminised carbon", "Carbono aluminizado" + k, "Carbone aluminisé" + k)
            v = (v[0], v[1][0].upper() + v[1][1:], v[2], v[3])
        else:
            v = ("Carbonio" + k, (k.strip() + " carbon").capitalize() if k else "Carbon", "Carbono" + k, "Carbone" + k)
            if k:
                v = (v[0], k.strip() + " carbon", v[2], v[3])
        if kev:
            v = tuple(x + y for x, y in zip(v, (" e kevlar", " and Kevlar", " y kevlar", " et kevlar")))
    elif vetro:
        v = ("Fibra di vetro alluminizzata", "Aluminised fiberglass", "Fibra de vidrio aluminizada", "Fibre de verre aluminisée") if alu else \
            ("Fibra di vetro", "Fiberglass", "Fibra de vidrio", "Fibre de verre")
    elif graf:
        v = ("Grafite e grafene", "Graphite and graphene", "Grafito y grafeno", "Graphite et graphène")
    elif kev:
        v = ("Kevlar", "Kevlar", "Kevlar", "Kevlar")
    else:
        return None
    return v


def nucleo_std(en):
    low = en.lower()
    if "polyethylene" in low or "polietileno" in low:
        base = ("Polietilene", "Polyethylene", "Polietileno", "Polyéthylène")
        if "soft" in low:
            return ("Polietilene morbido", "Soft polyethylene", "Polietileno blando", "Polyéthylène souple")
        return base
    foam = "foam" in low and "eva" not in low
    if foam:
        return ("Foam", "Foam", "Foam", "Mousse")
    if "multi" in low and "eva" in low:
        return ("EVA multistrato", "Multi-layer EVA", "EVA multicapa", "EVA multicouche")
    if re.search(r"ultra|super|extra soft", low):
        return ("EVA molto morbida", "Very soft EVA", "EVA muy blanda", "EVA très souple")
    if "soft" in low:
        return ("EVA morbida", "Soft EVA", "EVA blanda", "EVA souple")
    if re.search(r"medium|mid\b|media", low):
        return ("EVA media", "Medium EVA", "EVA media", "EVA medium")
    if re.search(r"hard|high.density|dura", low):
        return ("EVA dura", "Hard EVA", "EVA dura", "EVA dure")
    if "eva" in low or "hr" in low:
        return ("EVA", "EVA", "EVA", "EVA")
    return None


def telaio_std(en):
    low = en.lower()
    v = piatti_std(en)
    if not v:
        return None
    if "tub" in low:
        v = tuple(x + y for x, y in zip(v, (" tubolare", " tubular", " tubular", " tubulaire")))
        v = (v[0], v[1].replace("Carbon tubular", "Tubular carbon").replace("carbon tubular", "tubular carbon"), v[2], v[3])
    return v


def nz(s):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", s.lower()).encode("ascii", "ignore").decode().replace("+", "plus"))


def peso(p):
    if not p:
        return None
    m = re.findall(r"\d{3}", p)
    if len(m) >= 2:
        return f"{m[0]}–{m[1]} g"
    if m:
        return f"{m[0]} g"
    return None


def parse(d):
    u = d["url"]; s = u.rsplit("/", 1)[1]
    bkey = next((b for b in sorted(BRAND, key=len, reverse=True) if s.startswith(b + "-")), None)
    if not bkey:
        return None
    marca = BRAND[bkey]
    m = re.search(r"^(.*?)-(20\d\d)(?:-(.+))?$", s)
    if not m:
        return None
    anno = int(m.group(2)); coda = m.group(3) or ""
    tit = d.get("titolo") or ""
    # modello: dal titolo, togliendo marca, anno e giocatore
    tm = re.match(r"^(.*?)\s+20\d\d\b\s*(.*)$", tit)
    prima = tm.group(1) if tm else tit
    nb = len(bkey.split("-"))
    parole = prima.split()
    modello = " ".join(parole[nb:]) if len(parole) > nb else ""
    if not modello:
        modello = " ".join(w.capitalize() for w in m.group(1).split("-")[nb:])
    giocatore = None
    if coda and coda not in ("plus",):
        g = " ".join(w.capitalize() for w in coda.split("-"))
        giocatore = PLAYER_FIX.get(g, g)
    if coda == "plus":
        modello += "+"
    return marca, modello.strip(), anno, giocatore


def stima(r, sc):
    f, ta, c = r.get("f"), r.get("ta") or "", (r.get("c") or "").lower()
    st = {"diamante": "offensivo", "rotonda": "controllo"}.get(f, "polivalente")
    if sc:
        diff = sc[0] - sc[1]
        if diff >= 1.2:
            st = "offensivo"
        elif diff <= -1.2:
            st = "controllo"
    k = re.findall(r"(\d+)k", c)
    k = int(k[0]) if k else 0
    vetro = "vetro" in c
    if r.get("categoria") == "junior":
        l = "principiante"
    elif vetro and "morbido" in ta:
        l = "principiante-intermedio"
    elif vetro:
        l = "intermedio"
    elif ta == "duro" or k >= 15:
        l = "avanzato"
    elif "carbonio" in c and (k >= 12 or ta == "medio-duro"):
        l = "intermedio-avanzato"
    elif "carbonio" in c:
        l = "intermedio"
    else:
        l = "intermedio"
    return st, l


FORMA_D = {"diamante": ("a diamante", "Diamond", "diamante", "diamant"), "rotonda": ("rotonda", "Round", "redonda", "ronde"),
           "goccia": ("a goccia", "Teardrop", "de lágrima", "goutte d'eau"), "ibrida": ("ibrida", "Hybrid", "híbrida", "hybride")}
TATTO_D = {"morbido": ("morbido", "soft", "blando", "doux"), "medio": ("medio", "medium", "medio", "moyen"), "duro": ("duro", "hard", "duro", "dur"),
           "medio-morbido": ("medio-morbido", "medium-soft", "medio-blando", "moyen-doux"), "medio-duro": ("medio-duro", "medium-hard", "medio-duro", "moyen-dur")}
TARGET = {"offensivo": ("È pensata per chi chiude il punto con lo smash.", "It is built for players who finish points with the smash.",
                        "Está pensada para quien cierra el punto con el remate.", "Elle est pensée pour ceux qui finissent le point au smash."),
          "controllo": ("È pensata per chi costruisce il punto con precisione.", "It is built for players who build points with precision.",
                        "Está pensada para quien construye el punto con precisión.", "Elle est pensée pour ceux qui construisent le point avec précision."),
          "polivalente": ("È pensata per chi vuole una racchetta sola per difesa e attacco.", "It is built for players who want one racket for both defence and attack.",
                          "Está pensada para quien quiere una sola pala para defensa y ataque.", "Elle est pensée pour ceux qui veulent une seule raquette pour la défense et l'attaque.")}
JUNIOR_T = ("È pensata per bambini e ragazzi.", "It is designed for children and teenagers.", "Está pensada para niños y jóvenes.", "Elle est pensée pour les enfants et les ados.")


def descr(r, c4, nu4, t4):
    f = FORMA_D.get(r.get("f")); ta = TATTO_D.get(r.get("ta"))
    parti = [[], [], [], []]
    base = [("Racchetta" + (f" {f[0]}" if f else "")), ((f[1] + " racket") if f else "Racket"), ("Pala" + (f" {f[2]}" if f else "")), ("Raquette" + (f" {f[3]}" if f else ""))]
    for i in range(4):
        x = base[i]
        if ta:
            x += [f" dal tatto {ta[0]}", f" with a {ta[1]} feel", f" de tacto {ta[2]}", f" au toucher {ta[3]}"][i]
        mats = []
        if c4:
            lf = lambda x: x if x[:2].isupper() else x[0].lower() + x[1:]  # noqa: E731
            mats.append([f"piatti in {lf(c4[0])}", f"{lf(c4[1]) if not c4[1][0].isdigit() else c4[1]} faces", f"caras de {lf(c4[2])}", f"faces en {lf(c4[3])}"][i])
        if nu4:
            lw = lambda x: x if x[:3] == "EVA" else x[0].lower() + x[1:]  # noqa: E731
            art = "an" if re.match(r"[AEIOU]", nu4[1]) else "a"
            mats.append([f"gomma {lw(nu4[0])}", f"{art} {lw(nu4[1])} core", f"goma {lw(nu4[2])}", f"gomme {lw(nu4[3])}"][i])
        if mats:
            sep = [" e ", " and ", " y ", " et "][i]
            x += [", con ", ", ", ", con ", ", avec "][i] + sep.join(mats)
        parti[i].append(x + ".")
        parti[i].append((JUNIOR_T if r.get("categoria") == "junior" else TARGET[r["st"]])[i])
    return [" ".join(p) for p in parti]


def esistenti():
    k = set()
    for f in glob.glob(str(ROOT / "data/racchette/*.json")):
        j = json.load(open(f))
        k.add((nz(j["marca"]), nz(j["modello"]), j["anno"]))
    return k


def main():
    src, nome = sys.argv[1], sys.argv[2]
    amin = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    have = esistenti()
    R, TM, visti, scarti = [], {}, {}, []
    for l in open(src):
        d = json.loads(l)
        if "errore" in d or not d.get("forma"):
            scarti.append((d["url"], "dati mancanti")); continue
        p = parse(d)
        if not p:
            scarti.append((d["url"], "marca/anno")); continue
        marca, modello, anno, g = p
        if anno < amin:
            continue
        col = None
        modello = re.sub(COLORI_ES, "", modello)
        for k, v in GIOC_NOME.items():
            if modello.endswith(" " + k):
                modello, g = modello[: -len(k) - 1], (g or v)
        if (marca, modello) in MERGE:
            modello, col = MERGE[(marca, modello)]
        if any(re.match(x, f"{marca}|{modello}") for x in SKIP):
            scarti.append((d["url"], "già in catalogo (nome diverso) o edizione")); continue
        # colore finale -> variante
        mm = re.match(r"^(.*?)\s+(" + "|".join(COLORI) + r")$", modello, re.I)
        if mm and not col and len(mm.group(1).split()) >= 1:
            modello, col = mm.group(1), mm.group(2).lower()
        if any(re.match(x, f"{marca}|{modello}") for x in SKIP):
            scarti.append((d["url"], "già in catalogo (nome diverso) o edizione")); continue
        key = (nz(marca), nz(modello), anno)
        alt = {(nz(marca), nz(modello.replace("Woman", "W")), anno), (nz(marca), nz(modello.replace(" Woman", "")), anno),
               (nz(marca), nz(re.sub(r"\bPlus\b", "+", modello)), anno), (nz(marca), nz(modello.replace("+", " Plus")), anno),
               (nz(marca), nz(re.sub(r"\bPolietileno\b", "Poly", modello)), anno), (nz(marca), nz(re.sub(r"\s\d\.\d$", "", modello)), anno)}
        if marca in PERSISTENTI and anno == 2025 and any(h[0] == key[0] and h[1] == key[1] for h in have):
            scarti.append((d["url"], "stesso modello già in catalogo con altro anno")); continue
        if key in have or alt & have:
            scarti.append((d["url"], "già in catalogo")); continue
        if key in visti:
            if col:
                visti[key]["_col"].append(col)
            scarti.append((d["url"], "variante colore")); continue
        r = {"m": marca, "n": modello, "a": anno}
        if g:
            r["g"] = g
        low = modello.lower()
        if re.search(r"\bjunior\b|\bjr\b|\bkids?\b", low):
            r["categoria"] = "junior"
        if re.search(r"\bwoman\b|\bwomen\b|\bw\b|\bwmn\b|\blady\b|\bgirl\b", low):
            r["donna"] = True
        r["f"] = FORMA.get(d["forma"].lower().strip())
        if not r["f"]:
            scarti.append((d["url"], "forma " + d["forma"])); continue
        pz = peso(d.get("peso"))
        if pz:
            r["p"] = pz
        ta = TATTO.get((d.get("tatto") or "").lower().strip())
        if ta:
            r["ta"] = ta
        c4 = piatti_std(d["piatti"]) if d.get("piatti") else None
        nu4 = nucleo_std(d["nucleo"]) if d.get("nucleo") else None
        t4 = telaio_std(d["telaio"]) if d.get("telaio") else None
        for k4, kk in ((c4, "c"), (nu4, "nu"), (t4, "t")):
            if k4:
                r[kk] = k4[0]
                TM[k4[0]] = [k4[1], k4[2], k4[3]]
        sc = None
        ps = d.get("punteggi") or {}
        if d.get("voto") and len(ps) == 5:
            sc = [ps["Power"], ps["Control"], ps["Rebound"], ps["Maneuverability"], ps["Sweet spot"]]
            r["sc"] = {"fonte": "Padelful", "url": d["url"], "tot": d["voto"], "v": sc}
        r["st"], r["l"] = stima(r, sc)
        dd = descr(r, c4, nu4, t4)
        r["d"] = dd[0]
        TM[dd[0]] = dd[1:]
        TM[dd[0][0].lower() + dd[0][1:]] = [x[0].lower() + x[1:] for x in dd[1:]]
        for i, sent in enumerate(re.split(r"(?<=\.) ", dd[0])):
            tr = [re.split(r"(?<=\.) ", x)[i] for x in dd[1:]]
            TM[sent] = tr
            TM[sent[0].lower() + sent[1:]] = [x[0].lower() + x[1:] for x in tr]
        r["src"] = [("Padelful", d["url"])]
        r["_col"] = [col] if col else []
        visti[key] = r
        R.append(r)
    for r in R:
        cols = r.pop("_col")
        if len(cols) >= 2:
            it = ", ".join(COLORI[c][0] for c in cols)
            r["colori"] = it
            TM[it] = [", ".join(COLORI[c][i] for c in cols) for i in (1, 2, 3)]
    out = ROOT / "scripts" / "dati_lotto" / f"{nome}.py"
    out.write_text(f'# Lotto generato da schede Padelful (dati tecnici e punteggi), {len(R)} racchette.\nR = ' + json.dumps(R, ensure_ascii=False, indent=0).replace("true", "True").replace("false", "False").replace("null", "None") + "\n", encoding="utf-8")
    # traduzioni
    pp, pf = ROOT / "data/traduzioni/tm_pair_pf.json", ROOT / "data/traduzioni/tm_fr_pf.json"
    P = json.loads(pp.read_text()) if pp.exists() else {}
    F = dict(json.loads(pf.read_text())) if pf.exists() else {}
    for k, v in TM.items():
        if k == v[0] and k == v[1] and k == v[2]:
            P.setdefault(k, [k, k]); F.setdefault(k, k); continue
        P[k] = [v[0], v[1]]; F[k] = v[2]
    pp.write_text(json.dumps(P, ensure_ascii=False, indent=0), encoding="utf-8")
    pf.write_text(json.dumps([[k, v] for k, v in F.items()], ensure_ascii=False, indent=0), encoding="utf-8")
    import collections
    print(len(R), "schede;", collections.Counter(x[1] for x in scarti))
    print(collections.Counter(r["m"] for r in R).most_common())


if __name__ == "__main__":
    main()
