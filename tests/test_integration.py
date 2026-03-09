"""
集成测试

测试完整的检测流程。
"""

import pytest
import numpy as np
import cv2
import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from detector.active_speaker import ActiveSpeakerDetector


class TestIntegration:
    """集成测试类"""

    def setup_method(self):
        """每个测试前初始化"""
        self.detector = ActiveSpeakerDetector(
            window_size=15,
            variance_threshold=0.001,
            min_speaking_frames=9,
            mar_range=(0.05, 0.8),
        )

    def teardown_method(self):
        """每个测试后清理"""
        self.detector.close()

    def test_no_face_frame(self):
        """测试无人脸的帧"""
        # 创建一个纯色图像（无人脸）
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        is_speaking, debug_info = self.detector.process_frame(frame)

        assert not is_speaking
        assert not debug_info["face_detected"]
        assert debug_info["mouth_landmarks"] is None

    def test_reset(self):
        """测试重置功能"""
        # 创建测试帧
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        # 处理几帧
        for _ in range(5):
            self.detector.process_frame(frame)

        # 重置
        self.detector.reset()

        # 验证追踪器状态被重置
        assert len(self.detector.velocity_tracker.mar_history) == 0
        assert self.detector.velocity_tracker.speaking_frame_count == 0

    def test_draw_debug_info(self):
        """测试调试信息绘制"""
        frame = np.ones((480, 640, 3), dtype=np.uint8) * 128

        is_speaking, debug_info = self.detector.process_frame(frame)

        # 应该能正常绘制，不抛出异常
        debug_frame = self.detector.draw_debug_info(frame, is_speaking, debug_info)

        assert debug_frame.shape == frame.shape
        assert debug_frame.dtype == frame.dtype

    @pytest.mark.skipif(
        not cv2.VideoCapture(0).isOpened(),
        reason="No camera available",
    )
    def test_real_camera(self):
        """测试真实摄像头（如果可用）"""
        cap = cv2.VideoCapture(0)

        try:
            ret, frame = cap.read()
            if ret:
                is_speaking, debug_info = self.detector.process_frame(frame)

                # 验证返回值类型正确
                assert isinstance(is_speaking, bool)
                assert isinstance(debug_info, dict)
                assert "face_detected" in debug_info
                assert "mar" in debug_info
        finally:
            cap.release()
