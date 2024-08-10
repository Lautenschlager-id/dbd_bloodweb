from .ImageProcessorBase import ImageProcessorBase
from utils.enums import ROOT_DIRECTORY, OFFERING_TYPE

class ImageProcessorOffering(ImageProcessorBase):
	@property
	def path_resource_icon_base(self):
		return (
			ROOT_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('offerings')
				.joinpath(self.type)
		)

	@property
	def path_background_template_base(self):
		return (
			ROOT_DIRECTORY.TEMPLATE.full_path
				.joinpath('offerings')
		)

	@property
	def resource_icon_width(self):
		return 70

	def __init__(self, type):
		super().__init__()

		type = str(type)

		assert OFFERING_TYPE.any_matching(type), "Invalid offering type"
		self.type = type