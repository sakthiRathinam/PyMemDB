from typing import List, Tuple, Union

import pytest

from pymemdb.pymemdbcommands.handle_command import handle_command
from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    Integer,
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
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "command,expected_output,expected_output_data",
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
            "database-lover",
        ),
        (
            Array(
                [
                    BulkString(b"set"),
                    BulkString(b"whoami"),
                ]
            ),
            SimpleError("Length of set command should be 3 or 5"),
            None,
        ),
    ],
)
def test_command_set(
    command: Array,
    expected_output: SimpleString | SimpleError,
    expected_output_data: str | None,
) -> None:
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    assert datastore[str(command.data[1])] == expected_output_data


@pytest.mark.parametrize(
    "command,expected_output,set_data",
    [
        (
            Array(
                [
                    BulkString(b"get"),
                    BulkString(b"whoami"),
                ]
            ),
            BulkString(data=b"database-lover"),
            ("whoami", "database-lover"),
        ),
        (
            Array(
                [
                    BulkString(b"get"),
                    BulkString(b"naruto"),
                ]
            ),
            BulkString(data=b""),
            None,
        ),
        (
            Array(
                [
                    BulkString(b"get"),
                ]
            ),
            SimpleError("Length of get command should be 2"),
            None,
        ),
    ],
)
def test_command_get(
    command: Array,
    expected_output: SimpleString | SimpleError,
    set_data: Union[Tuple[str, str], None],
) -> None:
    datastore = DataStore()
    if set_data:
        datastore[set_data[0]] = set_data[1]
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output


@pytest.mark.parametrize(
    "command,expected_output,keys",
    [
        (
            Array(
                [
                    BulkString(b"del"),
                    BulkString(b"key1"),
                    BulkString(b"key2"),
                    BulkString(b"key3"),
                ]
            ),
            Integer(3),
            ["key1", "key2", "key3"],
        ),
        (
            Array(
                [
                    BulkString(b"del"),
                    BulkString(b"key1"),
                    BulkString(b"key2"),
                ]
            ),
            Integer(0),
            [],
        ),
        (
            Array(
                [
                    BulkString(b"del"),
                ]
            ),
            SimpleError("Length of del command should be at least 2"),
            [],
        ),
    ],
)
def test_command_delete(
    command: Array,
    expected_output: BulkString | SimpleError,
    keys: List[str],
) -> None:
    datastore = DataStore()
    for key in keys:
        datastore[key] = "dummy_value"
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    assert len(datastore) == 0


@pytest.mark.parametrize(
    "command,expected_output,keys",
    [
        (
            Array(
                [
                    BulkString(b"exists"),
                    BulkString(b"key1"),
                    BulkString(b"key2"),
                    BulkString(b"key3"),
                ]
            ),
            Integer(3),
            ["key1", "key2", "key3"],
        ),
        (
            Array(
                [
                    BulkString(b"exists"),
                    BulkString(b"key1"),
                    BulkString(b"key2"),
                ]
            ),
            Integer(0),
            [],
        ),
        (
            Array(
                [
                    BulkString(b"exists"),
                ]
            ),
            SimpleError("Length of exists command should be at least 2"),
            [],
        ),
    ],
)
def test_command_exists(
    command: Array,
    expected_output: BulkString | SimpleError,
    keys: List[str],
) -> None:
    datastore = DataStore()
    for key in keys:
        datastore[key] = "dummy_value"
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
