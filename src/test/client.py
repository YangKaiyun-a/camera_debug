import sys, os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, BASE_DIR)

GEN_DIR = os.path.join(BASE_DIR, "thrift_interface", "gen")
sys.path.insert(0, GEN_DIR)

from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift_interface.gen.SampleReg_Interface_LC import SampleRegLC
from src.thrift_helper import ThriftClient




def main():

    client = ThriftClient(
        transport_cls=TTransport.TBufferedTransport,
        protocol_cls=TBinaryProtocol.TBinaryProtocol
    )

    result_holder = {}

    # 短连接测试
    ok = client.call(
        "127.0.0.1",
        9090,
        SampleRegLC.Client,
        lambda stub: result_holder.update({
            "ret": stub.HeartbeatToLC(123456)
        })
    )

    if ok:
        print("✅ 服务端返回:", result_holder["ret"])
    else:
        print("❌ 调用失败:", client.error())

if __name__ == "__main__":
    main()
