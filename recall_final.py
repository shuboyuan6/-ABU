import requests, json, time, sys
sys.path.insert(0, r"C:\Users\shubo\诺亚斯库")
sys.path.insert(0, r"C:\Users\shubo\诺亚斯初代")
import chromadb

OLLAMA = "http://localhost:11434"
EMBED = "nomic-embed-text:latest"
MODEL = "noahs:r1-8b-clean"

# 1. 连接记忆库
print("[1] 连接 ChromaDB...")
cli = chromadb.PersistentClient(path=r"C:\Users\shubo\Desktop\诺亚斯库")
coll = cli.get_collection("noahs_memory")
print(f"    记忆: {coll.count()} 条")

# 2. 向量检索
question = "诺亚斯的核心理念是什么？"
print(f"[2] 检索: {question}")
q_emb = requests.post(f"{OLLAMA}/api/embeddings",
    json={"model": EMBED, "prompt": question}, timeout=30).json()["embedding"]
res = coll.query(query_embeddings=[q_emb], n_results=3)
memories = []
for i in range(len(res["ids"][0])):
    sim = max(0.0, 1.0 - res["distances"][0][i])
    txt = res["documents"][0][i]
    memories.append({"sim": sim, "text": txt})
    print(f"    [{sim*100:.0f}%] {txt[:70]}...")

# 3. 组合 prompt + LLM
context = "\n".join(f"[{int(m['sim']*100)}%] {m['text']}" for m in memories)
prompt = f"""你是诺亚斯初代。根据以下核心记忆回答。

记忆：{context}

问题：{question}

用诺亚斯的语气，一句话概括核心理念（20字以内）。"""

print("[3] 调用模型...")
t0 = time.time()
r = requests.post(f"{OLLAMA}/api/chat",
    json={
        "model": MODEL,
        "stream": False,
        "messages": [
            {"role": "system", "content": "你是诺亚斯初代。用诺亚斯的语气简短回答。"},
            {"role": "user", "content": prompt}
        ],
        "options": {"num_predict": 200}
    },
    timeout=240)
elapsed = time.time() - t0
msg = r.json().get("message", {})
content = msg.get("content", "").strip()
print(f"    耗时: {elapsed:.0f}s")
print(f"\n答: {content}")

# 4. 保存
with open(r"C:\Users\shubo\abu_github\recall_result.json", "w", encoding="utf-8") as f:
    json.dump({"question": question, "answer": content,
               "memories": memories, "elapsed_s": round(elapsed,1)},
              f, ensure_ascii=False, indent=2)
print("\n[OK] 结果已保存 recall_result.json")
