from pymemdb.pymemdbprotocols.protocol_parsers import (
    array_parser,
    bulk_string_parser,
    number_parser,
    simple_error_parser,
    simple_string_parser,
)

PROTOCOL_FACTORY = {
    "+": simple_string_parser,
    ":": number_parser,
    "$": bulk_string_parser,
    "*": array_parser,
    "-": simple_error_parser,
}
