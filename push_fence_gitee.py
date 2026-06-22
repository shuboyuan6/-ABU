import urllib.request, urllib.parse, base64, json

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
OWNER = 'yuanshubo'
REPO = 'noyas'
FILE_PATH = 'noahs_gitee/NOAH_FENCE_MAP.py'
API = 'https://gitee.com/api/v5/repos/{}/{}/contents/{}'.format(
    OWNER, REPO, urllib.parse.quote(FILE_PATH)
)

# Get SHA
get_url = API + '?access_token=' + TOKEN + '&ref=master'
sha = None
try:
    resp = urllib.request.urlopen(get_url, timeout=10)
    data = json.loads(resp.read())
    sha = data.get('sha')
    print('Gitee: 已存在 SHA=' + sha[:8])
except Exception as e:
    print('Gitee: 新建文件 (' + str(e) + ')')

encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
msg = '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图：五类拉弯点 + 镜检7问 + quick_mirror\n无闭环。'
data = {
    'access_token': TOKEN,
    'message': msg,
    'content': encoded,
    'branch': 'master',
}
if sha:
    data['sha'] = sha

put_req = urllib.request.Request(
    API,
    data=json.dumps(data).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
try:
    resp = urllib.request.urlopen(put_req, timeout=30)
    result = json.loads(resp.read())
    commit_sha = result.get('commit', {}).get('sha', 'OK')
    print('Gitee: 推送成功 commit=' + commit_sha[:8])
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8')
    print('Gitee: HTTP ' + str(e.code) + ' - ' + body[:300])
except Exception as e:
    print('Gitee: ' + str(e))
