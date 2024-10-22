from typing import Callable, Dict

from pymemdb.pymemdbcommands.commands import (
    decr_command,
    delete_command,
    echo_command,
    exists_command,
    get_command,
    incr_command,
    lpush_command,
    ping_command,
    rpush_command,
    set_command,
)

COMMAND_FACTORY: Dict[str, Callable] = {
    "ping": ping_command,
    "echo": echo_command,
    "get": get_command,
    "set": set_command,
    "exists": exists_command,
    "del": delete_command,
    "incr": incr_command,
    "decr": decr_command,
    "rpush": rpush_command,
    "lpush": lpush_command,
}
