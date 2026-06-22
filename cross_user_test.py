import urllib.request, base64, json

PAT = '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'

# Test with a DIFFERENT repo - use shuboyuan6's other known repo or create one
# First: check what other repos shuboyuan6 has
req = urllib.request.Request('https://api.github.com/users/shuboyuan6/repos?per_page=100')
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    repos = json.loads(resp.read())
    print('Repos:')
    for r in repos:
        print('  ' + r['full_name'] + ' (default_branch=' + r['default_branch'] + ')')
except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])
