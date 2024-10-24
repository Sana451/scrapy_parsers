import logging
import os
import datetime

from ..config import settings
from .singleton import Singleton


class MyLogger(object, metaclass=Singleton):
    _logger = None

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        log_level = settings["log_level"]
        if log_level == "info":
            log_level = logging.INFO
        elif log_level == "debug":
            log_level = logging.DEBUG
        self._logger.setLevel(log_level)
        formatter = logging.Formatter(
            fmt='%(asctime)s | [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s',
            datefmt='%H:%M:%S')

        now = datetime.datetime.now()
        dir_name = "./log"

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        file_handler = logging.FileHandler(dir_name + "/log_" + now.strftime("%Y-%m-%d") + ".log", mode='w')

        stream_handler = logging.StreamHandler()

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(file_handler)
        self._logger.addHandler(stream_handler)

        print("Generate new loger instance")

    def get_logger(self):
        return self._logger
