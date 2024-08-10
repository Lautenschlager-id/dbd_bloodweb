from .CommandHandlerBase import CommandHandlerBase
from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from core.image_processing.ImageProcessorItem import ImageProcessorItem
from core.image_processing.ImageProcessorOffering import ImageProcessorOffering
from core.image_processing.ImageProcessorPerk import ImageProcessorPerk
from utils.enums import (
	IMAGE_PROCESSING_PARAMETER, IMAGE_PROCESSING_PARAMETER_TARGET,
	ADDON_TYPE, OFFERING_TYPE, PERK_TYPE
)
from utils.functions import get_list_value, get_all_killer_names

class CommandHandlerImage(CommandHandlerBase):
	_initialized = False

	class_mapping = {
		IMAGE_PROCESSING_PARAMETER.addon.name: {
			'class': ImageProcessorAddon,
			IMAGE_PROCESSING_PARAMETER_TARGET.all.name: None,
			IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name: [
				ADDON_TYPE.SURVIVOR,
			],
			IMAGE_PROCESSING_PARAMETER_TARGET.killer.name: [
				ADDON_TYPE.KILLER,
			]
		},
		IMAGE_PROCESSING_PARAMETER.item.name: {
			'class': ImageProcessorItem,
			IMAGE_PROCESSING_PARAMETER_TARGET.all.name: None,
			'': [None]
		},
		IMAGE_PROCESSING_PARAMETER.offering.name: {
			'class': ImageProcessorOffering,
			IMAGE_PROCESSING_PARAMETER_TARGET.all.name: None,
			IMAGE_PROCESSING_PARAMETER_TARGET.killer.name: [
				OFFERING_TYPE.ALL,
				OFFERING_TYPE.KILLER,
			],
			IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name: [
				OFFERING_TYPE.ALL,
				OFFERING_TYPE.SURVIVOR,
			]
		},
		IMAGE_PROCESSING_PARAMETER.perk.name: {
			'class': ImageProcessorPerk,
			IMAGE_PROCESSING_PARAMETER_TARGET.all.name: None,
			IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name: [
				PERK_TYPE.SURVIVOR,
			],
			IMAGE_PROCESSING_PARAMETER_TARGET.killer.name: [
				PERK_TYPE.KILLER,
			]
		}
	}

	@classmethod
	def complete_class_mapping(cls):
		str_all = IMAGE_PROCESSING_PARAMETER_TARGET.all.name
		ignore = ['class', str_all]

		for mapping in cls.class_mapping.values():
			ref_class = mapping['class']
			ls_all = []

			for arg_enum, param_enum_ls in mapping.items():
				if arg_enum in ignore: continue

				mapping[arg_enum] = (
					lambda
						killer_name=None,
						arg_enum=arg_enum,
						param_enum_ls=param_enum_ls,
						ref_class=ref_class:
					[
						(
							ref_class(param_enum)
							if killer_name is None
							else ref_class(param_enum, killer_name=killer_name)
						).process_all_images()
						for param_enum in param_enum_ls
					]
				)

				ls_all += param_enum_ls

			mapping[str_all] = (
				lambda
					killer_name=None,
					ls_all=list(set(ls_all)),
					ref_class=ref_class:
				[
					(
						ref_class(param_enum)
						if param_enum is not None
						else ref_class()
					).process_all_images()
					for param_enum in ls_all
				]
			)

		cls.class_mapping[str_all] = {
			str_all: (
				lambda
					killer_name=None:
				[
					mapping[str_all]()
					for key, mapping in cls.class_mapping.items()
						if key != str_all
				]
			)
		}

	def __new__(cls, *args, **kwargs):
		if cls._initialized is False:
			cls._initialized = True
			cls.complete_class_mapping()
		return super().__new__(cls)

	def help(self):
		if self.args: return False

		print('Syntax:'
			'\n\t--image <type>'
			'\n\t--image <type> <target>'
			'\n\t--image <type> <target killer-name>')

		print('\n')

		print('Available types:')
		for type in IMAGE_PROCESSING_PARAMETER:
			print(f'\t{type.name} => {type.value}')

		print('\n')

		print('Available target types:')
		for target in IMAGE_PROCESSING_PARAMETER_TARGET:
			print(f'\t{target.name} => {target.value}')

		print('\n')

		print('Usage:'
			'\n\t--image addon killer'
			'\n\t--image addon killer trapper'
			'\n\t--image perk survivor'
			'\n\t--image all')

		return True

	def sanitize_arg(self):
		arg_type = self.args[0]
		if not IMAGE_PROCESSING_PARAMETER.any_matching(arg_type, is_key=True):
			print(f'No such <type> \'{arg_type}\'. Type \'-i\' to see the full list.')
			return

		if arg_type not in [
			IMAGE_PROCESSING_PARAMETER.addon.name,
			IMAGE_PROCESSING_PARAMETER.offering.name,
			IMAGE_PROCESSING_PARAMETER.perk.name,
		]:
			return [arg_type, IMAGE_PROCESSING_PARAMETER_TARGET.all.name, None]

		arg_target = get_list_value(self.args, 1, IMAGE_PROCESSING_PARAMETER_TARGET.all.name)
		if not IMAGE_PROCESSING_PARAMETER_TARGET.any_matching(arg_target, is_key=True):
			print(f'No such <target> \'{arg_target}\'. Type \'-i\' to see the full list.')
			return

		arg_killer_name = None
		if (
			arg_type == IMAGE_PROCESSING_PARAMETER.addon.name
			and arg_target == IMAGE_PROCESSING_PARAMETER_TARGET.killer.name
		):
			arg_killer_name = get_list_value(self.args, 2)

			if arg_killer_name is not None:
				killers = get_all_killer_names()
				if arg_killer_name not in killers:
					print(f'No such <killer_name> \'{arg_killer_name}\'.'
						'\n\nAvailable killers:\n\t'
						+ '\n\t'.join(killers))
					return

		return [arg_type, arg_target, arg_killer_name]

	def run(self):
		if self.help(): return

		sanitized_arg = self.sanitize_arg()
		if sanitized_arg is None: return

		self.class_mapping[sanitized_arg[0]][sanitized_arg[1]](sanitized_arg[2])
