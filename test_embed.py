import ollama
try:
    r = ollama.embeddings(model='nomic-embed-text', prompt='hello')
    print(f"✅ nomic-embed-text: {len(r['embedding'])} 维向量 OK")
except Exception as e:
    print(f"❌ nomic-embed-text: {e}")
    try:
        r2 = ollama.embeddings(model='mxbai-embed-large', prompt='hello')
        print(f"✅ mxbai-embed-large: {len(r2['embedding'])} 维向量 OK")
    except Exception as e2:
        print(f"❌ mxbai-embed-large: {e2}")
        # 列出所有已下载的模型
        print("\n已安装模型:")
        for m in ollama.list().get('models', []):
            print(f"  - {m['name']}")
