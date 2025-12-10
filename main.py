import os
import sys

# 导入 thrift_interface 包路径
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, BASE_DIR)
GEN_DIR = os.path.join(BASE_DIR, "thrift_interface", "gen")
sys.path.insert(0, GEN_DIR)



# print("========== 路径调试信息 ==========")
#
# # 当前 sys.path
# print("\n当前 sys.path：")
# for p in sys.path:
#     print("  ", p)
#
# print("================================")


from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow



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