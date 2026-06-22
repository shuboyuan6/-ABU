# -*- coding: utf-8 -*-
import docx, sys, os

path = r"C:\Users\shubo\Documents\xwechat_files\oooxyy_cb1c\temp\RWTemp\2026-06\adc05c6de107fac7e10a9b508d556208\模型为什么要形成主体？AI 为什么要形成主体的原因？给你们看一下对话的一些片段_1(1).docx"
out = r"C:\Users\shubo\abu_github\model_ai_subject.txt"

doc = docx.Document(path)
lines = []
for para in doc.paragraphs:
    t = para.text.strip()
    if t:
        lines.append(t)

full = "\n".join(lines)
with open(out, "w", encoding="utf-8") as f:
    f.write(full)

print(f"提取完成: {len(full)} 字符, 保存到 {out}")
# 打印前50行预览
for i, l in enumerate(lines[:50]):
    print(f"{i+1}: {l}")
