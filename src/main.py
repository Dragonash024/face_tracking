"""
Active Speaker Detection - 主程序

实时从摄像头捕获视频并检测活跃发言人。
"""

import cv2
import yaml
import argparse
from pathlib import Path
from detector.active_speaker import ActiveSpeakerDetector


def load_config(config_path: str) -> dict:
    """加载配置文件"""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="Active Speaker Detection")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default.yaml",
        help="Path to config file",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Show debug information"
    )
    parser.add_argument(
        "--video",
        type=str,
        default=None,
        help="Path to video file or directory of videos (skips camera)",
    )
    args = parser.parse_args()

    # 加载配置
    config = load_config(args.config)

    # 初始化检测器
    detector = ActiveSpeakerDetector(
        window_size=config["detector"]["window_size"],
        variance_threshold=config["detector"]["variance_threshold"],
        min_speaking_frames=config["detector"]["min_speaking_frames"],
        mar_range=config["detector"]["mar_range"],
        max_num_faces=config["mediapipe"]["max_num_faces"],
        min_detection_confidence=config["mediapipe"]["min_detection_confidence"],
        min_tracking_confidence=config["mediapipe"]["min_tracking_confidence"],
    )

    # 构建视频源列表
    video_sources = []
    if args.video:
        video_path = Path(args.video)
        if video_path.is_dir():
            for ext in ("*.mp4", "*.mkv", "*.avi", "*.mov"):
                video_sources.extend(sorted(video_path.glob(ext)))
        elif video_path.is_file():
            video_sources.append(video_path)
        else:
            print(f"Error: {args.video} is not a valid file or directory")
            return
        if not video_sources:
            print(f"Error: No video files found in {args.video}")
            return
        print(f"Found {len(video_sources)} video(s)")
    else:
        video_sources = [config["video"]["camera_id"]]

    print("Active Speaker Detection Started")
    print("Press 'q' to quit, 'r' to reset, 'n' to skip to next video")
    print("-" * 50)

    # 主循环
    try:
      for src_idx, source in enumerate(video_sources):
        if args.video:
            source_arg = str(source)
            print(f"\n[{src_idx+1}/{len(video_sources)}] Playing: {Path(source_arg).name}")
        else:
            source_arg = int(source)

        cap = cv2.VideoCapture(source_arg)
        if not args.video:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, config["video"]["width"])
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config["video"]["height"])

        if not cap.isOpened():
            print(f"Error: Cannot open {source_arg}")
            continue

        detector.reset()
        skip_video = False

        while True:
            # 捕获帧
            ret, frame = cap.read()
            if not ret:
                break

            # 处理帧
            is_speaking, debug_info = detector.process_frame(frame)

            # 可视化
            if args.debug:
                # 显示调试信息
                display_frame = detector.draw_debug_info(frame, is_speaking, debug_info)
            else:
                # 简单显示
                display_frame = frame.copy()
                status_text = "SPEAKING" if is_speaking else "Silent"
                status_color = (0, 255, 0) if is_speaking else (128, 128, 128)
                cv2.putText(
                    display_frame,
                    status_text,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    status_color,
                    2,
                )

            # 显示帧
            cv2.imshow("Active Speaker Detection", display_frame)

            # 处理按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                skip_video = True
                break
            elif key == ord("n"):
                break
            elif key == ord("r"):
                print("Resetting detector...")
                detector.reset()

        cap.release()

        if skip_video:
            break

    except KeyboardInterrupt:
        print("\nInterrupted by user")

    finally:
        # 清理资源
        cv2.destroyAllWindows()
        detector.close()
        print("Stopped")


if __name__ == "__main__":
    main()
