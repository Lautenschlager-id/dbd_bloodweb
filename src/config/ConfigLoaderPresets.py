import multiprocessing

from .ConfigLoader import ConfigLoader
from core.bloodweb_grinding.MatchingListTextProcessor import MatchingListTextProcessor
from utils.enums import CONFIG_DIRECTORY, IMAGE_PROCESSING_PARAMETER_TARGET

class ConfigLoaderPresets(ConfigLoader):
	@property
	def data_schema(self):
		str_pattern = MatchingListTextProcessor.RE_ENTRY_TEXT.pattern

		obj_structure = {
			'type': 'array',
			'items': {
				'oneOf': [
					{
						'type': 'string',
						'pattern': str_pattern
					},
					{
						'type': 'array',
						'prefixItems': [
							{
								'type': 'string',
								'pattern': str_pattern
							},
							{
								'type': 'number',
								'minimum': 0,
								'maximum': 1
							}
						],
						'minItems': 2,
						'maxItems': 2
					}
				]
			}
		}

		return {
			'type': 'object',
			'patternProperties': {
				'^[a-z0-9_]+$': {
					'type': 'object',
					'properties': {
						'match_and_grind': obj_structure,
						'match_and_skip': obj_structure,
						'wildcard_exception': obj_structure
					},
					'required': ['match_and_grind'],
					'additionalProperties': False
				},
			},
			'required': [IMAGE_PROCESSING_PARAMETER_TARGET.survivor.name],
			'additionalProperties': False
		}

	@property
	def config_path(self):
		return CONFIG_DIRECTORY.PRESET.full_path

PRESETS = (
	ConfigLoaderPresets()
	if multiprocessing.current_process().name == 'MainProcess'
	else None
)