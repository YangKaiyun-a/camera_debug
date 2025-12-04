from PyQt5 import QtWidgets, QtCore


from src.signal_manager import signal_manager



class CollapsibleSection(QtWidgets.QWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent)

        # 三角按钮
        self.toggle_button = QtWidgets.QToolButton(text=title, checkable=True)
        self.toggle_button.setStyleSheet("QToolButton { border: none; }")
        self.toggle_button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.toggle_button.setArrowType(QtCore.Qt.RightArrow)
        self.toggle_button.setChecked(False)
        self.toggle_button.clicked.connect(self.on_toggled)

        # 内容区域
        self.content_area = QtWidgets.QWidget()
        self.content_area.setVisible(False)

        # 布局
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.toggle_button)
        main_layout.addWidget(self.content_area)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(2)

        self.inner_layout = QtWidgets.QVBoxLayout(self.content_area)
        self.inner_layout.setContentsMargins(15, 5, 5, 5)
        self.inner_layout.setSpacing(5)

    def addWidget(self, w):
        self.inner_layout.addWidget(w)

    def on_toggled(self):
        checked = self.toggle_button.isChecked()
        self.toggle_button.setArrowType(
            QtCore.Qt.DownArrow if checked else QtCore.Qt.RightArrow
        )
        self.content_area.setVisible(checked)






class SchemeEditWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lab_path = None                    # 存图路径
        self.btn_path = None
        self.tool_checkboxes = None             # 收集所有工具
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
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)

        # 主布局
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)

        # 滚动主页面
        main_widget = QtWidgets.QWidget()
        main_widget.setStyleSheet(
            """
            background-color: #e8e8e8;
            """
        )
        scroll.setWidget(main_widget)

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


        # 可折叠工具组
        tools_group = CollapsibleSection("选择工具")
        # 动态添加工具
        self.tool_checkboxes = []
        for i in range(20):
            cb = QtWidgets.QCheckBox(f"工具 {i + 1}")
            self.tool_checkboxes.append(cb)
            tools_group.addWidget(cb)


        # 存图路径
        self.btn_path = QtWidgets.QPushButton()
        self.btn_path.setFixedSize(90, 25)
        self.btn_path.setText("选择存图路径")
        self.lab_path = QtWidgets.QLabel()
        self.lab_path.setText("存图路径")
        hlayout_7 = QtWidgets.QHBoxLayout()
        hlayout_7.addWidget(self.btn_path)
        hlayout_7.addWidget(self.lab_path)


        self.btn_ok = QtWidgets.QPushButton()
        self.btn_ok.setText("保存")
        self.btn_cancel = QtWidgets.QPushButton()
        self.btn_cancel.setText("取消")
        hlayout_8 = QtWidgets.QHBoxLayout()
        hlayout_8.addWidget(self.btn_ok)
        hlayout_8.addWidget(self.btn_cancel)

        # 滚动页面主布局
        main_vlayout = QtWidgets.QVBoxLayout(main_widget)
        main_vlayout.setSpacing(20)
        main_vlayout.setContentsMargins(9, 9, 9, 9)
        main_vlayout.addLayout(hlayout_1)
        main_vlayout.addLayout(hlayout_2)
        main_vlayout.addLayout(hlayout_3)
        main_vlayout.addLayout(hlayout_4)
        main_vlayout.addLayout(hlayout_5)
        main_vlayout.addLayout(hlayout_6)
        main_vlayout.addLayout(hlayout_7)
        main_vlayout.addWidget(tools_group)
        main_vlayout.addLayout(hlayout_8)
        main_vlayout.addStretch(1)


    def init_slots(self):
        self.btn_ok.clicked.connect(self.on_btn_ok_clicked)
        self.btn_cancel.clicked.connect(self.on_btn_cancel_clicked)
        self.btn_path.clicked.connect(self.on_btn_path_clicked)

    def on_btn_ok_clicked(self):
        """
        保存按钮槽函数
        """
        signal_manager.sig_edit_scheme.emit(True)

    def on_btn_cancel_clicked(self):
        """
        取消按钮槽函数
        """
        signal_manager.sig_edit_scheme.emit(False)

    def on_btn_path_clicked(self):
        """
        选择路径按钮槽函数（选择文件夹）
        """
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            "",
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if folder:
            self.lab_path.setText(folder)


