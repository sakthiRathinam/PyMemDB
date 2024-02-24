from pymemdb.pymemdbprotocols.protocol_factory import PROTOCOL_FACTORY
from pymemdb.pymemdbprotocols.protocol_types import RedisParsedData


def extract_data_from_buffer(buffer: bytes) -> RedisParsedData:
    first_character = chr(buffer[0])
    parsing_func = PROTOCOL_FACTORY[first_character]
    return parsing_func(buffer)
