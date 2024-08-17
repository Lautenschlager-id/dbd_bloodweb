from abc import ABC, abstractmethod
import json
from sys import exit

from utils.logger import logger
from utils.functions import jsonschema_with_default

class ConfigLoader(ABC):
	_instances = {}

	@property
	@abstractmethod
	def config_path(self): pass

	@property
	@abstractmethod
	def data_schema(self): pass

	def __new__(cls, *args, **kwargs):
		if cls not in cls._instances:
			instance = super().__new__(cls)
			instance._data = None
			instance.load()

			cls._instances[cls] = instance

		return cls._instances[cls]

	def load(self):
		logger.init(
			'init'
			, 'Loading config \'{}\''
			, self.config_path
		)

		with open(self.config_path, 'r') as file:
			data = json.load(file)

			try:
				jsonschema_with_default(self.data_schema).validate(data)
			except Exception as exception:
				logger.result(
					'Invalid schema:\n{}'
					, exception
				)
				exit()
			else:
				logger.result('Config loaded successfully!')
				self._data = data

		return self

	def get(self, config):
		return self._data.get(config, None)

	def get_keys(self):
		keys = list(self._data.keys())
		keys.sort()
		return keys