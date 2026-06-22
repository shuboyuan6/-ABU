import requests, json, time, os, sys

# 路径修复
sys.path.insert(0, r"C:\Users\shubo\诺亚斯库")
sys.path.insert(0, r"C:\Users\shubo\诺亚斯初代")

import chromadb
NOAH_LIB_PATH = r"C:\Users\shubo\Desktop\诺亚斯库"
EMBED_MODEL = "nomic-embed-text:latest"
OLLAMA_URL = "http://localhost:11434"

print("[1/4] 连接 ChromaDB...")
_client = chromadb.PersistentClient(path=NOAH_LIB_PATH)
_coll = _client.get_collection("noahs_memory")
print(f"    记忆总数: {_coll.count()} 条")

print("[2/4] 获取问题 embedding...")
question = "诺亚斯的核心理念是什么？"
r_emb = requests.post(f"{OLLAMA_URL}/api/embeddings",
    json={"model": EMBED_MODEL, "prompt": question}, timeout=30)
emb = r_emb.json()["embedding"]
print(f"    embedding 维度: {len(emb)}")

print("[3/4] 向量检索...")
results = _coll.query(query_embeddings=[emb], n_results=3)
memories = []
for mem_id, doc, dist in zip(results["ids"][0], results["documents"][0], results["distances"][0]):
    memories.append({"id": mem_id, "text": doc, "similarity": max(0.0, 1.0-dist)})
    print(f"    [{int(max(0,1-dist)*100)}%] {doc[:80]}...")

print("[4/4] 调用 LLM (noahs:r1-8b-clean)...")
context = "\n".join(f"[{int(m['similarity']*100)}%] {m['text']}" for m in memories)
prompt = f"""你是诺亚斯初代。基于以下核心记忆回答问题。

【相关记忆】
{context}

【当前问题】
{question}

要求：结合记忆内容，用诺亚斯的语气，一句话概括回答（20字以内）。"""

t0 = time.time()
r_llm = requests.post(f"{OLLAMA_URL}/api/generate",
    json={"model": "noahs:r1-8b-clean", "prompt": prompt, "stream": False,
          "options": {"num_predict": 300, "temperature": 0.7}},
    timeout=150)
elapsed = time.time() - t0
r = r_llm.json()
answer = r.get("response","").strip()
if not answer and r.get("thinking"):
    answer = r["thinking"].strip()[-300:]

print(f"\n=== 结果 (耗时 {elapsed:.1f}s) ===")
print(f"问: {question}")
print(f"答: {answer}")
print(f"tokens: {r.get('eval_count', '?')}")

# 保存
out = {"question": question, "answer": answer, "memories": memories,
       "elapsed_s": round(elapsed, 1), "eval_count": r.get("eval_count", 0)}
with open(r"C:\Users\shubo\abu_github\recall_result.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\n已保存 recall_result.json")
