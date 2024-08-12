import multiprocessing

from .ConfigLoader import ConfigLoader
from core.MatchingListTextProcessor import MatchingListTextProcessor
from utils.enums import CONFIG_DIRECTORY

class ConfigLoaderPresets(ConfigLoader):
	@property
	def data_schema(self):
		str_pattern = MatchingListTextProcessor.RE_ENTRY_TEXT.pattern
		return {
			'type': 'object',
			'patternProperties': {
				'^[a-z0-9_]+$': {
					'type': 'object',
					'properties': {
						'match': {
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
						},
						'ignore': {
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
					},
					'required': ['match'],
					'additionalProperties': False
				},
			},
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