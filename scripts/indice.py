"""Quali pagine lasciare indicizzate su Google (strategia di ripresa, 26 novembre 2026).

Le pagine escluse restano online e raggiungibili, ma ricevono <meta name="robots" content="noindex, follow">
e non entrano in sitemap.xml. Regole (uguali per le 4 lingue):
- schede racchetta: 2026-2027 con dati completi o valutazioni esterne, oppure 2026-2027 con prodotto Amazon collegato,
  oppure che hanno già avuto impressioni su Google;
- confronti: stesso modello anno su anno (es. X 2026 vs X 2027) oppure con impressioni;
- pagine domanda: solo quelle con impressioni (in almeno una lingua);
- pickleball: tutte (nicchia con pochi concorrenti, scelta di Luca);
- tutto il resto (home, sezioni, articoli, guide, marchi, glossario, offerte, legali): indicizzato.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEZ_SCHEDE = {"racchette", "rackets", "palas", "raquettes"}
SEZ_CONFRONTI = {"confronta", "compare", "comparar", "comparer"}
SEZ_DOMANDE = {"domande", "questions", "preguntas"}
CAMPI = ("forma", "peso", "nucleo", "telaio", "superficie")

_cache = {}


def _dati():
    if _cache:
        return _cache
    imp = ROOT / "scripts" / "dati_indice" / "pagine_impressioni.json"
    _cache["imp"] = set(json.loads(imp.read_text(encoding="utf-8"))) if imp.exists() else set()
    am = ROOT / "amazon" / "immagini.json"
    _cache["amazon"] = {p.get("scheda") for p in json.loads(am.read_text(encoding="utf-8")).get("prodotti", {}).values()} if am.exists() else set()
    schede = {}
    for f in (ROOT / "data" / "racchette").glob("*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        completa = all(d.get(k) for k in CAMPI) or bool(d.get("valutazioni_esterne"))
        schede[d["slug"]] = str(d.get("anno")) in ("2026", "2027") and completa
    _cache["schede"] = schede
    return _cache


def _senza_anno(s):
    return re.sub(r"-20\d\d$", "", s)


def indicizzabile(path, alt=None):
    parti = path.strip("/").split("/")
    if len(parti) < 2:
        return True
    sez, ultimo = parti[1], parti[-1]
    if len(parti) < 3:
        return True  # pagine indice delle sezioni
    d = _dati()
    percorsi = {path, *((alt or {}).values())}
    con_impressioni = bool(percorsi & d["imp"])
    if sez in SEZ_SCHEDE:
        recente = ultimo.endswith(("-2026", "-2027"))
        return d["schede"].get(ultimo, False) or (recente and ultimo in d["amazon"]) or con_impressioni
    if sez in SEZ_CONFRONTI:
        if "-vs-" in ultimo:
            a, b = ultimo.split("-vs-", 1)
            if _senza_anno(a) == _senza_anno(b):
                return True
        return con_impressioni
    if sez in SEZ_DOMANDE:
        return con_impressioni
    return True


META = '<meta name="robots" content="noindex, follow">'


def applica(html_txt, path, alt=None):
    """Aggiunge il meta noindex se la pagina non va indicizzata."""
    if indicizzabile(path, alt) or META in html_txt:
        return html_txt
    return html_txt.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n' + META, 1)
