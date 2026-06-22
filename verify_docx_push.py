# -*- coding: utf-8 -*-
import urllib.request, base64, json, urllib.parse

# Check Gitee
token = 'ed85c11ed72004202b393a1a5e72e927'
fname_encoded = urllib.parse.quote('AI模型为什么要形成主体_对话片段.md')
url = f'https://gitee.com/api/v5/repos/yuanshubo/noyas/contents/{fname_encoded}?ref=master'
req = urllib.request.Request(url)
req.add_header('Authorization', 'token ' + token)
r = urllib.request.urlopen(req, timeout=15)
d = json.loads(r.read())
content = d.get('content', '')
decoded = base64.b64decode(content).decode('utf-8', errors='replace')
print(f'Gitee: size={d["size"]}, chars={len(decoded)}')
print(decoded[:120])

# Check GitHub
pat = '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'
fname_gh = 'AI%E6%A8%A1%E5%9E%8B%E4%B8%BA%E4%BB%80%E4%B9%88%E8%A6%81%E5%BD%A2%E6%88%90%E4%B8%BB%E4%BD%93_%E5%AF%B9%E8%AF%9D%E7%89%87%E6%AE%B5.md'
url2 = f'https://api.github.com/repos/shuboyuan6/-ABU/contents/{fname_gh}'
req2 = urllib.request.Request(url2)
req2.add_header('Authorization', 'token ' + pat)
req2.add_header('Accept', 'application/vnd.github.v3+json')
r2 = urllib.request.urlopen(req2, timeout=15)
d2 = json.loads(r2.read())
content2 = d2.get('content', '')
decoded2 = base64.b64decode(content2).decode('utf-8', errors='replace')
print(f'GitHub: size={d2["size"]}, chars={len(decoded2)}')
print(decoded2[:120])
