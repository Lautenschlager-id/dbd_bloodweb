from enum import Enum
from pathlib import Path

def any_matching(enum, value):
	return value in enum._value2member_map_

class ROOT_DIRECTORY(Enum):
	ROOT = '.\\..\\images'
	RAW_RESOURCE = '\\originals\\'
	PROCESSED_RESOURCE = '\\processed\\'
	TEMPLATE = '\\templates\\'

	@property
	def full_path(self):
		return Path(f'{self.ROOT.value}{self.value}')

class FILE_EXTENSION(Enum):
	RAW_RESOURCE = '.webp'
	PROCESSED_RESOURCE = '.png'

	@property
	def name(self):
		return self.value[1:]

	@property
	def as_unix_filename_pattern(self):
		return f'*{self.value}'

class OFFERING_TYPE(Enum):
	ALL = 'all'
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def __str__(self):
		return self.value

	def any_matching(received_type):
		return any_matching(OFFERING_TYPE, received_type)

class PERK_TYPE(Enum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def __str__(self):
		return self.value

	def any_matching(received_type):
		return any_matching(PERK_TYPE, received_type)

class ADDON_TYPE(Enum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

	def __str__(self):
		return self.value

	def any_matching(received_type):
		return any_matching(ADDON_TYPE, received_type)