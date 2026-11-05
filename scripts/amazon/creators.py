"""Client minimo per la Amazon Creators API (catalogo prodotti per affiliati).

Credenziali dai segreti GitHub: CREATORS_CREDENTIAL_ID, CREATORS_CREDENTIAL_SECRET
(facoltativo CREATORS_VERSION, es. "3.2" per l'Europa). Non stampa mai le credenziali.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

API = "https://creatorsapi.amazon/catalog/v1/getItems"
# (versione, endpoint token, formato corpo, scope)
TOKEN_OPZIONI = {
    "3": [("https://api.amazon.co.uk/auth/o2/token", "json", "creatorsapi::default"),
          ("https://api.amazon.co.uk/auth/o2/token", "form", "creatorsapi::default")],
    "2": [("https://creatorsapi.auth.eu-south-2.amazoncognito.com/oauth2/token", "form", "creatorsapi/default")],
}
RISORSE = ["images.primary.large", "images.primary.medium", "itemInfo.title", "offersV2.listings.price"]


def _post(url, dati, headers):
    req = urllib.request.Request(url, data=dati, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def token(log=print):
    cid, sec = os.environ.get("CREATORS_CREDENTIAL_ID"), os.environ.get("CREATORS_CREDENTIAL_SECRET")
    if not cid or not sec:
        sys.exit("Credenziali mancanti nei segreti")
    ver = os.environ.get("CREATORS_VERSION", "")
    ordine = [ver[:1]] if ver[:1] in TOKEN_OPZIONI else ["3", "2"]
    for maj in ordine:
        for url, fmt, scope in TOKEN_OPZIONI[maj]:
            campi = {"grant_type": "client_credentials", "client_id": cid, "client_secret": sec, "scope": scope}
            if fmt == "json":
                body, ct = json.dumps(campi).encode(), "application/json"
            else:
                body, ct = urllib.parse.urlencode(campi).encode(), "application/x-www-form-urlencoded"
            st, txt = _post(url, body, {"Content-Type": ct})
            log(f"token v{maj} {urllib.parse.urlparse(url).netloc} ({fmt}): HTTP {st}")
            if st == 200:
                return json.loads(txt)["access_token"], (ver or {"3": "3.2", "2": "2.2"}[maj])
            try:
                err = json.loads(txt)
                log("  errore:", err.get("error"), "-", str(err.get("error_description", ""))[:150])
            except Exception:
                log("  risposta non JSON")
    sys.exit("Nessun endpoint token ha funzionato")


def get_items(asins, tok, ver, tag="padelmetrix-21", market="www.amazon.it", log=print):
    body = json.dumps({"itemIds": asins, "itemIdType": "ASIN", "marketplace": market,
                       "partnerTag": tag, "resources": RISORSE}).encode()
    out = None
    for auth in (f"Bearer {tok}, Version {ver}", f"Bearer {tok}"):
        st, txt = _post(API, body, {"Authorization": auth, "Content-Type": "application/json", "x-marketplace": market})
        log(f"getItems ({'con' if 'Version' in auth else 'senza'} Version): HTTP {st}")
        if st == 200:
            return json.loads(txt)
        out = txt[:400]
    log("  risposta:", out)
    return None


if __name__ == "__main__":
    asins = sys.argv[1:] or ["B0FPT5S2P7", "B0FPTM52HS"]
    t, v = token()
    res = get_items(asins, t, v)
    if res:
        items = (res.get("itemsResult") or {}).get("items") or res.get("items") or []
        print("chiavi risposta:", list(res))
        for it in items:
            img = (((it.get("images") or {}).get("primary") or {}).get("large") or {})
            titolo = (((it.get("itemInfo") or {}).get("title") or {}).get("displayValue"))
            print(it.get("asin"), "|", titolo, "|", img.get("url"), img.get("width"), img.get("height"))
        print("errori:", json.dumps(res.get("errors"))[:400] if res.get("errors") else "nessuno")
        os.makedirs("amazon-out", exist_ok=True)
        json.dump(res, open("amazon-out/risposta.json", "w"), ensure_ascii=False, indent=1)
