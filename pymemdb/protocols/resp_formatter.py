from typing import Tuple

from pymemdb.protocols.protocol_factory import PROTOCOL_FACTORY
from pymemdb.protocols.protocol_types import Array, RESPParsed


def decode_data_from_buffer(buffer: bytes) -> Tuple[(RESPParsed | None, int)]:
    first_character = chr(buffer[0])
    parsing_func = PROTOCOL_FACTORY[first_character]
    return parsing_func(buffer)


def decode_data_from_buffer_to_array(buffer: bytes) -> Tuple[Array | None, int]:
    from pymemdb.protocols.protocol_parsers import array_parser

    return array_parser(buffer)


def encode_data_from_resp_parsed(data: RESPParsed) -> bytes:
    return data.resp_encode()
