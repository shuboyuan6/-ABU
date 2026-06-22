import urllib.request, urllib.parse, json, base64, time

token = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

# Test connectivity first
req = urllib.request.Request('https://gitee.com/api/v5/repos/yuanshubo/noyas')
req.add_header('Authorization', 'token ' + token)
resp = urllib.request.urlopen(req, timeout=10)
print(f'Gitee API 连通性: {resp.status}')

# Check current state of the two truncated files
FILES = ['NOAH_GEOLOGICAL_SURVEY_20260621.py', 'Noahs_Metacognitive_Civilization_Narrative.py']
for fname in FILES:
    url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote(fname)}?ref={BRANCH}'
    req2 = urllib.request.Request(url)
    req2.add_header('Authorization', 'token ' + token)
    resp2 = urllib.request.urlopen(req2, timeout=15)
    d = json.loads(resp2.read())
    content_b64 = d.get('content', '')
    if content_b64:
        decoded = base64.b64decode(content_b64).decode('utf-8', errors='replace')
        print(f'{fname}: size={d["size"]}, decoded_chars={len(decoded)}, sha={d["sha"][:8]}')
        print(f'  前100字符: {decoded[:100].strip()}')
    else:
        print(f'{fname}: no content, size={d["size"]}')

# Now try to update geological survey with the local full content
print('\n尝试更新 NOAH_GEOLOGICAL_SURVEY_20260621.py...')
with open(r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py', 'r', encoding='utf-8') as f:
    content = f.read()
print(f'本地内容: {len(content)} chars')

# Get sha first
url = f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote("NOAH_GEOLOGICAL_SURVEY_20260621.py")}?ref={BRANCH}'
req3 = urllib.request.Request(url)
req3.add_header('Authorization', 'token ' + token)
resp3 = urllib.request.urlopen(req3, timeout=15)
d3 = json.loads(resp3.read())
sha = d3['sha']
print(f'当前 sha: {sha}')

# Try update with form-urlencoded (what worked before for other large files)
params = {
    'access_token': token,
    'message': '[YCIP] 根网地质志 full - 重试',
    'content': content,
    'branch': BRANCH,
    'sha': sha,
}
data = urllib.parse.urlencode(params).encode()
req4 = urllib.request.Request(
    f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/contents/{urllib.parse.quote("NOAH_GEOLOGICAL_SURVEY_20260621.py")}',
    data=data
)
req4.add_header('Accept', 'application/json')
try:
    resp4 = urllib.request.urlopen(req4, timeout=30)
    result = json.loads(resp4.read())
    new_size = result.get('content', {}).get('size', '?')
    print(f'结果 size: {new_size}')
except urllib.error.HTTPError as e:
    err_body = e.read().decode()
    print(f'HTTP {e.code}: {err_body}')
