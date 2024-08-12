from datetime import datetime
import jsonschema
import os
from pathlib import Path
import pyautogui

from .enums import RESOURCE_DIRECTORY

def get_all_killer_names():
	killers = [
		name.name
		for name in (
			RESOURCE_DIRECTORY.RAW_RESOURCE.full_path
				.joinpath('addon')
				.joinpath('killer')
			).glob('*')
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

def get_last_directory(parent_directory):
	parent_path = Path(parent_directory)

	directories = [
		dir for dir in parent_path.iterdir()
	]

	if not directories:
		return None

	last_directory = max(directories, key=lambda dir: dir.stat().st_ctime)
	return last_directory

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