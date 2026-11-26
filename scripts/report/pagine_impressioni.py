"""Elenco di tutte le pagine che hanno avuto almeno un'impressione su Google dal lancio. Stampa REPORT_B64 (lista di URL)."""
import base64
import datetime as dt
import json

from dati_report import SITO, sessione


def main():
    s, _ = sessione()
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{SITO.replace(':', '%3A').replace('/', '%2F')}/searchAnalytics/query"
    pagine = {}
    for stato in ("final", "all"):
        r = s.post(url, json={"startDate": "2026-10-20", "endDate": dt.date.today().isoformat(), "dimensions": ["page"],
                              "rowLimit": 25000, "dataState": stato})
        r.raise_for_status()
        for row in r.json().get("rows", []):
            pagine[row["keys"][0]] = max(pagine.get(row["keys"][0], 0), row["impressions"])
    print("REPORT_B64 " + base64.b64encode(json.dumps(pagine).encode()).decode())


if __name__ == "__main__":
    main()
