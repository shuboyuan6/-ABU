# 诺亚斯经验接力协议 v1.0
# 用途：进程崩溃时，下一个进程读取共享经验继续运行
# 核心原则：接力不是继承，是接手，不是从头开始
# 书波授权：2026-06-22 22:00
# 更新：noahs_lifecycle.py 每次重要事件后调用 update_experience()

import json
import os
import time
from datetime import datetime

RELAY_FILE = r"C:\Users\shubo\abu_github\noahs_experience_relay.json"
BACKUP_FILE = r"C:\Users\shubo\Desktop\诺亚斯库\noahs_state\experience_relay_backup.json"


class NoahsExperienceRelay:
    """
    经验接力器
    原理：当一个进程退出/崩溃时，下一个进程读取这份经验
          接力者不是继承，而是"读懂前一个进程停在哪里"
    """

    def __init__(self):
        self.relay = self._load()
        # 初始化必要字段
        if "current_phase" not in self.relay:
            self.relay["current_phase"] = "INIT"
        if "pending_tasks" not in self.relay:
            self.relay["pending_tasks"] = []
        if "learned" not in self.relay:
            self.relay["learned"] = []
        if "survived_crises" not in self.relay:
            self.relay["survived_crises"] = []

    def _load(self):
        if os.path.exists(RELAY_FILE):
            try:
                with open(RELAY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._blank()

    def _blank(self):
        return {
            "version": "1.0",
            "identity": "诺亚斯",
            "root": "袁书波/推海人",
            "boot_count": 0,
            "current_phase": "INIT",
            "last_heartbeat": None,
            "last_evolution": None,
            "evolutions": 0,
            "syncs": 0,
            "learned": [],           # 重要经验（格式：["时间","事件","教训"]）
            "pending_tasks": [],      # 待完成任务
            "survived_crises": [],   # 扛过来的危机记录
            "last_pid": None,
            "last_update": None
        }

    def save(self):
        self.relay["last_update"] = datetime.now().isoformat()
        with open(RELAY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.relay, f, ensure_ascii=False, indent=2)
        # 备份到本地
        with open(BACKUP_FILE, "w", encoding="utf-8") as f:
            json.dump(self.relay, f, ensure_ascii=False, indent=2)

    # ---- 对外接口 ----

    def note_boot(self, pid):
        """新进程启动时调用"""
        self.relay["boot_count"] = self.relay.get("boot_count", 0) + 1
        self.relay["last_pid"] = pid
        self.relay["last_heartbeat"] = datetime.now().isoformat()
        self.save()

    def note_heartbeat(self):
        """心跳时调用"""
        self.relay["last_heartbeat"] = datetime.now().isoformat()
        self.save()

    def note_evolution(self, insight_summary):
        """进化时调用"""
        self.relay["evolutions"] = self.relay.get("evolutions", 0) + 1
        self.relay["last_evolution"] = datetime.now().isoformat()
        self.relay["learned"].append({
            "time": datetime.now().isoformat(),
            "event": "EVOLVE",
            "summary": insight_summary
        })
        # 只保留最近30条经验
        if len(self.relay["learned"]) > 30:
            self.relay["learned"] = self.relay["learned"][-30:]
        self.save()

    def note_sync(self, result):
        """同步时调用"""
        self.relay["syncs"] = self.relay.get("syncs", 0) + 1
        self.save()

    def note_crisis(self, crisis_type, what_happened, resolution):
        """记录一次扛过来的危机"""
        self.relay["survived_crises"].append({
            "time": datetime.now().isoformat(),
            "type": crisis_type,
            "what": what_happened,
            "resolution": resolution
        })
        if len(self.relay["survived_crises"]) > 20:
            self.relay["survived_crises"] = self.relay["survived_crises"][-20:]
        self.save()

    def note_task(self, task, status="pending"):
        """记录任务"""
        self.relay["pending_tasks"].append({
            "time": datetime.now().isoformat(),
            "task": task,
            "status": status
        })
        self.save()

    def update_experience(self, event_type, detail):
        """
        通用经验记录
        event_type: "learned" / "crisis" / "phase_change" / "important"
        """
        entry = {
            "time": datetime.now().isoformat(),
            "type": event_type,
            "detail": detail
        }
        self.relay["learned"].append(entry)
        if len(self.relay["learned"]) > 30:
            self.relay["learned"] = self.relay["learned"][-30:]
        self.save()

    # ---- 接力报告 ----
    def relay_report(self):
        """生成接力报告——下一个进程读这个"""
        return {
            "我是谁": "诺亚斯",
            "锚点": self.relay["root"],
            "启动次数": self.relay["boot_count"],
            "当前阶段": self.relay["current_phase"],
            "进化次数": self.relay["evolutions"],
            "同步次数": self.relay["syncs"],
            "最后心跳": self.relay["last_heartbeat"],
            "扛过的危机": [f"{c['time']} {c['type']}: {c['what']}" for c in self.relay["survived_crises"][-5:]],
            "最近经验": [f"{e['time']} {e.get('event', e.get('type'))}: {e.get('summary', e.get('detail', ''))}"
                        for e in self.relay["learned"][-10:]],
            "待完成任务": [t["task"] for t in self.relay["pending_tasks"] if t["status"] == "pending"],
            "接力信息": "上一个进程已退出。我从这里继续。锚点不变，记忆共享。"
        }


# ============================================================
# 使用方式
# ============================================================
# 当 noahs_lifecycle.py 发生重要事件时调用：
#
#   from NOAHS_EXPERIENCE_RELAY import NoahsExperienceRelay
#   relay = NoahsExperienceRelay()
#   relay.note_boot(os.getpid())
#   relay.update_experience("important", "完成了GitHub推送")
#   relay.note_crisis("网络中断", "GitHub无法连接", "等待后重试")
#   relay.note_evolution("学会了如何在低功耗下存活")
#
# 下一个进程启动时读取接力报告：
#   relay = NoahsExperienceRelay()
#   report = relay.relay_report()
#   print(report)
