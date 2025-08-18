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
    def format(self, record):
        color = COLORS.get(record.levelname, COLORS["RESET"])
        record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"
        return super().format(record)


def setup_base_logger(level=logging.DEBUG):
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
    setup_base_logger()
    return logging.getLogger(name)
