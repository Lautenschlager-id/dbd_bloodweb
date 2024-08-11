from .ConfigLoader import ConfigLoader
from utils.enums import CONFIG_DIRECTORY, GRIND_STRATEGY

class ConfigLoaderSettings(ConfigLoader):
	@property
	def data_schema(self):
		return {
		    'type': 'object',
		    'properties': {
		        'default_matching_threshold': {
		            'type': 'number',
		            'minimum': 0,
		            'maximum': 1,
		            'default': 0.75
		        },
		        'default_ignore_threshold': {
		            'type': 'number',
		            'minimum': 0,
		            'maximum': 1,
		            # it's best if it's > default_matching_threshold
		            'default': 0.78
		        },
		        'grind_strategy': {
		            'type': 'string',
		            'enum': list(GRIND_STRATEGY.values()),
		            'default': GRIND_STRATEGY.DEFAULT.value
		        },
		        'use_bloodweb_level_controller': {
		            'type': 'boolean',
		            'default': True
		        },
		        'disable_addon_grinding': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_item_grinding': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_offering_grinding': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_perk_grinding': {
		            'type': 'boolean',
		            'default': True
		        },
		        'log_ignored_matches': {
		            'type': 'boolean',
		            'default': False
		        }
		    },
		    'additionalProperties': False
		}

	@property
	def config_path(self):
		return CONFIG_DIRECTORY.SETTING.full_path

SETTINGS = ConfigLoaderSettings()
