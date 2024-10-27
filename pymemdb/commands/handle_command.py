from pymemdb.commands.command_factory import COMMAND_FACTORY
from pymemdb.datastructures.datastore import DataStore
from pymemdb.persistence.persister import AppendOnlyPersister
from pymemdb.protocols.protocol_types import (
    Array,
    RESPParsed,
    SimpleError,
)


def handle_command(command_data: Array, datastore: "DataStore", persister: AppendOnlyPersister | None) -> RESPParsed:
    try:
        command = str(command_data.data[0])
        if not len(command_data.data):
            return SimpleError("Command shouldn't be empty")
        if command.lower() in COMMAND_FACTORY:
            command_executor = COMMAND_FACTORY.get(command.lower())
            command_output = command_executor(command_data, datastore)
            if isinstance(command_output, SimpleError):
                return command_output
            if persister:
                persisted = _persist_command_to_aof(command, command_data, persister)
                if not persisted:
                    print("Error in persisting the command")
            return command_output
        return _handle_unrecognized_command(command_data)
    except Exception as e:
        print(e)
        return SimpleError("Error in command execution")


def _handle_unrecognized_command(command_data: Array) -> RESPParsed:
    args = " ".join([str(arg) for arg in command_data.data[1:]])
    error_message = f"ERR unknown command '{str(command_data.data[0])}', with args beginning with: {args}"
    return SimpleError(error_message)


def _persist_command_to_aof(command: str, command_data: Array, persister: "AppendOnlyPersister") -> bool:
    to_perist_commands = ["set", "del", "incr", "lpush", "rpush"]
    if command in to_perist_commands:
        try:
            persister.log_command_to_file(command_data.data)
            return True
        except Exception as e:
            print(e)
            return False
    return True
