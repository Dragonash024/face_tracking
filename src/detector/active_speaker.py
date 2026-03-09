"""
Active Speaker Detector

整合所有模块，提供统一的活跃发言人检测接口。
"""

import numpy as np
from typing import Dict, Tuple, Optional
from .face_mesh import FaceMeshExtractor
from .mar_calculator import MARCalculator
from .velocity_tracker import VelocityTracker


class ActiveSpeakerDetector:
    """
    活跃发言人检测器

    整合面部关键点提取、MAR 计算和速度追踪，
    提供端到端的说话检测功能。
    """

    def __init__(
        self,
        window_size: int = 15,
        variance_threshold: float = 0.001,
        min_speaking_frames: int = 9,
        mar_range: Tuple[float, float] = (0.05, 0.8),
        max_num_faces: int = 1,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ):
        """
        初始化活跃发言人检测器

        Args:
            window_size: 滑动窗口大小
            variance_threshold: 方差阈值
            min_speaking_frames: 最小连续说话帧数
            mar_range: 有效 MAR 范围
            max_num_faces: 最大检测人脸数
            min_detection_confidence: 最小检测置信度
            min_tracking_confidence: 最小追踪置信度
        """
        # 初始化各模块
        self.face_mesh = FaceMeshExtractor(
            max_num_faces=max_num_faces,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.mar_calculator = MARCalculator()
        self.velocity_tracker = VelocityTracker(
            window_size=window_size,
            variance_threshold=variance_threshold,
            min_speaking_frames=min_speaking_frames,
            mar_range=mar_range,
        )

    def process_frame(self, frame: np.ndarray) -> Tuple[bool, Dict]:
        """
        处理单帧图像，检测是否有人在说话

        Args:
            frame: 输入图像 (BGR 格式)

        Returns:
            (is_speaking, debug_info)
            - is_speaking: 是否检测到说话
            - debug_info: 调试信息字典
        """
        debug_info = {
            "face_detected": False,
            "mouth_landmarks": None,
            "mar": None,
            "variance": 0.0,
            "in_range": False,
            "variance_triggered": False,
            "speaking_count": 0,
        }

        # 1. 提取嘴部关键点
        mouth_landmarks = self.face_mesh.extract_mouth_landmarks(frame)

        if mouth_landmarks is None:
            # 未检测到人脸
            is_speaking, tracker_debug = self.velocity_tracker.update(None)
            debug_info.update(tracker_debug)
            return False, debug_info

        debug_info["face_detected"] = True
        debug_info["mouth_landmarks"] = mouth_landmarks

        # 2. 计算 MAR
        mar = self.mar_calculator.calculate(mouth_landmarks)

        if mar is None:
            # MAR 计算失败
            is_speaking, tracker_debug = self.velocity_tracker.update(None)
            debug_info.update(tracker_debug)
            return False, debug_info

        debug_info["mar"] = mar

        # 3. 速度检测和持续时间过滤
        is_speaking, tracker_debug = self.velocity_tracker.update(mar)
        debug_info.update(tracker_debug)

        return is_speaking, debug_info

    def draw_debug_info(
        self, frame: np.ndarray, is_speaking: bool, debug_info: Dict
    ) -> np.ndarray:
        """
        在图像上绘制调试信息

        Args:
            frame: 输入图像
            is_speaking: 是否在说话
            debug_info: 调试信息

        Returns:
            标注后的图像
        """
        import cv2

        frame_copy = frame.copy()

        # 绘制嘴部关键点
        if debug_info["mouth_landmarks"] is not None:
            frame_copy = self.face_mesh.draw_mouth_landmarks(
                frame_copy, debug_info["mouth_landmarks"]
            )

        # 绘制说话状态
        status_text = "SPEAKING" if is_speaking else "Silent"
        status_color = (0, 255, 0) if is_speaking else (128, 128, 128)
        cv2.putText(
            frame_copy,
            status_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            status_color,
            2,
        )

        # 绘制 MAR 值
        if debug_info["mar"] is not None:
            mar_text = f"MAR: {debug_info['mar']:.4f}"
            cv2.putText(
                frame_copy,
                mar_text,
                (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                1,
            )

        # 绘制方差值
        var_text = f"Variance: {debug_info['variance']:.6f}"
        cv2.putText(
            frame_copy,
            var_text,
            (10, 85),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )

        # 绘制连续帧计数
        count_text = f"Count: {debug_info['speaking_count']}"
        cv2.putText(
            frame_copy,
            count_text,
            (10, 110),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1,
        )

        # 绘制触发状态
        if debug_info["variance_triggered"]:
            cv2.putText(
                frame_copy,
                "VARIANCE TRIGGERED",
                (10, 135),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 255),
                1,
            )

        return frame_copy

    def reset(self):
        """重置检测器状态"""
        self.velocity_tracker.reset()

    def close(self):
        """释放资源"""
        self.face_mesh.close()
