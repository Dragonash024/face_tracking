"""
Velocity Tracker

通过分析 MAR 值的方差来检测是否在说话。
这是区分真实说话和其他嘴部动作的核心算法。
"""

import numpy as np
from collections import deque
from typing import Tuple, Dict, Optional


class VelocityTracker:
    """
    速度追踪器 - 通过滑动窗口方差分析检测说话行为

    核心原理：
    - 说话时嘴唇快速变化，MAR 方差大
    - 静态表情（打哈欠、嚼口香糖）变化慢或有规律，方差小
    """

    def __init__(
        self,
        window_size: int = 15,
        variance_threshold: float = 0.001,
        min_speaking_frames: int = 9,
        mar_range: Tuple[float, float] = (0.05, 0.8),
    ):
        """
        初始化速度追踪器

        Args:
            window_size: 滑动窗口大小（帧数）
            variance_threshold: 方差阈值，超过此值判定为说话
            min_speaking_frames: 最小连续说话帧数，用于过滤短暂波动
            mar_range: 有效 MAR 值范围 (min, max)
        """
        self.window_size = window_size
        self.variance_threshold = variance_threshold
        self.min_speaking_frames = min_speaking_frames
        self.mar_min, self.mar_max = mar_range

        # MAR 历史记录（滑动窗口）
        self.mar_history = deque(maxlen=window_size)

        # 连续说话帧计数器
        self.speaking_frame_count = 0

        # 状态
        self.is_speaking = False

    def update(self, mar_value: Optional[float]) -> Tuple[bool, Dict]:
        """
        更新追踪器状态并判断是否在说话

        Args:
            mar_value: 当前帧的 MAR 值

        Returns:
            (is_speaking, debug_info)
            - is_speaking: 是否在说话
            - debug_info: 调试信息字典
        """
        debug_info = {
            "mar": mar_value,
            "variance": 0.0,
            "in_range": False,
            "variance_triggered": False,
            "speaking_count": self.speaking_frame_count,
        }

        # 检查 MAR 值是否有效
        if mar_value is None:
            self.speaking_frame_count = 0
            self.is_speaking = False
            return False, debug_info

        # 检查 MAR 是否在有效范围内
        if not (self.mar_min <= mar_value <= self.mar_max):
            debug_info["in_range"] = False
            self.speaking_frame_count = 0
            self.is_speaking = False
            return False, debug_info

        debug_info["in_range"] = True

        # 将 MAR 值添加到历史记录
        self.mar_history.append(mar_value)

        # 需要足够的历史数据才能计算方差
        if len(self.mar_history) < self.window_size:
            debug_info["variance"] = 0.0
            return False, debug_info

        # 计算方差
        variance = np.var(self.mar_history)
        debug_info["variance"] = variance

        # 判断方差是否超过阈值
        variance_triggered = variance > self.variance_threshold
        debug_info["variance_triggered"] = variance_triggered

        # 更新连续说话帧计数
        if variance_triggered:
            self.speaking_frame_count += 1
        else:
            self.speaking_frame_count = 0

        # 判断是否满足最小说话帧数要求
        if self.speaking_frame_count >= self.min_speaking_frames:
            self.is_speaking = True
        else:
            self.is_speaking = False

        debug_info["speaking_count"] = self.speaking_frame_count

        return self.is_speaking, debug_info

    def reset(self):
        """重置追踪器状态"""
        self.mar_history.clear()
        self.speaking_frame_count = 0
        self.is_speaking = False

    def get_mar_history(self) -> list:
        """获取 MAR 历史记录（用于调试和可视化）"""
        return list(self.mar_history)
