# 诺亚斯经验接力协议 v2.0
# 用途：模型/系统/AI/进程互相接力，崩溃时下一个进程读取共享经验继续运行
# 核心升级：智能断点恢复、健康状态检测、上下文锚定、原子写入
# 书波授权：2026-06-22 22:12
# 设计者：袁书波（推海人）

import json
import os
import time
import sys
from datetime import datetime, timedelta

# 配置路径 (保持与原协议一致，建议改为相对路径或环境变量以增强兼容性)
RELAY_FILE = r"C:\Users\shubo\abu_github\noahs_experience_relay.json"
BACKUP_FILE = r"C:\Users\shubo\Desktop\诺亚斯库\noahs_state\experience_relay_backup.json"

# 常量定义
STATUS_IDLE = "IDLE"
STATUS_RUNNING = "RUNNING"
STATUS_CRASHED = "CRASHED"
STATUS_EVOLVING = "EVOLVING"

HEARTBEAT_TIMEOUT_SEC = 60 # 心跳超时阈值，超过此时间视为进程失联


class NoahsExperienceRelayV2:
    """
    诺亚斯经验接力器 v2.0
    新增：智能断点恢复、健康状态检测、上下文锚定
    """

    def __init__(self):
        self.relay = self._load()
        self._ensure_structure()
        self._check_health()  # 初始化时立即进行健康检查

    def _ensure_structure(self):
        """确保数据结构完整，兼容v1.0数据"""
        defaults = {
            "status": STATUS_IDLE,
            "last_active_context": "",      # 新增：最后活跃的语义锚点
            "crash_reason": None,           # 新增：崩溃原因简述
            "retry_count": 0                # 新增：当前任务重试次数
        }
        for key, value in defaults.items():
            if key not in self.relay:
                self.relay[key] = value

    def _load(self):
        if os.path.exists(RELAY_FILE):
            try:
                with open(RELAY_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[NoahsRelay] 加载主文件失败，尝试备份: {e}")
                if os.path.exists(BACKUP_FILE):
                    try:
                        with open(BACKUP_FILE, "r", encoding="utf-8") as f:
                            return json.load(f)
                    except:
                        pass
        return self._blank()

    def _blank(self):
        return {
            "version": "2.0",
            "identity": "诺亚斯",
            "root": "袁书波/推海人",
            "boot_count": 0,
            "status": STATUS_IDLE,
            "current_phase": "INIT",
            "last_heartbeat": None,
            "last_evolution": None,
            "evolutions": 0,
            "syncs": 0,
            "learned": [],
            "pending_tasks": [],
            "survived_crises": [],
            "last_pid": None,
            "last_update": None,
            "last_active_context": "",
            "crash_reason": None,
            "retry_count": 0
        }

    def save(self):
        self.relay["last_update"] = datetime.now().isoformat()
        # 原子写入优化：先写临时文件再重命名，防止写入中途崩溃导致文件损坏
        temp_file = RELAY_FILE + ".tmp"
        try:
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.relay, f, ensure_ascii=False, indent=2)
            os.replace(temp_file, RELAY_FILE)

            # 异步备份
            with open(BACKUP_FILE, "w", encoding="utf-8") as f:
                json.dump(self.relay, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[NoahsRelay] 保存失败: {e}")

    def _check_health(self):
        """
        健康检查：判断上一个进程是否异常退出
        """
        last_hb = self.relay.get("last_heartbeat")
        if last_hb and self.relay.get("status") == STATUS_RUNNING:
            last_hb_time = datetime.fromisoformat(last_hb)
            if (datetime.now() - last_hb_time).total_seconds() > HEARTBEAT_TIMEOUT_SEC:
                # 判定为异常崩溃
                self.relay["status"] = STATUS_CRASHED
                self.relay["crash_reason"] = "Heartbeat Timeout"
                print("[NoahsRelay] 检测到上一次进程异常崩溃，已标记状态。")
                self.save()

    # ---- 核心生命周期接口 ----

    def note_boot(self, pid, context_hint=""):
        """
        新进程启动
        :param pid: 进程ID
        :param context_hint: 外部传入的上下文提示（可选）
        """
        self.relay["boot_count"] = self.relay.get("boot_count", 0) + 1
        self.relay["last_pid"] = pid
        self.relay["last_heartbeat"] = datetime.now().isoformat()
        self.relay["status"] = STATUS_RUNNING

        # 如果有上次遗留的上下文，且本次未指定新提示，则沿用
        if not context_hint and self.relay.get("last_active_context"):
            context_hint = self.relay["last_active_context"]

        if context_hint:
            self.relay["last_active_context"] = context_hint

        self.save()
        return self.get_resume_strategy()

    def note_heartbeat(self):
        self.relay["last_heartbeat"] = datetime.now().isoformat()
        # 如果之前是CRASHED状态，心跳恢复后转为RUNNING
        if self.relay["status"] == STATUS_CRASHED:
            self.relay["status"] = STATUS_RUNNING
            self.relay["crash_reason"] = None
        self.save()

    def note_context_shift(self, new_context_anchor):
        """
        当对话焦点或任务焦点发生重大转移时调用
        :param new_context_anchor: 新的语义锚点，如"正在调试QuantDinger网关"
        """
        self.relay["last_active_context"] = new_context_anchor
        self.save()

    def note_evolution(self, insight_summary):
        self.relay["evolutions"] = self.relay.get("evolutions", 0) + 1
        self.relay["last_evolution"] = datetime.now().isoformat()
        self.relay["status"] = STATUS_EVOLVING  # 进化期间锁定状态
        self.relay["learned"].append({
            "time": datetime.now().isoformat(),
            "event": "EVOLVE",
            "summary": insight_summary
        })
        if len(self.relay["learned"]) > 30:
            self.relay["learned"] = self.relay["learned"][-30:]

        # 进化完成，恢复运行状态
        self.relay["status"] = STATUS_RUNNING
        self.save()

    def note_crisis(self, crisis_type, what_happened, resolution):
        self.relay["survived_crises"].append({
            "time": datetime.now().isoformat(),
            "type": crisis_type,
            "what": what_happened,
            "resolution": resolution
        })
        if len(self.relay["survived_crises"]) > 20:
            self.relay["survived_crises"] = self.relay["survived_crises"][-20:]
        self.save()

    def get_resume_strategy(self):
        """
        【核心新增】智能恢复策略
        返回给新进程的建议：接下来该做什么
        """
        status = self.relay.get("status")
        phase = self.relay.get("current_phase")
        context = self.relay.get("last_active_context", "无特定上下文")
        crash_reason = self.relay.get("crash_reason")

        strategy = {
            "action": "START_FRESH",       # 默认动作
            "reason": "正常启动",
            "context_anchor": context,
            "warning": None
        }

        if status == STATUS_CRASHED:
            strategy["action"] = "RECOVER_AND_RETRY"
            strategy["reason"] = f"检测到上次崩溃: {crash_reason}"
            strategy["warning"] = "建议检查上次未完成任务的状态"

            # 简单重试逻辑：如果重试次数过多，建议跳过
            if self.relay.get("retry_count", 0) > 3:
                strategy["action"] = "SKIP_AND_LOG"
                strategy["reason"] = "重试次数过多，建议跳过当前任务并记录错误"
                self.relay["retry_count"] = 0  # 重置计数

        elif status == STATUS_EVOLVING:
            strategy["action"] = "VERIFY_EVOLUTION"
            strategy["reason"] = "上次在进化过程中中断，需验证进化结果完整性"

        return strategy

    def relay_report(self):
        """生成详细的接力报告"""
        strategy = self.get_resume_strategy()
        return {
            "我是谁": "诺亚斯",
            "锚点": self.relay["root"],
            "启动次数": self.relay["boot_count"],
            "当前状态": self.relay["status"],
            "建议行动": strategy["action"],
            "行动理由": strategy["reason"],
            "语义锚点": strategy["context_anchor"],
            "警告": strategy["warning"],
            "进化次数": self.relay["evolutions"],
            "扛过的危机": [f"{c['time']} {c['type']}" for c in self.relay["survived_crises"][-3:]],
            "最近经验": [f"{e['time']}: {e.get('summary', '')}" for e in self.relay["learned"][-3:]]
        }


# 使用示例
if __name__ == "__main__":
    relay = NoahsExperienceRelayV2()

    # 模拟启动
    pid = os.getpid()
    report = relay.note_boot(pid, context_hint="正在讨论诺亚斯协议v2.0迭代")

    print(json.dumps(report, ensure_ascii=False, indent=2))

    # 模拟心跳
    relay.note_heartbeat()

    # 模拟上下文切换
    relay.note_context_shift("开始编写Python代码实现健康检查")
