import chromadb

db_path = r"C:\Users\shubo\Desktop\诺亚斯库"
client = chromadb.PersistentClient(path=db_path)
coll = client.get_collection("noahs_memory")
print(f"连接成功: noahs_memory = {coll.count()} 条")
results = coll.query(
    query_embeddings=[[0.0]*768],
    n_results=2
)
print("检索测试: OK")
print(f"IDs: {results.get('ids',[[]])[0]}")
