from PyQt5 import QtWidgets
from src.signal_manager import signal_manager


class SchemeEditWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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

        lab_exposure_time = QtWidgets.QLabel()
        lab_exposure_time.setText("曝光时间")
        spin_exposure_time = QtWidgets.QSpinBox()
        hlayout_1 = QtWidgets.QHBoxLayout()
        hlayout_1.addWidget(lab_exposure_time)
        hlayout_1.addWidget(spin_exposure_time)

        lab_add = QtWidgets.QLabel()
        lab_add.setText("增益")
        spin_add = QtWidgets.QSpinBox()
        hlayout_2 = QtWidgets.QHBoxLayout()
        hlayout_2.addWidget(lab_add)
        hlayout_2.addWidget(spin_add)

        lab_focal_length = QtWidgets.QLabel()
        lab_focal_length.setText("焦距步进")
        spin_focal_length = QtWidgets.QSpinBox()
        hlayout_3 = QtWidgets.QHBoxLayout()
        hlayout_3.addWidget(lab_focal_length)
        hlayout_3.addWidget(spin_focal_length)

        lab_focal_point = QtWidgets.QLabel()
        lab_focal_point.setText("焦点位置")
        spin_focal_point = QtWidgets.QSpinBox()
        hlayout_4 = QtWidgets.QHBoxLayout()
        hlayout_4.addWidget(lab_focal_point)
        hlayout_4.addWidget(spin_focal_point)

        lab_white_balance = QtWidgets.QLabel()
        lab_white_balance.setText("白平衡参数")
        btn_white_balance = QtWidgets.QPushButton()
        btn_white_balance.setText("自动调节")
        hlayout_5 = QtWidgets.QHBoxLayout()
        hlayout_5.addWidget(lab_white_balance)
        hlayout_5.addWidget(btn_white_balance)

        lab_white_balance_R = QtWidgets.QLabel()
        lab_white_balance_R.setText("R")
        edit_white_balance_R = QtWidgets.QLineEdit()
        lab_white_balance_G = QtWidgets.QLabel()
        lab_white_balance_G.setText("G")
        edit_white_balance_G = QtWidgets.QLineEdit()
        lab_white_balance_B = QtWidgets.QLabel()
        lab_white_balance_B.setText("B")
        edit_white_balance_B = QtWidgets.QLineEdit()
        hlayout_6 = QtWidgets.QHBoxLayout()
        hlayout_6.addWidget(lab_white_balance_R)
        hlayout_6.addWidget(edit_white_balance_R)
        hlayout_6.addWidget(lab_white_balance_G)
        hlayout_6.addWidget(edit_white_balance_G)
        hlayout_6.addWidget(lab_white_balance_B)
        hlayout_6.addWidget(edit_white_balance_B)

        self.btn_ok = QtWidgets.QPushButton()
        self.btn_ok.setText("保存")
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

    def on_btn_ok_clicked(self):
        """
        切换按钮槽函数
        """
        signal_manager.sig_edit_scheme.emit(True)

    def on_btn_cancel_clicked(self):
        """
        取消按钮槽函数
        """
        signal_manager.sig_edit_scheme.emit(False)