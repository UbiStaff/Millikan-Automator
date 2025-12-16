# Millikan-Automator (油滴实验自动化)

[![English](https://img.shields.io/badge/Language-English-gray.svg)](README.md) [![Chinese](https://img.shields.io/badge/Language-中文-blue.svg)](README_CN.md)

**注意：本项目基于 [ricktjwong](https://github.com/ricktjwong/millikan) 的原始项目进行修改。**

### 主要修改内容
- **文档支持**：添加了中文文档说明 (`README_CN.md`)。
- **代码调整**：更新了文件路径配置，优化了本地运行体验。
- **功能增强**：在 `transform.py` 中增加了轨迹可视化功能，方便检查粒子运动情况。
- **参数调优**：针对特定实验环境调整了 `extract.py` 和 `transform.py` 中的关键参数（如电压、识别阈值等）。

## 在 Millikan 油滴实验中识别带电油滴

Millikan 油滴实验的核心任务是测量油滴在不同条件下的终端速度，以便最终推算出油滴的电荷。传统上，实验需要通过显微镜观察一个油滴，跟踪其位置变化，并记录下来计算其速度。这个过程既耗时又繁琐。

这些 Python 脚本的编写目的是为了：

1. 通过显微镜图像自动识别油滴。
2. 自动计算油滴的速度。

本项目使用了 [trackpy](https://github.com/soft-matter/trackpy)，这是一个 Crocker-Grier 算法的 Python 实现，用于在视频帧之间进行粒子追踪。

## 先决条件

- Python 3.6 或更高版本
- 依赖库：`trackpy`, `numpy`, `pandas`, `matplotlib`, `pims`, `slicerator`

## 安装步骤

1. 克隆项目仓库：
   ```bash
   git clone https://github.com/UbiStaff/Millikan-Automator.git
   cd Millikan-Automator
   ```

2. 创建并激活虚拟环境（可选但推荐）：
   ```bash
   python3 -m venv millikan_env
   source millikan_env/bin/activate
   # Windows 用户请使用: millikan_env\Scripts\activate
   ```

3. 安装依赖：
   ```bash
   pip install trackpy numpy pandas matplotlib pims slicerator
   ```

## 使用说明

### 1. 提取数据 (Extract)
运行 `python/extract.py` 读取 `test_video` 文件夹中的 MOV 视频文件。该脚本会自动识别油滴并进行追踪，最终将重要数据提取并保存为 `csvs/extract.csv`。

> **注意：** 这个过程可能需要一些时间，因为它会对视频中的大部分帧进行处理。

```bash
python python/extract.py
```

### 2. 转换数据 (Transform)
提取完成后，运行 `python/transform.py`。该脚本会过滤掉那些在电场移除后没有改变方向的油滴，并计算有用的物理量（如速度），结果将保存到 `csvs/transformed.csv`。

```bash
python python/transform.py
```
