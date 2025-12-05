import os
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QTimer
from PyQt5.uic import loadUi


from src.config.signal_manager import signal_manager
from src.ui.scheme_edit_widget import SchemeEditWidget
from src.ui.device_info_widget import DeviceInfoWidget
from src.config.utils import SchemeConfig
from src.config.utils import DEFAULT_SCHEME_DIR
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 加载 UI 文件
        ui_path = os.path.join(os.path.dirname(__file__), "main_window.ui")
        loadUi(ui_path, self)

        self.current_scheme = None      # 当前方案
        self.anim = None
        self.stackedWidget = None

        self.init()


    def init(self):
        self.init_Data()
        self.init_UI()
        self.init_slots()
        self.setFocus()

    def init_Data(self):
        # TODO: 当前从软件目录获取方案，后续应该从相机中获取
        for filename in os.listdir(DEFAULT_SCHEME_DIR):
            if filename.endswith(".json"):
                scheme_name = filename[:-5]  # 去掉 .json
                self.comboBox_scheme.addItem(scheme_name)

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

    def load_scheme_from_file(self, json_path):
        """
        从 JSON 文件读取方案并转成 SchemeConfig
        """
        if not os.path.exists(json_path):
            return None

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return SchemeConfig(
            exposure_time=data.get("exposure_time", 0),
            gain=data.get("gain", 0),
            focal_length_step=data.get("focal_length_step", 0),
            focal_point=data.get("focal_point", 0),

            white_balance_R=data.get("white_balance_R", ""),
            white_balance_G=data.get("white_balance_G", ""),
            white_balance_B=data.get("white_balance_B", ""),

            tools=data.get("tools", []),
            image_path=data.get("image_path", ""),

            scheme_name=data.get("scheme_name", ""),
            scheme_path=data.get("scheme_path", "")
        )

    def on_btn_load_shceme_clicked(self):
        """
        加载方案
        """
        self.stackedWidget.setCurrentIndex(0)
        self.show_stackedWidget(True)

    def on_btn_edit_shceme_clicked(self):
        """
        编辑方案按钮槽函数
        """
        scheme_name = self.comboBox_scheme.currentText()
        if not scheme_name:
            return

        # JSON 文件路径
        json_path = os.path.join(DEFAULT_SCHEME_DIR, scheme_name + ".json")

        # 加载 SchemeConfig
        self.current_scheme = self.load_scheme_from_file(json_path)

        # 更新右侧编辑页面
        scheme_edit_wgt = self.stackedWidget.widget(0)
        scheme_edit_wgt.refresh(self.current_scheme)

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
