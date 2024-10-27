import os

from pymemdb.commands.handle_command import handle_command
from pymemdb.datastructures.datastore import DataStore
from pymemdb.protocols.protocol_types import (
    SimpleError,
)
from pymemdb.protocols.resp_formatter import decode_data_from_buffer_to_array


def restore_from_file(
    file_path: str,
    datastore: "DataStore",
    buffer_read_size: int = 4096,
) -> bool:
    if not os.path.exists(file_path):
        print("Append only File does not exist")
    buffer = bytearray()
    with open(file_path, "rb") as file:
        while True:
            data = file.read(buffer_read_size)
            if not data:
                break
            buffer.extend(data)
            while buffer:
                frame, framesize = decode_data_from_buffer_to_array(buffer)
                if frame:
                    buffer = buffer[framesize:]
                    command_output = handle_command(frame, datastore, None)
                    if isinstance(command_output, SimpleError):
                        print("AOF file is corrupted")
                        return False
    return True
