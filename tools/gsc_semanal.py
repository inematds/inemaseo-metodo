#!/usr/bin/env python3
"""gsc_semanal.py — export semanal do Google Search Console SEPARANDO A MARCA (passo de medição do inemaSEO).

Por que separar: no começo quase todo clique vem de quem já procura o seu nome. O número que mostra se o
SEO está funcionando é o de consultas SEM a marca (gente que não te conhecia e te achou).

Autenticação: Application Default Credentials do gcloud, com o escopo do Search Console:
    gcloud auth application-default login \
      --scopes=https://www.googleapis.com/auth/webmasters.readonly,https://www.googleapis.com/auth/cloud-platform
Variáveis:
    GSC_SITES      propriedades, separadas por vírgula (ex.: "sc-domain:seusite.com,sc-domain:outro.com")
    GSC_MARCA      regex da marca (ex.: "seusite|seu nome|erro comum de digitação")
    GSC_QUOTA_PROJ projeto do Google Cloud que paga a cota (header x-goog-user-project)
Uso: python3 tools/gsc_semanal.py [--dias 7] [--saida dados/gsc]
Saída: <fim>_<site>_sem-marca.csv (query, page, cliques, impressões, ctr, posição) e resumo.csv (1 linha/semana/site).
"""
import csv, datetime, json, os, pathlib, re, subprocess, sys, urllib.parse, urllib.request

SITES = [s.strip() for s in os.environ.get('GSC_SITES', '').split(',') if s.strip()]
MARCA = re.compile(os.environ.get('GSC_MARCA', r'^$'), re.I)
PROJ = os.environ.get('GSC_QUOTA_PROJ', '')
if not SITES or not PROJ:
    sys.exit('defina GSC_SITES, GSC_MARCA e GSC_QUOTA_PROJ (ver o cabeçalho do script)')
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
DIAS = int(arg('--dias', 7))
OUT = pathlib.Path(arg('--saida', 'dados/gsc'))
B = 'https://www.googleapis.com/webmasters/v3/sites/'
TOK = subprocess.run(['gcloud', 'auth', 'application-default', 'print-access-token'],
                     capture_output=True, text=True).stdout.strip()


def query(site, body):
    r = urllib.request.Request(B + urllib.parse.quote(site, safe='') + '/searchAnalytics/query', method='POST',
                               data=json.dumps(body).encode(),
                               headers={'Authorization': 'Bearer ' + TOK, 'Content-Type': 'application/json',
                                        'x-goog-user-project': PROJ})
    return json.load(urllib.request.urlopen(r, timeout=60)).get('rows', [])


fim = datetime.date.today() - datetime.timedelta(days=2)  # o GSC atrasa ~2 dias
ini = fim - datetime.timedelta(days=DIAS - 1)
OUT.mkdir(parents=True, exist_ok=True)
resumo = OUT / 'resumo.csv'
novo = not resumo.exists() or resumo.stat().st_size == 0
CAMPOS = ['total_cliques', 'total_impr', 'marca_cliques', 'marca_impr', 'sem_marca_cliques', 'sem_marca_impr',
          'anonimas_cliques', 'anonimas_impr', 'consultas_sem_marca']
with open(resumo, 'a', newline='') as fr:
    wr = csv.writer(fr)
    if novo:
        wr.writerow(['inicio', 'fim', 'site', *CAMPOS])
    for site in SITES:
        base = {'startDate': str(ini), 'endDate': str(fim)}
        tot = (query(site, base) or [{'clicks': 0, 'impressions': 0}])[0]
        rows, start = [], 0
        while True:
            page = query(site, {**base, 'dimensions': ['query', 'page'], 'rowLimit': 25000, 'startRow': start})
            rows += page
            if len(page) < 25000:
                break
            start += 25000
        # Some pela dimensão "query" sozinha: com query+page a mesma busca conta uma vez por página.
        qs = query(site, {**base, 'dimensions': ['query'], 'rowLimit': 25000})
        marca = [r for r in qs if MARCA.search(r['keys'][0])]
        sem_q = [r for r in qs if not MARCA.search(r['keys'][0])]
        sem = [r for r in rows if not MARCA.search(r['keys'][0])]
        s = lambda rs, k: round(sum(r[k] for r in rs))
        nome = site.split(':')[-1].strip('/').replace('https://', '').replace('/', '_')
        with open(OUT / f'{fim}_{nome}_sem-marca.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['query', 'page', 'clicks', 'impressions', 'ctr', 'position'])
            for r in sorted(sem, key=lambda r: -r['impressions']):
                w.writerow([r['keys'][0], r['keys'][1], int(r['clicks']), int(r['impressions']),
                            round(r['ctr'], 4), round(r['position'], 1)])
        # "Anônimas": o Google esconde consultas raras quando a dimensão é query; é o que sobra do total.
        linha = [round(tot['clicks']), round(tot['impressions']), s(marca, 'clicks'), s(marca, 'impressions'),
                 s(sem_q, 'clicks'), s(sem_q, 'impressions'),
                 round(tot['clicks']) - s(marca, 'clicks') - s(sem_q, 'clicks'),
                 round(tot['impressions']) - s(marca, 'impressions') - s(sem_q, 'impressions'), len(sem_q)]
        wr.writerow([ini, fim, nome, *linha])
        print(nome, f'{ini}..{fim}', dict(zip(CAMPOS, linha)))
