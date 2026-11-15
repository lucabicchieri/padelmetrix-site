"""Cerca su amazon.it (Creators API, SearchItems) le racchette da padel di ogni marchio, pagina per pagina.

Stampa righe RAC (marchio cercato, asin, marca Amazon, prezzo, titolo) da confrontare con il catalogo:
servono a trovare i modelli ancora senza scheda."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

SEARCH = "https://creatorsapi.amazon/catalog/v1/searchItems"
MARCHE = ["Akkeron", "Sane", "Puma", "Mystica", "ShockOut", "Legend", "Prince", "Harlem", "Orygen", "Kaitt", "Slazenger", "Lacoste", "K-Swiss",
          "Enebe", "Vibor-A", "Vibora", "Royal Padel", "Black Crown", "Tecnifibre", "Lok", "Vairo", "Varlion", "Kombat", "Kuikma", "Softee", "Dunlop",
          "Drop Shot", "Oxdog", "Wilson", "Babolat", "Head", "Joma", "StarVie", "Siux", "Nox", "Bullpadel", "Adidas", "Hirostar", "Tenax", "QUAD",
          "Asics", "J'Hayber", "Artengo", "Kelme", "Endless", "Volt", "RS Padel", "Cartri", "Just Ten", "Toalson", "Middle Moon", "Bear Padel", "Ka-Pow"]


def cerca(kw, pagina, tok, ver):
    corpo = {"partnerTag": "padelmetrix-21", "marketplace": "www.amazon.it", "keywords": kw, "searchIndex": "SportsAndOutdoors",
             "itemCount": 10, "itemPage": pagina, "resources": ["itemInfo.title", "itemInfo.byLineInfo", "offersV2.listings.price"]}
    for tentativo in range(5):
        st, txt = creators._post(SEARCH, json.dumps(corpo).encode(), {"Authorization": f"Bearer {tok}, Version {ver}",
                                 "Content-Type": "application/json", "x-marketplace": "www.amazon.it"})
        if st == 200:
            return st, (json.loads(txt).get("searchResult") or {}).get("items") or []
        if st == 429:
            time.sleep(3 + 3 * tentativo)
            continue
        return st, txt[:200]
    return st, "troppe richieste"


def main():
    tok, ver = creators.token()
    pagine = int(os.environ.get("PAGINE", "5"))
    for m in MARCHE:
        for pg in range(1, pagine + 1):
            st, items = cerca(f"racchetta padel {m}", pg, tok, ver)
            if not isinstance(items, list) or not items:
                print(f"== {m} p{pg}: HTTP {st} {'' if isinstance(items, list) else items}")
                break
            for it in items:
                ii = it.get("itemInfo") or {}
                tit = (ii.get("title") or {}).get("displayValue", "").replace("\t", " ")
                marca = ((ii.get("byLineInfo") or {}).get("brand") or {}).get("displayValue", "")
                pz = ""
                for l in ((it.get("offersV2") or {}).get("listings") or [])[:1]:
                    pz = (((l.get("price") or {}).get("money") or {}).get("displayAmount") or "")
                print("RAC\t" + m + "\t" + (it.get("asin") or "") + "\t" + marca + "\t" + pz.replace(" ", " ") + "\t" + tit)
            time.sleep(1.1)


if __name__ == "__main__":
    main()
