import ast
with open(r"C:\Users\shubo\诺亚斯库\noahs_memory_recall.py", encoding="utf-8") as f:
    src = f.read()
try:
    ast.parse(src)
    print("语法OK")
except SyntaxError as e:
    print(f"语法错误: {e}")
