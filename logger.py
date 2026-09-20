import logging
import sys


class LogManager():
    def __init__(self) -> None:
        self.logger = logging.getLogger("ElmA")
        self.logger.setLevel(logging.DEBUG)
        logging.basicConfig(stream=sys.stdout)
        self.logger.info(f"{self.__class__.__name__} initialized")
        self.logger.info(f"{self.__class__.__name__} started")


log_manager = LogManager()