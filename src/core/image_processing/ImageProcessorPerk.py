from sys import exit

from .ImageProcessorBase import ImageProcessorBase
from utils.enums import PERK_TYPE, RESOURCE_DIRECTORY
from utils.logger import logger
from utils.ResolutionAdapter import ResolutionAdapter

class ImageProcessorPerk(ImageProcessorBase):
	template_with_all_icon_resources = 'template_1'

	@property
	def path_resource_icon_base(self):
		return (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('perk')
				.joinpath(self.type)
				.joinpath(self.template_with_all_icon_resources)
		)

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('perk')
		)

	@property
	def resource_icon_width(self):
		return ResolutionAdapter.get_width(70)

	@property
	def path_side_icon_template_base(self):
		return (
			self.path_background_template_base
				.joinpath('side')
		)

	@property
	def side_icon_position(self):
		gravity = 'center'
		offset = '+0'
		return (gravity, offset)

	@property
	def apply_resources_from_one_template_to_all_templates(self):
		return True

	def __init__(self, type):
		type = str(type)

		logger.init(
			'image'
			, 'Initialized {} <{}>'
			, self.class_name,
			type
		)

		if not PERK_TYPE.any_matching(type):
			logger.result(
				'Invalid perk type \'{}\''
				, type
			)
			exit()

		self.type = type
		super().__init__()
