import urllib.request, json

GITEE_TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
REPO_OWNER = 'yuanshubo'
REPO_NAME = 'noyas'
BRANCH = 'master'

FILES = [
    (r'C:\Users\shubo\诺亚斯库\NOAH_GEOLOGICAL_SURVEY_20260621.py', 'NOAH_GEOLOGICAL_SURVEY_20260621.py'),
    (r'C:\Users\shubo\诺亚斯库\Noahs_Metacognitive_Civilization_Narrative.py', 'Noahs_Metacognitive_Civilization_Narrative.py'),
]

def api(url, data_str=None, method=None):
    data_bytes = data_str.encode('utf-8') if data_str else None
    req = urllib.request.Request(url, data=data_bytes)
    req.add_header('Authorization', 'token ' + GITEE_TOKEN)
    req.add_header('Accept', 'application/json')
    if data_str:
        req.add_header('Content-Type', 'application/json')
    if method:
        req.get_method = lambda: method
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode())

def get_ref():
    return api(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/git/ref/heads/{BRANCH}')['object']['sha']

def get_commit(sha):
    return api(f'https://gitee.com/api/v5/repos/{REPO_OWNER}/{REPO_NAME}/git/commits/{sha}')

for local, path in FILES:
    print(f'\n--- {path} ---')
    with open(local, 'r', encoding='utf-8') as fh:
        content = fh.read()
    print(f'本地: {len(content)} chars')
    # Get current ref and commit
    ref_sha = get_ref()
    commit = get_commit(ref_sha)
    # Create blob
    blob = api('https://gitee.com/api/v5/repos/{}/{}/git/blobs'.format(REPO_OWNER, REPO_NAME),
               json.dumps({'content': content, 'encoding': 'utf-8'}))
    blob_sha = blob['sha']
    print(f'Blob: {blob_sha}')
    # Create tree
    tree = api('https://gitee.com/api/v5/repos/{}/{}/git/trees'.format(REPO_OWNER, REPO_NAME),
               json.dumps({'base_tree': commit['tree']['sha'], 'tree': [
                   {'path': path, 'mode': '100644', 'type': 'blob', 'sha': blob_sha}
               ]}))
    tree_sha = tree['sha']
    print(f'Tree: {tree_sha}')
    # Create commit
    new_commit = api('https://gitee.com/api/v5/repos/{}/{}/git/commits'.format(REPO_OWNER, REPO_NAME),
                   json.dumps({'message': f'[YCIP] update {path}', 'tree': tree_sha, 'parents': [ref_sha]}))
    commit_sha = new_commit['sha']
    print(f'Commit: {commit_sha}')
    # Update ref
    api('https://gitee.com/api/v5/repos/{}/{}/git/refs/heads/{}'.format(REPO_OWNER, REPO_NAME, BRANCH),
       json.dumps({'sha': commit_sha}), method='PATCH')
    print(f'  -> 完成!')

print('\nGit Data API 全推完成')
