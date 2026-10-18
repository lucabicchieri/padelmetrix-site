# PadelMetrix

Sito di padelmetrix.com — Il Padel, Analizzato.

Per ora contiene la pagina "work in progress". Il sito completo (racchette, abbigliamento, bambini, comparatore e selettore) arriverà in questo repository e verrà pubblicato automaticamente su Cloudflare Pages.

## Schede racchetta

Ogni racchetta è un file in `data/racchette/<slug>.json` (dati tecnici + blocco `pagina` con i testi).
Per rigenerare le pagine in `racchette/<slug>/index.html`:

    python3 scripts/genera_schede.py
