import os
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.uic import loadUi

from src.config.signal_manager import signal_manager
from src.ui.scheme_edit_widget import SchemeEditWidget
from src.ui.device_info_widget import DeviceInfoWidget
from src.config.utils import get_all_cameras, get_ip_and_port_by_camera_name, CameraConfig, get_schemes
from src.communication.camera_rpc_manager import CameraRpcManager
from thrift_interface.gen.SampleReg_Defs.ttypes import TaskInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        loadUi(ui_path, self)


        self.cameras_ip_map = None                  # 相机名称与ip的映射
        self.current_scheme = None                  # 当前方案
        self.anim = None
        self.paramStackedWidget = None              # 右侧参数页面
        self.rpc = CameraRpcManager()               # 通信单例

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
        self.init_paramStackedWidgets()

    def init_paramStackedWidgets(self):
        """
        初始化右侧参数页面
        """
        self.paramStackedWidget = QStackedWidget()
        self.paramStackedWidget.setFixedWidth(0)

        # 页面1：参数设置
        scheme_edit_wgt = SchemeEditWidget()
        self.paramStackedWidget.insertWidget(0, scheme_edit_wgt)

        # 页面2：设备列表
        device_info_wgt = DeviceInfoWidget()
        self.paramStackedWidget.insertWidget(1, device_info_wgt)

        self.paramStackedWidget.setCurrentIndex(0)
        self.contentHLayout.addWidget(self.paramStackedWidget)


    def init_slots(self):
        self.btn_edit_shceme.clicked.connect(self.handle_edit_shceme_clicked)
        self.btn_load_shceme.clicked.connect(self.handle_load_scheme_clicked)
        self.btn_switch_device.clicked.connect(self.handle_switch_device_clicked)

        signal_manager.sig_switch_device.connect(self.on_sig_switch_device)
        signal_manager.sig_close_scheme_widget.connect(self.on_close_scheme_widget)
        signal_manager.sig_connected_status.connect(self.on_connected_status)

    def show_paramStackedWidget(self, visible):
        anim = QPropertyAnimation(self.paramStackedWidget, b"minimumWidth")
        anim.setDuration(400)
        anim.setEasingCurve(QEasingCurve.InOutQuad)

        if visible:
            anim.setStartValue(0)
            anim.setEndValue(450)
        else:
            anim.setStartValue(self.paramStackedWidget.width())
            anim.setEndValue(0)

        self.btn_load_shceme.setEnabled(not visible)
        self.btn_edit_shceme.setEnabled(not visible)
        self.btn_switch_device.setEnabled(not visible)
        self.comboBox_scheme.setEnabled(not visible)

        anim.start()
        self.anim = anim  # 防止垃圾回收

        # 清除当前子控件的焦点
        if visible:
            current_page = self.paramStackedWidget.currentWidget()
            QTimer.singleShot(0, current_page.setFocus)


    def handle_load_scheme_clicked(self):
        """
        加载方案按钮槽函数
        """
        task_info = TaskInfo(
            taskId="task_001",      # ✅ 必须是字符串
            taskType=[0],           # ✅ 必须是 list
            state=0,  # ✅ i32
            mode=0,  # ✅ i32
            imageIn=None,  # ✅ optional list → None
            retCode=None,  # ✅ optional i32 → None
            imageOut=None,  # ✅ optional list → None
            result=None  # ✅ optional struct → None
        )

        self.rpc.send_task(task_info)


    def handle_edit_shceme_clicked(self):
        """
        编辑方案按钮槽函数
        """
        scheme_name = self.comboBox_scheme.currentText()
        if not scheme_name:
            return

        # 更新方案编辑页面
        scheme_edit_wgt = self.paramStackedWidget.widget(0)
        scheme_edit_wgt.refresh(self.current_camera.camera_current_scheme)

        self.paramStackedWidget.setCurrentIndex(0)
        self.show_paramStackedWidget(True)

    def on_close_scheme_widget(self):
        """
        关闭右侧编辑页面
        """
        self.show_paramStackedWidget(False)

    def handle_switch_device_clicked(self):
        """
        选择设备按钮槽函数
        """
        # 更新设备信息页面
        device_info_wgt = self.paramStackedWidget.widget(1)
        device_info_wgt.refresh(self.cameras_ip_map)

        self.paramStackedWidget.setCurrentIndex(1)
        self.show_paramStackedWidget(True)

    def on_sig_switch_device(self, name):
        """
        处理切换设备的逻辑
        name：目标设备
        """
        ip, port = get_ip_and_port_by_camera_name(name, self.cameras_ip_map)

        # 连接相机，槽函数中接收连接结果
        self.rpc.connect_camera(name, ip, port)



    def on_connected_status(self, status):
        """
        接收连接结果
        """
        ip = self.rpc.get_ip()
        port = self.rpc.get_port()
        camera_name = self.rpc.get_camera_name()
        error_msg = self.rpc.last_error()

        if not status:
            print(f"Connect Failed, {camera_name}, {ip}:{port}, {error_msg}")
            QMessageBox.critical(self, "错误", f"{camera_name}连接失败：" + error_msg)
        else:
            print(f"Connect Success, {camera_name}, {ip}:{port}")

            scheme_list = self.rpc.get_camera_camera_schemes()
            current_scheme = self.rpc.get_camera_current_scheme()

            # 更新当前设备QLabel
            self.lab_current_device.setText(camera_name)

            # 更新comboBox_scheme
            self.comboBox_scheme.clear()
            for scheme in scheme_list:
                self.comboBox_scheme.addItem(scheme.scheme_name)
            self.comboBox_scheme.setCurrentText(current_scheme.scheme_name)

            # 关闭右侧页面
            self.show_paramStackedWidget(False)







