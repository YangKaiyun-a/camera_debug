from PyQt5.QtCore import QObject, pyqtSignal



class SignalManager(QObject):

    """
    信号：切换设备
    参数1：切换 or 取消
    """
    sig_switch_device = pyqtSignal(bool)


    """
    信号：编辑方案
    参数1：保存 or 取消
    """
    sig_edit_scheme = pyqtSignal(bool)



# 实例化单例
signal_manager = SignalManager()