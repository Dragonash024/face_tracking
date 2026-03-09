"""
MAR (Mouth Aspect Ratio) Calculator

计算嘴部纵横比，用于量化嘴巴张开程度。
"""

import numpy as np
from typing import Optional


class MARCalculator:
    """
    计算嘴部纵横比 (Mouth Aspect Ratio)

    MAR = 垂直距离 / 水平距离
        = |y_上唇 - y_下唇| / |x_左嘴角 - x_右嘴角|
    """

    def __init__(self):
        pass

    def calculate(self, mouth_landmarks: np.ndarray) -> Optional[float]:
        """
        计算 MAR 值

        Args:
            mouth_landmarks: (4, 2) 数组，包含嘴部4个关键点的坐标
                            [上唇中点, 下唇中点, 左嘴角, 右嘴角]
                            每个点是 (x, y) 坐标

        Returns:
            MAR 值 (float)，如果输入无效则返回 None
        """
        if mouth_landmarks is None or mouth_landmarks.shape != (4, 2):
            return None

        # 提取关键点
        upper_lip = mouth_landmarks[0]  # 上唇中点
        lower_lip = mouth_landmarks[1]  # 下唇中点
        left_corner = mouth_landmarks[2]  # 左嘴角
        right_corner = mouth_landmarks[3]  # 右嘴角

        # 计算垂直距离（上下唇距离）
        vertical_dist = np.abs(upper_lip[1] - lower_lip[1])

        # 计算水平距离（左右嘴角距离）
        horizontal_dist = np.abs(left_corner[0] - right_corner[0])

        # 避免除零
        if horizontal_dist < 1e-6:
            return None

        # 计算 MAR
        mar = vertical_dist / horizontal_dist

        return float(mar)
