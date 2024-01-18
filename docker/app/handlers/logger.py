# -*- coding: utf-8 -*-

import logging
from config.basic import server

class Logger:
    def __init__(self):
        self.default_log_name = 'log'
        self.default_filename = 'logs/api.log'
        
    @classmethod
    def set_log_level(cls, debug):
        if debug:
            default_level = logging.DEBUG
        else:
            default_level = logging.INFO
        return default_level

    @classmethod
    def set_logger(cls, log_name=None, filename=None, level=None):
        if log_name is None:
            log_name = cls.default_log_name

        formatter = logging.Formatter("[%(asctime)s] - %(levelname)s :%(message)s")
        logger = logging.getLogger(log_name)
        if server['debug'] is True:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            logger.addHandler(streamHandler)

        if filename is None:
            filename = cls.default_filename

        if level is None:
            level = cls.set_log_level(server['debug'])

        fileHandler = logging.FileHandler(filename=filename)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)
        logger.setLevel(level=level)
        return logger
