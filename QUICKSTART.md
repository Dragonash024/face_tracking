# 快速开始 (Quick Start)

## 5分钟上手指南

### 步骤 1: 安装依赖

```bash
cd /Users/maxos/CJM

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
```

### 步骤 2: 验证安装

```bash
python verify_installation.py
```

如果看到 "All checks passed!"，说明安装成功。

### 步骤 3: 运行主程序

```bash
# 带调试信息运行（推荐第一次使用）
python src/main.py --debug
```

### 步骤 4: 测试检测效果

在摄像头前尝试以下动作，观察检测结果：

1. **正常说话** → 应显示 "SPEAKING" (绿色)
2. **保持沉默** → 应显示 "Silent" (灰色)
3. **打哈欠（慢速张嘴）** → 应保持 "Silent"
4. **嚼口香糖** → 应保持 "Silent"
5. **微笑** → 应保持 "Silent"

### 步骤 5: 调整参数（可选）

如果检测效果不理想，编辑 `configs/default.yaml`：

```yaml
detector:
  variance_threshold: 0.001  # 增大此值可减少误报
  min_speaking_frames: 9     # 增大此值可减少短暂误触发
```

修改后重新运行程序。

## 按键控制

- `q`: 退出程序
- `r`: 重置检测器（如果检测状态异常）

## 调试信息说明

当使用 `--debug` 参数时，屏幕上会显示：

- **SPEAKING / Silent**: 当前检测状态
- **MAR**: 嘴部纵横比值
- **Variance**: 当前滑动窗口方差
- **Count**: 连续检测到说话的帧数
- **VARIANCE TRIGGERED**: 方差是否超过阈值

## 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 只测试 MAR 计算
pytest tests/test_mar_calculator.py -v

# 只测试速度追踪
pytest tests/test_velocity_tracker.py -v
```

## 性能优化

如果 FPS 较低（< 20），尝试：

1. 降低视频分辨率（修改 `configs/default.yaml` 中的 width 和 height）
2. 关闭调试模式（不使用 `--debug`）
3. 关闭其他占用 CPU 的程序

## 参数调优

使用 Jupyter Notebook 进行交互式参数调优：

```bash
# 启动 Jupyter
jupyter notebook notebooks/algorithm_tuning.ipynb
```

在笔记本中可以：
- 可视化 MAR 时间序列
- 分析方差曲线
- 测试不同参数组合
- 实时调整阈值

## 常见问题

### Q: 摄像头无法打开

**A:** 检查系统权限设置，确保 Python/终端有摄像头访问权限。

### Q: 总是显示 "SPEAKING"（误报过多）

**A:** 增大 `variance_threshold` 或 `min_speaking_frames`。

### Q: 说话时不显示 "SPEAKING"（漏报）

**A:** 减小 `variance_threshold` 或确保光线充足、面部清晰可见。

### Q: 检测延迟较大

**A:** 减小 `min_speaking_frames` 或 `window_size`（但可能增加误报）。

## 下一步

- 阅读 [README.md](README.md) 了解技术原理
- 查看 [INSTALL.md](INSTALL.md) 了解详细安装说明
- 探索 [notebooks/algorithm_tuning.ipynb](notebooks/algorithm_tuning.ipynb) 进行参数调优

## 获取帮助

如果遇到问题：
1. 运行 `python verify_installation.py` 检查安装
2. 查看 [INSTALL.md](INSTALL.md) 的常见问题部分
3. 检查代码注释和文档字符串

祝使用愉快！ 🎉
