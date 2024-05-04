import sys

from loguru import logger

logger.remove() # Remove pre-attached stderr sink
logger.add(sys.stderr, colorize=True,
           # format="<green>{time}</green> <level>{level} {message}</level>",
           level="DEBUG",
           enqueue=True)
