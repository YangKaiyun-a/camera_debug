import os
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.uic import loadUi


from src.signal_manager import signal_manager
from src.ui.scheme_edit_widget import SchemeEditWidget
from src.ui.device_info_widget import DeviceInfoWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        loadUi(ui_path, self)

        self.anim = None
        self.stackedWidget = None

        self.init()


    def init(self):
        self.init_stackedWidgets()
        self.init_slots()

        self.setFocus()

    def init_stackedWidgets(self):
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setFixedWidth(0)

        # 页面1：参数设置
        scheme_edit_wgt = SchemeEditWidget()
        self.stackedWidget.insertWidget(0, scheme_edit_wgt)

        # 页面2：设备列表
        device_info_wgt = DeviceInfoWidget()
        self.stackedWidget.insertWidget(1, device_info_wgt)

        self.stackedWidget.setCurrentIndex(0)
        self.contentHLayout.addWidget(self.stackedWidget)


    def init_slots(self):
        self.btn_edit_shceme.clicked.connect(self.on_btn_edit_shceme_clicked)
        self.btn_load_shceme.clicked.connect(self.on_btn_load_shceme_clicked)
        self.btn_switch_device.clicked.connect(self.on_btn_switch_device_clicked)

        signal_manager.sig_switch_device.connect(self.on_sig_switch_device)
        signal_manager.sig_edit_scheme.connect(self.on_sig_edit_scheme)

    def show_stackedWidget(self, visible):
        anim = QPropertyAnimation(self.stackedWidget, b"minimumWidth")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.InOutQuad)

        if visible:
            anim.setStartValue(0)
            anim.setEndValue(450)
        else:
            anim.setStartValue(self.stackedWidget.width())
            anim.setEndValue(0)

        self.btn_load_shceme.setEnabled(not visible)
        self.btn_edit_shceme.setEnabled(not visible)
        self.btn_switch_device.setEnabled(not visible)
        self.comboBox_scheme.setEnabled(not visible)

        anim.start()
        self.anim = anim  # 防止垃圾回收

        # 清除当前子控件的焦点
        if visible:
            current_page = self.stackedWidget.currentWidget()
            QTimer.singleShot(0, current_page.setFocus)

    def on_btn_load_shceme_clicked(self):
        """
        加载方案
        TODO: 加载方案
        """
        pass

    def on_btn_edit_shceme_clicked(self):
        """
        编辑方案
        """
        self.stackedWidget.setCurrentIndex(0)
        self.show_stackedWidget(True)

    def on_sig_edit_scheme(self, result):
        """
        处理编辑方案的结果
        参数1：保存/取消
        TODO: 保存编辑好的方案
        """
        # 关闭右侧页面
        self.show_stackedWidget(False)

    def on_btn_switch_device_clicked(self):
        """
        切换设备
        """
        self.stackedWidget.setCurrentIndex(1)
        self.show_stackedWidget(True)

    def on_sig_switch_device(self, result):
        """
        处理切换设备的结果
        参数1：切换/取消
        TODO: 切换设备逻辑
        """
        # 关闭右侧页面
        self.show_stackedWidget(False)
