"""Logging seragam untuk seluruh tahap pipeline."""
import logging
import sys

_FORMAT = "%(asctime)s %(levelname)-7s %(name)s | %(message)s"


def get_logger(name, level=logging.INFO):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FORMAT))
        logger.addHandler(handler)
        logger.setLevel(level)
    return logger
