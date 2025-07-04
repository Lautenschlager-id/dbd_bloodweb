import multiprocessing

from .ConfigLoader import ConfigLoader
from utils.enums import CONFIG_DIRECTORY, GRIND_STRATEGY

class ConfigLoaderSettings(ConfigLoader):
	@property
	def data_schema(self):
		return {
		    'type': 'object',
		    'properties': {
		    	'parameters': {
		    		'type': 'array',
		    		'default': []
		    	},
		        'default_match_and_grind_threshold': {
		            'type': 'number',
		            'minimum': 0,
		            'maximum': 1,
		            'default': 0.75
		        },
		        'default_match_and_skip_threshold': {
		            'type': 'number',
		            'minimum': 0,
		            'maximum': 1,
		            # it's best if it's > default_match_and_grind_threshold
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
		        'disable_addon_resources': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_item_resources': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_offering_resources': {
		            'type': 'boolean',
		            'default': False
		        },
		        'disable_perk_resources': {
		            'type': 'boolean',
		            'default': True
		        },
				'disable_box_resources': {
		            'type': 'boolean',
		            'default': True
		        },
		        'log_skipped_matches': {
		            'type': 'boolean',
		            'default': False
		        }
		    },
		    'additionalProperties': False
		}

	@property
	def config_path(self):
		return CONFIG_DIRECTORY.SETTING.full_path

SETTINGS = (
	ConfigLoaderSettings()
	if multiprocessing.current_process().name == 'MainProcess'
	else None
)