"""Legge la sitemap di padelful.com e stampa gli URL delle schede racchetta (righe URL)."""
import re
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "replace")


def main():
    vist, coda, out = set(), ["https://www.padelful.com/sitemap.xml", "https://www.padelful.com/sitemap-index.xml", "https://www.padelful.com/robots.txt"], set()
    while coda:
        u = coda.pop(0)
        if u in vist:
            continue
        vist.add(u)
        try:
            t = get(u)
        except Exception as ex:  # noqa: BLE001
            print("ERR", u, ex)
            continue
        for m in re.findall(r"Sitemap:\s*(\S+)", t) + re.findall(r"<loc>\s*([^<]+?)\s*</loc>", t):
            if m.endswith(".xml") or "sitemap" in m:
                coda.append(m)
            elif "/en/rackets/" in m:
                out.add(m)
    for u in sorted(out):
        print("URL\t" + u)
    print("TOT", len(out))


if __name__ == "__main__":
    main()
