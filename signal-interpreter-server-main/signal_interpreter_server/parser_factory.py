"""
Module for implementing the parse factory file
"""


class ParserFactory:
    """
    Sets the init values
    """
    def __init__(self):
        self._parsers = {}
        self._signal_database_format = None

    def set_signal_database_format(self, signal_database_format):
        """
        Action : Set the signal database format.
        Expected Results : Proper signal database format set.
        Returns: N/A.
        """
        self._signal_database_format = signal_database_format

    def register_format(self, signal_database_format, parser):
        """
        Action : Register the format.
        Expected Results : Proper format set.
        Returns: N/A.
        """
        self._parsers[signal_database_format] = parser()

    def get_parser(self):
        """
        Action : Get the parser.
        Expected Results : Proper parser get.
        Returns: N/A.
        """
        parser = self._parsers.get(self._signal_database_format)
        if not parser:
            raise ValueError(self._signal_database_format)
        return parser
