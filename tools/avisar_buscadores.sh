#!/usr/bin/env bash
# avisar_buscadores.sh — avisa o Bing (Webmaster API) e o IndexNow (Bing, Yandex, Seznam, Naver...)
# que estas URLs são novas ou mudaram. Rode depois de cada publicação.
#
# Antes de usar:
#  - IndexNow: crie uma chave (32+ caracteres hex) e publique-a em https://<host>/<chave>.txt
#    contendo só a chave. Não é segredo: é pública por design.
#  - Bing Webmaster (opcional): bing.com/webmasters -> Settings -> API access -> gere a chave e exporte
#    BING_API_KEY. O site precisa estar verificado nessa conta. Cota típica: 10 mil URLs/dia.
#
# Uso: INDEXNOW_KEY=<chave> [BING_API_KEY=<chave>] [BING_SITE=https://seusite.com/] \
#      tools/avisar_buscadores.sh urls.txt          (uma URL por linha, todas do mesmo host)
set -euo pipefail
LIST=${1:?arquivo com uma URL por linha}
HOST=$(head -1 "$LIST" | sed -E 's#https?://([^/]+).*#\1#')
# Confere antes: só avisa URL que responde 200 (avisar 404 queima a confiança do buscador).
ruins=0
while read -r u; do
  [ -z "$u" ] && continue
  c=$(curl -4 -m 20 -s -o /dev/null -w '%{http_code}' "$u"); [ "$c" = 200 ] || { echo "NÃO 200 ($c): $u"; ruins=$((ruins+1)); }
done < "$LIST"
[ "$ruins" = 0 ] || { echo "corrija as URLs acima antes de avisar"; exit 1; }

json_list() { python3 -c 'import json,sys; print(json.dumps([l.strip() for l in open(sys.argv[1]) if l.strip()]))' "$LIST"; }

if [ -n "${INDEXNOW_KEY:-}" ]; then
  curl -4 -m 60 -s -o /dev/null -w "IndexNow: HTTP %{http_code}\n" -H 'Content-Type: application/json; charset=utf-8' \
    -X POST https://api.indexnow.org/indexnow \
    -d "{\"host\":\"$HOST\",\"key\":\"$INDEXNOW_KEY\",\"keyLocation\":\"https://$HOST/$INDEXNOW_KEY.txt\",\"urlList\":$(json_list)}"
fi
if [ -n "${BING_API_KEY:-}" ]; then
  curl -4 -m 60 -s -o /dev/null -w "Bing SubmitUrlBatch: HTTP %{http_code}\n" -H 'Content-Type: application/json; charset=utf-8' \
    -X POST "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey=$BING_API_KEY" \
    -d "{\"siteUrl\":\"${BING_SITE:-https://$HOST/}\",\"urlList\":$(json_list)}"
fi
