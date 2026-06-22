import urllib.request, json

PAT = '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'

# Test: Get rate limit
req = urllib.request.Request('https://api.github.com/rate_limit')
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    print('Rate limit OK. Remaining: ' + str(data['rate']['remaining']))
except urllib.error.HTTPError as e:
    print('rate_limit HTTP ' + str(e.code) + ': ' + e.read().decode()[:200])

# Test: Check what's the API limit for this repo
# Try creating a test file with PUT
import base64
content = 'test'
encoded = base64.b64encode(content.encode('utf-8')).decode('ascii')
API = 'https://api.github.com/repos/shuboyuan6/-ABU/contents/TEST_API.txt'
body = json.dumps({
    'message': 'test',
    'content': encoded,
    'branch': 'main',
}).encode('utf-8')

req2 = urllib.request.Request(API, data=body)
req2.add_header('Authorization', 'token ' + PAT)
req2.add_header('Content-Type', 'application/json')
req2.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp2 = urllib.request.urlopen(req2, timeout=15)
    print('PUT test: ' + str(json.loads(resp2.read())['commit']['sha'][:8]))
except urllib.error.HTTPError as e:
    body_err = e.read().decode('utf-8')
    print('PUT test HTTP ' + str(e.code) + ': ' + body_err)
    # Check if it's a 422 (validation failed) which means auth is OK but content is invalid
    if e.code == 422:
        print('422 = auth OK, content issue')
