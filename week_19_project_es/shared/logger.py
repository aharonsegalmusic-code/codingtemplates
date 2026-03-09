"""
shared/logger.py

Creates a logger for a service.
Each service creates ONE logger in main.py and passes it to all components.
This replaces print() everywhere.

Usage:
    from shared.logger import get_logger
    logger = get_logger("ingestion-service")
    logger.info("started")
    logger.error("something broke")
"""

import logging
import sys


def get_logger(name: str) -> logging.Logger:
    """
    Args:
        name: the service name — shows up in every log line.
              example: "ingestion-service", "cleaning-consumer"
    """

    logger = logging.getLogger(name)
    #  minimum level -> "show everything"
    logger.setLevel(logging.DEBUG)

    # don't add handlers twice if called again with the same name
    if logger.handlers:
        return logger

    # format:  2026-02-23 14:05:01 | INFO     | ingestion-service:process_image:45 - message
    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # print to terminal
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(fmt)
    logger.addHandler(handler)

    return logger