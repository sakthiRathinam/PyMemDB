from pymemdb.pymemdbcommands.command_factory import COMMAND_FACTORY
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    RESPParsed,
    SimpleError,
)


def handle_command(command_data: Array) -> RESPParsed:
    try:
        command = str(command_data.data[0])
        if not len(command_data.data):
            return SimpleError("Command shouldn't be empty")
        if command.lower() in COMMAND_FACTORY:
            command_executor = COMMAND_FACTORY.get(command.lower())
            if not command_executor:
                return SimpleError("Command not found")
        return command_executor(command_data)
    except Exception as e:
        print(e)
        return SimpleError("Error in command execution")
