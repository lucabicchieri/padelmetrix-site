"""Articolo: il pickleball spiegato a chi gioca a padel (novembre 2026). Importato da genera_articoli."""
import sito as S
from sito import L, P, e

PP_SLUG = "pickleball-per-chi-gioca-a-padel"
S.SLUG[PP_SLUG] = ("pickleball-for-padel-players", "pickleball-para-jugadores-de-padel")
S.SLUG_FR[PP_SLUG] = "pickleball-pour-joueurs-de-padel"

PF = {
    "pbreg": ("Regolamento USA Pickleball 2026, edizione EPF", "https://europeanpickleballfederation.org/wp-content/uploads/2026/04/2026-USAP-Official-Rulebook-–-EPF-Edition-–-Italian-Version.pdf"),
    "pdreg": ("Regolamento FIP del padel", "https://www.padelfip.com/wp-content/uploads/2025/12/FIP_Reglas-del-Padel.pdf"),
    "fitp": ("FITP, Pickleball attività di base 2026", "https://www.fitp.it/media/Files/20260203_PICKLEBALL.PRESENTAZIONE_ATTIVITA__DI_BASE_2026.aggiornamento.30.01.26.pdf"),
    "fitpi": ("FITP, campionati individuali pickleball 2026", "https://www.fitp.it/media/Pickleball/20260519_Regolamento_campionati_individuali_pickleball_2026_v3_.pdf"),
}


def art_pickleball_padel(db, fonte, faq, scrivi_articolo, tab):
    import dati_pickleball as DP
    import genera_pickleball as GP
    f = {k: fonte(u, n) for k, (n, u) in PF.items()}
    reg_pb = P("articoli", "regolamento-pickleball-regole-spiegate")
    reg_pd = P("articoli", "regolamento-padel-regole-spiegate")
    sez = P("pickleball")
    per_slug = {p["slug"]: p for p in DP.P}
    inizio = ", ".join(f'<a href="{P("pickleball", s)}">{e(GP.titolo(per_slug[s]))}</a>'
                       for s in ("joola-essentials", "slk-dauntless-widebody", "joola-agassi-champion-12mm") if s in per_slug)

    righe = [
        (L("Campo", "Court", "Pista", "Terrain"), "20 × 10 m", "13,41 × 6,10 m"),
        (L("Pareti", "Walls", "Paredes", "Vitres"), L("sì, si gioca anche di rimbalzo", "yes, part of the game", "sí, forman parte del juego", "oui, elles font partie du jeu"), L("no, la palla fuori è fuori", "no, out is out", "no, fuera es fuera", "non, dehors c'est dehors")),
        (L("Rete al centro", "Net height (centre)", "Red en el centro", "Filet au centre"), "88 cm", "86,36 cm"),
        (L("Racchetta", "Racket", "Pala", "Raquette"), L("forata, spessa fino a 38 mm", "perforated, up to 38 mm thick", "perforada, hasta 38 mm", "perforée, jusqu'à 38 mm"), L("piatta, senza fori, di solito 11–16 mm", "flat, no holes, usually 11–16 mm", "plana, sin agujeros, normalmente 11–16 mm", "plate, sans trous, en général 11–16 mm")),
        (L("Peso tipico", "Typical weight", "Peso típico", "Poids typique"), "≈ 365 g", "≈ 230 g"),
        (L("Pallina", "Ball", "Pelota", "Balle"), L("pressurizzata, in feltro", "pressurised, felt", "presurizada, de fieltro", "pressurisée, en feutre"), L("plastica forata, leggera", "light perforated plastic", "plástico perforado, ligera", "plastique perforé, légère")),
        (L("Servizio", "Serve", "Saque", "Service"), L("dal basso dopo un rimbalzo; 2 tentativi", "underhand after a bounce; 2 attempts", "por abajo tras bote; 2 intentos", "par en dessous après rebond ; 2 essais"), L("dal basso, al volo o a rimbalzo; 1 tentativo", "underhand, volley or drop; 1 attempt", "por abajo, de volea o con bote; 1 intento", "par en dessous, volée ou rebond ; 1 essai")),
        (L("Punteggio", "Scoring", "Puntuación", "Score"), L("come il tennis: 15, 30, 40, set a 6", "like tennis: 15, 30, 40, sets to 6", "como el tenis: 15, 30, 40, sets a 6", "comme le tennis : 15, 30, 40, sets à 6"), L("a 11 con 2 di scarto; fa punto solo chi serve", "to 11, win by 2; only the server scores", "a 11 con 2 de diferencia; solo puntúa quien saca", "à 11 avec 2 d'écart ; seul le serveur marque")),
        (L("Regola speciale", "Special rule", "Regla especial", "Règle spéciale"), L("si può giocare la palla dopo la parete", "you can play the ball off the wall", "se juega la bola tras la pared", "on joue la balle après la vitre"), L("niente volée nella kitchen; due rimbalzi a inizio scambio", "no volleys in the kitchen; two bounces to start the rally", "nada de voleas en la cocina; dos botes al inicio", "pas de volée dans la cuisine ; deux rebonds en début d'échange")),
    ]
    t = tab([L("", "", "", ""), "Padel", "Pickleball"], righe).replace('class="tab"', 'class="tab cmp2"')

    corpo = L(f'''<p><b>Se giochi a padel, il pickleball lo impari in un pomeriggio: si gioca soprattutto in doppio, il servizio è dal basso e la rete è alta quasi uguale (86 cm contro 88). Cambiano tre cose: non ci sono pareti, la racchetta pesa circa un terzo in meno e a rete c'è la "kitchen", una zona in cui non si può colpire al volo.</b> Qui trovi le differenze, cosa ti porti dietro dal padel, le abitudini che ti costano punti e come iniziare in Italia.</p>
<h2>Padel e pickleball a confronto</h2>{t}
<p class="note">Misure dai regolamenti ufficiali ({f["pdreg"]}; {f["pbreg"]}). Pesi tipici calcolati sulle racchette del nostro catalogo: mediana di 365 g per il padel e di 230 g per le racchette da pickleball con peso dichiarato.</p>
<p>Un campo da pickleball è grande meno della metà di uno da padel: per questo molti circoli disegnano le righe del pickleball su campi da padel o da tennis poco usati.</p>
<h2>Cosa ti porti dietro dal padel</h2>
<ul>
<li><b>Il gioco a rete.</b> Nel pickleball gli scambi decisivi si giocano con tutti e quattro i giocatori vicino alla rete, come nel padel. Volée, riflessi e posizione col compagno sono già tuoi.</li>
<li><b>I colpi morbidi.</b> Il "dink", la palla corta e lenta che cade nella kitchen avversaria, somiglia alla chiquita del padel: serve a far colpire l'avversario dal basso.</li>
<li><b>Il servizio dal basso.</b> Il gesto è quasi lo stesso. In più puoi colpire la palla al volo, purché sotto la vita e con la racchetta che sale dal basso verso l'alto.</li>
<li><b>Il doppio.</b> Coprire il centro, muoversi insieme, chiamare le palle: tutto uguale.</li>
</ul>
<h2>Le abitudini del padel che ti costano punti</h2>
<ul>
<li><b>Fare volée nella kitchen.</b> È l'errore numero uno. Nei 2,13 m vicino alla rete non si può colpire al volo, nemmeno se ci finisci dentro per lo slancio dopo il colpo. Puoi entrarci solo per giocare una palla che ha già rimbalzato.</li>
<li><b>Aspettare la parete.</b> Una palla che supera la linea di fondo è persa: va giocata prima, al volo o dopo un rimbalzo.</li>
<li><b>Correre a rete dopo il servizio.</b> Per la regola dei due rimbalzi, servizio e risposta devono rimbalzare. Chi serve deve quindi aspettare il terzo colpo prima di avanzare.</li>
<li><b>Contare sul secondo servizio.</b> Nel pickleball ce n'è uno solo: meglio un servizio sicuro e profondo che uno forte.</li>
<li><b>Il pallonetto da padel.</b> Senza pareti, un pallonetto lungo esce. Quello che funziona è più corto e alto, sopra chi sta a rete.</li>
<li><b>Il polso rigido.</b> La palla di plastica è leggera e rallenta molto: servono colpi più accompagnati e meno potenza.</li>
</ul>
<h2>Come iniziare: le prime tre uscite</h2>
<ol>
<li><b>Prima volta:</b> impara il punteggio a tre numeri e la regola dei due rimbalzi giocando con calma. Il nostro <a href="{reg_pb}">regolamento del pickleball spiegato semplice</a> ti prende 10 minuti.</li>
<li><b>Seconda volta:</b> 20 minuti solo di dink da kitchen a kitchen, poi partite. Il controllo della palla corta decide gran parte dei punti.</li>
<li><b>Terza volta:</b> lavora sul terzo colpo, quello di chi ha servito. Di solito è una palla morbida nella kitchen avversaria, per poter salire a rete.</li>
</ol>
<h2>Che racchetta prendere</h2>
<p>All'inizio va bene una racchetta di peso medio, intorno ai 220–240 g, con uno spessore di 14–16 mm, che perdona di più e dà controllo. Non serve spendere molto: le differenze tra modelli si sentono dopo qualche mese.</p>
<ul>
<li><b>Omologazione:</b> per i tornei serve un modello omologato USA Pickleball; per giocare con gli amici no.</li>
<li><b>Per cominciare:</b> nella nostra <a href="{sez}">sezione pickleball</a> trovi {len(DP.P)} racchette con peso, spessore e livello. Tra quelle adatte a chi inizia: {inizio}.</li>
</ul>
<h2>Dove giocare in Italia</h2>
<p>In Italia il pickleball fa capo alla FITP, la Federazione Italiana Tennis e Padel ({f["fitp"]}). Il modo più semplice per iniziare è chiedere a un circolo affiliato FITP: molti hanno già un campo o tracciano le righe su un campo da padel o da tennis.</p>
<ul>
<li><b>Tornei amatoriali:</b> si gioca nei tornei TPRA, aperti dai 10 anni in su a chi non ha classifiche alte; il livello di ogni giocatore è un valore "power" da 9 a 99 che si aggiorna dopo ogni partita.</li>
<li><b>Circuiti nazionali:</b> nel 2026 ci sono il Road to Roma e il Road to Torino, con le finali al Foro Italico e a Torino ({f["fitp"]}; {f["fitpi"]}).</li>
<li><b>Over:</b> c'è anche un programma per adulti con regole semplificate nelle categorie di base, per esempio due servizi invece di uno.</li>
</ul>
<p>Se vieni dal padel e vuoi ripassare le differenze sulle regole, tieni a portata di mano anche le <a href="{reg_pd}">regole del padel spiegate</a>.</p>
<p class="note">Fonti: {f["pbreg"]}; {f["pdreg"]}; {f["fitp"]}; {f["fitpi"]}.</p>''',
              f'''<p><b>If you play padel, you can learn pickleball in an afternoon: it is mostly played in doubles, the serve is underhand and the net is almost the same height (86 cm against 88). Three things change: there are no walls, the paddle weighs about a third less, and at the net there is the "kitchen", a zone where you cannot volley.</b> Here are the differences, what you bring from padel, the habits that cost you points and how to get started.</p>
<h2>Padel and pickleball compared</h2>{t}
<p class="note">Measurements from the official rulebooks ({f["pdreg"]}; {f["pbreg"]}). Typical weights calculated on the rackets in our catalogue: median 365 g for padel and 230 g for pickleball paddles with a stated weight.</p>
<p>A pickleball court is less than half the size of a padel court, which is why many clubs paint pickleball lines on little-used padel or tennis courts.</p>
<h2>What you bring from padel</h2>
<ul>
<li><b>Net play.</b> In pickleball the decisive rallies are played with all four players near the net, as in padel. Volleys, reflexes and positioning with your partner are already yours.</li>
<li><b>Soft shots.</b> The "dink", the short, slow ball that drops into the opponents' kitchen, is like padel's chiquita: it forces the opponent to hit up.</li>
<li><b>The underhand serve.</b> The motion is almost the same. You can also volley the serve, as long as you hit below the waist with the paddle moving upwards.</li>
<li><b>Doubles.</b> Covering the middle, moving together, calling balls: all the same.</li>
</ul>
<h2>Padel habits that cost you points</h2>
<ul>
<li><b>Volleying in the kitchen.</b> The number one mistake. In the 2.13 m (7 ft) next to the net you cannot volley, not even if your momentum carries you in after the shot. You can only step in to play a ball that has already bounced.</li>
<li><b>Waiting for the wall.</b> A ball that goes past the baseline is lost: play it before, on the volley or after one bounce.</li>
<li><b>Rushing the net after serving.</b> Under the two-bounce rule, the serve and the return must bounce. The serving side has to wait for the third shot before moving in.</li>
<li><b>Relying on a second serve.</b> Pickleball gives you only one: a safe, deep serve beats a hard one.</li>
<li><b>The padel lob.</b> Without walls, a long lob goes out. What works is shorter and higher, over the player at the net.</li>
<li><b>A stiff wrist.</b> The plastic ball is light and slows down a lot: you need smoother strokes and less power.</li>
</ul>
<h2>Getting started: your first three sessions</h2>
<ol>
<li><b>First time:</b> learn the three-number score and the two-bounce rule, playing calmly. Our <a href="{reg_pb}">pickleball rules explained simply</a> take 10 minutes.</li>
<li><b>Second time:</b> 20 minutes of dinking kitchen to kitchen, then games. Controlling the short ball decides most points.</li>
<li><b>Third time:</b> work on the third shot, the serving side's. It is usually a soft ball into the opponents' kitchen so you can move up to the net.</li>
</ol>
<h2>Which paddle to buy</h2>
<p>To start, a mid-weight paddle around 220–240 g (7.8–8.5 oz), 14–16 mm thick, is more forgiving and gives control. You do not need to spend much: differences between models show up after a few months.</p>
<ul>
<li><b>Approval:</b> tournaments require a USA Pickleball approved model; casual play does not.</li>
<li><b>To start with:</b> our <a href="{sez}">pickleball section</a> lists {len(DP.P)} paddles with weight, thickness and level. Among those suited to beginners: {inizio}.</li>
</ul>
<h2>Where to play in Italy</h2>
<p>In Italy pickleball is run by FITP, the Italian Tennis and Padel Federation ({f["fitp"]}). The easiest way to start is to ask an FITP club: many already have a court or paint lines on a padel or tennis court.</p>
<ul>
<li><b>Amateur events:</b> TPRA tournaments are open from age 10 to players without high rankings; each player's level is a "power" value from 9 to 99, updated after every match.</li>
<li><b>National circuits:</b> in 2026 there are the Road to Roma and Road to Torino, with finals at the Foro Italico and in Turin ({f["fitp"]}; {f["fitpi"]}).</li>
<li><b>Adults:</b> there is also an adult programme with simplified rules at entry level, for example two serves instead of one.</li>
</ul>
<p>Outside Italy, your national pickleball association or local padel and tennis clubs are the best place to start. To brush up on the rule differences, keep the <a href="{reg_pd}">padel rules explained</a> handy too.</p>
<p class="note">Sources: {f["pbreg"]}; {f["pdreg"]}; {f["fitp"]}; {f["fitpi"]}.</p>''',
              f'''<p><b>Si juegas al pádel, el pickleball lo aprendes en una tarde: se juega sobre todo en dobles, el saque es por abajo y la red tiene casi la misma altura (86 cm frente a 88). Cambian tres cosas: no hay paredes, la pala pesa alrededor de un tercio menos y junto a la red está la "cocina" (kitchen), una zona donde no se puede volear.</b> Aquí tienes las diferencias, lo que te llevas del pádel, los hábitos que te cuestan puntos y cómo empezar.</p>
<h2>Pádel y pickleball, cara a cara</h2>{t}
<p class="note">Medidas de los reglamentos oficiales ({f["pdreg"]}; {f["pbreg"]}). Pesos típicos calculados sobre las palas de nuestro catálogo: mediana de 365 g en pádel y de 230 g en las palas de pickleball con peso declarado.</p>
<p>Una pista de pickleball mide menos de la mitad que una de pádel: por eso muchos clubes pintan las líneas de pickleball en pistas de pádel o de tenis poco usadas.</p>
<h2>Lo que te llevas del pádel</h2>
<ul>
<li><b>El juego en la red.</b> En el pickleball los puntos decisivos se juegan con los cuatro jugadores cerca de la red, como en el pádel. Voleas, reflejos y posición con tu compañero ya son tuyos.</li>
<li><b>Los golpes suaves.</b> El "dink", la bola corta y lenta que cae en la cocina rival, se parece a la chiquita del pádel: obliga al rival a golpear de abajo arriba.</li>
<li><b>El saque por abajo.</b> El gesto es casi el mismo. Además puedes sacar de volea, siempre por debajo de la cintura y con la pala subiendo.</li>
<li><b>Los dobles.</b> Cubrir el centro, moverse juntos, cantar las bolas: todo igual.</li>
</ul>
<h2>Los hábitos del pádel que te cuestan puntos</h2>
<ul>
<li><b>Volear dentro de la cocina.</b> Es el error número uno. En los 2,13 m junto a la red no se puede volear, ni siquiera si la inercia te mete dentro después del golpe. Solo puedes entrar para jugar una bola que ya ha botado.</li>
<li><b>Esperar la pared.</b> Una bola que pasa la línea de fondo está perdida: hay que jugarla antes, de volea o tras un bote.</li>
<li><b>Subir a la red después de sacar.</b> Por la regla de los dos botes, el saque y el resto deben botar. Quien saca tiene que esperar al tercer golpe para avanzar.</li>
<li><b>Contar con el segundo saque.</b> En el pickleball solo hay uno: mejor un saque seguro y profundo que uno fuerte.</li>
<li><b>El globo de pádel.</b> Sin paredes, un globo largo se va fuera. Lo que funciona es más corto y alto, por encima de quien está en la red.</li>
<li><b>La muñeca rígida.</b> La bola de plástico es ligera y frena mucho: hacen falta golpes más acompañados y menos potencia.</li>
</ul>
<h2>Cómo empezar: tus tres primeras sesiones</h2>
<ol>
<li><b>Primera vez:</b> aprende la puntuación de tres números y la regla de los dos botes jugando con calma. Nuestro <a href="{reg_pb}">reglamento del pickleball explicado fácil</a> se lee en 10 minutos.</li>
<li><b>Segunda vez:</b> 20 minutos solo de dinks de cocina a cocina, luego partidos. Controlar la bola corta decide la mayoría de los puntos.</li>
<li><b>Tercera vez:</b> trabaja el tercer golpe, el de quien ha sacado. Suele ser una bola suave a la cocina rival para poder subir a la red.</li>
</ol>
<h2>Qué pala comprar</h2>
<p>Para empezar va bien una pala de peso medio, en torno a 220–240 g, de 14–16 mm de grosor, que perdona más y da control. No hace falta gastar mucho: las diferencias entre modelos se notan al cabo de unos meses.</p>
<ul>
<li><b>Homologación:</b> para torneos hace falta un modelo homologado por USA Pickleball; para jugar con amigos, no.</li>
<li><b>Para empezar:</b> en nuestra <a href="{sez}">sección de pickleball</a> tienes {len(DP.P)} palas con peso, grosor y nivel. Entre las adecuadas para empezar: {inizio}.</li>
</ul>
<h2>Dónde jugar en Italia</h2>
<p>En Italia el pickleball depende de la FITP, la Federación Italiana de Tenis y Pádel ({f["fitp"]}). Lo más sencillo es preguntar en un club afiliado: muchos ya tienen pista o pintan las líneas en una de pádel o de tenis.</p>
<ul>
<li><b>Torneos amateur:</b> se juegan los torneos TPRA, abiertos desde los 10 años a jugadores sin clasificación alta; el nivel de cada jugador es un valor "power" de 9 a 99 que se actualiza tras cada partido.</li>
<li><b>Circuitos nacionales:</b> en 2026 están el Road to Roma y el Road to Torino, con finales en el Foro Itálico y en Turín ({f["fitp"]}; {f["fitpi"]}).</li>
<li><b>Adultos:</b> hay también un programa para adultos con reglas simplificadas en las categorías de base, por ejemplo dos saques en lugar de uno.</li>
</ul>
<p>Fuera de Italia, la federación o asociación de pickleball de tu país y los clubes de pádel y tenis son el mejor punto de partida. Para repasar las diferencias de reglamento, ten a mano también las <a href="{reg_pd}">reglas del pádel explicadas</a>.</p>
<p class="note">Fuentes: {f["pbreg"]}; {f["pdreg"]}; {f["fitp"]}; {f["fitpi"]}.</p>''',
              f'''<p><b>Si vous jouez au padel, vous apprendrez le pickleball en un après-midi : on joue surtout en double, le service se fait par en dessous et le filet a presque la même hauteur (86 cm contre 88). Trois choses changent : il n'y a pas de vitres, la raquette pèse environ un tiers de moins et près du filet il y a la « cuisine » (kitchen), une zone où l'on ne peut pas volleyer.</b> Voici les différences, ce que vous gardez du padel, les habitudes qui vous coûtent des points et comment commencer.</p>
<h2>Padel et pickleball comparés</h2>{t}
<p class="note">Mesures issues des règlements officiels ({f["pdreg"]} ; {f["pbreg"]}). Poids typiques calculés sur les raquettes de notre catalogue : médiane de 365 g pour le padel et de 230 g pour les raquettes de pickleball au poids déclaré.</p>
<p>Un terrain de pickleball fait moins de la moitié d'un terrain de padel : c'est pourquoi beaucoup de clubs tracent des lignes de pickleball sur des terrains de padel ou de tennis peu utilisés.</p>
<h2>Ce que vous gardez du padel</h2>
<ul>
<li><b>Le jeu au filet.</b> Au pickleball, les points décisifs se jouent avec les quatre joueurs près du filet, comme au padel. Volées, réflexes et placement avec le partenaire sont déjà acquis.</li>
<li><b>Les coups doux.</b> Le « dink », la balle courte et lente qui tombe dans la cuisine adverse, ressemble à la chiquita du padel : il oblige l'adversaire à frapper de bas en haut.</li>
<li><b>Le service par en dessous.</b> Le geste est presque le même. On peut aussi servir de volée, à condition de frapper sous la taille avec la raquette qui monte.</li>
<li><b>Le double.</b> Couvrir le centre, bouger ensemble, annoncer les balles : rien ne change.</li>
</ul>
<h2>Les habitudes du padel qui coûtent des points</h2>
<ul>
<li><b>Volleyer dans la cuisine.</b> L'erreur numéro un. Dans les 2,13 m près du filet, on ne peut pas volleyer, même si l'élan vous y emmène après le coup. On n'y entre que pour jouer une balle qui a déjà rebondi.</li>
<li><b>Attendre la vitre.</b> Une balle qui dépasse la ligne de fond est perdue : il faut la jouer avant, de volée ou après un rebond.</li>
<li><b>Monter au filet après le service.</b> Avec la règle des deux rebonds, le service et le retour doivent rebondir. Le serveur doit attendre le troisième coup pour avancer.</li>
<li><b>Compter sur une seconde balle.</b> Au pickleball, il n'y a qu'un service : mieux vaut un service sûr et profond qu'un service puissant.</li>
<li><b>Le lob du padel.</b> Sans vitres, un lob long sort. Ce qui marche est plus court et plus haut, au-dessus du joueur au filet.</li>
<li><b>Le poignet raide.</b> La balle en plastique est légère et ralentit beaucoup : il faut des coups plus accompagnés et moins de puissance.</li>
</ul>
<h2>Commencer : vos trois premières séances</h2>
<ol>
<li><b>Première fois :</b> apprenez le score à trois chiffres et la règle des deux rebonds en jouant tranquillement. Nos <a href="{reg_pb}">règles du pickleball expliquées</a> se lisent en 10 minutes.</li>
<li><b>Deuxième fois :</b> 20 minutes de dinks de cuisine à cuisine, puis des matchs. Maîtriser la balle courte décide la plupart des points.</li>
<li><b>Troisième fois :</b> travaillez le troisième coup, celui du serveur. C'est souvent une balle douce dans la cuisine adverse pour pouvoir monter au filet.</li>
</ol>
<h2>Quelle raquette acheter</h2>
<p>Pour débuter, une raquette de poids moyen, autour de 220–240 g, épaisse de 14–16 mm, pardonne davantage et donne du contrôle. Inutile de dépenser beaucoup : les différences entre modèles se sentent après quelques mois.</p>
<ul>
<li><b>Homologation :</b> en tournoi, il faut un modèle homologué USA Pickleball ; entre amis, non.</li>
<li><b>Pour commencer :</b> notre <a href="{sez}">rubrique pickleball</a> recense {len(DP.P)} raquettes avec poids, épaisseur et niveau. Parmi celles adaptées aux débutants : {inizio}.</li>
</ul>
<h2>Où jouer en Italie</h2>
<p>En Italie, le pickleball dépend de la FITP, la Fédération italienne de tennis et de padel ({f["fitp"]}). Le plus simple est de demander à un club affilié : beaucoup ont déjà un terrain ou tracent les lignes sur un terrain de padel ou de tennis.</p>
<ul>
<li><b>Tournois amateurs :</b> on joue les tournois TPRA, ouverts dès 10 ans aux joueurs sans classement élevé ; le niveau de chaque joueur est une valeur « power » de 9 à 99, mise à jour après chaque match.</li>
<li><b>Circuits nationaux :</b> en 2026, il y a le Road to Roma et le Road to Torino, avec des finales au Foro Italico et à Turin ({f["fitp"]} ; {f["fitpi"]}).</li>
<li><b>Adultes :</b> il existe aussi un programme pour adultes aux règles simplifiées en catégories de base, par exemple deux services au lieu d'un.</li>
</ul>
<p>Hors d'Italie, la fédération de pickleball de votre pays et les clubs de padel et de tennis sont le meilleur point de départ. Pour réviser les différences de règles, gardez aussi sous la main les <a href="{reg_pd}">règles du padel expliquées</a>.</p>
<p class="note">Sources : {f["pbreg"]} ; {f["pdreg"]} ; {f["fitp"]} ; {f["fitpi"]}.</p>''')

    qa = [(L("Il pickleball è facile per chi gioca a padel?", "Is pickleball easy for padel players?", "¿Es fácil el pickleball para quien juega al pádel?", "Le pickleball est-il facile pour un joueur de padel ?"),
           L("Sì: doppio, servizio dal basso e gioco a rete sono simili. Le cose nuove sono l'assenza di pareti, la kitchen in cui non si fa volée, la regola dei due rimbalzi e il punteggio a 11.",
             "Yes: doubles, the underhand serve and net play are similar. What is new is the lack of walls, the kitchen where you cannot volley, the two-bounce rule and scoring to 11.",
             "Sí: dobles, saque por abajo y juego en la red son parecidos. Lo nuevo es que no hay paredes, la cocina donde no se volea, la regla de los dos botes y la puntuación a 11.",
             "Oui : double, service par en dessous et jeu au filet sont proches. Ce qui change : pas de vitres, la cuisine où l'on ne volleye pas, la règle des deux rebonds et le score à 11.")),
          (L("Qual è la differenza principale tra padel e pickleball?", "What is the main difference between padel and pickleball?", "¿Cuál es la principal diferencia entre pádel y pickleball?", "Quelle est la principale différence entre padel et pickleball ?"),
           L("Il padel si gioca in un campo chiuso da pareti con una racchetta forata di circa 365 g; il pickleball su un campo aperto di 13,41 × 6,10 m con una racchetta piatta di circa 230 g e una pallina di plastica forata.",
             "Padel is played on a walled court with a perforated racket of about 365 g; pickleball on an open 13.41 × 6.10 m (44 × 20 ft) court with a flat paddle of about 230 g and a perforated plastic ball.",
             "El pádel se juega en una pista cerrada con paredes y una pala perforada de unos 365 g; el pickleball en una pista abierta de 13,41 × 6,10 m con una pala plana de unos 230 g y una bola de plástico perforada.",
             "Le padel se joue sur un terrain entouré de vitres avec une raquette perforée d'environ 365 g ; le pickleball sur un terrain ouvert de 13,41 × 6,10 m avec une raquette plate d'environ 230 g et une balle en plastique perforée.")),
          (L("Si può giocare a pickleball su un campo da padel?", "Can you play pickleball on a padel court?", "¿Se puede jugar al pickleball en una pista de pádel?", "Peut-on jouer au pickleball sur un terrain de padel ?"),
           L("Sì: il campo da pickleball è meno della metà di uno da padel, e molti circoli tracciano le righe del pickleball su campi da padel o da tennis.",
             "Yes: a pickleball court is less than half the size of a padel court, and many clubs paint pickleball lines on padel or tennis courts.",
             "Sí: la pista de pickleball mide menos de la mitad que una de pádel, y muchos clubes pintan las líneas en pistas de pádel o de tenis.",
             "Oui : un terrain de pickleball fait moins de la moitié d'un terrain de padel, et beaucoup de clubs tracent les lignes sur des terrains de padel ou de tennis.")),
          (L("Chi gestisce il pickleball in Italia?", "Who runs pickleball in Italy?", "¿Quién gestiona el pickleball en Italia?", "Qui gère le pickleball en Italie ?"),
           L("La FITP, Federazione Italiana Tennis e Padel, che organizza tornei amatoriali TPRA, campionati e i circuiti Road to Roma e Road to Torino.",
             "FITP, the Italian Tennis and Padel Federation, which runs TPRA amateur events, championships and the Road to Roma and Road to Torino circuits.",
             "La FITP, Federación Italiana de Tenis y Pádel, que organiza torneos amateur TPRA, campeonatos y los circuitos Road to Roma y Road to Torino.",
             "La FITP, Fédération italienne de tennis et de padel, qui organise des tournois amateurs TPRA, des championnats et les circuits Road to Roma et Road to Torino."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("Pickleball per chi gioca a padel: differenze, errori da evitare e come iniziare", "Pickleball for padel players: differences, mistakes to avoid and how to start",
               "Pickleball para jugadores de pádel: diferencias, errores a evitar y cómo empezar", "Pickleball pour joueurs de padel : différences, erreurs à éviter et comment commencer")
    desc = L("Vieni dal padel? Il pickleball si impara in un pomeriggio. Differenze di campo, racchetta e regole, le abitudini che costano punti, che racchetta prendere e dove giocare in Italia.",
             "Coming from padel? You can learn pickleball in an afternoon. Court, paddle and rule differences, the habits that cost points, which paddle to buy and where to play.",
             "¿Vienes del pádel? El pickleball se aprende en una tarde. Diferencias de pista, pala y reglas, los hábitos que cuestan puntos, qué pala comprar y dónde jugar.",
             "Vous venez du padel ? Le pickleball s'apprend en un après-midi. Différences de terrain, de raquette et de règles, habitudes qui coûtent des points, quelle raquette acheter et où jouer.")
    scrivi_articolo(PP_SLUG, titolo + " | PadelMetrix", desc, titolo, L("Pickleball per chi gioca a padel", "Pickleball for padel players", "Pickleball para jugadores de pádel", "Pickleball pour joueurs de padel"), corpo + faq_htm, ld_extra=[faq_ld])
    return PP_SLUG, titolo, L("Differenze, abitudini da cambiare e come iniziare: il pickleball visto da chi gioca a padel.", "Differences, habits to change and how to start: pickleball seen by a padel player.",
                              "Diferencias, hábitos a cambiar y cómo empezar: el pickleball visto desde el pádel.", "Différences, habitudes à changer et comment commencer : le pickleball vu par un joueur de padel.")
