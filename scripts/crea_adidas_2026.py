#!/usr/bin/env python3
"""Crea i JSON delle 28 racchette Adidas 2026 in data/racchette/."""
import json
import pathlib

OUT = pathlib.Path("/home/claude/padelmetrix-site/data/racchette")
DATA_OGGI = "2026-10-19"
DATA_TXT = "19 ottobre 2026"
PZ = "https://padelzoom.es/"

# nome, slug-pz, linea, forma, peso, gomma, plano, telaio, tatto, pvp, miglior prezzo, scores(pot,ctrl,uscita,man,sweet,glob), giocatore, extra
R = [
    dict(slug="adidas-metalbone-hrd-plus-2026", nome="Metalbone HRD+ 2026", pz="adidas-metalbone-hrd-2026-ale-galan", linea="Metalbone", forma="diamante", peso="345–360 g (+ fino a 11,2 g)", gomma="EVA High Memory", plano="Carbonio alluminizzato 16K", telaio="Carbonio", tatto="medio-duro", pvp=390, best=389.90, s=(10, 9.5, 8, 8, 8, 8.7), giocatore="Ale Galán", wb=True,
         analisi="Per PadelZoom è la Metalbone più dura e la più potente: 10/10 in potenza e 9,5 in controllo nei colpi d'attacco, con un piatto fermo e stabile in volée. In cambio l'uscita di palla è moderata, in difesa bisogna accompagnare di più il colpo, e lo sweet spot è più piccolo di quello delle racchette meno rigide. È pensata per giocatori intermedi alti e avanzati che schiacciano molto e salgono spesso a rete."),
    dict(slug="adidas-metalbone-2026", nome="Metalbone 2026", pz="adidas-metalbone-2026-ale-galan", linea="Metalbone", forma="diamante", peso="345–360 g (+ fino a 11,2 g)", gomma="EVA Soft Performance", plano="Carbonio alluminizzato 16K", telaio="Carbonio", tatto="medio", pvp=390, best=285.95, s=(9, 8.5, 9.5, 8, 8, 8.6), giocatore="Ale Galán", wb=True,
         analisi="Per PadelZoom è una diamante offensiva più accessibile della versione HRD+: uscita di palla molto alta per una diamante (9,5/10), potenza solida in smash e volée aggressive e un tatto medio comodo. La maneggevolezza non spicca e chiede una buona preparazione del colpo; chi colpisce fortissimo può preferire la rigidità della HRD+."),
    dict(slug="adidas-metalbone-ctrl-2026", nome="Metalbone CTRL 2026", pz="adidas-metalbone-ctrl-2026", linea="Metalbone", forma="rotonda", peso="345–360 g (+ fino a 11,2 g)", gomma="EVA Soft Performance", plano="Carbonio alluminizzato 16K", telaio="Carbonio", tatto="medio", pvp=390, best=389.90, s=(8, 8.5, 9.5, 8, 9, 8.6), wb=True,
         analisi="Per PadelZoom è la Metalbone del controllo: sweet spot ampio e tollerante, uscita di palla alta che aiuta molto in difesa e tatto medio comodo. La potenza è limitata rispetto alle versioni a diamante e i giocatori molto aggressivi possono sentirne la mancanza. Indicata per intermedi e avanzati che cercano regolarità e meno errori."),
    dict(slug="adidas-metalbone-carbon-2026", nome="Metalbone Carbon 2026", pz="adidas-metalbone-carbon-2026", linea="Metalbone", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio 6K", telaio="Carbonio", tatto="medio-morbido", pvp=260, best=204.90, s=(8.5, 8, 9.5, 8, 8, 8.4)),
    dict(slug="adidas-metalbone-carbon-ctrl-2026", nome="Metalbone Carbon CTRL 2026", pz="adidas-metalbone-carbon-ctrl-2026", linea="Metalbone", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio 6K", telaio="Carbonio", tatto="medio-morbido", pvp=260, best=204.90, s=(7, 8.5, 9.5, 9, 8.5, 8.5)),
    dict(slug="adidas-metalbone-team-2026", nome="Metalbone Team 2026", pz="adidas-metalbone-team-2026", linea="Metalbone", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=200, best=152.74, s=(8, 8, 8.5, 8, 8, 8.1)),
    dict(slug="adidas-metalbone-team-light-2026", nome="Metalbone Team Light 2026", pz="adidas-metalbone-team-light-2026", linea="Metalbone", forma="rotonda", peso="345–360 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=200, best=152.74, s=(7, 8.5, 8.5, 8.5, 8.5, 8.2)),
    dict(slug="adidas-metalbone-superlight-2026", nome="Metalbone Superlight 2026", pz="adidas-metalbone-superlight-2026", linea="Metalbone", forma="goccia", peso="345–360 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=150, best=127.95, s=(7, 7.5, 8.5, 8, 8, 7.8)),
    dict(slug="adidas-arrow-hit-2026", nome="Arrow Hit 2026", pz="adidas-arrow-hit-2026", linea="Arrow Hit", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio ASC (adidas Signature Carbon)", telaio="Carbonio", tatto="medio", pvp=400, best=399.90, s=(8.5, 8.5, 9, 8, 8.5, 8.5)),
    dict(slug="adidas-arrow-hit-ctrl-2026", nome="Arrow Hit CTRL 2026", pz="adidas-arrow-hit-ctrl-2026", linea="Arrow Hit", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio ASC (adidas Signature Carbon)", telaio="Carbonio", tatto="medio", pvp=400, best=399.90, s=(7.5, 9, 9, 8.5, 9, 8.6)),
    dict(slug="adidas-arrow-hit-light-2026", nome="Arrow Hit Light 2026", pz=None, linea="Arrow Hit", forma="diamante", peso="350–360 g", gomma="EVA Soft Performance", plano="Carbonio", telaio="Carbonio", tatto="medio", pvp=300, best=None, s=None, giocatore="Ari Sánchez", bil="alto",
         fonte_extra=("Padel Deals", "https://padeldeals.co.za/products/2026-adidas-arrow-hit-light")),
    dict(slug="adidas-arrow-hit-carbon-2026", nome="Arrow Hit Carbon 2026", pz="adidas-arrow-hit-carbon-2026", linea="Arrow Hit", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio ASC (adidas Signature Carbon)", telaio="Carbonio", tatto="medio", pvp=270, best=199.90, s=(7.5, 8, 8.5, 8, 8.5, 8.1)),
    dict(slug="adidas-arrow-hit-carbon-ctrl-2026", nome="Arrow Hit Carbon CTRL 2026", pz="adidas-arrow-hit-carbon-ctrl-2026", linea="Arrow Hit", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio ASC (adidas Signature Carbon)", telaio="Carbonio", tatto="medio", pvp=270, best=199.90, s=(7, 8.5, 8.5, 8.5, 9, 8.3)),
    dict(slug="adidas-cross-it-light-2026", nome="Cross It Light 2026", pz="adidas-cross-it-light-2026-martita-ortega", linea="Cross It", forma="rotonda", peso="345–360 g", gomma="EVA Soft Energy", plano="Carbonio alluminizzato 24K", telaio="Carbonio", tatto="medio", pvp=300, best=299.95, s=(6, 8.5, 9.5, 9.5, 9, 8.5), giocatore="Martita Ortega",
         analisi="Per PadelZoom è una racchetta di controllo e costruzione del punto: maneggevolezza molto alta (9,5/10), uscita di palla alta e sweet spot ampio. La potenza è volutamente limitata (6/10), quindi non è la scelta giusta per chi vuole chiudere i punti di smash. Indicata per intermedi e avanzati che mettono regolarità e piazzamento davanti al colpo vincente."),
    dict(slug="adidas-cross-it-ctrl-2026", nome="Cross It CTRL 2026", pz="adidas-cross-it-ctrl-2026", linea="Cross It", forma="rotonda", peso="360–375 g", gomma="EVA High Memory", plano="Carbonio alluminizzato 15K", telaio="Carbonio", tatto="medio-duro", pvp=350, best=297.95, s=(7.5, 9, 8.5, 9, 9, 8.6)),
    dict(slug="adidas-cross-it-carbon-2026", nome="Cross It Carbon 2026", pz="adidas-cross-it-carbon-2026", linea="Cross It", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio 6K", telaio="Carbonio", tatto="medio", pvp=280, best=213.83, s=(8.5, 8, 9, 8, 8, 8.3)),
    dict(slug="adidas-cross-it-carbon-ctrl-2026", nome="Cross It Carbon CTRL 2026", pz="adidas-cross-it-carbon-ctrl-2026", linea="Cross It", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Carbonio 6K", telaio="Carbonio", tatto="medio", pvp=280, best=237.95, s=(7, 8, 9, 9, 8.5, 8.3)),
    dict(slug="adidas-cross-it-team-ctrl-2026", nome="Cross It Team CTRL 2026", pz="adidas-cross-it-team-ctrl-2026", linea="Cross It", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=180, best=152.95, s=(7, 7, 8, 8, 8, 7.6)),
    dict(slug="adidas-cross-it-team-light-2026", nome="Cross It Team Light 2026", pz="adidas-cross-it-team-light-2026", linea="Cross It", forma="rotonda", peso="345–360 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=180, best=159.90, s=(6.5, 7, 8, 9, 8, 7.7)),
    dict(slug="adidas-rx-series-2026", nome="RX Series 2026", pz="adidas-rx-series-2026", linea="RX Series", forma="goccia", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=120, best=107.90, s=(7, 7, 7.5, 7, 7, 7.1)),
    dict(slug="adidas-rx-series-light-2026", nome="RX Series Light 2026", pz="adidas-rx-series-light-2026", linea="RX Series", forma="goccia", peso="310–330 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Carbonio", tatto="medio-morbido", pvp=120, best=119.90, s=(6.5, 7, 7.5, 7.5, 7, 7.1)),
    dict(slug="adidas-drive-light-2026", nome="Drive Light 2026", pz="adidas-drive-light-2026", linea="Drive", forma="rotonda", peso="345–360 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=80, best=67.95, s=(5.5, 6, 5.5, 7.5, 5.5, 6.0)),
    dict(slug="adidas-drive-black-2026", nome="Drive Black 2026", pz="adidas-drive-black-2026", linea="Drive", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=80, best=67.95, s=(6, 6, 5.5, 7, 5.5, 6.0), gemella="adidas-drive-blue-2026"),
    dict(slug="adidas-drive-blue-2026", nome="Drive Blue 2026", pz="adidas-drive-blue-2026", linea="Drive", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=80, best=67.95, s=(6, 6, 5.5, 7, 5.5, 6.0), gemella="adidas-drive-black-2026"),
    dict(slug="adidas-match-black-2026", nome="Match Black 2026", pz="adidas-match-black-2026", linea="Match", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=75, best=63.95, s=(6, 6.5, 5.5, 7, 5, 6.0), gemella="adidas-match-black-lime-2026"),
    dict(slug="adidas-match-black-lime-2026", nome="Match Black Lime 2026", pz="adidas-match-black-lime-2026", linea="Match", forma="diamante", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=75, best=63.95, s=(6, 6.5, 5.5, 7, 5, 6.0), gemella="adidas-match-black-2026"),
    dict(slug="adidas-match-light-2026", nome="Match Light 2026", pz="adidas-match-light-2026", linea="Match", forma="diamante", peso="345–360 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="medio-morbido", pvp=75, best=63.95, s=(6, 6.5, 5.5, 7, 5, 6.0)),
    dict(slug="adidas-world-cup-2026", nome="World Cup 2026", pz=None, linea="World Cup", forma="rotonda", peso="360–375 g", gomma="EVA Soft Performance", plano="Fibra di vetro", telaio="Fibra di vetro", tatto="morbido", pvp=160, best=74.90, s=None, bil="basso",
         fonte_extra=("Tennis Warehouse Europe", "https://www.tenniswarehouse-europe.com/adidas_USA_World_Cup_2026__Padel_Racket/descpageRC-APRUSAWC26-EN.html")),
]

FORMA_IT = {"diamante": "Diamante", "rotonda": "Rotonda", "goccia": "Goccia"}
LINEA_TXT = {
    "Metalbone": "la linea della potenza di Adidas, quella di Ale Galán",
    "Arrow Hit": "la linea con il carbonio ASC (adidas Signature Carbon) e i pesi regolabili sul telaio",
    "Cross It": "la linea del controllo di Adidas, quella di Martita Ortega",
    "RX Series": "la linea d'ingresso di Adidas per chi inizia a giocare con regolarità",
    "Drive": "la linea economica di Adidas per chi inizia",
    "Match": "la linea economica di Adidas per chi inizia",
    "World Cup": "un'edizione da collezione per i Mondiali 2026",
}
VOCI = ["Potenza", "Controllo", "Uscita di palla", "Maneggevolezza", "Sweet spot"]


def euro(x):
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s[:-3] if s.endswith(",00") else s


def num(v):
    return f"{v:g}".replace(".", ",")


def lc(t):
    return t[0].lower() + t[1:]


def livello(r):
    if r["telaio"] == "Fibra di vetro":
        return "principiante"
    if r["plano"] == "Fibra di vetro":
        return "principiante-intermedio"
    if "16K" in r["plano"] or "24K" in r["plano"] or "15K" in r["plano"] or r["pvp"] >= 300:
        return "avanzato"
    return "intermedio-avanzato"


LIV_TXT = {
    "principiante": "Principiante",
    "principiante-intermedio": "Principiante / intermedio",
    "intermedio-avanzato": "Intermedio / avanzato",
    "avanzato": "Intermedio alto / avanzato",
}


def ruolo(r):
    if r["forma"] == "diamante":
        return "attacco"
    if r["forma"] == "rotonda":
        return "controllo"
    return "polivalente"


def sim_score(a, b):
    sc = 0
    if a["forma"] == b["forma"]:
        sc += 3
    if livello(a) == livello(b):
        sc += 3
    if a["linea"] == b["linea"]:
        sc += 2
    sc -= abs(a["pvp"] - b["pvp"]) / 100
    return sc


def simili(r):
    out = []
    others = [o for o in R if o["slug"] != r["slug"]]
    if r.get("gemella"):
        g = next(o for o in R if o["slug"] == r["gemella"])
        out.append(g)
    ranked = sorted(others, key=lambda o: -sim_score(r, o))
    for o in ranked:
        if o not in out:
            out.append(o)
        if len(out) == 3:
            break
    cards = []
    for o in out:
        if o.get("gemella") == r["slug"]:
            testo = "Stessa racchetta, cambia solo il colore."
        else:
            diff = []
            if o["forma"] != r["forma"]:
                diff.append(f"forma {o['forma']}")
            if o["plano"] != r["plano"]:
                diff.append(f"superficie in {lc(o['plano'])}")
            if o["peso"] != r["peso"]:
                diff.append(o["peso"].split(" (")[0])
            if o["gomma"] != r["gomma"]:
                diff.append(f"gomma {o['gomma']}")
            if o["tatto"] != r["tatto"]:
                diff.append(f"tatto {o['tatto']}")
            if o["linea"] != r["linea"]:
                diff.append(f"linea {o['linea']}")
            if diff:
                testo = "Differenze: " + ", ".join(diff) + ". "
            elif o["s"] and r["s"]:
                dd = [(n, b - a) for n, a, b in zip(VOCI, r["s"][:5], o["s"][:5])]
                piu = max(dd, key=lambda x: x[1]); meno = min(dd, key=lambda x: x[1])
                testo = "Specifiche dichiarate uguali"
                if piu[1] > 0:
                    testo += f"; per PadelZoom ha più {piu[0].lower()}"
                if meno[1] < 0:
                    testo += f" e meno {meno[0].lower()}"
                testo += ". "
            else:
                testo = ""
            testo += f"Listino {euro(o['pvp'])} €."
        cards.append({"url": f"/racchette/{o['slug']}/", "sopra": "Adidas · 2026", "nome": o["nome"], "testo": testo})
    return cards, [o["slug"] for o in out]


def pro_contro(r):
    if not r["s"]:
        return None, None
    vals = dict(zip(VOCI, r["s"][:5]))
    top = sorted(vals.items(), key=lambda kv: -kv[1])
    low = sorted(vals.items(), key=lambda kv: kv[1])
    pro, contro = [], []
    frasi_pro = {
        "Potenza": "Potenza alta nei colpi d'attacco",
        "Controllo": "Buon controllo e precisione",
        "Uscita di palla": "Uscita di palla alta: aiuta in difesa",
        "Maneggevolezza": "Facile e veloce da maneggiare",
        "Sweet spot": "Sweet spot ampio e tollerante",
    }
    frasi_contro = {
        "Potenza": "Poca potenza per chi vuole chiudere di smash",
        "Controllo": "Controllo non tra i migliori della gamma",
        "Uscita di palla": "Uscita di palla contenuta: in difesa va accompagnato il colpo",
        "Maneggevolezza": "Non tra le più maneggevoli",
        "Sweet spot": "Sweet spot ridotto: i colpi fuori centro si sentono",
    }
    for k, v in top[:2]:
        if v >= 8:
            pro.append(f"{frasi_pro[k]} ({num(v)}/10 per PadelZoom)")
    for k, v in low[:2]:
        if v <= 7.5:
            contro.append(f"{frasi_contro[k]} ({num(v)}/10)")
    return pro, contro


def costruisci(r):
    nome_full = f"Adidas {r['nome']}"
    liv = livello(r)
    ru = ruolo(r)
    forma = FORMA_IT[r["forma"]]
    peso_breve = r["peso"].split(" (")[0]
    gioc = r.get("giocatore")
    pz_url = PZ + r["pz"] + "/" if r["pz"] else None
    chips = [forma, peso_breve, r["plano"].replace("Carbonio alluminizzato", "Carbonio"), f"Tatto {r['tatto']}"]
    if gioc:
        chips.append(f"Racchetta di {gioc}")
    else:
        chips.append(LIV_TXT[liv])

    # lead
    ru_txt = {"attacco": "pensata per attaccare", "controllo": "pensata per il controllo e la regolarità", "polivalente": "polivalente"}[ru]
    fa = {"diamante": "a diamante", "rotonda": "rotonda", "goccia": "a goccia"}[r["forma"]]
    lead = f"Racchetta {fa} {ru_txt}, della linea {r['linea']}: {LINEA_TXT[r['linea']]}."
    if liv == "principiante":
        lead += " Interamente in fibra di vetro e con tatto morbido: economica, tollerante e adatta a chi inizia."
    elif liv == "principiante-intermedio":
        lead += " Superficie in fibra di vetro e telaio in carbonio: un buon compromesso tra comfort, prezzo e prestazioni per chi sta crescendo."
    elif liv == "intermedio-avanzato":
        lead += f" Superficie in {lc(r['plano'])} e telaio in carbonio, per giocatori che hanno già una buona base tecnica."
    else:
        lead += f" Materiali di fascia alta ({lc(r['plano'])}) per giocatori esperti."
    if r["slug"] == "adidas-world-cup-2026":
        lead = "L'edizione da collezione di Adidas per i Mondiali 2026: una bandiera nazionale su una faccia e il logo del Mondiale sull'altra. Sotto la grafica c'è una racchetta rotonda, morbida e tollerante, pensata per principianti e giocatori in crescita."
    if r.get("gemella"):
        g = next(o for o in R if o["slug"] == r["gemella"])
        lead += f" È la stessa racchetta della {g['nome'].replace(' 2026', '')}: cambia solo il colore."

    # specifiche
    spec = [["Marca", "Adidas"], ["Modello", r["nome"]], ["Linea", r["linea"]]]
    if gioc:
        spec.append(["Giocatore", gioc])
    spec += [["Peso", r["peso"]], ["Forma", forma]]
    if r.get("bil"):
        spec.append(["Bilanciamento", r["bil"].capitalize()])
    spec += [["Gomma", r["gomma"]], ["Superficie", r["plano"]], ["Telaio", r["telaio"]], ["Tatto", r["tatto"].capitalize()], ["Livello consigliato", LIV_TXT[liv]]]
    if r.get("wb"):
        spec.append(["Personalizzazione", "Weight & Balance: fino a 11,2 g aggiuntivi sul telaio"])
    if r["linea"] == "Arrow Hit" and r["slug"] != "adidas-arrow-hit-light-2026":
        spec.append(["Tecnologie di linea", "Carbonio ASC; IBS (Intelligent Balance System) dichiarato per la famiglia Arrow Hit"])
    if r["slug"] == "adidas-world-cup-2026":
        spec.append(["Edizioni", "Argentina, Belgio, Colombia, Inghilterra, Italia, Messico, Paesi Bassi, Spagna, USA e Multination"])

    if pz_url:
        nota_spec = f'Dati dalla scheda di <a href="{pz_url}" rel="nofollow noopener" target="_blank">PadelZoom</a>; livello consigliato stimato da PadelMetrix in base a materiali e tatto.'
    else:
        fn, fu = r["fonte_extra"]
        nota_spec = f'Dati da <a href="{fu}" rel="nofollow noopener" target="_blank">{fn}</a>; livello consigliato stimato da PadelMetrix in base a materiali e tatto.'
    if r["slug"] == "adidas-world-cup-2026":
        nota_spec = f'Dati da <a href="{r["fonte_extra"][1]}" rel="nofollow noopener" target="_blank">Tennis Warehouse Europe</a> (edizione USA), che la indica per principianti e intermedi.'

    # valutazioni
    if r["s"]:
        val = {
            "titolo": "Valutazioni PadelZoom",
            "scala": 10,
            "voci": [{"nome": n, "valore": v} for n, v in zip(VOCI, r["s"][:5])],
            "nota_html": f'Punteggi su 10 di <a href="{pz_url}" rel="nofollow noopener" target="_blank">PadelZoom</a>, voto complessivo {num(r["s"][5])}/10. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.',
        }
        tratti = None
    else:
        val = None
        if r["slug"] == "adidas-world-cup-2026":
            voci = ["Comfort", "Tolleranza", "Controllo", "Edizione da collezione"]
        else:
            voci = ["Potenza", "Maneggevolezza", "Comfort", "Gioco a rete"]
        tratti = {"titolo": "Punti chiave dichiarati", "voci": voci, "nota_html": "Non abbiamo ancora trovato test indipendenti con punteggi numerici per questa racchetta. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione."}

    # sintesi
    if r.get("analisi"):
        sintesi = r["analisi"]
    elif r["s"]:
        vals = dict(zip(VOCI, r["s"][:5]))
        top = sorted(vals.items(), key=lambda kv: -kv[1])
        low = min(vals.items(), key=lambda kv: kv[1])
        sintesi = (f"PadelZoom le assegna {num(r['s'][5])}/10 complessivo, ma senza un'analisi scritta: per ora ci sono solo i punteggi. "
                   f"I valori più alti sono {top[0][0].lower()} ({num(top[0][1])}) e {top[1][0].lower()} ({num(top[1][1])}), il più basso è {low[0].lower()} ({num(low[1])}). ")
        if liv == "principiante":
            sintesi += "Sono punteggi da racchetta d'ingresso: va giudicata per quello che è, una racchetta economica per iniziare, non per competere."
        elif ru == "attacco":
            sintesi += "È un profilo da racchetta d'attacco, coerente con la forma a diamante."
        elif ru == "controllo":
            sintesi += "È un profilo da racchetta di controllo, coerente con la forma rotonda."
        else:
            sintesi += "È un profilo equilibrato, coerente con la forma a goccia."
    elif r["slug"] == "adidas-arrow-hit-light-2026":
        sintesi = "Non abbiamo ancora trovato recensioni indipendenti complete: le aggiungeremo appena disponibili. I rivenditori la descrivono come la versione leggera della Arrow Hit, scelta da Ari Sánchez: diamante con bilanciamento alto per attaccare e dominare la rete, ma più maneggevole e confortevole grazie al peso contenuto e alla gomma morbida."
    else:
        sintesi = "Non esistono test indipendenti con punteggi per questa edizione. Tennis Warehouse Europe la descrive come una racchetta morbida e tollerante, con bilanciamento basso e telaio e superficie in fibra di vetro: punta su controllo e comfort, non sulla potenza. È soprattutto un oggetto da collezione per chi tifa una nazionale."

    pro, contro = pro_contro(r)
    if pro is None:
        if r["slug"] == "adidas-world-cup-2026":
            pro, contro = ["Morbida e tollerante, adatta a chi inizia", "Bilanciamento basso: facile da muovere", "Grafica da collezione con la propria nazionale", "Spesso scontata (da circa 75 €)"], ["Poca potenza", "Materiali da principiante: si cresce in fretta oltre questa racchetta"]
        else:
            pro, contro = ["Diamante leggera: più maneggevole delle Arrow Hit standard", "Bilanciamento alto per attaccare", "Gomma morbida per più comfort"], ["Pochi test indipendenti disponibili", "Per giocatori avanzati"]
    EXTRA_CONTRO = {
        "adidas-metalbone-hrd-plus-2026": ["Uscita di palla moderata: in difesa va accompagnato il colpo", "Sweet spot più piccolo delle racchette meno rigide"],
        "adidas-metalbone-2026": ["Maneggevolezza nella media: chiede una buona preparazione del colpo", "Meno rigida della HRD+ per chi colpisce fortissimo"],
        "adidas-metalbone-ctrl-2026": ["Potenza limitata rispetto alle Metalbone a diamante"],
    }
    contro = EXTRA_CONTRO.get(r["slug"], []) + contro
    # pro/contro di specifica
    if r.get("wb"):
        pro.append("Peso e bilanciamento regolabili (Weight & Balance)")
    if r["telaio"] == "Fibra di vetro" and r["slug"] != "adidas-world-cup-2026":
        pro.append(f"Prezzo basso (listino {euro(r['pvp'])} €)")
        contro.append("Materiali semplici: limitante quando il livello cresce")
    if r["pvp"] >= 350:
        contro.append(f"Prezzo di listino alto ({euro(r['pvp'])} €)")
    if r.get("gemella"):
        pro.append("Disponibile in due colori")
    if not contro:
        contro.append("Nessun punto debole netto nei punteggi: è una racchetta equilibrata")

    adatta, non_adatta = [], []
    if liv == "principiante":
        adatta = ["Hai appena iniziato a giocare", "Cerchi una racchetta economica e tollerante", "Giochi una o due volte a settimana per divertimento"]
        non_adatta = ["Giochi già con regolarità e vuoi migliorare: guarda la Metalbone Team o la Cross It Team", "Cerchi potenza vera nello smash"]
    elif liv == "principiante-intermedio":
        adatta = ["Stai passando dal livello principiante a quello intermedio", "Vuoi comfort senza spendere troppo"]
        non_adatta = ["Hai un livello avanzato: guarda le versioni Carbon o le top di gamma"]
    elif liv == "intermedio-avanzato":
        adatta = ["Hai una buona base tecnica e giochi con regolarità", "Vuoi materiali in carbonio senza arrivare ai prezzi delle top di gamma"]
        non_adatta = ["Sei principiante: meglio una versione Team", "Vuoi il massimo delle prestazioni: guarda le top di gamma della stessa linea"]
    else:
        adatta = ["Hai un livello intermedio alto o avanzato", "Cerchi una racchetta di fascia alta"]
        non_adatta = ["Sei principiante: costa molto e non sfrutteresti le sue qualità"]
    if ru == "attacco":
        adatta.append("Ti piace attaccare e chiudere il punto")
        non_adatta.append("Giochi soprattutto in difesa: meglio una rotonda")
    elif ru == "controllo":
        adatta.append("Costruisci il punto con pazienza e precisione")
        non_adatta.append("Cerchi soprattutto potenza: meglio una diamante")
    else:
        adatta.append("Vuoi un compromesso tra attacco e controllo")

    rec = []
    if r["s"]:
        rec.append({"fonte": "PadelZoom", "url": pz_url, "voto": f"{num(r['s'][5])}/10",
                    "voto_dettaglio": f"potenza {num(r['s'][0])} · controllo {num(r['s'][1])}",
                    "sintesi": ("Con analisi scritta, riassunta sopra. " if r.get("analisi") else "Solo punteggi, senza analisi scritta. ") + f"Uscita di palla {num(r['s'][2])}, maneggevolezza {num(r['s'][3])}, sweet spot {num(r['s'][4])}."})

    cards, sim_slugs = simili(r)
    prezzo_txt = f"Sito ufficiale · listino {euro(r['pvp'])} €"
    nota_prezzi = f"Prezzo di listino rilevato il {DATA_TXT}."
    if r["best"] and r["best"] < r["pvp"] - 1:
        nota_prezzi += f" Presso i rivenditori si trova già da circa {euro(r['best'])} €."

    titolo_tag = f"{nome_full}: scheda tecnica e valutazioni"
    meta = f"{nome_full}: forma {r['forma']}, {peso_breve}, {lc(r['plano'])}, gomma {r['gomma']}, tatto {r['tatto']}. Dati tecnici, valutazioni e alternative."
    eyebrow = f"Adidas · Collezione 2026 · {r['linea']}"

    d = {
        "slug": r["slug"], "marca": "Adidas", "modello": r["nome"].replace(" 2026", ""), "anno": 2026, "linea": r["linea"],
        "categoria": "adulto", "forma": r["forma"], "peso": r["peso"], "gomma": r["gomma"], "superficie": r["plano"],
        "telaio": r["telaio"], "sensazione": r["tatto"], "livello": liv, "stile": ru, "prezzo_listino_eur": r["pvp"],
        "prezzo_listino_data": DATA_OGGI, "simili": sim_slugs,
        "fonti_dati": [u for u in [pz_url, r.get("fonte_extra", (None, None))[1]] if u],
        "aggiornato": DATA_OGGI,
    }
    if gioc:
        d["giocatore"] = gioc
    if r["s"]:
        d["valutazioni_padelzoom"] = dict(zip(["potenza", "controllo", "uscita_palla", "maneggevolezza", "sweet_spot", "globale"], r["s"]))
    d["pagina"] = {
        "titolo": nome_full, "title_tag": titolo_tag, "meta_description": meta, "breadcrumb": r["nome"],
        "eyebrow": eyebrow, "chips": chips, "lead": lead,
        "negozi": [
            {"nome": "Amazon", "nota": "Spedizione e resi Amazon", "url": "https://www.amazon.it/s?k=" + ("Adidas " + r["nome"]).replace(" ", "+"), "pulsante": "Vedi su Amazon", "amazon": True},
            {"nome": "Adidas Padel", "nota": prezzo_txt, "url": "https://allforpadel.com/en/", "pulsante": "Vedi sul sito"},
        ],
        "nota_prezzi": nota_prezzi,
        "confronta": {"url": f"/confronta/?r={r['slug']},{sim_slugs[0]}", "testo": f"Confronta con la {next(o for o in R if o['slug']==sim_slugs[0])['nome'].replace(' 2026','')}"},
        "specifiche": spec, "nota_specifiche_html": nota_spec, "sintesi": sintesi,
        "pro": pro, "contro": contro, "adatta": adatta, "non_adatta": non_adatta,
        "recensioni": rec, "simili": cards, "aggiornata": DATA_TXT,
    }
    if val:
        d["pagina"]["valutazioni"] = val
    else:
        d["pagina"]["tratti"] = tratti
    return d


for r in R:
    d = costruisci(r)
    (OUT / f"{r['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(R), "file scritti")
