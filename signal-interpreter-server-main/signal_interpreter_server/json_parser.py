"""
Module for implementing the json parser
"""
import logging
import json
from signal_interpreter_server.exceptions import \
    ParserErrorFileNotFoundError, ParserErrorDecodeError


logger = logging.getLogger(__name__)


class LoadAndParseJson:
    """
    Class for the LoadAndParse functionalities.
    """
    def __init__(self):
        """
        Sets the init values
        """
        self.data = None
        self.title = None

    def load_file(self, path):
        """
        Action : Load the specified json file.
        Expected Results : Proper file load.
        Returns: N/A.
        """
        try:
            with open(path, "r") as json_file:
                self.data = json.load(json_file)
                logging.debug("Available Services : %s ", self.data)
                return self.data
        except FileNotFoundError as err:
            logging.error("Exception %s occurred", FileNotFoundError)
            raise ParserErrorFileNotFoundError() from err
        except json.decoder.JSONDecodeError as err:
            logging.error("Exception %s occurred",
                          json.decoder.JSONDecodeError)
            raise ParserErrorDecodeError() from err

    def return_signal_by_title(self, reqid):
        """
        Action : Return the service according with json file.
        Expected Results : Return the correct service.
        Returns: self.title.
        """
        services = self.data['services']
        for service in services:
            if service['id'] == reqid:
                self.title = service['title']
                logging.debug('Service : "%s"', self.title)
                return self.title
        logging.warning("Service %s not suported!", reqid)
        return "Service not suported!"
