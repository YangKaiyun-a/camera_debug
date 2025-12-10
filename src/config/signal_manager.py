from PyQt5.QtCore import QObject, pyqtSignal



class SignalManager(QObject):

    """
    信号：切换设备
    参数1：目标设备
    """
    sig_switch_device = pyqtSignal(str)


    """
    信号：关闭右侧编辑页面
    """
    sig_close_scheme_widget = pyqtSignal()

    """
    信号：连接状态改变
    """
    sig_connected_status = pyqtSignal(str, bool)



# 实例化单例
signal_manager = SignalManager()