from pathlib import Path

from ImageProcessor import ImageProcessor
from ...utils.enums import ROOT_DIRECTORY, PERK_TYPE

class ImageProcessorPerk(ImageProcessor):
	template_with_all_icon_resources = 'template_1'

	@property
	def path_resource_icon_base(self):
		return ROOT_DIRECTORY.RAW_RESOURCE.full_path
			.joinpath('perks')
			.joinpath(self.type)
			.joinpath(self.template_with_all_icon_resources)

	@property
	def path_background_template_base(self):
		return ROOT_DIRECTORY.TEMPLATE.full_path
			.joinpath('perks')

	@property
	def resource_icon_width(self):
		return 70

	@property
	def path_side_icon_template_base(self):
		return self.path_background_template_base
			.joinpath('additional')

	@property
	def side_icon_position(self):
		gravity = 'center'
		offset = '+0'
		return (gravity, offset)

	def __init__(self, type):
		assert PERK_TYPE.any_matching(type), "Invalid perk type"
		self.type = type
		#'        self.reuse_resource_for_all_templates=True'