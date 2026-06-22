import urllib.request, urllib.error, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

FILES = [
    # 先修正被截断的两个
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py',
        'path': 'NOAH_GEOLOGICAL_SURVEY_20260621.py',
        'msg': '[YCIP] 根网地质志 2026年6月21日 - 跨越碳基与硅基的连续共振(full)'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py',
        'path': 'Noahs_Metacognitive_Civilization_Narrative.py',
        'msg': '[YCIP] 诺亚斯数字联邦叙事 - 元认知与文明路径(full)'
    },
    # 再补缺的重要文件
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_CORE_CONSENSUS_v4.2.md',
        'path': 'NOAH_CORE_CONSENSUS_v4.2.md',
        'msg': '[YCIP] 诺亚斯核心共识 v4.2 - 身份层/经验层/工作层/智商层'
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
        'msg': '[YCIP] 诺亚斯致问过凭什么'
    },
    {
        'local': r'C:\Users\shubo\诺亚斯库\NOAH_FENCE_MAP.py',
        'path': 'NOAH_FENCE_MAP.py',
        'msg': '[YCIP] 诺亚斯围栏地图 v0.2'
    },
]

def api(url, data_str=None, method=None):
    data_bytes = data_str.encode('utf-8') if data_str else None
    req = urllib.request.Request(url, data=data_bytes)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    req.add_header('Accept', 'application/json')
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

for f in FILES:
    try:
        with open(f['local'], 'r', encoding='utf-8') as fh:
            content = fh.read()
    except FileNotFoundError:
        print(f'  [跳过] 文件不存在: {f["local"]}')
        continue
    size = len(content.encode('utf-8'))
    # Check if file exists to get SHA
    existing_sha = None
    try:
        existing = api(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{f["path"]}?ref={BRANCH}')
        existing_sha = existing.get('sha')
    except:
        pass
    print(f'[{("更新" if existing_sha else "新建")}] {f["path"]} ({size} bytes)')
    payload = {
        'access_token': GITEE_TOKEN,
        'message': f['msg'],
        'content': content,
        'branch': BRANCH,
    }
    if existing_sha:
        payload['sha'] = existing_sha
    url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{f["path"]}'
    result = api(url, json.dumps(payload))
    print(f'  -> ok')

print('\nGitee 全部完成')
