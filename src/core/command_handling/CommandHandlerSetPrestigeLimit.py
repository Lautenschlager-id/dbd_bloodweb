from .CommandHandlerBase import CommandHandlerBase
from config.ConfigLoaderSettings import SETTINGS
from core.BloodwebHandler import BloodwebHandler

class CommandHandlerSetPrestigeLimit(CommandHandlerBase):
	def help(self):
		if self.args: return False

		print('=> Limits how many prestiges the system will attempt to grind.')

		print('\n')

		print('Syntax:'
			'\n\t--p <prestiges>')

		print('\n')

		print('Usage:'
			'\n\t--p 1')

		return True

	def sanitize_arg(self):
		arg_prestiges = self.args[0]
		try:
			arg_prestiges = int(arg_prestiges)

			if arg_prestiges < 1:
				raise

			if SETTINGS.get('use_bloodweb_level_controller') is False:
				print(
					f'Command \'--p\' cannot be used: '
					'setting \'use_bloodweb_level_controller\' is False'
				)
				return

			return [arg_prestiges]
		except:
			print(
				f'Invalid <prestiges> \'{arg_prestiges}\'. '
				'The prestige should be a positive number.'
			)
			return

	def run(self):
		if self.help(): return

		sanitized_arg = self.sanitize_arg()
		if sanitized_arg is None:
			exit()

		BloodwebHandler.set_maximum_prestiges(sanitized_arg[0])
