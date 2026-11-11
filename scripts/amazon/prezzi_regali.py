"""Stampa titolo e prezzo attuale (Creators API getItems) per gli ASIN in regali_candidati.txt."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))
import creators  # noqa: E402

asins = open(os.path.join(os.path.dirname(__file__), "regali_candidati.txt")).read().split()
tok, ver = creators.token()
for i in range(0, len(asins), 10):
    time.sleep(1.5)
    res = creators.get_items(asins[i:i + 10], tok, ver) or {}
    items = (res.get("itemsResult") or {}).get("items") or res.get("items") or []
    if i == 0 and items:
        print("ESEMPIO", json.dumps(items[0].get("offersV2"))[:800])
    for it in items:
        o = (it.get("offersV2") or {}).get("listings") or []
        p = ((o[0].get("price") or {}).get("money") or {}) if o else {}
        tit = (((it.get("itemInfo") or {}).get("title") or {}).get("displayValue")) or ""
        img = "IMG" if ((it.get("images") or {}).get("primary") or {}).get("large") else "noimg"
        print("PRZ\t" + it["asin"] + "\t" + str(p.get("amount", "")) + "\t" + str(p.get("displayAmount", "")) + "\t" + img + "\t" + tit[:90])
    for e in res.get("errors") or []:
        print("ERR\t" + str(e)[:200])
