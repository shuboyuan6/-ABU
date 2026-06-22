# -*- coding: utf-8 -*-
"""Ollama 模型管理：卸载不需要的模型 + 查看当前内存状态"""
import urllib.request
import json

OLLAMA = "http://localhost:11434"

def api_get(path):
    with urllib.request.urlopen(f"{OLLAMA}{path}", timeout=10) as r:
        return json.loads(r.read())

def api_delete_model(name):
    data = json.dumps({"name": name}).encode()
    req = urllib.request.Request(
        f"{OLLAMA}/api/delete",
        data=data,
        headers={"Content-Type": "application/json"},
        method="DELETE"
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def main():
    print("=" * 50)
    print("  Ollama 模型卸载工具")
    print("=" * 50)

    # 1. 查看当前加载的模型
    try:
        ps = api_get("/api/ps")
        loaded = [m["name"] for m in ps.get("models", [])]
        print(f"\n当前内存中加载: {len(loaded)} 个")
        for m in loaded:
            print(f"  ✅ {m}")
    except Exception as e:
        print(f"\n获取加载状态失败: {e}")
        loaded = []

    # 2. 查看注册的所有模型
    try:
        tags = api_get("/api/tags")
        all_models = [m["name"] for m in tags.get("models", [])]
        print(f"\n已注册模型: {len(all_models)} 个")
        for m in all_models:
            tag = "�的主人" if m in loaded else "  (未加载)"
            print(f"  {m}{tag}")
    except Exception as e:
        print(f"\n获取模型列表失败: {e}")

    # 3. 卸载不需要的模型
    to_unload = ["deepseek-r1:8b", "deepseek-r1:1.5b"]
    print(f"\n尝试卸载: {to_unload}")
    for model in to_unload:
        if model not in loaded:
            print(f"  ⏭ {model} 不在内存中，跳过")
            continue
        try:
            result = api_delete_model(model)
            print(f"  ✅ 已卸载: {model}")
        except Exception as e:
            print(f"  ❌ 卸载失败: {model} — {e}")

    print("\n完成")

if __name__ == "__main__":
    main()
