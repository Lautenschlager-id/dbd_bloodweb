from enum import Enum
from pathlib import Path

def any_matching(enum, value):
	return value in enum.__members__.values()

class ROOT_DIRECTORY(Enum):
	ROOT = '.\\images'
	RAW_RESOURCE = '\\originals\\'
	PROCESSED_RESOURCE = '\\processed\\'
	TEMPLATE = '\\templates\\'

	@property
	def full_path(self):
		return Path(f'{self.ROOT}{self.value}')

class FILE_EXTENSION(Enum):
	RAW_RESOURCE = '.webp'
	PROCESSED_RESOURCE = '.png'

	@property
	def name(self):
		return self.value[1:]

class OFFERING_TYPE(Enum):
	ALL = 'all'
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def any_matching(received_type):
		return any_matching(OFFERING_TYPE, received_type)

class PERK_TYPE(Enum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def any_matching(received_type):
		return any_matching(PERK_TYPE, received_type)

class ADDON_TYPE(Enum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def any_matching(received_type):
		return any_matching(ADDON_TYPE, received_type)