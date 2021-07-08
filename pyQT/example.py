from PyQt5.QtCore import QDateTime, QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QLabel, QCheckBox, QRadioButton, QComboBox, QLineEdit, QTextEdit, QDialog,
                             QPushButton, QSlider, QScrollBar, QSpinBox, QTableWidget, QStyleFactory)


class WidgetGallery(QDialog):

    def __init__(self, parent=None):
        # 设置自定义样式
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()

        # 下拉列表
        style_combobox = QComboBox()
        style_combobox.addItems(QStyleFactory.keys())

        # 标签
        style_label = QLabel('样式')
        style_label.setBuddy(style_combobox)

        self.use_stander_checkox = QCheckBox('使用标准样式')
        self.use_stander_checkox.setChecked(True)

        disable_widget_checkbox = QCheckBox('禁用组件')

        # 顶端布局组件
        top_layout = QHBoxLayout()
        top_layout.addWidget(style_label)
        top_layout.addWidget(style_combobox)
        top_layout.addWidget(self.use_stander_checkox)
        top_layout.addWidget(disable_widget_checkbox)

        self.setLayout(top_layout)
        self.setWindowTitle('基本组件')


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
