#!/usr/bin/env python3
"""link_de_volta.py — põe, em lote, um link de volta dos seus sites satélites para a página certa do site
principal (ex.: cada curso no GitHub Pages -> a ficha dele no site). Autoridade que você já tem, sem pedir
link pra ninguém.

Regras de segurança (as mesmas que usamos):
  - Dry-run por padrão: só mostra o que faria. --apply grava; --commit também commita e faz push.
  - Pula repo com alterações não commitadas, repo fora da branch esperada e repo sem HTML.
  - Marcador no bloco (<!-- link-de-volta:v1 -->): rodar de novo não duplica.
  - Se o index.html for só um <meta refresh> (comum em sites gerados), o link vai na página de destino.

Mapa (JSON): [{"repo": "/caminho/do/repo", "destino": "https://www.seusite.com/cursos/x/", "rotulo": "Ficha completa"}]
Uso: python3 tools/link_de_volta.py mapa.json [--apply] [--commit] [--guia URL --guia-rotulo TEXTO] [--branch main]
"""
import json, pathlib, re, subprocess, sys

MARK = 'link-de-volta:v1'
args = sys.argv[1:]
if not args:
    sys.exit(__doc__)
opt = lambda k, d=None: args[args.index(k) + 1] if k in args else d
APPLY, COMMIT = '--apply' in args, '--commit' in args
GUIA, GUIA_ROT = opt('--guia'), opt('--guia-rotulo', 'Guia')
BRANCH = opt('--branch', 'main')


def git(repo, *a, check=True):
    return subprocess.run(['git', '-C', str(repo), *a], capture_output=True, text=True, check=check).stdout.strip()


def bloco(item):
    a = 'style="color:inherit;text-decoration:underline"'
    extra = f' · <a href="{GUIA}" {a}>{GUIA_ROT}</a>' if GUIA else ''
    return (f'\n<!-- {MARK} -->\n<p style="text-align:center;font-size:.85rem;margin:.75rem 0 0;opacity:.85">'
            f'<a href="{item["destino"]}" {a}>{item.get("rotulo", "Saiba mais")}</a>{extra}</p>\n<!-- /{MARK} -->\n')


def processa(item):
    repo = pathlib.Path(item['repo']).expanduser()
    if git(repo, 'status', '--porcelain', '--untracked-files=no'):
        return 'PULA: alterações não commitadas'
    if git(repo, 'rev-parse', '--abbrev-ref', 'HEAD') != BRANCH:
        return f'PULA: fora da branch {BRANCH}'
    alvo = repo / 'index.html'
    if not alvo.exists():
        return 'PULA: sem index.html'
    html = alvo.read_text(encoding='utf-8')
    m = len(html) < 2000 and re.search(r'http-equiv=["\']refresh["\'][^>]*url=([^"\'>\s]+)', html, re.I)
    if m and (repo / m.group(1)).is_file():
        alvo = repo / m.group(1)
        html = alvo.read_text(encoding='utf-8')
    if MARK in html:
        return 'OK: já tinha'
    i = html.rfind('</footer>')
    if i < 0:
        i = html.rfind('</body>')
    if i < 0:
        return 'PULA: sem </footer> nem </body>'
    if not APPLY:
        return f'DRY: entraria em {alvo.name}'
    alvo.write_text(html[:i] + bloco(item) + html[i:], encoding='utf-8')
    if COMMIT:
        git(repo, 'add', alvo.name)
        git(repo, 'commit', '-q', '-m', 'seo: link de volta para o site principal')
        p = subprocess.run(['git', '-C', str(repo), 'push', '-q'], capture_output=True, text=True)
        return f'APLICADO em {alvo.name}, push ' + ('ok' if p.returncode == 0 else 'FALHOU')
    return f'APLICADO em {alvo.name}'


for item in json.load(open(args[0])):
    try:
        print(f"{item['repo']}: {processa(item)}")
    except Exception as e:
        print(f"{item['repo']}: ERRO {e}")
