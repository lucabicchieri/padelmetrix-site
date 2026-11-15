"""Scarica pagine pubbliche di schede tecniche (elenco in un file di URL) e stampa il testo utile, riga PAG per pagina.
Serve a raccogliere le specifiche dichiarate (forma, peso, bilanciamento, materiali) per le nuove schede."""
import html
import os
import re
import sys
import time
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def testo(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA, "Accept-Language": "en,es;q=0.8"}), timeout=25)
    h = r.read().decode("utf-8", "replace")
    h = re.sub(r"(?is)<(script|style|noscript|svg)[^>]*>.*?</\1>", " ", h)
    h = re.sub(r"(?i)<(br|/p|/li|/tr|/h\d|/div|/dt|/dd|/td|/th)[^>]*>", "\n", h)
    t = html.unescape(re.sub(r"<[^>]+>", " ", h))
    t = re.sub(r"[ \t ]+", " ", t)
    return "\n".join(x.strip() for x in t.split("\n") if x.strip())


def main():
    f = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "pagine.txt")
    lim = int(os.environ.get("MAXC", "6000"))
    for u in open(f).read().split():
        try:
            t = testo(u)
            print("PAG\t" + u + "\t" + t[:lim].replace("\n", " ¶ ").replace("\t", " "))
        except Exception as ex:  # noqa: BLE001
            print("PAG\t" + u + "\tERRORE " + str(ex)[:150])
        time.sleep(1.5)


if __name__ == "__main__":
    main()
