"""
Module for implementing the unit tests
"""
import os
import sys
from unittest.mock import patch
import json
import pytest
from signal_interpreter_server.main import set_parser
from signal_interpreter_server.xml_parser import LoadAndParseXml
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.exceptions import \
    ParserErrorFileNotFoundError, ParserErrorDecodeError

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "signal_interpreter_server")
CURR_DIR = os.path.abspath(os.path.dirname(__file__))
TEST_BASIC_FIXTURE_PATH = os.path.join(CURR_DIR, "fixtures",
                                       "signal_database.xml")
TEST_BAD_BASIC_FIXTURE_PATH = os.path.join(CURR_DIR, "fixtures",
                                           "BAD_test_basic.xml")


PROCESSED_XML_DATA = {'services': [{'id': '11', 'title': 'ECU Reset'},
                                   {'id': '27', 'title': 'Security Access'}]}


def test_open_file():
    """
    Action : Test mocking xml file open.
    Expected Results : No difference from normal application usage.
    Returns: N/A.
    """
    xml_parser = LoadAndParseXml()
    xml_parser.load_file(TEST_BASIC_FIXTURE_PATH)
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
                            TEST_BAD_BASIC_FIXTURE_PATH])
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
