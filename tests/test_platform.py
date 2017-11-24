"""
Test class for the_platform object
"""

import logging
import uuid
import src.the_platform as the_platform

class TestPlatformClass():
    """
    Test class for the_platform object
    """

    def test_logger(self):
        """
        Checks if the log file is created and contain the entry test puts there
        """
        self.the_platform = the_platform.ThePlatformClass(log_level=logging.DEBUG)
        # Check that there is a FileHandler
        file_handler_exists = False
        for handler in self.the_platform.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                file_handler_exists = True
                file_handler = handler
                break
        assert file_handler_exists,  'No file handlers found in the logger!'
        # Check if the logging works
        _uuid = uuid.uuid1()
        self.the_platform.logger.debug('Logger test debug entry. UUID={}'.format(_uuid))
        log_filename = file_handler.stream.name
        try:
            f = open(log_filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError('Log file {} not found'.format(log_filename))
        except Exception as exc:
            raise exc
        # Look up for the 'Logger test debug entry' string
        assert str(_uuid) in f.read(), 'Cannot find logging debug entry'

if __name__ == '__main__':
    test_platform = TestPlatformClass()
    test_platform.test_logger()
    print('Blablabla')