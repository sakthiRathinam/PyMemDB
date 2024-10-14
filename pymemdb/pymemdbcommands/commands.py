from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    BulkString,
    RESPParsed,
    SimpleError,
    SimpleString,
)


def ping_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) != 1:
        return SimpleError("Length of ping command should be 1")
    return SimpleString("PONG")


def echo_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    return Array(data=command_data.data[1:])


def exists_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) < 2:
        return SimpleError("Length of exists command should be at least 2")
    keys = [str(key) for key in command_data.data[1:]]
    no_of_key_exists = datastore.no_of_keys_exists(keys)
    return BulkString(no_of_key_exists.encode())


def get_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) != 2:
        return SimpleError("Length of get command should be 2")
    decoded_key = str(command_data.data[1])
    value = datastore[decoded_key]
    if value is None:
        value = ""
    return BulkString(value.encode())


def set_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) not in [3, 5]:
        return SimpleError("Length of set command should be 3 or 5")
    decoded_key = str(command_data.data[1])
    decoded_value = str(command_data.data[2])
    if len(command_data.data) == 5:
        expiry_format = str(command_data.data[3])
        expiry_time = int(str(command_data.data[4]))
        datastore.set_item_with_expiry(
            decoded_key, decoded_value, expiry_time, expiry_format
        )
        return SimpleString("OK")
    datastore[decoded_key] = decoded_value
    return SimpleString("OK")
