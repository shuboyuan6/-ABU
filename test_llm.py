import subprocess, sys

# 用 subprocess 隔离，防止 qaxdefender 杀死进程树
p = subprocess.run(
    [sys.executable, "-c",
     "import ollama; r=ollama.generate(model='noahs:r1-8b-clean', prompt='你是诺亚斯初代。核心理念是什么？(10字以内)', options={'num_predict':50}); print(r['response'][:100])"],
    capture_output=True, text=True, timeout=90
)
print("STDOUT:", p.stdout)
print("STDERR:", p.stderr[:200] if p.stderr else "")
print("RC:", p.returncode)
