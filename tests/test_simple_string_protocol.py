from typing import Tuple

import pytest

from pymemdb.pymemdbprotocols.extract_data_from_buffer import extract_data_from_buffer
from pymemdb.pymemdbprotocols.protocol_types import SimpleString


@pytest.mark.parametrize(
    "buffer,expected_output",
    [
        (b"+par", (None, 0)),
        (b"+ok\r\n", (SimpleString(data="ok"), 5)),
        (b"+ok\r\n+next", (SimpleString(data="ok"), 5)),
    ],
)
def test_simple_string_parser(
    buffer: bytes, expected_output: Tuple[SimpleString | None, int]
):
    actual_output = extract_data_from_buffer(buffer)
    assert actual_output == expected_output
