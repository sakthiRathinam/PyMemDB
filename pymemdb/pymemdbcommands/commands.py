from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    RESPParsed,
    SimpleError,
    SimpleString,
)


def ping_command(command_data: Array) -> RESPParsed:
    if len(command_data.data) != 1:
        return SimpleError("Length of ping command should be 1")
    return SimpleString("PONG")


def echo_command(command_data: Array) -> RESPParsed:
    return Array(data=command_data.data[1:])
