import pytest

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbprotocols.protocol_types import Array, BulkString, SimpleString


@pytest.mark.parametrize(
    "command,expected_output",
    [(Array([BulkString(b"ping")]), (SimpleString("pong")))],
)
def test_command_ping(command: Array, expected_output: SimpleString) -> None:
    actual_output = handle_command(command)
    assert actual_output == expected_output
