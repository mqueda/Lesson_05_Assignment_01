"""
Module for implementing the routes
"""
import logging
from flask import Flask, request, jsonify, abort
from exceptions import ParserErrorKeyError  # pragma: no cover
from parser_factory import ParserFactory
from json_parser import LoadAndParseJson
from xml_parser import LoadAndParseXml
from yaml_parser import LoadAndParseYaml


signal_interpreter_app = Flask(__name__)


logger = logging.getLogger(__name__)


def set_parser(format, file):
    """
    Action : Set the factory parser.
    Expected Results : Proper factory parser set.
    Returns: N/A.
    """
    global PARSER
    factory = ParserFactory()
    factory.register_format("JSON", LoadAndParseJson)
    factory.register_format("XML", LoadAndParseXml)
    factory.register_format("YAML", LoadAndParseYaml)
    factory.set_signal_database_format(format)
    PARSER = factory.get_parser()
    PARSER.load_file(file)


@signal_interpreter_app.route("/", methods=["POST"])
def interpret_signal():
    """
    Action : Make the received code interpretation.
    Expected Results : Proper code interpretation.
    Returns: jsonfy_data.
    """
    try:
        logging.info("Processing Request...")
        data = request.get_json()
        logging.debug('Requested Id : "%s"', data['service'])
        parsed_data = PARSER.return_signal_by_title(data['service'])
        logging.debug('Answer : "%s"', parsed_data)
        jsonfy_data = jsonify(parsed_data)
        if jsonfy_data.json == "Service not suported!":
            logging.warning("The Requested Id is Not Avaiable")
            abort(503, description="Service Unavailable")
        logging.info("Sending data to client...")
        return (jsonfy_data), 201
    except Exception as err:
        logging.error("Exception %s occurred", str(err))
        raise ParserErrorKeyError() from err


@signal_interpreter_app.errorhandler(500)
def internal_error(error):
    """
    Action : Log error if HTTP code 500 happens.
    Expected Results : Proper error logged.
    Returns: "Invalid data received!!!".
    """
    logging.info("Check the Data Sent !!!")
    return "Invalid data received!!!"
