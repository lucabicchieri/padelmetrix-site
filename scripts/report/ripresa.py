"""Diagnosi del calo di Google: confronto prima (24/10-9/11) e dopo (12/11-ieri) per sezione, lingua, query e pagine,
controllo URL Inspection delle pagine che hanno perso di più e controllo HTTP degli host. Stampa REPORT_B64."""
import base64
import collections
import datetime as dt
import json

import requests

from dati_report import SITO, sessione, lingua


def q(s, a, b, dims, limite=25000, stato="final"):
    corpo = {"startDate": a.isoformat(), "endDate": b.isoformat(), "dimensions": dims, "rowLimit": limite, "dataState": stato}
    r = s.post(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{SITO.replace(':', '%3A').replace('/', '%2F')}/searchAnalytics/query", json=corpo)
    r.raise_for_status()
    return r.json().get("rows", [])


def sezione(u):
    p = u.split("/", 3)[3] if u.count("/") >= 3 else ""
    parti = p.strip("/").split("/")
    return parti[1] if len(parti) > 1 else (parti[0] or "home")


def main():
    s, _ = sessione()
    oggi = dt.date.today()
    A0, A1 = dt.date(2026, 10, 24), dt.date(2026, 11, 9)
    B0, B1 = dt.date(2026, 11, 12), oggi - dt.timedelta(days=1)
    out = {"prima": [A0.isoformat(), A1.isoformat()], "dopo": [B0.isoformat(), B1.isoformat()], "errori": []}
    try:
        pa, pb = q(s, A0, A1, ["page"]), q(s, B0, B1, ["page"], stato="all")
        sez = collections.defaultdict(lambda: [0, 0, 0, 0, 0])  # impr prima, impr dopo, clic prima, clic dopo, pagine con impr prima
        lin = collections.defaultdict(lambda: [0, 0])
        dopo = {r["keys"][0]: r for r in pb}
        for r in pa:
            k = lingua(r["keys"][0]) + ":" + sezione(r["keys"][0])
            sez[k][0] += r["impressions"]; sez[k][2] += r["clicks"]; sez[k][4] += 1
            lin[lingua(r["keys"][0])][0] += r["impressions"]
        for r in pb:
            k = lingua(r["keys"][0]) + ":" + sezione(r["keys"][0])
            sez[k][1] += r["impressions"]; sez[k][3] += r["clicks"]
            lin[lingua(r["keys"][0])][1] += r["impressions"]
        out["sezioni"] = dict(sorted(sez.items(), key=lambda x: -x[1][0]))
        out["lingue"] = lin
        out["pagine_prima_n"], out["pagine_dopo_n"] = len(pa), len(pb)
        top = sorted(pa, key=lambda r: -r["impressions"])[:40]
        out["top_pagine"] = [[r["keys"][0], r["impressions"], r["clicks"], round(r["position"], 1),
                              dopo.get(r["keys"][0], {}).get("impressions", 0), round(dopo.get(r["keys"][0], {}).get("position", 0), 1)] for r in top]
        qa = q(s, A0, A1, ["query"])
        qb = {r["keys"][0]: r for r in q(s, B0, B1, ["query"], stato="all")}
        out["top_query"] = [[r["keys"][0], r["impressions"], r["clicks"], round(r["position"], 1), qb.get(r["keys"][0], {}).get("impressions", 0)]
                            for r in sorted(qa, key=lambda r: -r["impressions"])[:60]]
        out["query_n"] = [len(qa), len(qb)]
        out["paesi"] = [[r["keys"][0], r["impressions"]] for r in sorted(q(s, A0, A1, ["country"]), key=lambda r: -r["impressions"])[:10]]
        out["giorni"] = [[r["keys"][0], r["impressions"], r["clicks"], round(r["position"], 1)] for r in q(s, A0, B1, ["date"], stato="all")]
        out["dispositivi"] = q(s, A0, A1, ["device"])
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"GSC: {e}")
    try:
        ins = []
        for u in [t[0] for t in out.get("top_pagine", [])[:25]]:
            r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect", json={"inspectionUrl": u, "siteUrl": SITO, "languageCode": "it"})
            ir = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
            ins.append([u, ir.get("verdict"), ir.get("coverageState"), ir.get("googleCanonical"), ir.get("lastCrawlTime"), ir.get("pageFetchState")])
        out["ispezione"] = ins
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"Inspection: {e}")
    http = []
    ua = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}
    for u in ["http://padelmetrix.com/", "https://padelmetrix.com/", "https://padelmetrix.com/it/", "http://www.padelmetrix.com/it/",
              "https://www.padelmetrix.com/", "https://www.padelmetrix.com/it/", "https://www.padelmetrix.com/it/racchette/",
              "https://www.padelmetrix.com/it/racchette/nox-ventus-attack-12k-xtrem-2027", "https://www.padelmetrix.com/sitemap.xml",
              "https://www.padelmetrix.com/robots.txt"]:
        try:
            r = requests.get(u, allow_redirects=False, timeout=20, headers=ua)
            http.append([u, r.status_code, r.headers.get("location"), r.headers.get("x-robots-tag"), r.headers.get("content-type"), len(r.content)])
        except Exception as e:  # noqa: BLE001
            http.append([u, str(e)[:80]])
    out["http"] = http
    try:
        out["sitemap_url"] = requests.get("https://www.padelmetrix.com/sitemap.xml", timeout=30).text.count("<loc>")
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"sitemap: {e}")
    print("REPORT_B64 " + base64.b64encode(json.dumps(out, ensure_ascii=False).encode()).decode())


if __name__ == "__main__":
    main()
