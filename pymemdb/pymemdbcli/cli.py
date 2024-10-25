import socket
from typing import Any

import typer

from pymemdb.pymemdbprotocols.protocol_types import Array, BulkString, RESPParsed
from pymemdb.pymemdbprotocols.resp_formatter import (
    decode_data_from_buffer,
    encode_data_from_resp_parsed,
)

DEFAULT_PORT: int = 7000
DEFAULT_SERVER: str = "127.0.0.1"
RECV_SIZE: int = 1024


def encode_command(command: str) -> RESPParsed:
    return Array([BulkString(sub_command.encode()) for sub_command in command.split()])


def get_command(server: str, port: int) -> str:
    return input(f"{server}:{port} > ")


def send_command(client_socket: socket.socket, command: str) -> None:
    convert_command: bytes = encode_data_from_resp_parsed(encode_command(command))
    client_socket.send(convert_command)


def receive_response(client_socket: socket.socket, buffer: bytearray) -> str:
    while True:
        received_buffer: Any = client_socket.recvmsg(RECV_SIZE)
        buffer.extend(received_buffer[0])
        frame, frame_size = decode_data_from_buffer(buffer)
        if frame:
            return frame.cli_resp_encode()


def main(
    server: str = DEFAULT_SERVER,
    port: int = DEFAULT_PORT,
) -> None:
    with socket.socket() as client_socket:
        client_socket.connect((server, port))
        while True:
            buffer: bytearray = bytearray()
            command: str = get_command(server, port)

            if command.lower() == "quit" or command.lower() == "exit":
                break

            if command.lower() == "clear":
                print("\033[H\033[J")
                continue

            send_command(client_socket, command)
            response: str = receive_response(client_socket, buffer)
            print(response)


if __name__ == "__main__":
    typer.run(main)
