import threading

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time

from src.config.signal_manager import signal_manager
from src.thrift_helper import ThriftClient
from thrift_interface.gen.SampleReg_Interface_LC import SampleRegLC


class CameraRpcManager:
    """
    相机 Thrift 通信 单例管理器
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CameraRpcManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_inited"):   # 防止重复初始化
            return

        self._inited = True
        self.client = ThriftClient(
            transport_cls=TTransport.TBufferedTransport,
            protocol_cls=TBinaryProtocol.TBinaryProtocol
        )

        self.camera_name = None
        self.ip = None
        self.port = None
        self.connected = False                  # 连接状态
        self.failed_count = 0                   # 心跳失败次数
        self._heartbeat_thread = None
        self._heartbeat_running = False


    # =====================================================
    # ✅ 连接相机（建立长连接）
    # =====================================================
    def connect_camera(self, name: str, ip: str, port: int):
        self.disconnect()

        ok = self.client.init(ip, port, SampleRegLC.Client)

        if ok:
            self.camera_name = name
            self.ip = ip
            self.port = port

            # 启动心跳线程
            self._heartbeat_running = True
            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop,
                daemon=True
            )
            self._heartbeat_thread.start()
        else:
            signal_manager.sig_connected_status.emit(name, False)

    # =====================================================
    # ✅ 断开连接，必须保证所有资源全部清空
    # =====================================================
    def disconnect(self):
        self._heartbeat_running = False
        self.client.release()
        self.camera_name = None
        self.ip = None
        self.port = None
        self.connected = False
        self.failed_count = 0

    # =====================================================
    # ✅ 持续发送心跳
    # =====================================================
    def _heartbeat_loop(self):
        while self._heartbeat_running:
            timestamp = int(time.time() * 1000)

            ok = self.client.call_inner(
                lambda stub: stub.HeartbeatToLC(timestamp)
            )

            if ok:
                print("心跳成功")
                if not self.connected:
                    self.connected = True
                    self.failed_count = 0
                    signal_manager.sig_connected_status.emit(self.camera_name, True)
            else:
                self.failed_count += 1
                if self.failed_count >= 3:
                    self._heartbeat_running = False
                    signal_manager.sig_connected_status.emit(self.camera_name, False)
                    self.disconnect()
                    return

            time.sleep(1)

    # =====================================================
    # ✅ 下发任务
    # =====================================================
    def send_task(self, task_info) -> bool:
        if not self.connected:
            return False

        ok = self.client.call_inner(
            lambda stub: stub.DistributeTask(task_info)
        )

        if not ok:
            self.connected = False

        return ok

    # =====================================================
    # ✅ 查询任务状态
    # =====================================================
    def get_task_info(self):
        if not self.connected:
            return False

        result_holder = {}

        ok = self.client.call_inner(
            lambda stub: result_holder.update({
                "ret": stub.GetTaskInfo()
            })
        )

        if not ok:
            self.connected = False
            return None

        return result_holder["ret"]

    # =====================================================
    # ✅ 查询设备状态
    # =====================================================
    def get_device_info(self):
        if not self.connected:
            return False

        result_holder = {}

        ok = self.client.call_inner(
            lambda stub: result_holder.update({
                "ret": stub.GetDeviceInfo()
            })
        )

        if not ok:
            self.connected = False
            return None

        return result_holder["ret"]

    # =====================================================
    # ✅ 获取错误信息
    # =====================================================
    def last_error(self):
        return self.client.error()

    # =====================================================
    # ✅ 获取相机名称
    # =====================================================
    def get_camera_name(self):
        return self.camera_name

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port
