from typing import Callable, Dict, Tuple

from pymemdb.pymemdbcommands.commands import ping_command

COMMAND_FACTORY: Dict[str, Tuple[Callable, int]] = {
    "ping": (ping_command, 1),  # handler,max len
}
