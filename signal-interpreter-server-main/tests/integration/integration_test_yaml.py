"""
Module for implementing the integration tests
"""
import os
import sys
import json
from mock import Mock
from unittest.mock import patch, call
import pytest
from signal_interpreter_server.main import set_parser
from signal_interpreter_server.routes import signal_interpreter_app
from signal_interpreter_server.yaml_parser import LoadAndParseYaml
from signal_interpreter_server.exceptions import\
    ParserErrorFileNotFoundError, ParserErrorDecodeError


test_basic_yaml_file = (os.path.join
                        (os.path.abspath(os.path.dirname(__file__)),
                         "fixtures\\test_basic.yaml"))
test_bad_yaml_file = (os.path.join
                      (os.path.abspath(os.path.dirname(__file__)),
                       "fixtures\\BAD_test_basic.yaml"))


def constructor_mock(name):
    """Create fake constructor that returns Mock object when invoked"""
    instance = Mock()
    instance._name_of_parent_class = name
    constructor = Mock(return_value=instance)
    return constructor


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            test_basic_yaml_file])
@patch('logging.Logger.debug')
def test_application_service_11_debug(mock_debug):
    """
    Action : Test the main server script loop.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    set_parser('YAML', sys.argv[2])
    signal_interpreter_app.test_client().post('/',
                                              data=json.dumps(
                                                  dict({'service': '11'})),
                                              content_type='application/json')
    mock_debug.assert_has_calls(
        [call('Available Services : %s ',
              {'services': [{'title': 'ECU Reset', 'id': '11'},
                            {'title': 'Security Access', 'id': '27'}]}),
         call('Requested Id : "%s"', '11'),
         call('Service : "%s"', 'ECU Reset'),
         call('Answer : "%s"', 'ECU Reset')])


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            test_basic_yaml_file])
@patch('logging.Logger.info')
def test_application_service_27_info(mock_info):
    """
    Action : Test the main server script loop.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    set_parser('YAML', sys.argv[2])
    signal_interpreter_app.test_client().post('/',
                                              data=json.dumps
                                              (dict({'service': '27'})),
                                              content_type='application/json')
    mock_info.assert_has_calls([call("Processing Request..."),
                                call("Sending data to client...")])


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            test_basic_yaml_file])
@patch('logging.Logger.warning')
def test_application_wrong_id_info(mock_warning):
    """
    Action : Test the server correct error check
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    set_parser('YAML', sys.argv[2])
    signal_interpreter_app.test_client().post('/',
                                              data=json.dumps
                                              (dict({'service': '1876871'})),
                                              content_type='application/json')
    mock_warning.assert_has_calls([call('Service %s not suported!', '1876871'),
                                   call("The Requested Id is Not Avaiable")])


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            test_basic_yaml_file])
@patch('logging.Logger.error')
def test_application_wrong_yaml_data_error(mock_error):
    """
    Action : Test the server correct error check
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    set_parser('YAML', sys.argv[2])
    signal_interpreter_app.test_client().post('/',
                                              data=json.dumps
                                              (dict({'xxxxx': '27'})),
                                              content_type='application/json')
    mock_error.assert_has_calls([call('Exception %s occurred', "'service'")])


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            "fixtures/xxxxx_xxxxx.yaml"])
def test_application_wrong_yaml_file_name_error():
    """
    Action : Test the server correct error check
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorFileNotFoundError):
        set_parser('YAML', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')


@patch.object(sys, "argv", ["signal_interpreter_server", "--file_path",
                            test_bad_yaml_file])
def test_application_wrong_yaml_file_content_error():
    """
    Action : Test the server correct error check.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    with pytest.raises(ParserErrorDecodeError):
        set_parser('YAML', sys.argv[2])
        signal_interpreter_app.test_client().post('/',
                                                  data=json.dumps
                                                  (dict({'service': '27'})),
                                                  content_type='application'
                                                               '/json')


def test_load_file(fixture_yaml_file_path):
    """
    Action : Test the server correct file load.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    load_and_parser_yaml = LoadAndParseYaml()
    returned_data = load_and_parser_yaml.load_file(fixture_yaml_file_path)
    assert returned_data['services'][0]['title'] == 'ECU Reset'
    assert returned_data['services'][1]['id'] == '27'
    with pytest.raises(ParserErrorFileNotFoundError):
        load_and_parser_yaml.load_file('fixtures/wrong_file_path.yaml')


def test_return_service_01(fixture_yaml_file_path, fixture_yaml_file):
    """
    Action : Test the server correct service return.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    load_and_parser_yaml = LoadAndParseYaml()
    load_and_parser_yaml.load_file(fixture_yaml_file_path)
    returned_service = load_and_parser_yaml.return_signal_by_title(
        fixture_yaml_file['services'][0]['id'])
    assert returned_service == 'ECU Reset'
    returned_service = load_and_parser_yaml.return_signal_by_title(
        fixture_yaml_file['services'][1]['id'])
    assert returned_service == 'Security Access'
    returned_service = load_and_parser_yaml.return_signal_by_title('XXXXX')
    assert returned_service == 'Service not suported!'


def test_return_service_02(fixture_yaml_file_path,
                           fixture_loadandparse_yaml_instance):
    """
    Action : Test the server correct service return.
    Expected Results : Test finished with status "Passed".
    Returns: N/A.
    """
    load_and_parser_yaml = LoadAndParseYaml()
    load_and_parser_yaml.load_file(fixture_yaml_file_path)
    returned_service = load_and_parser_yaml.return_signal_by_title(
        fixture_loadandparse_yaml_instance.data['services'][0]['id'])
    assert returned_service == 'ECU Reset'
    returned_service = load_and_parser_yaml.return_signal_by_title(
        fixture_loadandparse_yaml_instance.data['services'][1]['id'])
    assert returned_service == 'Security Access'
    returned_service = load_and_parser_yaml.return_signal_by_title('XXXXX')
    assert returned_service == 'Service not suported!'
