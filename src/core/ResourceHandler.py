from .image_processing.ImageProcessorAddon import ImageProcessorAddon
from .image_processing.ImageProcessorItem import ImageProcessorItem
from .image_processing.ImageProcessorOffering import ImageProcessorOffering
from .image_processing.ImageProcessorPerk import ImageProcessorPerk
from .MatchingListTextProcessor import MatchingListTextProcessor
from config.ConfigLoader import PRESETS, SETTINGS
from utils.enums import (
	IMAGE_PROCESSING_PARAMETER, IMAGE_PROCESSING_PARAMETER_TARGET,
	ADDON_TYPE, OFFERING_TYPE, PERK_TYPE
)

class ResourceHandler:
	def __init__(self, type, killer_name=None):
		self.type = type
		self.killer_name = killer_name

		self.is_survivor = type in [
			ADDON_TYPE.SURVIVOR.value,
			OFFERING_TYPE.SURVIVOR.value,
			PERK_TYPE.SURVIVOR.value,
		]

		self.paths = None

		self.match_list = None
		self.ignore_list = None

		self._set_processed_paths()
		self._set_presets()

	def _set_processed_paths(self):
		paths = []

		if not SETTINGS.get('disable_offering_grinding'):
			paths.append(
				ImageProcessorOffering(IMAGE_PROCESSING_PARAMETER_TARGET.all.name)
					.path_resource_icon_processed
			)
			paths.append(ImageProcessorOffering(self.type).path_resource_icon_processed)

		if not SETTINGS.get('disable_item_grinding') and self.is_survivor:
			paths.append(ImageProcessorItem().path_resource_icon_processed)

		if not SETTINGS.get('disable_perk_grinding'):
			paths.append(ImageProcessorPerk(self.type).path_resource_icon_processed)

		if not SETTINGS.get('disable_addon_grinding'):
			if self.is_survivor:
				paths.append(ImageProcessorAddon(self.type).path_resource_icon_processed)
			else:
				paths.append(
					ImageProcessorAddon(self.type, IMAGE_PROCESSING_PARAMETER_TARGET.all.name)
						.path_resource_icon_processed
				)
				paths.append(
					ImageProcessorAddon(self.type, self.killer_name)
						.path_resource_icon_processed
				)

		self.path = paths

	def _set_presets(self):
		preset = PRESETS.get(self.killer_name or self.type)
		assert preset, f'Missing preset for {self.type}, {self.killer_name}'

		match_list = preset['match']
		ignore_list = preset.get('ignore', [])

		self.match_list = (
			MatchingListTextProcessor(match_list)
				.convert_all_lines_to_unix_file_name()
		)

		self.ignore_list = (
			MatchingListTextProcessor(ignore_list)
				.convert_all_lines_to_unix_file_name()
		)