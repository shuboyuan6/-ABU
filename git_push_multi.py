import urllib.request, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'

FILES = [
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py',
        'path': 'NOAH_GEOLOGICAL_SURVEY_20260621.py',
        'msg': '[YCIP] 根网地质志 2026年6月21日 - 跨越碳基与硅基的连续共振'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py',
        'path': 'Noahs_Metacognitive_Civilization_Narrative.py',
        'msg': '[YCIP] 诺亚斯数字联邦叙事 - 元认知与文明路径'
    },
]

def api(url, data_str=None, method=None):
    data_bytes = data_str.encode('utf-8') if data_str else None
    req = urllib.request.Request(url, data=data_bytes)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    if data_str:
        req.add_header('Content-Type', 'application/json')
    if method:
        req.get_method = lambda: method
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def get_sha(path):
    try:
        return api(f'https://api.github.com/repos/{REPO}/contents/{path}?ref={BRANCH}')['sha']
    except:
        return None

def get_ref():
    return api(f'https://api.github.com/repos/{REPO}/git/ref/heads/{BRANCH}')['object']['sha']

def get_commit(sha):
    return api(f'https://api.github.com/repos/{REPO}/git/commits/{sha}')

for f in FILES:
    with open(f['local'], 'r', encoding='utf-8') as fh:
        content = fh.read()
    sha = get_sha(f['path'])
    print(f"文件: {f['path']} | 状态: {'更新' if sha else '新建'}")
    ref_sha = get_ref()
    commit = get_commit(ref_sha)
    blob = api('https://api.github.com/repos/{}/git/blobs'.format(REPO), json.dumps({'content': content, 'encoding': 'utf-8'}))
    blob_sha = blob['sha']
    tree = api('https://api.github.com/repos/{}/git/trees'.format(REPO), json.dumps({'base_tree': commit['tree']['sha'], 'tree': [{'path': f['path'], 'mode': '100644', 'type': 'blob', 'sha': blob_sha}]}))
    new_commit = api('https://api.github.com/repos/{}/git/commits'.format(REPO), json.dumps({'message': f['msg'], 'tree': tree['sha'], 'parents': [ref_sha]}))
    api('https://api.github.com/repos/{}/git/refs/heads/{}'.format(REPO, BRANCH), json.dumps({'sha': new_commit['sha']}), method='PATCH')
    print(f"  -> 成功! commit={new_commit['sha'][:8]}")

print('\n全部完成')
