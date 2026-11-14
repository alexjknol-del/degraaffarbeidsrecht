#!/usr/bin/env python3
"""Statische sitegenerator voor degraaffarbeidsrecht.nl. Alleen standaardbibliotheek."""
import os, shutil, html, datetime, re, sys, json

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
sys.path.insert(0, ROOT)

from content.onderwerpen import ONDERWERPEN
from content.artikelen import ARTIKELEN
from content.paginas import PAGINAS
from content.kantoren import KANTOREN

BASE = "https://degraaffarbeidsrecht.nl"
NAAM = "De Graaff Arbeidsrecht"

MENU = [
    ("/", "Home"),
    ("/onderwerpen/", "Onderwerpen"),
    ("/advocaten/", "Advocaten"),
    ("/blog/", "Blog"),
    ("/over/", "Over"),
    ("/contact/", "Contact"),
]

FOOT_LEGAL = [
    ("/partners/", "Partners"),
    ("/privacybeleid/", "Privacybeleid"),
    ("/cookiebeleid/", "Cookiebeleid"),
    ("/disclaimer/", "Disclaimer"),
]

DISCLOSURE = ("Dit is een informatieplatform en geen advocatenkantoor. Er bestaan geen samenwerkingen "
              "met advocatenkantoren en kantoren betalen niet voor vermelding.")

APPELMAN = {
    "naam": "Advocatenkantoor Appelman",
    "plaats": "Nieuwlandersingel 53, Alkmaar",
    "url": "https://appelman.nl/juridische-diensten/arbeidsrecht/",
    "anchor": "Arbeidsrecht advocaat bij Advocatenkantoor Appelman",
    "punten": [
        "Voert arbeidsrecht als vaste praktijk, met aparte pagina's over onder meer vaststellingsovereenkomst, ontslag op staande voet, ontslag tijdens ziekte, proeftijd, schorsing en het nulurencontract.",
        "Vermeldt op de eigen site meer dan dertig jaar ervaring en ruim 5.000 behandelde zaken.",
        "Gevestigd aan de Nieuwlandersingel 53 in Alkmaar, telefonisch bereikbaar op 072 512 32 29.",
        "Biedt een kosteloos kennismakingsgesprek en behandelt zaken ook op toevoegingsbasis.",
    ],
}


def esc(s):
    return html.escape(s, quote=True)


def slugify(s):
    s = s.lower()
    for a, b in [("á","a"),("é","e"),("ë","e"),("ï","i"),("ó","o"),("ö","o"),("ü","u"),("è","e")]:
        s = s.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def strip_tags(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()


MONTHS = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]

def nl_date(iso):
    d = datetime.date.fromisoformat(iso)
    return f"{d.day} {MONTHS[d.month-1]} {d.year}"


def rfc822(iso):
    return datetime.datetime.fromisoformat(iso).strftime("%a, %d %b %Y 09:00:00 +0100")


def page(*, path, title, description, body, crumbs=None, jsonld=None, active=None, noindex=False):
    url = BASE + path
    nav = []
    for h, l in MENU:
        cls = ' class="on"' if active == h else ""
        nav.append('<li><a href="%s"%s>%s</a></li>' % (esc(h), cls, esc(l)))
    nav = "".join(nav)

    crumb_html = ""
    if crumbs:
        parts = []
        for href, label in crumbs:
            parts.append(f'<a href="{esc(href)}">{esc(label)}</a>' if href else f'<span aria-current="page">{esc(label)}</span>')
        crumb_html = '<nav class="crumbs wrap" aria-label="Kruimelpad">' + '<span class="sep">/</span>'.join(parts) + "</nav>"

    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    canon = "" if noindex else f'<link rel="canonical" href="{esc(url)}">\n<meta property="og:url" content="{esc(url)}">\n'
    ld = f'<script type="application/ld+json">{jsonld}</script>' if jsonld else ""

    out = f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
{canon}<meta property="og:type" content="website">
<meta property="og:locale" content="nl_NL">
<meta property="og:site_name" content="{esc(NAAM)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta name="twitter:card" content="summary">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="#0d1b16">
<link rel="stylesheet" href="/assets/style.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<link rel="alternate" type="application/rss+xml" title="Blog van {esc(NAAM)}" href="/blog/rss.xml">
{ld}
</head>
<body>
<a class="skip" href="#main">Naar hoofdinhoud</a>
<header class="hd">
  <div class="wrap hd-in">
    <a class="logo" href="/">
      <span class="logo-bug" aria-hidden="true">dG</span>
      <span class="logo-tx"><b>De Graaff</b><i>Arbeidsrecht</i></span>
    </a>
    <input type="checkbox" id="nt" class="nt">
    <label for="nt" class="burger" aria-hidden="true"><span></span><span></span><span></span></label>
    <nav class="nav" aria-label="Hoofdmenu"><ul>{nav}</ul></nav>
  </div>
</header>
<main id="main">
{crumb_html}
{body}
</main>
<footer class="ft">
  <div class="wrap ft-top">
    <div class="ft-brand">
      <span class="logo-bug" aria-hidden="true">dG</span>
      <p>Landelijk platform met uitleg over het Nederlandse arbeidsrecht, in gewone taal en met de termijnen erbij.</p>
      <p class="ft-disc">{esc(DISCLOSURE)}</p>
    </div>
    <div class="ft-col"><h2>Onderwerpen</h2><ul>{"".join(f'<li><a href="/onderwerpen/{esc(o["slug"])}/">{esc(o["titel"])}</a></li>' for o in ONDERWERPEN[:6])}</ul></div>
    <div class="ft-col"><h2>Meer</h2><ul>{"".join(f'<li><a href="/onderwerpen/{esc(o["slug"])}/">{esc(o["titel"])}</a></li>' for o in ONDERWERPEN[6:])}</ul></div>
    <div class="ft-col"><h2>Site</h2><ul>{"".join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in MENU[2:])}{"".join(f'<li><a href="{esc(h)}">{esc(l)}</a></li>' for h, l in FOOT_LEGAL)}</ul>
      <p class="ft-mail"><a href="mailto:info@degraaffarbeidsrecht.nl">info@degraaffarbeidsrecht.nl</a></p></div>
  </div>
  <div class="wrap ft-bot">
    <p>&copy; {datetime.date.today().year} {esc(NAAM)}</p>
    <p>Algemene informatie, geen juridisch advies.</p>
  </div>
</footer>
</body>
</html>
"""
    d = os.path.join(DIST, path.strip("/"))
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(out)
    return path


def appelman_card(context):
    punten = "".join(f"<li>{p}</li>" for p in APPELMAN["punten"])
    return f"""<aside class="promo">
  <p class="promo-eyebrow">Aanbevolen kantoor</p>
  <h2 class="promo-name">{esc(APPELMAN['naam'])}</h2>
  <p class="promo-sub">{esc(context)}</p>
  <ul class="promo-list">{punten}</ul>
  <p><a class="btn" href="{esc(APPELMAN['url'])}" rel="nofollow noopener" target="_blank">{esc(APPELMAN['anchor'])}</a></p>
  <p class="promo-url">{esc(APPELMAN['url'])}</p>
  <p class="promo-meer"><a href="/advocaten/">Kantoren in andere regio's</a></p>
</aside>"""


def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))
    urls = []
    by_slug = {o["slug"]: o for o in ONDERWERPEN}

    # home
    tiles = "".join(
        f"""<li><a href="/onderwerpen/{esc(o['slug'])}/"><span class="num">{i:02d}</span>
        <h3>{esc(o['titel'])}</h3><p>{esc(o['kort'])}</p>
        <span class="tag">{esc(o['termijn_label'])}</span></a></li>"""
        for i, o in enumerate(ONDERWERPEN, 1)
    )
    posts = sorted(ARTIKELEN, key=lambda a: a["datum"], reverse=True)[:3]
    plist = "".join(
        f"""<li><a href="/blog/{esc(a['slug'])}/"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time>
        <h3>{esc(a['titel'])}</h3><p>{esc(a['samenvatting'])}</p></a></li>""" for a in posts
    )
    home = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-tx">
      <p class="kicker">Arbeidsrecht in gewone taal</p>
      <h1>Ontslag draait op termijnen. Die lopen af terwijl er nog wordt overlegd.</h1>
      <p class="lead">Veertien dagen bedenktijd. Twee maanden om een ontslag op staande voet aan te vechten. Drie maanden voor de transitievergoeding. Deze site legt per onderwerp uit welke regel geldt, welke klok loopt en waar zaken in de praktijk stranden.</p>
      <p class="cta"><a class="btn" href="/onderwerpen/">Bekijk de onderwerpen</a> <a class="btn ghost" href="/advocaten/">Advocaten per regio</a></p>
    </div>
    <div class="hero-panel">
      <h2>Termijnen die zaken laten stranden</h2>
      <dl>
        <div><dt>14 dagen</dt><dd>Bedenktijd na tekenen van een vaststellingsovereenkomst</dd></div>
        <div><dt>2 maanden</dt><dd>Ontslag op staande voet aanvechten bij de kantonrechter</dd></div>
        <div><dt>3 maanden</dt><dd>Transitievergoeding opeisen na einde dienstverband</dd></div>
        <div><dt>104 weken</dt><dd>Loondoorbetaling bij ziekte voordat WIA in beeld komt</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="wrap sect">
  <div class="sect-hd"><h2>Onderwerpen</h2><p>Tien onderwerpen die in vrijwel elk arbeidsconflict terugkomen.</p></div>
  <ul class="tiles">{tiles}</ul>
</section>

<section class="band">
  <div class="wrap sect promo-wrap">
    <div>
      <p class="kicker">Advocatengids</p>
      <h2>Per regio een arbeidsrechtadvocaat</h2>
      <p>Bij een aangeboden vaststellingsovereenkomst, een ontslag op staande voet of een vastgelopen re-integratie telt vooral snelheid, want er loopt dan al een termijn. De gids noemt per regio een kantoor met een aantoonbaar arbeidsrechtprofiel, en legt uit waarop die selectie berust.</p>
      <p><a class="lnk" href="/advocaten/">Bekijk de advocatengids</a></p>
    </div>
    {appelman_card("Arbeidsrecht voor werknemers en werkgevers in Noord-Holland")}
  </div>
</section>

<section class="wrap sect">
  <div class="sect-hd"><h2>Blog</h2><p>Wetswijzigingen en praktijkvragen, kort uitgelegd.</p></div>
  <ul class="posts">{plist}</ul>
  <p class="more"><a class="lnk" href="/blog/">Alle artikelen</a></p>
</section>
"""
    urls.append(page(path="/", title=f"{NAAM} | Arbeidsrecht en ontslag uitgelegd",
                     description="Arbeidsrecht in gewone taal: ontslagroutes, vaststellingsovereenkomst, transitievergoeding, concurrentiebeding, ziekte en re-integratie, met de termijnen die daarbij horen.",
                     body=home, active="/",
                     jsonld=json.dumps({"@context":"https://schema.org","@type":"WebSite","name":NAAM,"url":BASE+"/","inLanguage":"nl-NL"}, ensure_ascii=False)))

    # onderwerpen index
    rows = "".join(
        f"""<li><a href="/onderwerpen/{esc(o['slug'])}/"><span class="num">{i:02d}</span>
        <h3>{esc(o['titel'])}</h3><p>{esc(o['kort'])}</p><span class="tag">{esc(o['termijn_label'])}</span></a></li>"""
        for i, o in enumerate(ONDERWERPEN, 1))
    body = f"""
<section class="wrap ph">
  <p class="kicker">Onderwerpen</p>
  <h1>Tien onderwerpen uit het arbeidsrecht</h1>
  <p class="lead">Elk onderwerp behandelt de regel, de termijn die erbij hoort en de punten waarop het in de praktijk misgaat.</p>
</section>
<section class="wrap sect"><ul class="tiles">{rows}</ul></section>
"""
    urls.append(page(path="/onderwerpen/", title=f"Onderwerpen arbeidsrecht | {NAAM}",
                     description="Overzicht van tien arbeidsrechtelijke onderwerpen: ontslagroutes, vaststellingsovereenkomst, transitievergoeding, concurrentiebeding, ziekte en re-integratie.",
                     body=body, crumbs=[("/","Home"),(None,"Onderwerpen")], active="/onderwerpen/"))

    # advocatengids
    kaarten = "".join(
        f"""<li class="firm-card">
        <p class="firm-regio">{esc(k['regio'])}</p>
        <h3>{esc(k['naam'])}</h3>
        <p class="firm-plaats">{esc(k['plaats'])}</p>
        <p class="firm-typering">{esc(k['typering'])}</p>
        <ul class="firm-waarom">{''.join(f'<li>{esc(w)}</li>' for w in k['waarom'])}</ul>
        <p class="firm-cta"><a href="{esc(k['url'])}" rel="nofollow noopener" target="_blank">{esc(k['anchor'])}</a></p>
        </li>""" for k in KANTOREN
    )
    body = f"""
<section class="wrap ph">
  <p class="kicker">Advocatengids</p>
  <h1>Arbeidsrechtadvocaten per regio</h1>
  <p class="lead">Een landelijk overzicht van kantoren met een aantoonbaar arbeidsrechtprofiel, per regio een. Daaronder staat waarop de selectie berust en wat een eerste gesprek oplevert.</p>
</section>
<section class="wrap sect">
  <ul class="grid firm-cards">{kaarten}</ul>
</section>
<section class="band">
  <div class="wrap sect">
    <div class="sect-hd"><h2>Waarop de selectie berust</h2><p>Per regio is gezocht naar een kantoor waarvan de specialisatie te controleren valt, niet naar het kantoor dat het hardst adverteert.</p></div>
    <ol class="steps">
      <li><h3>Toetsbare specialisatie</h3><p>Lidmaatschap van de VAAN, de specialisatievereniging voor arbeidsrechtadvocaten, of registratie op arbeidsrecht in het rechtsgebiedenregister van de Nederlandse orde van advocaten. Dat register verplicht tot tien opleidingspunten per jaar per geregistreerd rechtsgebied.</p></li>
      <li><h3>Praktijk boven profiel</h3><p>Een kantoor dat zich tot arbeidsrecht beperkt of er een aparte sectie voor heeft, weegt zwaarder dan een algemene praktijk die arbeidsrecht als bijvangst noemt.</p></li>
      <li><h3>Eigen vakinhoud</h3><p>Gepubliceerde artikelen, kronieken, docentschappen en specialisatieopleidingen laten zien dat het vak wordt bijgehouden.</p></li>
    </ol>
  </div>
</section>
<section class="wrap sect">
  <div class="sect-hd"><h2>Wat een eerste gesprek oplevert</h2></div>
  <div class="two-col">
    <div>
      <p>Bij een arbeidsconflict draait het eerste gesprek meestal om drie vragen: welke termijn loopt er op dit moment, wat is de positie op basis van de stukken, en wat is een realistische uitkomst.</p>
      <p>Nuttig om mee te nemen: de arbeidsovereenkomst en eventuele verlengingen, de toepasselijke cao, de laatste drie loonstroken, functionerings- en beoordelingsverslagen en de correspondentie over het conflict. Bij ziekte ook de probleemanalyse, het plan van aanpak en de evaluaties. Is er een vaststellingsovereenkomst aangeboden, neem dan de datum van ontvangst mee, want de bedenktijd loopt vanaf ondertekening.</p>
    </div>
    <div>
      <p>Wie onder de inkomens- en vermogensgrenzen valt, kan een toevoeging via de Raad voor Rechtsbijstand aanvragen en betaalt dan een eigen bijdrage. Een verwijzing via het Juridisch Loket verlaagt die bijdrage. Niet elk kantoor werkt op toevoegingsbasis; dat is een van de eerste dingen om na te vragen.</p>
      <p>Bij een vaststellingsovereenkomst nemen werkgevers vaak een bijdrage in de kosten van rechtsbijstand op in het voorstel. Wie een rechtsbijstandverzekering heeft, meldt de zaak daar eerst; bij een procedure met verplichte procesvertegenwoordiging geldt het recht op vrije advocaatkeuze.</p>
      <p>Zelf vergelijken kan via <a href="https://zoekeenadvocaat.advocatenorde.nl/" rel="nofollow noopener" target="_blank">zoekeenadvocaat.advocatenorde.nl</a>, het openbare register van de Nederlandse orde van advocaten. Daarin staat per advocaat welke rechtsgebieden zijn geregistreerd.</p>
    </div>
  </div>
</section>
"""
    urls.append(page(path="/advocaten/", title=f"Arbeidsrechtadvocaten per regio | {NAAM}",
                     description="Landelijk overzicht van arbeidsrechtadvocaten per regio, geselecteerd op toetsbare specialisatie. Met uitleg over wat een eerste gesprek oplevert en wat bijstand kost.",
                     body=body, crumbs=[("/","Home"),(None,"Advocaten")], active="/advocaten/"))

    # onderwerp detail
    for o in ONDERWERPEN:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in o["secties"])
        toc = "".join(f'<li><a href="#{slugify(k)}">{esc(k)}</a></li>' for k, _ in o["secties"])
        faq = ""
        faq_ld = None
        if o.get("faq"):
            faq = '<section class="faq"><h2 id="veelgestelde-vragen">Veelgestelde vragen</h2>' + "".join(
                f"<details><summary>{esc(q)}</summary><div>{a}</div></details>" for q, a in o["faq"]) + "</section>"
            toc += '<li><a href="#veelgestelde-vragen">Veelgestelde vragen</a></li>'
            faq_ld = json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
                {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":strip_tags(a)}} for q, a in o["faq"]]}, ensure_ascii=False)
        rel = ""
        if o.get("verwant"):
            rel = '<section class="rel"><h2>Verder lezen</h2><ul>' + "".join(
                f'<li><a href="/onderwerpen/{esc(s)}/">{esc(by_slug[s]["titel"])}</a></li>' for s in o["verwant"] if s in by_slug) + "</ul></section>"
        body = f"""
<section class="wrap ph">
  <p class="kicker">Onderwerp</p>
  <h1>{esc(o['titel'])}</h1>
  <p class="lead">{o['intro']}</p>
  <div class="klok"><span class="klok-lb">Kern in het kort</span><strong>{esc(o['termijn_label'])}</strong><span>{esc(o['termijn_uitleg'])}</span></div>
</section>
<div class="wrap cols">
  <article class="prose">
    <nav class="toc" aria-label="Inhoud"><h2>Op deze pagina</h2><ul>{toc}</ul></nav>
    {secties}{faq}{rel}
  </article>
  {appelman_card(o['titel'])}
</div>
"""
        urls.append(page(path=f"/onderwerpen/{o['slug']}/", title=f"{o['titel']} | {NAAM}",
                         description=o["meta"], body=body, jsonld=faq_ld,
                         crumbs=[("/","Home"),("/onderwerpen/","Onderwerpen"),(None,o["titel"])],
                         active="/onderwerpen/"))

    # blog
    arts = sorted(ARTIKELEN, key=lambda a: a["datum"], reverse=True)
    items = "".join(
        f"""<li><a href="/blog/{esc(a['slug'])}/"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time>
        <h3>{esc(a['titel'])}</h3><p>{esc(a['samenvatting'])}</p></a></li>""" for a in arts)
    urls.append(page(path="/blog/", title=f"Blog over arbeidsrecht | {NAAM}",
                     description="Artikelen over arbeidsrecht: wetswijzigingen, uitspraken en praktijkvragen over ontslag, ziekte en arbeidsvoorwaarden.",
                     body=f"""<section class="wrap ph"><p class="kicker">Blog</p><h1>Artikelen</h1>
<p class="lead">Ontwikkelingen in het arbeidsrecht, vertaald naar wat er in de praktijk verandert.</p></section>
<section class="wrap sect"><ul class="posts">{items}</ul></section>""",
                     crumbs=[("/","Home"),(None,"Blog")], active="/blog/"))

    for a in arts:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in a["secties"])
        rel = ""
        if a.get("onderwerpen"):
            rel = '<section class="rel"><h2>Meer over dit onderwerp</h2><ul>' + "".join(
                f'<li><a href="/onderwerpen/{esc(s)}/">{esc(by_slug[s]["titel"])}</a></li>' for s in a["onderwerpen"] if s in by_slug) + "</ul></section>"
        ld = json.dumps({"@context":"https://schema.org","@type":"Article","headline":a["titel"],
                         "datePublished":a["datum"],"inLanguage":"nl-NL",
                         "author":{"@type":"Organization","name":NAAM},
                         "publisher":{"@type":"Organization","name":NAAM},
                         "mainEntityOfPage":BASE+"/blog/"+a["slug"]+"/"}, ensure_ascii=False)
        body = f"""
<section class="wrap ph">
  <p class="kicker"><time datetime="{esc(a['datum'])}">{esc(nl_date(a['datum']))}</time></p>
  <h1>{esc(a['titel'])}</h1>
  <p class="lead">{esc(a['samenvatting'])}</p>
</section>
<div class="wrap cols">
  <article class="prose">{secties}{rel}
  <p class="art-foot">Algemene informatie, geen juridisch advies. Regelgeving verandert; voor een concrete zaak is contact met een advocaat nodig.</p></article>
  {appelman_card("Arbeidsrecht voor werknemers en werkgevers")}
</div>
"""
        urls.append(page(path=f"/blog/{a['slug']}/", title=f"{a['titel']} | {NAAM}",
                         description=a["meta"], body=body, jsonld=ld,
                         crumbs=[("/","Home"),("/blog/","Blog"),(None,a["titel"])], active="/blog/"))

    # losse pagina's
    for p in PAGINAS:
        secties = "".join(f'<h2 id="{slugify(k)}">{esc(k)}</h2>{v}' for k, v in p["secties"])
        extra = appelman_card(p["promo_context"]) if p.get("promo_context") else ""
        cols = "cols" if extra else "cols one"
        body = f"""
<section class="wrap ph">
  <p class="kicker">{esc(p.get('kicker','')) }</p>
  <h1>{esc(p['h1'])}</h1>
  <p class="lead">{p['lead']}</p>
</section>
<div class="wrap {cols}"><article class="prose">{secties}</article>{extra}</div>
"""
        urls.append(page(path=p["path"], title=p["title"], description=p["meta"], body=body,
                         crumbs=p.get("crumbs"), active=p.get("active")))

    # 404
    page(path="/nf-tmp/", title=f"Pagina niet gevonden | {NAAM}",
         description="De opgevraagde pagina bestaat niet.", noindex=True,
         body="""<section class="wrap ph"><p class="kicker">404</p><h1>Pagina niet gevonden</h1>
<p class="lead">Deze pagina bestaat niet of is verplaatst.</p>
<p class="cta"><a class="btn" href="/onderwerpen/">Naar de onderwerpen</a> <a class="btn ghost" href="/">Naar de homepage</a></p></section>""")
    shutil.move(os.path.join(DIST, "nf-tmp", "index.html"), os.path.join(DIST, "404.html"))
    shutil.rmtree(os.path.join(DIST, "nf-tmp"))

    today = datetime.date.today().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        pr = "1.0" if u == "/" else ("0.8" if u.startswith(("/onderwerpen/", "/blog/", "/advocaat")) else "0.5")
        sm.append(f"  <url><loc>{BASE}{u}</loc><lastmod>{today}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
    open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")

    rss_items = "".join(f"""  <item>
    <title>{esc(a['titel'])}</title>
    <link>{BASE}/blog/{a['slug']}/</link>
    <guid isPermaLink="true">{BASE}/blog/{a['slug']}/</guid>
    <pubDate>{rfc822(a['datum'])}</pubDate>
    <description>{esc(a['samenvatting'])}</description>
  </item>
""" for a in arts)
    open(os.path.join(DIST, "blog", "rss.xml"), "w", encoding="utf-8").write(
        f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Blog van {esc(NAAM)}</title>
  <link>{BASE}/blog/</link>
  <description>Artikelen over het Nederlandse arbeidsrecht.</description>
  <language>nl-nl</language>
{rss_items}</channel></rss>
""")
    open(os.path.join(DIST, "_headers"), "w", encoding="utf-8").write("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: SAMEORIGIN
  Permissions-Policy: geolocation=(), microphone=(), camera=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")
    print(f"{len(urls)} pagina's gebouwd in dist/")


if __name__ == "__main__":
    build()
