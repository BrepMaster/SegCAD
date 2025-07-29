# history_dialog.py
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt


class HistoryDialog(QDialog):
    def __init__(self, history_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("处理历史记录")
        self.resize(800, 600)
        self.parent_ref = parent  # 保存父窗口引用

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.clearButton = QPushButton("清除历史记录")
        self.clearButton.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        self.clearButton.clicked.connect(self.clear_history)
        button_layout.addWidget(self.clearButton)

        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a6fa5;
                color: white;
                padding: 5px 15px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a7fb5;
            }
        """)
        close_btn.clicked.connect(self.close)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["时间", "模式", "STEP文件", "附加文件", "操作"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #d1d9e6;
                border-radius: 4px;
            }
            QHeaderView::section {
                background-color: #f0f4f8;
                padding: 5px;
                border: none;
            }
        """)
        main_layout.addWidget(self.table, 1)  # 添加伸缩因子使表格占据剩余空间

        self.history_data = history_data
        self.populate_table()

    def populate_table(self):
        """填充表格数据"""
        self.table.setRowCount(len(self.history_data))
        for row, item in enumerate(self.history_data):
            self.table.setItem(row, 0, QTableWidgetItem(item["time"]))
            self.table.setItem(row, 1, QTableWidgetItem(item["mode"]))
            self.table.setItem(row, 2, QTableWidgetItem(item["step_file"]))
            self.table.setItem(row, 3, QTableWidgetItem(item["extra_file"]))

            btn = QPushButton("查看")
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4a6fa5;
                    color: white;
                    padding: 3px 8px;
                    border-radius: 3px;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #5a7fb5;
                }
            """)
            btn.clicked.connect(lambda _, r=row: self.view_result(r))
            self.table.setCellWidget(row, 4, btn)

    def view_result(self, row):
        self.parent_ref.load_from_history(self.history_data[row])
        self.close()

    def clear_history(self):
        """清除历史记录"""
        reply = QMessageBox.question(
            self, '确认',
            '确定要清除所有历史记录吗？此操作不可撤销！',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.history_data.clear()
            self.parent_ref.history.clear()  # 同时清除父窗口的历史记录
            self.populate_table()  # 刷新表格显示
            self.parent_ref.save_history()  # 保存空历史到文件

            QMessageBox.information(
                self, '完成',
                '历史记录已清除',
                QMessageBox.Ok
            )