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

class RESOURCE_DIRECTORY(CustomEnum):
	PROCESSED_RESOURCE = '\\processed\\'
	RAW_RESOURCE = '\\original\\'
	ROOT = '.\\..\\image'
	TEMPLATE = '\\template\\'

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
	KILLER = 'killer'
	SURVIVOR = 'survivor'

class PERK_TYPE(CustomEnum):
	KILLER = 'killer'
	SURVIVOR = 'survivor'

class ADDON_TYPE(CustomEnum):
	KILLER = 'killer'
	SURVIVOR = 'survivor'

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

class CONFIG_DIRECTORY(CustomEnum):
	PRESET = '\\presets.json'
	ROOT = '.\\config'
	SETTING = '\\settings.json'

	@property
	def full_path(self):
		return Path(f'{self.ROOT.value}{self.value}')

class LOG(CustomEnum):
	FILENAME = '\\logs.txt'
	FORMATTING = '%(asctime)s: %(message)s'
	ROOT_DIRECTORY = '.\\..\\result'

class REGION_BLOODWEB(CustomEnum):
	NAME = 'Bloodweb Nodes'
	FILENAME = '\\bloodweb.png'

class REGION_LEVEL(CustomEnum):
	NAME = 'Bloodweb Level'
	FILENAME = None

class PAINT(CustomEnum):
	GREEN = (0, 255, 0)
	RED = (0, 0, 255)
	THICKNESS = 2

class MATCH(CustomEnum):
	FILENAME = '\\match_result.png'

class GRIND_STRATEGY(CustomEnum):
	DEFAULT = 'default'
	DISTANCE_CLOSER = 'distance_closer'
	DISTANCE_FURTHER = 'distance_further'
	PRIORITY = 'priority'
	PRIORITY_THEN_CLOSER_TO_CENTER = 'priority_then_closer_to_center'
	PRIORITY_THEN_FURTHER_TO_CENTER = 'priority_then_further_to_center'

class ICON_TYPE(CustomEnum):
	PERK = 'perk'
	ADDON = 'addon'