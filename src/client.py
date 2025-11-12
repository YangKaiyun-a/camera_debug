import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gen-py'))

from hello import HelloService
from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol

# 创建连接
transport = TSocket.TSocket('localhost', 9090)
transport = TTransport.TBufferedTransport(transport)
protocol = TBinaryProtocol.TBinaryProtocol(transport)
client = HelloService.Client(protocol)
transport.open()

# 调用远程方法
response = client.sayHello("YKY")
print("服务端返回:", response)

transport.close()
