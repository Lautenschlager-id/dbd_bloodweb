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
