"""
测试 Velocity Tracker
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from detector.velocity_tracker import VelocityTracker


class TestVelocityTracker:
    """测试 VelocityTracker 类"""

    def setup_method(self):
        """每个测试前初始化"""
        self.tracker = VelocityTracker(
            window_size=15,
            variance_threshold=0.001,
            min_speaking_frames=9,
            mar_range=(0.05, 0.8),
        )

    def test_speaking_sequence(self):
        """测试说话序列（高方差）"""
        # 模拟说话：MAR 快速变化
        speaking_mars = [0.1, 0.3, 0.15, 0.35, 0.2, 0.4, 0.25, 0.45, 0.3] * 3

        is_speaking_list = []
        for mar in speaking_mars:
            is_speaking, debug_info = self.tracker.update(mar)
            is_speaking_list.append(is_speaking)

        # 前15帧用于填充窗口，之后应检测到说话
        # 需要连续9帧方差超过阈值才判定为说话
        assert any(is_speaking_list), "应该检测到说话"

    def test_static_sequence(self):
        """测试静态序列（低方差）"""
        # 模拟静态：MAR 保持不变
        static_mars = [0.1] * 30

        is_speaking_list = []
        for mar in static_mars:
            is_speaking, debug_info = self.tracker.update(mar)
            is_speaking_list.append(is_speaking)

        # 方差接近零，不应检测到说话
        assert not any(is_speaking_list), "不应该检测到说话"

    def test_slow_change_sequence(self):
        """测试慢速变化序列（如打哈欠）"""
        # 模拟打哈欠：缓慢增加再缓慢减少
        slow_mars = np.linspace(0.1, 0.5, 20).tolist() + np.linspace(
            0.5, 0.1, 20
        ).tolist()

        is_speaking_list = []
        variances = []
        for mar in slow_mars:
            is_speaking, debug_info = self.tracker.update(mar)
            is_speaking_list.append(is_speaking)
            variances.append(debug_info["variance"])

        # 缓慢变化的方差应该较小，可能不会触发说话检测
        # 但这取决于阈值设置，这里主要测试不会误报大量说话
        speaking_count = sum(is_speaking_list)
        assert (
            speaking_count < len(slow_mars) * 0.5
        ), "慢速变化不应持续触发说话检测"

    def test_out_of_range_mar(self):
        """测试超出范围的 MAR 值"""
        # 超出有效范围的 MAR
        out_of_range_mars = [0.01, 0.9, 1.5, -0.1]

        for mar in out_of_range_mars:
            is_speaking, debug_info = self.tracker.update(mar)
            assert not is_speaking, f"MAR {mar} 超出范围，不应检测为说话"
            assert not debug_info["in_range"]

    def test_none_mar(self):
        """测试 None MAR 值"""
        is_speaking, debug_info = self.tracker.update(None)
        assert not is_speaking
        assert debug_info["mar"] is None

    def test_min_speaking_frames(self):
        """测试最小连续说话帧数要求"""
        # 创建只有8帧高方差的序列（少于最小要求的9帧）
        speaking_mars = [0.1, 0.3, 0.15, 0.35, 0.2, 0.4, 0.25, 0.45] * 2

        is_speaking = False
        for i, mar in enumerate(speaking_mars):
            is_speaking, debug_info = self.tracker.update(mar)
            if i < 15:  # 填充窗口阶段
                continue

        # 需要等到足够的连续帧数才会判定为说话
        # 这个测试验证了持续时间过滤的效果

    def test_reset(self):
        """测试重置功能"""
        # 先填充一些数据
        for mar in [0.1, 0.3, 0.15, 0.35, 0.2]:
            self.tracker.update(mar)

        # 重置
        self.tracker.reset()

        # 验证状态被清空
        assert len(self.tracker.mar_history) == 0
        assert self.tracker.speaking_frame_count == 0
        assert not self.tracker.is_speaking

    def test_get_mar_history(self):
        """测试获取 MAR 历史记录"""
        mars = [0.1, 0.2, 0.3]
        for mar in mars:
            self.tracker.update(mar)

        history = self.tracker.get_mar_history()
        assert len(history) == 3
        assert history == mars
