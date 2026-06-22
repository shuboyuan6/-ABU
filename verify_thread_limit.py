# verify_thread_limit.py - 验证 num_thread=4 是否正确加入各 Ollama 调用点
files = {
    r"C:\Users\shubo\诺亚斯初代\noahs_agent_loop.py": "call_ollama()",
    r"C:\Users\shubo\诺亚斯库\noahs_v2_cognition.py": "_think_slow()",
    r"C:\Users\shubo\诺亚斯库\noahs_memory_recall.py": "_call_llm()",
    r"C:\Users\shubo\诺亚斯库\noahs_concurrent_inference.py": "_local_task()",
}

all_ok = True
for f, name in files.items():
    try:
        with open(f, "r", encoding="utf-8") as fp:
            content = fp.read()
        has_thread = '"num_thread": 4' in content or "'num_thread': 4" in content
        status = "OK" if has_thread else "MISSING"
        if not has_thread:
            all_ok = False
        print(f"  [{status}] {name} ({f.split('\\')[-1]})")
    except Exception as e:
        print(f"  [ERROR] {name}: {e}")
        all_ok = False

print()
if all_ok:
    print("All 4 locations verified: num_thread=4 is correctly set.")
else:
    print("Some locations are missing num_thread=4 - please check!")
