from pymemdb.pymemdbcommands.command_factory import COMMAND_FACTORY
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    RESPParsed,
    SimpleError,
    SimpleString,
)


def handle_command(command_data: Array) -> RESPParsed:
    if not len(command_data.data):
        return SimpleError("Command shouldn't be empty")
    if (
        command_data.data[0] in COMMAND_FACTORY
        and type(command_data.data[0]) == SimpleString
    ):
        command_executor, max_len = COMMAND_FACTORY.get([command_data.data[0]])
        if len(command_data.data) > max_len:
            return SimpleError(
                "Command length should be less than or equal to {}".format(max_len)
            )
        return command_executor(command_data)
    return SimpleError("Error in command execution")
