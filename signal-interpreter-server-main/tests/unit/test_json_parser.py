"""
Module for implementing the unit tests
"""
import sys
from unittest.mock import patch, mock_open
import pytest
sys.path[0] = 'C:\\temp\\Lesson_04_Assignment_01-main\\' \
              'signal-interpreter-server-main\\' \
              'signal_interpreter_server'
from json_parser import LoadAndParseJson, json  # nopep8
from routes import signal_interpreter_app, set_parser  # nopep8
from exceptions import\
    ParserErrorFileNotFoundError, ParserErrorDecodeError  # nopep8


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
                            "..\\integration\\fixtures\\BAD_test_basic.json"])
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
