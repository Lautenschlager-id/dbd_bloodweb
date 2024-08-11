from fnmatch import fnmatch

from .image_processing.ImageProcessorAddon import ImageProcessorAddon
from .image_processing.ImageProcessorItem import ImageProcessorItem
from .image_processing.ImageProcessorOffering import ImageProcessorOffering
from .image_processing.ImageProcessorPerk import ImageProcessorPerk
from .MatchingListTextProcessor import MatchingListTextProcessor
from .Resource import Resource
from config.ConfigLoader import PRESETS, SETTINGS
from utils.logger import logger
from utils.enums import (
	ADDON_TYPE,
	FILE_EXTENSION,
	IMAGE_PROCESSING_PARAMETER,
	IMAGE_PROCESSING_PARAMETER_TARGET,
	OFFERING_TYPE,
	PERK_TYPE
)

class ResourceHandler:
	def __init__(self, type, killer_name=None, preset_name=None):
		self.type = type
		self.killer_name = killer_name
		self.preset_name = preset_name # todo

		self.is_survivor = type in [
			ADDON_TYPE.SURVIVOR.value,
			OFFERING_TYPE.SURVIVOR.value,
			PERK_TYPE.SURVIVOR.value,
		]

		self.paths = None
		self.resources = None

		self.match_list = None
		self.ignore_list = None

	def initialize(self):
		logger.log('Selecting templates:')

		self._set_processed_paths()
		self._set_presets()
		self._set_resources_based_on_presets()

		self.resources.sort(key=lambda resource: resource.priority)
		logger.log('\n')
		for resource in self.resources:
		    logger.log(f'\t{str(resource)}')

		return self.resources

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

		self.paths = paths

	def _set_presets(self):
		preset = PRESETS.get(self.preset_name or self.killer_name or self.type)
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

	def _set_resources_based_on_presets(self):
		files = [
			f'.\\{file}'
			for path in self.paths
				for file in path.rglob(
					FILE_EXTENSION.PROCESSED_RESOURCE.as_unix_filename_pattern
				)
		]

		resources = []
		identified_files = {}

		self._filter_paths_with_presets(
			preset_list=self.match_list,
			ref_resources=resources,
			ref_files_to_iter=files,
			ref_identified_files_against_duplicates=identified_files
		)

		self._filter_paths_with_presets(
			preset_list=self.ignore_list,
			ref_resources=resources,
			ref_files_to_iter=files,
			ref_identified_files_against_duplicates=identified_files,
			priority=-1,
			ignore=True
		)

		self.resources = resources

	def _filter_paths_with_presets(self,
		preset_list,
		ref_resources,
		ref_files_to_iter,
		ref_identified_files_against_duplicates,
		priority=None,
		ignore=False
	):
		for index in range(len(preset_list)):
			preset = preset_list[index]

			pattern, threshold = None, None
			if isinstance(preset, list):
				pattern, threshold = preset
			else:
				pattern = preset

			matched_at_least_once = False
			for file in ref_files_to_iter:
				if (
					ref_identified_files_against_duplicates.get(file) is None
					and fnmatch(file, pattern)
				):
					matched_at_least_once = True
					ref_identified_files_against_duplicates[file] = True

					ref_resources.append(
						Resource(
							path=file,
							priority=priority or index,
							threshold=threshold,
							ignore=ignore
						)
					)

			assert matched_at_least_once, f'Pattern \'{pattern}\' did not match any resource file'
