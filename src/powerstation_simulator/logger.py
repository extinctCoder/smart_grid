import logging
import sys

COLORS = {
    "DEBUG": "\033[34m",  # BLUE
    "INFO": "\033[32m",  # GREEN
    "WARNING": "\033[33m",  # YELLOW
    "ERROR": "\033[31m",  # RED
    "CRITICAL": "\033[1m\033[31m",  # BOLD RED
    "RESET": "\033[0m",  # RESET
}


class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that adds color to log level names in terminal output.

    This formatter wraps the log level name with ANSI color codes based on the
    severity level. Colors are defined in the COLORS dictionary.

    Methods:
        format: Overrides the base Formatter's format method to add colors.
    """

    def format(self, record) -> str:
        """
        Format the specified record with colored level names.

        Args:
            record: A LogRecord object containing all the information
                   needed to generate a log message.

        Returns:
            str: The formatted log message with colored level name.
        """
        color = COLORS.get(record.levelname, COLORS["RESET"])
        record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"
        return super().format(record)


def setup_base_logger(level=logging.DEBUG):
    """
    Configure and return the root logger with colored output.

    This function sets up the root logger with a StreamHandler that outputs
    to stdout and formats messages using the ColoredFormatter. If the root
    logger already has handlers configured, this function does nothing.

    Args:
        level: The logging level to set for the root logger.
               Default is logging.DEBUG.

    Returns:
        logging.Logger: The configured root logger instance.
    """
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():
        root_logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            ColoredFormatter("%(asctime)s %(filename)s: %(levelname)s, %(message)s")
        )
        root_logger.addHandler(handler)
        root_logger.propagate = False
    return root_logger


def getLogger(name: str):
    """
    Get a logger with the specified name, ensuring the base logger is configured.

    This function calls setup_base_logger() to ensure that logging is properly
    configured with colored output, then returns a logger with the given name.

    Args:
        name: A string that identifies the logger.

    Returns:
        logging.Logger: A configured logger instance with the specified name.
    """
    setup_base_logger()
    return logging.getLogger(name)
