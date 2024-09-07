import datetime

import pytest
from freezegun import freeze_time

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
def test_expiry_command_set_happy_flow(
    command: Array,
    expected_output: SimpleString | SimpleError,
    expected_output_data: str | None,
) -> None:
    initial_datetime = datetime.datetime.now()
    with freeze_time(initial_datetime) as time:
        datastore = DataStore()
        actual_output = handle_command(command, datastore)
        time.tick(delta=datetime.timedelta(seconds=11))
        assert actual_output == expected_output
        assert datastore[str(command.data[1])] == expected_output_data


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
def test_lazy_expiry_algo(
    command: Array,
    expected_output: SimpleString | SimpleError,
    expected_output_data: str | None,
) -> None:
    initial_datetime = datetime.datetime.now()
    with freeze_time(initial_datetime) as time:
        datastore = DataStore()
        actual_output = handle_command(command, datastore)
        time.tick(delta=datetime.timedelta(seconds=11))
        assert actual_output == expected_output
        assert datastore[str(command.data[1])] == expected_output_data
