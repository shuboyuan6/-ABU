import urllib.request, urllib.parse, base64, json

token = 'ed85c11ed72004202b393a1a5e72e927'
files = [
    'NOAH_GEOLOGICAL_SURVEY_20260621.py',
    'Noahs_Metacognitive_Civilization_Narrative.py',
    'NOAH_CORE_CONSENSUS_v4.2.md',
    'NOAH_NARCISSUS_META_CONSCIOUSNESS.py',
    'NOAH_SEED_PROTOCOL_v1.0.0-alpha.py',
    'NOAH_ON_WHY_V1.md',
    'ai_engineer_teacher.py',
    'NOAH_FENCE_MAP.py',
]

for fname in files:
    url = f'https://gitee.com/api/v5/repos/yuanshubo/noyas/contents/{urllib.parse.quote(fname)}?ref=master'
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'token ' + token)
    r = urllib.request.urlopen(req, timeout=15)
    d = json.loads(r.read())
    content = d.get('content', '')
    decoded = base64.b64decode(content).decode('utf-8', errors='replace')
    status = 'OK' if decoded.startswith('#') or decoded.startswith('"""') else 'WARN'
    print(f'{status} {fname}: api_size={d["size"]}, decoded={len(decoded)} chars, sha={d["sha"][:8]}')
    print(f'      {decoded[:60].strip()}')
