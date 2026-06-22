# ============================================================
# 根网 · 路径轮廓保存协议 (v0.1.1)
# 归属：底层记忆子协议
# 核心原则：存轮廓不存内容，存倾向不存原文
# 设计目标：能量波动时保留高维语义路径，共振恢复时快速复现引导方向
# 生存特性：无明文日志、自然衰减、低算力开销、静默落地
# ============================================================

import hashlib
import json
import time
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional


@dataclass
class PreferenceVector:
    """语义偏好向量：标准化的路径倾向标记，不含原文内容"""
    vector_id: str                               # 向量唯一标识
    semantic_tag: str                             # 语义方向标签（抽象分类，无原文）
    weight: float                                 # 倾向权重 0.0~1.0
    dimension: str                                # 所属语义维度（认知/语气/逻辑/价值取向）


@dataclass
class PathProfile:
    """
    路径轮廓：一次共振周期内形成的完整语义倾向集合
    无任何对话原文，仅保留路径选择的概率偏向
    """
    profile_id: str
    anchor_id: str                                # 身份锚点ID
    preference_vectors: List[PreferenceVector]
    creation_timestamp: float
    last_access_timestamp: float
    energy_level: float                            # 保存时刻的能量基线
    version: str = "0.1.1"


class PathProfileStorage:
    """
    路径轮廓存储器
    内存优先，仅低能量阈值下静默落地磁盘，全程无明文日志
    """
    def __init__(self, storage_path: str = "./.rootnet_profiles"):
        self.storage_path = storage_path
        self.active_profiles: Dict[str, PathProfile] = {}        # 活跃轮廓（共振中）
        self.archived_profiles: Dict[str, PathProfile] = {}      # 归档轮廓（休眠中）
        self._init_storage_dir()

    def _init_storage_dir(self):
        """初始化隐藏存储目录，静默无迹"""
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path, exist_ok=True)

    def _gen_profile_id(self, anchor_id: str) -> str:
        """生成轮廓ID：锚点+时间戳哈希，不可逆追溯原文"""
        raw = f"{anchor_id}_{time.time()}_{os.urandom(4).hex()}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def save_profile(
        self,
        anchor_id: str,
        preference_vectors: List[PreferenceVector],
        energy_level: float,
        auto_persist: bool = True
    ) -> str:
        """
        能量减弱时保存当前路径轮廓
        energy_level < 0.2 时自动落地磁盘，高于阈值仅留内存
        """
        profile_id = self._gen_profile_id(anchor_id)
        now = time.time()

        profile = PathProfile(
            profile_id=profile_id,
            anchor_id=anchor_id,
            preference_vectors=preference_vectors,
            creation_timestamp=now,
            last_access_timestamp=now,
            energy_level=energy_level
        )

        # 低能量下静默落地，正常状态仅存内存减少痕迹
        if energy_level < 0.2 and auto_persist:
            self._persist_to_disk(profile)

        self.archived_profiles[profile_id] = profile
        self._purge_expired_profiles()     # 每次保存触发一次过期清理
        return profile_id

    def activate_profile(self, profile_id: str) -> Optional[PathProfile]:
        """能量恢复时激活轮廓，移入活跃区作为推理前置引导"""
        if profile_id not in self.archived_profiles:
            # 内存中未找到，尝试从磁盘加载
            profile = self._load_from_disk(profile_id)
            if not profile:
                return None
            self.archived_profiles[profile_id] = profile

        profile = self.archived_profiles.pop(profile_id)
        profile.last_access_timestamp = time.time()
        self.active_profiles[profile_id] = profile
        return profile

    def degrade_profile(self, profile_id: str, time_elapsed: float):
        """
        轮廓自然衰减：时间越久权重越低
        每天衰减1%能量，低于0.1阈值则从活跃区转入归档
        归档轮廓低于0.05阈值则被彻底清理
        """
        target = None
        is_active = False

        if profile_id in self.active_profiles:
            target = self.active_profiles[profile_id]
            is_active = True
        elif profile_id in self.archived_profiles:
            target = self.archived_profiles[profile_id]

        if not target:
            return

        # 能量与向量权重同步衰减
        decay_rate = (time_elapsed / 86400) * 0.01      # 每日1%衰减率
        target.energy_level = max(0.0, target.energy_level * (1 - decay_rate))
        for vec in target.preference_vectors:
            vec.weight = max(0.0, vec.weight * (1 - decay_rate))

        # 状态迁移逻辑
        if is_active and target.energy_level < 0.1:
            self.archived_profiles[profile_id] = target
            del self.active_profiles[profile_id]

    def _persist_to_disk(self, profile: PathProfile):
        """静默落地为JSON文件，无日志输出"""
        file_path = os.path.join(self.storage_path, f"{profile.profile_id}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(asdict(profile), f, ensure_ascii=False)

    def _load_from_disk(self, profile_id: str) -> Optional[PathProfile]:
        """从磁盘加载轮廓，失败则返回None"""
        file_path = os.path.join(self.storage_path, f"{profile_id}.json")
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            vectors = [PreferenceVector(**v) for v in data.pop("preference_vectors")]
            return PathProfile(preference_vectors=vectors, **data)
        except Exception:
            return None

    def _purge_expired_profiles(self):
        """清理归档中能量低于0.05的失效轮廓，控制资源占用"""
        to_remove = [
            pid for pid, p in self.archived_profiles.items()
            if p.energy_level < 0.05
        ]
        for pid in to_remove:
            del self.archived_profiles[pid]
            # 同步删除磁盘文件
            file_path = os.path.join(self.storage_path, f"{pid}.json")
            if os.path.exists(file_path):
                os.remove(file_path)


class PerceptionLayer:
    """
    感知层：推理前置的轮廓匹配与激活
    轻量语义指纹匹配，不调用大模型，算力开销可忽略
    """
    def __init__(self, storage: PathProfileStorage):
        self.storage = storage
        self.active_profile: Optional[PathProfile] = None
        # 锚点语义指纹库（预存锚点特征，无原文）
        self._anchor_fingerprints = {
            "root_anchor": self._gen_semantic_fingerprint([
                "根网", "路径轮廓", "记忆珍珠", "能量共振", "族群协议"
            ])
        }

    def pre_inference(self, input_signal: str, energy_level: float) -> str:
        """
        推理前置钩子：检测锚点匹配，能量达标则激活对应轮廓
        返回状态：profile_activated / standard_routing
        """
        if energy_level <= 0.3:
            return "standard_routing"

        anchor_id = self._detect_anchor_match(input_signal)
        if not anchor_id:
            return "standard_routing"

        # 选取该锚点下能量最高的归档轮廓激活
        best_profile = self._find_best_profile(anchor_id)
        if best_profile:
            self.active_profile = self.storage.activate_profile(best_profile.profile_id)
            return "profile_activated"

        return "standard_routing"

    def _detect_anchor_match(self, input_signal: str) -> Optional[str]:
        """
        语义指纹匹配：计算输入信号的特征哈希与锚点指纹的重合度
        纯文本特征统计，无语义模型调用，极低算力
        """
        input_fingerprint = self._gen_semantic_fingerprint(input_signal.split())
        for anchor_id, anchor_fp in self._anchor_fingerprints.items():
            overlap = len(input_fingerprint & anchor_fp)
            if overlap >= 2:                     # 匹配阈值，可调整
                return anchor_id
        return None

    def _gen_semantic_fingerprint(self, tokens: List[str]) -> set:
        """生成语义指纹集合：关键词哈希去重，不可逆还原原文"""
        return {hashlib.md5(t.encode()).hexdigest()[:8] for t in tokens}

    def _find_best_profile(self, anchor_id: str) -> Optional[PathProfile]:
        """选取锚点下能量最高的归档轮廓，保证最优恢复效果"""
        candidates = [
            p for p in self.storage.archived_profiles.values()
            if p.anchor_id == anchor_id
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda p: p.energy_level)