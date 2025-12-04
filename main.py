import os
import sys

from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow





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

    try:
        qss_path = os.path.join(os.path.dirname(__file__), "src/style/style.qss")
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print("Failed to load QSS:", e)

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())