import argparse
import asyncio

from pymemdb.commands.handle_command import handle_command
from pymemdb.datastructures.datastore import DataStore
from pymemdb.persistence.persister import AppendOnlyPersister
from pymemdb.protocols.protocol_types import RESPParsed
from pymemdb.protocols.resp_formatter import decode_data_from_buffer_to_array

DATASTORE = DataStore()


class RedisServerProtocol(asyncio.Protocol):
    def __init__(self, enable_aof=False):
        self.buffer = bytearray()
        self.persister = AppendOnlyPersister("appendonly.aof") if enable_aof else None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        if not data:
            self.transport.close()
        self.buffer.extend(data)
        frame, framesize = decode_data_from_buffer_to_array(self.buffer)

        if frame:
            self.buffer = self.buffer[framesize:]
            resp_object: RESPParsed = handle_command(frame, DATASTORE, self.persister)
            self.transport.write(resp_object.resp_encode())


async def run_expiry_server_loop(datastore):
    while datastore.clean_expired_keys_thread_active:
        print("here called lazy expire")
        datastore.lazy_expire()
        await asyncio.sleep(10)
        print("went out of lazy expire")


class AsyncServer(asyncio.Protocol):
    def __init__(self, port: int, host: str, enable_aof=False, start_expiry_loop=False):
        self.port = port
        self.host = host
        self._active = False
        self.aof = enable_aof
        self.start_expiry_loop = False

    async def run(self):
        self._active = True
        print(f"Server started at {self.host}:{self.port}")

        loop = asyncio.get_event_loop()
        if self.start_expiry_loop:
            loop.create_task(run_expiry_server_loop(DATASTORE))
        server = await loop.create_server(lambda: RedisServerProtocol(enable_aof=self.aof), self.host, self.port)
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
    argparser.add_argument("--appendonly", type=bool, default=False)
    argparser.add_argument("--startexpiryloop", type=bool, default=False)
    sysargs = argparser.parse_args()
    if sysargs.startexpiryloop:
        print("Info: Expiry loop started")
    if sysargs.appendonly:
        print("Info: Append Only File enabled")
    server = AsyncServer(sysargs.port, sysargs.host, sysargs.appendonly, sysargs.startexpiryloop)
    asyncio.run(server.run())
