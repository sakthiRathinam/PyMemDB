from typing import List

from pymemdb.pymemdbprotocols.protocol_types import BulkString


def handle_command(command: BulkString, args: List[BulkString] | None):
    ...
