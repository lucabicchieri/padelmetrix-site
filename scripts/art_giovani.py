"""Articolo: i giovani talenti italiani del padel (novembre 2026). Importato da genera_articoli."""
import sito as S
from sito import L, P

GI_SLUG = "giovani-talenti-italiani-padel"
S.SLUG[GI_SLUG] = ("young-italian-padel-talents", "jovenes-talentos-italianos-padel")
S.SLUG_FR[GI_SLUG] = "jeunes-talents-italiens-padel"

GF = {
    "fitpj": ("FITP, convocati Junior Euro Padel Cup", "https://www.fitp.it/Federazione/News/Padel/italia-convocati-fip-junior-euro-padel-cup"),
    "srn": ("Sanremonews", "https://www.sanremonews.it/2026/07/04/leggi-notizia/argomenti/sport/articolo/limperiese-pietro-giovannini-trascina-litalia-al-bronzo-europeo-doppio-podio-azzurro-alla-fip-jun.html"),
    "agi": ("Agimeg, convocati Mondiali 2026", "https://www.agimeg.it/mondiali-padel-doha-2026-italia-convocati-tre-esordienti/"),
    "fitpm": ("FITP, bronzo mondiale 2026", "https://www.fitp.it/Federazione/News/Padel/Il-bronzo-mondiale-e-ancora-dellItalia-francesi-battute-per-2-0"),
    "fisu": ("FIP, Mondiali universitari Malaga", "https://www.padelfip.com/2026/07/malaga-crowns-spain-and-italy-celebrations-for-the-first-edition-of-the-fisu-world-university-championship-padel/"),
    "pm": ("Padel Magazine, classifiche italiani", "https://padelmagazine.it/news/le-classifiche-degli-italiani-posizioni-stabili-per-i-big-buon-salto-in-avanti-per-baldi/"),
    "st": ("SuperTennis, Platania", "https://www.supertennis.tv/News/Padel/Le-ambizioni-di-Platania-Prima-i-top-200-poi-Premier-Padel"),
    "bnl": ("BNL Italy Major, Dal Pozzo", "https://www.bnlitalymajorpremierpadel.com/it/News/Star/giulia-dal-pozzo-profilo-curiosita-errani"),
    "sp": ("StudyPadel, Dal Pozzo", "https://www.studypadel.com/players/giulia-dal-pozzo"),
}


def art_giovani(db, fonte, faq, scrivi_articolo, tab):
    f = {k: fonte(u, n) for k, (n, u) in GF.items()}
    pro = P("guide", "racchette-giocatori-professionisti")
    reg = P("articoli", "regolamento-padel-regole-spiegate")

    t_rank = tab([L("Giocatore", "Player", "Jugador", "Joueur"), L("Anno", "Born", "Año", "Né"), "FIP"], [
        ("Pier Giulio Farabbi", "2005", "244"), ("Noa Bonnefoy", "2005", "257"), ("Giuseppe Fino", "2006", "259"),
        ("Steve Piernicola Stracquadaini", "2004", "263"), ("Matteo Platania", "2006", "271"), ("Matteo Sargolini", "2007", "299"),
        ("Aurora Buscaino", "2006", "177 (F)"),
        ("Camilla Livioni", "2007", "210 (F)"),
        ("Luna Di Battista", "2007", "233 (F)"),
        ("Matilde Minelli", "2009", "237 (F)"),
        ("Giuditta Beltrami", "2006", "268 (F)")]).replace('class="tab"', 'class="tab cmp2 gtab"')

    corpo = L(f'''<p><b>Il padel italiano ha una nuova generazione che sta già arrivando in alto. Giulia Dal Pozzo, 21 anni, è la prima italiana nel ranking mondiale FIP; Michele Brambilla, classe 2005, è campione del mondo universitario ed è stato convocato per la prima volta in Nazionale; e le giovanili sono salite due volte sul podio agli Europei di Porto.</b></p>
<h2>Giulia Dal Pozzo, la più avanti di tutti</h2>
<p>Nata nel 2005 a Borgo Maggiore (San Marino) e cresciuta tra San Marino e Rimini, è figlia dell'ex tennista Francesca Guardigli ({f["bnl"]}). Con la Nazionale junior ha vinto il bronzo ai Mondiali di Asunción 2023; nel dicembre 2024, al Milano Premier Padel P1, è partita dalle qualificazioni con Caterina Baldi ed è arrivata agli ottavi battendo Carolina Navarro. Nel 2025 è entrata nella top 100 mondiale.</p>
<p>Oggi è la numero 1 d'Italia e intorno al 23° posto del ranking FIP; nel 2026 gioca con la spagnola Nuria Rodríguez ({f["sp"]}). Ai Mondiali di Doha, a novembre, ha vinto con Emily Stellato la partita decisiva per il bronzo contro la Francia, 7-6 6-3 ({f["fitpm"]}).</p>
<h2>Michele Brambilla e Noa Bonnefoy, campioni del mondo universitari</h2>
<p>A luglio 2026, a Malaga, si è giocato il primo Mondiale universitario di padel: il titolo maschile è andato a Michele Brambilla e Noa Bonnefoy, entrambi classe 2005, che in finale hanno battuto un'altra coppia italiana, Simone Iacovino e Matteo Brambilla, 4-6 6-3 6-4 ({f["fisu"]}). Michele Brambilla ha poi ricevuto la prima convocazione nella Nazionale maggiore per i Mondiali di Doha ({f["agi"]}).</p>
<h2>Le nuove azzurre: Caterina Baldi e Clarissa Aima</h2>
<p>A Doha hanno esordito in Nazionale maggiore anche Caterina Baldi e Clarissa Aima, premiate da una stagione di crescita ({f["agi"]}). Baldi aveva già fatto un salto a fine 2025, salendo al 90° posto mondiale con un titolo e due finali nei tornei FIP Bronze ({f["pm"]}); ai Mondiali ha vinto con Giulia Sussarello il primo punto della finale per il bronzo, 4-6 6-1 6-3 ({f["fitpm"]}). Le azzurre hanno chiuso al terzo posto, il quarto podio mondiale nelle ultime quattro edizioni; gli uomini sono arrivati quarti.</p>
<h2>Matteo Platania, dalla Sicilia verso Premier Padel</h2>
<p>Classe 2006, cresciuto ad Agrigento nel circolo del padre e trasferito a Roma, a febbraio 2025 ha superato le qualificazioni del Premier Padel P2 di Gijón vincendo tre turni senza perdere un set. Il suo obiettivo dichiarato: entrare nei primi 200 del mondo e poi giocare stabilmente nel circuito Premier Padel ({f["st"]}).</p>
<h2>Gli altri nomi nel ranking mondiale</h2>
<p>Queste le posizioni dei giovani italiani nel ranking FIP a fine novembre 2025, l'ultima fotografia completa pubblicata ({f["pm"]}). (F) indica il ranking femminile. Le classifiche cambiano ogni settimana.</p>{t_rank}
<h2>Le giovanili: doppio podio agli Europei</h2>
<p>Alla FIP Junior Euro Padel Cup di Porto, a luglio 2026, l'Italia ha vinto l'argento con le ragazze e il bronzo con i ragazzi ({f["srn"]}). Il trascinatore della squadra maschile è stato <b>Pietro Giovannini</b>, Under 18 di Imperia, al suo ultimo Europeo junior.</p>
<ul><li><b>Under 18:</b> Pietro Giovannini, Stefano Indomenico, Edoardo Riso, Gabriele Laurino; Vittoria Giraldi, Matilde Minelli, Matilde Laura, Lucrezia Piernera.</li>
<li><b>Under 16:</b> Jacopo Battilani, Tommaso Sarti, Mark Giulio Menotti, Tommaso Rufo; Emma Speziali, Alessia Sgattoni, Flavia Maltese, Sophie Caruso.</li>
<li><b>Under 14:</b> Giovanni Miriello, Lorenzo Margani, Gianmarco Tempreini, Francesco Filetti; Vittoria Conti, Matilde Scarcella, Marta La Carpia, Miriam Pentrella.</li></ul>
<p class="note">Convocati: {f["fitpj"]}; risultati: {f["srn"]}.</p>
<h2>Come seguirli</h2>
<p>I giovani italiani si vedono soprattutto nei tornei FIP Promises (Under 18) e nei FIP Bronze e Silver, dove si fanno i primi punti nel ranking mondiale; i migliori entrano poi nelle qualificazioni dei tornei Premier Padel, come il Major di Roma al Foro Italico. Per sapere con che racchetta giocano i professionisti di oggi c'è la nostra pagina sulle <a href="{pro}">racchette dei professionisti</a>; per le regole, le <a href="{reg}">regole del padel spiegate semplici</a>.</p>
<p class="note">Fonti: {f["bnl"]}; {f["sp"]}; {f["fitpm"]}; {f["fisu"]}; {f["agi"]}; {f["pm"]}; {f["st"]}; {f["srn"]}; {f["fitpj"]}.</p>''',
              f'''<p><b>Italian padel has a new generation that is already climbing high. Giulia Dal Pozzo, 21, is Italy's top player in the FIP world ranking; Michele Brambilla, born in 2005, is world university champion and has earned his first national team call-up; and the youth teams made the podium twice at the European Championships in Porto.</b></p>
<h2>Giulia Dal Pozzo, the furthest ahead</h2>
<p>Born in 2005 in Borgo Maggiore (San Marino) and raised between San Marino and Rimini, she is the daughter of former tennis player Francesca Guardigli ({f["bnl"]}). With the junior national team she won bronze at the 2023 Asunción World Championships; in December 2024, at the Milano Premier Padel P1, she came through qualifying with Caterina Baldi and reached the round of 16, beating Carolina Navarro. In 2025 she broke into the world top 100.</p>
<p>Today she is Italy's number 1 and around 23rd in the FIP ranking; in 2026 she plays with Spain's Nuria Rodríguez ({f["sp"]}). At the Doha World Championships in November she and Emily Stellato won the deciding match for bronze against France, 7-6 6-3 ({f["fitpm"]}).</p>
<h2>Michele Brambilla and Noa Bonnefoy, world university champions</h2>
<p>In July 2026 Malaga hosted the first world university padel championship: the men's title went to Michele Brambilla and Noa Bonnefoy, both born in 2005, who beat another Italian pair, Simone Iacovino and Matteo Brambilla, 4-6 6-3 6-4 in the final ({f["fisu"]}). Michele Brambilla then received his first senior call-up for the Doha World Championships ({f["agi"]}).</p>
<h2>The new Italian women: Caterina Baldi and Clarissa Aima</h2>
<p>Caterina Baldi and Clarissa Aima also made their senior debut in Doha after a season of progress ({f["agi"]}). Baldi had already jumped to 90th in the world at the end of 2025 with one title and two finals in FIP Bronze events ({f["pm"]}); at the World Championships she and Giulia Sussarello won the first point of the bronze match, 4-6 6-1 6-3 ({f["fitpm"]}). The Italian women finished third, their fourth world podium in the last four editions; the men came fourth.</p>
<h2>Matteo Platania, from Sicily towards Premier Padel</h2>
<p>Born in 2006, he grew up in Agrigento at his father's club and moved to Rome. In February 2025 he came through qualifying at the Gijón Premier Padel P2, winning three rounds without dropping a set. His stated goal: reach the world top 200 and then play regularly on the Premier Padel tour ({f["st"]}).</p>
<h2>Other names in the world ranking</h2>
<p>These are young Italians' FIP ranking positions at the end of November 2025, the last complete snapshot published ({f["pm"]}). (F) means the women's ranking. Rankings change every week.</p>{t_rank}
<h2>Youth teams: a double podium at the Europeans</h2>
<p>At the FIP Junior Euro Padel Cup in Porto in July 2026, Italy won silver with the girls and bronze with the boys ({f["srn"]}). The driving force of the boys' team was <b>Pietro Giovannini</b>, an Under 18 player from Imperia, at his last junior European Championship.</p>
<ul><li><b>Under 18:</b> Pietro Giovannini, Stefano Indomenico, Edoardo Riso, Gabriele Laurino; Vittoria Giraldi, Matilde Minelli, Matilde Laura, Lucrezia Piernera.</li>
<li><b>Under 16:</b> Jacopo Battilani, Tommaso Sarti, Mark Giulio Menotti, Tommaso Rufo; Emma Speziali, Alessia Sgattoni, Flavia Maltese, Sophie Caruso.</li>
<li><b>Under 14:</b> Giovanni Miriello, Lorenzo Margani, Gianmarco Tempreini, Francesco Filetti; Vittoria Conti, Matilde Scarcella, Marta La Carpia, Miriam Pentrella.</li></ul>
<p class="note">Squad: {f["fitpj"]}; results: {f["srn"]}.</p>
<h2>How to follow them</h2>
<p>Young Italians mostly appear in FIP Promises events (Under 18) and in FIP Bronze and Silver tournaments, where they earn their first world ranking points; the best then enter qualifying at Premier Padel events such as the Rome Major at the Foro Italico. To see which rackets today's pros use, check our page on <a href="{pro}">pro players' rackets</a>; for the rules, the <a href="{reg}">padel rules explained simply</a>.</p>
<p class="note">Sources: {f["bnl"]}; {f["sp"]}; {f["fitpm"]}; {f["fisu"]}; {f["agi"]}; {f["pm"]}; {f["st"]}; {f["srn"]}; {f["fitpj"]}.</p>''',
              f'''<p><b>El pádel italiano tiene una nueva generación que ya está llegando arriba. Giulia Dal Pozzo, de 21 años, es la primera italiana del ranking mundial FIP; Michele Brambilla, nacido en 2005, es campeón del mundo universitario y ha sido convocado por primera vez con la selección; y las categorías inferiores subieron dos veces al podio en el Europeo de Oporto.</b></p>
<h2>Giulia Dal Pozzo, la más adelantada</h2>
<p>Nacida en 2005 en Borgo Maggiore (San Marino) y criada entre San Marino y Rímini, es hija de la extenista Francesca Guardigli ({f["bnl"]}). Con la selección júnior ganó el bronce en el Mundial de Asunción 2023; en diciembre de 2024, en el Milano Premier Padel P1, salió de la previa con Caterina Baldi y llegó a octavos ganando a Carolina Navarro. En 2025 entró en el top 100 mundial.</p>
<p>Hoy es la número 1 de Italia y está en torno al puesto 23 del ranking FIP; en 2026 juega con la española Nuria Rodríguez ({f["sp"]}). En el Mundial de Doha, en noviembre, ganó con Emily Stellato el partido decisivo por el bronce ante Francia, 7-6 6-3 ({f["fitpm"]}).</p>
<h2>Michele Brambilla y Noa Bonnefoy, campeones del mundo universitarios</h2>
<p>En julio de 2026 Málaga acogió el primer Mundial universitario de pádel: el título masculino fue para Michele Brambilla y Noa Bonnefoy, ambos nacidos en 2005, que en la final ganaron a otra pareja italiana, Simone Iacovino y Matteo Brambilla, 4-6 6-3 6-4 ({f["fisu"]}). Después, Michele Brambilla recibió su primera convocatoria con la selección absoluta para el Mundial de Doha ({f["agi"]}).</p>
<h2>Las nuevas azzurre: Caterina Baldi y Clarissa Aima</h2>
<p>En Doha también debutaron con la selección absoluta Caterina Baldi y Clarissa Aima, tras una temporada de crecimiento ({f["agi"]}). Baldi ya había dado un salto a finales de 2025, subiendo al puesto 90 mundial con un título y dos finales en torneos FIP Bronze ({f["pm"]}); en el Mundial ganó con Giulia Sussarello el primer punto de la eliminatoria por el bronce, 4-6 6-1 6-3 ({f["fitpm"]}). Las italianas terminaron terceras, su cuarto podio mundial en las últimas cuatro ediciones; los hombres fueron cuartos.</p>
<h2>Matteo Platania, de Sicilia hacia Premier Padel</h2>
<p>Nacido en 2006, creció en Agrigento en el club de su padre y se trasladó a Roma. En febrero de 2025 superó la previa del Premier Padel P2 de Gijón ganando tres rondas sin ceder un set. Su objetivo declarado: entrar en el top 200 mundial y luego jugar de forma estable en el circuito Premier Padel ({f["st"]}).</p>
<h2>Otros nombres en el ranking mundial</h2>
<p>Estas son las posiciones de los jóvenes italianos en el ranking FIP a finales de noviembre de 2025, la última foto completa publicada ({f["pm"]}). (F) indica el ranking femenino. Los rankings cambian cada semana.</p>{t_rank}
<h2>Categorías inferiores: doble podio en el Europeo</h2>
<p>En la FIP Junior Euro Padel Cup de Oporto, en julio de 2026, Italia ganó la plata con las chicas y el bronce con los chicos ({f["srn"]}). El líder del equipo masculino fue <b>Pietro Giovannini</b>, sub-18 de Imperia, en su último Europeo júnior.</p>
<ul><li><b>Sub-18:</b> Pietro Giovannini, Stefano Indomenico, Edoardo Riso, Gabriele Laurino; Vittoria Giraldi, Matilde Minelli, Matilde Laura, Lucrezia Piernera.</li>
<li><b>Sub-16:</b> Jacopo Battilani, Tommaso Sarti, Mark Giulio Menotti, Tommaso Rufo; Emma Speziali, Alessia Sgattoni, Flavia Maltese, Sophie Caruso.</li>
<li><b>Sub-14:</b> Giovanni Miriello, Lorenzo Margani, Gianmarco Tempreini, Francesco Filetti; Vittoria Conti, Matilde Scarcella, Marta La Carpia, Miriam Pentrella.</li></ul>
<p class="note">Convocatoria: {f["fitpj"]}; resultados: {f["srn"]}.</p>
<h2>Cómo seguirlos</h2>
<p>Los jóvenes italianos juegan sobre todo los torneos FIP Promises (sub-18) y los FIP Bronze y Silver, donde suman sus primeros puntos en el ranking mundial; los mejores entran después en las previas de Premier Padel, como el Major de Roma en el Foro Itálico. Para saber con qué pala juegan los profesionales de hoy, mira nuestra página sobre las <a href="{pro}">palas de los profesionales</a>; para las reglas, las <a href="{reg}">reglas del pádel explicadas fácil</a>.</p>
<p class="note">Fuentes: {f["bnl"]}; {f["sp"]}; {f["fitpm"]}; {f["fisu"]}; {f["agi"]}; {f["pm"]}; {f["st"]}; {f["srn"]}; {f["fitpj"]}.</p>''',
              f'''<p><b>Le padel italien a une nouvelle génération qui grimpe déjà haut. Giulia Dal Pozzo, 21 ans, est la première Italienne au classement mondial FIP ; Michele Brambilla, né en 2005, est champion du monde universitaire et a été appelé pour la première fois en équipe nationale ; et les équipes jeunes sont montées deux fois sur le podium à l'Euro de Porto.</b></p>
<h2>Giulia Dal Pozzo, la plus avancée</h2>
<p>Née en 2005 à Borgo Maggiore (Saint-Marin) et élevée entre Saint-Marin et Rimini, elle est la fille de l'ancienne joueuse de tennis Francesca Guardigli ({f["bnl"]}). Avec l'équipe nationale junior, elle a remporté le bronze aux Mondiaux d'Asunción 2023 ; en décembre 2024, au Milano Premier Padel P1, elle est sortie des qualifications avec Caterina Baldi et a atteint les huitièmes en battant Carolina Navarro. En 2025, elle est entrée dans le top 100 mondial.</p>
<p>Aujourd'hui, elle est numéro 1 en Italie et autour de la 23e place du classement FIP ; en 2026, elle joue avec l'Espagnole Nuria Rodríguez ({f["sp"]}). Aux Mondiaux de Doha, en novembre, elle a gagné avec Emily Stellato le match décisif pour le bronze contre la France, 7-6 6-3 ({f["fitpm"]}).</p>
<h2>Michele Brambilla et Noa Bonnefoy, champions du monde universitaires</h2>
<p>En juillet 2026, Malaga a accueilli le premier championnat du monde universitaire de padel : le titre masculin est revenu à Michele Brambilla et Noa Bonnefoy, tous deux nés en 2005, qui ont battu en finale une autre paire italienne, Simone Iacovino et Matteo Brambilla, 4-6 6-3 6-4 ({f["fisu"]}). Michele Brambilla a ensuite reçu sa première convocation en équipe nationale A pour les Mondiaux de Doha ({f["agi"]}).</p>
<h2>Les nouvelles Italiennes : Caterina Baldi et Clarissa Aima</h2>
<p>À Doha, Caterina Baldi et Clarissa Aima ont aussi fait leurs débuts en équipe nationale A, après une saison de progrès ({f["agi"]}). Baldi avait déjà fait un bond fin 2025, montant à la 90e place mondiale avec un titre et deux finales en tournois FIP Bronze ({f["pm"]}) ; aux Mondiaux, elle a gagné avec Giulia Sussarello le premier point du match pour le bronze, 4-6 6-1 6-3 ({f["fitpm"]}). Les Italiennes ont terminé troisièmes, leur quatrième podium mondial lors des quatre dernières éditions ; les hommes ont fini quatrièmes.</p>
<h2>Matteo Platania, de la Sicile vers Premier Padel</h2>
<p>Né en 2006, il a grandi à Agrigente dans le club de son père et s'est installé à Rome. En février 2025, il est sorti des qualifications du Premier Padel P2 de Gijón en gagnant trois tours sans perdre un set. Son objectif affiché : entrer dans le top 200 mondial, puis jouer régulièrement sur le circuit Premier Padel ({f["st"]}).</p>
<h2>Les autres noms au classement mondial</h2>
<p>Voici les positions des jeunes Italiens au classement FIP fin novembre 2025, la dernière photographie complète publiée ({f["pm"]}). (F) indique le classement féminin. Les classements changent chaque semaine.</p>{t_rank}
<h2>Les jeunes : double podium à l'Euro</h2>
<p>À la FIP Junior Euro Padel Cup de Porto, en juillet 2026, l'Italie a remporté l'argent chez les filles et le bronze chez les garçons ({f["srn"]}). Le leader de l'équipe masculine a été <b>Pietro Giovannini</b>, moins de 18 ans, originaire d'Imperia, pour son dernier Euro junior.</p>
<ul><li><b>Moins de 18 ans :</b> Pietro Giovannini, Stefano Indomenico, Edoardo Riso, Gabriele Laurino ; Vittoria Giraldi, Matilde Minelli, Matilde Laura, Lucrezia Piernera.</li>
<li><b>Moins de 16 ans :</b> Jacopo Battilani, Tommaso Sarti, Mark Giulio Menotti, Tommaso Rufo ; Emma Speziali, Alessia Sgattoni, Flavia Maltese, Sophie Caruso.</li>
<li><b>Moins de 14 ans :</b> Giovanni Miriello, Lorenzo Margani, Gianmarco Tempreini, Francesco Filetti ; Vittoria Conti, Matilde Scarcella, Marta La Carpia, Miriam Pentrella.</li></ul>
<p class="note">Sélection : {f["fitpj"]} ; résultats : {f["srn"]}.</p>
<h2>Comment les suivre</h2>
<p>Les jeunes Italiens jouent surtout les tournois FIP Promises (moins de 18 ans) et les FIP Bronze et Silver, où ils gagnent leurs premiers points au classement mondial ; les meilleurs entrent ensuite dans les qualifications des tournois Premier Padel, comme le Major de Rome au Foro Italico. Pour savoir avec quelle raquette jouent les pros d'aujourd'hui, consultez notre page sur les <a href="{pro}">raquettes des professionnels</a> ; pour les règles, les <a href="{reg}">règles du padel expliquées simplement</a>.</p>
<p class="note">Sources : {f["bnl"]} ; {f["sp"]} ; {f["fitpm"]} ; {f["fisu"]} ; {f["agi"]} ; {f["pm"]} ; {f["st"]} ; {f["srn"]} ; {f["fitpj"]}.</p>''')

    qa = [(L("Chi sono i giovani talenti italiani del padel?", "Who are Italy's young padel talents?", "¿Quiénes son los jóvenes talentos italianos del pádel?", "Qui sont les jeunes talents italiens du padel ?"),
           L("I nomi più avanti sono Giulia Dal Pozzo (2005), prima italiana nel ranking FIP, Michele Brambilla e Noa Bonnefoy (2005), campioni del mondo universitari, Caterina Baldi e Clarissa Aima, esordienti in Nazionale ai Mondiali 2026, e Matteo Platania (2006). Tra gli junior spicca Pietro Giovannini.",
             "The furthest ahead are Giulia Dal Pozzo (2005), Italy's top player in the FIP ranking, Michele Brambilla and Noa Bonnefoy (2005), world university champions, Caterina Baldi and Clarissa Aima, national team debutantes at the 2026 World Championships, and Matteo Platania (2006). Among juniors, Pietro Giovannini stands out.",
             "Los más adelantados son Giulia Dal Pozzo (2005), primera italiana del ranking FIP, Michele Brambilla y Noa Bonnefoy (2005), campeones del mundo universitarios, Caterina Baldi y Clarissa Aima, debutantes con la selección en el Mundial 2026, y Matteo Platania (2006). Entre los júnior destaca Pietro Giovannini.",
             "Les plus avancés sont Giulia Dal Pozzo (2005), première Italienne au classement FIP, Michele Brambilla et Noa Bonnefoy (2005), champions du monde universitaires, Caterina Baldi et Clarissa Aima, débutantes en équipe nationale aux Mondiaux 2026, et Matteo Platania (2006). Chez les juniors, Pietro Giovannini se distingue.")),
          (L("Chi è Giulia Dal Pozzo?", "Who is Giulia Dal Pozzo?", "¿Quién es Giulia Dal Pozzo?", "Qui est Giulia Dal Pozzo ?"),
           L("È una giocatrice italiana nata nel 2005 a Borgo Maggiore (San Marino), figlia dell'ex tennista Francesca Guardigli. È la numero 1 d'Italia, intorno al 23° posto del ranking FIP, e ha vinto il bronzo ai Mondiali 2026 con la Nazionale.",
             "She is an Italian player born in 2005 in Borgo Maggiore (San Marino), daughter of former tennis player Francesca Guardigli. She is Italy's number 1, around 23rd in the FIP ranking, and won bronze at the 2026 World Championships with Italy.",
             "Es una jugadora italiana nacida en 2005 en Borgo Maggiore (San Marino), hija de la extenista Francesca Guardigli. Es la número 1 de Italia, en torno al puesto 23 del ranking FIP, y ganó el bronce en el Mundial 2026 con la selección.",
             "C'est une joueuse italienne née en 2005 à Borgo Maggiore (Saint-Marin), fille de l'ancienne joueuse de tennis Francesca Guardigli. Elle est numéro 1 en Italie, autour de la 23e place du classement FIP, et a gagné le bronze aux Mondiaux 2026 avec l'Italie.")),
          (L("Come è andata l'Italia ai Mondiali di padel 2026?", "How did Italy do at the 2026 Padel World Championships?", "¿Cómo le fue a Italia en el Mundial de pádel 2026?", "Comment s'est passée l'Italie aux Mondiaux de padel 2026 ?"),
           L("A Doha la squadra femminile ha vinto il bronzo battendo la Francia 2-0, il quarto podio nelle ultime quattro edizioni; quella maschile è arrivata quarta, perdendo 2-1 con il Portogallo.",
             "In Doha the women's team won bronze, beating France 2-0, their fourth podium in the last four editions; the men finished fourth after losing 2-1 to Portugal.",
             "En Doha el equipo femenino ganó el bronce al vencer a Francia 2-0, su cuarto podio en las últimas cuatro ediciones; el masculino fue cuarto tras perder 2-1 con Portugal.",
             "À Doha, l'équipe féminine a gagné le bronze en battant la France 2-0, son quatrième podium lors des quatre dernières éditions ; les hommes ont terminé quatrièmes après une défaite 2-1 contre le Portugal."))]
    faq_htm, faq_ld = faq(qa)
    titolo = L("I giovani talenti italiani del padel: chi sono e chi seguire (2026)", "Italy's young padel talents: who they are and who to watch (2026)",
               "Los jóvenes talentos italianos del pádel: quiénes son y a quién seguir (2026)", "Les jeunes talents italiens du padel : qui sont-ils et qui suivre (2026)")
    desc = L("Giulia Dal Pozzo, Michele Brambilla, Caterina Baldi, Matteo Platania e gli junior di Porto: i giovani italiani del padel che stanno emergendo, con risultati e ranking.",
             "Giulia Dal Pozzo, Michele Brambilla, Caterina Baldi, Matteo Platania and the Porto juniors: Italy's rising young padel players, with results and rankings.",
             "Giulia Dal Pozzo, Michele Brambilla, Caterina Baldi, Matteo Platania y los júnior de Oporto: los jóvenes italianos del pádel que emergen, con resultados y ranking.",
             "Giulia Dal Pozzo, Michele Brambilla, Caterina Baldi, Matteo Platania et les juniors de Porto : les jeunes Italiens du padel qui émergent, avec résultats et classements.")
    scrivi_articolo(GI_SLUG, titolo + " | PadelMetrix", desc, titolo, L("Giovani talenti italiani", "Young Italian talents", "Jóvenes talentos italianos", "Jeunes talents italiens"), corpo + faq_htm, ld_extra=[faq_ld])
    return GI_SLUG, titolo, L("Dal Pozzo, Brambilla, Baldi, Platania e gli junior: chi sta emergendo nel padel italiano.", "Dal Pozzo, Brambilla, Baldi, Platania and the juniors: who's rising in Italian padel.",
                              "Dal Pozzo, Brambilla, Baldi, Platania y los júnior: quién emerge en el pádel italiano.", "Dal Pozzo, Brambilla, Baldi, Platania et les juniors : qui émerge dans le padel italien.")
