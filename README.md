# 活跃发言人检测系统 (Active Speaker Detection)

基于计算机视觉的实时活跃发言人检测系统，使用 MediaPipe 和嘴部纵横比（MAR）方差分析。

## 功能特点

- ✅ 实时检测摄像头画面中的说话行为
- ✅ 区分真实说话和其他嘴部动作（打哈欠、嚼口香糖、微笑等）
- ✅ 轻量级设备端方案，无需云端或深度学习模型
- ✅ 基于 MediaPipe 的快速面部关键点提取
- ✅ 可配置的参数和调试模式

## 技术原理

### 核心算法

1. **MAR (Mouth Aspect Ratio) 计算**
   ```
   MAR = 垂直距离 / 水平距离
       = |y_上唇 - y_下唇| / |x_左嘴角 - x_右嘴角|
   ```

2. **方差分析**
   - 维护15帧的 MAR 滑动窗口
   - 计算窗口内 MAR 的方差
   - 说话时嘴唇快速变化，方差大
   - 静态表情变化慢或有规律，方差小

3. **持续时间过滤**
   - 需连续9帧以上高方差才确认为说话
   - 避免短暂波动的误触发

## 安装

### 环境要求

- Python 3.11+
- 摄像头

### 安装步骤

```bash
# 克隆或进入项目目录
cd /Users/maxos/CJM

# 创建虚拟环境（推荐）
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
# 运行主程序
python src/main.py

# 带调试信息运行
python src/main.py --debug

# 使用自定义配置
python src/main.py --config configs/custom.yaml --debug
```

### 按键控制

- `q`: 退出程序
- `r`: 重置检测器状态

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_mar_calculator.py -v
pytest tests/test_velocity_tracker.py -v
pytest tests/test_integration.py -v
```

## 项目结构

```
CJM/
├── requirements.txt           # Python 依赖
├── README.md                  # 项目说明
├── configs/
│   └── default.yaml          # 配置文件
├── src/
│   ├── main.py               # 主程序入口
│   └── detector/
│       ├── face_mesh.py      # MediaPipe 关键点提取
│       ├── mar_calculator.py # MAR 计算
│       ├── velocity_tracker.py # 速度追踪（核心算法）
│       └── active_speaker.py # 主检测器
├── tests/
│   ├── test_mar_calculator.py
│   ├── test_velocity_tracker.py
│   └── test_integration.py
└── notebooks/
    └── algorithm_tuning.ipynb # 参数调优笔记本
```

## 配置说明

编辑 `configs/default.yaml` 来调整参数：

```yaml
detector:
  window_size: 15              # 滑动窗口大小（帧数）
  variance_threshold: 0.001    # 方差阈值
  min_speaking_frames: 9       # 最小连续说话帧数
  mar_range: [0.05, 0.8]      # 有效 MAR 范围

mediapipe:
  max_num_faces: 1             # 最大检测人脸数
  min_detection_confidence: 0.5
  min_tracking_confidence: 0.5

video:
  camera_id: 0                 # 摄像头 ID
  width: 640
  height: 480
```

### 参数调优建议

- **降低误报（减少错误触发）**:
  - 增大 `variance_threshold`
  - 增大 `min_speaking_frames`

- **降低漏报（提高检测灵敏度）**:
  - 减小 `variance_threshold`
  - 减小 `min_speaking_frames`

- **提高响应速度**:
  - 减小 `min_speaking_frames`
  - 减小 `window_size`

## 性能指标

- **FPS**: 20-30 帧/秒（取决于硬件）
- **CPU 使用率**: < 40%
- **响应延迟**: < 0.5 秒

## 验证场景

系统已针对以下场景进行测试：

- ✅ 正常说话 → 应检测为"说话中"
- ✅ 打哈欠 → 不应触发（慢速张嘴）
- ✅ 嚼口香糖 → 不应触发（低方差周期运动）
- ✅ 微笑 → 不应触发（MAR 变化小）
- ✅ 快速张合嘴 → 应触发

## 局限性

- 侧脸时检测精度下降
- 极端光照条件下可能失败
- 不同人的 MAR 基线不同（可能需要个性化校准）
- 仅支持单人检测（当前配置）

## 后续增强方向

1. 多人同时检测
2. 音频能量融合
3. 深度学习分类器（LSTM）
4. 个性化校准流程
5. 移动端移植

## 技术栈

- **MediaPipe**: 面部关键点提取
- **OpenCV**: 视频捕获和处理
- **NumPy**: 数值计算
- **PyYAML**: 配置管理
- **Pytest**: 单元测试

## 许可证

本项目为概念验证项目，仅供学习和研究使用。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请提交 Issue。
