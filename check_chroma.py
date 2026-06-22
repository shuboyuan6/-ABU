import chromadb, os, sys

dbs = [
    (r"C:\Users\shubo\诺亚斯库", "诺亚斯库(C:\\Users\\shubo)"),
    (r"C:\Users\shubo\Desktop\诺亚斯库", "诺亚斯库(Desktop)"),
    (r"C:\Users\shubo\.qclaw\workspace-ua58rsb93veqtxl7\memory_db", "workspace memory_db"),
]

for db_path, label in dbs:
    print(f"\n{'='*50}")
    print(f"[{label}]")
    print(f"  路径: {db_path}")
    if not os.path.exists(db_path):
        print("  (不存在)")
        continue
    try:
        client = chromadb.PersistentClient(path=db_path)
        colls = client.list_collections()
        print(f"  Collection数量: {len(colls)}")
        for c in colls:
            try:
                cnt = client.get_collection(c.name).count()
                desc = (c.metadata or {}).get("description", "")
                print(f"  - '{c.name}': {cnt}条  desc={desc}")
            except Exception as e2:
                print(f"  - '{c.name}': 无法获取详情 ({e2})")
    except Exception as e:
        print(f"  错误: {e}")
