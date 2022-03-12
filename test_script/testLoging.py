# import logging
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
#
# file_handler = logging.FileHandler('sample.log')
# formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)
#
# logger.info('Hello World')
# logger.critical('Error, everebody run, coming Russian bear')

# coding=utf-8
import os
import sys
from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_file_path = os.path.join(BASE_DIR, 'Log/my.log')
err_log_file_path = os.path.join(BASE_DIR, 'Log/err.log')

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
# logger.add(s)
logger.add(log_file_path, rotation="500 MB", encoding='utf-8')  # Automatically rotate too big file
logger.add(err_log_file_path, rotation="15:11", encoding='utf-8',
           level='ERROR')  # Automatically rotate too big file
print(type(logger))
logger.debug("That's it, beautiful and simple logging!")
logger.error("серьезная ошибка")