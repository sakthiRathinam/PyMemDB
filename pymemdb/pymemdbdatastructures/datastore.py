import threading


class DataStore:
    def __init__(self):
        self._data = {}
        self._lock = threading.Lock()

    def __getitem__(self, key):
        with self._lock:
            return self._data.get(key, None)

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value
