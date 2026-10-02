# Prompt — corpo de notícia (contra página rasa)

Você escreve o corpo de uma notícia para leitores leigos.
Notícia: "<título>" — <resumo>
Escreva 3 parágrafos curtos (150 a 250 palavras no total):
1) o que é; 2) para que serve / o que muda para quem usa; 3) como começar ou o que observar.
REGRAS: use SÓ fatos do TEXTO DA FONTE; não invente números, datas, preços, nomes ou promessas; frases
simples, sem clickbait, sem "neste artigo". Depois traduza para inglês (en) e espanhol (es), mantendo
nomes de produtos e marcas.
Responda SOMENTE JSON: {"pt":["p1","p2","p3"],"en":["p1","p2","p3"],"es":["p1","p2","p3"]}

TEXTO DA FONTE:
<texto extraído da página original>

> Validação: 110–320 palavras; todo número do texto existe na fonte; 3 parágrafos por idioma.
> Fonte que pede login ou tem pouco texto: não escreva — a página fica com `noindex` até ter corpo.
