import logging
import multiprocessing

from .enums import LOG
from .functions import create_timestamp_directory, get_last_directory

class Logger:
    _instance = None

    message_metadata = {
        'module': {
            'format': '[{}] ',
            'log_level': 0,
            'breakline': True
        },
        'action': {
            'format': '>> ',
            'log_level': 1,
            'breakline': False
        },
        'result': {
            'format': '=> ',
            'log_level': 1,
            'breakline': False
        },
        'detail': {
            'log_level': 2
        }
    }

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

    def init(self, *args, **kwargs):
        kwargs['mode'] = 'module'
        kwargs['module_title'] = args[0]
        return self._log(*args[1:], **kwargs)

    def action(self, *args, **kwargs):
        kwargs['mode'] = 'action'
        return self._log(*args, **kwargs)

    def result(self, *args, **kwargs):
        kwargs['mode'] = 'result'
        return self._log(*args, **kwargs)

    def detail(self, *args, **kwargs):
        kwargs['mode'] = 'detail'
        return self._log(*args, **kwargs)

    def _log(self, *args, **kwargs):
        # parameters
        mode = kwargs.pop('mode')
        log_level = kwargs.pop('log_level', 0)
        breakline = kwargs.pop('breakline', None)
        module_title = kwargs.pop('module_title', None)

        message = args[0]
        args = args[1:]

        # processed parameters
        message_metadata = self.message_metadata.get(mode)
        tab_level = '\t' * (log_level or message_metadata.get('log_level', 0))
        prefix = message_metadata.get('format', '').format(module_title)

        add_breakline = (
            breakline
            if breakline is not None
            else message_metadata.get('breakline', False)
        )

        # log
        if add_breakline is True:
            self.logger.info('')

        self.logger.info(
            '%s%s%s'
            , tab_level
            , prefix
            , message.format(*args)
        )

logger = Logger()