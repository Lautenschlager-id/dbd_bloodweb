from abc import ABC, abstractmethod
from pathlib import Path
import os
import re

from ImageMagickWrapper import ImageMagickWrapper
from ...utils.enums import ROOT_DIRECTORY, FILE_EXTENSION

class ImageProcessor(ABC):
	RE_TEMPLATE_ID = re.compile(r'template_(\d)')

	@property
	@abstractmethod
	def path_resource_icon_base(self): pass

	@property
	@abstractmethod
	def path_background_template_base(self): pass

	@property
	@abstractmethod
	def resource_icon_width(self): pass

	@property
	@abstractmethod
	def path_side_icon_template_base(self): pass

	@property
	@abstractmethod
	def side_icon_position(self): pass

	@property
	@abstractmethod
	def resize_image_before_placing_side_icon(self): pass

	def __init__(self):
		self.magick = ImageMagickWrapper(
			final_extension=FILE_EXTENSION.PROCESSED_RESOURCE.name,
			resource_icon_width=self.resource_icon_width,
			side_icon_position=self.side_icon_position
		)

	def combine_image_resources(self, path_resource_icon, custom_output_template_id=None):
		self.magick.convert_resource_extension(path_resource_icon)

		path_resource_icon = self._evaluate_custom_resource_icon_template(
			path_resource_icon,
			custom_output_template_id
		)

		self.magick.place_background_template(
			self._get_background_template_by_path(path_resource_icon)
		)

		self.magick.resize_image()

		if self.path_side_icon_template_base is not None:
			self.magick.place_side_icon_template(
				self._get_side_icon_template_by_path(path_resource_icon)
			)

			if self.resize_image_before_placing_side_icon is True:
				self.magick.swap_last_command()

		output_path = self._get_processed_resource_path(path_resource_icon)
		self.magick.save_image(output_path)

	def _evaluate_custom_resource_icon_template(self, path_resource_icon, custom_output_template_id):
		if custom_output_template_id is None:
			return path_resource_icon

		original_path_resource_icon = str(path_resource_icon)

		custom_path_resource_icon = self.RE_TEMPLATE_ID.sub(
			f'template_{custom_output_template_id}',
			original_path_resource_icon
		)

		return Path(custom_path_resource_icon)

	def _get_background_template_by_path(self, path_resource_icon):
		template_id = self._get_template_id(path_resource_icon, include_extension=True)
		return self._get_background_template(template_id)

	def _get_background_template(template_id):
		return str(self.path_background_template_base.joinpath(template_id))

	def _get_side_icon_template_by_path(self, path_resource_icon):
		template_id = self._get_template_id(path_resource_icon, include_extension=True)
		return self._get_side_icon_template(template_id)

	def _get_side_icon_template(template_id):
		return str(self.path_side_icon_template_base.joinpath(template_id))

	def _get_template_id(self, path_resource, include_extension=False):
		template_id = self.RE_TEMPLATE_ID.search(str(path_resource)).group(1)
		if include_extension:
			template_id += FILE_EXTENSION.PROCESSED_RESOURCE
		return template_id

	def _get_processed_resource_path(self, path_resource_icon):
		self._start_processed_resource_directory(path_resource_icon)

		output_path = str(path_resource_icon).replace(
			ROOT_DIRECTORY.RAW_RESOURCE,
			ROOT_DIRECTORY.PROCESSED_RESOURCE
		).replace(
			FILE_EXTENSION.RAW_RESOURCE,
			FILE_EXTENSION.PROCESSED_RESOURCE
		)

		return output_path

	def _start_processed_resource_directory(self, path_resource_icon):
		output_dir = str(path_resource_icon.parent).replace(
			ROOT_DIRECTORY.RAW_RESOURCE,
			ROOT_DIRECTORY.PROCESSED_RESOURCE
		)
		os.makedirs(output_dir, exist_ok=True)