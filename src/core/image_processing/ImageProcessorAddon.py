from pathlib import Path

from ImageProcessor import ImageProcessor
from ...utils.enums import ROOT_DIRECTORY, ADDON_TYPE

class ImageProcessorAddon(ImageProcessor):
	default_side_icon_file = 'small.png'

	@property
	def path_resource_icon_base(self):
		path = ROOT_DIRECTORY.RAW_RESOURCE.full_path
			.joinpath('addons')
			.joinpath(self.type)

		if self.killer_name is not None:
			path.joinpath(self.killer_name)

		return path

	@property
	def path_background_template_base(self):
		return ROOT_DIRECTORY.TEMPLATE.full_path
			.joinpath('items')

	@property
	def resource_icon_width(self):
		return 58

	@property
	def path_side_icon_template_base(self):
		return self.path_background_template_base
			.joinpath('additional')

	@property
	def side_icon_position(self):
		gravity = 'northeast'
		offset = '-5'
		return (gravity, offset)

	@property
	def resize_image_before_placing_side_icon(self):
		return True

	def __init__(self, type, killer_name=None):
		assert ADDON_TYPE.any_matching(type), "Invalid addon type"
		self.type = type

		if type == ADDON_TYPE.KILLER:
			assert killer_name is not None, "Missing killer name"
			self.killer_name = killer_name

	# @override
	def _get_side_icon_template_by_path(self):
		return str(
			self.path_side_icon_template_base.joinpath(
				self.default_side_icon_file
			)
		)