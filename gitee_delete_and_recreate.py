import urllib.request, urllib.parse, urllib.error, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

def gitee_req(url, data=None, method=None):
    if isinstance(data, str):
        data = data.encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    if data:
        req.add_header('Content-Type', 'application/json')
    if method:
        req.get_method = lambda: method
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()}

FILES = [
    ('NOAH_GEOLOGICAL_SURVEY_20260621.py', r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py', '[YCIP] 根网地质志 2026.6.21 full'),
    ('Noahs_Metacognitive_Civilization_Narrative.py', r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py', '[YCIP] 数字联邦叙事 full'),
]

for fname, local, msg in FILES:
    print(f'\n--- {fname} ---')
    # Get current sha
    url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(fname)}?ref={BRANCH}'
    r = gitee_req(url)
    sha = r.get('sha')
    print(f'当前 sha: {sha}')
    with open(local, 'r', encoding='utf-8') as fh:
        content = fh.read()
    print(f'本地内容: {len(content)} chars')
    # Delete
    del_url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(fname)}'
    del_params = json.dumps({'access_token': GITEE_TOKEN, 'message': 'delete for re-create', 'branch': BRANCH, 'sha': sha})
    r2 = gitee_req(del_url, del_params, method='DELETE')
    print(f'DELETE: {r2}')
    # Recreate
    create_params = json.dumps({'access_token': GITEE_TOKEN, 'message': msg, 'content': content, 'branch': BRANCH})
    r3 = gitee_req(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(fname)}', create_params)
    print(f'CREATE: {r3}')
    if 'content' in str(r3):
        print(f'  -> ok!')
    elif 'error' in r3:
        print(f'  -> 失败: {r3}')

print('\n全部完成')
