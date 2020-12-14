"""
Module for implementing the conftest file
"""
import os
import sys
import pytest
sys.path[0] = 'C:\\temp\\Lesson_04_Assignment_01-main' \
              '\\signal-interpreter-server-main\\signal_interpreter_server'
from json_parser import LoadAndParseJson  # nopep8
from xml_parser import LoadAndParseXml  # nopep8
from yaml_parser import LoadAndParseYaml  # nopep8


@pytest.fixture
def fixture_json_file_path():
    """
    Action : Return json file path.
    Expected Correct json file path returned.
    Returns: json file path.
    """
    test_basic_json_file = (os.path.join
                            (os.path.abspath(os.path.dirname(__file__)),
                             "fixtures\\test_basic.json"))
    return test_basic_json_file


@pytest.fixture
def fixture_xml_file_path():
    """
    Action : Return xml file path.
    Expected Correct xml file path returned.
    Returns: xml file path.
    """
    test_basic_xml_file = (os.path.join
                           (os.path.abspath
                            (os.path.dirname(__file__)),
                            "fixtures\\test_basic.xml"))
    return test_basic_xml_file


@pytest.fixture
def fixture_yaml_file_path():
    """
    Action : Return yaml file path.
    Expected Correct yaml file path returned.
    Returns: yaml file path.
    """
    test_basic_yaml_file = (os.path.join
                            (os.path.abspath(os.path.dirname(__file__)),
                             "fixtures\\test_basic.yaml"))
    return test_basic_yaml_file


@pytest.fixture(name="fixture_json_file")
def fixture_json_file_main():
    """
    Action : Return json file structure.
    Expected Correct json file structure returned.
    Returns: json file structure.
    """
    return {
                "services": [
                    {
                        "title": "ECU Reset",
                        "id": "11"
                    },
                    {
                        "title": "Security Access",
                        "id": "27"
                    }
                ]
            }


@pytest.fixture(name="fixture_xml_file")
def fixture_xml_file_main():
    """
    Action : Return xml file structure.
    Expected Correct xml file structure returned.
    Returns: xml file structure.
    """
    return {
                "services": [
                    {
                        "title": "ECU Reset",
                        "id": "11"
                    },
                    {
                        "title": "Security Access",
                        "id": "27"
                    }
                ]
            }


@pytest.fixture(name="fixture_yaml_file")
def fixture_yaml_file_main():
    """
    Action : Return yaml file structure.
    Expected Correct yaml file structure returned.
    Returns: yaml file structure.
    """
    _data_list = []
    _data_dic = {'title': 'ECU Reset', 'id': '11'}
    _data_list.append(_data_dic)
    _data_dic = {'title': 'Security Access', 'id': '27'}
    _data_list.append(_data_dic)
    yaml = {'services': _data_list}
    return yaml


@pytest.fixture
def fixture_loadandparse_json_instance(fixture_json_file):
    """
    Action : LoadAndParse class instance.
    Expected Correct LoadAndParse class instance returned.
    Returns: LoadAndParse class instance.
    """
    load_and_parser = LoadAndParseJson()
    load_and_parser.data = fixture_json_file
    load_and_parser.title = None
    return load_and_parser


@pytest.fixture
def fixture_loadandparse_xml_instance(fixture_xml_file):
    """
    Action : LoadAndParse class instance.
    Expected Correct LoadAndParse class instance returned.
    Returns: LoadAndParse class instance.
    """
    load_and_parser = LoadAndParseXml()
    load_and_parser.data = fixture_xml_file
    load_and_parser.title = None
    return load_and_parser


@pytest.fixture
def fixture_loadandparse_yaml_instance(fixture_yaml_file):
    """
    Action : LoadAndParse class instance.
    Expected Correct LoadAndParse class instance returned.
    Returns: LoadAndParse class instance.
    """
    load_and_parser = LoadAndParseYaml()
    load_and_parser.data = fixture_yaml_file
    load_and_parser.title = None
    return load_and_parser
