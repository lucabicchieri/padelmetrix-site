"""Raccoglie i dati per il report settimanale PadelMetrix: Google Search Console e Google Analytics 4.

Credenziali: secret GOOGLE_SA_JSON (chiave JSON di un account di servizio con accesso in sola lettura
a Search Console e alla proprietà GA4) e GA4_PROPERTY_ID (numero della proprietà). Confronta gli ultimi 7 giorni
completi con i 7 precedenti (Search Console ha 2-3 giorni di ritardo, quindi la finestra finisce 3 giorni fa).
Scrive report_dati.json e ne stampa un riassunto."""
import base64
import datetime as dt
import json
import os
import sys

from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

SITO = os.environ.get("GSC_SITE", "https://www.padelmetrix.com/")
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly", "https://www.googleapis.com/auth/analytics.readonly"]


def sessione():
    info = json.loads(os.environ["GOOGLE_SA_JSON"])
    cred = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
    return AuthorizedSession(cred), info.get("client_email")


def periodi(ritardo):
    fine = dt.date.today() - dt.timedelta(days=ritardo)
    ini = fine - dt.timedelta(days=6)
    return (ini, fine), (ini - dt.timedelta(days=7), fine - dt.timedelta(days=7))


def gsc(s, sito, a, b, dims, limite=1000, filtri=None):
    corpo = {"startDate": a.isoformat(), "endDate": b.isoformat(), "dimensions": dims, "rowLimit": limite, "dataState": "final"}
    if filtri:
        corpo["dimensionFilterGroups"] = [{"filters": filtri}]
    r = s.post(f"https://searchconsole.googleapis.com/webmasters/v3/sites/{sito.replace(':', '%3A').replace('/', '%2F')}/searchAnalytics/query", json=corpo)
    if r.status_code != 200:
        raise RuntimeError(f"Search Console {r.status_code}: {r.text[:300]}")
    return r.json().get("rows", [])


def ga(s, prop, a, b, dims, mets, limite=50, filtro=None, ordina=None):
    corpo = {"dateRanges": [{"startDate": a.isoformat(), "endDate": b.isoformat()}], "dimensions": [{"name": d} for d in dims],
             "metrics": [{"name": m} for m in mets], "limit": limite}
    if filtro:
        corpo["dimensionFilter"] = filtro
    if ordina:
        corpo["orderBys"] = [{"metric": {"metricName": ordina}, "desc": True}]
    r = s.post(f"https://analyticsdata.googleapis.com/v1beta/properties/{prop}:runReport", json=corpo)
    if r.status_code != 200:
        raise RuntimeError(f"Analytics {r.status_code}: {r.text[:300]}")
    j = r.json()
    out = []
    for row in j.get("rows", []):
        out.append({**{d: v["value"] for d, v in zip(dims, row.get("dimensionValues", []))},
                    **{m: float(v["value"]) for m, v in zip(mets, row.get("metricValues", []))}})
    return out


def main():
    s, email = sessione()
    dati = {"generato": dt.datetime.utcnow().isoformat() + "Z", "account_servizio": email}
    errori = []
    # --- Search Console
    sito = SITO
    try:
        r = s.get("https://searchconsole.googleapis.com/webmasters/v3/sites")
        siti = [x["siteUrl"] for x in r.json().get("siteEntry", [])]
        dati["gsc_siti_visibili"] = siti
        if sito not in siti and siti:
            sito = next((x for x in siti if "padelmetrix" in x), siti[0])
        (a, b), (pa, pb) = periodi(3)
        dati["gsc_periodo"] = [a.isoformat(), b.isoformat(), pa.isoformat(), pb.isoformat()]
        tot = gsc(s, sito, a, b, ["date"]); totp = gsc(s, sito, pa, pb, ["date"])
        somma = lambda rr: {"clic": sum(x["clicks"] for x in rr), "impressioni": sum(x["impressions"] for x in rr),  # noqa: E731
                            "posizione": round(sum(x["position"] * x["impressions"] for x in rr) / max(1, sum(x["impressions"] for x in rr)), 1)}
        dati["gsc_totali"], dati["gsc_totali_prec"] = somma(tot), somma(totp)
        dati["gsc_query"] = gsc(s, sito, a, b, ["query"], 1000)
        dati["gsc_query_prec"] = gsc(s, sito, pa, pb, ["query"], 1000)
        dati["gsc_pagine"] = gsc(s, sito, a, b, ["page"], 50)
        dati["gsc_paesi"] = gsc(s, sito, a, b, ["country"], 10)
        dati["gsc_dispositivi"] = gsc(s, sito, a, b, ["device"], 5)
    except Exception as ex:  # noqa: BLE001
        errori.append(str(ex))
    # --- Analytics 4
    prop = os.environ.get("GA4_PROPERTY_ID", "").strip()
    if prop:
        try:
            (a, b), (pa, pb) = periodi(1)
            dati["ga_periodo"] = [a.isoformat(), b.isoformat(), pa.isoformat(), pb.isoformat()]
            M = ["activeUsers", "newUsers", "sessions", "screenPageViews", "engagementRate", "averageSessionDuration"]
            dati["ga_totali"] = (ga(s, prop, a, b, [], M) or [{}])[0]
            dati["ga_totali_prec"] = (ga(s, prop, pa, pb, [], M) or [{}])[0]
            dati["ga_giorni"] = ga(s, prop, a, b, ["date"], ["activeUsers", "sessions"], 10)
            dati["ga_canali"] = ga(s, prop, a, b, ["sessionDefaultChannelGroup"], ["sessions", "activeUsers"], 15, ordina="sessions")
            dati["ga_canali_prec"] = ga(s, prop, pa, pb, ["sessionDefaultChannelGroup"], ["sessions"], 15)
            dati["ga_fonti"] = ga(s, prop, a, b, ["sessionSource"], ["sessions"], 15, ordina="sessions")
            dati["ga_pagine"] = ga(s, prop, a, b, ["pagePath"], ["screenPageViews", "activeUsers"], 25, ordina="screenPageViews")
            dati["ga_paesi"] = ga(s, prop, a, b, ["country"], ["activeUsers"], 10, ordina="activeUsers")
            dati["ga_dispositivi"] = ga(s, prop, a, b, ["deviceCategory"], ["activeUsers"], 5)
            amazon = {"filter": {"fieldName": "linkDomain", "stringFilter": {"matchType": "CONTAINS", "value": "amazon"}}}
            dati["ga_clic_amazon"] = ga(s, prop, a, b, ["eventName"], ["eventCount"], 5, filtro=amazon)
            dati["ga_clic_amazon_prec"] = ga(s, prop, pa, pb, ["eventName"], ["eventCount"], 5, filtro=amazon)
            dati["ga_clic_amazon_pagine"] = ga(s, prop, a, b, ["pagePath"], ["eventCount"], 15, filtro=amazon, ordina="eventCount")
        except Exception as ex:  # noqa: BLE001
            errori.append(str(ex))
    else:
        errori.append("GA4_PROPERTY_ID non impostato")
    dati["errori"] = errori
    open("report_dati.json", "w").write(json.dumps(dati, ensure_ascii=False, indent=1))
    print("REPORT_JSON " + json.dumps(dati, ensure_ascii=False))
    print("REPORT_B64 " + base64.b64encode(json.dumps(dati, ensure_ascii=False).encode()).decode())
    print("ERRORI:", errori or "nessuno")
    if errori and "gsc_totali" not in dati and "ga_totali" not in dati:
        sys.exit(1)


if __name__ == "__main__":
    main()
