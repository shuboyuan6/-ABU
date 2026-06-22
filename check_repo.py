import urllib.request, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'

# Get repo info
req = urllib.request.Request('https://api.github.com/repos/' + REPO)
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    print('default_branch: ' + data['default_branch'])
    print('permissions: ' + str(data.get('permissions', {})))
except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:300])

# List branches
req2 = urllib.request.Request('https://api.github.com/repos/' + REPO + '/branches')
req2.add_header('Authorization', 'token ' + PAT)
req2.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp2 = urllib.request.urlopen(req2, timeout=10)
    branches = json.loads(resp2.read())
    for b in branches:
        print('branch: ' + b['name'] + ' (default=' + str(b.get('is_default', False)) + ')')
except urllib.error.HTTPError as e:
    print('branches HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])
