"""
Module for implementing the unit tests
"""
import os
import sys
from unittest.mock import patch, mock_open
import pytest
from signal_interpreter_server.main import set_parser
from signal_interpreter_server.json_parser import LoadAndParseJson, json
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.exceptions import\
    ParserErrorFileNotFoundError, ParserErrorDecodeError


CURR_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_BAD_BASIC_FIXTURE_PATH = os.path.join(CURR_DIR, "fixtures", "BAD_test_basic.json")


RAW_JSON_DATA = '{ "json" : "json reference!" }'
PROCESSED_JSON_DATA = {"json": "json reference!"}


def test_open_file():
    """
    Action : Test mocking json file open.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    with patch("builtins.open", mock_open(read_data=RAW_JSON_DATA)):
        json_parser = LoadAndParseJson()
        json_parser.load_file("file/path")
        assert json_parser.data == PROCESSED_JSON_DATA


def test_file_load():
    """
    Action : Test mocking json file loading.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    with patch(
            "builtins.open", mock_open(read_data=RAW_JSON_DATA))\
            as mock_file_object:
        with patch.object(
                json, "load", return_value=PROCESSED_JSON_DATA)\
                as mock_json_load:
            json_parser = LoadAndParseJson()
            json_parser.load_file("path/to/json/file")
            mock_json_load.assert_called_with(mock_file_object.return_value)
            assert json_parser.data == PROCESSED_JSON_DATA


def test_interpretation_01():
    """
    Action : Test mocking interpretation.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    json_parser = LoadAndParseJson()
    json_parser.data = {"services": [{"title": "Security Access", "id": "27"}]}
    assert json_parser.return_signal_by_title("27") == "Security Access"


@pytest.mark.parametrize("reqid, expected_result",  [
    ("11", "ECU Reset"),
    ("27", "Security Access"),
    ("32.", "Service not suported!"),
    ("47", "Service not suported!"),
    ("", "Service not suported!"),
])
def test_interpretation_02(reqid, expected_result):
    """
    Action : Test mocking interpretation.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    json_parser = LoadAndParseJson()
    json_parser.data = {"services": [{"title": "ECU Reset", "id": "11"},
                                     {"title": "Security Access", "id": "27"}]}
    assert json_parser.return_signal_by_title(reqid) == expected_result


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "fixtures/xxxxx_xxxxx.json"])
def test_application_wrong_json_file_name_error():
    """
    Action : Test the server correct error check
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorFileNotFoundError):
        set_parser('JSON', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            TEST_BAD_BASIC_FIXTURE_PATH])
def test_application_wrong_json_file_content_error():
    """
    Action : Test the server correct error check.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorDecodeError):
        set_parser('JSON', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')
