from .ImageProcessorBase import ImageProcessorBase
from utils.enums import ADDON_TYPE, RESOURCE_DIRECTORY

class ImageProcessorAddon(ImageProcessorBase):
	default_side_icon_file = 'small.png'

	@property
	def path_resource_icon_base(self):
		path = (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('addons')
				.joinpath(self.type)
		)

		if self.killer_name is not None:
			path = path.joinpath(self.killer_name)

		return path

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('items')
		)

	@property
	def resource_icon_width(self):
		return 58

	@property
	def path_side_icon_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('addons')
				.joinpath('additional')
		)

	@property
	def side_icon_position(self):
		gravity = 'northeast'
		offset = '-5'
		return (gravity, offset)

	@property
	def resize_image_before_placing_side_icon(self):
		return True

	def __init__(self, type, killer_name=None):
		super().__init__()

		type = str(type)

		assert ADDON_TYPE.any_matching(type), f'Invalid addon type \'{type}\''
		self.type = type
		self.killer_name = killer_name

	# @override
	def _get_side_icon_template_by_path(self, _=None):
		return str(
			self.path_side_icon_template_base.joinpath(
				self.default_side_icon_file
			)
		)