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

    info = TaskInfo(
        taskId=1,
        taskType=1,
        state=0,
        mode=0,
        imageIn=0,
        retCode=0,
        imageOut=0,
        result=0
    )

    ok = client.call(
        "127.0.0.1",
        9090,
        SampleRegLC.Client,
        lambda stub: result_holder.update({
            "ret": stub.DistributeTask(info)
        })
    )

    if ok:
        print("✅ 服务端返回:", result_holder["ret"])
    else:
        print("❌ 调用失败:", client.error())
