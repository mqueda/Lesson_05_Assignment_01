"""
Module for implementing the unit tests
"""
import pytest
from signal_interpreter_server.parser_factory import ParserFactory
from signal_interpreter_server.json_parser import LoadAndParseJson


def test_get_parser_function_ok():
    """
    Action : Test proper function return.
    Expected Results : Function returns proper object.
    Returns: N/A.
    """
    factory = ParserFactory()
    factory.register_format("JSON", LoadAndParseJson)
    factory.set_signal_database_format('JSON')
    parser = factory.get_parser()
    assert parser is not None


def test_get_parser_function_raise_error():
    """
    Action : Test proper function error raise.
    Expected Results : Proper error raised.
    Returns: N/A.
    """
    factory = ParserFactory()
    factory.register_format("JSON", LoadAndParseJson)
    factory.set_signal_database_format('None')
    with pytest.raises(ValueError):
        factory.get_parser()
