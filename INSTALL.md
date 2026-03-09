# 安装指南 (Installation Guide)

## 快速开始

### 1. 安装 Python 3.11

#### 使用 pyenv (推荐)

```bash
# 安装 pyenv
brew install pyenv

# 安装 Python 3.11.8
pyenv install 3.11.8

# 在项目目录中设置本地 Python 版本
cd /Users/maxos/CJM
pyenv local 3.11.8
```

#### 或者直接使用系统 Python

确保系统已安装 Python 3.11+：

```bash
python3 --version  # 应该显示 3.11.x 或更高
```

### 2. 创建虚拟环境

```bash
cd /Users/maxos/CJM

# 创建虚拟环境
python3.11 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 升级 pip

```bash
pip install --upgrade pip
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

这将安装以下包：
- `mediapipe==0.10.9` - 面部关键点检测
- `opencv-python==4.9.0.80` - 视频处理
- `numpy==1.26.4` - 数值计算
- `scipy==1.12.0` - 科学计算
- `pyyaml==6.0.1` - 配置文件解析
- `pytest==8.0.0` - 单元测试
- `jupyter==1.0.0` - 交互式笔记本

### 5. 验证安装

运行测试以验证安装是否成功：

```bash
pytest tests/ -v
```

如果所有测试通过，说明安装成功！

### 6. 运行主程序

```bash
# 基本运行
python src/main.py

# 带调试信息运行
python src/main.py --debug
```

## 常见问题

### Q1: MediaPipe 安装失败

**解决方案：**
- 确保使用 Python 3.11
- 尝试升级 pip: `pip install --upgrade pip`
- 如果仍然失败，尝试从源码安装：
  ```bash
  pip install mediapipe --no-cache-dir
  ```

### Q2: OpenCV 无法打开摄像头

**解决方案：**
- 检查摄像头权限（系统设置 > 隐私 > 摄像头）
- 尝试不同的 camera_id（在 configs/default.yaml 中修改）
- 确保没有其他程序占用摄像头

### Q3: 测试失败

**解决方案：**
- 确保在项目根目录运行测试
- 检查 Python 路径是否正确
- 尝试重新安装依赖：
  ```bash
  pip uninstall -y -r requirements.txt
  pip install -r requirements.txt
  ```

### Q4: 性能较差（FPS < 15）

**解决方案：**
- 降低视频分辨率（在 configs/default.yaml 中修改 width 和 height）
- 关闭调试模式（不使用 --debug 参数）
- 确保没有其他高 CPU 占用的程序在运行

## 开发环境设置

如果你想修改代码，推荐安装开发工具：

```bash
pip install black flake8 mypy ipython
```

- `black`: 代码格式化
- `flake8`: 代码检查
- `mypy`: 类型检查
- `ipython`: 增强的 Python 交互式环境

## 卸载

```bash
# 停用虚拟环境
deactivate

# 删除虚拟环境
rm -rf venv

# 删除项目目录（可选）
rm -rf /Users/maxos/CJM
```

## 下一步

安装完成后，查看 [README.md](README.md) 了解如何使用系统。
