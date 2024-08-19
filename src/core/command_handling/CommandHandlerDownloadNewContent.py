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
			'{full_command}: Downloads perks and addons from a new survivor/killer.'
			'\n'
				'\t>> Syntax:'
					'\n\t\t{full_command} <survivor name|killer name>'
			'\n\n'
				'\t>> Usage:'
					'\n\t\t{full_command} ace visconti'
					'\n\t\t{full_command} the skull merchant'
					'\n\t\t{full_command} skull merchant'
		).format(
			full_command=CommandHandlerDownloadNewContent.get_full_command()
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

	def run(self):
		sanitized_arg = super().run()
		ContentDownloader(sanitized_arg[0]).download()