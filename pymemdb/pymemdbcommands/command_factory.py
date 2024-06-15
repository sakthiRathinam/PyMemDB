from typing import Callable, Dict

from pymemdb.pymemdbcommands.commands import (
    echo_command,
    get_command,
    ping_command,
    set_command,
)

COMMAND_FACTORY: Dict[str, Callable] = {
    "ping": ping_command,
    "echo": echo_command,
    "get": get_command,
    "set": set_command,
}
