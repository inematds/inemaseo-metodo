#!/usr/bin/env bash
# auditoria.sh — raio-x de SEO técnico de um site, só leitura (passo 1 do método inemaSEO).
# Confere: redirecionamento www/sem www, robots.txt, sitemaps (quantas URLs, quantas com hreflang),
# llms.txt, e para cada página: status, <title>, canonical, hreflang, meta robots, JSON-LD (@type) e
# quantos links internos ela tem no HTML que o servidor entrega (o que o buscador vê sem rodar JS).
#
# Uso: tools/auditoria.sh https://www.seusite.com [/pagina-1/ /pagina-2/ ...]
set -uo pipefail
SITE=${1:?uso: auditoria.sh https://www.seusite.com [/caminho ...]}; shift
SITE=${SITE%/}
HOST=$(echo "$SITE" | sed -E 's#https?://##')
C="curl -4 -m 20 -s"

echo "== Redirecionamentos"
for u in "http://$HOST/" "https://${HOST#www.}/" "https://www.${HOST#www.}/"; do
  echo "  $u -> $($C -o /dev/null -w '%{http_code} %{redirect_url}' "$u")"
done

echo "== robots.txt"
$C "$SITE/robots.txt" | sed 's/^/  /'

echo "== Sitemaps"
for sm in $($C "$SITE/robots.txt" | grep -i '^sitemap:' | awk '{print $2}' | tr -d '\r'); do
  x=$($C "$sm")
  echo "  $sm: $(echo "$x" | grep -c '<loc>') URLs, $(echo "$x" | grep -c 'hreflang') anotações hreflang"
done

echo "== llms.txt: $($C -o /dev/null -w '%{http_code}' "$SITE/llms.txt")"

echo "== Páginas"
for p in / "$@"; do
  h=$($C "$SITE$p")
  echo "-- $p  [$($C -o /dev/null -w '%{http_code}' "$SITE$p")]"
  echo "   title:     $(echo "$h" | grep -oE '<title>[^<]*' | head -1 | sed 's/<title>//')"
  echo "   canonical: $(echo "$h" | grep -oE 'rel="canonical" href="[^"]*"' | head -1 | sed -E 's/.*href="//; s/"$//')"
  echo "   hreflang:  $(echo "$h" | grep -oiE 'hreflang="[^"]*"' | sort -u | tr '\n' ' ')"
  echo "   robots:    $(echo "$h" | grep -oE '<meta name="robots" content="[^"]*"' | sed -E 's/.*content="//; s/"$//')"
  echo "   JSON-LD:   $(echo "$h" | grep -oE '"@type":"[A-Za-z]+"' | sort | uniq -c | tr -s ' ' | tr '\n' ' ')"
  echo "   links internos no HTML: $(echo "$h" | grep -oE "href=\"(/|$SITE/)[^\"#]*\"" | sort -u | wc -l)"
done
