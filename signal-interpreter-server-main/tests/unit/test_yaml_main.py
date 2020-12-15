"""
Module for implementing the unit tests
"""
from mock import Mock
from unittest.mock import patch
from argparse import Namespace
import pytest
from signal_interpreter_server.main import main, init, ArgumentParser, \
get_arguments
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.yaml_parser import LoadAndParseYaml


class MockMainClassNoRaise:
    """
    Class for the mock functionalities.
    """
    file_path = "file/path"


def constructor_mock(name):
    """Create fake constructor that returns Mock object when invoked"""
    instance = Mock()
    instance._name_of_parent_class = name
    constructor = Mock(return_value=instance)
    return constructor


@patch.object(ArgumentParser, "parse_args", return_value=MockMainClassNoRaise)
@patch.object(ArgumentParser, "add_argument")
def test_main_arguments(mock_add_argument, mock_parse_args):
    """
    Action : Test mocking parse arguments.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    assert get_arguments() == MockMainClassNoRaise
    mock_add_argument.assert_called_with('--file_path', required=True)


@patch.object(signal_interpreter_app, "run")
@patch("signal_interpreter_server.main.get_arguments",
       return_value=Namespace(file_path='signal_database.yaml'))
@patch("signal_interpreter_server.main.set_parser")
def test_main_functions(mock_set_parser, mock_get_arguments, mock_run):
    """
    Action : Test mocking signal interpretation.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    main()
    mock_get_arguments.assert_called_once()
    mock_set_parser.assert_called_with('YAML', 'signal_database.yaml')
    mock_run.assert_called_once()


@patch("signal_interpreter_server.main.main")
@patch("signal_interpreter_server.main.__name__", "__main__")
def test_init(mock_main):
    """
    Action : Test init call.
    Expected Results : Init correctly called.
    Returns: N/A.
    """
    init()
    mock_main.assert_called_once()


class MockMainClassRaise:
    """
    Class for the mock functionalities.
    """
    file_pather = "file/path"


@patch.object(signal_interpreter_app, "run")
@patch.object(LoadAndParseYaml, "load_file")
@patch("signal_interpreter_server.main.get_arguments",
       return_value=MockMainClassRaise)
def test_main_raise(mock_get_arguments, mock_load_file, mock_run):
    """
    Action : Test mocking signal interpretation.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    with pytest.raises(AttributeError):
        main()
