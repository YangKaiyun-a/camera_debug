from PyQt5 import QtWidgets
from src.config.signal_manager import signal_manager
from src.config.utils import get_ip_and_port_by_camera_name


class DeviceInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lab_ip_value = None        # IP地址
        self.cameras_ip_map = None
        self.combo_device = None
        self.btn_cancel = None
        self.btn_ok = None
        self.init()

    def init(self):
        self.init_data()
        self.init_ui()
        self.init_slots()
        self.setFocus()


    def init_data(self):
        pass

    def init_ui(self):
        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet(
            """
            background-color: #e8e8e8; 
            """
        )

        lab_device = QtWidgets.QLabel()
        lab_device.setText("设备列表")
        self.combo_device = QtWidgets.QComboBox()
        hlayout_1 = QtWidgets.QHBoxLayout()
        hlayout_1.addWidget(lab_device)
        hlayout_1.addWidget(self.combo_device)

        lab_name = QtWidgets.QLabel()
        lab_name.setText("网卡")
        lab_name_value = QtWidgets.QLabel()
        lab_name_value.setText("ASIX USB to Gigabit Ethenet")
        hlayout_2 = QtWidgets.QHBoxLayout()
        hlayout_2.addWidget(lab_name)
        hlayout_2.addWidget(lab_name_value)

        lab_device_name = QtWidgets.QLabel()
        lab_device_name.setText("设备名称")
        lab_device_name_value = QtWidgets.QLabel()
        lab_device_name_value.setText("---")
        hlayout_3 = QtWidgets.QHBoxLayout()
        hlayout_3.addWidget(lab_device_name)
        hlayout_3.addWidget(lab_device_name_value)

        lab_mac = QtWidgets.QLabel()
        lab_mac.setText("物理地址")
        lab_mac_value = QtWidgets.QLabel()
        lab_mac_value.setText("34:BD:20:6B:61:14")
        hlayout_4 = QtWidgets.QHBoxLayout()
        hlayout_4.addWidget(lab_mac)
        hlayout_4.addWidget(lab_mac_value)

        lab_ip = QtWidgets.QLabel()
        lab_ip.setText("IP地址")
        self.lab_ip_value = QtWidgets.QLabel()
        self.lab_ip_value.setText("192.168.127.12")
        hlayout_5 = QtWidgets.QHBoxLayout()
        hlayout_5.addWidget(lab_ip)
        hlayout_5.addWidget(self.lab_ip_value)

        lab_subnet_mask = QtWidgets.QLabel()
        lab_subnet_mask.setText("子网掩码")
        lab_subnet_mask_value = QtWidgets.QLabel()
        lab_subnet_mask_value.setText("255.255.255.0")
        hlayout_6 = QtWidgets.QHBoxLayout()
        hlayout_6.addWidget(lab_subnet_mask)
        hlayout_6.addWidget(lab_subnet_mask_value)

        lab_gateway = QtWidgets.QLabel()
        lab_gateway.setText("网关")
        lab_gateway_value = QtWidgets.QLabel()
        lab_gateway_value.setText("192.168.127.1")
        hlayout_6 = QtWidgets.QHBoxLayout()
        hlayout_6.addWidget(lab_gateway)
        hlayout_6.addWidget(lab_gateway_value)

        self.btn_ok = QtWidgets.QPushButton()
        self.btn_ok.setText("连接")
        self.btn_cancel = QtWidgets.QPushButton()
        self.btn_cancel.setText("取消")
        hlayout_7 = QtWidgets.QHBoxLayout()
        hlayout_7.addWidget(self.btn_ok)
        hlayout_7.addWidget(self.btn_cancel)

        # 主布局
        main_vlayout = QtWidgets.QVBoxLayout(main_widget)
        main_vlayout.setSpacing(20)
        main_vlayout.setContentsMargins(9, 9, 9, 0)
        main_vlayout.addLayout(hlayout_1)
        main_vlayout.addLayout(hlayout_2)
        main_vlayout.addLayout(hlayout_3)
        main_vlayout.addLayout(hlayout_4)
        main_vlayout.addLayout(hlayout_5)
        main_vlayout.addLayout(hlayout_6)
        main_vlayout.addLayout(hlayout_7)
        main_vlayout.addStretch(1)

        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(main_widget)
        
    def init_slots(self):
        self.btn_ok.clicked.connect(self.on_btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_clicked)

    def refresh(self, cameras_ip_map):
        """
        刷新页面
        """
        self.combo_device.clear()
        self.cameras_ip_map = cameras_ip_map
        for name in self.cameras_ip_map:
            self.combo_device.addItem(name)

    def on_btn_ok_clicked(self):
        """
        连接按钮槽函数
        """
        signal_manager.sig_switch_device.emit(self.combo_device.currentText())

    def on_btn_cancel_clicked(self):
        """
        取消按钮槽函数
        """
        signal_manager.sig_close_scheme_widget.emit()
