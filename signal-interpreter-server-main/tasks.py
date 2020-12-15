'''
tasks.py
'''
import os
import subprocess
from invoke import task


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "signal_interpreter_server")
TEST_DIR = os.path.join(ROOT_DIR, "tests")
TEST_INT_DIR = os.path.join(TEST_DIR, "integration")


@task  # pylint: disable=undefined-variable
def pycodestyle_check(_):
    '''
    style method
    :return:
    '''
    cmd = (f"pycodestyle {SRC_DIR} {TEST_DIR}")
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def pylint_check(_):
    '''
    lint method
    :return:
    '''
    cmd = (f"pylint {SRC_DIR} {TEST_DIR}")
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def code_coverage_check(_):
    '''
    unit_test method
    :return:
    '''
    coveragerc_path = os.path.join(ROOT_DIR, "coveragerc")
    cmd = (f"pytest {TEST_DIR} --cov {SRC_DIR} --cov-config={coveragerc_path}")
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_json(_):
    '''
    lint method
    :return:
    '''
    test_dir = os.path.join(TEST_INT_DIR, "integration_test_json.py")
    cmd = (f"pytest {test_dir} --verbose")
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_yaml(_):
    '''
    lint method
    :return:
    '''
    test_dir = os.path.join(TEST_INT_DIR, "integration_test_yaml.py")
    cmd = (f"pytest {test_dir} --verbose")
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_xml(_):
    '''
    lint method
    :return:
    '''
    test_dir = os.path.join(TEST_INT_DIR, "integration_test_xml.py")
    cmd = (f"pytest {test_dir} --verbose")
    subprocess.call(cmd, shell=True)
