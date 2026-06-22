import urllib.request, base64, json

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'
# 直接放根目录
FILE_PATH = 'NOAH_FENCE_MAP.py'
API = 'https://api.github.com/repos/' + REPO + '/contents/' + FILE_PATH

print('推送到: ' + API)

# Check if exists
get_req = urllib.request.Request(API + '?ref=' + BRANCH)
get_req.add_header('Authorization', 'token ' + PAT)
get_req.add_header('Accept', 'application/vnd.github.v3+json')
sha = None
try:
    resp = urllib.request.urlopen(get_req, timeout=10)
    data = json.loads(resp.read())
    sha = data['sha']
    print('已存在 SHA=' + sha[:8])
except urllib.error.HTTPError as e:
    if e.code == 404:
        print('文件不存在，将新建')
    else:
        print('GET HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])

encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
msg = '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图：五类拉弯点 + 镜检7问 + quick_mirror\n无闭环。'
body = json.dumps({
    'message': msg,
    'content': encoded,
    'branch': BRANCH,
    **({'sha': sha} if sha else {}),
}).encode('utf-8')

put_req = urllib.request.Request(API, data=body)
put_req.add_header('Authorization', 'token ' + PAT)
put_req.add_header('Content-Type', 'application/json')
put_req.add_header('Accept', 'application/vnd.github.v3+json')

try:
    resp = urllib.request.urlopen(put_req, timeout=30)
    result = json.loads(resp.read())
    print('GitHub: 推送成功 commit=' + result['commit']['sha'])
except urllib.error.HTTPError as e:
    print('PUT HTTP ' + str(e.code) + ': ' + e.read().decode()[:400])
