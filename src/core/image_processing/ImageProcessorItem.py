from pathlib import Path

from ImageProcessor import ImageProcessor
from ...utils.enums import ROOT_DIRECTORY

class ImageProcessorItem(ImageProcessor):
	@property
	def path_resource_icon_base(self):
		return ROOT_DIRECTORY.RAW_RESOURCE.full_path
			.joinpath('items')
			.joinpath('survivors')

	@property
	def path_background_template_base(self):
		return ROOT_DIRECTORY.TEMPLATE.full_path
			.joinpath('items')

	@property
	def resource_icon_width(self):
		return 55