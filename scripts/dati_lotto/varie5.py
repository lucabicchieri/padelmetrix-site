def PF(slug, lang="en"):
    return ("Padelful", f"https://www.padelful.com/{lang}/{'rackets' if lang=='en' else 'palas'}/{slug}")
def SC(slug, tot, v, lang="en"):
    return dict(fonte="Padelful", url=PF(slug, lang)[1], tot=tot, v=v)
R = [
 dict(m="Lok", n="Easy Flow Gen 2", a=2026, f="rotonda", p="360–375 g", nu="EVA", c="Carbonio flessibile", t="Carbonio", ta="medio-morbido", l="intermedio", st="controllo", pr=130,
      d="Rotonda facile da gestire con sweet spot ampio, che favorisce controllo difensivo e piazzamento più della potenza.",
      src=[PF("lok-easy-flow-gen-2-2026")], sc=SC("lok-easy-flow-gen-2-2026", 8.2, [7, 7.7, 8.8, 8.5, 8.9])),
 dict(m="Lok", n="Easy Hype Gen 2", a=2026, f="diamante", p="360–375 g", nu="EVA", c="Carbonio flessibile", t="Carbonio", ta="medio-morbido", l="intermedio", st="offensivo", pr=130,
      d="Diamante d'attacco tollerante con rimbalzo vivace e sweet spot generoso, a scapito di rapidità e tocco.",
      src=[PF("lok-easy-hype-gen-2-2026")], sc=SC("lok-easy-hype-gen-2-2026", 7.9, [7.8, 7.6, 8.9, 7.3, 8])),
 dict(m="Lok", n="Maxx Hype Gen 2", a=2026, g="Mike Yanguas", f="diamante", p="360–375 g", nu="EVA", c="Carbonio C18", t="Carbonio", ta="medio-duro", l="avanzato", st="offensivo",
      d="Diamante d'attacco potente con sweet spot abbastanza ampio; chiede impatti puliti e anticipati e aiuta poco in difesa.",
      src=[PF("lok-maxx-hype-gen-2-2026-mike-yanguas")], sc=SC("lok-maxx-hype-gen-2-2026-mike-yanguas", 8.4, [9.6, 9, 7.7, 7.6, 8])),
 dict(m="Lok", n="Maxx Flow Gen 2", a=2026, f="rotonda", p="360–375 g", nu="EVA", c="Carbonio C18", t="Carbonio", ta="medio-duro", l="avanzato", st="controllo", pr=169,
      d="Rotonda di controllo con sweet spot ampio e risposta stabile; poca potenza facile.",
      src=[PF("lok-maxx-flow-gen-2-2026")], sc=SC("lok-maxx-flow-gen-2-2026", 8.5, [8.4, 9.1, 7.5, 8.4, 8.9])),
 dict(m="Royal Padel", n="M27 Light", a=2026, f="rotonda", p="350–365 g", b="medio-basso", nu="Polietilene ad alta densità", c="Carbonio 3K", t="Carbonio", ta="medio-morbido", l="intermedio", st="controllo",
      d="Rotonda di controllo leggera e morbida con sweet spot ampio, ottima in difesa e a rete; poca potenza nello smash.",
      src=[PF("royal-padel-m27-light-2026")], sc=SC("royal-padel-m27-light-2026", 8.5, [6.6, 9.1, 8.9, 9.1, 9])),
 dict(m="Royal Padel", n="M27 R-Ace", a=2026, f="diamante", b="alto", nu="EVA Mid Hard", t="Carbonio 3K", ta="fermo", l="avanzato", st="offensivo", pr=350,
      d="Diamante offensiva con bilanciamento alto e nucleo EVA duro, per chi vuole dominare da rete.",
      src=[("Ipontennis", "https://www.ipontennis.com/en/palas-de-padel/royal-padel-m27-r-ace-2026")]),
 dict(m="Wilson", n="Blade LS V4", a=2026, f="goccia", p="355 g", nu="Soft EVA", c="Fibra di vetro", t="Carbonio tubolare C2", ta="morbido", l="intermedio", st="controllo",
      d="Racchetta leggera e morbida di controllo, con buona uscita di palla e agilità a rete; poca potenza per chiudere.",
      src=[PF("wilson-blade-ls-v4-2026", "es")], sc=SC("wilson-blade-ls-v4-2026", 8.4, [6.7, 8.1, 9.1, 9.2, 8.8], "es")),
 dict(m="Joma", n="Slam Pro Iconic", a=2026, f="goccia", p="355–365 g", b="medio-alto", nu="Black EVA", c="Carbonio 3K", t="Carbonio 3K", ta="medio-morbido", l="intermedio-avanzato", st="polivalente",
      d="Goccia versatile con potenza ferma, volée solide e buona maneggevolezza; i colpi decentrati possono vibrare.",
      src=[PF("joma-slam-pro-iconic-2026", "es")], sc=SC("joma-slam-pro-iconic-2026", 8.2, [8.1, 8, 8.5, 8.4, 8], "es")),
 dict(m="Varlion", n="LW Carbon Ti", a=2026, f="rotonda", p="345–365 g", b="basso", nu="EVA media (SoftColor)", c="Carbonio e fibra di vetro con biossido di titanio", t="Esagonale con ponte Hexaforce", l="avanzato", st="controllo",
      d="Rotonda di controllo per avanzati che vincono con il piazzamento: maneggevole e con sweet spot tollerante.",
      src=[("Padel Gear", "https://www.padelgear.co.za/products/varlion-lw-carbon-ti-2026")]),
]
