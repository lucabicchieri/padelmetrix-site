"""Scarica da amazon.it (Creators API, GetItems) titolo, marca, caratteristiche e dati tecnici degli ASIN in dettagli_asin.txt.
Stampa una riga DET con il JSON di ogni prodotto: serve a raccogliere le specifiche dichiarate per le nuove schede."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

URL = "https://creatorsapi.amazon/catalog/v1/getItems"
RES = ["itemInfo.title", "itemInfo.byLineInfo", "itemInfo.features", "itemInfo.productInfo", "itemInfo.technicalInfo",
       "itemInfo.manufactureInfo", "itemInfo.contentInfo", "itemInfo.classifications", "offersV2.listings.price"]


def main():
    tok, ver = creators.token()
    asins = open(os.path.join(os.path.dirname(__file__), "dettagli_asin.txt")).read().split()
    for i in range(0, len(asins), 10):
        corpo = {"partnerTag": "padelmetrix-21", "marketplace": "www.amazon.it", "itemIds": asins[i:i + 10], "resources": RES}
        for t in range(5):
            st, txt = creators._post(URL, json.dumps(corpo).encode(), {"Authorization": f"Bearer {tok}, Version {ver}",
                                     "Content-Type": "application/json", "x-marketplace": "www.amazon.it"})
            if st != 429:
                break
            time.sleep(3 + 3 * t)
        if st != 200:
            print("ERR", st, txt[:200]); continue
        for it in (json.loads(txt).get("itemsResult") or {}).get("items") or []:
            print("DET\t" + json.dumps(it, ensure_ascii=False))
        time.sleep(1.2)


if __name__ == "__main__":
    main()
