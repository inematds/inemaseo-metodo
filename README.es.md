# 🔎 inemaSEO — tu sitio en primer plano

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![inemaSEO — tu sitio en primer plano](guia/assets/banner-es.jpg)](https://inematds.github.io/inemaseo-metodo/guia/es/)

El método que usamos en el ecosistema INEMA para que nos encuentren en **Google**, en **Bing** y en las respuestas
de las **IAs** (ChatGPT, Perplexity, Copilot, AI Overviews), sin herramientas de pago y sin contenido inventado.
Los agentes de IA hacen el trabajo repetitivo; el humano decide.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/inemaseo-metodo/guia/es/**

## Las 10 etapas

1. **Auditoría real:** el HTML que entrega el servidor (canónico, hreflang, JSON-LD, enlaces internos).
2. **Base técnica:** canónico único, sitemaps con idioma, robots que habilita a las IAs, `llms.txt`, manifiesto de contenido, `noindex` en páginas superficiales.
3. **Medición sin la marca:** Search Console semanal que separa las búsquedas por tu nombre.
4. **Entidad:** `Person` + `Organization` con `@id` fijo en todas las páginas y subdominios.
5. **Un territorio por sitio:** evergreen, noticias y eventos en lugares distintos; una página dueña por intención.
6. **Contenido propio:** pilares, páginas de pregunta con respuesta directa, fichas con datos extraídos y validados.
7. **Hubs y enlaces internos:** escalera de enlaces, páginas hub que leen el manifiesto de los otros sitios.
8. **Enlaces de vuelta:** cada satélite enlaza la página correcta del sitio principal.
9. **Noticias con página propia:** `NewsArticle`, archivo permanente, cuerpo mínimo solo con hechos de la fuente.
10. **Avisar y dar seguimiento:** IndexNow + Bing en cada publicación, lectura semanal, prueba mensual en las IAs.

Detalles, puntaje de palabras clave y plan B: [docs/METODO.md](docs/METODO.md) (en portugués) ·
lista de verificación de publicación: [docs/CHECKLIST.md](docs/CHECKLIST.md) (en portugués).

## Herramientas

| Archivo | Qué hace |
|---|---|
| `tools/auditoria.sh` | diagnóstico de SEO técnico de un sitio (solo lectura) |
| `tools/gsc_semanal.py` | exportación semanal de Search Console que separa la marca |
| `tools/gsc_inspecionar.py` | estado de indexación de cada URL (URL Inspection API) |
| `tools/avisar_buscadores.sh` | IndexNow + Bing Webmaster, solo con URLs que responden 200 |
| `tools/link_de_volta.py` | enlace de vuelta de los satélites al sitio principal, por lotes, con dry-run |
| `tools/validar_extracao.mjs` | freno anti-invención para texto generado por LLM |
| `templates/` | `robots.txt`, `llms.txt`, `content-index.json`, JSON-LD de entidad y de noticia, prompts |

Nada aquí contiene claves, IDs ni datos de sitios: todo entra por variable de entorno o argumento.

## Proyectos relacionados

- [WebMCP Readiness](https://webmcp.inema.pro/): comprueba si tu sitio está listo para agentes de IA.
- [Formación WebMCP](https://inematds.github.io/webmcp-1-formacao/): cinco cursos, de cero a experto.
- [AIV 2026 — AI Visibility](https://inematds.github.io/aiv2026/guia/): playbook de AEO/GEO.
- [WebMCP en Eventos INEMA](https://eventos.inema.pro/webmcp/)
- [claude-seo](https://github.com/inematds/claude-seo): skill de análisis de SEO para Claude Code.
- [Aprender IA en INEMA.CLUB](https://www.inema.club/aprender-inteligencia-artificial/)

---

Licencia MIT · [INEMA.CLUB](https://inema.club)
