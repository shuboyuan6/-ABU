import urllib.request, urllib.error, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

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
        print(f'HTTP {e.code}: {err[:200]}')
        raise

for f in FILES:
    with open(f['local'], 'r', encoding='utf-8') as fh:
        content = fh.read()
    # Check if file exists
    existing_sha = None
    try:
        existing = api(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{f["path"]}?ref={BRANCH}')
        existing_sha = existing.get('sha')
    except:
        pass
    print(f"文件: {f['path']} | 状态: {'更新' if existing_sha else '新建'}")
    # Create/update file
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
    print(f"  -> {result.get('content',{}).get('path', result.get('path', 'ok'))}")

print('\nGitee 全部完成')
