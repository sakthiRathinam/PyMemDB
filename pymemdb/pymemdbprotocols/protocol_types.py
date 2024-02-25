from abc import ABC
from dataclasses import dataclass


class RESPParsed(ABC):
    ...


@dataclass
class SimpleString(RESPParsed):
    data: str


@dataclass
class BulkString(RESPParsed):
    data: bytes


@dataclass
class Integer(RESPParsed):
    data: int


@dataclass
class SimpleError(RESPParsed):
    data: str


@dataclass
class Array(RESPParsed):
    data: list[RESPParsed]
