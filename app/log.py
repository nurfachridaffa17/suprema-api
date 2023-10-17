import logging
import sys

# Configure the logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
logger = logging.getLogger()

file_handler = logging.FileHandler("app.log")
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

class Logger:
    def info(self, message):
        logger.info(message)

    def warning(self, message):
        logger.warning(message)

    def error(self, message):
        logger.error(message)