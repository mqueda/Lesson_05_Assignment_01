"""
Module for implementing the unit tests
"""
import os
import sys
from unittest.mock import patch
import pytest
from signal_interpreter_server.main import set_parser
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.yaml_parser import LoadAndParseYaml
from signal_interpreter_server.exceptions import ParserErrorKeyError


os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__))))


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "../../signal_database.yaml"])
def test_correct_data():
    """
    Action : Test mocking server answer.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    set_parser('YAML', sys.argv[2])
    signal_interpreter_app.testing = True
    signal_interpreter_app_instance = signal_interpreter_app.test_client()
    with patch.object(
            LoadAndParseYaml, "return_signal_by_title",
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
            LoadAndParseYaml, "return_signal_by_title",
            return_value="Service not suported!"):
        with signal_interpreter_app_instance as client:
            payload = {"service": "XXXXX"}
            with pytest.raises(ParserErrorKeyError):
                client.post("/", json=payload)
