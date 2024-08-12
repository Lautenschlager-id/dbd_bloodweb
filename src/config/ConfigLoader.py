from abc import ABC, abstractmethod
import json

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
		logger.log('\n[init] Loading config \'%s\'', self.config_path)

		with open(self.config_path, 'r') as file:
			data = json.load(file)

			try:
				logger.log('\t>> Validating config')
				jsonschema_with_default(self.data_schema).validate(data)
			except Exception as exception:
				logger.log('\t=> Invalid schema:\n%s', exception)
				exit()
			else:
				logger.log('\t=> Valid config!')
				self._data = data

		return self

	def get(self, config):
		return self._data.get(config, None)

	def list_keys(self, div='\n\t'):
		keys = list(self._data.keys())
		keys.sort()
		return div.join(keys)