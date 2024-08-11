from datetime import datetime
import os

from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from .enums import ADDON_TYPE

def get_all_killer_names():
	killers = [
		name.name
		for name in ImageProcessorAddon(ADDON_TYPE.KILLER).path_resource_icon_base.glob('*')
	]
	return killers

def get_list_value(array, index, default=None):
	try:
		return array[index]
	except:
		return default

def create_timestamp_directory(parent_directory):
    timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')

    timestamp_directory = f'{parent_directory}/00_TEST_{timestamp}/'
    os.makedirs(timestamp_directory, exist_ok=True)

    return timestamp_directory