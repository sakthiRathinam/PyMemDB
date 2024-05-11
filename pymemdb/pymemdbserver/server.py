import socket

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbprotocols.protocol_types import RESPParsed
from pymemdb.pymemdbprotocols.resp_formatter import decode_data_from_buffer_to_array


class Server:
    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host
        self._active = False

    def run(self):
        self._active = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            self._server_socket = server_socket
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            conn, addr = server_socket.accept()
            self.handle_client_connection(conn)

    def handle_client_connection(self, conn: socket.socket):
        buffer = bytearray()
        while True:
            print("Waiting for data")
            data = conn.recv(1024)
            buffer.extend(data)
            frame, framesize = decode_data_from_buffer_to_array(buffer)
            print(frame, framesize)
            if frame:
                resp_object: RESPParsed = handle_command(frame)
                conn.sendall(resp_object.resp_encode())
                buffer = buffer[framesize:]


if __name__ == "__main__":
    server = Server(7000, "127.0.0.1")
    server.run()
