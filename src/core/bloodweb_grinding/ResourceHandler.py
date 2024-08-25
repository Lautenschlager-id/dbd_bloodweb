from fnmatch import fnmatch
from sys import exit

from .MatchingListTextProcessor import MatchingListTextProcessor
from .Resource import Resource
from config.ConfigLoaderPresets import PRESETS
from config.ConfigLoaderSettings import SETTINGS
from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from core.image_processing.ImageProcessorItem import ImageProcessorItem
from core.image_processing.ImageProcessorOffering import ImageProcessorOffering
from core.image_processing.ImageProcessorPerk import ImageProcessorPerk
from utils.enums import (
	ADDON_TYPE,
	FILE_EXTENSION,
	IMAGE_PROCESSING_PARAMETER,
	IMAGE_PROCESSING_PARAMETER_TARGET,
	OFFERING_TYPE,
	PERK_TYPE
)
from utils.logger import logger

class ResourceHandler:
	def __init__(self, type, killer_name=None, preset_name=None):
		self.type = type
		self.killer_name = killer_name
		self.preset_name = preset_name

		self.is_survivor = type in [
			ADDON_TYPE.SURVIVOR.value,
			OFFERING_TYPE.SURVIVOR.value,
			PERK_TYPE.SURVIVOR.value,
		]

		self.paths = None
		self.resources = None

		self.match_list = None
		self.ignore_list = None
		self.match_exception_list = None

	def initialize(self):
		self._set_processed_paths()
		self._set_presets()
		self._set_resources_based_on_presets()

		self.resources.sort(key=lambda resource: resource.priority)

		logger.init(
			'resource',
			'Selected resources for preset <{}, {}, {}>:'
			, self.type
			, self.killer_name
			, self.preset_name
		)

		logger.action('[')

		logger.detail(
			'{}'
			, '\n\t\t'.join([
				str(resource)
				for resource in self.resources
			])
		)

		logger.action(']')

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

		if not preset:
			logger.result(
				'Missing preset for <{}, {}, {}>:'
				, self.type
				, self.killer_name
				, self.preset_name
			)
			exit()

		match_list = preset['match']
		ignore_list = preset.get('ignore', [])
		match_exception_list = preset.get('match_exception', [])

		self.match_list = (
			MatchingListTextProcessor(match_list)
				.get_data_from_all_identifiers()
		)

		self.ignore_list = (
			MatchingListTextProcessor(ignore_list)
				.get_data_from_all_identifiers()
		)

		self.match_exception_list = (
			MatchingListTextProcessor(match_exception_list)
				.get_data_from_all_identifiers()
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

		# Blocks the 'identified_files' for certain patterns
		# E.g.: match: *, exception: abc = matches all (*), except (abc)
		self._filter_paths_with_presets(
			preset_list=self.match_exception_list,
			ref_files_to_iter=files,
			ref_identified_files_against_duplicates=identified_files,
			ref_resources=None
		)

		# List of items to be compared and considered
		self._filter_paths_with_presets(
			preset_list=self.match_list,
			ref_files_to_iter=files,
			ref_identified_files_against_duplicates=identified_files,
			ref_resources=resources
		)

		# List of items to be compared but not considered
		self._filter_paths_with_presets(
			preset_list=self.ignore_list,
			ref_files_to_iter=files,
			ref_identified_files_against_duplicates=identified_files,
			ref_resources=resources,
			priority=-1,
			ignore=True
		)

		self.resources = resources

	def _filter_paths_with_presets(self,
		preset_list,
		ref_files_to_iter,
		ref_identified_files_against_duplicates,
		ref_resources=None,
		priority=None,
		ignore=False,
	):
		should_exit = False

		for index in range(len(preset_list)):
			preset = preset_list[index]

			pattern = preset.pattern
			threshold = preset.threshold

			matched_at_least_once = False
			for file in ref_files_to_iter:
				if (
					ref_identified_files_against_duplicates.get(file) is None
					and fnmatch(file, pattern)
				):
					matched_at_least_once = True
					ref_identified_files_against_duplicates[file] = True

					if ref_resources is not None:
						ref_resources.append(
							Resource(
								path=file,
								priority=priority or index,
								threshold=threshold,
								ignore=ignore
							)
						)

			if not matched_at_least_once:
				logger.result(
					'Pattern \'{}\' did not match any resource file'
					, pattern
				)
				should_exit = True

		if should_exit:
			exit()