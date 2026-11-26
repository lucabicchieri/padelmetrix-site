"""Articolo: racchette da pickleball per principianti, dai dati del nostro catalogo. Importato da genera_articoli."""
import sito as S
from sito import L, P, e

PB_SLUG = "racchette-pickleball-principianti"
S.SLUG[PB_SLUG] = ("pickleball-paddles-for-beginners", "palas-pickleball-principiantes")
S.SLUG_FR[PB_SLUG] = "raquettes-pickleball-debutants"

LIV = {"principiante": ("principiante", "beginner", "principiante", "débutant"),
       "principiante-intermedio": ("principiante-intermedio", "beginner to intermediate", "principiante-intermedio", "débutant à intermédiaire")}
FO = {"standard": ("standard", "standard", "estándar", "standard"), "larga": ("larga", "widebody", "ancha", "large"),
      "allungata": ("allungata", "elongated", "alargada", "allongée"), "ibrida": ("ibrida", "hybrid", "híbrida", "hybride")}


def art_pickleball_principianti(db, fonte, faq, scrivi_articolo, tab):
    import dati_pickleball as DP
    import genera_pickleball as GP
    li = S.LINGUE.index(S.lang())
    sel = [p for p in DP.P if p["livello"] in LIV]
    sel.sort(key=lambda p: (p.get("prezzo_usd") or 999))

    def peso(p):
        v = p.get("peso_oz")
        if not v:
            return "–"
        a, b = (v if isinstance(v, (list, tuple)) else (v, v))
        return f"{round(a * 28.35)}–{round(b * 28.35)} g" if a != b else f"{round(a * 28.35)} g"

    righe = [(f'<a href="{P("pickleball", p["slug"])}">{e(GP.titolo(p))}</a>', LIV[p["livello"]][li], FO.get(p.get("forma"), ("–",) * 4)[li],
              f'{p["spessore_mm"]} mm' if p.get("spessore_mm") else "–", peso(p), e(GP.g(p["faccia"])) if p.get("faccia") else "–",
              f'{p["prezzo_usd"]:.2f} $'.replace(".", "," if li in (0, 2, 3) else ".") if p.get("prezzo_usd") else "–") for p in sel]
    t = tab([L("Racchetta", "Paddle", "Pala", "Raquette"), L("Livello", "Level", "Nivel", "Niveau"), L("Forma", "Shape", "Forma", "Forme"),
             L("Spessore", "Thickness", "Grosor", "Épaisseur"), L("Peso", "Weight", "Peso", "Poids"), L("Faccia", "Face", "Cara", "Tamis"),
             L("Listino USA", "US list price", "Precio EE. UU.", "Prix US")], righe)
    guida, sez = P("articoli", "pickleball-per-chi-gioca-a-padel"), P("pickleball")
    reg = P("articoli", "regolamento-pickleball-regole-spiegate")
    n = len(sel)
    corpo = L(f'''<p><b>Per iniziare a giocare a pickleball basta una racchetta in fibra di vetro, spessa 14–16 mm, di peso medio (220–240 g) e con una forma standard o larga, che perdona i colpi decentrati. Non serve spendere più di 60–100 dollari di listino: nel nostro catalogo ci sono {n} modelli adatti a chi inizia, dal set da due racchette a meno di 40 $ alla JOOLA firmata da Andre Agassi.</b></p>
<h2>Le racchette per principianti del nostro catalogo</h2>{t}
<p class="note">Dati dichiarati dai produttori, con le fonti nelle singole schede. Prezzi di listino USA in dollari; in Italia i prezzi cambiano per negozio.</p>
<h2>Come sceglierla: 4 cose che contano</h2>
<ul>
<li><b>Materiale della faccia.</b> La fibra di vetro è più elastica e perdona di più; il carbonio dà più controllo e "morde" la palla per l'effetto, ma costa di più. Per i primi mesi la fibra di vetro va benissimo.</li>
<li><b>Spessore.</b> 14–16 mm danno più controllo e un tocco più morbido, ideale per i colpi corti vicino alla rete; 11–13 mm danno più spinta ma meno precisione.</li>
<li><b>Forma.</b> Standard e larga hanno la zona utile più ampia; la forma allungata dà più portata ma richiede più precisione.</li>
<li><b>Omologazione.</b> Serve solo per i tornei: in quel caso scegli un modello approvato USA Pickleball (USAP), come la JOOLA Agassi Champion o la Essentials.</li>
</ul>
<h2>Da dove partire</h2>
<p>Se vieni dal padel, leggi prima la nostra guida <a href="{guida}">pickleball per chi gioca a padel</a> e il <a href="{reg}">regolamento spiegato semplice</a>. Tutte le altre racchette, anche per giocatori avanzati, sono nella <a href="{sez}">sezione pickleball</a>.</p>''',
              f'''<p><b>To start playing pickleball you only need a fibreglass paddle, 14–16 mm thick, mid-weight (220–240 g, about 7.8–8.5 oz) and with a standard or wide shape that forgives off-centre hits. There is no need to spend more than $60–100 at list price: our catalogue has {n} beginner-friendly models, from a two-paddle set under $40 to the JOOLA signed by Andre Agassi.</b></p>
<h2>Beginner paddles in our catalogue</h2>{t}
<p class="note">Manufacturers' stated data, with sources on each paddle page. US list prices in dollars; prices vary by shop.</p>
<h2>How to choose: 4 things that matter</h2>
<ul>
<li><b>Face material.</b> Fibreglass is more elastic and more forgiving; carbon gives more control and grips the ball for spin, but costs more. Fibreglass is fine for the first months.</li>
<li><b>Thickness.</b> 14–16 mm gives more control and a softer touch, ideal for short shots at the net; 11–13 mm gives more pop but less precision.</li>
<li><b>Shape.</b> Standard and widebody shapes have the biggest sweet spot; elongated shapes give more reach but need more precision.</li>
<li><b>Approval.</b> Only needed for tournaments: in that case pick a USA Pickleball (USAP) approved model, like the JOOLA Agassi Champion or the Essentials.</li>
</ul>
<h2>Where to start</h2>
<p>If you come from padel, read our guide <a href="{guida}">pickleball for padel players</a> and the <a href="{reg}">rules explained simply</a> first. All the other paddles, including for advanced players, are in the <a href="{sez}">pickleball section</a>.</p>''',
              f'''<p><b>Para empezar a jugar al pickleball basta una pala de fibra de vidrio, de 14–16 mm de grosor, peso medio (220–240 g) y forma estándar o ancha, que perdona los golpes descentrados. No hace falta gastar más de 60–100 dólares de precio de lista: en nuestro catálogo hay {n} modelos para empezar, desde un set de dos palas por menos de 40 $ hasta la JOOLA firmada por Andre Agassi.</b></p>
<h2>Las palas para principiantes de nuestro catálogo</h2>{t}
<p class="note">Datos declarados por los fabricantes, con las fuentes en cada ficha. Precios de lista en EE. UU. en dólares; en cada tienda cambian.</p>
<h2>Cómo elegirla: 4 cosas que importan</h2>
<ul>
<li><b>Material de la cara.</b> La fibra de vidrio es más elástica y perdona más; el carbono da más control y "agarra" la bola para el efecto, pero cuesta más. Para los primeros meses la fibra de vidrio va de sobra.</li>
<li><b>Grosor.</b> 14–16 mm dan más control y un toque más blando, ideal para los golpes cortos junto a la red; 11–13 mm dan más salida pero menos precisión.</li>
<li><b>Forma.</b> Estándar y ancha tienen el punto dulce más grande; la alargada da más alcance pero exige más precisión.</li>
<li><b>Homologación.</b> Solo hace falta para torneos: en ese caso elige un modelo aprobado por USA Pickleball (USAP), como la JOOLA Agassi Champion o la Essentials.</li>
</ul>
<h2>Por dónde empezar</h2>
<p>Si vienes del pádel, lee antes nuestra guía <a href="{guida}">pickleball para jugadores de pádel</a> y el <a href="{reg}">reglamento explicado fácil</a>. Todas las demás palas, también para jugadores avanzados, están en la <a href="{sez}">sección de pickleball</a>.</p>''',
              f'''<p><b>Pour débuter au pickleball, il suffit d'une raquette en fibre de verre, épaisse de 14–16 mm, de poids moyen (220–240 g) et de forme standard ou large, qui pardonne les frappes décentrées. Inutile de dépasser 60–100 dollars de prix catalogue : notre catalogue compte {n} modèles adaptés aux débutants, du lot de deux raquettes à moins de 40 $ à la JOOLA signée Andre Agassi.</b></p>
<h2>Les raquettes pour débutants de notre catalogue</h2>{t}
<p class="note">Données déclarées par les fabricants, avec les sources sur chaque fiche. Prix catalogue américains en dollars ; les prix varient selon les magasins.</p>
<h2>Bien choisir : 4 critères</h2>
<ul>
<li><b>Matériau du tamis.</b> La fibre de verre est plus élastique et pardonne davantage ; le carbone donne plus de contrôle et « accroche » la balle pour l'effet, mais coûte plus cher. Pour les premiers mois, la fibre de verre suffit largement.</li>
<li><b>Épaisseur.</b> 14–16 mm donnent plus de contrôle et un toucher plus doux, idéal pour les balles courtes au filet ; 11–13 mm donnent plus de puissance mais moins de précision.</li>
<li><b>Forme.</b> Les formes standard et large ont la plus grande zone de frappe ; la forme allongée donne plus d'allonge mais demande plus de précision.</li>
<li><b>Homologation.</b> Seulement pour les tournois : choisissez alors un modèle homologué USA Pickleball (USAP), comme la JOOLA Agassi Champion ou l'Essentials.</li>
</ul>
<h2>Par où commencer</h2>
<p>Si vous venez du padel, lisez d'abord notre guide <a href="{guida}">pickleball pour joueurs de padel</a> et les <a href="{reg}">règles expliquées simplement</a>. Toutes les autres raquettes, y compris pour joueurs confirmés, sont dans la <a href="{sez}">rubrique pickleball</a>.</p>''')
    qa = [(L("Qual è la migliore racchetta da pickleball per principianti?", "What is the best pickleball paddle for beginners?", "¿Cuál es la mejor pala de pickleball para principiantes?", "Quelle est la meilleure raquette de pickleball pour débuter ?"),
           L("Una racchetta in fibra di vetro, spessa 14–16 mm e di peso medio: per esempio la Head Radical Elite (15 mm). Per giocare in coppia da subito, il set VICLION da due racchette in fibra di vetro (14 mm) costa meno di 40 $ di listino.",
             "A fibreglass paddle, 14–16 mm thick and mid-weight: for example the Head Radical Elite (15 mm). To play with a partner straight away, the VICLION two-paddle fibreglass set (14 mm) lists at under $40.",
             "Una pala de fibra de vidrio, de 14–16 mm y peso medio: por ejemplo la Head Radical Elite (15 mm). Para jugar en pareja desde el principio, el set VICLION de dos palas de fibra de vidrio (14 mm) cuesta menos de 40 $ de precio de lista.",
             "Une raquette en fibre de verre, épaisse de 14–16 mm et de poids moyen : par exemple la Head Radical Elite (15 mm). Pour jouer à deux tout de suite, le lot VICLION de deux raquettes en fibre de verre (14 mm) coûte moins de 40 $ au prix catalogue.")),
          (L("Quanto deve pesare una racchetta da pickleball per iniziare?", "How heavy should a beginner pickleball paddle be?", "¿Cuánto debe pesar una pala de pickleball para empezar?", "Quel poids pour une raquette de pickleball de débutant ?"),
           L("Tra 220 e 240 g circa (7,8–8,5 once): abbastanza per avere stabilità, non troppo per stancare il braccio.",
             "About 220–240 g (7.8–8.5 oz): enough for stability without tiring your arm.",
             "Entre 220 y 240 g aproximadamente (7,8–8,5 onzas): suficiente estabilidad sin cansar el brazo.",
             "Environ 220 à 240 g (7,8–8,5 onces) : assez pour la stabilité, sans fatiguer le bras."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("Racchette da pickleball per principianti: come sceglierle e i modelli consigliati", "Pickleball paddles for beginners: how to choose and recommended models",
               "Palas de pickleball para principiantes: cómo elegirlas y modelos recomendados", "Raquettes de pickleball pour débutants : bien choisir et modèles conseillés")
    desc = L("Che racchetta da pickleball comprare per iniziare: materiale, spessore, peso e forma, con i modelli per principianti del nostro catalogo e i prezzi di listino.",
             "Which pickleball paddle to buy as a beginner: face material, thickness, weight and shape, with the beginner models in our catalogue and their list prices.",
             "Qué pala de pickleball comprar para empezar: material, grosor, peso y forma, con los modelos para principiantes de nuestro catálogo y sus precios.",
             "Quelle raquette de pickleball acheter pour débuter : matériau, épaisseur, poids et forme, avec les modèles débutants de notre catalogue et leurs prix.")
    scrivi_articolo(PB_SLUG, titolo + " | PadelMetrix", desc, titolo, L("Pickleball per principianti", "Beginner pickleball paddles", "Pickleball para principiantes", "Pickleball pour débutants"), corpo + faq_htm, ld_extra=[faq_ld])
    return PB_SLUG, titolo, L("Materiale, spessore, peso e forma: come scegliere la prima racchetta da pickleball.", "Material, thickness, weight and shape: how to choose your first pickleball paddle.",
                              "Material, grosor, peso y forma: cómo elegir tu primera pala de pickleball.", "Matériau, épaisseur, poids et forme : comment choisir sa première raquette de pickleball.")
