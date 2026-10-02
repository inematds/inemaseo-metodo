// validar_extracao.mjs — a trava anti-invenção que usamos sempre que um LLM escreve conteúdo a partir
// de uma página fonte (ementa de curso, corpo de notícia, FAQ). O LLM pode reescrever, mas não inventar:
//   1. título/módulo citado tem que existir na fonte;
//   2. frase precisa reusar a maior parte das palavras da fonte (limiar ajustável);
//   3. todo número (horas, aulas, preços, datas) tem que aparecer na fonte.
// Item que falha é descartado (não "consertado"): melhor uma ficha menor do que uma ficha mentirosa.
//
// Uso como biblioteca:
//   import { normaliza, apoiada, numerosNaFonte, tituloNaFonte } from './validar_extracao.mjs'
// Uso pela linha de comando (teste rápido):
//   node tools/validar_extracao.mjs fonte.txt "frase gerada pelo LLM"

const STOP = new Set('a o e de da do das dos em no na nos nas um uma para por com como que se ao aos à às seu sua seus suas é the and of to in'.split(' '))

export const normaliza = (s) => s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim()

/** Fração das palavras "de conteúdo" da frase que existem na fonte >= limiar. */
export function apoiada(frase, fonte, limiar = 0.7) {
  const palavrasFonte = new Set(normaliza(fonte).split(' '))
  const ws = normaliza(frase).split(' ').filter((w) => w.length > 2 && !STOP.has(w))
  if (!ws.length) return false
  return ws.filter((w) => palavrasFonte.has(w)).length / ws.length >= limiar
}

/** Todos os números da frase aparecem na fonte (ignora separador de milhar/decimal). */
export function numerosNaFonte(frase, fonte) {
  const f = normaliza(fonte).replace(/ (?=\d)/g, '')
  return (frase.match(/\d+(?:[.,]\d+)*/g) || []).map((n) => n.replace(/[.,]/g, '')).every((n) => f.includes(n))
}

/** O título (de módulo, trilha, aula) existe literalmente na fonte. */
export const tituloNaFonte = (titulo, fonte) => normaliza(titulo).length >= 3 && normaliza(fonte).includes(normaliza(titulo))

if (import.meta.url === `file://${process.argv[1]}`) {
  const fs = await import('node:fs')
  const [arq, frase] = process.argv.slice(2)
  if (!arq || !frase) { console.log('uso: node tools/validar_extracao.mjs fonte.txt "frase"'); process.exit(1) }
  const fonte = fs.readFileSync(arq, 'utf8')
  console.log({ apoiada: apoiada(frase, fonte), numerosNaFonte: numerosNaFonte(frase, fonte), tituloNaFonte: tituloNaFonte(frase, fonte) })
}
