from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
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


def get_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) != 2:
        return SimpleError("Length of get command should be 2")
    decoded_key = str(command_data.data[1])
    value = datastore[decoded_key]
    if value is None:
        return SimpleError("Key not found")
    return SimpleString(value)


def set_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    if len(command_data.data) != 3:
        return SimpleError("Length of set command should be 3")
    decoded_key = str(command_data.data[1])
    decoded_value = str(command_data.data[2])
    datastore[decoded_key] = decoded_value
    return SimpleString("OK")
