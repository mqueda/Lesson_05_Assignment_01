"""
Module for implementing the unit tests
"""
import os
import sys
from mock import Mock
from unittest.mock import patch
import pytest
sys.path[0] = 'C:\\temp\\Lesson_04_Assignment_01-main\\' \
              'signal-interpreter-server-main\\' \
              'signal_interpreter_server'
from routes import signal_interpreter_app, set_parser  # nopep8
from xml_parser import LoadAndParseXml  # nopep8
from exceptions import ParserErrorKeyError  # nopep8


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
                            "../../signal_database.xml"])
def test_correct_data():
    """
    Action : Test mocking server answer.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    set_parser('XML', sys.argv[2])
    signal_interpreter_app.testing = True
    signal_interpreter_app_instance = signal_interpreter_app.test_client()
    with patch.object(
            LoadAndParseXml, "return_signal_by_title",
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
            LoadAndParseXml, "return_signal_by_title",
            return_value="Service not suported!"):
        with signal_interpreter_app_instance as client:
            payload = {"service": "XXXXX"}
            with pytest.raises(ParserErrorKeyError):
                client.post("/", json=payload)
