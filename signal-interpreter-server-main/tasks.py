'''
tasks.py
'''
import subprocess
from invoke import task


@task  # pylint: disable=undefined-variable
def pycodestyle_check(_):
    '''
    style method
    :return:
    '''
    cmd = r"pycodestyle ..\signal-interpreter-server-main"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def pylint_sources_check(_):
    '''
    lint method
    :return:
    '''
    cmd = f"pylint signal_interpreter_server"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def pylint_unit_tests_check(_):
    '''
    lint method
    :return:
    '''
    cmd = f"pylint tests.unit"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def pylint_integration_tests_check(_):
    '''
    lint method
    :return:
    '''
    cmd = f"pylint tests.integration"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def code_coverage_check(_):
    '''
    unit_test method
    :return:
    '''
    cmd = f"pytest tests " \
          f"--cov signal_interpreter_server " \
          f"--cov-config=coveragerc"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_start_server(_):
    '''
    lint method
    :return:
    '''
    cmd = f"python signal_interpreter_server\\main.py " \
          f" --file_path signal_database.json"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_json(_):
    '''
    lint method
    :return:
    '''
    cmd = f"python -m pytest tests/integration/integration_test_json.py"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_yaml(_):
    '''
    lint method
    :return:
    '''
    cmd = f"python -m pytest tests/integration/integration_test_json.py"
    subprocess.call(cmd, shell=True)


@task  # pylint: disable=undefined-variable
def call_integration_tests_xml(_):
    '''
    lint method
    :return:
    '''
    cmd = f"python -m pytest tests/integration/integration_test_json.py"
    subprocess.call(cmd, shell=True)
