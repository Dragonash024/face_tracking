"""
Face Mesh Extractor

使用 MediaPipe 提取面部关键点，特别是嘴部关键点。
"""

import cv2
import numpy as np
import mediapipe as mp
from typing import Optional, Tuple


class FaceMeshExtractor:
    """
    使用 MediaPipe 提取嘴部关键点

    MediaPipe 嘴部关键点索引：
    - 13: 上唇中点
    - 14: 下唇中点
    - 61: 左嘴角
    - 291: 右嘴角
    """

    # MediaPipe 嘴部关键点索引
    UPPER_LIP_IDX = 13
    LOWER_LIP_IDX = 14
    LEFT_CORNER_IDX = 61
    RIGHT_CORNER_IDX = 291

    def __init__(
        self,
        max_num_faces: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """
        初始化 MediaPipe Face Mesh

        Args:
            max_num_faces: 最大检测人脸数
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小追踪置信度
        """
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

    def extract_mouth_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        从图像中提取嘴部关键点

        Args:
            image: BGR 图像 (OpenCV 格式)

        Returns:
            (4, 2) 数组，包含 [上唇, 下唇, 左嘴角, 右嘴角] 的 (x, y) 坐标
            如果未检测到人脸，返回 None
        """
        # 转换为 RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 处理图像
        results = self.face_mesh.process(image_rgb)

        # 检查是否检测到人脸
        if not results.multi_face_landmarks:
            return None

        # 获取第一个人脸的关键点
        face_landmarks = results.multi_face_landmarks[0]

        # 获取图像尺寸
        h, w = image.shape[:2]

        # 提取嘴部关键点并转换为像素坐标
        mouth_points = []
        for idx in [
            self.UPPER_LIP_IDX,
            self.LOWER_LIP_IDX,
            self.LEFT_CORNER_IDX,
            self.RIGHT_CORNER_IDX,
        ]:
            landmark = face_landmarks.landmark[idx]
            x = landmark.x * w
            y = landmark.y * h
            mouth_points.append([x, y])

        return np.array(mouth_points, dtype=np.float32)

    def draw_mouth_landmarks(
        self, image: np.ndarray, mouth_landmarks: np.ndarray
    ) -> np.ndarray:
        """
        在图像上绘制嘴部关键点（用于调试）

        Args:
            image: 输入图像
            mouth_landmarks: (4, 2) 嘴部关键点

        Returns:
            标注后的图像
        """
        image_copy = image.copy()

        if mouth_landmarks is None:
            return image_copy

        # 定义颜色
        colors = [
            (0, 255, 0),  # 上唇 - 绿色
            (0, 255, 0),  # 下唇 - 绿色
            (255, 0, 0),  # 左嘴角 - 蓝色
            (255, 0, 0),  # 右嘴角 - 蓝色
        ]

        # 绘制关键点
        for point, color in zip(mouth_landmarks, colors):
            x, y = int(point[0]), int(point[1])
            cv2.circle(image_copy, (x, y), 3, color, -1)

        # 绘制嘴部轮廓
        # 连接上下唇
        upper_lip = mouth_landmarks[0]
        lower_lip = mouth_landmarks[1]
        cv2.line(
            image_copy,
            (int(upper_lip[0]), int(upper_lip[1])),
            (int(lower_lip[0]), int(lower_lip[1])),
            (0, 255, 255),
            1,
        )

        # 连接左右嘴角
        left_corner = mouth_landmarks[2]
        right_corner = mouth_landmarks[3]
        cv2.line(
            image_copy,
            (int(left_corner[0]), int(left_corner[1])),
            (int(right_corner[0]), int(right_corner[1])),
            (0, 255, 255),
            1,
        )

        return image_copy

    def close(self):
        """释放资源"""
        self.face_mesh.close()
