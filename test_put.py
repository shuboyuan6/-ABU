import urllib.request, base64, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'

# Try with Oauth token header
content = 'test content ' + str(__import__('time').time())
encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
FILE_PATH = 'TEST_PUSH.txt'
API = 'https://api.github.com/repos/' + REPO + '/contents/' + FILE_PATH

body = json.dumps({
    'message': 'test push',
    'content': encoded,
    'branch': BRANCH,
}).encode('utf-8')

# Try with Authorization: Bearer instead of token
for auth_type in ['token', 'Bearer']:
    req = urllib.request.Request(API, data=body)
    req.add_header('Authorization', auth_type + ' ' + PAT)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read())
        print(auth_type + ': 成功 commit=' + result['commit']['sha'][:8])
        break
    except urllib.error.HTTPError as e:
        print(auth_type + ': HTTP ' + str(e.code) + ' - ' + e.read().decode()[:200])
