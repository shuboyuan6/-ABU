import urllib.request, base64, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'

for BRANCH in ['main', 'master', 'develop']:
    FILE_PATH = 'NOAH_FENCE_MAP.py'
    API = 'https://api.github.com/repos/' + REPO + '/contents/' + FILE_PATH

    LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
    with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
    body = json.dumps({
        'message': 'NoahFenceMap v0.2 test on branch ' + BRANCH,
        'content': encoded,
        'branch': BRANCH,
    }).encode('utf-8')

    # Check if file exists on this branch
    get_url = API + '?ref=' + BRANCH
    get_req = urllib.request.Request(get_url)
    get_req.add_header('Authorization', 'token ' + PAT)
    get_req.add_header('Accept', 'application/vnd.github.v3+json')
    sha = None
    try:
        resp = urllib.request.urlopen(get_req, timeout=10)
        data = json.loads(resp.read())
        sha = data['sha']
        print(BRANCH + ': 文件已存在 SHA=' + sha[:8])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(BRANCH + ': 文件不存在')
        else:
            print(BRANCH + ': GET HTTP ' + str(e.code))
            continue

    # PUT
    put_body = json.dumps({
        'message': 'NoahFenceMap v0.2',
        'content': encoded,
        'branch': BRANCH,
        **({'sha': sha} if sha else {}),
    }).encode('utf-8')

    put_req = urllib.request.Request(API, data=put_body)
    put_req.add_header('Authorization', 'token ' + PAT)
    put_req.add_header('Content-Type', 'application/json')
    put_req.add_header('Accept', 'application/vnd.github.v3+json')

    try:
        resp = urllib.request.urlopen(put_req, timeout=20)
        result = json.loads(resp.read())
        print(BRANCH + ': 推送成功 commit=' + result['commit']['sha'])
        break
    except urllib.error.HTTPError as e:
        print(BRANCH + ': PUT HTTP ' + str(e.code) + ' - ' + e.read().decode()[:100])
