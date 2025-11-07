"""Logging configuration."""

import sys
from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO", backtrace=True, diagnose=False)

