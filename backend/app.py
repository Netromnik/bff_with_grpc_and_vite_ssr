from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from grpclib.client import Channel

from engine_template import templates
from grpc_contracts.helloworld import GreeterStub, HelloRequest, HelloReply


class LazyHttpSingleLazyObject:
    """Тест оптимизации"""
    def __init__(self):
        self._channel = None

    @property
    async def channel(self):
        if self._channel is None:
            self._channel = Channel('127.0.0.1', 50051)
        return self._channel


class LazyUnixSingleLazyObject:
    """Тест оптимизации"""
    def __init__(self):
        self._channel = None

    @property
    async def channel(self):
        if self._channel is None:
            self._channel = Channel(path='./test.sock')
        return self._channel

lazy_channel_http = LazyHttpSingleLazyObject()
lazy_channel_unix = LazyUnixSingleLazyObject()

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )


@app.get("/test", response_class=HTMLResponse)
async def read_item2(request: Request):
    return templates.TemplateResponse(
        request=request, name="index.html"
    )

@app.post('/api/echo_grpc', response_model=HelloReply)
async def echo_grpc(hello: HelloRequest):
    async with (await lazy_channel_http.channel) as channel:
        greeter_service = GreeterStub(channel=channel)
        message = await greeter_service.say_hello(hello)
    return message


@app.post('/api/echo_grpc_over_unix_socket', response_model=HelloReply)
async def echo_grpc(hello: HelloRequest):
    async with (await lazy_channel_unix.channel) as channel:
        greeter_service = GreeterStub(channel=channel)
        message = await greeter_service.say_hello(hello)
    return message


async def run():
    """ Запуск только для dev режима """
    from hypercorn.asyncio import serve
    from hypercorn.config import Config
    config = Config()
    config.bind = ["localhost:8000"]
    await serve(app, config)


if __name__ == "__main__":
    import asyncio
    asyncio.run(run())
