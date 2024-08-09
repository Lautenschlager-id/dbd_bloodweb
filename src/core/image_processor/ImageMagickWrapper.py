import subprocess

class ImageMagickWrapper:
	def __init__(self,
		final_extension,
		resource_icon_width,
		side_icon_position=None
	):
		self.final_extension = final_extension
		self.resource_icon_width = resource_icon_width
		if side_icon_position is not None:
			(side_icon_gravity, side_icon_offset) = side_icon_position
			self.side_icon_gravity = side_icon_gravity
			self.side_icon_offset = str(side_icon_offset)

		self.command_list = []

	def convert_resource_extension(self, path_resource_icon):
		command = f'magick {str(path_resource_icon)} {self.final_extension}:-'
		self._add_command_to_list(command)

	def place_background_template(self, path_background_template):
		command = (
			f'magick composite -gravity center'
			f' - {path_background_template} {self.final_extension}:-'
		)
		self._add_command_to_list(command)

	def resize_image(self):
		command = f'magick - -resize {self.resource_icon_width}x {self.final_extension}:-'
		self._add_command_to_list(command)

	def place_side_icon_template(self, path_side_icon_template):
		command = (
			f'magick composite -gravity {self.side_icon_gravity} '
			f'-geometry {2 * self.side_icon_offset} '
			f'{path_side_icon_template} - {self.final_extension}:-'
		)
		self._add_command_to_list(command)

	def swap_last_command(self):
		self.command_list[-1], self.command_list[-2] = self.command_list[-2], self.command_list[-1]

	def save_image(self, output_path):
		commands = ' | '.join(self.command_list)

		command_to_execute = f'{commands} > {output_path}'
		subprocess.call(command_to_execute, shell=True)

		self.command_list = []

	def _add_command_to_list(self, command):
		self.command_list.append(command)