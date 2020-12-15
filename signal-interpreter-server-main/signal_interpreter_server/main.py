"""
Module for implementing the main file
"""
import os
import logging
import logging.config
from argparse import ArgumentParser
import yaml
from signal_interpreter_server.routes import\
    signal_interpreter_app, set_factory_object
from signal_interpreter_server.parser_factory import ParserFactory
from signal_interpreter_server.json_parser import LoadAndParseJson
from signal_interpreter_server.xml_parser import LoadAndParseXml
from signal_interpreter_server.yaml_parser import LoadAndParseYaml

# Remeber to set the parameter " --file_path signal_database.XXX "


os.chdir(os.path.dirname(os.path.dirname
                         (os.path.realpath(__file__))))


with open(r'cfg\logger_configuration.yaml', "r") as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)


def get_arguments():
    """
    Action : Load the specified arguments.
    Expected Results : Proper arguments load.
    Returns: parser.parse_args().
    """
    parser = ArgumentParser()
    parser.add_argument('--file_path', required=True)
    logging.debug("Using JSON from file : %s", parser.parse_args().file_path)
    return parser.parse_args()


def set_parser(format, file):
    """
    Action : Set the factory parser.
    Expected Results : Proper factory parser set.
    Returns: N/A.
    """
    factory = ParserFactory()
    factory.register_format("JSON", LoadAndParseJson)
    factory.register_format("XML", LoadAndParseXml)
    factory.register_format("YAML", LoadAndParseYaml)
    factory.set_signal_database_format(format)
    loaded_object = factory.get_parser()
    loaded_object.load_file(file)
    set_factory_object(loaded_object)


def main():
    """
    Action : Start the server application.
    Expected Results : Proper file load.
    Returns: N/A.
    """
    try:
        args = get_arguments()
        if args.file_path[-4:] == 'json':
            set_parser('JSON', args.file_path)
        if args.file_path[-4:] == 'yaml':
            set_parser('YAML', args.file_path)
        if args.file_path[-3:] == 'xml':
            set_parser('XML', args.file_path)
        logging.info("!!!!! Starting the Server !!!!!")
        signal_interpreter_app.run()
    except AttributeError as err:
        logging.error("Exception %s occurred", AttributeError)
        raise AttributeError from err


def init():
    """
    Sets the init values
    """
    if __name__ == '__main__':
        main()


init()
