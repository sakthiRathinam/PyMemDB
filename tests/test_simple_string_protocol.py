from typing import Any

import pytest

from pymemdb.pymemdbprotocols.extract_data_from_buffer import extract_data_from_buffer
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    Integer,
    SimpleError,
    SimpleString,
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
    actual_output = extract_data_from_buffer(buffer)
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
    actual_output = extract_data_from_buffer(buffer)
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
    actual_output = extract_data_from_buffer(buffer)
    assert actual_output == expected_output


group_of_bulk_strings = b"*2\r\n$4\r\necho\r\n$5\r\nworld\r\n"

group_of_bulk_strings_and_numbers = b"*3\r\n:3\r\n$4\r\necho\r\n$5\r\nworld\r\n"

everything_mixed = b"*5\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\necho\r\n$5\r\nworld\r\n"

corrupted_data = b"*5\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\nechoo\r\n$5\r\nworld\r\n"

wrong_array_len = b"*0\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\nechoo\r\n$5\r\nworld\r\n"

wrong_array_len_part_two = (
    b"*3\r\n:3\r\n:-5\r\n+this was fun\r\n$4\r\necho\r\n$5\r\nworld\r\n"
)


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
    actual_output = extract_data_from_buffer(buffer)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b"-par", (None, 0)),
        (b"-Error message\r\n", (SimpleError(data="Error message"), 16)),
    ],
)
def test_simple_error_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = extract_data_from_buffer(buffer)
    assert actual_output == expected_output
