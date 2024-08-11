import json

from utils.enums import CONFIG_DIRECTORY

class ConfigLoader:
	def __init__(self, config_path):
		self.config_path = config_path
		self._data = None

	def load(self):
		with open(self.config_path, 'r') as file:
			self._data = json.load(file)

		return self

	def get(self, config):
		return self._data.get(config, None)

	def list_keys(self, div='\n\t'):
		keys = list(self._data.keys())
		keys.sort()
		return div.join(keys)

SETTINGS = ConfigLoader(CONFIG_DIRECTORY.SETTING.full_path).load()
PRESETS = ConfigLoader(CONFIG_DIRECTORY.PRESET.full_path).load()