"""Immagini di anteprima per i social (og:image, 1200x630) per articoli, schede racchetta e pagine generiche.

Va eseguito dopo gli altri generatori: legge data/articoli.json e il database delle racchette.
È incrementale: rigenera solo le immagini il cui contenuto è cambiato (data/og_manifest.json).
Richiede Playwright (Chromium) e il font Space Grotesk installato sul sistema.
"""
import hashlib
import html
import json

import sito as S
from comune import racket_svg

ROOT = S.ROOT
OUT = ROOT / "og"
MAN = ROOT / "data" / "og_manifest.json"
VERSIONE = "1"
CAT = {"giocatori": ("Giocatori", "Players", "Jugadores", "Joueurs"), "regali": ("Regali di Natale", "Christmas gifts", "Regalos de Navidad", "Cadeaux de Noël"),
       "novita": ("Novità e confronti", "New and compared", "Novedades y comparativas", "Nouveautés et comparatifs"), "guide": ("Guide", "Guides", "Guías", "Guides")}
CLAIM = {"it": "Il padel, analizzato.", "en": "Padel, analysed.", "es": "El pádel, analizado.", "fr": "Le padel, analysé."}
SOTTO = {"it": "Schede, confronti e guide per scegliere la racchetta", "en": "Specs, comparisons and guides to choose your racket",
         "es": "Fichas, comparativas y guías para elegir tu pala", "fr": "Fiches, comparatifs et guides pour choisir votre raquette"}
LI = {"it": 0, "en": 1, "es": 2, "fr": 3}

BASE = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1200px;height:630px;overflow:hidden;font-family:'Space Grotesk','IBM Plex Sans',sans-serif}
.c{width:1200px;height:630px;position:relative;overflow:hidden;padding:64px 72px;display:flex;flex-direction:column}
.k{font-size:26px;font-weight:700;letter-spacing:.1em;text-transform:uppercase}
h1{font-weight:700;letter-spacing:-.025em;line-height:1.05;margin-top:22px;max-width:860px}
.wm{margin-top:auto;font-size:34px;letter-spacing:-.03em;display:flex;align-items:baseline}.wm span{margin-left:4px}.wm b{font-weight:700}.wm i{font-style:normal;font-weight:400}
.d{position:absolute;border-radius:50%}
.scuro{background:#0F3D2E;color:#FAFAF7}.scuro .k,.scuro .wm i{color:#C6F432}
.lime{background:#C6F432;color:#0B2E23}.lime .k{color:#0F3D2E}
.chiaro{background:#F1F5EE;color:#0F3D2E}.chiaro .k{color:#3C6B57}
.campo{background:#134A38;color:#FAFAF7}.campo .k,.campo .wm i{color:#C6F432}
.chip{display:inline-block;font-size:28px;font-weight:500;border:2px solid #0F3D2E;border-radius:99px;padding:6px 22px;margin:26px 12px 0 0}"""
DECO = {
    "giocatori": ('scuro', '<div class="d" style="width:520px;height:520px;right:-150px;top:-190px;border:84px solid #C6F432"></div><div class="d" style="width:86px;height:86px;right:210px;bottom:70px;background:#C6F432"></div>'),
    "regali": ('lime', '<div class="d" style="border-radius:22px;width:300px;height:230px;right:90px;bottom:-30px;background:#0F3D2E"></div><div class="d" style="border-radius:16px;width:350px;height:74px;right:65px;bottom:170px;background:#0F3D2E"></div><div class="d" style="border-radius:0;width:40px;height:330px;right:220px;bottom:-30px;background:#FAFAF7"></div>'),
    "novita": ('chiaro', '<div class="d" style="width:270px;height:330px;border-radius:135px 135px 160px 160px;right:110px;top:80px;background:#0F3D2E;transform:rotate(16deg)"></div><div class="d" style="width:60px;height:60px;right:120px;top:84px;background:#C6F432"></div><div class="d" style="border-radius:14px;width:46px;height:170px;right:285px;top:380px;background:#0F3D2E;transform:rotate(16deg)"></div>'),
    "guide": ('campo', '<div class="d" style="border-radius:16px;width:560px;height:360px;right:-120px;top:140px;border:6px solid rgba(198,244,50,.7)"></div><div class="d" style="border-radius:0;width:6px;height:420px;right:160px;top:110px;background:#fff"></div><div class="d" style="width:46px;height:46px;right:40px;top:230px;background:#C6F432"></div>'),
}


def pagina(corpo):
    return f'<!doctype html><html><head><meta charset="utf-8"><style>{BASE}</style></head><body>{corpo}</body></html>'


def wm():
    return '<div class="wm"><b>padel</b><i>metrix</i><span style="font-size:24px;opacity:.75">.com</span></div>'


def art_html(titolo, cat, l):
    cls, deco = DECO[cat]
    n = len(titolo)
    fs = 78 if n < 45 else 66 if n < 70 else 56 if n < 95 else 48
    return pagina(f'<div class="c {cls}">{deco}<div class="k">{html.escape(CAT[cat][LI[l]])}</div><h1 style="font-size:{fs}px;max-width:{760 if cat != "giocatori" else 820}px">{html.escape(titolo)}</h1>{wm()}</div>')


def racchetta_html(n):
    nome = n["nome"]
    fs = 92 if len(nome) < 16 else 76 if len(nome) < 26 else 60
    chip = f'<span class="chip">{html.escape(n["peso"].split(" (")[0])}</span>' if n.get("peso") else ""
    svg = racket_svg(n["forma"], 250, n["titolo"])
    return pagina(f'<div class="c chiaro"><div class="d" style="width:520px;height:520px;right:40px;top:55px;background:#E2EADD"></div>'
                  f'<div style="position:absolute;right:175px;top:95px">{svg}</div>'
                  f'<div class="k">{html.escape(n["marca"])} · {n["anno"]}</div><h1 style="font-size:{fs}px;max-width:640px">{html.escape(nome)}</h1><div>{chip}</div>{wm()}</div>')


def quadrata_html(n):
    """Immagine quadrata 1200x1200 per la scheda: disegno della forma su fondo chiaro, nome in basso."""
    svg = racket_svg(n["forma"], 560, n["titolo"])
    return pagina(f'<div class="c" style="width:1200px;height:1200px;padding:0;background:radial-gradient(circle at 50% 42%,#EEF3EA,#DDE6D8)">'
                  f'<div style="position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center">{svg}</div>'
                  f'<div style="position:absolute;left:70px;right:70px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end">'
                  f'<div style="font-size:40px;line-height:1.15;color:#0F3D2E;font-weight:700;max-width:760px">{html.escape(n["marca"])}<br>'
                  f'<span style="font-weight:400">{html.escape(n["nome"])}</span></div>'
                  f'<div style="font-size:30px;color:#0F3D2E;opacity:.7"><b>padel</b>metrix</div></div></div>')


def generica_html(l):
    cls, deco = DECO["guide"]
    return pagina(f'<div class="c {cls}">{deco}<div class="k">{html.escape(CLAIM[l])}</div>'
                  f'<h1 style="font-size:104px"><span style="font-weight:700">padel</span><span style="font-weight:400;color:#C6F432">metrix</span></h1>'
                  f'<p style="font-size:34px;margin-top:26px;max-width:640px;line-height:1.25;font-family:sans-serif">{html.escape(SOTTO[l])}</p></div>')


def lavori():
    out = {}
    for l in S.LINGUE:
        out[f"padelmetrix-{l}.jpg"] = generica_html(l)
    f = ROOT / "data" / "articoli.json"
    for a in (json.loads(f.read_text(encoding="utf-8")) if f.exists() else []):
        for l, tit in a["titolo"].items():
            out[f"a/{a['slug']}-{l}.jpg"] = art_html(tit, a.get("cat", "guide"), l)
    S.set_lang("it")
    for n in S.carica():
        out[f"r/{n['slug']}.jpg"] = racchetta_html(n)
        out[f"q/{n['slug']}.jpg"] = quadrata_html(n)
    return out


def main():
    from playwright.sync_api import sync_playwright
    jobs = lavori()
    man = json.loads(MAN.read_text(encoding="utf-8")) if MAN.exists() else {}
    nuovo, fare = {}, []
    for rel, htm in jobs.items():
        h = hashlib.sha1((VERSIONE + htm).encode("utf-8")).hexdigest()[:16]
        nuovo[rel] = h
        if man.get(rel) != h or not (OUT / rel).exists():
            fare.append((rel, htm))
    if fare:
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            for rel, htm in fare:
                dest = OUT / rel
                dest.parent.mkdir(parents=True, exist_ok=True)
                q = rel.startswith("q/")
                pg.set_viewport_size({"width": 1200, "height": 1200 if q else 630})
                pg.set_content(htm)
                pg.evaluate("document.fonts.ready")
                pg.screenshot(path=str(dest), type="jpeg", quality=80)
                if q:  # versione leggera 600 px in WebP per la pagina
                    from PIL import Image
                    w = OUT / "q6" / (dest.stem + ".webp")
                    w.parent.mkdir(parents=True, exist_ok=True)
                    Image.open(dest).resize((600, 600), Image.LANCZOS).save(w, "WEBP", quality=80)
            b.close()
    for rel in set(man) - set(nuovo):  # immagini di pagine che non esistono più
        (OUT / rel).unlink(missing_ok=True)
    MAN.write_text(json.dumps(dict(sorted(nuovo.items())), indent=0), encoding="utf-8")
    print(f"{len(fare)} anteprime social generate, {len(jobs)} totali")


if __name__ == "__main__":
    main()
