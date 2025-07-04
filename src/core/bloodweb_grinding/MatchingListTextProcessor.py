import re
from sys import exit
import unicodedata

from .FilenamePattern import FilenamePattern
from utils.functions import set_text_to_camel_case
from utils.logger import logger

class MatchingListTextProcessor:
	TEMPLATE_COLOR = {
		"brown": 1,
		"green": 2,
		"blue": 3,
		"purple": 4,
		"red": 5,
		"orange": 6,
	}

	RESOURCE_PREFIX = {
		"addon": "IconAddon_",
		"item": "IconItems_",

		"offer": "IconFavors_",
		"offering": "IconFavors_",

		"perk": "IconPerks_",

		"map": "maps*IconFavors_",
		"realm": "maps*IconFavors_",
		"level": "maps*IconFavors_",

		"event": "events*IconFavors_",

		"box": "IconBox_",
		"mystery": "IconBox_",
		"mystery_box": "IconBox_",
	}

	FNMATCH_ANY_CHAR = '[!:]'
	RE_SPECIAL_CHARACTERS = re.compile(r'[\u0300-\u036f&@#]')

	RE_ENTRY_TEXT = re.compile(r'^\s*(?:(\S+?)\s+)?(\S+?)\s*:\s*(.+)$')

	def __init__(self, entry_list):
		self.entry_list = entry_list

	def get_pattern_from_identifier(self, identifier):
		# purple item: flashlight -> template_4*IconItems_*flashlight*
		# item: flashlight -> IconItems_*flashlight*

		valid_identifier = self.RE_ENTRY_TEXT.search(identifier.lower())
		if not valid_identifier:
			logger.result(
				'Got invalid identifier \'{}\''
				, identifier
			)
			exit()

		(color, type, description) = valid_identifier.groups()

		resource_prefix = self.RESOURCE_PREFIX.get(type)
		if not resource_prefix:
			logger.result(
				'Got invalid type \'{}\' at identifier \'{}\''
				, type
				, identifier
			)
			exit()

		color = self.TEMPLATE_COLOR.get(color)
		color = '*' if color is None else f'template_{color}'

		description = self._replace_special_characters_with_wildcard(
			set_text_to_camel_case(description)
		)
		return f'*{color}*{resource_prefix}*{description}*'


	def get_data_from_all_identifiers(self):
		logger.init(
			'text'
			, 'Processing preset paths'
		)

		pattern_list = []

		for entry in self.entry_list:
			pattern = FilenamePattern(entry)

			pattern.pattern = self.get_pattern_from_identifier(
				pattern.identifier
			)

			pattern_list.append(pattern)

		logger.result('Preset paths processed successfully!')

		return pattern_list

	def _replace_special_characters_with_wildcard(self, content):
		normalized_text = unicodedata.normalize('NFD', content)
		replaced_text = self.RE_SPECIAL_CHARACTERS.sub(
			self.FNMATCH_ANY_CHAR,
			normalized_text
		)
		return replaced_text
