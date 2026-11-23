"""Font ospitati su padelmetrix.com (Space Grotesk e IBM Plex Sans, licenza SIL OFL, da @fontsource).
FONT_HEAD va nel <head> di ogni pagina al posto del link a Google Fonts."""
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
EXT = "U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF"


def _ff(fam, file, w):
    out = []
    for sub, rng in (("latin", LAT), ("latin-ext", EXT)):
        out.append(f"@font-face{{font-family:'{fam}';font-style:normal;font-display:swap;font-weight:{w};"
                   f"src:url(/font/{file}-{sub}-{w}-normal.woff2) format('woff2');unicode-range:{rng}}}")
    return "".join(out)


_CSS = "".join(_ff("Space Grotesk", "space-grotesk", w) for w in (400, 500, 700)) + "".join(_ff("IBM Plex Sans", "ibm-plex-sans", w) for w in (400, 500, 600))
FONT_HEAD = ('<link rel="preload" href="/font/ibm-plex-sans-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             '<link rel="preload" href="/font/space-grotesk-latin-700-normal.woff2" as="font" type="font/woff2" crossorigin>\n'
             f"<style>{_CSS}</style>")
