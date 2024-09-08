import datetime
import uuid

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
        ),
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
    ],
)
def test_lazy_expiry_algo_while_getting(
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


def create_dummy_keys_in_datastore(
    datastore: DataStore, no_of_keys: int, expiry_in_seconds: int
) -> None:
    if expiry_in_seconds == 0:
        for i in range(no_of_keys):
            datastore[f"key{i}-{uuid.uuid1()}"] = f"value{i}"
    for i in range(no_of_keys):
        datastore.set_item_with_expiry(
            f"key{i}-{uuid.uuid1()}", f"value{i}", expiry_in_seconds, "ex"
        )


def test_background_lazy_expiry():
    test_datastore = DataStore()

    initial_datetime = datetime.datetime.now()
    with freeze_time(initial_datetime) as time:
        create_dummy_keys_in_datastore(test_datastore, 10, 10)
        create_dummy_keys_in_datastore(test_datastore, 10, 30)
        assert len(test_datastore._data) == 20

        test_datastore.clean_expired_keys()
        time.tick(delta=datetime.timedelta(seconds=10))
        assert len(test_datastore._data.keys()) == 10

        time.tick(delta=datetime.timedelta(seconds=10))
        assert len(test_datastore._data.keys()) == 10

        time.tick(delta=datetime.timedelta(seconds=10))
        assert len(test_datastore._data.keys()) == 0
