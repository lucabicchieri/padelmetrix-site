#!/usr/bin/env python3
"""Genera sitemap.xml (con le versioni linguistiche di ogni pagina) e robots.txt."""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITO = "https://www.padelmetrix.com"
OGGI = "2026-10-24"


def main():
    voci = [{"path": f"/{l}/", "alt": {x: f"/{x}/" for x in ("it", "en", "es")}} for l in ("it", "en", "es")]
    for nome in ("pagine_schede.json", "pagine_sezioni.json", "pagine_geo.json", "pagine_legale.json", "pagine_pickleball.json", "pagine_selettore.json", "pagine_articoli.json"):
        f = ROOT / "scripts" / nome
        if f.exists():
            voci += json.loads(f.read_text(encoding="utf-8"))
    agg = {}
    for f in (ROOT / "data" / "racchette").glob("*.json"):
        d = json.loads(f.read_text(encoding="utf-8"))
        agg[d["slug"]] = d.get("aggiornato", OGGI)
    righe, visti = [], set()
    for v in voci:
        p = v["path"]
        if p in visti:
            continue
        visti.add(p)
        slug = p.strip("/").split("/")[-1]
        mod = agg.get(slug, OGGI)
        alt = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITO}{u}"/>' for l, u in v.get("alt", {}).items())
        if v.get("alt"):
            alt += f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITO}{v["alt"].get("en", p)}"/>'
        righe.append(f"  <url><loc>{SITO}{p}</loc><lastmod>{mod}</lastmod>{alt}</url>")
    (ROOT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(righe) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITO}/sitemap.xml\n", encoding="utf-8")
    print(len(righe), "URL nella sitemap")


if __name__ == "__main__":
    main()
