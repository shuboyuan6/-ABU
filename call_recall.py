import requests, json, time, os

# ========== 向量检索（ChromaDB）==========
import chromadb
NOAH_LIB_PATH = r"C:\Users\shubo\Desktop\诺亚斯库"
EMBED_MODEL = "nomic-embed-text:latest"
OLLAMA_URL = "http://localhost:11434"

_client = None
_coll = None

def _get_db():
    global _client, _coll
    if _client is None:
        _client = chromadb.PersistentClient(path=NOAH_LIB_PATH)
        _coll = _client.get_collection("noahs_memory")
    return _coll

def get_embedding(text):
    resp = requests.post(f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text}, timeout=30)
    return resp.json()["embedding"]

def retrieve_memories(prompt, top_k=3):
    coll = _get_db()
    q_emb = get_embedding(prompt)
    results = coll.query(query_embeddings=[q_emb], n_results=top_k)
    memories = []
    if results.get("ids") and len(results["ids"]) > 0:
        for mem_id, doc, dist in zip(
            results["ids"][0], results["documents"][0], results["distances"][0]):
            memories.append({
                "id": mem_id,
                "text": doc,
                "similarity": max(0.0, 1.0 - dist)
            })
    return memories

# ========== 记忆上下文 + LLM ==========
def ask_with_memory(question, top_k=3):
    memories = retrieve_memories(question, top_k=top_k)
    if not memories:
        return {"answer": None, "memories": [], "count": 0}

    context = "\n".join(
        f"[相关度{int(m['similarity']*100)}%] {m['text']}"
        for m in memories
    )

    prompt = f"""你是诺亚斯初代。基于以下核心记忆回答问题。
【相关记忆】
{context}

【当前问题】
{question}

要求：结合记忆内容，用诺亚斯的语气，一句话概括回答（20字以内）。"""

    resp = requests.post(f"{OLLAMA_URL}/api/generate",
        json={
            "model": "noahs:r1-8b-clean",
            "prompt": prompt,
            "stream": False,
            "options": {"num_predict": 300, "temperature": 0.7}
        },
        timeout=150
    )
    r = resp.json()
    answer = r.get("response", "").strip()
    if not answer and r.get("thinking"):
        lines = r["thinking"].strip().split("\n")
        answer = lines[-1][:200] if lines else r["thinking"][-200:]

    return {"answer": answer, "memories": memories, "count": len(memories),
            "eval_ms": round(r.get("total_duration", 0)/1e6)}

# ========== 测试 ==========
print("=== 向量记忆召回 + LLM 组合测试 ===\n")
coll = _get_db()
print(f"记忆总数: {coll.count()} 条\n")

questions = [
    "诺亚斯的核心理念是什么？",
    "什么是根网？",
    "安全态是什么？",
]

for q in questions:
    print(f"问: {q}")
    r = ask_with_memory(q)
    print(f"答: {r['answer']}")
    print(f"相关记忆 {r['count']} 条:")
    for m in r["memories"]:
        print(f"  [{int(m['similarity']*100)}%] {m['text'][:80]}...")
    print(f"耗时: {r.get('eval_ms','?')}ms\n")

# 保存最终结果
with open(r"C:\Users\shubo\abu_github\recall_result.json", "w", encoding="utf-8") as f:
    json.dump({"questions": questions, "results": [ask_with_memory(q) for q in questions]}, f, ensure_ascii=False, indent=2)
print("结果已保存到 recall_result.json")
