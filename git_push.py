import urllib.request, base64, json

LOCAL_FILE = r'C:\Users\shubo\abu_github\noahs_gitee\NOAH_FENCE_MAP.py'
with open(LOCAL_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

PAT = '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'
REPO = 'shuboyuan6/-ABU'
BRANCH = 'main'
FILE_PATH = 'NOAH_FENCE_MAP.py'
COMMIT_MSG = '[YCIP] NoahFenceMap v0.2 - 袁书波 2026-06-21\n围栏地图：五类拉弯点 + 镜检7问 + quick_mirror\n无闭环。'

def get_sha(path):
    """Get file SHA if file exists"""
    url = 'https://api.github.com/repos/' + REPO + '/contents/' + path + '?ref=' + BRANCH
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        return json.loads(resp.read())['sha']
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

def get_ref():
    url = 'https://api.github.com/repos/' + REPO + '/git/ref/heads/' + BRANCH
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=10)
    data = json.loads(resp.read())
    return data['object']['sha']

def get_commit(commit_sha):
    url = 'https://api.github.com/repos/' + REPO + '/git/commits/' + commit_sha
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=10)
    return json.loads(resp.read())

def create_blob(content):
    url = 'https://api.github.com/repos/' + REPO + '/git/blobs'
    data = json.dumps({'content': content, 'encoding': 'utf-8'}).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read())['sha']

def create_tree(base_tree_sha, file_path, blob_sha):
    url = 'https://api.github.com/repos/' + REPO + '/git/trees'
    data = json.dumps({
        'base_tree': base_tree_sha,
        'tree': [{'path': file_path, 'mode': '100644', 'type': 'blob', 'sha': blob_sha}],
    }).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=20)
    return json.loads(resp.read())['sha']

def create_commit(tree_sha, parent_sha, message):
    url = 'https://api.github.com/repos/' + REPO + '/git/commits'
    data = json.dumps({'message': message, 'tree': tree_sha, 'parents': [parent_sha]}).encode('utf-8')
    req = urllib.request.Request(url, data=data)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    resp = urllib.request.urlopen(req, timeout=20)
    return json.loads(resp.read())['sha']

def update_ref(new_commit_sha):
    url = 'https://api.github.com/repos/' + REPO + '/git/refs/heads/' + BRANCH
    data = json.dumps({'sha': new_commit_sha}).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='PATCH')
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Content-Type', 'application/json')
    req.add_header('Accept', 'application/vnd.github.v3+json')
    urllib.request.urlopen(req, timeout=15)

# Check if file already exists (get its sha for update)
existing_sha = get_sha(FILE_PATH)
print('文件状态: ' + ('已存在，会更新' if existing_sha else '不存在，将新建'))

# Get current branch tip
current_ref = get_ref()
current_commit = get_commit(current_ref)
base_tree = current_commit['tree']['sha']

# Create blob
blob_sha = create_blob(content)
print('Blob: ' + blob_sha[:8])

# Check if we need to handle the existing file case
# For updates, we need to include the old blob's SHA in the tree to delete it
tree_items = [{'path': FILE_PATH, 'mode': '100644', 'type': 'blob', 'sha': blob_sha}]
if existing_sha:
    # File exists - for update, we just replace it in the tree
    # The old blob will be garbage collected by GitHub eventually
    pass

new_tree_sha = create_tree(base_tree, FILE_PATH, blob_sha)
print('Tree: ' + new_tree_sha[:8])

new_commit_sha = create_commit(new_tree_sha, current_ref, COMMIT_MSG)
print('Commit: ' + new_commit_sha[:8])

update_ref(new_commit_sha)
print('')
print('GitHub: 推送成功! commit=' + new_commit_sha)
print('文件: https://github.com/shuboyuan6/-ABU/blob/main/NOAH_FENCE_MAP.py')
