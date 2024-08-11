from datetime import datetime
import jsonschema
import os
import pyautogui

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

def create_directory(parent_directory, directory_name):
	directory = f'{parent_directory}\\{directory_name}'
	os.makedirs(directory, exist_ok=True)
	return directory

def create_timestamp_directory(parent_directory):
	timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')
	return create_directory(parent_directory, timestamp)

def take_screenshot(region=None, save_path=None):
	screenshot = pyautogui.screenshot(region=region)

	if save_path is not None:
		screenshot.save(save_path)

	return (save_path, screenshot)

def extend_jsonschema_with_default_fields(validator_class):
	validate_properties = validator_class.VALIDATORS["properties"]

	def set_defaults(validator, properties, instance, schema):
		for property, subschema in properties.items():
			if "default" in subschema:
				instance.setdefault(property, subschema["default"])

		for error in validate_properties(
			validator, properties, instance, schema,
		):
			yield error

	return jsonschema.validators.extend(
		validator_class, {"properties" : set_defaults},
	)

jsonschema_with_default = extend_jsonschema_with_default_fields(jsonschema.Draft202012Validator)