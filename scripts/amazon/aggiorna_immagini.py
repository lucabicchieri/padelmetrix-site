"""Aggiorna amazon/immagini.json con le immagini ufficiali dei prodotti (Creators API).

Raccoglie gli ASIN dai negozi Amazon delle schede (data/racchette/*.json), interroga
getItems a blocchi di 10 e salva solo URL, misure e titolo restituiti dall'API.
Le immagini non vengono copiate: le pagine le mostrano dagli URL Amazon, aggiornati ogni giorno.
"""
import datetime
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(RADICE, "amazon", "immagini.json")


def asin_schede():
    out = {}
    for f in sorted(glob.glob(os.path.join(RADICE, "data", "racchette", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        negozi = d.get("negozi") or (d.get("pagina") or {}).get("negozi") or []
        for s in negozi:
            if s.get("amazon") and s.get("asin"):
                out[s["asin"]] = os.path.basename(f)[:-5]
    sys.path.insert(0, os.path.join(RADICE, "scripts"))
    from dati_pickleball import P as PADDLE
    for p in PADDLE:
        if p.get("asin"):
            out[p["asin"]] = "pickleball/" + p["slug"]
    from dati_regali_prodotti import P as REGALI
    for a in REGALI:
        out.setdefault(a, "regali")
    return out


def main():
    schede = asin_schede()
    print(f"ASIN nelle schede: {len(schede)}")
    if not schede:
        return
    tok, ver = creators.token()
    oggi = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    risultato, asins = {}, list(schede)
    import time
    for i in range(0, len(asins), 10):
        if i:
            time.sleep(1.5)
        res = creators.get_items(asins[i:i + 10], tok, ver) or {}
        items = (res.get("itemsResult") or {}).get("items") or res.get("items") or []
        for it in items:
            img = (((it.get("images") or {}).get("primary") or {}).get("large") or {})
            if not img.get("url"):
                continue
            titolo = (((it.get("itemInfo") or {}).get("title") or {}).get("displayValue")) or ""
            risultato[it["asin"]] = {"img": img["url"], "w": img.get("width"), "h": img.get("height"),
                                     "titolo": titolo, "scheda": schede.get(it["asin"])}
            off = ((it.get("offersV2") or {}).get("listings") or [{}])[0]
            soldi = (off.get("price") or {}).get("money") or {}
            if soldi.get("displayAmount"):
                risultato[it["asin"]]["prezzo"] = soldi["displayAmount"]
        for err in res.get("errors") or []:
            print("errore:", str(err)[:200])
    if not risultato:
        sys.exit("Nessuna immagine ricevuta: il file esistente non viene toccato")
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump({"aggiornato": oggi, "prodotti": risultato}, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Salvate {len(risultato)} immagini in amazon/immagini.json")


if __name__ == "__main__":
    main()
