"""Visite per lingua dall'inizio: GA4 (dalla creazione della proprietà) e Search Console (fino a 16 mesi).
La lingua è il primo segmento del percorso (/it/, /en/, /es/, /fr/); il resto va in "altro". Stampa REPORT_B64."""
import base64
import collections
import datetime as dt
import json
import os

from dati_report import SITO, ga, gsc, sessione


def lingua(p):
    seg = (p or "/").split("?")[0].strip("/").split("/")[0]
    if p.startswith("http"):
        seg = p.split("/", 3)[3].split("/")[0] if p.count("/") >= 3 else ""
    return seg if seg in ("it", "en", "es", "fr") else ("home" if seg == "" else "altro")


def main():
    s, _ = sessione()
    oggi = dt.date.today()
    ini = dt.date(2025, 1, 1)
    prop = os.environ["GA4_PROPERTY_ID"]
    out = {"dal": ini.isoformat(), "al": oggi.isoformat(), "errori": []}
    mets = ["sessions", "screenPageViews", "activeUsers"]
    try:
        tot = collections.defaultdict(lambda: dict.fromkeys(mets, 0.0))
        rows = ga(s, prop, ini, oggi, ["landingPage"], mets, limite=100000)
        for r in rows:
            for m in mets:
                tot[lingua(r["landingPage"])][m] += r[m]
        out["ga_ingresso"] = tot
        pv = collections.defaultdict(float)
        for r in ga(s, prop, ini, oggi, ["pagePath"], ["screenPageViews"], limite=100000):
            pv[lingua(r["pagePath"])] += r["screenPageViews"]
        out["ga_pagine_viste"] = pv
        out["ga_totali"] = ga(s, prop, ini, oggi, [], mets)
        out["ga_primo_giorno"] = min((r["date"] for r in ga(s, prop, ini, oggi, ["date"], ["sessions"], limite=1000) if r["sessions"] > 0), default=None)
        mese = collections.defaultdict(lambda: collections.defaultdict(float))
        for r in ga(s, prop, ini, oggi, ["yearMonth", "landingPage"], ["sessions"], limite=100000):
            mese[r["yearMonth"]][lingua(r["landingPage"])] += r["sessions"]
        out["ga_mesi"] = mese
        paesi = collections.defaultdict(lambda: collections.defaultdict(float))
        for r in ga(s, prop, ini, oggi, ["country", "landingPage"], ["sessions"], limite=100000):
            paesi[lingua(r["landingPage"])][r["country"]] += r["sessions"]
        out["ga_paesi"] = {k: dict(sorted(v.items(), key=lambda x: -x[1])[:5]) for k, v in paesi.items()}
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"GA4: {e}")
    try:
        g = collections.defaultdict(lambda: {"clic": 0.0, "impressioni": 0.0})
        a = oggi - dt.timedelta(days=480)
        for r in gsc(s, SITO, a, oggi - dt.timedelta(days=2), ["page"], limite=25000):
            l = lingua(r["keys"][0])
            g[l]["clic"] += r["clicks"]
            g[l]["impressioni"] += r["impressions"]
        out["gsc"] = g
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"Search Console: {e}")
    t = json.dumps(out, ensure_ascii=False)
    print("REPORT_B64 " + base64.b64encode(t.encode()).decode())


if __name__ == "__main__":
    main()
