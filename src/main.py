from argparse import ArgumentParser

from core.command_handling.CommandHandlerImage import CommandHandlerImage
from core.command_handling.CommandHandlerGrind import CommandHandlerGrind

from core.ResourceHandler import ResourceHandler

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
		help='Target for the blodweeb grinding. E.g.: -r survivor, -r trapper'
	)
	#parser.add_argument('--noskip', action='store_true', help='Disables bloodweb level detection.')

	return parser.parse_args()

if __name__ == '__main__':
	args = capture_command_arguments()

	if args.image is not None:
		CommandHandlerImage(args.image).run()
	elif args.run is not None:
		CommandHandlerGrind(args.run).run()


	x = ResourceHandler('killers', 'nurse')
	print(x.match_list)

