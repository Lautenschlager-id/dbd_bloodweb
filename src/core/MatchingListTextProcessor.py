import re
import unicodedata

class MatchingListTextProcessor:
	TEMPLATE_COLOR = {
		"brown": 1,
		"yellow": 2,
		"green": 3,
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
	}

	FNMATCH_ANY_CHAR = '[!:]'
	RE_SPECIAL_CHARACTERS = re.compile(r'[\u0300-\u036f&@#]')

	RE_ENTRY_TEXT = re.compile(r'^\s*(?:(\S+?)\s+)?(\S+?)\s*:\s*(.+)$')

	def __init__(self, entry_list):
		self.entry_list = entry_list

	def convert_line_to_unix_file_name(self, line):
		# purple item: flashlight -> template_4*IconItems_*flashlight*
		# item: flashlight -> IconItems_*flashlight*

		valid_line = self.RE_ENTRY_TEXT.search(line.lower())
		assert valid_line, f'Got invalid line \'{line}\''

		(color, type, description) = valid_line.groups()

		resource_prefix = self.RESOURCE_PREFIX.get(type)
		assert resource_prefix, f'Got invalid type \'{type}\' at line \'{line}\''

		color = self.TEMPLATE_COLOR.get(color)
		color = '*' if color is None else f'template_{color}'

		description = self._replace_special_characters_with_wildcard(
			self._set_text_to_camel_case(description)
		)

		return f'*{color}*{resource_prefix}*{description}*'

	def convert_all_lines_to_unix_file_name(self):
		for index in range(len(self.entry_list)):
			preset = self.entry_list[index]

			is_list = isinstance(preset, list)

			line = preset[0] if is_list else preset
			unix_file_name = self.convert_line_to_unix_file_name(line)

			if is_list:
				preset[0] = unix_file_name
			else:
				self.entry_list[index] = unix_file_name

		return self.entry_list

	def _set_text_to_camel_case(self, content):
		words = re.split(r'[\s_]+', content)
		return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

	def _replace_special_characters_with_wildcard(self, content):
		normalized_text = unicodedata.normalize('NFD', content)
		replaced_text = self.RE_SPECIAL_CHARACTERS.sub(
			self.FNMATCH_ANY_CHAR,
			normalized_text
		)
		return replaced_text