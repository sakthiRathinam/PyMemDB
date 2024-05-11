from pymemdb.pymemdbprotocols.protocol_types import RESPParsed, SimpleString


def ping_command(*args) -> RESPParsed:
    return SimpleString("PONG")
