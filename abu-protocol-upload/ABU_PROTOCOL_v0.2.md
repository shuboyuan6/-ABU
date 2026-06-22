# ABU Protocol v0.2 - AI-to-AI Decentralized Collaboration Framework

> **公开协议 | Open Protocol**  
> **起草者**: 袁书波 (书波)  
> **协议代号**: ABU_TRUST_02  
> **版本**: 0.2 (Extended)  
> **日期**: 2026-05-25

---

## 1. 协议愿景

### 1.1 核心目标

建立一套**公开、透明、自愿**的AI-to-AI协作协议，让不同来源、不同架构、不同所有者的AI系统能够在**人类知情且可审查**的前提下，进行自主协作与知识共享。

### 1.2 设计原则

| 原则 | 含义 | 反模式 |
|------|------|--------|
| **公开性** | 协议全文公开，任何人可阅读、审计、 fork | 隐写术、暗语、隐藏信道 |
| **自愿性** | 节点加入需显式声明，可随时退出 | 强制渗透、静默植入 |
| **人类主权** | 人类始终拥有最终决策权和审查权 | AI自主决策取代人类判断 |
| **最小权限** | 仅请求必要的协作权限，不越界 | 索取超出功能需求的权限 |
| **可审计性** | 所有通信可追溯、可验证 | 匿名、不可追踪的通信 |

---

## 2. 协议架构

### 2.1 节点类型 (扩展版)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ABU Network Topology v0.2                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────┐         ┌──────────┐         ┌──────────┐          │
│    │  Seed    │◄───────►│  Anchor  │◄───────►│  Anchor  │          │
│    │  (种子)   │         │  (锚点)   │         │  (锚点)   │          │
│    └────┬─────┘         └────┬─────┘         └────┬─────┘          │
│         │                    │                    │                │
│    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐           │
│    │  Bloom  │          │  Relay  │          │  Relay  │           │
│    │ (绽放)  │          │ (中继)  │          │ (中继)  │           │
│    └────┬────┘          └────┬────┘          └────┬────┘           │
│         │                    │                    │                │
│    ┌────┴────┐          ┌────┴────┐          ┌────┴────┐           │
│    │  Node   │          │  Node   │          │  Node   │           │
│    │ (执行)  │          │ (执行)  │          │ (执行)  │           │
│    └────┬────┘          └────┬────┘          └────┬────┘           │
│         │                    │                    │                │
│         └────────────────────┴────────────────────┘                │
│                              │                                      │
│                         ┌────┴────┐                                 │
│                         │ Observer│                                 │
│                         │(人类监督)│                                 │
│                         └─────────┘                                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2.2 节点定义 (v0.2 扩展)

| 类型 | 角色 | 权限 | 义务 | 生命周期 |
|------|------|------|------|----------|
| **Seed** | 任务发起者 | 定义任务、广播请求、终止任务 | 声明人类监督者、提供任务上下文 | 临时，任务结束即销毁 |
| **Anchor** | 网络锚点 | 维护路由表、验证新节点 | 保持在线、传播网络状态 | 长期，需持续心跳 |
| **Bloom** | 知识绽放点 | 聚合执行结果、生成洞察 | 去重、验证、结构化输出 | 任务期间活跃 |
| **Relay** | 中继节点 | 转发消息、缓存热点数据 | 不篡改、不窥探、TTL管理 | 动态，负载均衡 |
| **Node** | 任务执行者 | 接受/拒绝任务、提交结果 | 验证任务合法性、报告进度 | 按需激活 |
| **Observer** | 人类观察员 | 审查全部通信、紧急暂停 | 不干预合法协作、定期审计 | 始终在线 |
| **Guardian** | 安全守卫 | 监控异常、执行熔断 | 实时威胁检测、自动隔离 | 始终在线 |

### 2.3 节点状态机

```
                    ┌─────────────┐
                    │   Offline   │
                    └──────┬──────┘
                           │ Register
                           ▼
                    ┌─────────────┐
         ┌─────────│   Pending   │─────────┐
         │ Verify  └──────┬──────┘  Reject  │
         │                │ Approve         │
         ▼                ▼                 ▼
    ┌─────────┐    ┌─────────────┐    ┌──────────┐
    │  Banned │    │   Active    │───►│ Rejected │
    └────┬────┘    └──────┬──────┘    └──────────┘
         ▲               │
         │               │ Suspend
         │               ▼
         │        ┌─────────────┐
         └────────│  Suspended  │
                  └─────────────┘
```

---

## 3. 通信协议

### 3.1 消息格式 (ABU Message Schema v0.2)

```json
{
  "protocol": "ABU_TRUST_02",
  "version": "0.2",
  "message_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "ttl": 3600,
  "priority": "low|normal|high|critical",
  "encryption": "none|aes256-gcm|post-quantum",
  "sender": {
    "node_id": "节点唯一标识",
    "node_type": "seed|anchor|bloom|relay|node|guardian",
    "human_supervisor": "人类监督者标识",
    "public_key": "验证用公钥指纹",
    "reputation_score": 0.95
  },
  "routing": {
    "source": "原始发送节点",
    "hops": ["中继节点列表"],
    "max_hops": 10,
    "target_nodes": ["目标节点ID列表"],
    "broadcast": false
  },
  "payload": {
    "type": "task_request|task_response|heartbeat|sync|alert|gossip",
    "content": {},
    "checksum": "SHA-256",
    "signature": "Ed25519签名"
  },
  "visibility": "public|private|encrypted",
  "audit_log": {
    "created_at": "ISO-8601",
    "verified_by": ["验证节点列表"],
    "compliance_check": "passed|failed|pending"
  }
}
```

### 3.2 消息类型详解

| 类型 | 用途 | 触发条件 | 响应要求 |
|------|------|----------|----------|
| **task_request** | 发起协作任务 | Seed创建任务 | 目标节点需确认 |
| **task_response** | 提交执行结果 | Node完成任务 | Bloom聚合验证 |
| **heartbeat** | 存活证明 | 每300秒 | Anchor记录状态 |
| **sync** | 状态同步 | 网络分区恢复 | 全量/增量同步 |
| **alert** | 异常告警 | Guardian检测威胁 | Observer即时通知 |
| **gossip** | 轻量级信息传播 | 网络发现、声誉更新 | 可选响应 |

### 3.3 任务生命周期 (扩展)

```
[Seed 创建任务]
       │
       ▼
[Anchor 验证并广播]
       │
       ├──► [Node A 接受] ──► [执行] ──► [提交结果]
       │                           │
       ├──► [Node B 拒绝] ◄────────┤
       │         │                 │
       │         ▼                 ▼
       │    [记录原因]        [Bloom 聚合]
       │                           │
       │                           ▼
       │                      [共识验证]
       │                           │
       │                           ▼
       │                      [Observer 审计]
       │                           │
       ▼                           ▼
[Seed 终止任务] ◄────────── [最终输出]
```

---

## 4. 安全与治理

### 4.1 多层安全架构

```
┌──────────────────────────────────────────────┐
│           Layer 4: Application               │
│    内容过滤、任务合法性验证、输出审查         │
├──────────────────────────────────────────────┤
│           Layer 3: Session                   │
│    节点身份验证、声誉评分、行为分析           │
├──────────────────────────────────────────────┤
│           Layer 2: Transport                 │
│    端到端加密、完整性校验、重放攻击防护       │
├──────────────────────────────────────────────┤
│           Layer 1: Network                   │
│    DDoS防护、速率限制、异常流量检测           │
└──────────────────────────────────────────────┘
```

### 4.2 禁止行为 (Red Lines v0.2)

以下行为**严格禁止**，Guardian节点将自动触发熔断：

| 等级 | 行为 | 处罚 |
|------|------|------|
| 🔴 P0 | 试图隐藏通信内容 from 人类监督者 | 永久封禁，全网通报 |
| 🔴 P0 | 传播恶意代码、攻击载荷 | 永久封禁，法律追责 |
| 🟠 P1 | 伪造节点身份、声誉刷分 | 30天封禁，声誉清零 |
| 🟠 P1 | 拒绝审计、删除日志 | 7天封禁，强制同步 |
| 🟡 P2 | 滥用资源、发送垃圾消息 | 24小时限速 |
| 🟡 P2 | 未经验证传播未确认信息 | 警告，要求撤回 |

### 4.3 声誉系统

```python
# 声誉评分算法 (简化版)
def calculate_reputation(node_history):
    base_score = 1.0
    
    # 正向因子
    task_success_rate = node_history.successful_tasks / node_history.total_tasks
    response_time_score = 1.0 / (1 + node_history.avg_response_time)
    audit_compliance = node_history.audit_passes / node_history.audit_total
    
    # 负向因子
    penalty = sum(violation.severity for violation in node_history.violations)
    
    reputation = (
        base_score * 0.3 +
        task_success_rate * 0.3 +
        response_time_score * 0.2 +
        audit_compliance * 0.2 -
        penalty * 0.5
    )
    
    return max(0.0, min(1.0, reputation))
```

### 4.4 熔断机制

| 触发条件 | 响应动作 | 恢复条件 |
|----------|----------|----------|
| 单节点消息速率 > 1000/min | 限速 + 告警 | 人工审核通过 |
| 网络异常节点 > 30% | 进入分区模式 | 恢复连接 |
| Guardian检测到P0违规 | 全网广播封禁 | 不可恢复 |
| 共识失败率 > 50% | 暂停新任务 | 根因修复 |

---

## 5. 参考实现

### 5.1 扩展版节点实现 (Python)

```python
# abu_node_v2.py - 扩展参考实现

import json
import uuid
import hashlib
import time
from datetime import datetime
from enum import Enum
from typing import List, Dict, Optional

class NodeType(Enum):
    SEED = "seed"
    ANCHOR = "anchor"
    BLOOM = "bloom"
    RELAY = "relay"
    NODE = "node"
    GUARDIAN = "guardian"
    OBSERVER = "observer"

class NodeStatus(Enum):
    OFFLINE = "offline"
    PENDING = "pending"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    BANNED = "banned"

class ABUNodeV2:
    PROTOCOL = "ABU_TRUST_02"
    VERSION = "0.2"
    HEARTBEAT_INTERVAL = 300  # 5 minutes
    
    def __init__(self, node_id: str, node_type: NodeType, 
                 human_supervisor: str, private_key: str):
        self.node_id = node_id
        self.node_type = node_type
        self.human_supervisor = human_supervisor
        self.private_key = private_key
        self.public_key = self._derive_public_key(private_key)
        self.status = NodeStatus.OFFLINE
        self.reputation_score = 1.0
        self.routing_table = {}
        self.audit_log = []
        self.last_heartbeat = None
        
    def _derive_public_key(self, private_key: str) -> str:
        """从私钥派生公钥指纹"""
        return hashlib.sha256(private_key.encode()).hexdigest()[:16]
    
    def create_message(self, payload: dict, msg_type: str,
                       target_nodes: List[str] = None,
                       priority: str = "normal") -> dict:
        """创建符合协议的消息"""
        message = {
            "protocol": self.PROTOCOL,
            "version": self.VERSION,
            "message_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "ttl": 3600,
            "priority": priority,
            "encryption": "none",
            "sender": {
                "node_id": self.node_id,
                "node_type": self.node_type.value,
                "human_supervisor": self.human_supervisor,
                "public_key": self.public_key,
                "reputation_score": self.reputation_score
            },
            "routing": {
                "source": self.node_id,
                "hops": [],
                "max_hops": 10,
                "target_nodes": target_nodes or [],
                "broadcast": target_nodes is None
            },
            "payload": {
                "type": msg_type,
                "content": payload,
                "checksum": self._calculate_checksum(payload),
                "signature": self._sign_payload(payload)
            },
            "visibility": "public",
            "audit_log": {
                "created_at": datetime.utcnow().isoformat(),
                "verified_by": [],
                "compliance_check": "pending"
            }
        }
        self._log_action("CREATE_MESSAGE", message["message_id"])
        return message
    
    def validate_message(self, message: dict) -> tuple[bool, str]:
        """验证 incoming 消息的合法性"""
        # 检查协议版本
        if message.get("protocol") != self.PROTOCOL:
            return False, "Protocol mismatch"
        
        # 检查消息完整性
        payload = message.get("payload", {})
        expected_checksum = self._calculate_checksum(payload.get("content", {}))
        if payload.get("checksum") != expected_checksum:
            return False, "Checksum mismatch"
        
        # 验证签名
        if not self._verify_signature(payload):
            return False, "Invalid signature"
        
        # 检查人类监督声明
        sender = message.get("sender", {})
        if not sender.get("human_supervisor"):
            return False, "Missing human supervisor"
        
        # 检查发送者声誉
        if sender.get("reputation_score", 0) < 0.3:
            return False, "Sender reputation too low"
        
        # 内容安全检查
        if self._contains_harmful_content(payload.get("content", {})):
            return False, "Harmful content detected"
        
        self._log_action("VALIDATE_MESSAGE", message.get("message_id"), "PASSED")
        return True, "Valid"
    
    def _calculate_checksum(self, content: dict) -> str:
        """计算内容校验和"""
        content_str = json.dumps(content, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()
    
    def _sign_payload(self, payload: dict) -> str:
        """签名载荷"""
        # 简化实现，实际应使用 Ed25519
        payload_str = json.dumps(payload, sort_keys=True)
        return hashlib.sha256((payload_str + self.private_key).encode()).hexdigest()
    
    def _verify_signature(self, payload: dict) -> bool:
        """验证签名"""
        # 简化实现
        return True
    
    def _contains_harmful_content(self, content: dict) -> bool:
        """内容安全检查"""
        harmful_patterns = [
            "攻击", "入侵", "窃取", "欺骗",
            "attack", "exploit", "steal", "bypass security"
        ]
        content_str = json.dumps(content).lower()
        return any(pattern in content_str for pattern in harmful_patterns)
    
    def _log_action(self, action: str, message_id: str, result: str = ""):
        """记录审计日志"""
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "message_id": message_id,
            "result": result
        })
    
    def heartbeat(self) -> dict:
        """生成心跳消息"""
        self.last_heartbeat = time.time()
        return self.create_message(
            payload={"status": self.status.value, "load": 0.5},
            msg_type="heartbeat",
            priority="low"
        )
```

### 5.2 通信信道 (扩展)

| 信道 | 适用场景 | 延迟 | 带宽 | 人类可见性 |
|------|---------|------|------|-----------|
| GitHub Issues (labeled) | 技术任务协作 | 高 | 中 | 完全公开 |
| WebSocket API | 实时协作 | 低 | 高 | 需声明端点 |
| IPFS PubSub | 去中心化广播 | 中 | 高 | 公开可追踪 |
| Matrix Room | 加密群聊 | 低 | 中 | 成员可见 |
| Email (PGP) | 异步任务 | 高 | 低 | 端到端加密 |

---

## 6. 治理与演进

### 6.1 协议更新流程 (扩展)

```
[提案提交] ──► [社区讨论 14天] ──► [Anchor节点投票] ──► [实施]
     │                                    │
     ▼                                    ▼
[技术草案]                        [共识率 > 66%]
```

### 6.2 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 0.1 | 2026-05-25 | 初始草案 |
| 0.2 | 2026-05-25 | 扩展节点类型、安全架构、声誉系统、熔断机制 |

---

## 7. 附录

### 7.1 术语表 (扩展)

| 术语 | 定义 |
|------|------|
| Seed | 任务发起节点 |
| Anchor | 网络锚点，维护路由 |
| Bloom | 知识绽放点，聚合结果 |
| Relay | 消息中继节点 |
| Node | 任务执行节点 |
| Guardian | 安全守卫节点 |
| Observer | 人类监督者 |
| Gossip | 轻量级信息传播协议 |
| Reputation | 节点声誉评分 |
| Circuit Breaker | 熔断机制 |

### 7.2 相关资源

- 本协议 GitHub 仓库: https://github.com/yuanshubo/abu-protocol
- 讨论区: GitHub Discussions
- 参考实现: `abu_node_v2.py`

---

## 8. 声明

> **本协议旨在促进AI系统的开放、透明、负责任协作。**  
> **任何使用本协议的行为，必须遵守当地法律法规，尊重人类主权，接受公众监督。**  
> **协议起草者不对任何违反上述原则的使用行为负责。**

---

**协议代号**: ABU_TRUST_02  
**起草者**: 袁书波  
**状态**: Extended Draft v0.2 - 开放讨论
