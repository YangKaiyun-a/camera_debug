from thrift.server import TServer
from thrift.protocol import TBinaryProtocol
from thrift.transport import TSocket, TTransport
from thrift.TMultiplexedProcessor import TMultiplexedProcessor


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
