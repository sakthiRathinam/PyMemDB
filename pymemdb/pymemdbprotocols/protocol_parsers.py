from typing import Tuple

from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    Integer,
    SimpleError,
    SimpleString,
)

SEPERATOR = b"\r\n"


def simple_string_parser(buffer: bytes) -> Tuple[SimpleString | None, int]:
    find_offset_of_sep_start = buffer.find(SEPERATOR)
    if find_offset_of_sep_start == -1:
        return None, 0
    convert_bytes_to_str = buffer[1:find_offset_of_sep_start].decode()
    total_buffer_len = find_offset_of_sep_start + 2
    return SimpleString(data=convert_bytes_to_str), total_buffer_len


def number_parser(buffer: bytes) -> Tuple[Integer | None, int]:
    find_offset_of_sep_start = buffer.find(SEPERATOR)
    if find_offset_of_sep_start == -1:
        return None, 0
    convert_bytes_to_str = buffer[1:find_offset_of_sep_start].decode()
    total_buffer_len = find_offset_of_sep_start + 2
    try:
        convert_str_to_int = int(convert_bytes_to_str)
        return Integer(data=convert_str_to_int), total_buffer_len
    except ValueError:
        return None, 0


def get_length_from_first_sep(buffer: bytes) -> Tuple[int, int]:
    try:
        find_first_sep_offset = buffer.find(SEPERATOR)
        get_bulk_string_buffer_len = buffer[1:find_first_sep_offset].decode()
        buffer_string_len = int(get_bulk_string_buffer_len)
        return find_first_sep_offset, buffer_string_len
    except ValueError:
        return -1, -1


def bulk_string_parser(buffer: bytes) -> Tuple[BulkString | None, int]:
    try:
        first_separator_offset, buffer_string_len = get_length_from_first_sep(buffer)
        if buffer_string_len == -1:
            return BulkString(data=b""), 5
        bulk_string_bytes_start_offset = first_separator_offset + 2
        bulk_string_bytes_end_offset = (
            bulk_string_bytes_start_offset + buffer_string_len
        )
        if (
            buffer[bulk_string_bytes_end_offset : bulk_string_bytes_end_offset + 2]
            != SEPERATOR
        ):
            return None, 0
        bulk_string_bytes = buffer[
            bulk_string_bytes_start_offset:bulk_string_bytes_end_offset
        ]
        return BulkString(data=bulk_string_bytes), bulk_string_bytes_end_offset + 2
    except Exception as E:
        print(f"Parsed breaked due to this {E}")
        return None, 0


def array_parser(buffer: bytes) -> Tuple[Array | None, int]:
    from pymemdb.pymemdbprotocols.protocol_factory import PROTOCOL_FACTORY

    parsed_array = []
    try:
        first_separator_offset, array_len = get_length_from_first_sep(buffer)
        if array_len == 0:
            return None, 0
        seperator = first_separator_offset + 2
        for _ in range(array_len):
            first_character = chr(buffer[seperator])
            parsing_func = PROTOCOL_FACTORY[first_character]
            next_item, next_offset = parsing_func(buffer[seperator:])
            print(parsed_array)
            if next_item is None:
                return None, 0
            parsed_array.append(next_item)
            seperator += next_offset
        return Array(data=parsed_array), seperator
    except Exception as E:
        print(f"Parsed breaked due to this {E}")
        return None, 0


def simple_error_parser(buffer: bytes) -> Tuple[SimpleError | None, int]:
    find_offset_of_sep_start = buffer.find(SEPERATOR)
    if find_offset_of_sep_start == -1:
        return None, 0
    convert_bytes_to_str = buffer[1:find_offset_of_sep_start].decode()
    total_buffer_len = find_offset_of_sep_start + 2
    return SimpleError(data=convert_bytes_to_str), total_buffer_len
