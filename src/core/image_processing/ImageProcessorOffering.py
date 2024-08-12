from .ImageProcessorBase import ImageProcessorBase
from utils.enums import OFFERING_TYPE, RESOURCE_DIRECTORY
from utils.logger import logger

class ImageProcessorOffering(ImageProcessorBase):
	@property
	def path_resource_icon_base(self):
		return (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('offering')
				.joinpath(self.type)
		)

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('offering')
		)

	@property
	def resource_icon_width(self):
		return 70

	def __init__(self, type):
		type = str(type)

		logger.init(
			'image'
			, 'Initialized {} <{}>'
			, self.class_name
			, type
		)

		if not OFFERING_TYPE.any_matching(type):
			logger.result(
				'Invalid offering type \'{}\''
				, type
			)
			exit()

		self.type = type
		super().__init__()