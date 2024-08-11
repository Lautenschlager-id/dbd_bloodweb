from .ImageProcessorBase import ImageProcessorBase
from utils.enums import RESOURCE_DIRECTORY

class ImageProcessorItem(ImageProcessorBase):
	@property
	def path_resource_icon_base(self):
		return (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('item')
				.joinpath('survivor')
		)

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('item')
		)

	@property
	def resource_icon_width(self):
		return 55