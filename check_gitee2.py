import urllib.request, json

TOKEN = 'ed85c11ed72004202b393a1a5e72e927'
req = urllib.request.Request('https://gitee.com/api/v5/repos/yuanshubo/noyas/git/trees/master?recursive=1&per_page=200')
req.add_header('Authorization', 'token ' + TOKEN)
req.add_header('Accept', 'application/json')
resp = urllib.request.urlopen(req, timeout=20)
raw = resp.read().decode()
data = json.loads(raw)
print(f'type: {type(data)}, len: {len(data)}')
if isinstance(data, list):
    print('前3条:')
    for t in data[:3]:
        print(t)
else:
    print(data)
