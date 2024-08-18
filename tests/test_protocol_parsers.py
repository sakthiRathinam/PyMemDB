from typing import Any

import pytest

from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    Integer,
    RESPParsed,
    SimpleError,
    SimpleString,
)
from pymemdb.pymemdbprotocols.resp_formatter import (
    decode_data_from_buffer,
    encode_data_from_resp_parsed,
)


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b"+par", (None, 0)),
        (b"+ok\r\n", (SimpleString(data="ok"), 5)),
        (b"+ok\r\n+next", (SimpleString(data="ok"), 5)),
    ],
)
def test_simple_string_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = decode_data_from_buffer(buffer)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b":23\r\n", (Integer(data=23), 5)),
        (b":2.9\r\n", (None, 0)),
        (b":-2\r\n", (Integer(data=-2), 5)),
    ],
)
def test_number_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = decode_data_from_buffer(buffer)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b"$5\r\nhello\r\n", (BulkString(data=b"hello"), 11)),
        (b"$5n\r\nhello\r\n", (None, 0)),
        (b"$5\r\nhelloooo\r\n", (None, 0)),
    ],
)
def test_bulk_string_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = decode_data_from_buffer(buffer)
    assert actual_output == expected_output


group_of_bulk_strings = b"*2\r\n$4\r\necho\r\n$5\r\nworld\r\n"

group_of_bulk_strings_and_numbers = b"*3\r\n:3\r\n$4\r\necho\r\n$5\r\nworld\r\n"

everything_mixed = b"*5\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\necho\r\n$5\r\nworld\r\n"

corrupted_data = b"*5\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\nechoo\r\n$5\r\nworld\r\n"

wrong_array_len = b"*0\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\nechoo\r\n$5\r\nworld\r\n"

wrong_array_len_part_two = (
    b"*3\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\necho\r\n$5\r\nworld\r\n"
)

group_of_arrays = b"*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$4\r\nsave\r\n*3\r\n$6\r\nCONFIG\r\n$3\r\nGET\r\n$10\r\nappendonly\r\n"


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (
            group_of_bulk_strings,
            (
                Array(data=[BulkString(data=b"echo"), BulkString(data=b"world")]),
                len(group_of_bulk_strings),
            ),
        ),
        (
            group_of_bulk_strings_and_numbers,
            (
                Array(
                    data=[
                        Integer(data=3),
                        BulkString(data=b"echo"),
                        BulkString(data=b"world"),
                    ]
                ),
                len(group_of_bulk_strings_and_numbers),
            ),
        ),
        (
            everything_mixed,
            (
                Array(
                    data=[
                        Integer(data=3),
                        Integer(data=-5),
                        SimpleString(data="this was fun"),
                        BulkString(data=b"echo"),
                        BulkString(data=b"world"),
                    ]
                ),
                len(everything_mixed),
            ),
        ),
        (
            corrupted_data,
            (
                None,
                0,
            ),
        ),
        (
            wrong_array_len,
            (
                None,
                0,
            ),
        ),
        (
            wrong_array_len_part_two,
            (
                None,
                0,
            ),
        ),
    ],
)
def test_array_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = decode_data_from_buffer(buffer)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b"-par", (None, 0)),
        (b"-Error message\r\n", (SimpleError(data="Error message"), 16)),
    ],
)
def test_simple_error_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = decode_data_from_buffer(buffer)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "resp_parsed,expected_output",
    [
        (
            SimpleError(data="Error message"),
            b"-Error message\r\n",
        ),
        (Integer(data=23), b":23\r\n"),
        (SimpleString(data="ok"), b"+ok\r\n"),
        (
            BulkString(data=b"hello"),
            b"$5\r\nhello\r\n",
        ),
        (
            Array(
                data=[
                    Integer(data=3),
                    Integer(data=-5),
                    SimpleString(data="this was fun"),
                    BulkString(data=b"echo"),
                    BulkString(data=b"world"),
                ]
            ),
            everything_mixed,
        ),
    ],
)
def test_protocol_encoders(resp_parsed: RESPParsed, expected_output: bytes):
    actual_output = encode_data_from_resp_parsed(resp_parsed)
    assert actual_output == expected_output


def test_group_of_arrays_parsing():
    buffer = group_of_arrays
    expected_output = [
        Array(
            data=[
                BulkString(data=b"CONFIG"),
                BulkString(data=b"GET"),
                BulkString(data=b"save"),
            ]
        ),
        Array(
            data=[
                BulkString(data=b"CONFIG"),
                BulkString(data=b"GET"),
                BulkString(data=b"appendonly"),
            ]
        ),
    ]
    first_array, frame_size = decode_data_from_buffer(buffer)
    assert first_array == expected_output[0]
    buffer = buffer[frame_size:]
    second_array, frame_size = decode_data_from_buffer(buffer)
    assert second_array == expected_output[1]
