from abc import ABC, abstractmethod
from dataclasses import dataclass


class RESPParsed(ABC):
    @abstractmethod
    def resp_encode(self) -> bytes:
        ...


@dataclass
class SimpleString(RESPParsed):
    data: str

    def resp_encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()


@dataclass
class BulkString(RESPParsed):
    data: bytes

    def resp_encode(self) -> bytes:
        return f"${len(self.data)}\r\n{self.data.decode()}\r\n".encode()


@dataclass
class Integer(RESPParsed):
    data: int

    def resp_encode(self) -> bytes:
        return f":{self.data}\r\n".encode()


@dataclass
class SimpleError(RESPParsed):
    data: str

    def resp_encode(self) -> bytes:
        return f"-{self.data}\r\n".encode()


@dataclass
class Array(RESPParsed):
    data: list[RESPParsed]

    def resp_encode(self) -> bytes:
        stringified_array_data = f"*{len(self.data)}\r\n" + "".join(
            [resp_parsed.resp_encode().decode() for resp_parsed in self.data]
        )
        return stringified_array_data.encode()
