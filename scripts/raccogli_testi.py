"""Elenca i testi delle schede che la memoria di traduzione non copre ancora."""
import json, glob, sys
import traduci as T

def campi(p):
    out = [p.get("lead"), p.get("sintesi"), p.get("avviso_html"), p.get("eyebrow"), p.get("nota_prezzi"), p.get("nota_specifiche_html")]
    for k in ("pro", "contro", "adatta", "non_adatta", "chips"):
        out += p.get(k, [])
    for k, v in p.get("specifiche", []):
        out += [k] + ([] if k in ("Marca", "Modello", "Giocatore", "Linea") else [v])
    if p.get("tratti"):
        out += [p["tratti"]["titolo"], p["tratti"]["nota_html"]] + p["tratti"]["voci"]
    if p.get("valutazioni"):
        out += [p["valutazioni"]["titolo"], p["valutazioni"]["nota_html"]] + [v["nome"] for v in p["valutazioni"]["voci"]]
    for s in p.get("negozi", []):
        out += [s["nota"], s["pulsante"]]
    for r in p.get("recensioni", []):
        out += [r.get("voto"), r.get("voto_dettaglio"), r.get("sintesi")]
    for s in p.get("simili", []):
        out += [s["testo"]]
    return [x for x in out if x]

for f in sorted(glob.glob("../data/racchette/*.json")):
    p = json.load(open(f))["pagina"]
    for x in campi(p):
        for l in T.LANGS:
            T.t(x, l)
lang = sys.argv[1] if len(sys.argv) > 1 else "en"
m = sorted(T.MANCANTI[lang])
print(len(m), sum(len(x.split()) for x in m), file=sys.stderr)
json.dump(m, open(f"/tmp/claude-0/-home-claude/4f320c5c-3ec7-574f-9d0f-809318da5085/scratchpad/mancanti_{lang}.json", "w"), ensure_ascii=False, indent=0)
