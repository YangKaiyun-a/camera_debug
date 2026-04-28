import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "thrift_interface", "gen")))
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

GEN_DIR = os.path.join(BASE_DIR, "thrift_interface", "gen")
sys.path.insert(0, GEN_DIR)


from thrift_interface.gen.SampleReg_Interface_LC import SampleRegLC
from src.thrift_helper import ThriftService


# =========================================================
# � 下位机服务端 Handler 实现
# =========================================================
class SimpleRegLCHandler(SampleRegLC.Iface):
    def __init__(self):
        print("✅ SimpleRegLC Server Initialized")

    def HeartbeatToLC(self, timeStamp):
        # print("Received heartbeat ", timeStamp)
        pass

    def DistributeOper(self, info):
        print("🛠 收到通用操作:", info)
        return 0

    def DistributeTask(self, info):
        print("📦 收到任务:", info.taskId)
        return 0

    def GetTaskInfo(self):
        print("1")

    def GetDeviceInfo(self):
        print("1")

    def GetOperInfo(self):
        print("1")



# =========================================================
# � 启动下位机 Thrift 服务
# =========================================================
def main():
    processor = SampleRegLC.Processor(SimpleRegLCHandler())

    service = ThriftService(
        processor=processor,
        port=9090,
        # worker_num=8
    )

    service.start()



if __name__ == "__main__":
    main()


