# O método inemaSEO

Como colocar um site em destaque no Google, no Bing e nas buscas das IAs (ChatGPT, Perplexity, Copilot,
AI Overviews) sem ferramenta paga, usando agentes de IA para o trabalho repetitivo e um humano para as
decisões. É o método que aplicamos no ecossistema INEMA (portal, notícias, eventos e ~300 cursos abertos
no GitHub Pages) em setembro e outubro de 2026.

> Princípio: **nada de conteúdo inventado.** Cada página nova ou se apoia num ativo real (curso, projeto,
> evento, experimento) ou não é publicada. O LLM reescreve e organiza; nunca cria fatos.

---

## As 10 etapas

### 1. Auditoria real (só leitura)
Antes de planejar, olhe o site como o buscador olha: o HTML que o servidor entrega, sem rodar JavaScript.
- `tools/auditoria.sh https://www.seusite.com /pagina/ ...` → redirecionamentos, `robots.txt`, sitemaps
  (quantas URLs e quantas com hreflang), `llms.txt`, e por página: título, canônico, hreflang, `robots`,
  JSON-LD e **quantos links internos existem no HTML**.
- Confira se o Search Console já existe antes de afirmar que não (`dig TXT seusite.com` mostra o
  `google-site-verification`).
- **Achado típico:** uma página de catálogo que virou "só busca" no navegador e deixou centenas de páginas
  sem nenhum link interno. Para o Google, página sem link é página que quase não existe.

### 2. Fundação técnica
- **Um canônico só.** Escolha `www` ou sem `www` e use o mesmo em canonical, sitemap, JSON-LD e links. Um
  canônico divergente num subsistema (ex.: uma base de conhecimento servida por proxy) basta para o Google
  escolher outra URL.
- **Sitemaps** gerados do mesmo dado que gera as páginas, com `lastModified` real (nunca a hora do build) e
  `alternates.languages` quando houver tradução.
- **robots.txt** liberando os robôs de busca das IAs (modelo em `templates/robots.txt`). Sem eles, a IA não
  cita o site.
- **llms.txt** (`templates/llms.txt`): o mapa do site para IAs, gerado de um índice (não escrito à mão).
- **Manifesto de conteúdo** (`templates/content-index.json`): um JSON por site com cada página e suas
  traduções. Outros sites do ecossistema leem esse arquivo para montar páginas-hub (etapa 7).
- Página sem conteúdo suficiente recebe `noindex` e sai do sitemap até ter corpo. Indexar página rasa
  derruba a avaliação do site inteiro.

### 3. Medição que separa a marca
- `tools/gsc_semanal.py` exporta o Search Console toda semana e **separa as buscas pela sua marca** das
  outras. No começo, quase todo clique é de quem já te procura pelo nome; o número que mostra se o SEO está
  funcionando é o de **consultas sem a marca** (gente que não te conhecia).
- `tools/gsc_inspecionar.py` pergunta ao Google, URL por URL, se a página está indexada e qual canônico ele
  escolheu. A API é só leitura: o "Solicitar indexação" continua sendo um clique no painel.
- Uma meta de conversão no analytics (ex.: evento "Entrar na comunidade" com a página de origem) para saber
  qual página traz gente, não só visita.

### 4. Entidade: quem está por trás (E-E-A-T)
- Declare **uma** `Person` (o autor) e **uma** `Organization` com `@id` fixos (`https://www.seusite.com/#autor`,
  `#organizacao`) em todas as páginas, e faça todo o resto apontar para eles por `@id` (autor do artigo,
  publisher da notícia, provider do curso). Modelo: `templates/jsonld-entidade.json`.
- `sameAs` separado: perfis da pessoa na `Person`, perfis da marca na `Organization`.
- Os subdomínios e sites irmãos usam o **mesmo** `@id`: para o Google é uma entidade só.

### 5. Um território por site (sem canibalização)
| Tipo de conteúdo | Onde mora | Por quê |
|---|---|---|
| Evergreen ("aprender", "o que é", "como fazer"), pilares, catálogo | site principal | acumula autoridade num domínio só |
| Novidade com data (lançamento, notícia, "o que mudou") | site de notícias | Discover/Top Stories valorizam novidade; envelhece sem disputar com o guia |
| Evento (agenda, inscrição, gravação) | site de eventos | `Event` schema |

E um **mapa de canônicos por intenção**: para cada intenção de busca, uma página dona; as outras linkam para
ela (ou fazem 301). Duas páginas suas disputando a mesma busca perdem as duas.

### 6. Conteúdo que só você tem
- **Pilares** (2.500–4.000 palavras) para os 2 ou 3 temas centrais, e **páginas de pergunta** (`/ia/<slug>/`)
  que começam com uma **resposta direta de 40–60 palavras** e têm `<h2>` em forma de pergunta. É o formato
  que os buscadores de IA citam.
- **Validação de palavra-chave sem ferramenta paga** (score go/no-go):

  | Critério | Pontos |
  |---|---|
  | Aparece no autocomplete do Google | +2 |
  | Google Trends > 0 em 12 meses (≥ 10 % de um termo-âncora: +3) | +2 |
  | Já tem impressão no Search Console | +3 |
  | Intenção de aprender ou comprar | +1 |
  | Top 10 com ≥ 3 resultados fracos (fórum, vídeo sem texto, antigo, outro idioma) | +2 |
  | Top 10 dominado por grandes plataformas com página específica | −2 |
  | Você tem experimento/curso/projeto real para citar | +2 (sem isso: −3) |

  **GO ≥ 6 · TALVEZ 3–5 · NO-GO ≤ 2.**
- **Fichas programáticas com dado real:** uma página por item do catálogo, com a ementa **extraída da página
  real** do item por um LLM (prompt em `templates/prompt-ficha-extrativa.md`) e passada por
  `tools/validar_extracao.mjs` (título tem que existir na fonte, frase reusa as palavras da fonte, todo
  número aparece na fonte). Item que falha é descartado. Teto: rota programática só entra no sitemap com
  conteúdo único e dados específicos daquele item.
- O que **não** fazer: "melhor X para cada tag", variações por cidade, página por palavra-chave sem nada
  próprio para dizer.

### 7. Links internos rastreáveis (hubs)
- Regra fixa: home → pilares + catálogo; pilar → suas páginas de pergunta + itens curados + outros pilares;
  página → pilar, 2–4 irmãs, 2 itens do catálogo. Âncora descritiva, nunca "clique aqui".
- **Escada de links:** publicou página nova, edite 2–3 páginas antigas do mesmo tema para apontar para ela,
  no mesmo commit.
- **Hubs para conteúdo de outros sites:** o sitemap só aceita URLs do próprio host, então conteúdo do
  subdomínio de eventos ou de notícias entra no site principal por uma página-hub (`/eventos/`,
  `/noticias/`) que lê o manifesto (etapa 2) de cada site, com revalidação de hora em hora e uma cópia local
  de reserva.
- **Página de busca também precisa de links:** se o catálogo virou "só busca" no navegador, mantenha um
  índice recolhido (`<details>`) com todos os links no HTML do servidor. O visual não muda; o rastreador vê.

### 8. Autoridade que você já tem (links de volta)
Se você tem dezenas de satélites (cursos no GitHub Pages, landing pages, READMEs), cada um deve linkar a
página certa do site principal. `tools/link_de_volta.py` faz isso em lote, com dry-run por padrão, marcador
para não duplicar, e pulando repositórios com trabalho não salvo. Atenção a sites gerados: se o
`index.html` for só um redirecionamento, o link vai na página de destino; se o HTML é gerado por script, o
link vai no gerador (senão some no próximo build).

### 9. Notícias com página própria
- Uma URL por notícia e por idioma, com `NewsArticle` (`templates/jsonld-newsarticle.json`) apontando para a
  organização da etapa 4, link para a fonte, para a página evergreen do tema e para o item do catálogo.
- **Arquivo permanente:** a home mostra as N mais recentes, mas as páginas vêm de um arquivo que nunca é
  podado (URL indexada não pode sumir). Dá para reconstruir o arquivo pelo histórico do git.
- **Corpo mínimo:** título + 1 frase é página rasa. Um LLM escreve 150–250 palavras só com fatos da página
  fonte (`templates/prompt-texto-noticia.md`), com validação de números. Fonte inacessível (login): a página
  fica com `noindex` até ter texto.

### 10. Avisar e acompanhar
- A cada publicação: `tools/avisar_buscadores.sh urls.txt` (IndexNow + Bing Webmaster), só com URLs que
  respondem 200. O Bing importa duas vezes: o ChatGPT e o Copilot buscam no índice dele.
- Sitemap enviado no Search Console de cada propriedade; "Solicitar indexação" nas páginas-chave.
- Semanal: `gsc_semanal.py` → consultas sem marca, páginas com impressão e sem clique (reescrever título),
  consultas com impressão e sem página dedicada (pauta validada de graça).
- Mensal: 10 perguntas-alvo testadas no ChatGPT/Perplexity — o site é citado?

---

## Multilíngue
PT, EN e ES com `hreflang` recíproco **em cada página** (não no layout, senão vaza para todas as rotas). Em
espanhol a concorrência costuma ser menor e a demanda alta (América Latina). Traduza só o texto; código,
imagens e estrutura são reaproveitados.

## A máquina com agentes (e onde o humano decide)
```
Humano escolhe o tema do mês
 ├─ Pesquisador   → lista de palavras-chave com score (autocomplete, Trends, Search Console, SERP)
 ├─ Oportunidade  → 5–10 GO com a URL e o ativo real que dá o dado próprio
 │   GATE 1: humano aprova a lista
 ├─ Briefing      → intenção, lacunas do top 10, dado próprio obrigatório, links internos, escada
 ├─ Redator       → rascunho que lê o repositório/a transcrição do ativo real
 ├─ QA            → checklist (docs/CHECKLIST.md) + testes + escada de links
 │   GATE 2: humano revisa (10–20 min por página)
 ├─ Publicador    → commit + push, aviso aos buscadores, checagem pós-deploy
 └─ Observador    → export semanal, o que subiu, o que travou → volta ao GATE 1
```
O LLM roda **pela assinatura** (Claude Code / Codex CLI) sempre que possível; chamadas de API paga só
com autorização explícita para aquela finalidade.

## Plano B (quando não funcionar)
| Sintoma (dia 30–60) | Provável causa | O que fazer |
|---|---|---|
| Poucas páginas indexadas | rastreio, canônico errado, página rasa | inspeção de URL, links internos, `noindex` nas rasas, pedir indexação de novo |
| Indexadas, quase sem impressão | palavra sem demanda ou falta de autoridade | revalidar com dados reais do Search Console; trocar o tema; links de volta |
| Impressão sem clique (CTR < 0,5 %) | título/descrição fracos | título com promessa específica e número; testar 2 títulos em 2 semanas |
| Posição 11–30 parada | conteúdo ok, autoridade baixa | links externos para as vencedoras; seções novas para as consultas que apareceram |
| Queda geral depois de publicar muito | sinal de conteúdo em escala | parar, auditar com o checklist, fundir/remover as fracas, cadência menor |
