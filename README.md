# PadelMetrix

Sito di padelmetrix.com — Il Padel, Analizzato.

Sito multilingua: home in `/it/`, `/en/`, `/es/`; la radice reindirizza in base alla lingua del browser. Pubblicato automaticamente su Cloudflare Pages.

## Schede racchetta

Ogni racchetta è un file in `data/racchette/<slug>.json` (dati tecnici + blocco `pagina` con i testi).
Per rigenerare le pagine in `it/racchette/<slug>/index.html`:

    python3 scripts/genera_schede.py

## Home

    python3 scripts/genera_home.py

Genera `/it/`, `/en/`, `/es/`, la pagina radice e `_redirects`.
