from .ImageProcessorBase import ImageProcessorBase
from utils.enums import RESOURCE_DIRECTORY, PERK_TYPE

class ImageProcessorPerk(ImageProcessorBase):
	template_with_all_icon_resources = 'template_1'

	@property
	def path_resource_icon_base(self):
		return (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('perks')
				.joinpath(self.type)
				.joinpath(self.template_with_all_icon_resources)
		)

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('perks')
		)

	@property
	def resource_icon_width(self):
		return 70

	@property
	def path_side_icon_template_base(self):
		return (
			self.path_background_template_base
				.joinpath('additional')
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
		super().__init__()

		type = str(type)

		assert PERK_TYPE.any_matching(type), f'Invalid perk type \'{type}\''
		self.type = type
		#'        self.reuse_resource_for_all_templates=True'