"""
Module for implementing the unit tests
"""
import sys
from unittest.mock import patch
import pytest
import json
sys.path[0] = 'C:\\temp\\Lesson_04_Assignment_01-main\\' \
              'signal-interpreter-server-main\\' \
              'signal_interpreter_server'
from xml_parser import LoadAndParseXml  # nopep8
from routes import signal_interpreter_app, set_parser  # nopep8
from exceptions import \
    ParserErrorFileNotFoundError, ParserErrorDecodeError  # nopep8


PROCESSED_XML_DATA = {'services': [{'id': '11', 'title': 'ECU Reset'},
                                   {'id': '27', 'title': 'Security Access'}]}


def test_open_file():
    """
    Action : Test mocking xml file open.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    xml_parser = LoadAndParseXml()
    xml_parser.load_file("..\\..\\signal_database.xml")
    assert xml_parser.data == PROCESSED_XML_DATA


def test_interpretation_01():
    """
    Action : Test mocking interpretation.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    xml_parser = LoadAndParseXml()
    xml_parser.data = {"services": [{"title": "Security Access", "id": "27"}]}
    assert xml_parser.return_signal_by_title("27") == "Security Access"


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
    xml_parser = LoadAndParseXml()
    xml_parser.data = {"services": [{"title": "ECU Reset", "id": "11"},
                                    {"title": "Security Access", "id": "27"}]}
    assert xml_parser.return_signal_by_title(reqid) == expected_result


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "fixtures/xxxxx_xxxxx.xml"])
def test_application_wrong_json_file_name_error():
    """
    Action : Test the server correct error check
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorFileNotFoundError):
        set_parser('XML', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "..\\integration\\fixtures\\BAD_test_basic.xml"])
def test_application_wrong_json_file_content_error():
    """
    Action : Test the server correct error check.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorDecodeError):
        set_parser('XML', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')
