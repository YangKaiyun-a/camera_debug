import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "thrift_interface", "gen")))


from thrift_interface.gen.hello import HelloService
from thrift_interface.gen.SampleReg_Interface_LC import SampleRegLC
from src.thrift_helper import ThriftService


# =========================================================
# � 服务端 Handler 实现
# =========================================================
class SimpleRegLCHandler(SampleRegLC.Iface):
    def __init__(self):
        print("✅ SimpleRegLC Server Initialized")

    def HeartbeatToLC(self, timeStamp):
        return timeStamp

    def DistributeOper(self, info):
        print("1")

    def DistributeTask(self, info):
        print("1")

    def GetTaskInfo(self):
        print("1")

    def GetDeviceInfo(self):
        print("1")

    def GetOperInfo(self):
        print("1")


class HelloHandler(HelloService.Iface):
    def __init__(self):
        print("✅ HelloService Server Initialized")

    def sayHello(self, name):
        print(f"收到客户端请求: {name}")
        return f"你好, {name}! 来自 Thrift 服务端的问候～"


# =========================================================
# � 启动 Thrift 服务
# =========================================================
def main():

    processor_1 = SampleRegLC.Processor(SimpleRegLCHandler())

    service = ThriftService([("processor_1", processor_1)], port=9090)
    service.start()



if __name__ == "__main__":
    main()


