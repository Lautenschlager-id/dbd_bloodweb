from argparse import ArgumentParser
import sys

from .CommandHandlerDownloadNewContent import CommandHandlerDownloadNewContent
from .CommandHandlerGrind import CommandHandlerGrind
from .CommandHandlerImage import CommandHandlerImage
from .CommandHandlerSetLevelLimit import CommandHandlerSetLevelLimit
from .CommandHandlerSetPrestigeLimit import CommandHandlerSetPrestigeLimit
from config.ConfigLoaderSettings import SETTINGS

class CommandListener:
	def execute(self):
		args = self._capture_command_arguments()

		if args.image is not None:
			CommandHandlerImage(args.image).run()
		elif args.download is not None:
			CommandHandlerDownloadNewContent(args.download).run()
		else:
			if args.p is not None:
				CommandHandlerSetPrestigeLimit(args.p).run()
			if args.l is not None:
				CommandHandlerSetLevelLimit(args.l).run()

			if args.run is not None:
				CommandHandlerGrind(args.run).run()

	def _capture_command_arguments(cls):
		parser = ArgumentParser()

		argument_parameter_info = CommandHandlerImage.get_argument_parameter_info()
		parser.add_argument(
			CommandHandlerImage.get_short_command(),
			CommandHandlerImage.get_full_command(),
			type=argument_parameter_info['type'],
			nargs=argument_parameter_info['nargs'],
			help=CommandHandlerImage.get_help_message()
		)

		argument_parameter_info = CommandHandlerGrind.get_argument_parameter_info()
		parser.add_argument(
			CommandHandlerGrind.get_short_command(),
			CommandHandlerGrind.get_full_command(),
			type=argument_parameter_info['type'],
			nargs=argument_parameter_info['nargs'],
			help=CommandHandlerGrind.get_help_message()
		)

		argument_parameter_info = CommandHandlerSetPrestigeLimit.get_argument_parameter_info()
		parser.add_argument(
			CommandHandlerSetPrestigeLimit.get_short_command(),
			type=argument_parameter_info['type'],
			nargs=argument_parameter_info['nargs'],
			help=CommandHandlerSetPrestigeLimit.get_help_message()
		)

		argument_parameter_info = CommandHandlerSetLevelLimit.get_argument_parameter_info()
		parser.add_argument(
			CommandHandlerSetLevelLimit.get_short_command(),
			type=argument_parameter_info['type'],
			nargs=argument_parameter_info['nargs'],
			help=CommandHandlerSetLevelLimit.get_help_message()
		)

		argument_parameter_info = CommandHandlerDownloadNewContent.get_argument_parameter_info()
		parser.add_argument(
			CommandHandlerDownloadNewContent.get_short_command(),
			CommandHandlerDownloadNewContent.get_full_command(),
			type=argument_parameter_info['type'],
			nargs=argument_parameter_info['nargs'],
			help=CommandHandlerDownloadNewContent.get_help_message()
		)

		setting_parameters = SETTINGS.get('parameters') + sys.argv[1:]
		return parser.parse_args(args=setting_parameters)