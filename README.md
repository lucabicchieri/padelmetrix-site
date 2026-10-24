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

## Lotto di racchette (ottobre 2026)

I dati grezzi di 251 racchette sono in `scripts/dati_lotto/*.py` (con le fonti di ogni dato).
`python3 scripts/crea_lotto.py` crea i JSON in `data/racchette/`; poi `genera_schede.py`, `genera_home.py` e
`python3 scripts/genera_sitemap.py` (sitemap.xml e robots.txt).

## Generazione completa del sito

    python3 scripts/genera_schede.py     # schede racchetta
    python3 scripts/genera_sezioni.py    # Racchette, marche, confronti, guide, Bambini
    python3 scripts/genera_geo.py        # chi siamo, report, dati aperti, glossario, domande, llms.txt
    python3 scripts/genera_legale.py     # privacy e cookie
    python3 scripts/genera_home.py
    python3 scripts/genera_sitemap.py

Ogni generatore scrive le pagine in tre lingue (`/it/`, `/en/`, `/es/`) con i tag hreflang.
Percorsi e slug tradotti sono in `scripts/sito.py` (`SEZ` e `SLUG`); i testi fissi sono nei generatori con `L(it, en, es)`.

## Traduzioni delle schede

I testi delle schede sono scritti in italiano nei JSON. Inglese e spagnolo vengono da `scripts/traduci.py`:
memoria di traduzione in `data/traduzioni/tm_pair_*.json` (formato `{"testo italiano": ["inglese", "spagnolo"]}`)
più modelli per le frasi generate automaticamente.

Dopo aver aggiunto o modificato schede:

    python3 scripts/raccogli_testi.py en   # elenca i testi senza traduzione (anche: es)

e aggiungi le frasi mancanti in un nuovo file `tm_pair_NN.json`. Un testo non tradotto resta in italiano.
