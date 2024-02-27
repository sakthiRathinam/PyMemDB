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
        return b""


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
        return b""
