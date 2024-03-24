import logging


LOGGER_NAME = 'eeg-bloom-template'


def get_logger() -> logging.Logger:
    """
    Simple helper function to retrieve a logger instance using the default logging name for the package.

    :returns: A logger instance.
    """
    return logging.getLogger(LOGGER_NAME)
