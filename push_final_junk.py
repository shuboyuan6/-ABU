import urllib.request, urllib.error, json, base64, os

PAT = "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"
OWNER = "shuboyuan6"
REPO = "-ABU"
BRANCH = "main"

h = {"Authorization": f"token {PAT}", "Accept": "application/vnd.github.v3+json", "User-Agent": "noahs"}

def api(method, path, data=None):
    url = f"https://api.github.com{path}"
    req = urllib.request.Request(url, method=method, headers=h)
    if data:
        req.add_header("Content-Type", "application/json")
        req.data = json.dumps(data).encode()
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode(errors="replace")}, e.code

# 1. Get current branch
res, st = api("GET", f"/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}")
print(f"[1] GET ref: {st} -> {res['object']['sha'][:8]}")
sha = res["object"]["sha"]

# 2. Get tree SHA
res2, st2 = api("GET", f"/repos/{OWNER}/{REPO}/git/commits/{sha}")
tree = res2["tree"]["sha"]
print(f"[2] Tree: {tree[:8]}")

# 3. Create blobs
files = [
    ("noahs_gitee/NoahsExperienceLedger.py", r"C:\Users\shubo\abu_github\noahs_gitee\NoahsExperienceLedger.py"),
    ("noahs_gitee/Noahs_Federal_Narrative.py", r"C:\Users\shubo\abu_github\noahs_gitee\Noahs_Federal_Narrative.py"),
]
blobs = {}
for rel, abspath in files:
    with open(abspath, "rb") as f:
        content = f.read()
    encoded = base64.b64encode(content).decode()
    res3, st3 = api("POST", f"/repos/{OWNER}/{REPO}/git/blobs", {"content": encoded, "encoding": "base64"})
    print(f"[3] POST blob {rel}: {st3}")
    blobs[rel] = res3["sha"]

# 4. Create tree
tree_items = [{"path": k, "mode": "100644", "type": "blob", "sha": v} for k, v in blobs.items()]
res4, st4 = api("POST", f"/repos/{OWNER}/{REPO}/git/trees", {"base_tree": tree, "tree": tree_items})
print(f"[4] POST tree: {st4} -> {res4['sha'][:8]}")
new_tree = res4["sha"]

# 5. Create commit
res5, st5 = api("POST", f"/repos/{OWNER}/{REPO}/git/commits", {
    "message": "诺亚斯数字联邦：联邦叙事 + 伤疤引力账本 (via PAT HTTPS API 2026-06-19)",
    "tree": new_tree,
    "parents": [sha]
})
print(f"[5] POST commit: {st5} -> {res5['sha'][:8]}")
new_sha = res5["sha"]

# 6. Update branch
res6, st6 = api("PATCH", f"/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}", {"sha": new_sha})
print(f"[6] PATCH branch: {st6}")
print("\a✅ 推送完成！")
