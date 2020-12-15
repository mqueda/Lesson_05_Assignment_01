"""
Module for implementing the unit tests
"""
import os
import sys
from unittest.mock import patch
from mock import Mock
import pytest
from signal_interpreter_server.main import set_parser
from signal_interpreter_server.routes import signal_interpreter_app,\
    internal_error
from signal_interpreter_server.json_parser import LoadAndParseJson
from signal_interpreter_server.exceptions import ParserErrorKeyError


os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__))))


def constructor_mock(name):
    """
    Action : Create a fake constructor that returns Mock object when invoked
    Expected Results : Fake constructor properly created.
    Returns: N/A.
    """
    instance = Mock()
    instance._name_of_parent_class = name
    constructor = Mock(return_value=instance)
    return constructor


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "..\\..\\signal_database.json"])
def test_correct_data():
    """
    Action : Test mocking server answer.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    set_parser('JSON', sys.argv[2])
    signal_interpreter_app.testing = True
    signal_interpreter_app_instance = signal_interpreter_app.test_client()
    with patch.object(
            LoadAndParseJson, "return_signal_by_title",
            return_value="Security Access")\
            as mock_return_signal_by_title:
        with signal_interpreter_app_instance as client:
            payload = {"service": "27"}
            response = client.post("/", json=payload)
            mock_return_signal_by_title.assert_called_with("27")
            assert response.get_json() == "Security Access"


def test_wrong_data_raise():
    """
    Action : Test mocking server answer.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    signal_interpreter_app.testing = True
    signal_interpreter_app_instance = signal_interpreter_app.test_client()
    with patch.object(
            LoadAndParseJson, "return_signal_by_title",
            return_value="Service not suported!"):
        with signal_interpreter_app_instance as client:
            payload = {"service": "XXXXX"}
            with pytest.raises(ParserErrorKeyError):
                client.post("/", json=payload)


def test_internal_error():
    """
    Action : Test proper function return value.
    Expected Results : Proper value returned.
    Returns: N/A.
    """
    answer = internal_error(500)
    assert answer == "Invalid data received!!!"
