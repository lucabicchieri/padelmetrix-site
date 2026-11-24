"""Analisi di un singolo giorno (default: ieri, ora di Roma) con confronto al giorno prima e a 7 giorni prima.
GA4 + Search Console (dati freschi, dataState=all). Stampa REPORT_B64."""
import base64
import datetime as dt
import json
import os
import zoneinfo

from dati_report import SITO, ga, sessione, lingua


def gsc_all(s, a, b, dims, limite=1000):
    corpo = {"startDate": a.isoformat(), "endDate": b.isoformat(), "dimensions": dims, "rowLimit": limite, "dataState": "all"}
    r = s.post(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{SITO.replace(':', '%3A').replace('/', '%2F')}/searchAnalytics/query", json=corpo)
    if r.status_code != 200:
        raise RuntimeError(f"Search Console {r.status_code}: {r.text[:300]}")
    return r.json().get("rows", [])


def main():
    s, _ = sessione()
    oggi = dt.datetime.now(zoneinfo.ZoneInfo("Europe/Rome")).date()
    g = dt.date.fromisoformat(os.environ.get("GIORNO") or (oggi - dt.timedelta(days=1)).isoformat())
    prima, sett = g - dt.timedelta(days=1), g - dt.timedelta(days=7)
    prop = os.environ["GA4_PROPERTY_ID"]
    out = {"giorno": g.isoformat(), "errori": []}
    mets = ["sessions", "activeUsers", "newUsers", "screenPageViews", "engagementRate", "averageSessionDuration"]
    try:
        out["ga_giorni"] = sorted(ga(s, prop, g - dt.timedelta(days=27), g, ["date"], mets, limite=100), key=lambda r: r["date"])
        for nome, d in (("g", g), ("prima", prima), ("sett", sett)):
            out[f"ga_canali_{nome}"] = ga(s, prop, d, d, ["sessionDefaultChannelGroup"], ["sessions", "engagementRate"], limite=20, ordina="sessions")
            out[f"ga_lingue_{nome}"] = ga(s, prop, d, d, ["landingPage"], ["sessions"], limite=5000)
        out["ga_sorgenti"] = ga(s, prop, g, g, ["sessionSource", "sessionMedium"], ["sessions", "engagementRate"], limite=25, ordina="sessions")
        out["ga_paesi"] = ga(s, prop, g, g, ["country"], ["sessions"], limite=15, ordina="sessions")
        out["ga_device"] = ga(s, prop, g, g, ["deviceCategory"], ["sessions", "engagementRate"], limite=5, ordina="sessions")
        out["ga_ingresso"] = ga(s, prop, g, g, ["landingPage"], ["sessions", "engagementRate", "averageSessionDuration"], limite=30, ordina="sessions")
        out["ga_pagine"] = ga(s, prop, g, g, ["pagePath"], ["screenPageViews", "activeUsers"], limite=30, ordina="screenPageViews")
        out["ga_eventi"] = ga(s, prop, g, g, ["eventName"], ["eventCount", "totalUsers"], limite=40, ordina="eventCount")
        out["ga_eventi_sett"] = ga(s, prop, sett, sett, ["eventName"], ["eventCount"], limite=40, ordina="eventCount")
        out["ga_ore"] = sorted(ga(s, prop, g, g, ["hour"], ["sessions"], limite=24), key=lambda r: r["hour"])
        out["ga_goni"] = ga(s, prop, g, g, ["pagePath"], ["screenPageViews"], limite=20, filtro={"filter": {"fieldName": "pagePath", "stringFilter": {"matchType": "CONTAINS", "value": "goni"}}})
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"GA4: {e}")
    try:
        out["gsc_giorni"] = gsc_all(s, g - dt.timedelta(days=27), oggi, ["date"], limite=100)
        out["gsc_query"] = gsc_all(s, g, g, ["query"], limite=40)
        out["gsc_pagine"] = gsc_all(s, g, g, ["page"], limite=30)
        out["gsc_paesi"] = gsc_all(s, g, g, ["country"], limite=10)
        out["gsc_lingue_pagine"] = gsc_all(s, g, g, ["page"], limite=5000)
        out["gsc_lingue_pagine_sett"] = gsc_all(s, sett, sett, ["page"], limite=5000)
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"Search Console: {e}")
    for k in [k for k in out if k.startswith("ga_lingue_")]:
        agg = {}
        for r in out[k]:
            agg[lingua(r["landingPage"])] = agg.get(lingua(r["landingPage"]), 0) + r["sessions"]
        out[k] = agg
    for k in ("gsc_lingue_pagine", "gsc_lingue_pagine_sett"):
        agg = {}
        for r in out.get(k, []):
            l = lingua(r["keys"][0])
            a = agg.setdefault(l, [0, 0])
            a[0] += r["clicks"]; a[1] += r["impressions"]
        out[k] = agg
    print("REPORT_B64 " + base64.b64encode(json.dumps(out, ensure_ascii=False).encode()).decode())


if __name__ == "__main__":
    main()
