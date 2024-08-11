from .ImageProcessorBase import ImageProcessorBase
from utils.enums import OFFERING_TYPE, RESOURCE_DIRECTORY

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
		super().__init__()

		type = str(type)

		assert OFFERING_TYPE.any_matching(type), f'Invalid offering type \'{type}\''
		self.type = type