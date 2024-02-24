from pymemdb.pymemdbprotocols.protocol_parsers import (
    number_parser,
    simple_string_parser,
)

PROTOCOL_FACTORY = {"+": simple_string_parser, ":": number_parser}
