# 🔎 inemaSEO — seu site em destaque

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![inemaSEO — seu site em destaque](guia/assets/banner.jpg)](https://inematds.github.io/inemaseo-metodo/guia/)

O método que usamos no ecossistema INEMA para ser encontrado no **Google**, no **Bing** e nas respostas
das **IAs** (ChatGPT, Perplexity, Copilot, AI Overviews), sem ferramenta paga e sem conteúdo inventado.
Agentes de IA fazem o trabalho repetitivo; o humano decide.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/inemaseo-metodo/guia/**

## As 10 etapas

1. **Auditoria real:** o HTML que o servidor entrega (canônico, hreflang, JSON-LD, links internos).
2. **Fundação técnica:** canônico único, sitemaps com idioma, robots liberando as IAs, `llms.txt`, manifesto de conteúdo, `noindex` em página rasa.
3. **Medição sem a marca:** Search Console semanal separando as buscas pelo seu nome.
4. **Entidade:** `Person` + `Organization` com `@id` fixo em todas as páginas e subdomínios.
5. **Um território por site:** evergreen, notícia e evento em lugares diferentes; uma página dona por intenção.
6. **Conteúdo próprio:** pilares, páginas de pergunta com resposta direta, fichas com dado extraído e validado.
7. **Hubs e links internos:** escada de links, páginas-hub que leem o manifesto dos outros sites.
8. **Links de volta:** cada satélite linka a página certa do site principal.
9. **Notícias com página própria:** `NewsArticle`, arquivo permanente, corpo mínimo só com fatos da fonte.
10. **Avisar e acompanhar:** IndexNow + Bing a cada publicação, leitura semanal, teste mensal nas IAs.

Detalhes, score de palavra-chave e plano B: [docs/METODO.md](docs/METODO.md) ·
checklist de publicação: [docs/CHECKLIST.md](docs/CHECKLIST.md).

## Ferramentas

| Arquivo | O que faz |
|---|---|
| `tools/auditoria.sh` | raio-x de SEO técnico de um site (só leitura) |
| `tools/gsc_semanal.py` | export semanal do Search Console separando a marca |
| `tools/gsc_inspecionar.py` | estado de indexação de cada URL (URL Inspection API) |
| `tools/avisar_buscadores.sh` | IndexNow + Bing Webmaster, só com URLs que respondem 200 |
| `tools/link_de_volta.py` | link de volta dos satélites para o site principal, em lote, com dry-run |
| `tools/validar_extracao.mjs` | trava anti-invenção para texto gerado por LLM |
| `templates/` | `robots.txt`, `llms.txt`, `content-index.json`, JSON-LD de entidade e de notícia, prompts |

Nada aqui tem chave, ID ou dado de site: tudo entra por variável de ambiente ou argumento.

## Projetos relacionados

- [WebMCP Readiness](https://webmcp.inema.pro/): teste se o seu site está pronto para agentes de IA.
- [Formação WebMCP](https://inematds.github.io/webmcp-1-formacao/): cinco cursos, do zero ao expert.
- [AIV 2026 — AI Visibility](https://inematds.github.io/aiv2026/guia/): playbook de AEO/GEO.
- [WebMCP no Eventos INEMA](https://eventos.inema.pro/webmcp/)
- [claude-seo](https://github.com/inematds/claude-seo): skill de análise de SEO para o Claude Code.
- [Aprender IA no INEMA.CLUB](https://www.inema.club/aprender-inteligencia-artificial/)

---

Licença MIT · [INEMA.CLUB](https://inema.club)
