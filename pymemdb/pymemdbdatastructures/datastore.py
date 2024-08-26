import dataclasses as dc
import threading
import time
from typing import Any


@dc.dataclass
class DataEntry:
    data: Any
    ttl: int = 0


def to_ns(format: str, expiry: int) -> int:
    match format.lower():
        case "ex":
            return expiry * 10**9
        case "px":
            return expiry * 10**6
        case _:
            return expiry * 10**9


class DataStore:
    def __init__(self):
        self._data: dict = {}
        self._lock: threading.Lock = threading.Lock()

    def __getitem__(self, key: Any) -> Any:
        with self._lock:
            key_value = self._data.get(key, None)
            if not key_value:
                return None
            elif key_value is not None and key_value.ttl < time.time_ns():
                del self._data[key]
                return None
            return key_value.data

    def __setitem__(self, key: Any, value: Any) -> None:
        with self._lock:
            self._data[key] = DataEntry(value)

    def set_item_with_expiry(
        self, key: Any, value: Any, expiry: int, format: str
    ) -> None:
        with self._lock:
            expiry_in_ns: int = time.time_ns() + to_ns(format, expiry)
            self._data[key] = DataEntry(value, expiry_in_ns)

    def lazy_expire(self):
        with self._lock:
            for key, value in self._data.items():
                if value.ttl < time.time_ns():
                    del self._data[key]
