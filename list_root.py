import urllib.request, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'

req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/contents/?ref=main')
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(req, timeout=15)
    files = json.loads(resp.read())
    for f in files:
        print(f['type'] + '  ' + f['name'])
except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:400])
