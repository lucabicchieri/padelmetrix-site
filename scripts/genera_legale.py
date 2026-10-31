#!/usr/bin/env python3
"""Genera le pagine Privacy e Cookie in it/en/es.

Descrivono il sito com'è oggi: nessun cookie proprio, nessun analytics, nessun modulo;
servizi esterni caricati: Google Fonts (caratteri) e Cloudflare (hosting).
Se si aggiungono analytics, pubblicità, newsletter o moduli, queste pagine vanno aggiornate.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sito as S  # noqa: E402
from sito import ROOT, L, P, ALT, crumbs, pagina, data_txt, LINGUE, set_lang  # noqa: E402
import consenso as C  # noqa: E402

EMAIL = "info@padelmetrix.com"
MAIL = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'


def privacy():
    cr, ld = crumbs([S.home_crumb(), (L("Privacy", "Privacy", "Privacidad"), None)])
    agg = data_txt()
    corpo = L(f'''{cr}
<div class="intro"><h1>Informativa sulla privacy</h1>
<p><b>PadelMetrix non chiede dati personali, non usa cookie propri, non usa strumenti di analisi né pubblicità profilata.</b> Questa pagina spiega quali dati tecnici vengono comunque trattati quando visiti il sito e quali sono i tuoi diritti, ai sensi del Regolamento UE 2016/679 (GDPR).</p>
<p class="note">Ultimo aggiornamento: {agg}</p></div>
<div class="prose">
<h2>Titolare del trattamento</h2>
<p>Luca Bicchieri, persona fisica, gestore del sito padelmetrix.com. Contatto: {MAIL}.</p>
<h2>Quali dati vengono trattati</h2>
<ul>
<li><b>Dati di navigazione.</b> Come per qualsiasi sito, i server che lo ospitano ricevono automaticamente l'indirizzo IP, il tipo di browser, la pagina richiesta e l'ora della richiesta. Servono a mostrare le pagine, a garantire la sicurezza e a contrastare abusi. Non li usiamo per identificarti né per profilarti.</li>
<li><b>Dati che ci invii tu.</b> Se scrivi all'indirizzo email, trattiamo il tuo indirizzo e il contenuto del messaggio solo per risponderti.</li>
</ul>
<p>Il sito non ha moduli di registrazione, newsletter, commenti o account utente.</p>
<h2>Servizi di terze parti</h2>
<ul>
<li><b>Cloudflare</b> (Cloudflare, Inc.) ospita il sito e ne protegge la sicurezza: tratta i dati di navigazione per conto del titolare. <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener" target="_blank">Privacy di Cloudflare</a>.</li>
<li><b>Google Fonts</b> (Google Ireland Ltd / Google LLC) fornisce i caratteri tipografici: quando apri una pagina, il tuo browser li scarica dai server di Google, che ricevono il tuo indirizzo IP. <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Privacy di Google</a>.</li>
</ul>
<p>Cloudflare e Google possono trattare dati anche negli Stati Uniti; entrambe aderiscono all'EU-U.S. Data Privacy Framework.</p>
<h2>Link ai negozi e link di affiliazione</h2>
<p>Le schede contengono link verso negozi esterni, tra cui Amazon. Alcuni sono link di affiliazione: se acquisti, PadelMetrix può ricevere una commissione. Nessun dato passa da PadelMetrix al negozio: quando clicchi lasci il sito, e da quel momento si applicano la privacy e i cookie del negozio. In qualità di Affiliato Amazon, PadelMetrix riceve un guadagno dagli acquisti idonei.</p>
<h2>Base giuridica e conservazione</h2>
<p>I dati di navigazione sono trattati sulla base del legittimo interesse del titolare a far funzionare il sito in modo sicuro (art. 6.1.f GDPR) e sono conservati dai fornitori per il tempo previsto dalle loro politiche. Le email sono trattate per rispondere alla tua richiesta (art. 6.1.b) e conservate per il tempo necessario a gestirla.</p>
<h2>I tuoi diritti</h2>
<p>Puoi chiedere l'accesso ai tuoi dati, la rettifica, la cancellazione, la limitazione del trattamento, la portabilità e opporti al trattamento, scrivendo a {MAIL}. Hai anche il diritto di presentare reclamo al <a href="https://www.garanteprivacy.it/" rel="noopener" target="_blank">Garante per la protezione dei dati personali</a> o all'autorità di controllo del Paese in cui vivi.</p>
<h2>Cookie</h2>
<p>Le informazioni sui cookie sono nella <a href="{P("cookie")}">cookie policy</a>.</p>
<h2>Modifiche</h2>
<p>Se il sito cambierà (per esempio con l'aggiunta di statistiche o di una newsletter) questa pagina sarà aggiornata prima, e la data in alto lo indicherà.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Privacy policy</h1>
<p><b>PadelMetrix does not ask for personal data, does not set its own cookies and uses no analytics or targeted advertising.</b> This page explains which technical data are still processed when you visit the site and what your rights are under EU Regulation 2016/679 (GDPR).</p>
<p class="note">Last updated: {agg}</p></div>
<div class="prose">
<h2>Data controller</h2>
<p>Luca Bicchieri, private individual, who runs padelmetrix.com. Contact: {MAIL}.</p>
<h2>What data is processed</h2>
<ul>
<li><b>Browsing data.</b> As with any website, the servers hosting it automatically receive your IP address, browser type, the page requested and the time of the request. This is needed to serve the pages, keep the site secure and prevent abuse. We do not use it to identify or profile you.</li>
<li><b>Data you send us.</b> If you write to our email address, we process your address and the content of your message only to reply to you.</li>
</ul>
<p>The site has no sign-up forms, newsletter, comments or user accounts.</p>
<h2>Third-party services</h2>
<ul>
<li><b>Cloudflare</b> (Cloudflare, Inc.) hosts the site and protects its security, processing browsing data on behalf of the controller. <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener" target="_blank">Cloudflare privacy policy</a>.</li>
<li><b>Google Fonts</b> (Google Ireland Ltd / Google LLC) provides the typefaces: when you open a page, your browser downloads them from Google's servers, which receive your IP address. <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Google privacy policy</a>.</li>
</ul>
<p>Cloudflare and Google may also process data in the United States; both participate in the EU-U.S. Data Privacy Framework.</p>
<h2>Shop links and affiliate links</h2>
<p>Racket pages contain links to external shops, including Amazon. Some are affiliate links: if you buy, PadelMetrix may receive a commission. No data passes from PadelMetrix to the shop: when you click you leave the site, and from then on the shop's privacy and cookie policies apply. As an Amazon Associate, PadelMetrix earns from qualifying purchases.</p>
<h2>Legal basis and retention</h2>
<p>Browsing data are processed on the basis of the controller's legitimate interest in running the site securely (Art. 6(1)(f) GDPR) and are kept by the providers for the period set out in their policies. Emails are processed to answer your request (Art. 6(1)(b)) and kept for as long as needed to deal with it.</p>
<h2>Your rights</h2>
<p>You can request access to your data, rectification, erasure, restriction of processing and portability, and you can object to processing, by writing to {MAIL}. You also have the right to lodge a complaint with the Italian data protection authority (<a href="https://www.garanteprivacy.it/" rel="noopener" target="_blank">Garante per la protezione dei dati personali</a>) or with the supervisory authority of the country where you live.</p>
<h2>Cookies</h2>
<p>Information about cookies is in the <a href="{P("cookie")}">cookie policy</a>.</p>
<h2>Changes</h2>
<p>If the site changes (for example by adding statistics or a newsletter), this page will be updated beforehand, and the date at the top will show it.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Política de privacidad</h1>
<p><b>PadelMetrix no pide datos personales, no usa cookies propias ni herramientas de análisis ni publicidad personalizada.</b> Esta página explica qué datos técnicos se tratan igualmente cuando visitas la web y cuáles son tus derechos según el Reglamento UE 2016/679 (RGPD).</p>
<p class="note">Última actualización: {agg}</p></div>
<div class="prose">
<h2>Responsable del tratamiento</h2>
<p>Luca Bicchieri, persona física, gestor de la web padelmetrix.com. Contacto: {MAIL}.</p>
<h2>Qué datos se tratan</h2>
<ul>
<li><b>Datos de navegación.</b> Como en cualquier web, los servidores que la alojan reciben automáticamente la dirección IP, el tipo de navegador, la página solicitada y la hora de la solicitud. Sirven para mostrar las páginas, garantizar la seguridad y evitar abusos. No los usamos para identificarte ni para elaborar perfiles.</li>
<li><b>Datos que nos envías.</b> Si escribes a la dirección de correo, tratamos tu dirección y el contenido del mensaje solo para responderte.</li>
</ul>
<p>La web no tiene formularios de registro, newsletter, comentarios ni cuentas de usuario.</p>
<h2>Servicios de terceros</h2>
<ul>
<li><b>Cloudflare</b> (Cloudflare, Inc.) aloja la web y protege su seguridad: trata los datos de navegación por cuenta del responsable. <a href="https://www.cloudflare.com/privacypolicy/" rel="noopener" target="_blank">Privacidad de Cloudflare</a>.</li>
<li><b>Google Fonts</b> (Google Ireland Ltd / Google LLC) proporciona las tipografías: al abrir una página, tu navegador las descarga de los servidores de Google, que reciben tu dirección IP. <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">Privacidad de Google</a>.</li>
</ul>
<p>Cloudflare y Google pueden tratar datos también en Estados Unidos; ambas están adheridas al EU-U.S. Data Privacy Framework.</p>
<h2>Enlaces a tiendas y enlaces de afiliado</h2>
<p>Las fichas contienen enlaces a tiendas externas, entre ellas Amazon. Algunos son enlaces de afiliado: si compras, PadelMetrix puede recibir una comisión. PadelMetrix no transmite ningún dato a la tienda: al hacer clic sales de la web y, a partir de ese momento, se aplican la privacidad y las cookies de la tienda. Como Afiliado de Amazon, PadelMetrix obtiene ingresos por las compras adscritas que cumplen los requisitos aplicables.</p>
<h2>Base jurídica y conservación</h2>
<p>Los datos de navegación se tratan sobre la base del interés legítimo del responsable en que la web funcione de forma segura (art. 6.1.f RGPD) y los conservan los proveedores durante el tiempo previsto en sus políticas. Los correos se tratan para responder a tu solicitud (art. 6.1.b) y se conservan el tiempo necesario para gestionarla.</p>
<h2>Tus derechos</h2>
<p>Puedes solicitar el acceso a tus datos, su rectificación, supresión, la limitación del tratamiento y la portabilidad, y oponerte al tratamiento, escribiendo a {MAIL}. También tienes derecho a presentar una reclamación ante la autoridad italiana de protección de datos (<a href="https://www.garanteprivacy.it/" rel="noopener" target="_blank">Garante per la protezione dei dati personali</a>) o ante la autoridad de control del país en el que vives (en España, la <a href="https://www.aepd.es/" rel="noopener" target="_blank">AEPD</a>).</p>
<h2>Cookies</h2>
<p>La información sobre las cookies está en la <a href="{P("cookie")}">política de cookies</a>.</p>
<h2>Cambios</h2>
<p>Si la web cambia (por ejemplo, si se añaden estadísticas o una newsletter), esta página se actualizará antes, y la fecha de arriba lo indicará.</p>
</div>''')
    if C.attivo():
        corpo = ga_privacy(corpo)
    path, alt = P("privacy"), ALT("privacy")
    S.scrivi(path, pagina(L("Informativa sulla privacy | PadelMetrix", "Privacy policy | PadelMetrix", "Política de privacidad | PadelMetrix"),
                          L("Come PadelMetrix tratta i dati personali: nessun cookie proprio, nessun analytics; dati di navigazione, servizi di terze parti e diritti GDPR.",
                            "How PadelMetrix handles personal data: no own cookies, no analytics; browsing data, third-party services and your GDPR rights.",
                            "Cómo trata PadelMetrix los datos personales: sin cookies propias ni analítica; datos de navegación, servicios de terceros y derechos RGPD."),
                          path, corpo, ld=[ld], alt=alt), alt)


def cookie():
    cr, ld = crumbs([S.home_crumb(), (L("Cookie", "Cookies", "Cookies"), None)])
    agg = data_txt()
    corpo = L(f'''{cr}
<div class="intro"><h1>Cookie policy</h1>
<p><b>PadelMetrix non installa cookie propri e non usa cookie di analisi, di profilazione o pubblicitari.</b> Per questo il sito non mostra un banner per il consenso.</p>
<p class="note">Ultimo aggiornamento: {agg}</p></div>
<div class="prose">
<h2>Cosa sono i cookie</h2>
<p>I cookie sono piccoli file di testo che un sito salva nel browser. Quelli tecnici servono a far funzionare il sito; quelli di analisi e di profilazione servono a misurare le visite o a mostrare pubblicità mirata, e richiedono il tuo consenso.</p>
<h2>Cookie usati da questo sito</h2>
<table class="tab"><thead><tr><th>Tipo</th><th>Usati?</th></tr></thead><tbody>
<tr><td>Cookie tecnici propri</td><td>No</td></tr>
<tr><td>Cookie di analisi (statistiche)</td><td>No</td></tr>
<tr><td>Cookie di profilazione o pubblicitari</td><td>No</td></tr>
<tr><td>Cookie tecnici del fornitore di hosting (Cloudflare)</td><td>Solo se necessari alla sicurezza</td></tr>
</tbody></table>
<p>Cloudflare, che ospita il sito, può impostare cookie tecnici di sicurezza (per esempio <code>__cf_bm</code>) per distinguere i visitatori reali dai bot. Sono necessari al funzionamento sicuro del sito e non richiedono consenso. <a href="https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/" rel="noopener" target="_blank">Elenco dei cookie di Cloudflare</a>.</p>
<p>Il sito non usa nemmeno altre forme di memorizzazione nel browser (come localStorage).</p>
<h2>Caratteri tipografici di Google</h2>
<p>I caratteri del sito sono caricati da Google Fonts. Google Fonts non imposta cookie, ma il tuo browser contatta i server di Google, che ricevono il tuo indirizzo IP. Dettagli nell'<a href="{P("privacy")}">informativa sulla privacy</a>.</p>
<h2>Siti esterni</h2>
<p>Quando clicchi su un link verso un negozio (per esempio Amazon) o verso un'altra fonte, lasci PadelMetrix: quel sito può usare i propri cookie, regolati dalla sua cookie policy. È così che i negozi riconoscono gli acquisti arrivati tramite link di affiliazione.</p>
<h2>Come gestire i cookie</h2>
<p>Puoi vedere e cancellare i cookie dalle impostazioni del browser, e bloccarli tutti o solo quelli di terze parti. Su questo sito bloccarli non cambia nulla nel funzionamento delle pagine.</p>
<h2>Contatti</h2>
<p>Per domande: {MAIL}. Se in futuro aggiungeremo statistiche o pubblicità, aggiorneremo questa pagina e chiederemo il consenso dove serve.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Cookie policy</h1>
<p><b>PadelMetrix does not set its own cookies and uses no analytics, profiling or advertising cookies.</b> That is why the site shows no consent banner.</p>
<p class="note">Last updated: {agg}</p></div>
<div class="prose">
<h2>What cookies are</h2>
<p>Cookies are small text files that a website stores in your browser. Technical cookies make the site work; analytics and profiling cookies measure visits or show targeted ads, and require your consent.</p>
<h2>Cookies used by this site</h2>
<table class="tab"><thead><tr><th>Type</th><th>Used?</th></tr></thead><tbody>
<tr><td>Own technical cookies</td><td>No</td></tr>
<tr><td>Analytics cookies (statistics)</td><td>No</td></tr>
<tr><td>Profiling or advertising cookies</td><td>No</td></tr>
<tr><td>Technical cookies from the hosting provider (Cloudflare)</td><td>Only if needed for security</td></tr>
</tbody></table>
<p>Cloudflare, which hosts the site, may set security cookies (for example <code>__cf_bm</code>) to tell real visitors from bots. They are necessary for the site to run securely and do not require consent. <a href="https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/" rel="noopener" target="_blank">List of Cloudflare cookies</a>.</p>
<p>The site does not use other forms of browser storage either (such as localStorage).</p>
<h2>Google typefaces</h2>
<p>The site's typefaces are loaded from Google Fonts. Google Fonts does not set cookies, but your browser contacts Google's servers, which receive your IP address. Details in the <a href="{P("privacy")}">privacy policy</a>.</p>
<h2>External sites</h2>
<p>When you click a link to a shop (for example Amazon) or to another source, you leave PadelMetrix: that site may use its own cookies, governed by its cookie policy. This is how shops recognise purchases that came through affiliate links.</p>
<h2>Managing cookies</h2>
<p>You can view and delete cookies in your browser settings, and block all cookies or only third-party ones. On this site, blocking them changes nothing in how the pages work.</p>
<h2>Contact</h2>
<p>Questions: {MAIL}. If we add statistics or advertising in the future, we will update this page and ask for consent where required.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Política de cookies</h1>
<p><b>PadelMetrix no instala cookies propias ni usa cookies de análisis, de perfilado ni publicitarias.</b> Por eso la web no muestra un banner de consentimiento.</p>
<p class="note">Última actualización: {agg}</p></div>
<div class="prose">
<h2>Qué son las cookies</h2>
<p>Las cookies son pequeños archivos de texto que una web guarda en el navegador. Las técnicas sirven para que la web funcione; las de análisis y de perfilado sirven para medir las visitas o mostrar publicidad personalizada, y requieren tu consentimiento.</p>
<h2>Cookies que usa esta web</h2>
<table class="tab"><thead><tr><th>Tipo</th><th>¿Se usan?</th></tr></thead><tbody>
<tr><td>Cookies técnicas propias</td><td>No</td></tr>
<tr><td>Cookies de análisis (estadísticas)</td><td>No</td></tr>
<tr><td>Cookies de perfilado o publicitarias</td><td>No</td></tr>
<tr><td>Cookies técnicas del proveedor de alojamiento (Cloudflare)</td><td>Solo si son necesarias para la seguridad</td></tr>
</tbody></table>
<p>Cloudflare, que aloja la web, puede instalar cookies técnicas de seguridad (por ejemplo <code>__cf_bm</code>) para distinguir a los visitantes reales de los bots. Son necesarias para el funcionamiento seguro de la web y no requieren consentimiento. <a href="https://developers.cloudflare.com/fundamentals/reference/policies-compliances/cloudflare-cookies/" rel="noopener" target="_blank">Lista de cookies de Cloudflare</a>.</p>
<p>La web tampoco usa otras formas de almacenamiento en el navegador (como localStorage).</p>
<h2>Tipografías de Google</h2>
<p>Las tipografías de la web se cargan desde Google Fonts. Google Fonts no instala cookies, pero tu navegador contacta con los servidores de Google, que reciben tu dirección IP. Detalles en la <a href="{P("privacy")}">política de privacidad</a>.</p>
<h2>Webs externas</h2>
<p>Al hacer clic en un enlace a una tienda (por ejemplo Amazon) o a otra fuente, sales de PadelMetrix: esa web puede usar sus propias cookies, reguladas por su política de cookies. Así es como las tiendas reconocen las compras que llegan a través de enlaces de afiliado.</p>
<h2>Cómo gestionar las cookies</h2>
<p>Puedes ver y borrar las cookies desde los ajustes del navegador, y bloquearlas todas o solo las de terceros. En esta web, bloquearlas no cambia nada en el funcionamiento de las páginas.</p>
<h2>Contacto</h2>
<p>Para cualquier duda: {MAIL}. Si en el futuro añadimos estadísticas o publicidad, actualizaremos esta página y pediremos el consentimiento cuando sea necesario.</p>
</div>''')
    if C.attivo():
        corpo = ga_cookie(corpo)
    path, alt = P("cookie"), ALT("cookie")
    S.scrivi(path, pagina(L("Cookie policy | PadelMetrix", "Cookie policy | PadelMetrix", "Política de cookies | PadelMetrix"),
                          L("PadelMetrix non usa cookie propri, di analisi o pubblicitari: quali cookie tecnici possono essere impostati e come gestirli.",
                            "PadelMetrix uses no own, analytics or advertising cookies: which technical cookies may be set and how to manage them.",
                            "PadelMetrix no usa cookies propias, de análisis ni publicitarias: qué cookies técnicas pueden instalarse y cómo gestionarlas."),
                          path, corpo, ld=[ld], alt=alt), alt)


GA_PRIV = {
    "it": ("non usa cookie propri, non usa strumenti di analisi né pubblicità profilata.</b>",
           "non usa pubblicità profilata e usa Google Analytics solo se lo accetti.</b>",
           "<li><b>Google Analytics 4</b> (Google Ireland Ltd / Google LLC), gestito tramite Google Tag Manager: <b>solo se accetti i cookie</b> nel banner, raccoglie in forma statistica le pagine visitate, la provenienza delle visite, il tipo di dispositivo e la posizione approssimativa. Google dichiara che GA4 non registra né conserva gli indirizzi IP. Usiamo questi dati solo per capire quali contenuti sono utili; non li usiamo per pubblicità e non li incrociamo con altri dati. Base giuridica: il tuo consenso (art. 6.1.a GDPR), che puoi revocare in qualsiasi momento dal link «Preferenze cookie» in fondo a ogni pagina. Conservazione dei dati in Analytics: 14 mesi.</li>"),
    "en": ("does not set its own cookies and uses no analytics or targeted advertising.</b>",
           "uses no targeted advertising and uses Google Analytics only if you accept it.</b>",
           "<li><b>Google Analytics 4</b> (Google Ireland Ltd / Google LLC), managed through Google Tag Manager: <b>only if you accept cookies</b> in the banner, it collects statistical data on the pages visited, where visits come from, device type and approximate location. Google states that GA4 does not log or store IP addresses. We use this data only to understand which content is useful; we do not use it for advertising or combine it with other data. Legal basis: your consent (Art. 6(1)(a) GDPR), which you can withdraw at any time via the \"Cookie preferences\" link at the bottom of every page. Data retention in Analytics: 14 months.</li>"),
    "es": ("no usa cookies propias ni herramientas de análisis ni publicidad personalizada.</b>",
           "no usa publicidad personalizada y usa Google Analytics solo si lo aceptas.</b>",
           "<li><b>Google Analytics 4</b> (Google Ireland Ltd / Google LLC), gestionado mediante Google Tag Manager: <b>solo si aceptas las cookies</b> en el banner, recoge de forma estadística las páginas visitadas, la procedencia de las visitas, el tipo de dispositivo y la ubicación aproximada. Google declara que GA4 no registra ni almacena las direcciones IP. Usamos estos datos solo para saber qué contenidos son útiles; no los usamos para publicidad ni los cruzamos con otros datos. Base jurídica: tu consentimiento (art. 6.1.a RGPD), que puedes retirar en cualquier momento desde el enlace «Preferencias de cookies» al pie de cada página. Conservación de los datos en Analytics: 14 meses.</li>"),
}


def ga_privacy(corpo):
    vecchio, nuovo, voce = GA_PRIV[S.lang()]
    corpo = corpo.replace(vecchio, nuovo)
    corpo = corpo.replace(L("non usa cookie propri, ", "", "no usa cookies propias, "), "")
    return corpo.replace("</ul>\n<p>Cloudflare", voce + "</ul>\n<p>Cloudflare", 1).replace("</ul>\n<p>Cloudflare and Google", voce + "</ul>\n<p>Cloudflare and Google", 1).replace("</ul>\n<p>Cloudflare y Google", voce + "</ul>\n<p>Cloudflare y Google", 1)


GA_COOKIE = {
    "it": ("non installa cookie propri e non usa cookie di analisi, di profilazione o pubblicitari.</b> Per questo il sito non mostra un banner per il consenso.",
           "usa cookie di analisi (Google Analytics) solo se li accetti dal banner, e non usa mai cookie di profilazione o pubblicitari.</b>",
           "<tr><td>Cookie di analisi (statistiche)</td><td>No</td></tr>",
           "<tr><td>Cookie di analisi (Google Analytics: <code>_ga</code>, <code>_ga_*</code>)</td><td>Sì, solo con il tuo consenso; durata fino a 2 anni</td></tr>",
           "<h2>Caratteri tipografici di Google</h2>",
           "<h2>Google Analytics e consenso</h2><p>Google Analytics 4, caricato tramite Google Tag Manager, si attiva solo dopo che clicchi «Accetta» nel banner. Se rifiuti, Tag Manager non viene nemmeno caricato. La tua scelta viene salvata nel browser (voce tecnica <code>pm_consenso</code>, senza dati personali) e puoi cambiarla in ogni momento dal link «Preferenze cookie» in fondo alla pagina. <a href=\"https://policies.google.com/technologies/cookies\" rel=\"noopener\" target=\"_blank\">Come Google usa i cookie</a>.</p>\n<h2>Caratteri tipografici di Google</h2>",
           "<p>Il sito non usa nemmeno altre forme di memorizzazione nel browser (come localStorage).</p>", "",
           "Se in futuro aggiungeremo statistiche o pubblicità", "Se in futuro aggiungeremo pubblicità"),
    "en": ("does not set its own cookies and uses no analytics, profiling or advertising cookies.</b> That is why the site shows no consent banner.",
           "uses analytics cookies (Google Analytics) only if you accept them in the banner, and never uses profiling or advertising cookies.</b>",
           "<tr><td>Analytics cookies (statistics)</td><td>No</td></tr>",
           "<tr><td>Analytics cookies (Google Analytics: <code>_ga</code>, <code>_ga_*</code>)</td><td>Yes, only with your consent; lasting up to 2 years</td></tr>",
           "<h2>Google typefaces</h2>",
           "<h2>Google Analytics and consent</h2><p>Google Analytics 4, loaded through Google Tag Manager, is only activated after you click \"Accept\" in the banner. If you reject, Tag Manager is not even loaded. Your choice is saved in your browser (a technical entry, <code>pm_consenso</code>, with no personal data) and you can change it at any time via the \"Cookie preferences\" link at the bottom of the page. <a href=\"https://policies.google.com/technologies/cookies\" rel=\"noopener\" target=\"_blank\">How Google uses cookies</a>.</p>\n<h2>Google typefaces</h2>",
           "<p>The site does not use other forms of browser storage either (such as localStorage).</p>", "",
           "If we add statistics or advertising in the future", "If we add advertising in the future"),
    "es": ("no instala cookies propias ni usa cookies de análisis, de perfilado ni publicitarias.</b> Por eso la web no muestra un banner de consentimiento.",
           "usa cookies de análisis (Google Analytics) solo si las aceptas en el banner, y nunca usa cookies de perfilado ni publicitarias.</b>",
           "<tr><td>Cookies de análisis (estadísticas)</td><td>No</td></tr>",
           "<tr><td>Cookies de análisis (Google Analytics: <code>_ga</code>, <code>_ga_*</code>)</td><td>Sí, solo con tu consentimiento; duración de hasta 2 años</td></tr>",
           "<h2>Tipografías de Google</h2>",
           "<h2>Google Analytics y consentimiento</h2><p>Google Analytics 4, cargado mediante Google Tag Manager, solo se activa después de que hagas clic en «Aceptar» en el banner. Si rechazas, Tag Manager ni siquiera se carga. Tu elección se guarda en el navegador (una entrada técnica, <code>pm_consenso</code>, sin datos personales) y puedes cambiarla en cualquier momento desde el enlace «Preferencias de cookies» al pie de la página. <a href=\"https://policies.google.com/technologies/cookies\" rel=\"noopener\" target=\"_blank\">Cómo usa Google las cookies</a>.</p>\n<h2>Tipografías de Google</h2>",
           "<p>La web tampoco usa otras formas de almacenamiento en el navegador (como localStorage).</p>", "",
           "Si en el futuro añadimos estadísticas o publicidad", "Si en el futuro añadimos publicidad"),
}


def ga_cookie(corpo):
    t = GA_COOKIE[S.lang()]
    for a, b in zip(t[0::2], t[1::2]):
        assert a in corpo, a[:50]
        corpo = corpo.replace(a, b)
    return corpo


def contatti():
    cr, ld = crumbs([S.home_crumb(), (L("Contatti", "Contact", "Contacto"), None)])
    corpo = L(f'''{cr}
<div class="intro"><h1>Contatti</h1>
<p><b>Per qualsiasi richiesta scrivi a {MAIL}.</b> Rispondo personalmente, di solito entro pochi giorni.</p></div>
<div class="prose">
<h2>Per i giocatori</h2>
<ul>
<li><b>Hai trovato un dato sbagliato o mancante?</b> Indicami la racchetta e, se puoi, la fonte (sito del produttore, scheda del negozio). Correggo la scheda e cito la fonte.</li>
<li><b>Vorresti una racchetta che non trovi?</b> Scrivimi marca, modello e anno: la aggiungo quando trovo dati verificabili.</li>
</ul>
<h2>Per negozi e marchi</h2>
<p>PadelMetrix confronta le racchette con dati dichiarati e fonti citate. Se gestisci un negozio di padel o un marchio, puoi scrivermi per:</p>
<ul>
<li><b>programmi di affiliazione</b>: aggiungere il tuo negozio tra quelli indicati nelle schede, accanto ad Amazon;</li>
<li><b>schede tecniche e dati ufficiali</b> dei tuoi modelli, per completare quelli che oggi risultano "non dichiarati";</li>
<li><b>nuove collezioni</b>, per inserirle nel database appena escono.</li>
</ul>
<p>Le regole restano le stesse per tutti: i confronti, i voti e le classifiche non si comprano e non dipendono dagli accordi di affiliazione. I link di affiliazione sono sempre indicati come tali. Il metodo è spiegato nella pagina <a href="{P("chi-siamo")}">Chi siamo e metodo</a>.</p>
<h2>Privacy</h2>
<p>Uso il tuo indirizzo e il contenuto del messaggio solo per risponderti. Dettagli nell'<a href="{P("privacy")}">informativa sulla privacy</a>.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Contact</h1>
<p><b>For any request, write to {MAIL}.</b> I reply personally, usually within a few days.</p></div>
<div class="prose">
<h2>For players</h2>
<ul>
<li><b>Found a wrong or missing figure?</b> Tell me the racket and, if you can, the source (manufacturer's site, shop listing). I'll fix the page and cite the source.</li>
<li><b>Looking for a racket that isn't here?</b> Send me brand, model and year: I'll add it once I find verifiable data.</li>
</ul>
<h2>For shops and brands</h2>
<p>PadelMetrix compares rackets using declared data and cited sources. If you run a padel shop or a brand, you can write to me about:</p>
<ul>
<li><b>affiliate programmes</b>: adding your shop to those listed on the racket pages, next to Amazon;</li>
<li><b>official spec sheets and data</b> for your models, to fill in what is currently "not stated";</li>
<li><b>new collections</b>, so they can be added to the database as soon as they launch.</li>
</ul>
<p>The rules are the same for everyone: comparisons, scores and rankings cannot be bought and do not depend on affiliate agreements. Affiliate links are always labelled as such. The method is explained on the <a href="{P("chi-siamo")}">About and method</a> page.</p>
<h2>Privacy</h2>
<p>I use your address and the content of your message only to reply to you. Details in the <a href="{P("privacy")}">privacy policy</a>.</p>
</div>''', f'''{cr}
<div class="intro"><h1>Contacto</h1>
<p><b>Para cualquier consulta escribe a {MAIL}.</b> Respondo personalmente, normalmente en pocos días.</p></div>
<div class="prose">
<h2>Para jugadores</h2>
<ul>
<li><b>¿Has encontrado un dato erróneo o que falta?</b> Indícame la pala y, si puedes, la fuente (web del fabricante, ficha de la tienda). Corrijo la ficha y cito la fuente.</li>
<li><b>¿Buscas una pala que no está?</b> Escríbeme marca, modelo y año: la añado cuando encuentre datos verificables.</li>
</ul>
<h2>Para tiendas y marcas</h2>
<p>PadelMetrix compara palas con datos declarados y fuentes citadas. Si gestionas una tienda de pádel o una marca, puedes escribirme para:</p>
<ul>
<li><b>programas de afiliación</b>: añadir tu tienda a las indicadas en las fichas, junto a Amazon;</li>
<li><b>fichas técnicas y datos oficiales</b> de tus modelos, para completar los que hoy figuran como "no declarados";</li>
<li><b>nuevas colecciones</b>, para incluirlas en la base de datos en cuanto salgan.</li>
</ul>
<p>Las reglas son las mismas para todos: las comparativas, las notas y los rankings no se compran y no dependen de los acuerdos de afiliación. Los enlaces de afiliado siempre se indican como tales. El método se explica en la página <a href="{P("chi-siamo")}">Quiénes somos y método</a>.</p>
<h2>Privacidad</h2>
<p>Uso tu dirección y el contenido del mensaje solo para responderte. Detalles en la <a href="{P("privacy")}">política de privacidad</a>.</p>
</div>''')
    org = {"@context": "https://schema.org", "@type": "ContactPage", "name": L("Contatti", "Contact", "Contacto"), "url": S.SITO + P("contatti"),
           "mainEntity": {"@type": "Organization", "name": "PadelMetrix", "url": S.SITO, "email": EMAIL,
                          "contactPoint": {"@type": "ContactPoint", "email": EMAIL, "contactType": "customer support", "availableLanguage": ["it", "en", "es"]}}}
    path, alt = P("contatti"), ALT("contatti")
    S.scrivi(path, pagina(L("Contatti | PadelMetrix", "Contact | PadelMetrix", "Contacto | PadelMetrix"),
                          L("Scrivi a PadelMetrix: segnalazioni sui dati delle racchette, richieste di nuovi modelli, affiliazioni per negozi e schede tecniche per i marchi.",
                            "Write to PadelMetrix: corrections to racket data, requests for new models, affiliate partnerships for shops and spec sheets from brands.",
                            "Escribe a PadelMetrix: correcciones de datos de palas, peticiones de nuevos modelos, afiliaciones para tiendas y fichas técnicas para marcas."),
                          path, corpo, ld=[ld, org], alt=alt), alt)


def main():
    for l in LINGUE:
        set_lang(l)
        privacy()
        cookie()
        contatti()
    set_lang("it")
    (ROOT / "scripts" / "pagine_legale.json").write_text(json.dumps(S.PAGINE, indent=0), encoding="utf-8")
    print(len(S.PAGINE), "pagine legali generate")


if __name__ == "__main__":
    main()
