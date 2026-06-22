import urllib.request, base64, json

PAT = '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'

# Try with a simple 5-byte file
test_content = 'hello'
encoded = base64.b64encode(test_content.encode('utf-8')).decode('ascii')

API = 'https://api.github.com/repos/shuboyuan6/-ABU/contents/test_simple_123.txt'
body = json.dumps({
    'message': 'simple test',
    'content': encoded,
    'branch': 'main',
}).encode('utf-8')

req = urllib.request.Request(API, data=body)
req.add_header('Authorization', 'token ' + PAT)
req.add_header('Content-Type', 'application/json')
req.add_header('Accept', 'application/vnd.github.v3+json')

try:
    resp = urllib.request.urlopen(req, timeout=20)
    result = json.loads(resp.read())
    print('简单文件推送成功: ' + result['commit']['sha'][:8])
    # Delete the test file immediately
    # Get its sha first
    get_req = urllib.request.Request(API + '?ref=main')
    get_req.add_header('Authorization', 'token ' + PAT)
    get_req.add_header('Accept', 'application/vnd.github.v3+json')
    get_resp = urllib.request.urlopen(get_req, timeout=10)
    sha = json.loads(get_resp.read())['sha']
    del_body = json.dumps({
        'message': 'cleanup test',
        'sha': sha,
        'branch': 'main',
    }).encode('utf-8')
    del_req = urllib.request.Request(API, data=del_body, method='DELETE')
    del_req.add_header('Authorization', 'token ' + PAT)
    del_req.add_header('Content-Type', 'application/json')
    del_req.add_header('Accept', 'application/vnd.github.v3+json')
    del_resp = urllib.request.urlopen(del_req, timeout=20)
    print('清理测试文件成功')
except urllib.error.HTTPError as e:
    body_err = e.read().decode('utf-8')
    print('HTTP ' + str(e.code) + ': ' + body_err)
    # If 404, the whole API endpoint might be broken for this repo
    if e.code == 404:
        print('*** 404 on contents API - 尝试检查这个仓库是否支持某些操作 ***')
        # Check repo topics
        topics_req = urllib.request.Request('https://api.github.com/repos/shuboyuan6/-ABU/topics')
        topics_req.add_header('Authorization', 'token ' + PAT)
        topics_req.add_header('Accept', 'application/vnd.github.v3+json')
        try:
            tr = urllib.request.urlopen(topics_req, timeout=10)
            print('topics: ' + str(json.loads(tr.read())))
        except:
            print('topics also 404')
