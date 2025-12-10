from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from thrift_interface.gen.SampleReg_Defs.ttypes import TaskInfo
from thrift_interface.gen.SampleReg_Interface_LC import SampleRegLC
from src.thrift_helper import ThriftClient


def test_distribute():
    client = ThriftClient(
        transport_cls=TTransport.TBufferedTransport,
        protocol_cls=TBinaryProtocol.TBinaryProtocol
    )

    result_holder = {}

    ok = client.call(
        "127.0.0.1",
        9090,
        SampleRegLC.Client,
        lambda stub: result_holder.update({
            "ret": stub.HeartbeatToLC(11)
        })
    )

    if ok:
        print("✅ 心跳发送成功（通信正常）")
    else:
        print("❌ 心跳发送失败:", client.error())

