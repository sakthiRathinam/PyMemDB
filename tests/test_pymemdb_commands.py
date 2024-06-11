import pytest

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbprotocols.protocol_types import Array, BulkString, SimpleString


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (Array([BulkString(b"ping")]), (SimpleString("PONG"))),
        (Array([BulkString(b"Ping")]), (SimpleString("PONG"))),
    ],
)
def test_command_ping(command: Array, expected_output: SimpleString) -> None:
    actual_output = handle_command(command)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (
            Array(
                [
                    BulkString(b"echo"),
                    BulkString(b"i"),
                    BulkString(b"love"),
                    BulkString(b"you"),
                ]
            ),
            Array(
                [
                    BulkString(b"i"),
                    BulkString(b"love"),
                    BulkString(b"you"),
                ]
            ),
        ),
    ],
)
def test_command_echo(command: Array, expected_output: Array) -> None:
    actual_output = handle_command(command)
    print(actual_output)
    assert actual_output == expected_output
