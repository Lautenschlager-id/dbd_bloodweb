from .CommandHandlerBase import CommandHandlerBase
from config.ConfigLoaderSettings import SETTINGS
from core.BloodwebHandler import BloodwebHandler
from utils.logger import logger

class CommandHandlerSetPrestigeLimit(CommandHandlerBase):
	@staticmethod
	def get_full_command(): pass

	@staticmethod
	def get_short_command():
		return '-p'

	@staticmethod
	def get_help_message():
		return (
			'{short_command}: Limits how many prestiges the system will attempt to grind.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{short_command} <prestige>'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{short_command} 1'
		).format(
			short_command=CommandHandlerSetPrestigeLimit.get_short_command()
		)

	@staticmethod
	def get_argument_parameter_info():
		return {
			'type': int,
			'nargs': '*'
		}

	def sanitize_arg(self):
		super().sanitize_arg()

		arg_prestiges = self.args[0]
		try:
			arg_prestiges = int(arg_prestiges)

			if arg_prestiges < 1 or len(self.args) > 1:
				raise

			if SETTINGS.get('use_bloodweb_level_controller') is False:
				logger.result('Bad configuration:')
				logger.detail(
					'Command \'{}\' cannot be used because '
					'the setting \'use_bloodweb_level_controller\' is disabled.'
					, self.__class__.get_short_command()
				)
				return

			return [arg_prestiges]
		except:
			logger.result('Bad parameter:')
			logger.detail(
				'No such <prestiges> \'{}\'. '
				'The prestige should be one positive number.'
				, arg_prestiges
			)
			return

	def run(self):
		sanitized_arg = super().run()
		BloodwebHandler.set_maximum_prestiges(sanitized_arg[0])