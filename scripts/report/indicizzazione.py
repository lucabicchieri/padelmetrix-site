"""Controllo indicizzazione: sitemap inviate, andamento giornaliero (dati finali e freschi) e ispezione di un campione di URL.
Stampa REPORT_B64."""
import base64
import collections
import datetime as dt
import json
import random
import re

from dati_report import SITO, gsc, sessione


def main():
    s, _ = sessione()
    sito_enc = SITO.replace(":", "%3A").replace("/", "%2F")
    out = {"errori": []}
    try:
        r = s.get(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{sito_enc}/sitemaps")
        out["sitemap"] = r.json()
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"sitemap: {e}")
    oggi = dt.date.today()
    for stato in ("final", "all"):
        try:
            corpo = {"startDate": (oggi - dt.timedelta(days=35)).isoformat(), "endDate": oggi.isoformat(), "dimensions": ["date"], "dataState": stato, "rowLimit": 100}
            r = s.post(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{sito_enc}/searchAnalytics/query", json=corpo)
            out[f"giorni_{stato}"] = [(x["keys"][0], x["clicks"], x["impressions"], round(x["position"], 1)) for x in r.json().get("rows", [])]
        except Exception as e:  # noqa: BLE001
            out["errori"].append(f"giorni {stato}: {e}")
    try:
        pg = gsc(s, SITO, oggi - dt.timedelta(days=90), oggi, ["page"], 25000)
        out["pagine_con_impressioni_90g"] = len(pg)
        cnt = collections.Counter()
        for x in pg:
            m = re.match(r"https://www\.padelmetrix\.com/(\w\w)/([^/]+)/", x["keys"][0])
            cnt[(m.group(1) + "/" + m.group(2)) if m else "altro"] += 1
        out["pagine_con_impressioni_per_sezione"] = cnt.most_common(40)
    except Exception as e:  # noqa: BLE001
        out["errori"].append(f"pagine: {e}")
    # campione URL dalla sitemap
    urls = re.findall(r"<loc>([^<]+)</loc>", open("../../sitemap.xml").read())
    random.seed(7)
    gruppi = collections.defaultdict(list)
    for u in urls:
        m = re.match(r"https://www\.padelmetrix\.com/(\w\w)/([^/]+)/", u)
        gruppi[(m.group(1), m.group(2)) if m else ("-", "-")].append(u)
    camp = []
    for k, v in sorted(gruppi.items()):
        camp += random.sample(v, min(len(v), 6))
    camp = camp[:400]
    ris = []
    for u in camp:
        try:
            r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect", json={"inspectionUrl": u, "siteUrl": SITO, "languageCode": "it"})
            j = r.json()
            ir = j.get("inspectionResult", {}).get("indexStatusResult", {})
            ris.append({"url": u, "verdetto": ir.get("verdict"), "stato": ir.get("coverageState"), "crawl": ir.get("lastCrawlTime"),
                        "canonical_google": ir.get("googleCanonical"), "canonical_utente": ir.get("userCanonical"), "robots": ir.get("robotsTxtState"),
                        "indexing": ir.get("indexingState"), "fetch": ir.get("pageFetchState"), "err": j.get("error", {}).get("message")})
        except Exception as e:  # noqa: BLE001
            ris.append({"url": u, "err": str(e)})
    out["ispezioni"] = ris
    print("REPORT_B64 " + base64.b64encode(json.dumps(out, ensure_ascii=False).encode()).decode())


if __name__ == "__main__":
    main()
