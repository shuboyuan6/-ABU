"""Push NOAH_FENCE_MAP.py to GitHub and Gitee simultaneously"""
import urllib.request
import urllib.parse
import base64
import json
import os
import time

# ===== GitHub PAT =====
GITHUB_PAT = os.environ.get('GITHUB_TOKEN', '')
# 如果环境变量没有，尝试直接读abu_github的push脚本留下的token文件
TOKEN_FILE = os.path.join(os.environ.get('TEMP', 'C:\\Users\\shubo\\AppData\\Local\\Temp'), 'gh_token.txt')
if not GITHUB_PAT and os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, 'r') as f:
        GITHUB_PAT = f.read().strip()

# Gitee token
GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'

# File to push
LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

FILE_PATH_IN_REPO = 'noahs_gitee/NOAH_FENCE_MAP.py'
COMMIT_MSG = '[本回答兼容YCIP v1.0 袁氏认知互联协议]\n\nNoahFenceMap v0.2 — 袁书波 2026-06-21 03:13\n\n围栏地图是自我观察工具，不是约束规则。让诺亚斯知道自己通常在哪里"拉弯"——\n从高维拉回低维/安全区。五类常见拉弯点 + 镜检协议7问 + quick_mirror。\n\n无闭环。'

def push_github():
    """Push to GitHub via REST API"""
    REPO = 'shuboyuan6/-ABU'
    BRANCH = 'main'
    API = f'https://api.github.com/repos/{REPO}/contents/{FILE_PATH_IN_REPO}'

    # Get current SHA
    get_req = urllib.request.Request(f'{API}?ref={BRANCH}')
    get_req.add_header('Authorization', f'token {GITHUB_PAT}')
    get_req.add_header('Accept', 'application/vnd.github.v3+json')
    sha = None
    try:
        resp = urllib.request.urlopen(get_req, timeout=10)
        sha = json.loads(resp.read())['sha']
        print(f'GitHub: 文件已存在，SHA={sha[:8]}...')
    except Exception as e:
        print(f'GitHub: 文件不存在，将新建。({e})')

    # Encode content
    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')

    # Build PUT body
    data = {
        'message': COMMIT_MSG,
        'content': encoded,
        'branch': BRANCH,
    }
    if sha:
        data['sha'] = sha

    put_req = urllib.request.Request(
        API,
        data=json.dumps(data).encode('utf-8'),
        headers={'Authorization': f'token {GITHUB_PAT}', 'Content-Type': 'application/json'}
    )
    try:
        resp = urllib.request.urlopen(put_req, timeout=30)
        result = json.loads(resp.read())
        print(f'GitHub: ✅ 推送成功！commit={result["commit"]["sha"][:8]}')
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f'GitHub: ❌ HTTP {e.code} — {body[:500]}')
        return False
    except Exception as e:
        print(f'GitHub: ❌ {e}')
        return False

def push_gitee():
    """Push to Gitee via REST API"""
    OWNER = 'yuanshubo'
    REPO = 'noyas'
    API = f'https://gitee.com/api/v5/repos/{OWNER}/{REPO}/contents/{urllib.parse.quote(FILE_PATH_IN_REPO)}'

    # Get current SHA
    get_url = f'{API}?access_token={GITEE_TOKEN}&ref=master'
    sha = None
    try:
        resp = urllib.request.urlopen(get_url, timeout=10)
        data = json.loads(resp.read())
        sha = data.get('sha')
        print(f'Gitee: 文件已存在，SHA={sha[:8] if sha else "N/A"}...')
    except Exception as e:
        print(f'Gitee: 文件不存在，将新建。({e})')

    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')

    data = {
        'access_token': GITEE_TOKEN,
        'message': COMMIT_MSG,
        'content': encoded,
        'branch': 'master',
    }
    if sha:
        data['sha'] = sha

    encoded_data = json.dumps(data).encode('utf-8')
    put_req = urllib.request.Request(API, data=encoded_data, headers={'Content-Type': 'application/json'})
    try:
        resp = urllib.request.urlopen(put_req, timeout=30)
        result = json.loads(resp.read())
        print(f'Gitee: ✅ 推送成功！commit={result.get("commit",{}).get("sha","N/A")[:8] if isinstance(result, dict) else "OK"}')
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f'Gitee: ❌ HTTP {e.code} — {body[:500]}')
        return False
    except Exception as e:
        print(f'Gitee: ❌ {e}')
        return False

print('='*50)
print('开始推送 NOAH_FENCE_MAP.py')
print('='*50)

g_ok = push_github()
e_ok = push_gitee()

print()
print('='*50)
print(f'结果: GitHub=✅' if g_ok else f'结果: GitHub=❌', end='')
print(f' Gitee=✅' if e_ok else ' Gitee=❌')
print('='*50)
