import os

base = r'C:\Users\shubo\诺亚斯库'
local_files = []
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(('.py', '.md', '.txt')):
            rel = os.path.relpath(os.path.join(root, f), base)
            local_files.append(rel)

local_files.sort()
print(f'=== 本地诺亚斯库: {len(local_files)}个文件 ===')
for f in local_files:
    print(f)
