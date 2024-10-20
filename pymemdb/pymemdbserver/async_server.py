import argparse
import asyncio

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import RESPParsed
from pymemdb.pymemdbprotocols.resp_formatter import decode_data_from_buffer_to_array

_DATASTORE = DataStore()


class RedisServerProtocol(asyncio.Protocol):
    def __init__(self):
        self.buffer = bytearray()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if not data:
            self.transport.close()
        print(data, "data received")
        self.buffer.extend(data)
        print(self.buffer, "buffer")
        frame, framesize = decode_data_from_buffer_to_array(self.buffer)

        if frame:
            self.buffer = self.buffer[framesize:]
            print(self.buffer, "buffer after frame")
            resp_object: RESPParsed = handle_command(frame, _DATASTORE)
            print(resp_object.resp_encode())
            self.transport.write(resp_object.resp_encode())


async def run_expiry_server_loop(datastore):
    while datastore.clean_expired_keys_thread_active:
        print("here called lazy expire")
        datastore.lazy_expire()
        await asyncio.sleep(10)
        print("went out of lazy expire")


class AsyncServer(asyncio.Protocol):
    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host
        self._active = False

    async def run(self):
        self._active = True
        print(f"Server started at {self.host}:{self.port}")

        loop = asyncio.get_event_loop()
        # loop.create_task(run_expiry_server_loop(_DATASTORE))
        server = await loop.create_server(lambda: RedisServerProtocol(), self.host, self.port)
        try:
            async with server:
                await server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._active = False
            server.close()
            await server.wait_closed()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--port", type=int, default=7000)
    argparser.add_argument("--host", type=str, default="127.0.0.1")
    sysargs = argparser.parse_args()
    server = AsyncServer(sysargs.port, sysargs.host)
    asyncio.run(server.run())
