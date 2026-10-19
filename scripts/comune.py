"""Elementi condivisi dai generatori del sito (illustrazioni, lingue, URL)."""

LINGUE = ["it", "en", "es"]

# Percorsi delle sezioni per lingua
SEZIONI = {
    "it": {"racchette": "racchette", "abbigliamento": "abbigliamento", "bambini": "bambini", "confronta": "confronta", "selettore": "trova-la-tua-racchetta", "chi": "chi-siamo", "privacy": "privacy", "cookie": "cookie"},
    "en": {"racchette": "rackets", "abbigliamento": "clothing", "bambini": "kids", "confronta": "compare", "selettore": "racket-finder", "chi": "about", "privacy": "privacy", "cookie": "cookies"},
    "es": {"racchette": "palas", "abbigliamento": "ropa", "bambini": "ninos", "confronta": "comparar", "selettore": "encuentra-tu-pala", "chi": "quienes-somos", "privacy": "privacidad", "cookie": "cookies"},
}


def url(lang, sezione, slug=None):
    base = f"/{lang}/{SEZIONI[lang][sezione]}/"
    return base + (f"{slug}/" if slug else "")


def racket_svg(forma, width=150, label=None):
    """Illustrazione di una racchetta in base alla forma: diamante, rotonda, goccia."""
    teste = {
        # tracciati della testa della racchetta, viewBox 0 0 200 300
        "rotonda": "M100 18 C150 18 178 52 178 104 C178 156 146 188 100 196 C54 188 22 156 22 104 C22 52 50 18 100 18 Z",
        "goccia": "M100 14 C146 14 176 44 178 92 C180 140 150 182 100 198 C50 182 20 140 22 92 C24 44 54 14 100 14 Z",
        "diamante": "M100 14 C128 14 156 30 170 58 C182 82 178 116 162 146 C146 174 122 190 100 198 C78 190 54 174 38 146 C22 116 18 82 30 58 C44 30 72 14 100 14 Z",
    }
    d = teste.get(forma, teste["goccia"])
    fori = []
    for row, (y, xs) in enumerate([(62, [76, 100, 124]), (84, [64, 88, 112, 136]), (106, [64, 88, 112, 136]), (128, [76, 100, 124]), (150, [88, 112])]):
        for x in xs:
            fori.append(f'<circle cx="{x}" cy="{y}" r="4.5" fill="#FAFAF7" fill-opacity="0.55"/>')
    lab = f'<title>{label}</title>' if label else ""
    return (f'<svg viewBox="0 0 200 300" width="{width}" role="img" aria-label="{label or "Illustrazione racchetta"}">{lab}'
            f'<path d="{d}" fill="#0F3D2E"/>'
            f'<path d="{d}" fill="none" stroke="#C6F432" stroke-width="5" stroke-opacity="0.9"/>'
            + "".join(fori) +
            '<path d="M84 194 L100 214 L116 194 Z" fill="#0F3D2E"/>'
            '<rect x="88" y="208" width="24" height="78" rx="8" fill="#0F3D2E"/>'
            '<rect x="88" y="236" width="24" height="5" fill="#C6F432" fill-opacity="0.8"/>'
            '<rect x="88" y="252" width="24" height="5" fill="#C6F432" fill-opacity="0.8"/>'
            '<circle cx="150" cy="40" r="15" fill="#C6F432"/>'
            '</svg>')
