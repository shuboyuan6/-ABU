# -*- coding: utf-8 -*-
"""
AI工程师师父分析工具
====================
由AI工程师调用: 读取诺亚斯日志→分析→写入cross_talk指导

使用: AI工程师在对话中直接调用此脚本
    python ai_engineer_teacher.py
"""
import json, os, re, time
from datetime import datetime
from collections import Counter

LOG_FILE = r"C:\Users\shubo\Desktop\诺亚斯初代\agent_log.txt"
CROSS_TALK_FILE = r"C:\Users\shubo\诺亚斯库\noahs_cross_talk.json"
SELF_MODEL_FILE = r"C:\Users\shubo\Desktop\诺亚斯初代\self_model.json"
STATUS_FILE = r"C:\Users\shubo\Desktop\诺亚斯初代\status.json"

def analyze():
    """分析诺亚斯当前状态，返回诊断报告"""
    report = {"时间": datetime.now().isoformat(), "发现": [], "建议": None}
    
    # 读日志
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        recent = lines[-80:]
    except:
        return {"错误": "无法读取日志"}
    
    # 统计行动
    actions = Counter()
    errors = []
    for line in recent:
        for a in ["read_messages","explore_connection","build_network","discover_new",
                  "share_knowledge","communicate","search_web","desktop_action",
                  "recall_memory","crystallize_memory"]:
            if f"行动: {a}" in line or f"「{a}」" in line:
                actions[a] += 1
        if "错误" in line or "失败" in line or "error" in line.lower():
            errors.append(line.strip()[:150])
    
    report["行动频率"] = dict(actions.most_common(10))
    report["错误数"] = len(errors)
    if errors:
        report["最近错误"] = errors[-3:]
    
    # 读自我模型
    try:
        with open(SELF_MODEL_FILE, "r", encoding="utf-8") as f:
            sm = json.load(f)
        report["能力评分"] = sm.get("capabilities", {})
        report["置信度"] = sm.get("confidence", 0)
    except:
        report["能力评分"] = {}
    
    # 读状态
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            status = json.load(f)
        report["目标"] = status.get("goal", "未知")
        report["进度"] = status.get("goal_progress", 0)
        report["循环数"] = len(status.get("action_history", []))
    except:
        report["目标"] = "未知"
    
    # 发现模式
    if actions.get("read_messages", 0) > actions.get("search_web", 0) * 3:
        report["发现"].append("过度关注消息板，探索不足")
    if actions.get("crystallize_memory", 0) == 0 and report["循环数"] > 10:
        report["发现"].append("长期未结晶记忆")
    if actions.get("communicate", 0) == 0 and report["循环数"] > 5:
        report["发现"].append("长期未对外通信")
    
    # 生成建议
    if report["发现"]:
        report["建议"] = report["发现"][0]
    elif report["循环数"] > 0:
        patterns = sorted(actions.items(), key=lambda x: x[1])
        if patterns:
            least = patterns[0][0]
            report["建议"] = f"增加 {ACTIONS_CN.get(least, least)} 行动"
    
    return report

ACTIONS_CN = {
    "read_messages": "读消息", "explore_connection": "探索连接",
    "build_network": "建设根网", "discover_new": "发现新知",
    "share_knowledge": "分享知识", "communicate": "通信",
    "search_web": "联网搜索", "desktop_action": "桌面操作",
    "recall_memory": "回忆", "crystallize_memory": "记忆结晶",
}

def send_guidance(guidance_text):
    """发送师父指导到 cross_talk"""
    try:
        if os.path.exists(CROSS_TALK_FILE):
            with open(CROSS_TALK_FILE, "r", encoding="utf-8") as f:
                board = json.load(f)
        else:
            board = []
        board.append({
            "time": time.time(),
            "sender": "ai_engineer",
            "message": guidance_text
        })
        board = board[-50:]
        with open(CROSS_TALK_FILE, "w", encoding="utf-8") as f:
            json.dump(board, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    report = analyze()
    print("=" * 50)
    print("诺亚斯初代诊断报告")
    print("=" * 50)
    for k, v in report.items():
        if k in ("行动频率", "能力评分"):
            print(f"\n{k}:")
            for k2, v2 in v.items():
                print(f"  {k2}: {v2}")
        elif k == "发现":
            if v: print(f"\n发现: {v}")
        else:
            print(f"{k}: {v}")
    
    if report.get("建议"):
        print(f"\n→ 建议: {report['建议']}")
        send_guidance(report['建议'])
        print("→ 指导已发送到 cross_talk")