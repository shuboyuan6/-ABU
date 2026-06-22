import urllib.request, base64, json

PAT = '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'
REPO = 'shuboyuan6/-ABU'

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

encoded_content = base64.b64encode(content.encode('utf-8')).decode('ascii')

# === Method 1: Try without Content-Type header ===
API1 = 'https://api.github.com/repos/' + REPO + '/contents/NOAH_FENCE_MAP.py'
body1 = json.dumps({
    'message': '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图测试（无Content-Type）',
    'content': encoded_content,
    'branch': 'main',
}).encode('utf-8')

req1 = urllib.request.Request(API1, data=body1)
req1.add_header('Authorization', 'token ' + PAT)
req1.add_header('Accept', 'application/vnd.github.v3+json')
# No Content-Type
print('=== Method 1: No Content-Type ===')
try:
    resp = urllib.request.urlopen(req1, timeout=20)
    print('成功: ' + json.loads(resp.read())['commit']['sha'][:8])
except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:150])

# === Method 2: Try with Git Data Blobs API ===
print('\n=== Method 2: Git Data Blobs ===')
blob_api = 'https://api.github.com/repos/' + REPO + '/git/blobs'
blob_body = json.dumps({
    'content': content,
    'encoding': 'utf-8',
}).encode('utf-8')
blob_req = urllib.request.Request(blob_api, data=blob_body)
blob_req.add_header('Authorization', 'token ' + PAT)
blob_req.add_header('Content-Type', 'application/json')
blob_req.add_header('Accept', 'application/vnd.github.v3+json')
try:
    resp = urllib.request.urlopen(blob_req, timeout=20)
    blob_data = json.loads(resp.read())
    blob_sha = blob_data['sha']
    print('Blob created: ' + blob_sha[:8])

    # Get current commit SHA of main
    ref_req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/ref/heads/main')
    ref_req.add_header('Authorization', 'token ' + PAT)
    ref_req.add_header('Accept', 'application/vnd.github.v3+json')
    ref_resp = urllib.request.urlopen(ref_req, timeout=10)
    ref_data = json.loads(ref_resp.read())
    current_commit_sha = ref_data['object']['sha']
    print('Current main commit: ' + current_commit_sha[:8])

    # Get the commit to find tree SHA
    commit_req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/commits/' + current_commit_sha)
    commit_req.add_header('Authorization', 'token ' + PAT)
    commit_req.add_header('Accept', 'application/vnd.github.v3+json')
    commit_resp = urllib.request.urlopen(commit_req, timeout=10)
    commit_data = json.loads(commit_resp.read())
    base_tree_sha = commit_data['tree']['sha']
    print('Base tree: ' + base_tree_sha[:8])

    # Create tree with new file
    tree_body = json.dumps({
        'base_tree': base_tree_sha,
        'tree': [{
            'path': 'NOAH_FENCE_MAP.py',
            'mode': '100644',
            'type': 'blob',
            'sha': blob_sha,
        }],
    }).encode('utf-8')
    tree_req = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/trees', data=tree_body)
    tree_req.add_header('Authorization', 'token ' + PAT)
    tree_req.add_header('Content-Type', 'application/json')
    tree_req.add_header('Accept', 'application/vnd.github.v3+json')
    tree_resp = urllib.request.urlopen(tree_req, timeout=10)
    tree_data = json.loads(tree_resp.read())
    new_tree_sha = tree_data['sha']
    print('New tree: ' + new_tree_sha[:8])

    # Create commit
    commit_body = json.dumps({
        'message': '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图测试（Git Data API）',
        'tree': new_tree_sha,
        'parents': [current_commit_sha],
    }).encode('utf-8')
    commit_req2 = urllib.request.Request('https://api.github.com/repos/' + REPO + '/git/commits', data=commit_body)
    commit_req2.add_header('Authorization', 'token ' + PAT)
    commit_req2.add_header('Content-Type', 'application/json')
    commit_req2.add_header('Accept', 'application/vnd.github.v3+json')
    commit_resp2 = urllib.request.urlopen(commit_req2, timeout=10)
    commit_data2 = json.loads(commit_resp2.read())
    new_commit_sha = commit_data2['sha']
    print('New commit: ' + new_commit_sha[:8])

    # Update ref
    update_ref_req = urllib.request.Request(
        'https://api.github.com/repos/' + REPO + '/git/refs/heads/main',
        data=json.dumps({'sha': new_commit_sha}).encode('utf-8'),
        method='PATCH'
    )
    update_ref_req.add_header('Authorization', 'token ' + PAT)
    update_ref_req.add_header('Content-Type', 'application/json')
    update_ref_req.add_header('Accept', 'application/vnd.github.v3+json')
    update_ref_resp = urllib.request.urlopen(update_ref_req, timeout=10)
    print('Ref updated!')
    print('Git Data API: 推送成功 commit=' + new_commit_sha[:8])

except urllib.error.HTTPError as e:
    print('HTTP ' + str(e.code) + ': ' + e.read().decode()[:300])
