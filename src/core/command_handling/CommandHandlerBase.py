from abc import ABC, abstractmethod

class CommandHandlerBase(ABC):
	def __init__(self, args):
		self.args = args

	@abstractmethod
	def help(self): pass

	def sanitize_arg(self): pass

	@abstractmethod
	def run(self): pass