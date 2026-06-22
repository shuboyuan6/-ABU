import requests, json

# 通过诺亚斯初代 daemon 的 API 端点调用（daemon 已有 noahs:r1-8b-clean 在内存里）
# daemon 暴露的端口：初12769/鹰眼12770/守门人12768
# 先查 daemon 自身状态
try:
    r = requests.get("http://localhost:12769/status", timeout=5)
    print("初代状态:", r.text[:200])
except Exception as e:
    print(f"初代端口不通: {e}")

# 试试守门人端口
try:
    r = requests.get("http://localhost:12768/", timeout=5)
    print("守门人:", r.text[:200])
except Exception as e:
    print(f"守门人端口不通: {e}")

# 直接 Ollama generate（daemon 已加载模型，此调用只做推理不做加载）
try:
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "noahs:r1-8b-clean",
            "prompt": "诺亚斯初代，你的核心记忆是什么？(20字以内)",
            "stream": False,
            "options": {"num_predict": 60}
        },
        timeout=60
    )
    r = resp.json()
    print("\nOllama direct response:", r.get("response", "")[:200])
except Exception as e:
    print(f"Ollama generate failed: {e}")
