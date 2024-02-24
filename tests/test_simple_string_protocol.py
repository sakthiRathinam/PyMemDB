from typing import Any

import pytest

from pymemdb.pymemdbprotocols.extract_data_from_buffer import extract_data_from_buffer
from pymemdb.pymemdbprotocols.protocol_types import Integer, SimpleString


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
        (b":23\r\n", (Integer(data=23), 5)),  # Normal integer case
        (b":2.9\r\n", (None, 0)),
        (b":-2\r\n", (Integer(data=-2), 5)),
    ],
)
def test_number_parser(buffer: bytes, expected_output: Any) -> None:
    actual_output = extract_data_from_buffer(buffer)
    assert actual_output == expected_output
