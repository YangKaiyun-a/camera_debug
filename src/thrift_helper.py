# thrift_service.py
from thrift.server import TServer
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), 'gen-py'))

from hello import HelloService

class ThriftService:
    def __init__(self, processor_list, port=9090, worker_num=8):
        """
        processor_list:  list of (service_name, processor_instance)
            eg: [("LoginService", LoginService.Processor(handler))]

        port: listen port
        worker_num: thread pool size
        """
        self.processor_list = processor_list
        self.port = port
        self.worker_num = worker_num
        self.server = None

    def start(self):
        sock = TSocket.TServerSocket(port=self.port)
        transport_factory = TTransport.TBufferedTransportFactory()
        protocol_factory = TBinaryProtocol.TBinaryProtocolFactory()

        # multiplexer
        from thrift.TMultiplexedProcessor import TMultiplexedProcessor
        mux = TMultiplexedProcessor()
        for name, proc in self.processor_list:
            mux.registerProcessor(name, proc)

        # thread pool server
        self.server = TServer.TThreadPoolServer(
            mux, sock, transport_factory, protocol_factory)
        self.server.setNumThreads(self.worker_num)

        print(f"thrift server start on {self.port}")
        self.server.serve()

    def stop(self):
        if self.server:
            print("stop server")
            self.server.stop()


class HelloHandler:
    def sayHello(self, name):
        print(f"收到客户端请求: {name}")
        return f"你好, {name}! 来自 Thrift 服务端的问候～"

if __name__ == "__main__":

    processor = HelloService.Processor(HelloHandler())

    service = ThriftService([("processor", processor)], port=9090)
    service.start()