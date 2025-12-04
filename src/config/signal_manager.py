from PyQt5.QtCore import QObject, pyqtSignal



class SignalManager(QObject):

    """
    信号：切换设备
    参数1：切换 or 取消
    """
    sig_switch_device = pyqtSignal(bool)


    """
    信号：关闭右侧编辑页面
    参数1：保存 or 取消
    """
    sig_close_scheme_widget = pyqtSignal()



# 实例化单例
signal_manager = SignalManager()