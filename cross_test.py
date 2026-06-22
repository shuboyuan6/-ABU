import urllib.request, base64, json

PAT = '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'

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')

# Test with a known good public repo (microsoft/vscode-docs as test - should fail auth)
# Instead test with a different approach: use GitHub's GraphQL API to verify write access
# Or: try to get the repo'scollaborators to see if we're actually an owner

# Let me check repo permissions more carefully
req = urllib.request.Request('https://api.github.com/repos/shuboyuan6/-ABU')
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    print('repo.id: ' + str(data['id']))
    print('repo.full_name: ' + str(data['full_name']))
    print('repo.owner.type: ' + str(data['owner']['type']))
    print('repo.private: ' + str(data['private']))
    print('repo.permissions: ' + str(data['permissions']))
    print('repo.default_branch: ' + str(data['default_branch']))
except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])

# Also check: can we list collaborators?
req2 = urllib.request.Request('https://api.github.com/repos/shuboyuan6/-ABU/collaborators')
req2.add_header('Authorization', 'token ' + PAT)
req2.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp2 = urllib.request.urlopen(req2, timeout=10)
    collabs = json.loads(resp2.read())
    print('Collaborators: ' + str(len(collabs)))
    for c in collabs:
        print('  ' + c['login'] + ' permission=' + c.get('role_name', 'unknown'))
except urllib.error.HTTPError as e:
    print('collaborators HTTP ' + str(e.code))
