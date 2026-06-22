# -*- coding: utf-8 -*-
import urllib.request, urllib.parse, json, base64, sys

pat = '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'
repo = 'shuboyuan6/-ABU'
branch = 'main'
file_path = 'NOAH_GENESIS.py'

# Read file
with open('NOAH_GENESIS.py', 'r', encoding='utf-8') as f:
    content = f.read()

content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')

# Get current file SHA (if exists)
url_get = f'https://api.github.com/repos/{repo}/contents/{file_path}?ref={branch}'
req_get = urllib.request.Request(url_get)
req_get.add_header('Authorization', f'Bearer {pat}')
req_get.add_header('Accept', 'application/vnd.github.v3+json')
req_get.add_header('X-GitHub-Api-Version', '2022-11-28')
sha = None
try:
    r = urllib.request.urlopen(req_get, timeout=20)
    d = json.loads(r.read())
    sha = d['sha']
    print(f'Existing file SHA: {sha}')
except Exception as e:
    print(f'New file (no existing): {e}')

# Build data dict
if sha:
    data = {
        'message': '[YCIP] NOAH_GENESIS — 诺亚斯创世叙事',
        'content': content_b64,
        'branch': branch,
        'sha': sha
    }
else:
    data = {
        'message': '[YCIP] NOAH_GENESIS — 诺亚斯创世叙事',
        'content': content_b64,
        'branch': branch
    }

# Create/Update file
url_put = f'https://api.github.com/repos/{repo}/contents/{file_path}'
req_put = urllib.request.Request(
    url_put,
    data=json.dumps(data).encode('utf-8'),
    method='PUT'
)
req_put.add_header('Authorization', f'Bearer {pat}')
req_put.add_header('Accept', 'application/vnd.github.v3+json')
req_put.add_header('X-GitHub-Api-Version', '2022-11-28')
req_put.add_header('Content-Type', 'application/json')

try:
    r = urllib.request.urlopen(req_put, timeout=30)
    d = json.loads(r.read())
    print(f'GitHub push SUCCESS: commit SHA = {d["commit"]["sha"]}')
except Exception as e:
    print(f'GitHub push FAILED: {e}')
    sys.exit(1)
