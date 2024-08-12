from .ImageProcessorBase import ImageProcessorBase
from utils.enums import ADDON_TYPE, RESOURCE_DIRECTORY
from utils.functions import get_all_killer_names
from utils.logger import logger

class ImageProcessorAddon(ImageProcessorBase):
	default_side_icon_file = 'small.png'

	@property
	def path_resource_icon_base(self):
		path = (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('addon')
				.joinpath(self.type)
		)

		if self.killer_name is not None:
			path = path.joinpath(self.killer_name)

		return path

	@property
	def path_background_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('item')
		)

	@property
	def resource_icon_width(self):
		return 58

	@property
	def path_side_icon_template_base(self):
		return (
			RESOURCE_DIRECTORY.TEMPLATE.full_path
				.joinpath('addon')
				.joinpath('side')
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
		type = str(type)

		logger.log(
			'\n[image] Initialized %s <%s, %s>'
			, self.class_name,
			type,
			killer_name
		)

		if not ADDON_TYPE.any_matching(type):
			logger.log(
				'\t=> Invalid addon type \'%s\''
				, type
			)
			exit()

		if type == ADDON_TYPE.KILLER.value and killer_name:
			killer_name = str(killer_name)

			killers = get_all_killer_names()
			if killer_name not in killers:
				logger.log(
					'\t=> Invalid killer name \'%s\'.'
					'\n\n'
						'\t\t'
						'Available killers:'
							'\n\t\t\t%s'
					, killer_name,
					'\n\t\t\t'.join(killers)
				)
				exit()

		self.type = type
		self.killer_name = killer_name
		super().__init__()

	# @override
	def _get_side_icon_template_by_path(self, _=None):
		return str(
			self.path_side_icon_template_base.joinpath(
				self.default_side_icon_file
			)
		)