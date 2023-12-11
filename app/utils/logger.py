from datetime import date, timedelta
import logging
import os
from typing import Literal

from config import Config

class Logger:
    
    _formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S")
    _logger = None
    _level = logging.DEBUG if Config().DEBUG else logging.INFO

    def __init__(self, name: str) -> None:
        '''
        Initializer of instance. Aditionally, if DEBUG is True, set logger level to DEBUG.'''
        self._logger = logging.getLogger(name)
        ch = logging.StreamHandler()
        ch.setFormatter(self._formatter)

        ch.setLevel(self._level)
        self._logger.setLevel(self._level)

        self._logger.addHandler(ch)


    def set_level(self, 
        level: Literal['debug', 'info', 'warning', 'error', 'critical']):
        '''
        Sets level of _logger attribute.\n
        Param:
        ------
        level: str. As per logging standards. You doesn't need to pass it uppercase.
        '''
        _level = logging.getLevelName(level.upper())
        self._logger.setLevel(_level)
    

    def get_logger(self, name: str = None) -> logging.Logger:
        '''
        Returns self._logger, an instance of logging.Logger
        '''
        if name and self._logger is None:
            self.__init__(name)
        return self._logger
    

    def delete_file_handler(self) -> None:
        '''
        Deletes file_handlers.
        This because the final resolution for log files is to have
        a log for every table that's gonna be extracted, and so if there's
        multiple tables, there's gonna be multiple file logs.
        '''
        file_handlers = filter(
            lambda h: isinstance(h, logging.FileHandler),
            self._logger.handlers
            )
        
        for handler in (file_handlers):
            self._logger.removeHandler(handler)


    def file_handler_attacher(self, logfile_path: str) -> None:
        '''
        Creates log_path/table/date.log file.
        If there's a previous logging.fileHandler, it will be deleted.
        '''
        self.delete_file_handler()

        if not os.path.exists(logfile_path):
                os.makedirs(logfile_path)
        
        file_name = os.path.join(logfile_path, f'{date.today()}')
        file_handler = logging.FileHandler(f'{file_name}.log', encoding='utf-8')
        file_handler.setFormatter(self._formatter)
        self._logger.addHandler(file_handler)


def timer_format(tm):
    return str(timedelta(seconds = tm))
