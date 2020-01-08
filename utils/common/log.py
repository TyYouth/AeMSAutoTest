import os
import logging
from logging.handlers import TimedRotatingFileHandler
from utils.Config import LOG_PATH, Config



class Logger(object):
    def __init__(self, logger_name='autoTest_project'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        c = Config().get('log')
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        if c:
            self.log_file_name = c.get('file_name') if c.get('file_name') else 'test.log'
            self.backup_count = c.get('backup_count') if c.get('backup_count') else 7
            self.console_output_level = c.get('console_level') if c.get('console_level') else 'DEBUG'
            self.file_output_level = c.get('file_level') if c.get('file_level') else 'WARNING'
            pattern = c.get('pattern') if c.get(
                'pattern') else "%(asctime)s-%(funcName)s-%(levelname)s-%(message)s"
            self.formatter = logging.Formatter(pattern, datefmt='%Y-%m-%d %H:%M:%S')

        # add handlers in logger, if exist, return directly
        # to avoid record the same log

    def get_logger(self):
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_output_level)
            self.logger.addHandler(console_handler)

            # create log file every interval D, and save backupCount day(s)
            file_handler = TimedRotatingFileHandler(
                filename=os.path.join(LOG_PATH, self.log_file_name),
                when='D',
                interval=1,
                backupCount=self.backup_count,
                delay=True,
                encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_output_level)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()
