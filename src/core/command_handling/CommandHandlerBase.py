from abc import ABC, abstractmethod

from utils.logger import logger

class CommandHandlerBase(ABC):
	@staticmethod
	@abstractmethod
	def get_full_command(): pass

	@staticmethod
	@abstractmethod
	def get_short_command(): pass

	@staticmethod
	@abstractmethod
	def get_help_message(): pass

	@staticmethod
	@abstractmethod
	def get_argument_parameter_info(): pass

	def __init__(self, args):
		self.args = args

	def help(self):
		if self.args: return
		logger.init(
			'help'
			, self.__class__.get_help_message()
			, breakline=True
		)
		exit()

	@abstractmethod
	def sanitize_arg(self):
		logger.action('Validating parameters')

	@abstractmethod
	def run(self):
		self.help()

		logger.init(
			'cmd'
			, 'Running command \'{}\''
			, (
				self.__class__.get_full_command()
				or self.__class__.get_short_command()
			)
		)

		sanitized_arg = self.sanitize_arg()

		if sanitized_arg is None:
			exit()

		logger.result('Valid parameters!')

		return sanitized_arg