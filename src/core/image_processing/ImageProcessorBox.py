from .ImageProcessorBase import ImageProcessorBase
from utils.enums import RESOURCE_DIRECTORY
from utils.logger import logger

class ImageProcessorBox(ImageProcessorBase):
	@property
	def path_resource_icon_base(self):
		return (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('box')
		)

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('box')
		)

	@property
	def resource_icon_width(self):
		return 70

	def __init__(self):
		logger.init(
			'image'
			, 'Initialized {}'
			, self.class_name
		)

		super().__init__()