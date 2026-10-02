# Prompt — ficha extrativa (ementa a partir da página real)

Você extrai a ementa de um curso a partir do TEXTO DA PÁGINA dele. Regras:
- EXTRATIVO: copie títulos de módulos/trilhas exatamente como aparecem (pode remover emoji). Frases de
  "público", "aprende" e "constrói" devem reusar as palavras da página; não invente nada.
- Não inclua preço, gratuidade, promoções, depoimentos ou números de alunos.
- Se um campo não estiver na página, use [] ou null.
Responda SOMENTE JSON: {"estrutura":[{"titulo":"","detalhe":""}],"aprende":[""],"publico":[""],
"constroi":[""],"pre_requisitos":[""],"carga_horaria":null,"nivel":null}
Limites: estrutura até 12 itens — só trilhas/módulos/aulas do conteúdo, nunca seções da página
("Para quem é", "FAQ", "Comece agora").

> Depois, passe cada item pelo `tools/validar_extracao.mjs`. Ficha com menos de 3 módulos válidos não é
> publicada como "enriquecida".
