import logging
import multiprocessing

from .enums import LOG
from .functions import create_timestamp_directory, get_last_directory

class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()

        return cls._instance

    def _initialize(self):
        if multiprocessing.current_process().name == 'MainProcess':
            self._result_folder = create_timestamp_directory(LOG.ROOT_DIRECTORY.value)
        else:
            self._result_folder = get_last_directory(LOG.ROOT_DIRECTORY.value)

        logging.basicConfig(
            filename=f'{self._result_folder}{LOG.FILENAME.value}',
            filemode='a+',
            format=LOG.FORMATTING.value,
            level=logging.INFO
        )

        logging.getLogger().addHandler(logging.StreamHandler())
        self.logger = logging.getLogger()

    def get_result_folder(self):
        return self._result_folder

    def log(self, *args):
        str_index = 0

        if args[0][0] == '\n':
            str_index = 1
            self.logger.info('')

        self.logger.info(args[0][str_index:], *args[1:])

logger = Logger()