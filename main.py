import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from util.image_with_mouse_control import ImageWithMouseControl
from util.img_pro import Merge
import os
import shutil
from ui import ui_main_window
import config
from cut_and_detect import cut_and_detect

sys.path.append('./yolov5')
sys.path.append('./CenterNet/src')


class MainWindow(QtWidgets.QMainWindow, ui_main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        self.img_dir = None  # 切割检测后的图片路径
        self.save_dir = None
        self.img_list = None  # 图片路径下的所有图片名称数组
        self.img_name = None  # 当前显示图片的名称
        self.big_img_path = None  # 待选择的大视场原图的路径
        self.label_name = "保存的图片"
        self.pic_name_dic = {}
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle(config.app_name)
        self.setupUi(self)
        self.setListener()

    def setupUi(self, MainWindow):
        # 继承ui, 添加图片展示
        super().setupUi(self)
        self.photo = ImageWithMouseControl(self.frame)
        self.photo.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.photo.sizePolicy().hasHeightForWidth())
        self.photo.setSizePolicy(sizePolicy)
        self.photo.setTabletTracking(False)
        self.photo.setObjectName("photo")
        self.horizontalLayout.addWidget(self.photo)

    # Qt::TabFocus
    # 通过Tab键获得焦点
    # Qt::ClickFocus
    # 通过被单击获得焦点
    # Qt::StrongFocus
    # 可通过上面两种方式获得焦点
    # Qt::NoFocus
    # 不能通过上两种方式获得焦点(默认值), setFocus仍可使其获得焦点
    def setListener(self):
        # 设置强焦点事件, 只能通过TAB和鼠标获取焦点, 保证能使用空格切换图片
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        # 上面都是qt designer 自动生成的, 监听函数放在下面绑定
        self.prev_button.clicked.connect(self.prev_button_listener)
        self.next_button.clicked.connect(self.next_button_listener)

        self.action_open_big_img.triggered.connect(self.clear_and_choose_big_img_path)
        self.action_change_img_save_path.triggered.connect(self.change_img_save_path_listener)
        self.action_help.triggered.connect(self.help_listener)
        self.img_preview_list.itemActivated.connect(self.item_activated)

        # 倒数第三个按钮
        self.set_3x3_button.clicked.connect(self.set_3x3_img)

        # 开始写保存
        self.save_img_button.clicked.connect(self.save_img)

        # 倒数第二个
        self.set_5x5_button.clicked.connect(self.set_5x5_img)

    def keyReleaseEvent(self, e):
        if e.key() == QtCore.Qt.Key_Left or e.key() == QtCore.Qt.Key_Up:
            self.prev_button.click()
        if e.key() == QtCore.Qt.Key_Right or e.key() == QtCore.Qt.Key_Down:
            self.next_button.click()

    def set_img(self, path=None):
        # 绘制图像
        path = os.path.join(self.img_dir, self.img_name) if path is None else path
        # print(self.img_name.split("-")[-1].split(".")[0])

        self.photo.img = QtGui.QPixmap(path)
        self.photo.adjust_image()
        self.photo.update()
        self.img_preview_list.setCurrentRow(self.img_list.index(self.img_name))

    def set_3x3_img(self):
        path = os.path.join(self.img_dir, self.img_name)  # if path is None else path
        # print(path)
        m = Merge(path, self.img_dir, self.the_shorter_num)
        self.photo.img = m.merge3()
        self.photo.adjust_image()
        self.photo.update()

    def set_5x5_img(self):
        path = os.path.join(self.img_dir, self.img_name)  # if path is None else path
        m = Merge(path, self.img_dir, self.the_shorter_num)
        self.photo.img = m.merge5()
        self.photo.adjust_image()
        self.photo.update()

    def prev_button_listener(self):
        if self.img_dir is not None:
            index = self.img_list.index(self.img_name)

            self.img_name = self.img_list[(index - 1) % len(self.img_list)]
            self.set_img()

    def next_button_listener(self):
        if self.img_dir is not None:
            index = self.img_list.index(self.img_name)

            self.img_name = self.img_list[(index + 1) % len(self.img_list)]
            self.set_img()

    ##self.progress.reset()
    def run_cut_and_detect_cancel(self):
        if not self.cut_and_detect_finish:
            self.run_cut_and_detect_label = 0
            self.big_img_path = None
            self.choose_big_img_path()
            self.run_cut_and_detect()

    def run_cut_and_detect(self):
        self.progress = QtWidgets.QProgressDialog(self)
        self.progress.setWindowModality(QtCore.Qt.ApplicationModal)
        self.progress.setWindowTitle("请稍等")
        self.progress.setLabelText("正在识别大视场图像...")
        self.progress.setCancelButtonText("取消识别并更换图片")
        self.progress.canceled.connect(self.run_cut_and_detect_cancel)
        self.progress.resize(300, 180)
        # Qt::NonModal  非模态：正常模式,能和其它窗口交互
        # Qt::WindowModal  半模态：窗口级模态对话框，阻塞父窗口、父窗口的父窗口及兄弟窗口。
        # Qt::ApplicationModal  应用程序级模态对话框，阻塞整个应用程序的所有窗口。
        self.run_cut_and_detect_label = 1
        self.img_dir = cut_and_detect(self, chosen_model='CenterNet')
        self.open_img_dir_listener()

    def clear_and_choose_big_img_path(self):
        self.big_img_path = None  # 得加这个逻辑，否则，完成后，点更换图片，再不选图片，也会重新识别前面识别的图片
        self.open_big_img()

    # 下方两段代码不会产生递归检查，不会递归产生窗口，很棒
    def choose_big_img_path(self):
        if self.big_img_path is None:
            QtWidgets.QMessageBox.information(self.centralwidget, '注意', '请选择大视场图片')
            self.action_open_big_img.trigger()

    def open_big_img(self):
        # 在当前窗口内打开文件对话窗口
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "请选择大视场图片", os.getcwd())
        suffix = ['jpg', 'jpeg', 'bmp', 'png']
        if any(fileName.endswith(ext) for ext in suffix):
            self.big_img_path = fileName
            print('打开大视场图片:', fileName)
        self.choose_big_img_path()
        self.run_cut_and_detect()

    def check_save_dir(self):
        if self.save_dir is None:
            QtWidgets.QMessageBox.information(self.centralwidget, '注意', '请选择保存路径')
            self.action_change_img_save_path.trigger()

    def save_img(self):
        self.check_save_dir()
        if self.img_name not in os.listdir(os.path.join(self.save_dir, "保存的图片")):
            shutil.copy(os.path.join(self.img_dir, self.img_name), os.path.join(self.save_dir, "保存的图片"))

        # 可能可以不用warning，后续考虑代替
        QtWidgets.QMessageBox.warning(self, "保存成功", "保存成功！", QtWidgets.QMessageBox.Yes)

    def open_img_dir_listener(self):
        self.img_list = os.listdir(self.img_dir)
        self.img_list = sorted(self.img_list, key=lambda x: self.pic_name_dic[x], reverse=True)

        # print(self.img_list)

        # self.img_list =self.img_list[::-1]
        self.img_name = self.img_list[0]
        self.img_preview_list.clear()
        self.img_preview_list.addItems(self.img_list)
        self.set_img()
        # self.pic_name_dic = {ele.split('-')[1]: ele.split('-')[0] for ele in self.img_list}

    def change_img_save_path_listener(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, '请选择图片保存的路径')
        print('打开文件夹:', directory)
        if directory != '':
            self.save_dir = directory

        if self.save_dir is not None:
            if not os.path.exists(os.path.join(self.save_dir, self.label_name)):
                os.mkdir(os.path.join(self.save_dir, self.label_name))
        else:
            self.check_save_dir()

    def help_listener(self):
        QtWidgets.QMessageBox.information(self.centralwidget, '帮助', config.help_text)  # 后续可以进入config.help_text修改

    def item_activated(self, item):
        self.img_name = item.text()
        self.set_img()

    def closeEvent(self, e):
        reply = QtWidgets.QMessageBox.question(self, '确认退出', "是否要退出程序？",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            e.accept()
        else:
            e.ignore()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.choose_big_img_path()
    sys.exit(app.exec_())
