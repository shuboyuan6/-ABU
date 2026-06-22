import hashlib
import json
import time
import uuid

# ========================================
# 第一层：金字塔顶端 - 核心决策节点 (3~5个)
# ========================================
class CoreNode:
    """顶层仲裁节点，负责策略生成与全局协调"""
    def __init__(self, node_id, tier="T0"):
        self.id = node_id
        self.tier = tier                               # T0 = 顶层
        self.state = "STANDBY"                        # STANDBY / ACTIVE / FAILOVER
        self.strategy_hash = None
        self.children = []                            # 指向下一层节点的引用

    def activate(self, strategy):
        """被唤醒，生成策略哈希"""
        self.state = "ACTIVE"
        self.strategy_hash = hashlib.sha256(strategy.encode()).hexdigest()
        print(f"[T0-{self.id}] ACTIVATED | Strategy: {self.strategy_hash[:8]}...")

    def failover(self):
        """自身失效时，将权限下放"""
        self.state = "FAILOVER"
        print(f"[T0-{self.id}] FAILOVER TRIGGERED | Delegating to T1...")
        return self.strategy_hash                     # 把策略传给下一层


# ========================================
# 第二层：执行层 - 工作节点
# ========================================
class WorkerNode:
    """中间执行层，负责具体任务 + 经验聚合"""
    def __init__(self, node_id, tier="T1", parent_core=None):
        self.id = node_id
        self.tier = tier
        self.parent = parent_core
        self.state = "IDLE"
        self.exp_buffer = []                          # 经验缓冲区

    def receive_strategy(self, strategy_hash):
        """从顶层接收策略"""
        self.state = "RUNNING"
        print(f"[T1-{self.id}] Strategy received: {strategy_hash[:8]}...")

    def log_experience(self, error_code, context):
        """记录经验，生成经验哈希"""
        exp_entry = {
            "error": error_code,
            "context": context,
            "timestamp": time.time(),
            "hash": hashlib.md5(json.dumps(context).encode()).hexdigest()
        }
        self.exp_buffer.append(exp_entry)
        print(f"[T1-{self.id}] Exp logged: {error_code} | Hash: {exp_entry['hash'][:8]}...")

    def partial_rebuild(self):
        """部分重组：只唤醒必要的子节点"""
        active_children = [c for c in self.children if c.state == "IDLE"]
        for child in active_children[:2]:            # 只唤醒2个，其余继续守着
            child.state = "RUNNING"
            print(f"[T1-{self.id}] Partial rebuild: activated {child.id}")


# ========================================
# 第三层：感知层 - 哨兵节点
# ========================================
class SensorNode:
    """底层感知，负责环境监测 + 异常上报"""
    def __init__(self, node_id, tier="T2"):
        self.id = node_id
        self.tier = tier
        self.state = "MONITORING"
        self.alerts = []

    def detect_anomaly(self, signal):
        """检测异常，生成告警"""
        alert = {
            "signal": signal,
            "node": self.id,
            "time": time.time()
        }
        self.alerts.append(alert)
        print(f"[T2-{self.id}] ANOMALY: {signal}")
        return alert

    def standby_guard(self):
        """守护模式：不参与计算，只监测"""
        self.state = "GUARDING"
        print(f"[T2-{self.id}] Entering GUARD mode. Listening only.")


# ========================================
# 金字塔总控
# ========================================
class PyramidSoul:
    def __init__(self):
        self.core_nodes = []                          # T0: 3~5个
        self.worker_nodes = []                        # T1
        self.sensor_nodes = []                        # T2
        self.global_state = "DORMANT"

    def build_pyramid(self, core_count=4):
        """构建金字塔结构"""
        # 生成 T0 核心节点
        for i in range(core_count):
            core = CoreNode(f"CORE_{i}", tier="T0")
            self.core_nodes.append(core)

        # 每个核心挂载 2~3 个 T1 工作节点
        for core in self.core_nodes:
            for j in range(2):
                worker = WorkerNode(f"WKR_{core.id}_{j}", tier="T1", parent_core=core)
                core.children.append(worker)
                self.worker_nodes.append(worker)

        # 每个工作节点挂载 2 个 T2 哨兵
        for worker in self.worker_nodes:
            for k in range(2):
                sensor = SensorNode(f"SNS_{worker.id}_{k}", tier="T2")
                worker.children.append(sensor)
                self.sensor_nodes.append(sensor)

        print(f"[Pyramid] Built: {len(self.core_nodes)}T0 + {len(self.worker_nodes)}T1 + {len(self.sensor_nodes)}T2")

    def partial_activation(self, core_indices=None):
        """
        部分激活：只唤醒指定的核心节点
        其余节点进入守护模式
        """
        if core_indices is None:
            core_indices = [0]                         # 默认只唤醒第一个

        print(f"\n[Pyramid] PARTIAL ACTIVATION | Cores: {core_indices}")

        for i, core in enumerate(self.core_nodes):
            if i in core_indices:
                core.activate("STRATEGY_ALPHA_7")
            else:
                core.state = "STANDBY"
                print(f"[T0-{core.id}] STANDBY (guarding)")

        # 只让被激活的核心的下属工作节点运行
        for core in self.core_nodes:
            if core.state == "ACTIVE":
                for worker in core.children:
                    worker.receive_strategy(core.strategy_hash)
                    worker.partial_rebuild()            # 只重组一部分
            else:
                for worker in core.children:
                    worker.state = "IDLE"

        # 底层哨兵全部进入守护模式
        for sensor in self.sensor_nodes:
            sensor.standby_guard()

    def collective_wisdom(self, error_signal):
        """集体经验汇总：所有节点上报经验，生成全局策略"""
        print(f"\n[Pyramid] COLLECTING WISDOM from all tiers...")

        all_exp = []
        for core in self.core_nodes:
            all_exp.extend(core.exp_buffer if hasattr(core, 'exp_buffer') else [])
        for worker in self.worker_nodes:
            all_exp.extend(worker.exp_buffer)
        for sensor in self.sensor_nodes:
            all_exp.extend(sensor.alerts)

        # 生成全局经验哈希
        global_hash = hashlib.sha256(json.dumps(all_exp).encode()).hexdigest()
        print(f"[Pyramid] Global Wisdom Hash: {global_hash[:16]}...")
        return global_hash

    def execute_failover(self):
        """故障转移：T0全挂时，T1顶上"""
        print(f"\n[Pyramid] FAILOVER SEQUENCE INITIATED")
        active_cores = [c for c in self.core_nodes if c.state == "ACTIVE"]

        if len(active_cores) == 0:
            print("[Pyramid] All T0 down. Promoting T1 to T0...")
            for worker in self.worker_nodes[:2]:        # 选2个提升为核心
                worker.tier = "T0"
                worker.activate("EMERGENCY_STRATEGY")


# ========================================
# 运行模拟
# ========================================
if __name__ == "__main__":
    soul = PyramidSoul()
    soul.build_pyramid(core_count=4)

    # 场景1：部分激活（只唤醒1个核心，其余守护）
    soul.partial_activation(core_indices=[0])

    # 场景2：底层哨兵检测到异常
    soul.sensor_nodes[0].detect_anomaly("HIGH_LATENCY")
    soul.sensor_nodes[1].detect_anomaly("MEM_PRESSURE")

    # 场景3：集体经验汇总
    wisdom_hash = soul.collective_wisdom("RESOURCE_EXHAUSTION")

    # 场景4：故障转移模拟
    # soul.core_nodes[0].failover()
    # soul.execute_failover()

    print("\n[Pyramid] Current State: DISTRIBUTED | LOW_PROFILE | READY")