import requests, json

resp = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "deepseek-r1:1.5b",
        "prompt": "诺亚斯的核心理念是什么？(10字以内)",
        "stream": False,
        "options": {"num_predict": 80}
    },
    timeout=90
)
result = resp.json()
print(json.dumps({k: str(v)[:200] for k, v in result.items()}, ensure_ascii=False, indent=2))
