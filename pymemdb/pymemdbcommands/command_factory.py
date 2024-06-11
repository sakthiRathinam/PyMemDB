from typing import Callable, Dict

from pymemdb.pymemdbcommands.commands import echo_command, ping_command

COMMAND_FACTORY: Dict[str, Callable] = {
    "ping": ping_command,
    "echo": echo_command,
}
