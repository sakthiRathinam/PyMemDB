import socket

from ..pymemdbprotocols.resp_formatter import decode_data_from_buffer


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
            server_socket.bind((self.port, self.host))
            server_socket.listen()
            conn, addr = server_socket.accept()
            self.handle_client_connection(conn)

    def handle_client_connection(self, conn: socket.socket):
        buffer = bytearray()
        while True:
            data = conn.recv(1024)
            buffer.extend(data)
            frame, framesize = decode_data_from_buffer(buffer)
            if frame:
                buffer = buffer[framesize:]
