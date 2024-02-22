from pymemdb.pymemdbprotocols.protocol_parsers import simple_string_parser
from pymemdb.pymemdbprotocols.protocol_types import SimpleString


def test_simple_string_parser():
    actual_output = simple_string_parser(b"+ok\r\n")
    expected_frame = (SimpleString("ok"),2)
    assert actual_output == expected_frame