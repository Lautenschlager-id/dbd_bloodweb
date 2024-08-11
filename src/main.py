from argparse import ArgumentParser

from core.command_handling.CommandHandlerImage import CommandHandlerImage
from core.command_handling.CommandHandlerGrind import CommandHandlerGrind
from core.command_handling.CommandHandlerSetPrestigeLimit import CommandHandlerSetPrestigeLimit

def capture_command_arguments():
	parser = ArgumentParser()

	parser.add_argument(
		'-i', '--image',
		type=str,
		nargs='*',
		help='Process images. E.g.: -i addon killer trapper, -i offering all'
	)
	parser.add_argument(
		'-r', '--run',
		type=str,
		nargs='*',
		help='Target for the blodweeb grinding. E.g.: -r survivor, -r trapper'
	)
	parser.add_argument(
		'-p',
		type=int,
		nargs='*',
		help='Limits how many prestiges the system will attempt to grind. E.g.: -l 2'
	)

	return parser.parse_args()

if __name__ == '__main__':
	args = capture_command_arguments()

	if args.image is not None:
		CommandHandlerImage(args.image).run()
	elif args.run is not None:
		if args.p is not None:
			CommandHandlerSetPrestigeLimit(args.p).run()

		CommandHandlerGrind(args.run).run()