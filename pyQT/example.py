from PyQt5.QtCore import QDateTime, QTimer, Qt
from PyQt5.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QVBoxLayout,
                             QGroupBox, QLabel, QCheckBox, QRadioButton, QComboBox, QLineEdit, QTextEdit, QDialog,
                             QPushButton, QSlider, QScrollBar, QSpinBox, QTableWidget, QStyleFactory, QSizePolicy,
                             QWidget)


class WidgetGallery(QDialog):

    def __init__(self, parent=None):
        # 设置自定义样式
        super(WidgetGallery, self).__init__(parent)
        self.originalPalette = QApplication.palette()
        # 标题
        self.setWindowTitle('基本组件')
        # 初始化其他组件
        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomRightGroupBox()

        # 下拉列表
        style_combobox = QComboBox()
        style_combobox.addItems(QStyleFactory.keys())

        # 标签
        style_label = QLabel('样式')
        style_label.setBuddy(style_combobox)

        self.use_stander_checkbox = QCheckBox('使用标准样式')
        self.use_stander_checkbox.setChecked(True)

        disable_widget_checkbox = QCheckBox('禁用组件')

        # 顶端布局组件
        top_layout = QHBoxLayout()
        top_layout.addWidget(style_label)  # 标签
        top_layout.addWidget(style_combobox)  # 下拉列表
        top_layout.addWidget(self.use_stander_checkbox)  # 下拉列表
        top_layout.addWidget(disable_widget_checkbox)  # 检查单选框

        # 网格布局
        main_layout = QGridLayout()
        main_layout.addLayout(top_layout, 0, 0, 1, 2)  # 将顶端布局组件放在网格布局里的第0行第0列的位置
        main_layout.addWidget(self.top_left_group, 1, 0)
        main_layout.addWidget(self.top_right_group, 1, 1)
        main_layout.addWidget(self.bottom_left_group, 2, 0)

        # 把网格布局呈现出来
        self.setLayout(main_layout)

    # 第一组 基本组件
    def createTopLeftGroupBox(self):
        self.top_left_group = QGroupBox('第一组')

        radioButtion1 = QRadioButton('单选框1')
        radioButtion2 = QRadioButton('单选框2')
        radioButtion3 = QRadioButton('单选框3')
        checkBox = QCheckBox('Tri_state checkbox')
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)
        # 垂直布局
        layout = QVBoxLayout()
        layout.addWidget(radioButtion1)
        layout.addWidget(radioButtion2)
        layout.addWidget(radioButtion3)
        layout.addWidget(checkBox)

        self.top_left_group.setLayout(layout)

    # 第二组 基本组件
    def createTopRightGroupBox(self):
        self.top_right_group = QGroupBox('第二组')

        default_botton = QPushButton('默认Button')
        default_botton.setDefault(True)

        toggle_button = QPushButton('开关Button')
        toggle_button.setCheckable(True)
        toggle_button.setChecked(True)

        flat_button = QPushButton('FlatButton')
        flat_button.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(default_botton)
        layout.addWidget(toggle_button)
        layout.addWidget(flat_button)

        self.top_right_group.setLayout(layout)

    # 第三组 基本组件
    def createBottomRightGroupBox(self):
        self.bottom_left_group = QTableWidget()
        self.bottom_left_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Ignored)
        # 标签
        tab1 = QWidget()
        table_widget = QTableWidget(10, 10)
        tab1h_box = QHBoxLayout()
        tab1h_box.addWidget(table_widget)
        tab1.setLayout(tab1h_box)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
