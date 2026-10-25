"""Google Tag Manager + Google Analytics 4 con consenso preventivo (banner cookie in it/en/es).

Imposta GTM_ID e GA4_ID: finché GTM_ID è None non viene inserito nulla nelle pagine
e le pagine Privacy/Cookie dicono che non ci sono analytics.

Funzionamento (Consent Mode di Google in modalità "base"):
- consenso predefinito negato per tutte le categorie;
- Tag Manager viene caricato SOLO dopo che il visitatore clicca "Accetta";
- la scelta resta nel browser (localStorage "pm_consenso") e si può cambiare dal link
  "Preferenze cookie" nel footer;
- nessun cookie pubblicitario: ad_storage resta sempre negato.
"""

GTM_ID = "GTM-TGBVDSQM"
GA4_ID = "G-GMK0SLHCDG"  # configurato dentro Tag Manager


def attivo():
    return bool(GTM_ID)


TESTI = {
    "it": ("Usiamo cookie di Google Analytics per contare le visite e capire quali pagine sono utili. Li attiviamo solo se accetti.",
           "Accetta", "Rifiuta", "Cookie policy", "Preferenze cookie"),
    "en": ("We use Google Analytics cookies to count visits and see which pages are useful. We only turn them on if you accept.",
           "Accept", "Reject", "Cookie policy", "Cookie preferences"),
    "es": ("Usamos cookies de Google Analytics para contar las visitas y saber qué páginas son útiles. Solo las activamos si aceptas.",
           "Aceptar", "Rechazar", "Política de cookies", "Preferencias de cookies"),
}


def head(lang):
    """Da inserire subito dopo <meta charset>."""
    if not attivo():
        return ""
    return ("<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}"
            "gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied'});"
            "window.pmGTM=function(){if(window.pmGTMok)return;window.pmGTMok=1;gtag('consent','update',{analytics_storage:'granted'});"
            "(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})"
            f"(window,document,'script','dataLayer','{GTM_ID}');}};"
            "try{if(localStorage.getItem('pm_consenso')==='si')window.pmGTM();}catch(e){}</script>")


CSS = """<style>
#pm-cc{position:fixed;left:16px;right:16px;bottom:16px;z-index:50;max-width:720px;margin:0 auto;background:#fff;color:#1F2D27;border:1px solid #E1E5DF;border-radius:14px;box-shadow:0 8px 30px rgba(0,0,0,.15);padding:16px 18px;display:none;font:15px/1.5 'IBM Plex Sans',system-ui,sans-serif}
#pm-cc p{margin:0 0 12px}#pm-cc .b{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
#pm-cc button{flex:1 1 140px;font:600 15px 'IBM Plex Sans',system-ui,sans-serif;padding:11px 16px;border-radius:10px;cursor:pointer;border:1.5px solid #0F3D2E;background:#fff;color:#0F3D2E}
#pm-cc button.ok{background:#0F3D2E;color:#fff}#pm-cc a{color:#0F3D2E;font-size:14px}
</style>"""


def body(lang, cookie_url):
    """Da inserire prima di </body>: banner e funzione per riaprirlo."""
    if not attivo():
        return ""
    txt, ok, no, link, _ = TESTI[lang]
    return (CSS + f'<div id="pm-cc" role="dialog" aria-live="polite" aria-label="Cookie"><p>{txt}</p><div class="b">'
            f'<button type="button" id="pm-no">{no}</button><button type="button" class="ok" id="pm-ok">{ok}</button>'
            f'<a href="{cookie_url}">{link}</a></div></div>'
            "<script>(function(){var b=document.getElementById('pm-cc');function set(v){try{localStorage.setItem('pm_consenso',v)}catch(e){}b.style.display='none';"
            "if(v==='si')window.pmGTM();else{document.cookie.split(';').forEach(function(x){var n=x.split('=')[0].trim();if(n.indexOf('_ga')===0){document.cookie=n+'=;Max-Age=0;path=/';document.cookie=n+'=;Max-Age=0;path=/;domain=.'+location.hostname.replace(/^www\\./,'');}});if(window.pmGTMok)location.reload();}}"
            "document.getElementById('pm-ok').onclick=function(){set('si')};document.getElementById('pm-no').onclick=function(){set('no')};"
            "window.pmApriCookie=function(){b.style.display='block';return false};"
            "var c=null;try{c=localStorage.getItem('pm_consenso')}catch(e){}if(!c)b.style.display='block';})();</script>")


def link_footer(lang):
    if not attivo():
        return ""
    return f'<a href="#" onclick="return pmApriCookie()">{TESTI[lang][4]}</a>'
