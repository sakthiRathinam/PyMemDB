from abc import ABC, abstractmethod
from dataclasses import dataclass


class RESPParsed(ABC):
    @abstractmethod
    def resp_encode(self) -> bytes: ...

    @abstractmethod
    def cli_resp_encode(self) -> str: ...


@dataclass
class SimpleString(RESPParsed):
    data: str

    def resp_encode(self) -> bytes:
        return f"+{self.data}\r\n".encode()

    def cli_resp_encode(self) -> str:
        return self.data


@dataclass
class BulkString(RESPParsed):
    data: bytes

    def resp_encode(self) -> bytes:
        if len(self.data) == 0:
            return b"$-1\r\n"
        return f"${len(self.data)}\r\n{self.data.decode()}\r\n".encode()

    def __str__(self) -> str:
        return self.data.decode()

    def cli_resp_encode(self) -> str:
        return self.data.decode()


@dataclass
class Integer(RESPParsed):
    data: int

    def resp_encode(self) -> bytes:
        return f":{self.data}\r\n".encode()

    def cli_resp_encode(self) -> str:
        return str(self.data)


@dataclass
class SimpleError(RESPParsed):
    data: str

    def resp_encode(self) -> bytes:
        return f"-{self.data}\r\n".encode()

    def cli_resp_encode(self) -> str:
        return self.data


@dataclass
class Array(RESPParsed):
    data: list[RESPParsed]

    def resp_encode(self) -> bytes:
        stringified_array_data = f"*{len(self.data)}\r\n" + "".join(
            [resp_parsed.resp_encode().decode() for resp_parsed in self.data]
        )
        return stringified_array_data.encode()

    def cli_resp_encode(self) -> str:
        return " ".join([resp_parsed.cli_resp_encode() for resp_parsed in self.data])
