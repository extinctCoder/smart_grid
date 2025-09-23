import logging
import sys
from logging import Logger, LogRecord

COLORS = {
    "DEBUG": "\033[34m",
    "INFO": "\033[32m",
    "WARNING": "\033[33m",
    "ERROR": "\033[31m",
    "CRITICAL": "\033[1m\033[31m",
    "RESET": "\033[0m",
}


class ColoredFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        color = COLORS.get(record.levelname, COLORS["RESET"])
        record.levelname = f"{color}{record.levelname}{COLORS['RESET']}"
        return super().format(record)


def setup_base_logger(level: int | str = logging.INFO) -> Logger:
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


def getLogger(name: str) -> Logger:
    setup_base_logger()
    return logging.getLogger(name)
