from pymemdb.pymemdbprotocols.protocol_types import SimpleString


def ping_command(*args) -> bytes:
    return SimpleString("PONG").resp_encode()
