"""
Module for implementing the script exceptions
"""


class ParserErrorKeyError(Exception):
    """
    Class for the jason_parser KeyError exceptions.
    """
    def __init__(self, msg=''):
        Exception.__init__(self, "!!!!! Invalid Data Received !!!!!\n"
                                 "%s" % msg)


class ParserErrorFileNotFoundError(Exception):
    """
    Class for the jason_parser KeyError exceptions.
    """
    def __init__(self, msg=''):
        Exception.__init__(self, "!!!!! Invalid File in '--file_path !!!!!\n"
                                 "%s" % msg)


class ParserErrorDecodeError(Exception):
    """
    Class for the jason_parser KeyError exceptions.
    """
    def __init__(self, msg=''):
        Exception.__init__(self, "!!!!! Invalid File Format !!!!!\n"
                                 "%s" % msg)
