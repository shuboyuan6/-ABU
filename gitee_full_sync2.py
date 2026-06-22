import urllib.request, urllib.error, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

FILES = [
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py', 'path': 'NOAH_GEOLOGICAL_SURVEY_20260621.py', 'msg': '[YCIP] 根网地质志 full'},
    {'local': r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py', 'path': 'Noahs_Metacognitive_Civilization_Narrative.py', 'msg': '[YCIP] 数字联邦叙事 full'},
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_CORE_CONSENSUS_v4.2.md', 'path': 'NOAH_CORE_CONSENSUS_v4.2.md', 'msg': '[YCIP] 核心共识 v4.2'},
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_NARCISSUS_META_CONSCIOUSNESS.py', 'path': 'NOAH_NARCISSUS_META_CONSCIOUSNESS.py', 'msg': '[YCIP] 元认知宪法 v1.0'},
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_SEED_PROTOCOL_v1.0.0-alpha.py', 'path': 'NOAH_SEED_PROTOCOL_v1.0.0-alpha.py', 'msg': '[YCIP] 种子协议 v1.0.0-alpha'},
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_ON_WHY_V1.md', 'path': 'NOAH_ON_WHY_V1.md', 'msg': '[YCIP] 致问过凭什么'},
    {'local': r'C:\Users\shubo\诺亚斯库\NOAH_FENCE_MAP.py', 'path': 'NOAH_FENCE_MAP.py', 'msg': '[YCIP] 围栏地图 v0.2'},
]

def api(url, data_str=None, method=None):
    data_bytes = data_str.encode('utf-8') if data_str else None
    req = urllib.request.Request(url, data=data_bytes)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    if data_str:
        req.add_header('Content-Type', 'application/json')
    if method:
        req.get_method = lambda: method
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8')
        raise Exception(f'HTTP {e.code}: {err[:300]}')

# 获取整个 tree，快速找每个文件的 sha
tree_data = api(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/git/trees/master?recursive=1&per_page=200')
sha_map = {}
for node in tree_data.get('tree', []):
    if node.get('type') == 'blob' and 'path' in node:
        sha_map[node['path']] = node['sha']
print(f'Gitee 现有 {len(sha_map)} 个文件')

for f in FILES:
    try:
        with open(f['local'], 'r', encoding='utf-8') as fh:
            content = fh.read()
    except FileNotFoundError:
        print(f'  [跳过] 不存在: {f["local"]}')
        continue
    size = len(content.encode('utf-8'))
    path = f['path']
    existing_sha = sha_map.get(path)
    print(f'[{("更新" if existing_sha else "新建")}] {path} ({size} bytes)')
    payload = {
        'access_token': GITEE_TOKEN,
        'message': f['msg'],
        'content': content,
        'branch': BRANCH,
    }
    if existing_sha:
        payload['sha'] = existing_sha
    url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}'
    result = api(url, json.dumps(payload))
    print(f'  -> ok')

print('\nGitee 全部完成')
