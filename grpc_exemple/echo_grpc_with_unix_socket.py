import asyncio
from grpc_contracts.helloworld import GreeterBase, HelloRequest, HelloReply
from grpclib.server import Server


class EchoService(GreeterBase):
    async def say_hello(self, echo_request: HelloRequest) -> "HelloReply":
        return HelloReply(message=echo_request.name)

async def main():
    server = Server([EchoService()])
    await server.start(path="./test.sock")
    await server.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
