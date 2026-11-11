"""Cerca su amazon.it (Creators API, SearchItems) prodotti per le guide regalo di Natale.

Stampa nel log righe REG (cat, asin, marca, titolo) e FEAT (caratteristiche) da verificare a mano.
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

SEARCH = "https://creatorsapi.amazon/catalog/v1/searchItems"
Q = [
    ("pressurizzatore", "pressurizzatore palline padel", "SportsAndOutdoors"),
    ("pressurizzatore", "pressurizzatore palline tennis", "SportsAndOutdoors"),
    ("palline", "palline padel Head", "SportsAndOutdoors"),
    ("palline", "palline padel Bullpadel", "SportsAndOutdoors"),
    ("palline", "palline padel Wilson", "SportsAndOutdoors"),
    ("overgrip", "overgrip padel", "SportsAndOutdoors"),
    ("polsini", "polsini spugna sport", "SportsAndOutdoors"),
    ("fascia", "fascia sudore testa sport", "SportsAndOutdoors"),
    ("protezione", "protezione racchetta padel adesivo", "SportsAndOutdoors"),
    ("borsa", "borsa padel Bullpadel", "SportsAndOutdoors"),
    ("borsa", "borsa padel Adidas", "SportsAndOutdoors"),
    ("borsa", "borsa padel Head", "SportsAndOutdoors"),
    ("borsa", "zaino padel", "SportsAndOutdoors"),
    ("borsa", "paletero padel", "SportsAndOutdoors"),
    ("scarpe_u", "scarpe padel uomo Asics", "Fashion"),
    ("scarpe_u", "scarpe padel uomo Bullpadel", "Fashion"),
    ("scarpe_u", "scarpe padel uomo Adidas", "Fashion"),
    ("scarpe_u", "scarpe padel uomo Babolat", "Fashion"),
    ("scarpe_d", "scarpe padel donna Asics", "Fashion"),
    ("scarpe_d", "scarpe padel donna Bullpadel", "Fashion"),
    ("scarpe_d", "scarpe padel donna Adidas", "Fashion"),
    ("abb_u", "maglietta padel uomo", "Fashion"),
    ("abb_u", "pantaloncini padel uomo", "Fashion"),
    ("abb_u", "felpa padel uomo", "Fashion"),
    ("abb_d", "maglietta padel donna", "Fashion"),
    ("abb_d", "gonna padel donna", "Fashion"),
    ("abb_d", "vestito padel donna", "Fashion"),
    ("calze", "calze tecniche padel", "Fashion"),
    ("cappello", "cappellino visiera running tennis", "Fashion"),
    ("borraccia", "borraccia termica sport 750 ml", "SportsAndOutdoors"),
    ("junior", "racchetta padel junior bambino", "SportsAndOutdoors"),
    ("junior", "palline padel bambini depressurizzate", "SportsAndOutdoors"),
    ("gadget", "portachiavi racchetta padel", "SportsAndOutdoors"),
    ("gadget", "cestino raccogli palline padel", "SportsAndOutdoors"),
    ("gadget", "tubo raccogli palline tennis", "SportsAndOutdoors"),
    ("gadget", "libro padel", "Books"),
    ("gadget", "ginocchiera sport", "SportsAndOutdoors"),
    ("gadget", "gomitiera epicondilite tennis", "SportsAndOutdoors"),
    ("gadget", "occhiali protettivi padel", "SportsAndOutdoors"),
    ("gadget", "asciugamano microfibra sport", "SportsAndOutdoors"),
]


def cerca(kw, indice, tok, ver):
    corpo = {"partnerTag": "padelmetrix-21", "marketplace": "www.amazon.it", "keywords": kw, "searchIndex": indice,
             "itemCount": 10, "resources": ["itemInfo.title", "itemInfo.byLineInfo", "itemInfo.features"]}
    for tentativo in range(4):
        st, txt = creators._post(SEARCH, json.dumps(corpo).encode(), {"Authorization": f"Bearer {tok}, Version {ver}",
                                 "Content-Type": "application/json", "x-marketplace": "www.amazon.it"})
        if st == 200:
            return st, (json.loads(txt).get("searchResult") or {}).get("items") or []
        if st == 429:
            time.sleep(3 + 3 * tentativo)
            continue
        return st, txt[:300]
    return st, "troppe richieste"


def main():
    tok, ver = creators.token()
    for cat, kw, ind in Q:
        st, items = cerca(kw, ind, tok, ver)
        print(f"== {cat} | {kw}: HTTP {st} {'' if isinstance(items, list) else items}")
        for it in (items if isinstance(items, list) else []):
            ii = it.get("itemInfo") or {}
            tit = (ii.get("title") or {}).get("displayValue", "").replace("\t", " ")
            marca = ((ii.get("byLineInfo") or {}).get("brand") or {}).get("displayValue", "")
            print("REG\t" + cat + "\t" + (it.get("asin") or "") + "\t" + marca + "\t" + tit)
            feats = ((ii.get("features") or {}).get("displayValues") or [])[:4]
            print("FEAT\t" + (it.get("asin") or "") + "\t" + " || ".join(f.replace("\t", " ")[:220] for f in feats))
        time.sleep(1.2)


if __name__ == "__main__":
    main()
