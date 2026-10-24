def PF(slug, lang="en"):
    return ("Padelful", f"https://www.padelful.com/{lang}/{'rackets' if lang=='en' else 'palas'}/{slug}")
def SC(slug, tot, v, lang="en"):
    return dict(fonte="Padelful", url=PF(slug, lang)[1], tot=tot, v=v)
OX = ("PadelPROShop", "https://padelproshop.com/en/blogs/blog/nueva-coleccion-oxdog-2026-guia-completa")
def DS(n, slug, f, p, nu, c, ta, l, st, pr, d, tot, v, g=None, lang="en", b=None):
    r = dict(m="Drop Shot", n=n, a=2026, f=f, p=p, nu=nu, c=c, t="Carbonio", ta=ta, l=l, st=st, pr=pr, d=d,
             src=[PF(slug, lang)], sc=SC(slug, tot, v, lang))
    if g: r["g"] = g
    if b: r["b"] = b
    return r
R = [
 DS("Axion Comfort 1.0", "drop-shot-axion-comfort-1-0-2026", "rotonda", "350–370 g", "EVA Pro High Density", "Carbonio 3K", "medio", "intermedio", "controllo", 239.95,
    "Rotonda comoda e controllata, a suo agio in blocchi, volée e bandeja; poca potenza pura.", 8.2, [8, 8.1, 8.4, 8.4, 8.2], b="neutro"),
 DS("Canyon Pro Comfort 2.0", "drop-shot-canyon-pro-comfort-2-0-2026", "rotonda", "350–370 g", "EVA Pro High Density", "Carbonio 3K", "medio", "intermedio", "controllo", 229.95,
    "Rotonda di controllo con difesa stabile, sweet spot tollerante e maneggevolezza a rete; potenza limitata.", 8.3, [6.8, 9.4, 8.5, 8.6, 8]),
 DS("Explorer Pro Attack Soft", "drop-shot-explorer-pro-attack-soft-2026", "goccia", "350–370 g", "EVA Soft Low Density", "Carbonio 12K", "medio-morbido", "intermedio-avanzato", "polivalente", 279.95,
    "Goccia comoda e amica del braccio, maneggevole a rete e in difesa; manca di spinta negli smash pesanti.", 8.3, [7.6, 8.7, 9.1, 8.1, 8]),
 DS("Furia Attack 2.0", "drop-shot-furia-attack-2-0-2026", "rotonda", "350–370 g", "EVA Pro High Density", "Carbonio 18K", "medio", "intermedio-avanzato", "polivalente", 299.95,
    "Rotonda dal tatto medio, equilibrata e controllata, forte a rete e stabile da fondo; poca potenza facile.", 8.2, [8, 8.1, 8.6, 8.6, 7.9]),
 DS("Explorer Soft Women", "drop-shot-explorer-soft-women-2026", "goccia", "350–370 g", "EVA Pro High Density", "Carbonio 3K", "medio", "intermedio", "polivalente", None,
    "Maneggevole e comoda, con uscita di palla viva e sweet spot tollerante; poca potenza per chiudere.", 7.9, [7.9, 7.3, 8.4, 8.1, 8]),
 DS("Explorer Pro Comfort 2.0", "drop-shot-explorer-pro-comfort-2-0-2026-lucas-campagnolo", "rotonda", "350–370 g", "EVA Pro High Density", "Carbonio 3K", "medio", "intermedio", "polivalente", None,
    "Rotonda facile da gestire con uscita di palla viva e sweet spot generoso, adatta al gioco settimanale.", 8.0, [7.1, 7.3, 8.4, 8.6, 8.6], g="Lucas Campagnolo"),
 DS("Cyber Attack", "drop-shot-cyber-attack-2026", "goccia", "350–370 g", "EVA Pro High Density", "Carbonio 24K", "medio-duro", "intermedio", "polivalente", 199,
    "Goccia dal controllo prima di tutto: risposta ferma e precisa, maneggevole e tollerante; poca potenza gratuita.", 8.5, [7.3, 8.9, 8.7, 9, 8.5]),
 DS("Flame Soft", "drop-shot-flame-soft-2026", "goccia", "350–370 g", "EVA Soft Low Density", "Carbonio 12K", "medio-morbido", "intermedio", "controllo", 160,
    "Goccia di controllo dal tatto medio-morbido, sweet spot generoso e facile da muovere.", 8.0, [8, 7.3, 8.9, 8, 7.9], lang="es"),
 dict(m="Babolat", n="Viper Soft Juan Lebrón 3.0", a=2026, g="Juan Lebrón", f="diamante", p="365 g", b="alto", nu="Black EVA", c="Carbonio morbido (Soft Carbon)", t="Carbonio", ta="medio", l="avanzato", st="offensivo",
      d="Una Viper più morbida, con uscita di palla più facile e impatto più tollerante, ma sempre pesante in testa ed esigente.",
      src=[PF("babolat-viper-soft-3-0-2026-juan-lebron")], sc=SC("babolat-viper-soft-3-0-2026-juan-lebron", 8.6, [9.6, 8.5, 8.7, 7.6, 8.7])),
 dict(m="Babolat", n="Viper Juan Lebrón 3.0", a=2026, g="Juan Lebrón", f="diamante", p="370 g", b="alto", nu="Black EVA", c="Carbonio 3K", t="Carbonio", ta="duro", l="avanzato", st="offensivo",
      d="Diamante rigida e offensiva che eccelle a rete e negli smash, ma chiede una tecnica precisa in difesa.",
      src=[PF("babolat-viper-3-0-2026-juan-lebron")], sc=SC("babolat-viper-3-0-2026-juan-lebron", 8.7, [9.8, 9.4, 8.2, 7.6, 8.6]), simili_fissi=["babolat-viper-juan-lebron-3-1-2027"]),
 # Oxdog dalla guida PadelPROShop
 dict(m="Oxdog", n="Pure Court", a=2026, f="ibrida", fn="ibrida tendente alla rotonda", nu="gomma morbida", c="Fibra di vetro", ta="medio-morbido", l="intermedio", st="controllo",
      d="La Pure più confortevole: assorbe parte dell'impatto e perdona i colpi decentrati. Per controllo, difesa e scambi lunghi.", src=[OX]),
 dict(m="Oxdog", n="Pure Pro+", a=2026, ta="medio", l="intermedio-avanzato", st="controllo",
      d="Racchetta di controllo più ferma, per chi vuole più precisione nei colpi offensivi senza un modello estremo.", src=[OX]),
 dict(m="Oxdog", n="Hyper Tour X", a=2026, nu="gomma di durezza media", c="Carbonio HES", ta="medio", l="intermedio", st="polivalente",
      d="Polivalente equilibrata per partite al circolo e campionati, prevedibile anche sui colpi un po' decentrati.", src=[OX]),
 dict(m="Oxdog", n="Hyper Pro 2.0", a=2026, nu="gomma Medium Plus", c="Carbonio HES", ta="medio-secco", l="intermedio-avanzato", st="polivalente",
      d="Un passo in più di rigidità: più spinta in bandeja, víbora e colpi a media altezza.", src=[OX]),
 dict(m="Oxdog", n="Hyper Pro+ 2.0", a=2026, ta="fermo", l="avanzato", st="polivalente",
      d="Una Hyper più rigida, stabile quando lo scambio accelera.", src=[OX]),
 dict(m="Oxdog", n="Ultimate NXT-Gen", a=2026, f="diamante", ta="morbido", l="intermedio", st="offensivo",
      d="Porta d'ingresso alla forma diamante, con peso contenuto e più margine d'errore; adatta anche ai ragazzi.", src=[OX]),
 dict(m="Oxdog", n="Ultimate Tour X", a=2026, f="diamante", l="intermedio-avanzato", st="polivalente",
      d="Diamante con potenza extra che consente ancora una difesa ordinata: un ponte tra attacco e controllo.", src=[OX, PF("oxdog-ultimate-tour-x-2026")]),
]
