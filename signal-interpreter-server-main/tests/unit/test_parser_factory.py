"""
Module for implementing the unit tests
"""
import sys
import pytest
sys.path[0] = 'C:\\temp\\Lesson_04_Assignment_01-main' \
              '\\signal-interpreter-server-main' \
              '\\signal_interpreter_server'
from parser_factory import ParserFactory  # nopep8
from json_parser import LoadAndParseJson  # nopep8


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
