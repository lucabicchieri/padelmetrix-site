"""Legge schede padelful.com (URL in un file) ed estrae solo i dati tecnici e i punteggi, riga PF con JSON.

Campi: url, titolo, voto, punteggi (potenza, controllo, uscita di palla, maneggevolezza, sweet spot),
forma, peso, tatto, nucleo, piatti, telaio, bilanciamento e livello se presenti. I testi delle recensioni non vengono copiati."""
import html
import json
import re
import sys
import time
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
CAMPI = {"Shape": "forma", "Weight": "peso", "Touch": "tatto", "Core": "nucleo", "Faces": "piatti", "Frame": "telaio",
         "Balance": "bilanciamento", "Level": "livello", "Thickness": "spessore", "Surface": "superficie"}
VOCI = ["Power", "Control", "Rebound", "Maneuverability", "Sweet spot"]


def righe(u):
    h = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "en"}), timeout=25).read().decode("utf-8", "replace")
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<(br|/p|/li|/tr|/h\d|/div|/dt|/dd|/td|/th|/span|/a|/button)[^>]*>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    return [x.strip() for x in re.sub(r"[ \t ]+", " ", t).split("\n") if x.strip()]


def estrai(u):
    L = righe(u)
    d = {"url": u}
    tit = next((x for x in L if x.endswith(": Review and Best Price")), "")
    d["titolo"] = tit.replace(": Review and Best Price", "")
    for i, x in enumerate(L[:-1]):
        if x == "Our Take" and i > 0 and re.fullmatch(r"\d+(\.\d)?", L[i - 1]):
            d["voto"] = float(L[i - 1])
        for v in VOCI:
            m = re.fullmatch(re.escape(v) + r" (\d+(\.\d)?)", x)
            if m:
                d.setdefault("punteggi", {})[v] = float(m.group(1))
        if x in CAMPI and CAMPI[x] not in d and len(L[i + 1]) < 90:
            d[CAMPI[x]] = L[i + 1]
    return d


def main():
    for u in open(sys.argv[1]).read().split():
        try:
            print("PF\t" + json.dumps(estrai(u), ensure_ascii=False))
        except Exception as ex:  # noqa: BLE001
            print("PF\t" + json.dumps({"url": u, "errore": str(ex)[:120]}))
        time.sleep(1.2)


if __name__ == "__main__":
    main()
