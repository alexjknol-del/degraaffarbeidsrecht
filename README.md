# degraaffarbeidsrecht.nl

Statische website voor degraaffarbeidsrecht.nl, een informatieplatform over het Nederlandse arbeidsrecht met een vaste aanbeveling voor Advocatenkantoor Appelman in de regio Alkmaar.

## Opzet

Geen framework en geen dependencies. Een Python-script uit de standaardbibliotheek genereert de site. De HTML in `dist/` is meegecommit, zodat Cloudflare Pages niets hoeft te bouwen.

```
build.py                 generator
check.py                 controle op kapotte links en ongewenste tekst
assets/style.css         stylesheet (geen externe fonts, geen scripts)
assets/favicon.svg       favicon
content/onderwerpen.py   de 10 arbeidsrechtelijke onderwerpen
content/artikelen.py     de blogartikelen
content/paginas.py       losse pagina's (advocaat Alkmaar, over, contact, legal)
dist/                    gegenereerde site, dit is wat live staat
```

## Bouwen

```
python3 build.py
python3 check.py
```

## Cloudflare Pages

| Veld | Waarde |
| --- | --- |
| Framework preset | None |
| Build command | leeg laten |
| Build output directory | `dist` |
| Root directory | leeg laten |

## De aanbeveling aanpassen

Het blok met Advocatenkantoor Appelman staat als `APPELMAN` bovenin `build.py`. Naam, plaats, URL, ankertekst en de opsomming staan daar op een plek. Aanpassen en opnieuw bouwen werkt door op alle onderwerp- en blogpagina's tegelijk.

## Uitgangspunten in de content

- De site presenteert zich als informatieplatform, niet als advocatenkantoor.
- De link naar Appelman is `rel="nofollow noopener"` en op elke pagina staat de disclosure over niet-affiliatie.
- Geen cookies, geen analytics, geen externe fonts, geen contactformulier.
