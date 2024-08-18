import argparse
import socket
import threading

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import RESPParsed
from pymemdb.pymemdbprotocols.resp_formatter import decode_data_from_buffer_to_array


class Server:
    def __init__(self, port: int, host: str):
        self.port = port
        self.host = host
        self.datastore = DataStore()
        self._active = False

    def run(self):
        self._active = True
        print(f"Server started at {self.host}:{self.port}")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                self._server_socket = server_socket
                server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server_socket.bind((self.host, self.port))
                server_socket.listen()
                while self._active:
                    print("Waiting for connection")
                    conn, addr = server_socket.accept()
                    print("Connected by", addr)
                    threading.Thread(
                        target=self.handle_client_connection, args=(conn,)
                    ).start()
        except OSError as e:
            print(e)

        finally:
            self._active = False
            self._server_socket.close()

    def handle_client_connection(self, conn: socket.socket):
        buffer = bytearray()
        try:
            while True:
                print("Waiting for data")
                data = conn.recv(1024)
                print(data)
                if not data:
                    break
                buffer.extend(data)
                frame, framesize = decode_data_from_buffer_to_array(buffer)
                print(frame, framesize)
                if frame:
                    buffer = buffer[framesize:]
                    resp_object: RESPParsed = handle_command(frame, self.datastore)
                    print(resp_object)
                    conn.sendall(resp_object.resp_encode())
        finally:
            conn.close()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--port", type=int, default=7000)
    argparser.add_argument("--host", type=str, default="127.0.0.1")
    sysargs = argparser.parse_args()
    server = Server(sysargs.port, sysargs.host)
    server.run()
