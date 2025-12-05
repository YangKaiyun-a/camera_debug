from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

from src.config.signal_manager import signal_manager
from src.config.utils import SchemeConfig, save_scheme_config
from thrift_interface.gen.SampleReg_Defs import ttypes



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
        self.scheme = SchemeConfig()               # 保存结构体
        self.edit_white_balance_B = None        # B
        self.edit_white_balance_G = None        # G
        self.edit_white_balance_R = None        # R
        self.spin_focal_point = None            # 焦点位置
        self.spin_focal_length = None           # 焦距步进
        self.spin_add = None                    # 增益
        self.spin_exposure_time = None          # 曝光时间
        self.lab_image_path = None              # 存图路径
        self.btn_image_path = None
        self.tool_checkboxes = []             # 收集所有工具
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
        self.spin_exposure_time = QtWidgets.QSpinBox()
        self.spin_exposure_time.setValue(self.scheme.exposure_time)
        hlayout_1 = QtWidgets.QHBoxLayout()
        hlayout_1.addWidget(lab_exposure_time)
        hlayout_1.addWidget(self.spin_exposure_time)

        lab_add = QtWidgets.QLabel()
        lab_add.setText("增益")
        self.spin_add = QtWidgets.QSpinBox()
        self.spin_add.setValue(self.scheme.gain)
        hlayout_2 = QtWidgets.QHBoxLayout()
        hlayout_2.addWidget(lab_add)
        hlayout_2.addWidget(self.spin_add)

        lab_focal_length = QtWidgets.QLabel()
        lab_focal_length.setText("焦距步进")
        self.spin_focal_length = QtWidgets.QSpinBox()
        self.spin_focal_length.setValue(self.scheme.focal_length_step)
        hlayout_3 = QtWidgets.QHBoxLayout()
        hlayout_3.addWidget(lab_focal_length)
        hlayout_3.addWidget(self.spin_focal_length)

        lab_focal_point = QtWidgets.QLabel()
        lab_focal_point.setText("焦点位置")
        self.spin_focal_point = QtWidgets.QSpinBox()
        self.spin_focal_point.setValue(self.scheme.focal_point)
        hlayout_4 = QtWidgets.QHBoxLayout()
        hlayout_4.addWidget(lab_focal_point)
        hlayout_4.addWidget(self.spin_focal_point)

        lab_white_balance = QtWidgets.QLabel()
        lab_white_balance.setText("白平衡参数")
        btn_white_balance = QtWidgets.QPushButton()
        btn_white_balance.setText("自动调节")
        hlayout_5 = QtWidgets.QHBoxLayout()
        hlayout_5.addWidget(lab_white_balance)
        hlayout_5.addWidget(btn_white_balance)

        lab_white_balance_R = QtWidgets.QLabel()
        lab_white_balance_R.setText("R")
        self.edit_white_balance_R = QtWidgets.QLineEdit()
        self.edit_white_balance_R.setText(self.scheme.white_balance_R)
        lab_white_balance_G = QtWidgets.QLabel()
        lab_white_balance_G.setText("G")
        self.edit_white_balance_G = QtWidgets.QLineEdit()
        self.edit_white_balance_G.setText(self.scheme.white_balance_G)
        lab_white_balance_B = QtWidgets.QLabel()
        lab_white_balance_B.setText("B")
        self.edit_white_balance_B = QtWidgets.QLineEdit()
        self.edit_white_balance_B.setText(self.scheme.white_balance_B)
        hlayout_6 = QtWidgets.QHBoxLayout()
        hlayout_6.addWidget(lab_white_balance_R)
        hlayout_6.addWidget(self.edit_white_balance_R)
        hlayout_6.addWidget(lab_white_balance_G)
        hlayout_6.addWidget(self.edit_white_balance_G)
        hlayout_6.addWidget(lab_white_balance_B)
        hlayout_6.addWidget(self.edit_white_balance_B)


        # 可折叠工具组
        tools_group = CollapsibleSection("选择工具")
        for value, name in ttypes.TaskType._VALUES_TO_NAMES.items():
            cb = QtWidgets.QCheckBox(name)
            cb.enum_value = value
            self.tool_checkboxes.append(cb)
            tools_group.addWidget(cb)


        # 存图路径
        self.btn_image_path = QtWidgets.QPushButton()
        self.btn_image_path.setFixedSize(90, 25)
        self.btn_image_path.setText("选择存图路径")
        self.lab_image_path = QtWidgets.QLabel()
        self.lab_image_path.setText("存图路径")
        hlayout_7 = QtWidgets.QHBoxLayout()
        hlayout_7.addWidget(self.btn_image_path)
        hlayout_7.addWidget(self.lab_image_path)


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
        self.btn_image_path.clicked.connect(self.on_btn_image_path_clicked)

    def refresh(self, scheme):
        """
        刷新页面
        """
        if not isinstance(scheme, SchemeConfig):
            return

        self.scheme = scheme  # 更新内部结构体

        # ----------- 更新数值控件 -----------
        self.spin_exposure_time.setValue(scheme.exposure_time)
        self.spin_add.setValue(scheme.gain)
        self.spin_focal_length.setValue(scheme.focal_length_step)
        self.spin_focal_point.setValue(scheme.focal_point)

        # ----------- 白平衡 -----------
        self.edit_white_balance_R.setText(scheme.white_balance_R)
        self.edit_white_balance_G.setText(scheme.white_balance_G)
        self.edit_white_balance_B.setText(scheme.white_balance_B)

        # ----------- 更新存图路径 -----------
        self.lab_image_path.setText(scheme.image_path)

        # ----------- 更新工具勾选状态 -----------
        tools_set = set(scheme.tools or [])

        for cb in self.tool_checkboxes:
            cb.setChecked(cb.enum_value in tools_set)

        # 强制刷新 UI
        self.update()

    def on_btn_ok_clicked(self):
        """
        保存按钮槽函数
        """
        # 组合结构体
        self.scheme.exposure_time = self.spin_exposure_time.value()
        self.scheme.gain = self.spin_add.value()
        self.scheme.focal_length_step = self.spin_focal_length.value()
        self.scheme.focal_point = self.spin_focal_point.value()

        self.scheme.white_balance_R = self.edit_white_balance_R.text()
        self.scheme.white_balance_G = self.edit_white_balance_G.text()
        self.scheme.white_balance_B = self.edit_white_balance_B.text()

        selected_tools = [ cb.enum_value for cb in self.tool_checkboxes if cb.isChecked()]
        self.scheme.tools = selected_tools
        self.scheme.image_path = self.lab_image_path.text()

        # 保存
        ok, msg = save_scheme_config(self.scheme)

        if ok:
            QMessageBox.information(self, "成功", "方案保存成功")
            signal_manager.sig_close_scheme_widget.emit()
        else:
            QMessageBox.critical(self, "保存失败", "方案保存失败")


    def on_btn_cancel_clicked(self):
        """
        取消按钮槽函数
        """
        signal_manager.sig_close_scheme_widget.emit()

    def on_btn_image_path_clicked(self):
        """
        选择存图路径按钮槽函数
        """
        folder = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "选择文件夹",
            "",
            QtWidgets.QFileDialog.ShowDirsOnly
        )

        if folder:
            self.lab_image_path.setText(folder)


