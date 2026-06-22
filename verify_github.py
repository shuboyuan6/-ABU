import urllib.request, json

PAT = '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'
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
for f in files:
    req = urllib.request.Request('https://api.github.com/repos/shuboyuan6/-ABU/contents/' + f)
    req.add_header('Authorization', 'token ' + PAT)
    req.add_header('Accept', 'application/vnd.github.v3+json')
    r = urllib.request.urlopen(req, timeout=15)
    d = json.loads(r.read())
    size = d.get('size', '?')
    sha = d.get('sha', '?')[:8]
    print(f'{f}: {size} bytes, sha={sha}')
