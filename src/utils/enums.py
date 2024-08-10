from enum import Enum
from pathlib import Path

class CustomEnum(Enum):
	def __str__(self):
		return str(self.value)

	@classmethod
	def any_matching(cls, value, is_key=False):
		return value in (
			cls.__members__ if is_key
			else cls._value2member_map_
		)

	@classmethod
	def keys(cls):
		return cls.__members__.keys()

	@classmethod
	def values(cls):
		return cls._value2member_map_.keys()

	@classmethod
	def get_all(cls):
		return cls._value2member_map_

class ROOT_DIRECTORY(CustomEnum):
	PROCESSED_RESOURCE = '\\processed\\'
	RAW_RESOURCE = '\\originals\\'
	ROOT = '.\\..\\images'
	TEMPLATE = '\\templates\\'

	@property
	def full_path(self):
		return Path(f'{self.ROOT.value}{self.value}')

class FILE_EXTENSION(CustomEnum):
	PROCESSED_RESOURCE = '.png'
	RAW_RESOURCE = '.webp'

	@property
	def name(self):
		return self.value[1:]

	@property
	def as_unix_filename_pattern(self):
		return f'*{self.value}'

class OFFERING_TYPE(CustomEnum):
	ALL = 'all'
	KILLER = 'killers'
	SURVIVOR = 'survivors'


class PERK_TYPE(CustomEnum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

class ADDON_TYPE(CustomEnum):
	KILLER = 'killers'
	SURVIVOR = 'survivors'

class IMAGE_PROCESSING_PARAMETER(CustomEnum):
	all = 'Process all images'
	addon = 'Process addon images'
	item = 'Process item images'
	offering = 'Process offer images'
	perk = 'Process perk images'

class IMAGE_PROCESSING_PARAMETER_TARGET(CustomEnum):
	all = 'Process for all killers and survivors'
	killer = 'Process for all killers or specified killer'
	survivor = 'Process for survivors'