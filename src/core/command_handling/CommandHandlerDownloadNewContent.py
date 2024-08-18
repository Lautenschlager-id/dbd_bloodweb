from .CommandHandlerBase import CommandHandlerBase
from core.content_download.ContentDownloader import ContentDownloader
from utils.logger import logger

class CommandHandlerDownloadNewContent(CommandHandlerBase):
	@staticmethod
	def get_full_command():
		return '--download'

	@staticmethod
	def get_short_command():
		return '-d'

	@staticmethod
	def get_help_message():
		return (
			'{short_command}: Limits how many levels the system will attempt to grind.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{short_command} <levels>'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{short_command} 1'
		).format(
			short_command=CommandHandlerDownloadNewContent.get_short_command()
		)

	@staticmethod
	def get_argument_parameter_info():
		return {
			'type': str,
			'nargs': '*'
		}

	def sanitize_arg(self):
		super().sanitize_arg()

		arg_content_name = ' '.join(self.args)
		return [arg_content_name]

		# try:
		# 	arg_levels = int(arg_levels)

		# 	if arg_levels < 1 or len(self.args) > 1:
		# 		raise

		# 	return [arg_levels]
		# except:
		# 	logger.result('Bad parameter:')
		# 	logger.detail(
		# 		'No such <levels> \'{}\'. '
		# 		'The level should be one positive number.'
		# 		, arg_levels
		# 	)
		# 	return

	def run(self):
		sanitized_arg = super().run()
		ContentDownloader(sanitized_arg[0]).download()