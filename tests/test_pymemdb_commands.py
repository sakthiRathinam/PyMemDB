from collections import deque
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


@pytest.mark.parametrize(
    "command, expected_output, initial_value",
    [
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            Integer(2),
            "1",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            Integer(3),
            "2",
        ),
        (
            Array([BulkString(b"incr")]),
            SimpleError("Length of incr command should be 2"),
            "3",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key"), BulkString(b"key")]),
            SimpleError("Length of incr command should be 2"),
            "4",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "not_an_integer",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "1.0",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "1.0",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "not_an_integer",
        ),
        (
            Array([BulkString(b"incr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "1.0",
        ),
    ],
)
def test_command_incr(
    command: Array,
    expected_output: Integer | SimpleError,
    initial_value: str,
) -> None:
    datastore = DataStore()
    datastore["key"] = initial_value
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    if isinstance(expected_output, Integer):
        assert datastore["key"] == str(expected_output.data)


@pytest.mark.parametrize(
    "command, expected_output, initial_value",
    [
        (
            Array([BulkString(b"decr"), BulkString(b"key")]),
            Integer(-3),
            "-2",
        ),
        (
            Array([BulkString(b"decr"), BulkString(b"key")]),
            Integer(-4),
            "-3",
        ),
        (
            Array([BulkString(b"decr")]),
            SimpleError("Length of decr command should be 2"),
            "-4",
        ),
        (
            Array([BulkString(b"decr"), BulkString(b"key"), BulkString(b"key")]),
            SimpleError("Length of decr command should be 2"),
            "-5",
        ),
        (
            Array([BulkString(b"decr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "not_an_integer",
        ),
        (
            Array([BulkString(b"decr"), BulkString(b"key")]),
            SimpleError("Value is not an integer"),
            "1.0",
        ),
    ],
)
def test_command_decr(
    command: Array,
    expected_output: Integer | SimpleError,
    initial_value: str,
) -> None:
    datastore = DataStore()
    datastore["key"] = initial_value
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    if isinstance(expected_output, Integer):
        assert datastore["key"] == str(expected_output.data)


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                    BulkString(b"1"),
                    BulkString(b"2"),
                    BulkString(b"3"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                    BulkString(b"4"),
                    BulkString(b"5"),
                    BulkString(b"6"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                ]
            ),
            SimpleError("Length of rpush command should be at least 3"),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                ]
            ),
            SimpleError("Length of rpush command should be at least 3"),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                    BulkString(b"7"),
                    BulkString(b"8"),
                ]
            ),
            Integer(2),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                    BulkString(b"9"),
                    BulkString(b"10"),
                    BulkString(b"11"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"rpush"),
                    BulkString(b"key"),
                    BulkString(b"12"),
                    BulkString(b"13"),
                    BulkString(b"14"),
                    BulkString(b"15"),
                ]
            ),
            Integer(4),
        ),
    ],
)
def test_command_rpush(command: Array, expected_output: Integer | SimpleError) -> None:
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    if isinstance(expected_output, Integer):
        assert datastore[str(command.data[1])] == deque([str(data) for data in command.data[2:]])


@pytest.mark.parametrize(
    "command,expected_output",
    [
        (
            Array(
                [
                    BulkString(b"lpush"),
                    BulkString(b"key"),
                    BulkString(b"1"),
                    BulkString(b"2"),
                    BulkString(b"3"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"Lpush"),
                    BulkString(b"key"),
                    BulkString(b"4"),
                    BulkString(b"5"),
                    BulkString(b"6"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"lpush"),
                    BulkString(b"key"),
                ]
            ),
            SimpleError("Length of lpush command should be at least 3"),
        ),
        (
            Array(
                [
                    BulkString(b"lpush"),
                ]
            ),
            SimpleError("Length of lpush command should be at least 3"),
        ),
        (
            Array(
                [
                    BulkString(b"lpush"),
                    BulkString(b"key"),
                    BulkString(b"7"),
                    BulkString(b"8"),
                ]
            ),
            Integer(2),
        ),
        (
            Array(
                [
                    BulkString(b"lpush"),
                    BulkString(b"key"),
                    BulkString(b"9"),
                    BulkString(b"10"),
                    BulkString(b"11"),
                ]
            ),
            Integer(3),
        ),
        (
            Array(
                [
                    BulkString(b"lpush"),
                    BulkString(b"key"),
                    BulkString(b"12"),
                    BulkString(b"13"),
                    BulkString(b"14"),
                    BulkString(b"15"),
                ]
            ),
            Integer(4),
        ),
    ],
)
def test_command_lpush(command: Array, expected_output: Integer | SimpleError) -> None:
    datastore = DataStore()
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output
    if isinstance(expected_output, Integer):
        assert datastore[str(command.data[1])] == deque([str(data) for data in command.data[2:]][::-1])


@pytest.mark.parametrize(
    "command, expected_output",
    [
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"0"),
                    BulkString(b"2"),
                ]
            ),
            Array(
                [
                    BulkString(b"0"),
                    BulkString(b"1"),
                    BulkString(b"2"),
                ]
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"2"),
                    BulkString(b"5"),
                ]
            ),
            Array(
                [
                    BulkString(b"2"),
                    BulkString(b"3"),
                    BulkString(b"4"),
                    BulkString(b"5"),
                ]
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"0"),
                    BulkString(b"-5"),
                ]
            ),
            Array(
                [
                    BulkString(b"0"),
                    BulkString(b"1"),
                    BulkString(b"2"),
                    BulkString(b"3"),
                    BulkString(b"4"),
                    BulkString(b"5"),
                ]
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"5"),
                    BulkString(b"9"),
                ]
            ),
            Array(
                [
                    BulkString(b"5"),
                    BulkString(b"6"),
                    BulkString(b"7"),
                    BulkString(b"8"),
                    BulkString(b"9"),
                ]
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"0"),
                    BulkString(b"0"),
                ]
            ),
            Array(
                [
                    BulkString(b"0"),
                ]
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"10"),
                    BulkString(b"15"),
                ]
            ),
            Array(
                [],
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"2"),
                    BulkString(b"1"),
                ]
            ),
            Array(
                [],
            ),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                    BulkString(b"key"),
                    BulkString(b"2"),
                ]
            ),
            SimpleError("Length of lrange command should be 4"),
        ),
        (
            Array(
                [
                    BulkString(b"lrange"),
                ]
            ),
            SimpleError("Length of lrange command should be 4"),
        ),
    ],
)
def test_command_lrange(command: Array, expected_output: Array | SimpleError) -> None:
    datastore = DataStore()
    datastore["key"] = deque([str(i) for i in range(10)])
    actual_output = handle_command(command, datastore)
    assert actual_output == expected_output


def test_command_not_found() -> None:
    datastore = DataStore()
    command = Array([BulkString(b"flush"), BulkString(b"all"), BulkString(b"keys")])
    actual_output = handle_command(command, datastore)
    assert actual_output == SimpleError("ERR unknown command 'flush', with args beginning with: all keys")
