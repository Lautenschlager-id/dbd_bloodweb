from .CommandHandlerBase import CommandHandlerBase
from config.ConfigLoaderPresets import PRESETS
from core.BloodwebHandler import BloodwebHandler
from core.ImageMatcher import ImageMatcher
from core.ResourceHandler import ResourceHandler
from utils.enums import IMAGE_PROCESSING_PARAMETER_TARGET

class CommandHandlerGrind(CommandHandlerBase):
	def help(self):
		if self.args: return False

		print('=> Identifies preset nodes and grinds them on the current bloodweb.')

		print('\n')

		print('Syntax:'
			'\n\t--run <preset>')

		print('\n')

		print(f'Available presets:\n\t{PRESETS.list_keys()}')

		print('\n')

		print('Usage:'
			'\n\t--run survivor'
			'\n\t--run trapper')

		return True

	def sanitize_arg(self):
		arg_preset = self.args[0]
		if arg_preset not in PRESETS.list_keys():
			print(f'No such <preset> \'{arg_preset}\'. Type \'-r\' to see the full list.')
			return

		killer_name = None
		if arg_preset != IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name:
			killer_name = arg_preset
			arg_preset = IMAGE_PROCESSING_PARAMETER_TARGET.killer.name

		return [arg_preset, killer_name]

	def run(self):
		if self.help(): return

		sanitized_arg = self.sanitize_arg()
		if sanitized_arg is None: return

		resources = ResourceHandler(*sanitized_arg).initialize()
		ImageMatcher.set_resources(resources)

		bloodweb = BloodwebHandler()
		bloodweb.grind()