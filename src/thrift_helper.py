from thrift.Thrift import TException
from thrift.server import TServer
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport, THttpClient


class ThriftService:
    """
    单端口 = 单 Service
    TBufferedTransport + TBinaryProtocol
    线程池模型
    """

    def __init__(self, processor, port=9090, worker_num=8):
        """
        processor: 单个 Thrift Processor，例如 SampleRegLC.Processor(handler)
        port: 服务端口
        worker_num: 线程池大小
        """
        self.processor = processor
        self.port = port
        self.worker_num = worker_num
        self.server = None

    def start(self):
        try:
            sock = TSocket.TServerSocket(port=self.port)
            transport_factory = TTransport.TBufferedTransportFactory()
            protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

            # 线程池服务器
            self.server = TServer.TThreadPoolServer(
                self.processor,
                sock,
                transport_factory,
                protocol_factory
            )

            self.server.setNumThreads(self.worker_num)

            print(f"✅ thrift server start on {self.port}")
            self.server.serve()

        except TException as e:
            print("❌ Thrift server exception:", e)
        except Exception as e:
            print("❌ Unknown error:", e)

    def stop(self):
        if self.server:
            print("🛑 stop server")
            self.server.stop()



class ThriftClient:
    """
    支持 Transport / Protocol 可配置
    支持短连接 / 长连接
    """

    def __init__(self,
                 transport_cls=TTransport.TBufferedTransport,
                 protocol_cls=TBinaryProtocol.TBinaryProtocol):
        """
        :param transport_cls: 传输层类型 (TBufferedTransport / TFramedTransport / THttpClient)
        :param protocol_cls:  协议类型 (TBinaryProtocol / TCompactProtocol / TJSONProtocol)
        """
        self.transport_cls = transport_cls
        self.protocol_cls = protocol_cls

        self.socket = None
        self.transport = None
        self.protocol = None
        self.stub = None
        self.error_msg = ""

    # ==============================
    # ✅ 短连接模式（一次调用一次连接）
    # ==============================
    def call(self, host: str, port: int, stub_cls, fn):
        """
        :param host: 服务器 IP
        :param port: 端口
        :param stub_cls: Thrift 生成的 Client 类，如 SampleRegLC.Client
        :param fn: lambda stub: stub.xxx()
        """
        if self.init(host, port, stub_cls):
            ok = self.call_inner(fn)
            self.release()
            return ok
        return False

    # ==============================
    # 初始化
    # ==============================
    def init(self, host: str, port: int, stub_cls):
        self.release()
        self.error_msg = ""

        try:
            # -------- Transport 选择 --------
            if self.transport_cls == THttpClient.THttpClient:
                # HTTP 模式
                self.transport = self.transport_cls(host, port)
            else:
                # TCP Socket 模式
                self.socket = TSocket.TSocket(host, port)
                self.transport = self.transport_cls(self.socket)

            # -------- Protocol 选择 --------
            self.protocol = self.protocol_cls(self.transport)

            # -------- 打开连接 --------
            self.transport.open()

            # -------- 创建 Stub --------
            self.stub = stub_cls(self.protocol)
            return True

        except TException as e:
            self.error_msg = str(e)
        except Exception as e:
            self.error_msg = f"Unknown error: {e}"

        self.release()
        return False

    # ==============================
    # ✅ 长连接调用
    # ==============================
    def call_inner(self, fn):
        if not self.stub:
            self.error_msg = "stub is not initialized"
            return False

        try:
            fn(self.stub)
            return True

        except TException as e:
            self.error_msg = str(e)
        except Exception as e:
            self.error_msg = f"Unknown error: {e}"

        return False

    # ==============================
    # 释放连接
    # ==============================
    def release(self):
        try:
            if self.transport:
                self.transport.close()
        except Exception:
            pass

        self.socket = None
        self.transport = None
        self.protocol = None
        self.stub = None

    def error(self):
        return self.error_msg
