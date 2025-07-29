# 3D CAD Intelligent Segmentation System / 3D CAD智能分割系统

An industrial-grade CAD model intelligent segmentation system developed based on PyQt5 and PythonOCC, supporting three segmentation modes with complete 3D visualization and label configuration.

基于PyQt5和PythonOCC开发的工业级CAD模型智能分割系统，支持三种分割模式，提供完整的3D可视化与标签配置功能。

![image-20250701095628547](https://github.com/BrepMaster/SegCAD/raw/main/1.png)

📦 Download (Windows EXE version):

链接: https://pan.baidu.com/s/152cwyWQOjsbSrqTNwou9dQ?pwd=2iez 

提取码: 2iez

**温馨提示**
如果本项目对您有所帮助，欢迎点击右上角⭐Star支持！
如需在学术或商业用途中使用本项目，请注明出处。



## Table of Contents / 目录

- [Core Features](#core-features--核心功能)
- [System Requirements](#system-requirements--系统要求)
- [Usage Instructions](#usage-instructions--使用说明)
- [Project Structure](#project-structure--项目结构)
- [Development Guide](#development-guide--开发指南)
- [License](#license--许可证)

## Core Features / 核心功能

### Segmentation Modes / 分割模式

| 模式               | 描述                             | 输入要求                          |
| ------------------ | -------------------------------- | --------------------------------- |
| 模式1: 实时分割    | 使用深度学习模型直接分割STEP文件 | 需要模型文件(.ckpt/.pt)和标签配置 |
| 模式2: 使用BIN文件 | 基于预处理BIN图像文件进行分割    | 需要BIN文件及对应STEP文件         |
| 模式3: 使用SEG文件 | 直接加载预分割结果               | 需要SEG文件及对应STEP文件         |

### Key Features / 特色功能

```text
✅ 多语言支持 - 中英文界面一键切换
✅ 智能标签系统 - 可配置的类别名称和颜色
✅ 交互式3D查看 - 面选择与类别高亮
✅ 批量处理 - 支持文件夹批量处理
✅ 历史记录 - 保存50条最近操作记录
✅ 多种导出格式 - JSON/TXT/SEG报告

✅ Multi-language Support - Chinese/English UI toggle
✅ Smart Label System - Configurable category names and colors
✅ Interactive 3D Viewing - Face selection and category highlighting
✅ Batch Processing - Supports folder batch processing
✅ History Tracking - Saves 50 most recent operations
✅ Multiple Export Formats - JSON/TXT/SEG reports
```

## System Requirements / 系统要求

- Python 3.8+
- PyQt5 5.15+
- PythonOCC 7.6+
- PyTorch 1.10+
- DGL 0.8+

## Usage Instructions / 使用说明

### Basic Workflow / 基本工作流程

1. **选择分割模式** - 从下拉菜单中选择合适模式
2. **加载所需文件** - 根据模式加载模型/BIN/SEG文件
3. **配置标签** - 自定义类别名称和显示颜色
4. **加载STEP文件** - 拖放或通过对话框选择
5. **执行分割** - 点击"开始分割"按钮
6. **查看结果** - 在3D视图和面列表中检查分割结果

### Advanced Features / 高级功能

- **批量处理**: 通过"批量处理STEP文件"按钮处理整个文件夹
- **历史追踪**: 通过"历史记录"按钮查看和恢复之前的操作
- **标签配置**: 支持动态添加/删除标签类别

## Project Structure / 项目结构

```
├── constants.py          # 常量定义（颜色、样式、多语言）
├── graph_utils.py        # 图构建工具（STEP转DGL图）
├── preprocessor.py       # 数据预处理（归一化/缩放）
├── segmentation_logic.py # 核心业务逻辑
├── segmentation_model.py # PyTorch Lightning模型定义
├── segmentation_ui.py    # 界面交互逻辑
├── ui_app.py             # 主应用入口
├── label_config.py       # 标签配置对话框
├── history_dialog.py     # 历史记录对话框
└── README.md             # 说明文档

├── constants.py          # Constant definitions (colors, styles, i18n)
├── graph_utils.py        # Graph construction tools (STEP to DGL graph)
├── preprocessor.py       # Data preprocessing (normalization/scaling)
├── segmentation_logic.py # Core business logic
├── segmentation_model.py # PyTorch Lightning model definition
├── segmentation_ui.py    # UI interaction logic
├── ui_app.py             # Main application entry
├── label_config.py       # Label configuration dialog
├── history_dialog.py     # History dialog
└── README.md             # Documentation
```

## Development Guide / 开发指南

### Key Technologies / 关键技术栈

- **前端框架**: PyQt5 + PythonOCC
- **深度学习**: PyTorch Lightning + DGL
- **3D可视化**: OpenCASCADE
- **数据处理**: NumPy

- **Frontend Framework**: PyQt5 + PythonOCC
- **Deep Learning**: PyTorch Lightning + DGL
- **3D Visualization**: OpenCASCADE
- **Data Processing**: NumPy

## License / 许可证

MIT License

---

> For technical support or commercial cooperation, please contact me.
> 如需技术支持或商业合作，请联系我。
