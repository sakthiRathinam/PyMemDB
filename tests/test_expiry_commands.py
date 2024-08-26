from time import sleep

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
    "command,expected_output,expected_output_data",
    [
        (
            Array(
                [
                    BulkString(b"set"),
                    BulkString(b"whoami"),
                    BulkString(b"database-lover"),
                    BulkString(b"ex"),
                    BulkString(b"10"),
                ]
            ),
            SimpleString("OK"),
            None,
        )
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
    print(datastore[str(command.data[1])])
    sleep(11)
    assert datastore[str(command.data[1])] == expected_output_data
