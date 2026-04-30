import threading

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
import time

from src.config.signal_manager import signal_manager
from src.config.utils import CameraConfig, get_schemes
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

        self.current_camera = CameraConfig()    # 当前相机的所有配置（整个程序唯一一份）
        self.connected = False                  # 连接状态
        self._heartbeat_thread = None
        self._heartbeat_running = False


    # =====================================================
    # ✅ 连接相机（建立长连接）
    # =====================================================
    def connect_camera(self, name: str, ip: str, port: int):
        self.disconnect()

        ok = self.client.init(ip, port, SampleRegLC.Client)

        if ok:
            self.current_camera.camera_name = name
            self.current_camera.camera_ip = ip
            self.current_camera.camera_port = port

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
        self.current_camera.clear()
        self.connected = False


    # =====================================================
    # ✅ 持续发送心跳
    #
    #    目前重连机制没做，因为当前采用一个客户端长连接模式，
    #    重连机制需要重新创建新客户端，适合短连接模式
    # =====================================================
    def _heartbeat_loop(self):

        while self._heartbeat_running:
            timestamp = int(time.time() * 1000)

            ok = self.client.call_inner(
                lambda stub: stub.HeartbeatToLC(timestamp)
            )

            if ok:
                if not self.connected:
                    self.connected = True

                    # 填充 CameraConfig 结构体，获取其方案等数据
                    current_scheme, scheme_list = get_schemes(self.current_camera.camera_name)
                    self.current_camera.camera_current_scheme = current_scheme
                    self.current_camera.camera_schemes = scheme_list

                    signal_manager.sig_connected_status.emit(True)
            else:
                self._heartbeat_running = False
                signal_manager.sig_connected_status.emit(False)
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

        if ok:
            print("✅ 调用成功:")
        else:
            print("❌ 调用失败:")

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
        return self.current_camera.camera_name

    # =====================================================
    # ✅ 获取相机首选方案
    # =====================================================
    def get_camera_current_scheme(self):
        return self.current_camera.camera_current_scheme


    # =====================================================
    # ✅ 获取相机所有方案
    # =====================================================
    def get_camera_camera_schemes(self):
        return self.current_camera.camera_schemes


    # =====================================================
    # ✅ 获取相机IP
    # =====================================================
    def get_ip(self):
        return self.current_camera.camera_ip


    # =====================================================
    # ✅ 获取相机端口
    # =====================================================
    def get_port(self):
        return self.current_camera.camera_port
