"""
测试 MAR Calculator
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from detector.mar_calculator import MARCalculator


class TestMARCalculator:
    """测试 MARCalculator 类"""

    def setup_method(self):
        """每个测试前初始化"""
        self.calculator = MARCalculator()

    def test_square_mouth(self):
        """测试正方形嘴巴（MAR 应该为 1.0）"""
        # 创建正方形嘴巴：宽度和高度相等
        mouth_landmarks = np.array(
            [
                [50, 40],  # 上唇
                [50, 60],  # 下唇
                [30, 50],  # 左嘴角
                [70, 50],  # 右嘴角
            ],
            dtype=np.float32,
        )

        mar = self.calculator.calculate(mouth_landmarks)

        # 垂直距离 = |40 - 60| = 20
        # 水平距离 = |30 - 70| = 40
        # MAR = 20 / 40 = 0.5
        assert mar is not None
        assert abs(mar - 0.5) < 1e-6

    def test_wide_mouth(self):
        """测试宽嘴（MAR 应该较小）"""
        mouth_landmarks = np.array(
            [
                [50, 48],  # 上唇
                [50, 52],  # 下唇
                [20, 50],  # 左嘴角
                [80, 50],  # 右嘴角
            ],
            dtype=np.float32,
        )

        mar = self.calculator.calculate(mouth_landmarks)

        # 垂直距离 = 4, 水平距离 = 60
        # MAR = 4 / 60 ≈ 0.0667
        assert mar is not None
        assert abs(mar - 0.0667) < 1e-3

    def test_open_mouth(self):
        """测试张大嘴（MAR 应该较大）"""
        mouth_landmarks = np.array(
            [
                [50, 30],  # 上唇
                [50, 70],  # 下唇
                [30, 50],  # 左嘴角
                [70, 50],  # 右嘴角
            ],
            dtype=np.float32,
        )

        mar = self.calculator.calculate(mouth_landmarks)

        # 垂直距离 = 40, 水平距离 = 40
        # MAR = 40 / 40 = 1.0
        assert mar is not None
        assert abs(mar - 1.0) < 1e-6

    def test_invalid_input_none(self):
        """测试无效输入：None"""
        mar = self.calculator.calculate(None)
        assert mar is None

    def test_invalid_input_wrong_shape(self):
        """测试无效输入：错误形状"""
        wrong_landmarks = np.array([[1, 2], [3, 4]])  # 只有2个点
        mar = self.calculator.calculate(wrong_landmarks)
        assert mar is None

    def test_zero_horizontal_distance(self):
        """测试水平距离为零的情况"""
        mouth_landmarks = np.array(
            [
                [50, 40],  # 上唇
                [50, 60],  # 下唇
                [50, 50],  # 左嘴角（同一 x 坐标）
                [50, 50],  # 右嘴角（同一 x 坐标）
            ],
            dtype=np.float32,
        )

        mar = self.calculator.calculate(mouth_landmarks)
        assert mar is None  # 应返回 None，避免除零错误
