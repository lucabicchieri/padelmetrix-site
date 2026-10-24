#!/usr/bin/env python3
"""Crea i JSON delle racchette del lotto di ottobre 2026 a partire da scripts/dati_lotto/*.py.

Ogni file di dati espone R (lista di racchette) e facoltativamente UPD (correzioni).
Campi brevi: m marca, n modello, a anno, g giocatore, f forma, fn nota forma, p peso, b bilanciamento,
nu nucleo, c superficie, t telaio, ta tatto, l livello, st stile, pr prezzo di listino, d descrizione
dalla fonte, src [(nome, url)], sc punteggi esterni, meas (durezza, swingweight misurati),
pot potenza dichiarata su 10, colori, donna, categoria, simili_fissi.

Regole: nessun punteggio inventato; ogni dato viene dalle fonti elencate; dove manca si dice.
"""
import importlib.util
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATI = ROOT / "scripts" / "dati_lotto"
OUT = ROOT / "data" / "racchette"
OGGI = "2026-10-24"
OGGI_TXT = "24 ottobre 2026"

FORMA_IT = {"diamante": "Diamante", "rotonda": "Rotonda", "goccia": "Goccia", "ibrida": "Ibrida"}
LIV_IT = {
    "principiante": "Principiante", "principiante-intermedio": "Principiante / intermedio",
    "intermedio": "Intermedio", "intermedio-avanzato": "Intermedio / avanzato",
    "avanzato": "Avanzato", "professionale": "Avanzato / professionale",
}
LIV_FRASE = {
    "principiante": "chi inizia", "principiante-intermedio": "principianti e intermedi",
    "intermedio": "giocatori intermedi", "intermedio-avanzato": "intermedi alti e avanzati",
    "avanzato": "giocatori avanzati", "professionale": "giocatori avanzati e agonisti",
}
STILE_IT = {"offensivo": "Offensivo", "controllo": "Controllo", "polivalente": "Polivalente"}
STILE_CHIP = {"offensivo": "Racchetta d'attacco", "controllo": "Racchetta di controllo", "polivalente": "Polivalente"}
VOCI = ["Potenza", "Controllo", "Uscita di palla", "Maneggevolezza", "Sweet spot"]
PRO_SC = ["Potenza nei colpi d'attacco", "Controllo e precisione", "Uscita di palla facile",
          "Maneggevole e veloce a rete", "Sweet spot ampio e tollerante"]
CONTRO_SC = ["Potenza limitata nello smash", "Controllo meno preciso della media",
             "Uscita di palla contenuta: in difesa va accompagnata", "Meno maneggevole negli scambi veloci",
             "Sweet spot ridotto: serve un impatto pulito"]
LIV_ORD = ["principiante", "principiante-intermedio", "intermedio", "intermedio-avanzato", "avanzato", "professionale"]
NEGOZI = {"PadelMarket", "PadelPROShop", "Padelshop", "Ipontennis", "Tennis Warehouse", "Tennis Warehouse Europe",
          "Tecnifibre", "Merchant of Tennis", "Padelkiwi", "Padel Gear", "Padelgids", "Tennis Nuts",
          "Racket Central", "Total Padel", "Padel Deals"}


def slugify(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower().replace("+", " plus")
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def euro(x):
    s = f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return s[:-3] if s.endswith(",00") else s


def num(v):
    return f"{v:g}".replace(".", ",")


def a_link(nome, url):
    return f'<a href="{url}" rel="nofollow noopener" target="_blank">{nome}</a>'


def carica():
    rs, upd = [], {}
    for f in sorted(DATI.glob("*.py")):
        spec = importlib.util.spec_from_file_location(f.stem, f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rs += mod.R
        upd.update(getattr(mod, "UPD", {}))
    for r in rs:
        k = (r["m"], r["n"], r["a"])
        if k in upd:
            u = dict(upd[k])
            add = u.pop("src_add", [])
            if "d" in u and add:
                r["d_src"] = add[0][0]
            r.update(u)
            r["src"] = r["src"] + [s for s in add if s not in r["src"]]
        r["slug"] = slugify(f"{r['m']} {r['n']} {r['a']}")
        r.setdefault("categoria", "adulto")
    return rs


def esistenti():
    out = []
    for f in sorted(OUT.glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        st = (d.get("stile") or "").lower()
        st = "offensivo" if any(w in st for w in ("attacco", "offens", "potenza")) else ("controllo" if "controllo" in st else "polivalente")
        out.append(dict(slug=d["slug"], m=d["marca"], n=d["modello"], a=d["anno"], f=d.get("forma"), l=d.get("livello"),
                        st=st, pr=d.get("prezzo_listino_eur"), categoria=d.get("categoria", "adulto"), esistente=True,
                        titolo=d["pagina"]["titolo"], c=d.get("superficie") or d.get("plano"),
                        p=d.get("peso") if isinstance(d.get("peso"), str) else (f"{d['peso_g'][0]}–{d['peso_g'][1]} g" if isinstance(d.get("peso_g"), list) else None)))
    return out


def peso_txt(r):
    return r.get("p")


def pot_sc(r):
    return r["sc"]["v"] if r.get("sc") else None


def sim_score(a, b):
    if a["categoria"] != b["categoria"]:
        return -99
    sc = 0
    if a.get("f") and a.get("f") == b.get("f"):
        sc += 3
    if a.get("l") and b.get("l"):
        da = abs(LIV_ORD.index(a["l"]) - LIV_ORD.index(b["l"])) if a["l"] in LIV_ORD and b["l"] in LIV_ORD else 3
        sc += max(0, 3 - 1.5 * da)
    if a.get("st") == b.get("st"):
        sc += 2
    if a["m"] == b["m"]:
        sc += 0.5
    if a.get("pr") and b.get("pr"):
        sc -= abs(a["pr"] - b["pr"]) / 120
    if bool(a.get("donna")) != bool(b.get("donna")):
        sc -= 0.5
    return sc


def testo_simile(r, o):
    if o["m"] == r["m"] and o["n"] == r["n"]:
        return f"La versione {o['a']} dello stesso modello." if o["a"] != r["a"] else "Stessa racchetta."
    STL = {"offensivo": "d'attacco", "controllo": "di controllo", "polivalente": "polivalente"}
    testa = FORMA_IT.get(o.get("f"), "Racchetta") if o.get("f") else "Racchetta"
    if o.get("st"):
        testa += " " + STL[o["st"]]
    parti = [testa]
    if o.get("p"):
        parti.append(o["p"])
    mk = re.search(r"(\d+)K", o.get("c") or "")
    if mk:
        parti.append(f"carbonio {mk.group(1)}K")
    elif "vetro" in (o.get("c") or "").lower():
        parti.append("fibra di vetro")
    if o.get("l") in LIV_IT:
        parti.append("livello " + LIV_IT[o["l"]].lower())
    if o.get("pr") and r.get("pr") and abs(o["pr"] - r["pr"]) >= 40:
        parti.append("listino più alto" if o["pr"] > r["pr"] else "listino più basso")
    return ", ".join(parti) + "."


def simili(r, tutti):
    scelti = []
    for s in r.get("simili_fissi", []):
        o = next((x for x in tutti if x["slug"] == s), None)
        if o:
            scelti.append(o)
    # stessa racchetta in un altro anno
    for o in tutti:
        if o["m"] == r["m"] and o["n"] == r["n"] and o["a"] != r["a"] and o not in scelti:
            scelti.append(o)
    altri = sorted((o for o in tutti if o["slug"] != r["slug"] and o not in scelti), key=lambda o: -sim_score(r, o))
    marche = {o["m"] for o in scelti}
    for o in altri:
        if len(scelti) >= 3:
            break
        if o["m"] in marche and len(marche) < 2 and any(x["m"] != r["m"] for x in altri[:10]):
            continue  # varietà: almeno una marca diversa
        scelti.append(o)
        marche.add(o["m"])
    out = []
    for o in scelti[:3]:
        nome = o.get("titolo", f"{o['m']} {o['n']} {o['a']}").replace(o["m"] + " ", "", 1)
        if str(o["a"]) not in nome:
            nome += f" {o['a']}"
        out.append({"url": f"/racchette/{o['slug']}/", "sopra": f"{o['m']} · {o['a']}", "nome": nome, "testo": testo_simile(r, o)})
    return out, scelti[:3]


def lc_inizio(t, r):
    w = t.split(" ")[0]
    propri = set((r["m"] + " " + r["n"] + " " + (r.get("g") or "")).split())
    if w in propri or w.isupper():
        return t
    return t[0].lower() + t[1:]


def pro_contro(r):
    pro, contro = [], []
    v = pot_sc(r)
    f, st, l, ta = r.get("f"), r.get("st"), r.get("l"), (r.get("ta") or "")
    c = r.get("c") or ""
    if v:
        for i in sorted(range(5), key=lambda i: -v[i]):
            if v[i] >= 8.5 and len(pro) < 2:
                pro.append(PRO_SC[i])
        for i in sorted(range(5), key=lambda i: v[i]):
            if v[i] <= 7.5 and len(contro) < 2:
                contro.append(CONTRO_SC[i])
    def add(lst, x):
        if x not in lst and len(lst) < 4:
            lst.append(x)
    if st == "offensivo":
        add(pro, "Pensata per chiudere i punti: smash e volée" if f == "diamante" else "Impronta offensiva con buona spinta")
    elif st == "controllo":
        add(pro, "Controllo e regolarità negli scambi")
    elif st == "polivalente":
        add(pro, "Versatile tra difesa e attacco")
    if "morbid" in ta:
        add(pro, "Tatto morbido, più comfort per il braccio")
    elif "dur" in ta or "secc" in ta or "ferm" in ta:
        add(pro, "Risposta secca e precisa all'impatto")
    m = re.search(r"(\d+)K", c)
    if m and int(m.group(1)) >= 12:
        add(pro, f"Superficie in carbonio {m.group(1)}K")
    elif "vetro" in c.lower():
        add(pro, "Fibra di vetro: tatto morbido e uscita di palla facile")
    pnum = re.findall(r"\d{3}", r.get("p") or "")
    if pnum and int(pnum[0]) <= 345 and r["categoria"] != "junior":
        add(pro, "Leggera e facile da muovere")
    if r.get("g") and "ispirata" not in r["g"]:
        add(pro, f"Il modello di {r['g']}")
    # limiti
    b = r.get("b") or ""
    if f == "diamante" and "alto" in b:
        add(contro, "Bilanciamento alto: più impegnativa in difesa")
    if ta == "duro":
        add(contro, "Rigida: può affaticare gomito e spalla")
    elif "dur" in ta:
        add(contro, "Tatto medio-duro: meno comfort di una racchetta morbida")
    if st == "controllo" and not any("Potenza" in x for x in contro):
        add(contro, "Poca potenza facile nello smash")
    if l in ("avanzato", "professionale"):
        add(contro, "Esigente per chi non ha ancora una tecnica solida")
    if l in ("principiante", "principiante-intermedio") and r["categoria"] != "junior":
        add(contro, "Si rischia di superarla presto crescendo di livello")
    if r.get("pr") and r["pr"] >= 300:
        add(contro, "Prezzo di listino alto")
    if r["categoria"] == "junior":
        add(contro, "Da sostituire quando il ragazzo passa al peso adulto")
    if st == "offensivo" and "morbid" in ta:
        add(contro, "Meno esplosiva delle versioni più rigide")
    if len(contro) < 2:
        add(contro, "Recensioni indipendenti ancora poche")
    if len(contro) < 2:
        add(contro, "Alcuni dati tecnici non sono dichiarati dal produttore")
    if len(pro) < 2:
        add(pro, f"Collezione {r['a']} di {r['m']}")
    return pro[:4], contro[:4]


def adatta(r):
    l, st, f = r.get("l"), r.get("st"), r.get("f")
    a, n = [], []
    if r["categoria"] == "junior":
        a.append("Cerchi una racchetta più leggera e corta per un ragazzo")
        a.append("Il ragazzo sta imparando i colpi base" if l == "principiante" else "Il ragazzo gioca già con regolarità")
        n.append("Il ragazzo ha già il fisico per una racchetta da adulto")
        n.append("Cerchi una racchetta da adulto leggera: guarda i modelli Light")
        return a, n
    if l:
        a.append(f"Sei {'un principiante' if l == 'principiante' else 'di livello ' + LIV_IT[l].lower()}")
    a.append({"offensivo": "Ti piace attaccare e chiudere i punti a rete", "controllo": "Costruisci il punto con pazienza e piazzamento",
              "polivalente": "Vuoi una racchetta sola per difesa e attacco"}.get(st, "Cerchi un modello recente di " + r["m"]))
    if "morbid" in (r.get("ta") or ""):
        a.append("Vuoi proteggere gomito e spalla")
    elif f == "diamante":
        a.append("Hai un buon tempismo nei colpi sopra la testa")
    elif f == "rotonda":
        a.append("Vuoi uno sweet spot centrato e tollerante")
    if l in ("avanzato", "professionale", "intermedio-avanzato"):
        n.append("Sei principiante: meglio una racchetta più tollerante")
    else:
        n.append("Sei avanzato e cerchi il massimo delle prestazioni")
    n.append({"offensivo": "Giochi soprattutto in difesa da fondo campo", "controllo": "Cerchi tanta potenza nello smash",
              "polivalente": "Cerchi una racchetta specializzata in attacco o in difesa"}.get(st, "Cerchi una racchetta con più recensioni"))
    if r.get("ta") == "duro":
        n.append("Hai fastidi a gomito o spalla")
    return a[:3], n[:3]


def build(r, tutti):
    titolo = f"{r['m']} {r['n']} {r['a']}"
    forma = r.get("f")
    forma_txt = FORMA_IT.get(forma, "") if forma else ""
    fonti = r["src"]
    fonti_nomi = []
    for nme, _ in fonti:
        if nme not in fonti_nomi:
            fonti_nomi.append(nme)
    liv = r.get("l")
    st = r.get("st")
    junior = r["categoria"] == "junior"

    chips = []
    if forma_txt:
        chips.append(forma_txt)
    if r.get("p"):
        chips.append(r["p"])
    if r.get("b"):
        chips.append("Bilanciamento " + r["b"].split(" (")[0])
    m = re.search(r"(\d+)K", r.get("c") or "")
    if m:
        chips.append(f"Carbonio {m.group(1)}K")
    elif "vetro" in (r.get("c") or "").lower():
        chips.append("Fibra di vetro")
    if liv:
        chips.append(LIV_IT[liv])
    if junior:
        chips.append("Junior")
    elif r.get("donna"):
        chips.append("Modello femminile")
    if r.get("g") and "ispirata" not in r["g"]:
        chips.append(f"Racchetta di {r['g']}")

    # meta description
    det = []
    if forma_txt:
        det.append(f"forma {forma_txt.lower()}")
    if r.get("p"):
        det.append(f"peso {r['p']}")
    if r.get("b"):
        det.append(f"bilanciamento {r['b'].split(' (')[0]}")
    if r.get("c"):
        c0 = r["c"].split(",")[0].split(" (")[0]
        det.append(c0[0].lower() + c0[1:] if c0.startswith(("Carbonio", "Fibra")) else c0)
    gtxt = f" ({r['g']})" if r.get("g") and "ispirata" not in r["g"] else ""
    meta = f"{titolo}{gtxt}: " + (", ".join(det) + ". " if det else "") + "Dati tecnici, a chi è adatta e racchette simili."
    if len(meta) > 160:
        meta = f"{titolo}{gtxt}: " + ", ".join(det[:3]) + ". Scheda tecnica e alternative."

    # lead
    lead = r["d"]
    if liv and LIV_FRASE[liv] not in lead:
        lead += f" Indicata per {LIV_FRASE[liv]}." if not junior else " Pensata per ragazzi."

    # avviso: altra versione dello stesso modello
    avviso = None
    altre = [o for o in tutti if o["m"] == r["m"] and o["n"] == r["n"] and o["a"] != r["a"]]
    if altre:
        o = altre[0]
        if o["a"] > r["a"]:
            avviso = f'<p>È uscita la versione {o["a"]}: <a href="/it/racchette/{o["slug"]}/">{r["m"]} {r["n"]} {o["a"]}</a>. Il modello {r["a"]} resta in vendita e spesso si trova scontato.</p>'
        else:
            avviso = f'<p>Questa è la nuova versione. Il <a href="/it/racchette/{o["slug"]}/">modello {o["a"]}</a> resta in vendita e spesso si trova scontato.</p>'

    # valutazioni / tratti
    valutazioni = tratti = None
    if r.get("sc"):
        sc = r["sc"]
        valutazioni = {
            "titolo": f"Valutazioni di {sc['fonte']}", "scala": 10,
            "voci": [{"nome": n, "valore": v} for n, v in zip(VOCI, sc["v"])],
            "nota_html": f"Punteggi su 10 pubblicati da {a_link(sc['fonte'], sc['url'])}, voto complessivo {num(sc['tot'])}/10. Il punteggio PadelMetrix arriverà con il nostro metodo di valutazione.",
        }
    else:
        voci = []
        if st:
            voci.append(STILE_CHIP[st])
        if liv:
            voci.append("Livello " + LIV_IT[liv].lower())
        if r.get("ta"):
            voci.append("Tatto " + r["ta"])
        if forma_txt:
            voci.append("Forma " + (r.get("fn") or forma_txt.lower()))
        if r.get("pot"):
            voci.append(f"Potenza {num(r['pot'])}/10 secondo {fonti[0][0]}")
        if r.get("meas"):
            voci.append(f"Durezza misurata {r['meas'][0]}")
        nota = "Caratteristiche dichiarate dal produttore e dai rivenditori. "
        if r.get("pot"):
            nota = "Caratteristiche e indice di potenza come pubblicati da " + a_link(fonti[0][0], fonti[0][1]) + ". "
        if r.get("meas"):
            nota += f"Durezza e swingweight misurati da {a_link('Padelshop', 'https://padelshop.com/collections/bullpadel-padel-rackets?page=3')}. "
        nota += "Valutazioni indipendenti in arrivo: il punteggio PadelMetrix arriverà con il nostro metodo di valutazione."
        tratti = {"titolo": "In sintesi", "voci": voci, "nota_html": nota}

    # negozi
    negozi = [{"nome": "Amazon", "nota": "Spedizione e resi Amazon", "url": "https://www.amazon.it/s?k=" + titolo.replace(" ", "+"),
               "pulsante": "Vedi su Amazon", "amazon": True}]
    for nme, u in fonti:
        if nme in NEGOZI:
            negozi.append({"nome": nme, "nota": "Scheda prodotto del rivenditore", "url": u, "pulsante": "Vedi sul sito"})
            break
    if r.get("pr"):
        nota_prezzi = f"Prezzo di listino indicativo {euro(r['pr'])} € secondo i rivenditori consultati a ottobre 2026; i prezzi reali cambiano spesso, verifica sul negozio."
    else:
        nota_prezzi = "Prezzo non ancora rilevato: verifica sul sito del negozio."

    # specifiche
    sp = [["Marca", r["m"]], ["Modello", r["n"]], ["Collezione", str(r["a"])]]
    if r.get("g"):
        sp.append(["Giocatore", r["g"]])
    if junior:
        sp.append(["Categoria", "Junior"])
    elif r.get("donna"):
        sp.append(["Categoria", "Modello femminile"])
    if r.get("fn") and r["fn"].startswith(forma_txt.lower()):
        ftxt = r["fn"][0].upper() + r["fn"][1:]
    else:
        ftxt = forma_txt + (f" ({r['fn']})" if r.get("fn") else "")
    sp.append(["Forma", ftxt if forma_txt else "Non dichiarata"])
    sp.append(["Peso", r.get("p") or "Non dichiarato"])
    sp.append(["Bilanciamento", (r["b"][0].upper() + r["b"][1:]) if r.get("b") else "Non dichiarato"])
    for k, lab in (("nu", "Nucleo"), ("c", "Superficie"), ("t", "Telaio")):
        if r.get(k):
            sp.append([lab, r[k][0].upper() + r[k][1:]])
    if r.get("ta"):
        sp.append(["Tatto", r["ta"][0].upper() + r["ta"][1:]])
    if liv:
        sp.append(["Livello", LIV_IT[liv]])
    if st:
        sp.append(["Stile di gioco", STILE_IT[st]])
    if r.get("meas"):
        sp.append(["Durezza misurata", str(r["meas"][0])])
        sp.append(["Swingweight misurato", str(r["meas"][1])])
    if r.get("pot"):
        sp.append([f"Indice di potenza ({fonti[0][0]})", f"{num(r['pot'])}/10"])
    if r.get("colori"):
        sp.append(["Colori", r["colori"]])
    if r.get("pr"):
        sp.append(["Prezzo di listino", f"{euro(r['pr'])} €"])
    nota_sp = "Dati raccolti da " + ", ".join(a_link(n, u) for n, u in fonti) + ". I campi \"non dichiarato\" non sono pubblicati dalle fonti consultate; li completeremo appena disponibili."

    # sintesi
    fonte_desc = r.get("d_src") or fonti[0][0]
    if r.get("sc"):
        v = r["sc"]["v"]
        best = max(range(5), key=lambda i: v[i])
        worst = min(range(5), key=lambda i: v[i])
        sintesi = (f"Per Padelful ottiene {num(r['sc']['tot'])}/10. In sintesi: {lc_inizio(r['d'], r)} "
                   f"Il valore più alto è {VOCI[best].lower()} ({num(v[best])}/10), il più basso {VOCI[worst].lower()} ({num(v[worst])}/10). "
                   "Le altre recensioni indipendenti sono ancora poche: aggiorneremo la scheda appena ne usciranno.")
    else:
        sintesi = (f"Le recensioni indipendenti di questo modello sono ancora poche. {fonte_desc} la descrive così: {lc_inizio(r['d'], r)} "
                   "Aggiorneremo la sintesi appena saranno disponibili test e recensioni.")
    pro, contro = pro_contro(r)
    ad, nad = adatta(r)

    rec = []
    if r.get("sc"):
        sc = r["sc"]
        rec.append({"fonte": sc["fonte"], "url": sc["url"], "voto": f"{num(sc['tot'])}/10",
                    "voto_dettaglio": f"potenza {num(sc['v'][0])} · controllo {num(sc['v'][1])}", "sintesi": r["d"]})

    sim, sim_objs = simili(r, tutti)
    conf = sim_objs[0]["slug"] if sim_objs else None

    eyebrow = f"{r['m']} · Collezione {r['a']}" + (" · Junior" if junior else (" · Donna" if r.get("donna") else ""))
    d = {
        "slug": r["slug"], "marca": r["m"], "modello": r["n"], "anno": r["a"],
        "giocatore": r.get("g"), "categoria": r["categoria"], "donna": bool(r.get("donna")),
        "peso": r.get("p"), "forma": forma, "forma_nota": r.get("fn"), "bilanciamento": r.get("b"),
        "nucleo": r.get("nu"), "superficie": r.get("c"), "telaio": r.get("t"), "sensazione": r.get("ta"),
        "livello": liv, "stile": st, "prezzo_listino_eur": r.get("pr"),
        "valutazioni_esterne": r.get("sc"), "misure": r.get("meas"), "potenza_dichiarata": r.get("pot"),
        "simili": [o["slug"] for o in sim_objs], "fonti_dati": [u for _, u in fonti], "aggiornato": OGGI,
        "pagina": {
            "titolo": titolo,
            "title_tag": f"{titolo}: scheda tecnica, caratteristiche e alternative",
            "meta_description": meta,
            "breadcrumb": f"{r['n']} {r['a']}",
            "eyebrow": eyebrow,
            "chips": chips,
            "lead": lead,
            "negozi": negozi,
            "nota_prezzi": nota_prezzi,
            "confronta": {"url": f"/confronta/?r={r['slug']},{conf}" if conf else f"/confronta/?r={r['slug']}",
                          "testo": f"Confronta con {sim[0]['nome']}" if sim else "Confronta con un'altra racchetta"},
            "specifiche": sp,
            "nota_specifiche_html": nota_sp,
            "sintesi": sintesi,
            "pro": pro, "contro": contro, "adatta": ad, "non_adatta": nad,
            "recensioni": rec,
            "simili": sim,
            "aggiornata": OGGI_TXT,
        },
    }
    if avviso:
        d["pagina"]["avviso_html"] = avviso
    if valutazioni:
        d["pagina"]["valutazioni"] = valutazioni
    else:
        d["pagina"]["tratti"] = tratti
    return {k: v for k, v in d.items() if v is not None}


def main():
    nuovi = carica()
    slugs_nuovi = {r["slug"] for r in nuovi}
    gia = [o for o in esistenti() if o["slug"] not in slugs_nuovi]
    tutti = nuovi + gia
    for r in nuovi:
        d = build(r, tutti)
        (OUT / f"{r['slug']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(nuovi), "racchette create")


if __name__ == "__main__":
    main()
