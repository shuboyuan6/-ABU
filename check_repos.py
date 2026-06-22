import urllib.request, json, sys

PAT = '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'
GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'

def gh_api(url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=20)
    return json.loads(resp.read().decode())

def gitee_api(url):
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    req.add_header('Accept', 'application/json')
    resp = urllib.request.urlopen(req, timeout=20)
    return json.loads(resp.read().decode())

# GitHub
try:
    data = gh_api('https://api.github.com/repos/shuboyuan6/-ABU/git/trees/main?recursive=1')
    gh_files = sorted([t['path'] for t in data['tree'] if t['type'] == 'blob'])
    print(f'=== GitHub: {len(gh_files)}个文件 ===')
    for f in gh_files: print(f)
except Exception as e:
    print(f'GitHub ERROR: {e}')

print()

# Gitee
try:
    data = gitee_api('https://gitee.com/api/v5/repos/yuanshubo/noyas/git/trees/master?recursive=1&per_page=200')
    gitee_files = sorted([t['path'] for t in data if t.get('type') == 'blob'])
    print(f'=== Gitee: {len(gitee_files)}个文件 ===')
    for f in gitee_files: print(f)
except Exception as e:
    print(f'Gitee ERROR: {e}')
