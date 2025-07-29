# ui_app.py
import os
import sys
import json
import numpy as np
from datetime import datetime
from PyQt5.QtCore import Qt, QTimer, QUrl, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QLabel, QFileDialog, QMessageBox, QGroupBox, QFrame, QSizePolicy,
    QGridLayout, QComboBox, QScrollArea, QLineEdit, QDialog, QListWidget,
    QCheckBox, QListWidgetItem, QTableWidget, QTableWidgetItem, QProgressDialog
)
from PyQt5.QtGui import QFont, QColor, QDragEnterEvent, QDropEvent
from OCC.Display.backend import load_backend
from segmentation_ui import SegmentationUI
from history_dialog import HistoryDialog
from label_config import LabelConfigDialog
from segmentation_logic import SegmentationLogic
from constants import DEFAULT_COLORS, STYLESHEET, LANGUAGE_STRINGS
from PyQt5.QtWidgets import QApplication

load_backend("pyqt5")
from OCC.Display.qtDisplay import qtViewer3d
from OCC.Extend.DataExchange import read_step_file
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.AIS import AIS_InteractiveObject
from OCC.Core.TopoDS import TopoDS_Face
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopAbs import TopAbs_FACE


class SegmentationApp(QWidget, SegmentationUI):
    def __init__(self):
        super().__init__()
        self.title = "3D CAD 智能分割系统"
        self.setWindowTitle(self.title)
        self.resize(1200, 800)

        self.logic = SegmentationLogic()
        self.current_step_file = None
        self.current_bin_file = None
        self.current_seg_file = None
        self.current_model = None
        self.ais_list = []
        self.model_loaded = False
        self.labels_loaded = False
        self.step_loaded = False
        self.bin_loaded = False
        self.seg_loaded = False
        self.segmentation_mode = 1
        self.face_items = []
        self.history = []
        self.current_language = "zh"  # Default to Chinese

        self.canvas = qtViewer3d(self)
        self.setup_ui()
        self.setup_style()
        self.canvas.InitDriver()
        self.display = self.canvas._display
        self.setAcceptDrops(True)
        QTimer.singleShot(300, self.force_refresh_display)
        self.load_history()

    def convert_to_python_types(self, obj):
        if isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: self.convert_to_python_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.convert_to_python_types(x) for x in obj]
        return obj

    def setup_style(self):
        self.setStyleSheet(STYLESHEET)
        self.modeCombo.setAutoFillBackground(True)
        palette = self.modeCombo.palette()
        palette.setColor(palette.Window, QColor(255, 255, 255))
        palette.setColor(palette.WindowText, QColor(51, 51, 51))
        palette.setColor(palette.Highlight, QColor(74, 111, 165))
        palette.setColor(palette.HighlightedText, QColor(255, 255, 255))
        self.modeCombo.setPalette(palette)

        # 设置语言按钮的醒目样式
        self.languageButton.setStyleSheet("""
            QPushButton {
                color: #ffffff;
                background-color: #3498db;
                border: 2px solid #2980b9;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
                min-width: 50px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1d6fa5;
            }
        """)

    def setup_ui(self):
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(6)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(6)

        # Title bar with language button
        title_container = QWidget()
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0, 0, 0, 0)

        self.title_label = QLabel(self.title)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.languageButton = QPushButton("EN" if self.current_language == "zh" else "中文")
        self.languageButton.setObjectName("language_button")
        self.languageButton.setCursor(Qt.PointingHandCursor)
        self.languageButton.clicked.connect(self.toggle_language)

        title_layout.addWidget(self.title_label, 1)
        title_layout.addWidget(self.languageButton)
        title_container.setLayout(title_layout)

        left_layout.addWidget(title_container)

        # Control Panel
        self.control_panel = QGroupBox(LANGUAGE_STRINGS[self.current_language]["control_panel"])
        control_layout = QGridLayout()
        control_layout.setSpacing(6)
        control_layout.setContentsMargins(8, 12, 8, 8)

        self.modeCombo = QComboBox()
        self.modeCombo.addItems([
            LANGUAGE_STRINGS[self.current_language]["mode1"],
            LANGUAGE_STRINGS[self.current_language]["mode2"],
            LANGUAGE_STRINGS[self.current_language]["mode3"]
        ])
        self.modeCombo.currentIndexChanged.connect(self.on_mode_changed)

        self.loadModelButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["load_model"])
        self.loadLabelsButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["load_labels"])
        self.loadButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["load_step"])
        self.loadBinButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["load_bin"])
        self.loadSegButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["load_seg"])
        self.clearButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["clear"])
        self.exampleButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["help"])
        self.exportButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["export"])
        self.statsButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["stats"])
        self.configButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["config"])
        self.segmentButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["segment"])
        self.historyButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["history"])
        self.batchProcessButton = QPushButton(LANGUAGE_STRINGS[self.current_language]["batch"])

        self.segmentButton.setEnabled(False)

        # Button actions mapping
        button_actions = {
            LANGUAGE_STRINGS["zh"]["load_model"]: self.load_model,
            LANGUAGE_STRINGS["zh"]["load_labels"]: self.load_label_mapping,
            LANGUAGE_STRINGS["zh"]["load_step"]: self.load_step,
            LANGUAGE_STRINGS["zh"]["load_bin"]: self.load_bin,
            LANGUAGE_STRINGS["zh"]["load_seg"]: self.load_seg,
            LANGUAGE_STRINGS["zh"]["clear"]: self.clear_all,
            LANGUAGE_STRINGS["zh"]["help"]: self.show_examples,
            LANGUAGE_STRINGS["zh"]["export"]: self.export_results,
            LANGUAGE_STRINGS["zh"]["stats"]: self.show_statistics,
            LANGUAGE_STRINGS["zh"]["config"]: self.configure_labels,
            LANGUAGE_STRINGS["zh"]["segment"]: self.start_segmentation,
            LANGUAGE_STRINGS["zh"]["history"]: self.show_history,
            LANGUAGE_STRINGS["zh"]["batch"]: self.batch_process_step_files
        }

        # Connect button signals
        for btn in [self.loadModelButton, self.loadLabelsButton, self.loadButton,
                    self.loadBinButton, self.loadSegButton, self.clearButton,
                    self.exampleButton, self.exportButton, self.statsButton,
                    self.configButton, self.segmentButton, self.historyButton,
                    self.batchProcessButton]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(button_actions[btn.text()])

        self.modeComboLabel = QLabel(LANGUAGE_STRINGS[self.current_language]["choose_mode"])
        control_layout.addWidget(self.modeComboLabel, 0, 0)
        control_layout.addWidget(self.modeCombo, 0, 1, 1, 2)
        control_layout.addWidget(self.loadModelButton, 1, 0)
        control_layout.addWidget(self.loadLabelsButton, 1, 1)
        control_layout.addWidget(self.loadButton, 1, 2)
        control_layout.addWidget(self.loadBinButton, 2, 0)
        control_layout.addWidget(self.loadSegButton, 2, 1)
        control_layout.addWidget(self.clearButton, 2, 2)
        control_layout.addWidget(self.exportButton, 3, 0)
        control_layout.addWidget(self.statsButton, 3, 1)
        control_layout.addWidget(self.configButton, 3, 2)
        control_layout.addWidget(self.segmentButton, 4, 0)
        control_layout.addWidget(self.historyButton, 4, 1)
        control_layout.addWidget(self.batchProcessButton, 4, 2)
        self.control_panel.setLayout(control_layout)
        left_layout.addWidget(self.control_panel)

        # Display area
        display_frame = QFrame()
        display_frame.setObjectName("display_frame")
        display_layout = QHBoxLayout()
        display_layout.setContentsMargins(0, 0, 0, 0)

        self.canvas.setMinimumSize(600, 400)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.drop_label = QLabel(LANGUAGE_STRINGS[self.current_language]["drop_file"])
        self.drop_label.setObjectName("drop_label")
        self.drop_label.setVisible(False)

        display_layout.addWidget(self.canvas)
        display_layout.addWidget(self.drop_label)
        display_frame.setLayout(display_layout)
        left_layout.addWidget(display_frame, 1)

        # Status bar
        status_frame = QFrame()
        status_layout = QVBoxLayout()
        status_layout.setContentsMargins(6, 6, 6, 6)

        self.predictionLabel = QLabel(LANGUAGE_STRINGS[self.current_language]["ready"])
        self.predictionLabel.setObjectName("status_label")
        self.predictionLabel.setAlignment(Qt.AlignCenter)
        self.predictionLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        info_label = QLabel("© 3D CAD分割系统")
        info_label.setAlignment(Qt.AlignRight)
        info_label.setStyleSheet("color: #666; font-size: 10px;")

        status_layout.addWidget(self.predictionLabel)
        status_layout.addWidget(info_label)
        status_frame.setLayout(status_layout)
        left_layout.addWidget(status_frame)

        left_panel.setLayout(left_layout)

        # Right panel
        right_panel = QWidget()
        right_panel.setMinimumWidth(250)
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(6)

        self.face_list_title = QLabel(LANGUAGE_STRINGS[self.current_language]["face_list"])
        self.face_list_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.face_list_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.face_list_title)

        self.category_buttons_frame = QFrame()
        self.category_buttons_layout = QVBoxLayout()
        self.category_buttons_layout.setContentsMargins(0, 5, 0, 5)
        self.category_buttons_layout.setSpacing(5)
        self.category_buttons_frame.setLayout(self.category_buttons_layout)
        right_layout.addWidget(self.category_buttons_frame)

        self.faceListWidget = QListWidget()
        self.faceListWidget.setSelectionMode(QListWidget.SingleSelection)
        self.faceListWidget.itemClicked.connect(self.on_face_selected)
        right_layout.addWidget(self.faceListWidget)

        right_panel.setLayout(right_layout)

        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel)

        self.setLayout(main_layout)
        self.update_ui_for_mode()

    def toggle_language(self):
        """Toggle between Chinese and English"""
        self.current_language = "en" if self.current_language == "zh" else "zh"
        self.update_ui_language()

    def update_ui_language(self):
        """Update all UI elements with the current language"""
        lang = self.current_language
        strings = LANGUAGE_STRINGS[lang]

        # Update window title
        self.setWindowTitle(strings["title"])
        self.title_label.setText(strings["title"])

        # Update mode combo box
        self.modeCombo.clear()
        self.modeCombo.addItems([strings["mode1"], strings["mode2"], strings["mode3"]])

        # Update buttons
        self.loadModelButton.setText(strings["load_model"])
        self.loadLabelsButton.setText(strings["load_labels"])
        self.loadButton.setText(strings["load_step"])
        self.loadBinButton.setText(strings["load_bin"])
        self.loadSegButton.setText(strings["load_seg"])
        self.clearButton.setText(strings["clear"])
        self.exampleButton.setText(strings["help"])
        self.exportButton.setText(strings["export"])
        self.statsButton.setText(strings["stats"])
        self.configButton.setText(strings["config"])
        self.segmentButton.setText(strings["segment"])
        self.historyButton.setText(strings["history"])
        self.batchProcessButton.setText(strings["batch"])

        # Update other UI elements
        self.control_panel.setTitle(strings["control_panel"])
        self.face_list_title.setText(strings["face_list"])
        self.predictionLabel.setText(strings["ready"])
        self.drop_label.setText(strings["drop_file"])
        self.modeComboLabel.setText(strings["choose_mode"])

        # Update language toggle button text
        self.languageButton.setText("中文" if lang == "en" else "EN")

    def on_mode_changed(self, index):
        self.segmentation_mode = index + 1
        self.update_ui_for_mode()

    def update_ui_for_mode(self):
        self.model_loaded = False
        self.bin_loaded = False
        self.seg_loaded = False

        if self.segmentation_mode == 1:
            self.loadModelButton.setEnabled(True)
            self.loadBinButton.setEnabled(False)
            self.loadSegButton.setEnabled(False)
            self.loadModelButton.setProperty("loaded", "false")
            self.loadBinButton.setProperty("loaded", "false")
            self.loadSegButton.setProperty("loaded", "false")
        elif self.segmentation_mode == 2:
            self.loadModelButton.setEnabled(True)
            self.loadBinButton.setEnabled(True)
            self.loadSegButton.setEnabled(False)
            self.loadModelButton.setProperty("loaded", "false")
            self.loadBinButton.setProperty("loaded", "false")
            self.loadSegButton.setProperty("loaded", "false")
        elif self.segmentation_mode == 3:
            self.loadModelButton.setEnabled(False)
            self.loadBinButton.setEnabled(False)
            self.loadSegButton.setEnabled(True)
            self.loadModelButton.setProperty("loaded", "false")
            self.loadBinButton.setProperty("loaded", "false")
            self.loadSegButton.setProperty("loaded", "false")

        self.loadModelButton.style().polish(self.loadModelButton)
        self.loadBinButton.style().polish(self.loadBinButton)
        self.loadSegButton.style().polish(self.loadSegButton)

    def configure_labels(self):
        dialog = LabelConfigDialog(self)
        label_info = self.logic.get_label_info()

        if dialog.exec_() == QDialog.Accepted:
            config = dialog.get_config()
            self.logic.update_label_config(config)
            self.segmentButton.setEnabled(True)
            self.update_status("标签配置已更新")
            self.create_category_buttons()

    def show_examples(self):
        help_text = """
        <b>使用说明:</b>
        <ol>
            <li><b>模式1: 实时分割</b>
                <ul>
                    <li>加载模型文件(.ckpt/.pt/.pth)</li>
                    <li>配置标签和颜色(可选)</li>
                    <li>加载STEP文件(.step/.stp)</li>
                    <li>点击"开始分割"按钮进行实时分割</li>
                </ul>
            </li>
            <li><b>模式2: 使用BIN文件</b>
                <ul>
                    <li>加载模型文件(.ckpt/.pt/.pth)</li>
                    <li>配置标签和颜色(可选)</li>
                    <li>加载BIN图文件(.bin)</li>
                    <li>加载STEP文件(.step/.stp)用于显示</li>
                    <li>点击"开始分割"按钮使用BIN文件进行分割</li>
                </ul>
            </li>
            <li><b>模式3: 使用SEG文件</b>
                <ul>
                    <li>加载标签配置</li>
                    <li>加载SEG分割结果文件(.seg)</li>
                    <li>加载STEP文件(.step/.stp)用于显示</li>
                    <li>点击"开始分割"按钮直接渲染分割结果</li>
                </ul>
            </li>
        </ol>
        <b>支持拖拽操作</b>"""

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("帮助")
        msg.setTextFormat(Qt.RichText)
        msg.setText(help_text)
        msg.exec_()

    def force_refresh_display(self):
        self.canvas.resize(self.canvas.width() + 1, self.canvas.height() + 1)
        self.canvas.resize(self.canvas.width() - 1, self.canvas.height() - 1)
        self.display.Repaint()

    def update_status(self, message, is_error=False):
        self.predictionLabel.setText(message)
        self.predictionLabel.setProperty("error", "true" if is_error else "false")
        self.predictionLabel.style().polish(self.predictionLabel)

    def show_error(self, message):
        self.update_status(message, is_error=True)
        QMessageBox.critical(self, "错误", message)

    def add_to_history(self, mode, step_file, extra_file=None):
        record = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": f"模式{mode}",
            "step_file": os.path.basename(step_file),
            "extra_file": os.path.basename(extra_file) if extra_file else "",
            "step_path": step_file,
            "extra_path": extra_file if extra_file else "",
            "labels": self.convert_to_python_types(self.logic.get_predicted_labels()),
            "label_info": self.convert_to_python_types(self.logic.get_label_info())
        }
        self.history.append(record)

        if len(self.history) > 50:
            self.history = self.history[-50:]

    def show_history(self):
        if not self.history:
            QMessageBox.information(self, "历史记录", "没有历史记录")
            return

        dialog = HistoryDialog(self.history, self)
        dialog.exec_()

    def load_from_history(self, record):
        try:
            self.current_step_file = record["step_path"]
            self.step_loaded = True
            self.loadButton.setProperty("loaded", "true")
            self.loadButton.style().polish(self.loadButton)

            mode_num = int(record["mode"][-1])  # Extract number from "模式X"
            self.segmentation_mode = mode_num
            self.modeCombo.setCurrentIndex(mode_num - 1)
            self.update_ui_for_mode()

            self.logic.update_label_config({
                "label_names": record["label_info"]["names"],
                "colors": record["label_info"]["colors"]
            })
            self.labels_loaded = True

            self.logic.predicted_labels = np.array(record["labels"])
            self.logic.face_count = len(record["labels"])
            self.logic.label_counts = [0] * len(record["label_info"]["names"])

            labels = self.convert_to_python_types(record["labels"])
            unique, counts = np.unique(labels, return_counts=True)

            for u, c in zip(unique, counts):
                if u < len(self.logic.label_counts):
                    self.logic.label_counts[u] = c

            self.display_segmentation(record["step_path"])
            self.update_status(f"已加载历史记录: {record['time']}")

        except Exception as e:
            self.show_error(f"加载历史记录出错: {str(e)}")

    def save_history(self):
        try:
            history_path = os.path.join(os.path.expanduser("~"), ".cad_segmentation_history.json")
            with open(history_path, 'w', encoding='utf-8') as f:
                json.dump(self.convert_to_python_types(self.history), f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存历史记录出错: {str(e)}")

    def load_history(self):
        try:
            history_path = os.path.join(os.path.expanduser("~"), ".cad_segmentation_history.json")
            if os.path.exists(history_path):
                with open(history_path, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            print(f"加载历史记录出错: {str(e)}")
            self.history = []

    def closeEvent(self, event):
        self.save_history()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setFont(QFont("Microsoft YaHei", 9))
    window = SegmentationApp()
    window.show()
    sys.exit(app.exec_())