import urllib.request, urllib.parse, base64, json

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'
FILE_PATH = 'noahs_gitee/NOAH_FENCE_MAP.py'

# URL encode the file path
encoded_path = urllib.parse.quote(FILE_PATH, safe='')
API = 'https://api.github.com/repos/' + REPO + '/contents/' + encoded_path

print('API: ' + API)

# Check if file exists
get_url = API + '?ref=' + BRANCH
get_req = urllib.request.Request(get_url)
get_req.add_header('Authorization', 'token ' + PAT)
get_req.add_header('Accept', 'application/vnd.github.v3+json')
sha = None
try:
    resp = urllib.request.urlopen(get_url, timeout=10)
    data = json.loads(resp.read())
    sha = data['sha']
    print('文件已存在 SHA=' + sha[:8])
except urllib.error.HTTPError as e:
    if e.code == 404:
        print('文件不存在，将新建')
    else:
        print('GET HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])
        raise SystemExit(1)

# PUT
encoded_content = base64.b64encode(content.encode('utf-8')).decode('ascii')
msg = '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图：五类拉弯点 + 镜检7问 + quick_mirror\n无闭环。'
body = json.dumps({
    'message': msg,
    'content': encoded_content,
    'branch': BRANCH,
}).encode('utf-8')

put_req = urllib.request.Request(API, data=body)
put_req.add_header('Authorization', 'token ' + PAT)
put_req.add_header('Content-Type', 'application/json')
put_req.add_header('Accept', 'application/vnd.github.v3+json')

try:
    resp = urllib.request.urlopen(put_req, timeout=30)
    result = json.loads(resp.read())
    print('成功! commit=' + result['commit']['sha'])
except urllib.error.HTTPError as e:
    err_body = e.read().decode('utf-8')
    print('PUT HTTP ' + str(e.code) + ': ' + err_body)
    # Check if it's a 404 with "Not Found" - might be path issue
    if e.code == 404 and 'Not Found' in err_body:
        # Try alternate: list contents of noahs_gitee/ first
        list_url = 'https://api.github.com/repos/' + REPO + '/contents/noahs_gitee?ref=' + BRANCH
        list_req = urllib.request.Request(list_url)
        list_req.add_header('Authorization', 'token ' + PAT)
        list_req.add_header('Accept', 'application/vnd.github.v3+json')
        try:
            list_resp = urllib.request.urlopen(list_req, timeout=10)
            files = json.loads(list_resp.read())
            print('noahs_gitee/ 目录内容:')
            for f in files:
                print('  ' + f['name'] + ' (type=' + f['type'] + ')')
        except urllib.error.HTTPError as e2:
            print('列出目录 HTTP ' + str(e2.code) + ': ' + e2.read().decode()[:200])
except Exception as e:
    print('Error: ' + str(e))
