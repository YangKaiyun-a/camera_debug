import os
import sys
from datetime import datetime

# 将 thrift 生成目录加入 sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '../thrift/gen-py'))

# 导入生成的 Thrift 接口
from hello import HelloService
from SimpleReg_Interface_UC import SimpleRegUC
from SimpleReg_Defs import ttypes as defs

from thrift_helper import ThriftService


# =========================================================
# � 服务端 Handler 实现
# =========================================================
class SimpleRegUCHandler(SimpleRegUC.Iface):
    def __init__(self):
        print("✅ SimpleRegUC Server Initialized")

    def HeartbeatToUC(self, timeStamp):
        print(f"[Heartbeat] Received at {datetime.now().strftime('%H:%M:%S')} | Timestamp: {timeStamp}")

    def DeviceInfoChanged(self, info):
        print("[DeviceInfoChanged] Device runningState =", info.runningState)
        return 0  # 返回 i32

    def TaskInfoChanged(self, info):
        print(f"[TaskInfoChanged] taskId={info.taskId}, state={info.state}")
        if info.info and info.info.barcode:
            print("  - barcode:", info.info.barcode)
        return 0  # 返回 i32


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

    processor_1 = SimpleRegUC.Processor(SimpleRegUCHandler())
    processor_2 = HelloService.Processor(HelloHandler())

    service = ThriftService([("processor_1", processor_1),("processor_2", processor_2)], port=9090)
    service.start()



if __name__ == "__main__":
    main()
