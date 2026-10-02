# 🔎 inemaSEO — your site in the spotlight

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![inemaSEO — your site in the spotlight](guia/assets/banner-en.jpg)](https://inematds.github.io/inemaseo-metodo/guia/en/)

The method we use across the INEMA ecosystem to get found on **Google**, **Bing** and in answers from
**AIs** (ChatGPT, Perplexity, Copilot, AI Overviews), with no paid tools and no invented content.
AI agents do the repetitive work; the human decides.

## 📖 User guide

Full guide (landing page + step by step): **https://inematds.github.io/inemaseo-metodo/guia/en/**

## The 10 steps

1. **Real audit:** the HTML the server delivers (canonical, hreflang, JSON-LD, internal links).
2. **Technical foundation:** a single canonical, sitemaps with language, robots letting the AIs in, `llms.txt`, content manifest, `noindex` on thin pages.
3. **Brand-free measurement:** weekly Search Console export separating searches for your own name.
4. **Entity:** `Person` + `Organization` with a fixed `@id` on every page and subdomain.
5. **One territory per site:** evergreen, news and events in different places; one owner page per intent.
6. **Original content:** pillars, question pages with a direct answer, fact sheets with extracted and validated data.
7. **Hubs and internal links:** a ladder of links, hub pages that read the other sites' manifests.
8. **Backlinks:** each satellite links to the right page on the main site.
9. **News with its own page:** `NewsArticle`, permanent archive, minimal body with facts from the source only.
10. **Notify and follow up:** IndexNow + Bing on every publish, weekly review, monthly test on the AIs.

Details, keyword score and plan B: [docs/METODO.md](docs/METODO.md) (in Portuguese) ·
publishing checklist: [docs/CHECKLIST.md](docs/CHECKLIST.md) (in Portuguese).

## Tools

| File | What it does |
|---|---|
| `tools/auditoria.sh` | technical SEO X-ray of a site (read-only) |
| `tools/gsc_semanal.py` | weekly Search Console export separating the brand |
| `tools/gsc_inspecionar.py` | indexing status of each URL (URL Inspection API) |
| `tools/avisar_buscadores.sh` | IndexNow + Bing Webmaster, only with URLs that return 200 |
| `tools/link_de_volta.py` | backlinks from satellites to the main site, in batch, with dry run |
| `tools/validar_extracao.mjs` | anti-invention lock for LLM-generated text |
| `templates/` | `robots.txt`, `llms.txt`, `content-index.json`, entity and news JSON-LD, prompts |

Nothing here contains a key, ID or site data: everything comes in through environment variables or arguments.

## Related projects

- [WebMCP Readiness](https://webmcp.inema.pro/): test whether your site is ready for AI agents.
- [WebMCP Training](https://inematds.github.io/webmcp-1-formacao/): five courses, from zero to expert.
- [AIV 2026 — AI Visibility](https://inematds.github.io/aiv2026/guia/): AEO/GEO playbook.
- [WebMCP at INEMA Events](https://eventos.inema.pro/webmcp/)
- [claude-seo](https://github.com/inematds/claude-seo): SEO analysis skill for Claude Code.
- [Learn AI at INEMA.CLUB](https://www.inema.club/aprender-inteligencia-artificial/)

---

MIT License · [INEMA.CLUB](https://inema.club)
