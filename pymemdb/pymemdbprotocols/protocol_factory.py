from pymemdb.pymemdbprotocols.protocol_parsers import (
    bulk_string_parser,
    number_parser,
    simple_string_parser,
)

PROTOCOL_FACTORY = {
    "+": simple_string_parser,
    ":": number_parser,
    "$": bulk_string_parser,
}
