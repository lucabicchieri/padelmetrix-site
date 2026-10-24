#!/usr/bin/env python3
"""Genera sitemap.xml e robots.txt con le home e tutte le schede racchetta."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://www.padelmetrix.com"


def main():
    urls = []
    for l in ("it", "en", "es"):
        urls.append((f"{SITO}/{l}/", "2026-10-24"))
    for f in sorted((ROOT / "data" / "racchette").glob("*.json")):
        d = json.loads(f.read_text(encoding="utf-8"))
        if "pagina" in d:
            urls.append((f"{SITO}/it/racchette/{d['slug']}/", d.get("aggiornato", "2026-10-24")))
    body = "\n".join(f"  <url><loc>{u}</loc><lastmod>{m}</lastmod></url>" for u, m in urls)
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + "\n</urlset>\n",
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITO}/sitemap.xml\n", encoding="utf-8")
    print(len(urls), "URL nella sitemap")


if __name__ == "__main__":
    main()
