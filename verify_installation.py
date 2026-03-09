#!/usr/bin/env python3
"""
Installation Verification Script

验证所有依赖是否正确安装。
"""

import sys


def check_python_version():
    """检查 Python 版本"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(
            f"✗ Python {version.major}.{version.minor}.{version.micro} - "
            f"Requires Python 3.11+"
        )
        return False


def check_imports():
    """检查所有必需的包"""
    print("\nChecking required packages...")

    packages = {
        "cv2": "opencv-python",
        "mediapipe": "mediapipe",
        "numpy": "numpy",
        "scipy": "scipy",
        "yaml": "pyyaml",
        "pytest": "pytest",
    }

    all_ok = True
    for module_name, package_name in packages.items():
        try:
            __import__(module_name)
            print(f"✓ {package_name} - OK")
        except ImportError:
            print(f"✗ {package_name} - NOT FOUND")
            all_ok = False

    return all_ok


def check_camera():
    """检查摄像头是否可用"""
    print("\nChecking camera access...")
    try:
        import cv2

        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret and frame is not None:
                print(f"✓ Camera (ID: 0) - OK (Resolution: {frame.shape[1]}x{frame.shape[0]})")
                return True
            else:
                print("✗ Camera - Cannot read frame")
                return False
        else:
            print("✗ Camera - Cannot open (check permissions)")
            return False
    except Exception as e:
        print(f"✗ Camera - Error: {e}")
        return False


def check_mediapipe():
    """检查 MediaPipe 是否正常工作"""
    print("\nChecking MediaPipe...")
    try:
        import mediapipe as mp
        import numpy as np

        # 创建一个简单的 Face Mesh 实例
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1)

        # 创建一个测试图像
        test_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # 尝试处理
        results = face_mesh.process(test_image)
        face_mesh.close()

        print("✓ MediaPipe Face Mesh - OK")
        return True
    except Exception as e:
        print(f"✗ MediaPipe Face Mesh - Error: {e}")
        return False


def check_project_structure():
    """检查项目结构"""
    print("\nChecking project structure...")
    from pathlib import Path

    required_files = [
        "configs/default.yaml",
        "src/main.py",
        "src/detector/face_mesh.py",
        "src/detector/mar_calculator.py",
        "src/detector/velocity_tracker.py",
        "src/detector/active_speaker.py",
        "tests/test_mar_calculator.py",
        "tests/test_velocity_tracker.py",
        "tests/test_integration.py",
    ]

    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            all_ok = False

    return all_ok


def main():
    """主函数"""
    print("=" * 60)
    print("Active Speaker Detection - Installation Verification")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_imports),
        ("Camera Access", check_camera),
        ("MediaPipe", check_mediapipe),
        ("Project Structure", check_project_structure),
    ]

    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} - Unexpected error: {e}")
            results.append((name, False))

    # 总结
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
        if not result:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 All checks passed! You're ready to go.")
        print("\nNext steps:")
        print("  1. Run tests: pytest tests/ -v")
        print("  2. Run main program: python src/main.py --debug")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nRefer to INSTALL.md for troubleshooting.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
