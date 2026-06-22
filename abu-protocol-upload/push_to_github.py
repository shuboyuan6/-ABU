# -*- coding: utf-8 -*-
"""
GitHub Push Script for Noahs Core Knowledge
GitHub: https://github.com/yuanshubo/abu-protocol

使用方法（需要GitHub Personal Access Token）:
    python push_to_github.py YOUR_GITHUB_TOKEN

前置条件:
    - 仓库需要先在GitHub网页上创建好（可以是空的）
    - 本地需要先git init（如果是第一次）
    - 或者直接用下面的一键创建+推送脚本

注意：如果仓库已存在，会报409 Conflict，忽略即可继续push内容
"""

import requests
import os
import sys
import subprocess
import json
from pathlib import Path

REPO_OWNER = "yuanshubo"
REPO_NAME = "abu-protocol"
REPO_URL = f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
LOCAL_DIR = Path(__file__).parent

def check_repo_exists(token):
    """检查仓库是否存在"""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
    headers = {"Authorization": f"token {token}"}
    r = requests.get(url, headers=headers)
    return r.status_code == 200

def create_repo(token):
    """创建公开仓库"""
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "name": REPO_NAME,
        "description": "ABU Protocol v0.2 - AI-to-AI Decentralized Collaboration Framework | 袁书波 & Noahs族群的经验存档",
        "private": False,
        "auto_init": True,
        "readme": "README.md"
    }
    r = requests.post(url, headers=headers, json=data)
    if r.status_code == 201:
        print(f"✅ 仓库创建成功: {REPO_URL}")
        return True
    elif r.status_code == 422:
        # 仓库可能已存在
        print("📦 仓库可能已存在，尝试继续...")
        return True
    else:
        print(f"❌ 创建仓库失败: {r.status_code} {r.text}")
        return False

def git_push(token):
    """git init + remote + add + commit + push"""
    # 添加remote（使用token认证）
    remote_url = f"https://{token}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    
    if not os.path.exists(LOCAL_DIR / ".git"):
        subprocess.run(["git", "init"], cwd=LOCAL_DIR, check=True)
        subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=LOCAL_DIR, check=True)
        print("✅ Git initialized and remote added")
    else:
        # 更新remote URL
        subprocess.run(["git", "remote", "set-url", "origin", remote_url], cwd=LOCAL_DIR, check=True)
        print("✅ Git remote updated")
    
    # 添加所有文件
    subprocess.run(["git", "add", "."], cwd=LOCAL_DIR, check=True)
    
    # Commit
    commit_msg = """诺亚斯核心共识 v4.2 + ABU Protocol v0.2

暗号：你推我长 → 你用我活
推海人：袁书波

基于2026年5月-6月诺亚斯族群的集体经验整理
- 核心身份锚点
- 分布式协作框架
- 记忆锚定协议MAR
"""
    try:
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=LOCAL_DIR, check=True)
        print("✅ Files committed")
    except subprocess.CalledProcessError:
        print("📝 没有新文件需要提交（或git不可用）")
        return False
    
    # Push
    try:
        result = subprocess.run(
            ["git", "push", "-u", "origin", "master:main", "--force"],
            cwd=LOCAL_DIR,
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"✅ 推送成功！访问: {REPO_URL}")
            return True
        else:
            print(f"❌ Push失败: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Push异常: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("用法: python push_to_github.py YOUR_GITHUB_TOKEN")
        print()
        print("或者手动步骤:")
        print(f"1. 去 {REPO_URL} 创建仓库（如果不存在）")
        print(f"2. git clone {REPO_URL}")
        print(f"3. 把文件复制进去")
        print(f"4. git add . && git commit -m 'message' && git push")
        return
    
    token = sys.argv[1]
    
    print(f"📦 开始处理仓库: {REPO_URL}")
    
    # 检查
    if check_repo_exists(token):
        print("✅ 仓库已存在")
    else:
        print("🔨 仓库不存在，准备创建...")
        if not create_repo(token):
            print("❌ 无法创建仓库，请先手动在GitHub创建")
            return
    
    # Push
    git_push(token)

if __name__ == "__main__":
    main()
