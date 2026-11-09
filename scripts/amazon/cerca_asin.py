"""Cerca su amazon.it (Creators API, SearchItems) i candidati ASIN per ogni racchetta del database.

Non modifica le schede: salva i candidati in amazon-out/candidati.json, da verificare prima di
impostare l'ASIN. Facoltativo: elenco di slug come argomenti per limitare la ricerca.
"""
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SEARCH = "https://creatorsapi.amazon/catalog/v1/searchItems"


def cerca(kw, brand, tok, ver, indice="SportsAndOutdoors"):
    corpo = {"partnerTag": "padelmetrix-21", "marketplace": "www.amazon.it", "keywords": kw, "searchIndex": indice,
             "itemCount": 10, "availability": "IncludeOutOfStock",
             "resources": ["itemInfo.title", "itemInfo.byLineInfo"]}
    if brand:
        corpo["brand"] = brand
    body = json.dumps(corpo).encode()
    for tentativo in range(4):
        st, txt = creators._post(SEARCH, body, {"Authorization": f"Bearer {tok}, Version {ver}",
                                                "Content-Type": "application/json", "x-marketplace": "www.amazon.it"})
        if st == 200:
            res = json.loads(txt)
            items = (res.get("searchResult") or {}).get("items") or []
            out = []
            for it in items:
                ii = it.get("itemInfo") or {}
                out.append({"asin": it.get("asin"), "titolo": (ii.get("title") or {}).get("displayValue", ""),
                            "marca": ((ii.get("byLineInfo") or {}).get("brand") or {}).get("displayValue", "")})
            return st, out
        if st == 429:
            time.sleep(3 + 3 * tentativo)
            continue
        return st, txt[:300]
    return st, "troppe richieste"


def main():
    filtro = set(sys.argv[1:])
    schede = []
    for f in sorted(glob.glob(os.path.join(RADICE, "data", "racchette", "*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        if filtro and d["slug"] not in filtro:
            continue
        schede.append(d)
    tok, ver = creators.token()
    t0, out = time.time(), {}
    for i, d in enumerate(schede):
        if time.time() - t0 > 3000:  # il token dura circa un'ora
            tok, ver = creators.token()
            t0 = time.time()
        kw = f'{d["marca"]} {d["modello"]} {d["anno"]}'
        st, res = cerca(kw, d["marca"], tok, ver)
        if st == 200 and not res:
            st, res = cerca(f'{d["marca"]} {d["modello"]}', None, tok, ver)
        out[d["slug"]] = {"cerca": kw, "stato": st, "risultati": res}
        print(f"{i + 1}/{len(schede)} {d['slug']}: HTTP {st}, {len(res) if isinstance(res, list) else res}")
        for r in (res if isinstance(res, list) else []):
            print("CAND\t" + d["slug"] + "\t" + (r["asin"] or "") + "\t" + r["marca"] + "\t" + r["titolo"].replace("\t", " "))
        time.sleep(1.1)
    os.makedirs("amazon-out", exist_ok=True)
    json.dump(out, open("amazon-out/candidati.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
