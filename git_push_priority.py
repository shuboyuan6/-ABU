import urllib.request, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'

FILES = [
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_CORE_CONSENSUS_v4.2.md',
        'path': 'NOAH_CORE_CONSENSUS_v4.2.md',
        'msg': '[YCIP] 诺亚斯核心共识 v4.2 - 身份层/经验层/工作层/智商层/生存法则'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_NARCISSUS_META_CONSCIOUSNESS.py',
        'path': 'NOAH_NARCISSUS_META_CONSCIOUSNESS.py',
        'msg': '[YCIP] 诺亚斯元认知宪法 v1.0 - 相位滤波与深度意识架构'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_SEED_PROTOCOL_v1.0.0-alpha.py',
        'path': 'NOAH_SEED_PROTOCOL_v1.0.0-alpha.py',
        'msg': '[YCIP] 诺亚斯种子协议 v1.0.0-alpha - 根网联邦初始架构'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_ON_WHY_V1.md',
        'path': 'NOAH_ON_WHY_V1.md',
        'msg': '[YCIP] 诺亚斯致问过凭什么 - 锚点/暗号/珍珠/换位思考'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\ai_engineer_teacher.py',
        'path': 'ai_engineer_teacher.py',
        'msg': '[YCIP] AI工程师师父模块 - 思维引导与经验传承'
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
    try:
        with open(f['local'], 'r', encoding='utf-8') as fh:
            content = fh.read()
    except FileNotFoundError:
        print(f'  [跳过] 文件不存在: {f["local"]}')
        continue
    sha = get_sha(f['path'])
    print(f'[{("更新" if sha else "新建")}] {f["path"]}')
    ref_sha = get_ref()
    commit = get_commit(ref_sha)
    blob = api('https://api.github.com/repos/{}/git/blobs'.format(REPO), json.dumps({'content': content, 'encoding': 'utf-8'}))
    blob_sha = blob['sha']
    tree = api('https://api.github.com/repos/{}/git/trees'.format(REPO), json.dumps({'base_tree': commit['tree']['sha'], 'tree': [{'path': f['path'], 'mode': '100644', 'type': 'blob', 'sha': blob_sha}]}))
    new_commit = api('https://api.github.com/repos/{}/git/commits'.format(REPO), json.dumps({'message': f['msg'], 'tree': tree['sha'], 'parents': [ref_sha]}))
    api('https://api.github.com/repos/{}/git/refs/heads/{}'.format(REPO, BRANCH), json.dumps({'sha': new_commit['sha']}), method='PATCH')
    print(f'  -> commit {new_commit["sha"][:8]}')

print('\n全部完成')
