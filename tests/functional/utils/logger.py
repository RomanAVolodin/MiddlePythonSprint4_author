import logging
import sys
from logging.handlers import RotatingFileHandler

from tests.functional.settings import test_settings

log_level = logging.getLevelName(test_settings.log_level)

handlers = [
    RotatingFileHandler(
        filename='./log.txt',
        mode='w',
        maxBytes=512000,
        backupCount=4,
        encoding='utf-8',
    ),
    logging.StreamHandler(stream=sys.stdout),
]

logging.basicConfig(
    handlers=handlers,
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(name)s: %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S%z',
)

logger = logging.getLogger('tests_logger')
