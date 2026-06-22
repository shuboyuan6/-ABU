import urllib.request, base64, json

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'
FILE_PATH = 'noahs_gitee/NOAH_FENCE_MAP.py'
API = 'https://api.github.com/repos/' + REPO + '/contents/' + FILE_PATH

# Get current SHA
get_url = API + '?ref=' + BRANCH
get_req = urllib.request.Request(get_url)
get_req.add_header('Authorization', 'token ' + PAT)
get_req.add_header('Accept', 'application/vnd.github.v3+json')
sha = None
try:
    resp = urllib.request.urlopen(get_req, timeout=10)
    data = json.loads(resp.read())
    sha = data['sha']
    print('GitHub: 已存在 SHA=' + sha[:8])
except Exception as e:
    print('GitHub: 新建文件 (' + str(e) + ')')

encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
msg = '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图：五类拉弯点 + 镜检7问 + quick_mirror\n无闭环。'
data = {
    'message': msg,
    'content': encoded,
    'branch': BRANCH,
}
if sha:
    data['sha'] = sha

put_req = urllib.request.Request(
    API,
    data=json.dumps(data).encode('utf-8'),
    headers={
        'Authorization': 'token ' + PAT,
        'Content-Type': 'application/json',
        'Accept': 'application/vnd.github.v3+json',
    }
)
try:
    resp = urllib.request.urlopen(put_req, timeout=30)
    result = json.loads(resp.read())
    commit_sha = result['commit']['sha']
    print('GitHub: 推送成功 commit=' + commit_sha)
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    print('GitHub: HTTP ' + str(e.code) + ' - ' + body[:500])
except Exception as e:
    print('GitHub: ' + str(e))
