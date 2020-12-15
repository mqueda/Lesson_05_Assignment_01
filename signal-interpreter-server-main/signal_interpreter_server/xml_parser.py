"""
Module for implementing the xml parser
"""
import logging
import xml.etree.ElementTree as ET
from signal_interpreter_server.exceptions import \
    ParserErrorFileNotFoundError, ParserErrorDecodeError


logger = logging.getLogger(__name__)


class LoadAndParseXml:
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
        Action : Load the specified xml file.
        Expected Results : Proper file load.
        Returns: N/A.
        """
        parsed_data_list = []
        try:
            tree = ET.parse(path)
            root = tree.getroot()
            for service in root:
                for description in service:
                    parsed_data_dic = {'title': description.text,
                                       'id': service.attrib['id']}
                    parsed_data_list.append(parsed_data_dic)
                    self.data = {'services': parsed_data_list}
                    logging.debug("Available Services : %s ", self.data)
            return self.data
        except FileNotFoundError as err:
            logging.error("Exception %s occurred", FileNotFoundError)
            raise ParserErrorFileNotFoundError() from err
        except Exception as err:
            logging.error("Exception %s occurred",
                          err)
            raise ParserErrorDecodeError() from err

    def return_signal_by_title(self, reqid):
        """
        Action : Return the service according with xml file.
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
