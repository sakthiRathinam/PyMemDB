
from typing import Tuple

from pymemdb.pymemdbprotocols.protocol_factory import PROTOCOL_FACTORY
from pymemdb.pymemdbprotocols.protocol_types import Array, RESPParsed


def decode_data_from_buffer(buffer: bytes) -> Tuple[(RESPParsed | None, int)]:
    first_character = chr(buffer[0])
    parsing_func = PROTOCOL_FACTORY[first_character]
    return parsing_func(buffer)


def decode_data_from_buffer_to_array(buffer: bytes) -> Tuple[Array | None, int]:
    from pymemdb.pymemdbprotocols.protocol_parsers import array_parser
    array,array_len = array_parser(buffer)  
    return array_parser(buffer)


def encode_data_from_resp_parsed(data: RESPParsed) -> bytes:
    return data.resp_encode()