import os
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.uic import loadUi


from src.config.signal_manager import signal_manager
from src.ui.scheme_edit_widget import SchemeEditWidget
from src.ui.device_info_widget import DeviceInfoWidget
from src.config.utils import get_all_cameras, get_ip_and_port_by_camera_name, CameraConfig, get_schemes
from src.config.utils import load_camera_and_scheme_config
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载 UI 文件

        ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        loadUi(ui_path, self)
        self.cameras_ip_map = None                  # 相机名称与ip的映射
        self.current_camera = CameraConfig()        # 当前相机配置
        self.current_scheme = None                  # 当前方案
        self.anim = None
        self.stackedWidget = None

        self.init()


    def init(self):
        self.init_Data()
        self.init_UI()
        self.init_slots()
        self.setFocus()

    def init_Data(self):
        """
        获取所有相机的名称、ip、端口
        """
        self.cameras_ip_map = get_all_cameras()


    def init_UI(self):
        self.init_stackedWidgets()

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
        signal_manager.sig_close_scheme_widget.connect(self.on_close_scheme_widget)

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
        """
        pass

    def on_btn_edit_shceme_clicked(self):
        """
        编辑方案按钮槽函数
        """
        scheme_name = self.comboBox_scheme.currentText()
        if not scheme_name:
            return

        # 更新方案编辑页面
        scheme_edit_wgt = self.stackedWidget.widget(0)
        scheme_edit_wgt.refresh(self.current_camera.camera_current_scheme)

        self.stackedWidget.setCurrentIndex(0)
        self.show_stackedWidget(True)

    def on_close_scheme_widget(self):
        """
        关闭右侧编辑页面
        """
        self.show_stackedWidget(False)

    def on_btn_switch_device_clicked(self):
        """
        切换设备按钮槽函数
        """
        # 更新设备信息页面
        device_info_wgt = self.stackedWidget.widget(1)
        device_info_wgt.refresh(self.cameras_ip_map)

        self.stackedWidget.setCurrentIndex(1)
        self.show_stackedWidget(True)

    def on_sig_switch_device(self, name):
        """
        处理切换设备的结果
        result：切换/取消
        """
        ip, port = get_ip_and_port_by_camera_name(name, self.cameras_ip_map)
        current_scheme, scheme_list = get_schemes(name)

        print(f"切换设备为：{name}, ip:{ip}, port:{port}")

        self.current_camera.camera_name = name
        self.current_camera.camera_ip = ip
        self.current_camera.camera_port = port
        self.current_camera.camera_current_scheme = current_scheme
        self.current_camera.camera_scheme_list = scheme_list

        # 刷新方案下拉框
        self.comboBox_scheme.clear()
        for scheme_config in scheme_list:
            self.comboBox_scheme.addItem(scheme_config.scheme_name)

        self.comboBox_scheme.setCurrentText(current_scheme.scheme_name)

        # 关闭右侧页面
        self.show_stackedWidget(False)
