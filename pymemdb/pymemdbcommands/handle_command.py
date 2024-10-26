from pymemdb.pymemdbcommands.command_factory import COMMAND_FACTORY
from pymemdb.pymemdbdatastructures.datastore import DataStore
from pymemdb.pymemdbprotocols.protocol_types import (
    Array,
    RESPParsed,
    SimpleError,
)


def handle_command(command_data: Array, datastore: "DataStore") -> RESPParsed:
    try:
        command = str(command_data.data[0])
        if not len(command_data.data):
            return SimpleError("Command shouldn't be empty")
        if command.lower() in COMMAND_FACTORY:
            command_executor = COMMAND_FACTORY.get(command.lower())
            return command_executor(command_data, datastore)
        return _handle_unrecognized_command(command_data)
    except Exception as e:
        print(e)
        return SimpleError("Error in command execution")


def _handle_unrecognized_command(command_data: Array) -> RESPParsed:
    args = " ".join([str(arg) for arg in command_data.data[1:]])
    error_message = f"ERR unknown command '{str(command_data.data[0])}', with args beginning with: {args}"
    return SimpleError(error_message)
