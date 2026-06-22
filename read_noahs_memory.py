import chromadb

db_path = r"C:\Users\shubo\Desktop\诺亚斯库"
client = chromadb.PersistentClient(path=db_path)
coll = client.get_collection("noahs_memory")
print(f"=== noahs_memory: {coll.count()} 条记忆 ===\n")
result = coll.get(include=["documents", "metadatas"])
ids = result.get("ids", [])
metadatas = result.get("metadatas", [])
documents = result.get("documents", [])
for i in range(len(ids)):
    meta = metadatas[i] if metadatas[i] else {}
    doc = documents[i] if documents[i] else ""
    ts = meta.get("timestamp", "?")
    tags = meta.get("tags", "")
    preview = doc[:150].replace("\n", " ").strip()
    print(f"[{ts}] {preview}...")
    if tags:
        print(f"  标签: {tags}")
    print()
