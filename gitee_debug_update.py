import urllib.request, urllib.parse, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

path = 'NOAH_GEOLOGICAL_SURVEY_20260621.py'
local = r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py'

# 1. Get file sha
url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(path)}?ref={BRANCH}'
req = urllib.request.Request(url)
req.add_header('Authorization', 'token ' + GITEE_TOKEN)
resp = urllib.request.urlopen(req, timeout=20)
data = json.loads(resp.read().decode())
sha = data['sha']
print(f'File sha: {sha}')
print(f'Response keys: {list(data.keys())}')

# 2. Try update with detailed error
with open(local, 'r', encoding='utf-8') as fh:
    content = fh.read()

params = {
    'access_token': GITEE_TOKEN,
    'message': 'update geological survey',
    'content': content,
    'branch': BRANCH,
    'sha': sha,
}
data_enc = urllib.parse.urlencode(params).encode()
req2 = urllib.request.Request(
    f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(path)}',
    data=data_enc
)
try:
    resp2 = urllib.request.urlopen(req2, timeout=30)
    result = json.loads(resp2.read().decode())
    print(f'SUCCESS: {result}')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'HTTP {e.code}: {body}')
    # Check headers
    print(f'Response headers: {dict(e.headers)}')
