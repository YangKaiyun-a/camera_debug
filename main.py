import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QStackedWidget
 )

from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, qDebug

from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QRect
from src.ui.main_window import Ui_MainWindow
from src.ui.scheme_edit_widget import SchemeEditWidget
from src.ui.device_info_widget import DeviceInfoWidget



class MainWindow(QMainWindow,  Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.anim = None
        self.stackedWidget = None
        self.setupUi(self)
        self.init()


    def init(self):
        self.init_stackedWidgets()
        self.init_slots()

    def init_stackedWidgets(self):
        self.stackedWidget = QStackedWidget()
        self.stackedWidget.setFixedWidth(0)  # 默认收起

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
        anim.start()
        self.anim = anim  # 防止垃圾回收

    def on_btn_edit_shceme_clicked(self):
        self.stackedWidget.setCurrentIndex(0)
        self.show_stackedWidget(True)

    def on_btn_load_shceme_clicked(self):
        pass

    def on_btn_switch_device_clicked(self):
        self.stackedWidget.setCurrentIndex(1)
        self.show_stackedWidget(True)

    # def on_btn_modify_ip_clicked(self):
    #     if self.btn_ip.text() == "编辑":
    #         self.btn_ip.setText("保存")
    #         self.lineEdit_ip.setReadOnly(False)
    #         self.lineEdit_ip.setFocus()
    #         self.lineEdit_ip.setStyleSheet(
    #             """
    #             background-color: #ffffff;
    #             border: 1px solid #0078d7;
    #             border-radius: 4px;
    #             """
    #         )
    #     elif self.btn_ip.text() == "保存":
    #         self.lineEdit_ip.setReadOnly(True)
    #         self.lineEdit_ip.setStyleSheet(
    #             """
    #             background: transparent;
    #             border: none;
    #             """
    #         )
    #         self.btn_ip.setText("编辑")





if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())