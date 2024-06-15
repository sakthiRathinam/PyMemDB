import pytest

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    SimpleError,
    SimpleString,
)


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (Array([BulkString(b"ping")]), (SimpleString("PONG"))),
        (Array([BulkString(b"Ping")]), (SimpleString("PONG"))),
    ],
)
def test_command_ping(command: Array, expected_output: SimpleString) -> None:
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
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
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
    print(actual_output)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (
            Array(
                [
                    BulkString(b"set"),
                    BulkString(b"whoami"),
                    BulkString(b"database-lover"),
                ]
            ),
            SimpleString("OK"),
        ),
        (
            Array(
                [
                    BulkString(b"set"),
                    BulkString(b"whoami"),
                ]
            ),
            SimpleError("Length of set command should be 3"),
        ),
    ],
)
def test_command_set(command: Array, expected_output: Array) -> None:
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
    print(actual_output)
    assert actual_output == expected_output
