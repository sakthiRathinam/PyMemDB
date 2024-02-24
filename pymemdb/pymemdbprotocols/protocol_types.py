from abc import ABC
from dataclasses import dataclass


class RESPParsed(ABC):
    ...


@dataclass
class SimpleString(RESPParsed):
    data: str


@dataclass
class BulkString(RESPParsed):
    data: str


@dataclass
class Integer(RESPParsed):
    data: int


@dataclass
class Array(RESPParsed):
    data: list[RESPParsed]
