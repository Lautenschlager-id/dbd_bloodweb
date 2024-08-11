from abc import ABC, abstractmethod
import json

from utils.logger import logger
from utils.functions import jsonschema_with_default

class ConfigLoader(ABC):
	@property
	@abstractmethod
	def config_path(self): pass

	@property
	@abstractmethod
	def data_schema(self): pass

	def __init__(self):
		self._data = None
		self.load()

	def load(self):
		with open(self.config_path, 'r') as file:
			data = json.load(file)

			try:
				jsonschema_with_default(self.data_schema).validate(data)
			except Exception as exception:
				logger.log(f'Invalid JSON at \'{self.config_path}\':')
				logger.log(exception)
				exit()

			self._data = data

		return self

	def get(self, config):
		return self._data.get(config, None)

	def list_keys(self, div='\n\t'):
		keys = list(self._data.keys())
		keys.sort()
		return div.join(keys)