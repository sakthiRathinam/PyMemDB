from typing import List

import pytest

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbprotocols.protocol_types import BulkString, SimpleString


@pytest.mark.parametrize(
    "command,args,expected_output",
    [(BulkString(b"ping"), None, (SimpleString("pong")))],
)
def test_command_ping(
    command: BulkString, args: List[BulkString] | None, expected_output: SimpleString
) -> None:
    actual_output = handle_command(command, args)
    assert actual_output == expected_output
