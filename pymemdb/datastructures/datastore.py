import dataclasses as dc
import random
import threading
import time
from collections import deque
from typing import Any, List


@dc.dataclass
class DataEntry:
    data: Any
    ttl: int = 0


def to_ns(format: str, expiry: int) -> int:
    match format.lower():
        case "ex" | "exat":
            return expiry * 10**9
        case "px" | "pxat":
            return expiry * 10**6
        case _:
            return expiry * 10**9


class DataStore:
    def __init__(self):
        self._data: dict = {}
        self._lock: threading.Lock = threading.Lock()
        self.clean_expired_keys_thread_active = True

    def __len__(self) -> int:
        return len(self._data)

    def __getitem__(self, key: Any) -> Any:
        with self._lock:
            key_value = self._data.get(key, None)
            if not key_value:
                return None
            elif key_value.ttl != 0 and key_value.ttl < time.time_ns():
                del self._data[key]
                return None
            return key_value.data

    def __setitem__(self, key: Any, value: Any) -> None:
        with self._lock:
            self._data[key] = DataEntry(value)

    def no_of_keys_exists(self, key: List[str]) -> int:
        with self._lock:
            existing_key_count = 0
            for k in key:
                if k in self._data:
                    existing_key_count += 1
            return existing_key_count

    def del_all_keys(self, key: List[str]) -> int:
        with self._lock:
            deleted_count = 0
            for k in key:
                if k in self._data:
                    del self._data[k]
                    deleted_count += 1
            return deleted_count

    def append_to_list(self, key: Any, value: List[Any]) -> int:
        with self._lock:
            if key not in self._data:
                self._data[key] = DataEntry(deque(value))
            else:
                if not isinstance(self._data[key].data, deque):
                    raise ValueError("Key is not a list")
                self._data[key].data.extend(value)
            return len(self._data[key].data)

    def prepend_to_list(self, key: Any, value: List[Any]) -> int:
        with self._lock:
            if key not in self._data:
                self._data[key] = DataEntry(deque(value))
            else:
                if not isinstance(self._data[key].data, deque):
                    raise ValueError("Key is not a list")
                self._data[key].data.extendleft(value)
            return len(self._data[key].data)

    def get_list_range(self, key: Any, start: int, end: int) -> List[Any]:
        with self._lock:
            range_list = []
            if key not in self._data:
                return []
            if not isinstance(self._data[key].data, deque):
                raise ValueError("Key is not a list")
            if end < 0:
                end = len(self._data[key].data) - abs(end)
            try:
                for index in range(start, end + 1):
                    range_list.append(self._data[key].data[index])
            except IndexError:
                pass
            return range_list

    def set_item_with_expiry(self, key: Any, value: Any, expiry: int, format: str) -> None:
        with self._lock:
            if format.lower() in ["ex", "px"]:
                expiry_in_ns: int = time.time_ns() + to_ns(format, expiry)
            else:
                expiry_in_ns = to_ns(format, expiry)
            self._data[key] = DataEntry(value, expiry_in_ns)

    def lazy_expire(self, lazy_expire_retry_percentage: int = 25) -> None:
        total_no_of_keys = 0
        cleaning_loop_is_active = True
        with self._lock:
            while cleaning_loop_is_active:
                deleted_keys = 0
                total_no_of_keys = len(self._data)
                random_keys = random.sample(list(self._data.keys()), min(20, total_no_of_keys))
                for key in random_keys:
                    if self._data[key].ttl != 0 and self._data[key].ttl < time.time_ns():
                        del self._data[key]
                        deleted_keys += 1
                        total_no_of_keys -= 1
                if (total_no_of_keys * lazy_expire_retry_percentage) // 100 > deleted_keys or total_no_of_keys == 0:
                    cleaning_loop_is_active = False

    def stop_cleaning_expired_keys_thread(self) -> None:
        self.clean_expired_keys_thread_active = False
