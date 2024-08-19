from .CommandHandlerBase import CommandHandlerBase
from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from core.image_processing.ImageProcessorItem import ImageProcessorItem
from core.image_processing.ImageProcessorOffering import ImageProcessorOffering
from core.image_processing.ImageProcessorPerk import ImageProcessorPerk
from utils.enums import (
	ADDON_TYPE,
	IMAGE_PROCESSING_PARAMETER,
	IMAGE_PROCESSING_PARAMETER_TARGET,
	OFFERING_TYPE,
	PERK_TYPE
)
from utils.functions import get_list_value, get_all_killer_names
from utils.logger import logger

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

	@staticmethod
	def get_full_command():
		return '--image'

	@staticmethod
	def get_short_command():
		return '-i'

	@staticmethod
	def get_help_message():
		return (
			'{full_command}: Processes raw images to be used in the grinding system.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{full_command} <type>'
					'\n\t\t{full_command} <type> <target>'
					'\n\t\t{full_command} <type> <target> <killer_name>'
			'\n\n'
				'\t>> Available types:'
					'\n\t\t{types}'
			'\n\n'
				'\t>> Available targets:'
					'\n\t\t{targets}'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{full_command} addon killer'
					'\n\t\t{full_command} addon killer trapper'
					'\n\t\t{full_command} perk survivor'
					'\n\t\t{full_command} all'
		).format(
			full_command=CommandHandlerImage.get_full_command(),
			types='\n\t\t'.join([
				f'{type.name} => {type.value}'
				for type in IMAGE_PROCESSING_PARAMETER
			]),
			targets='\n\t\t'.join([
				f'{target.name} => {target.value}'
				for target in IMAGE_PROCESSING_PARAMETER_TARGET
			])
		)

	@staticmethod
	def get_argument_parameter_info():
		return {
			'type': str,
			'nargs': '*'
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

	@classmethod
	def initialize(cls):
		cls.complete_class_mapping()

	def __new__(cls, *args, **kwargs):
		if cls._initialized is False:
			cls._initialized = True
			cls.initialize()
		return super().__new__(cls)

	def sanitize_arg(self):
		super().sanitize_arg()

		arg_type = self.args[0]
		if not IMAGE_PROCESSING_PARAMETER.any_matching(arg_type, is_key=True):
			logger.result('Bad parameter:')
			logger.detail(
				'No such <type> \'{}\'. '
				'Type \'{}\' to learn more.'
				, arg_type
				, self.__class__.get_short_command()
			)
			return

		if arg_type not in [
			IMAGE_PROCESSING_PARAMETER.addon.name,
			IMAGE_PROCESSING_PARAMETER.offering.name,
			IMAGE_PROCESSING_PARAMETER.perk.name,
		]:
			return [arg_type, IMAGE_PROCESSING_PARAMETER_TARGET.all.name, None]

		arg_target = get_list_value(self.args, 1, IMAGE_PROCESSING_PARAMETER_TARGET.all.name)
		if not IMAGE_PROCESSING_PARAMETER_TARGET.any_matching(arg_target, is_key=True):
			logger.result('Bad parameter:')
			logger.detail(
				'No such <target> \'{}\'. '
				'Type \'{}\' to learn more.'
				, arg_target
				, self.__class__.get_short_command()
			)
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
					logger.result('Bad parameter:')
					logger.detail(
						'No such <killer_name> \'{}\'.'
						, arg_killer_name
					)
					logger.detail(
						'Available killers:'
							'\n\t\t\t{}'
						, '\n\t\t\t'.join(killers)
						, breakline=True
					)
					return

		return [arg_type, arg_target, arg_killer_name]

	def run(self):
		sanitized_arg = super().run()
		self.class_mapping[sanitized_arg[0]][sanitized_arg[1]](sanitized_arg[2])
