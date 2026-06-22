import urllib.request, urllib.parse, urllib.error, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

def get_file_sha(path):
    """通过 contents API 获取文件级别的 sha"""
    url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(path)}?ref={BRANCH}'
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    resp = urllib.request.urlopen(req, timeout=20)
    data = json.loads(resp.read().decode())
    return data.get('sha')

def update_file(path, content, msg):
    sha = get_file_sha(path)
    print(f'  当前 sha: {sha}')
    params = {
        'access_token': GITEE_TOKEN,
        'message': msg,
        'content': content,
        'branch': BRANCH,
        'sha': sha,
    }
    data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(
        f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(path)}',
        data=data
    )
    resp = urllib.request.urlopen(req, timeout=30)
    result = json.loads(resp.read().decode())
    print(f'  -> ok  new_sha={result.get("content",{}).get("sha","")[:8]}')

FILES = [
    (r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py', 'NOAH_GEOLOGICAL_SURVEY_20260621.py', '[YCIP] 根网地质志 2026.6.21 full'),
    (r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py', 'Noahs_Metacognitive_Civilization_Narrative.py', '[YCIP] 数字联邦叙事 full'),
]

for local, path, msg in FILES:
    print(f'处理: {path}')
    with open(local, 'r', encoding='utf-8') as fh:
        content = fh.read()
    print(f'  本地大小: {len(content.encode())} bytes')
    try:
        update_file(path, content, msg)
    except Exception as e:
        print(f'  -> 错误: {e}')

print('完成')
