import os


class AppendOnlyPersister:
    def __init__(self, path):
        self.path = path
        self._file = open(path, mode="ab", buffering=0)

    def log_command_to_file(self, data):
        self._file.write(f"*{len(data)}\r\n".encode())
        for item in data:
            self._file.write(item.resp_encode())

    def exists(self):
        return os.path.exists(self.path)

    def remove(self):
        os.remove(self.path)

    def close(self):
        self._file.close()
