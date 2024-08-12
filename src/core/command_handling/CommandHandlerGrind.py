from .CommandHandlerBase import CommandHandlerBase
from config.ConfigLoaderPresets import PRESETS
from core.BloodwebHandler import BloodwebHandler
from core.ImageMatcher import ImageMatcher
from core.ResourceHandler import ResourceHandler
from utils.enums import IMAGE_PROCESSING_PARAMETER_TARGET
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
			'\n'
			'[cmd] {full_command}: Identifies and grinds bloodweb nodes displayed in the screen.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{full_command} <preset>'
			'\n\n'
				'\t>> Available presets:'
					'\n\t\t{presets}'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{full_command} survivor'
					'\n\t\t{full_command} trapper'
		).format(
			full_command=CommandHandlerGrind.get_full_command(),
			presets=PRESETS.list_keys(div='\n\t\t')
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
		if arg_preset not in PRESETS.list_keys():
			logger.log(
				'\t=> Bad parameter:\n'
					'\t\t'
					'No such <preset> \'%s\'. '
					'Type \'%s\' to learn more.'
				, arg_preset,
				self.__class__.get_short_command()
			)
			return

		killer_name = None
		if arg_preset != IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name:
			killer_name = arg_preset
			arg_preset = IMAGE_PROCESSING_PARAMETER_TARGET.killer.name

		return [arg_preset, killer_name]

	def run(self):
		sanitized_arg = super().run()
		if sanitized_arg is None: return

		resources = ResourceHandler(*sanitized_arg).initialize()
		ImageMatcher.set_resources(resources)

		bloodweb = BloodwebHandler()
		bloodweb.grind()