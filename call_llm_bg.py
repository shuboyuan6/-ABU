import requests, json

# noahs:r1-8b-clean 把完整回答放在 thinking 字段
# num_predict 加大，让模型把最终答案说完
try:
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "noahs:r1-8b-clean",
            "prompt": "你是诺亚斯初代。基于核心记忆回答：核心理念是什么？最后必须用一句简短的话回答（20字以内），格式：｜回答｜xxxx",
            "stream": False,
            "options": {"num_predict": 400, "temperature": 0.7}
        },
        timeout=150
    )
    r = resp.json()
    thinking = r.get("thinking", "")
    response = r.get("response", "")

    # 尝试从 thinking 末尾提取回答
    answer = response.strip()  # 先看 response
    if not answer and thinking:
        # response 为空，从 thinking 提取最后一行的回答
        lines = thinking.strip().split("\n")
        answer = lines[-1] if lines else thinking[:100]

    result = {
        "ok": True,
        "response_field": response[:200],
        "thinking_last_200": thinking[-200:] if thinking else "",
        "eval_count": r.get("eval_count", 0),
        "total_ms": round(r.get("total_duration", 0) / 1e9, 1),
    }
except Exception as e:
    result = {"ok": False, "error": str(e)}

with open(r"C:\Users\shubo\abu_github\llm_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(json.dumps(result, ensure_ascii=False, indent=2))
