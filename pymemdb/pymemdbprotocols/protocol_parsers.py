from typing import Tuple

from pymemdb.pymemdbprotocols.protocol_types import SimpleString

SEPERATOR = b"\r\n"


def simple_string_parser(buffer: bytes) -> Tuple[SimpleString | None, int]:
    find_offset_of_sep_start = buffer.find(SEPERATOR)
    if find_offset_of_sep_start == -1:
        return None, 0
    convert_bytes_to_str = buffer[1:find_offset_of_sep_start].decode()
    total_buffer_len = find_offset_of_sep_start + 2
    return SimpleString(data=convert_bytes_to_str), total_buffer_len
