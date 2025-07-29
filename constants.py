# constants.py
DEFAULT_COLORS = [
    [78, 101, 148],  # 钢蓝 (冷轧钢色)
    [191, 87, 0],    # 氧化铁红
    [169, 169, 169],  # 机械灰 (铸铁色)
    [218, 165, 32],   # 黄铜金
    [112, 128, 105],  # 军绿 (工业漆)
    [61, 158, 211],   # 阳极蓝
    [150, 0, 24],     # 深红 (警告色)
    [200, 160, 100],  # 青铜
    [70, 70, 80],     # 枪金属黑
    [0, 180, 180],    # 氰化蓝 (电镀色)
    [180, 100, 60],   # 铜锈橙
    [100, 120, 140],  # 铝灰
    [255, 126, 0],    # 安全橙
    [83, 107, 83],    # 橄榄钢
    [150, 150, 200],  # 不锈钢浅蓝
    [194, 178, 128]   # 哑光金
]

STYLESHEET = """
/* 基础样式 */
QWidget {
    font-family: 'Microsoft YaHei';
    font-size: 12px;
    background-color: #f5f7fa;
}

/* 按钮样式 */
QPushButton {
    min-width: 80px;
    min-height: 28px;
    padding: 4px 8px;
    border-radius: 4px;
    background-color: #4a6fa5;
    color: white;
    border: none;
}
QPushButton:hover {
    background-color: #5a7fb5;
}
QPushButton:pressed {
    background-color: #3a5f95;
}
QPushButton:disabled {
    background-color: #cccccc;
    color: #666666;
}
QPushButton[loaded="true"] {
    background-color: #4caf50;
}

/* 改进的语言切换按钮样式 */
QPushButton#language_button {
    min-width: 100px;
    min-height: 28px;
    padding: 0 5px;
    border-radius: 4px;
    background-color: #e1f5fe;
    border: 1px solid #d1d9e6;
}
QPushButton#language_button:hover {
    background-color: #b3e5fc;
    border: 1px solid #81d4fa;
}
QPushButton#language_button:pressed {
    background-color: #81d4fa;
}
QPushButton#language_button QLabel {
    color: #0288d1;
    font-size: 12px;
}

/* 组合框样式 */
QComboBox {
    padding: 5px 8px;
    border: 1px solid #d1d9e6;
    border-radius: 4px;
    min-width: 120px;
    background: white;
    color: #333;
}
QComboBox:on {
    background: white;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
    border-left: 1px solid #d1d9e6;
}
QComboBox::down-arrow {
    width: 12px;
    height: 12px;
}
QComboBox QAbstractItemView {
    border: 1px solid #d1d9e6;
    background: white;
    selection-background-color: #4a6fa5;
    selection-color: white;
    outline: 0;
    padding: 4px;
    margin: 0;
    min-width: 150px;
}
QComboBox QAbstractItemView::item {
    height: 25px;
    padding: 0 8px;
    color: #333;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #e0e0e0;
    color: #333;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #4a6fa5;
    color: white;
}

/* 分组框样式 */
QGroupBox {
    border: 1px solid #d1d9e6;
    border-radius: 5px;
    margin-top: 6px;
    padding-top: 10px;
    background-color: white;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
    color: #4a6fa5;
}

/* 显示区域框架 */
QFrame#display_frame {
    border: 1px solid #d1d9e6;
    border-radius: 5px;
    background-color: white;
}

/* 状态标签 */
QLabel#status_label {
    background-color: white;
    color: #2c3e50;
    border: 1px solid #d1d9e6;
    border-radius: 4px;
    padding: 10px;
    min-height: 40px;
    min-width: 300px;
    font-size: 15px;
    font-weight: bold;
    font-family: 'Segoe UI', 'Microsoft YaHei';
}
QLabel#status_label[error="true"] {
    background-color: #ffebee;
    color: #c62828;
    border: 1px solid #ef9a9a;
}

/* 拖拽标签 */
QLabel#drop_label {
    background-color: rgba(255, 255, 255, 0.9);
    color: #666;
    border: 2px dashed #4a6fa5;
    border-radius: 6px;
    padding: 15px;
    font-size: 13px;
    qproperty-alignment: AlignCenter;
}

/* 面列表样式 */
QListWidget {
    border: 1px solid #d1d9e6;
    border-radius: 4px;
    background: white;
    padding: 2px;
}
QListWidget::item {
    padding: 5px;
    border-bottom: 1px solid #eee;
}
QListWidget::item:hover {
    background: #e3f2fd;
}
QListWidget::item:selected {
    background: #bbdefb;
    color: black;
}
QListWidget::item:selected:active {
    background: #90caf9;
}
"""

LANGUAGE_STRINGS = {
    "en": {
        "title": "3D CAD Intelligent Segmentation System",
        "mode1": "Mode 1: Real-time Segmentation",
        "mode2": "Mode 2: Using BIN File",
        "mode3": "Mode 3: Using SEG File",
        "load_model": "Load Model",
        "load_labels": "Load Labels",
        "load_step": "Load STEP",
        "load_bin": "Load BIN",
        "load_seg": "Load SEG",
        "clear": "Clear Display",
        "help": "Help",
        "export": "Export Results",
        "stats": "Show Statistics",
        "config": "Configure Labels",
        "segment": "Start Segmentation",
        "history": "History",
        "batch": "Batch Process STEP Files",
        "choose_mode": "Select Mode:",
        "control_panel": "Control Panel",
        "face_list": "Face List",
        "ready": "Ready",
        "drop_file": "Drop STEP file here"
    },
    "zh": {
        "title": "3D CAD 智能分割系统",
        "mode1": "模式1: 实时分割",
        "mode2": "模式2: 使用BIN文件",
        "mode3": "模式3: 使用SEG文件",
        "load_model": "加载模型",
        "load_labels": "加载标签",
        "load_step": "加载STEP",
        "load_bin": "加载BIN图",
        "load_seg": "加载SEG",
        "clear": "清空显示",
        "help": "帮助",
        "export": "导出结果",
        "stats": "显示统计",
        "config": "配置标签",
        "segment": "开始分割",
        "history": "历史记录",
        "batch": "批量处理STEP文件",
        "choose_mode": "选择模式:",
        "control_panel": "控制面板",
        "face_list": "面列表",
        "ready": "准备就绪",
        "drop_file": "拖拽STEP文件到此处"
    }
}