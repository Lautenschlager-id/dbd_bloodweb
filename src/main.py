from argparse import ArgumentParser

from core.command_handling.CommandHandlerImage import CommandHandlerImage
from core.command_handling.CommandHandlerGrind import CommandHandlerGrind
from core.command_handling.CommandHandlerSetPrestigeLimit import CommandHandlerSetPrestigeLimit

def capture_command_arguments():
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

	return parser.parse_args()

if __name__ == '__main__':
	args = capture_command_arguments()

	if args.image is not None:
		CommandHandlerImage(args.image).run()
	else:
		if args.p is not None:
			CommandHandlerSetPrestigeLimit(args.p).run()

		if args.run is not None:
			CommandHandlerGrind(args.run).run()