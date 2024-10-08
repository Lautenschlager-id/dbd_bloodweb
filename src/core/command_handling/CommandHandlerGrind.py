from .CommandHandlerBase import CommandHandlerBase
from config.ConfigLoaderPresets import PRESETS
from core.bloodweb_grinding.BloodwebHandler import BloodwebHandler
from core.bloodweb_grinding.ImageMatcher import ImageMatcher
from core.bloodweb_grinding.ResourceHandler import ResourceHandler
from utils.enums import IMAGE_PROCESSING_PARAMETER_TARGET
from utils.functions import get_list_value
from utils.logger import logger

class CommandHandlerGrind(CommandHandlerBase):
	@staticmethod
	def get_full_command():
		return '--run'

	@staticmethod
	def get_short_command():
		return '-r'

	@staticmethod
	def get_help_message():
		return (
			'{full_command}: Identifies and grinds bloodweb nodes displayed in the screen.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{full_command} <survivor|killer_name>'
					'\n\t\t{full_command} <survivor|killer_name> <custom_preset_name>'
			'\n\n'
				'\t>> Available presets:'
					'\n\t\t{presets}'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{full_command} survivor'
					'\n\t\t{full_command} trapper'
					'\n\t\t{full_command} trapper custom_basement_preset'
		).format(
			full_command=CommandHandlerGrind.get_full_command(),
			presets='\n\t\t'.join(PRESETS.get_keys())
		)

	@staticmethod
	def get_argument_parameter_info():
		return {
			'type': str,
			'nargs': '*'
		}

	def sanitize_arg(self):
		super().sanitize_arg()

		arg_preset = self.args[0]
		arg_custom_preset = get_list_value(self.args, 1)

		target_preset = arg_custom_preset or arg_preset

		if target_preset not in PRESETS.get_keys():
			logger.result('Bad parameter:')
			logger.detail(
				'No such <preset> \'{}\'. '
				'Type \'{}\' to learn more.'
				, target_preset
				, self.__class__.get_short_command()
			)
			return

		killer_name = None
		if arg_preset != IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name:
			killer_name = arg_preset
			arg_preset = IMAGE_PROCESSING_PARAMETER_TARGET.killer.name

		return [arg_preset, killer_name, target_preset]

	def run(self):
		sanitized_arg = super().run()
		if sanitized_arg is None: return

		resources = ResourceHandler(*sanitized_arg).initialize()
		ImageMatcher.set_resources(resources)

		bloodweb = BloodwebHandler()
		bloodweb.grind()