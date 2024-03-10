import socket
from typing import Annotated

import typer

from pymemdb.pymemdbprotocols.protocol_types import Array, BulkString, RESPParsed
from pymemdb.pymemdbprotocols.resp_formatter import (
    decode_data_from_buffer,
    encode_data_from_resp_parsed,
)

DEFAULT_PORT = 6379
DEFAULT_SERVER = "127.0.0.1"
RECV_SIZE = 1024


def encode_command(command: str) -> RESPParsed:
    return Array([BulkString(sub_command.encode()) for sub_command in command.split()])


def main(
    server: Annotated[str, typer.Argument()] = DEFAULT_SERVER,
    port: Annotated[int, typer.Argument] = DEFAULT_PORT,
) -> None:
    with socket.socket() as client_socket:
        client_socket.connect((server, port))
        buffer = bytearray()
        while True:
            command = input(f"{server}:{port}>")

            if command.lower() == "quit":
                break

            convert_command = encode_data_from_resp_parsed(encode_command(command))
            client_socket.send(convert_command)

            while True:
                recieved_buffer = client_socket.recvmsg(RECV_SIZE)
                buffer.extend(recieved_buffer[0])
                frame, frame_size = decode_data_from_buffer(buffer)
                if frame:
                    buffer = buffer[frame_size:]
                    print(frame.resp_encode().decode())
                    break


if __name__ == "__main__":
    typer.run(main)
