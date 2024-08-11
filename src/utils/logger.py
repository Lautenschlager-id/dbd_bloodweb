import logging

from .enums import LOG
from .functions import create_timestamp_directory

class Logger:
    _initialized = False
    _result_folder = create_timestamp_directory(LOG.ROOT_DIRECTORY.value)

    def __new__(cls, *args, **kwargs):
        if cls._initialized is False:
            cls._initialized = True
            cls.initialize()
        return super().__new__(cls)

    @classmethod
    def initialize(cls):
        logging.basicConfig(
            filename=cls._result_folder + LOG.FILENAME.value,
            format=LOG.FORMATTING.value,
            level=logging.INFO
        )

        logging.getLogger().addHandler(logging.StreamHandler())

    def __init__(self):
        self.logger = logging.getLogger()

    def log(self, *args):
        self.logger.info(*args)

logger = Logger()