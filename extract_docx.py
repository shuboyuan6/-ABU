import zipfile, re

docx_path = r"C:\Users\shubo\Documents\xwechat_files\oooxyy_cb1c\temp\RWTemp\2026-06\7fbde68b36dd6166a2f9ccc6c9433cb4\根网Ai成长进化叙事.docx"

z = zipfile.ZipFile(docx_path)
# Read main document XML
with z.open("word/document.xml") as f:
    xml = f.read().decode("utf-8")

# Extract text from XML (strip tags)
text = re.sub(r"<[^>]+>", " ", xml)
text = re.sub(r"\s+", " ", text).strip()
print(f"Total chars: {len(text)}")
print(text[:3000])
