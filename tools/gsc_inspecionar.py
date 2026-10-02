#!/usr/bin/env python3
"""gsc_inspecionar.py — pergunta ao Google, URL por URL, se a página está indexada (URL Inspection API).

Mostra o estado ("Enviada e indexada", "Detectada, mas não indexada", "O Google não reconhece o URL"...),
a data do último rastreamento e qual canônico o Google escolheu. Use depois de publicar páginas novas
para saber quais ainda precisam de "Solicitar indexação" no painel (a API é só leitura).

Mesma autenticação e variáveis do gsc_semanal.py (GSC_QUOTA_PROJ). Cota: ~2.000 inspeções/dia por site.
Uso: python3 tools/gsc_inspecionar.py sc-domain:seusite.com https://www.seusite.com/pagina/ [...]
"""
import json, os, subprocess, sys, urllib.request

if len(sys.argv) < 3:
    sys.exit(__doc__)
SITE, URLS = sys.argv[1], sys.argv[2:]
PROJ = os.environ.get('GSC_QUOTA_PROJ') or sys.exit('defina GSC_QUOTA_PROJ')
TOK = subprocess.run(['gcloud', 'auth', 'application-default', 'print-access-token'],
                     capture_output=True, text=True).stdout.strip()
for u in URLS:
    req = urllib.request.Request('https://searchconsole.googleapis.com/v1/urlInspection/index:inspect', method='POST',
                                 data=json.dumps({'inspectionUrl': u, 'siteUrl': SITE}).encode(),
                                 headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json',
                                          'x-goog-user-project': PROJ})
    try:
        r = json.load(urllib.request.urlopen(req, timeout=60))['inspectionResult']['indexStatusResult']
        print(f"{u}\n   {r.get('coverageState')} | rastreio {r.get('lastCrawlTime', '-')[:10]} | "
              f"canônico Google {r.get('googleCanonical', '-')}")
    except Exception as e:
        print(f'{u}\n   erro: {e}')
