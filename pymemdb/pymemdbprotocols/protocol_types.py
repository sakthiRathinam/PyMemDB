from abc import ABC
from dataclasses import dataclass


class RedisParsedData(ABC):
    ...


@dataclass
class SimpleString(RedisParsedData):
    data: str
