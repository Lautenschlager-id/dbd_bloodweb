import requests
import os
from sys import exit

from utils.enums import FILE_EXTENSION, ICON_TYPE
from utils.logger import logger

class Icon:
	rarity_map = {
		"common-item-element": 1,
		"uncommon-item-element": 2,
		"rare-item-element": 3,
		"very-rare-item-element": 4,
		"ultra-rare-item-element": 5
	}

	def __init__(self, icon, type):
		if not ICON_TYPE.any_matching(type):
			logger.result(
				'Invalid icon type \'{}\''
				, type
				, log_level=2
			)
			exit()

		self.icon = icon
		self.type = type

		self.source = icon.get('data-src')

		file_name = self.source.split('/')[-3][:-4]
		self.name = file_name
		self.file_name = f'{file_name}{FILE_EXTENSION.RAW_RESOURCE}'

		self.is_addon = type == ICON_TYPE.ADDON.value
		if self.is_addon:
			self.rarity = self.search_rarity()

	def __str__(self):
		if self.is_addon:
			return f'Icon(name={self.name}, type={self.type}, rarity={self.rarity})'
		else:
			return f'Icon(name={self.name}, type={self.type})'

	def search_rarity(self):
		rarity_div = self.icon.find_parent('div').find_parent('div').find()
		rarity = rarity_div.get('class')[-1]

		mapped_rarity = self.rarity_map.get(rarity)
		if mapped_rarity is None:
			logger.result(
				'Got unknown rarity type \'{}\' for image \'{}\'.'
				, rarity
				, self.name
				, log_level=2
			)
			exit()

		return mapped_rarity

	def get_image_binary(self):
		try:
			response = requests.get(self.source, stream=True)
			response.raise_for_status()
			return response
		except Exception as exception:
			logger.result(
				'Could not get URL {}: {}'
				, self.source
				, exception
				, log_level=2
			)
			exit()

	def save_in_local_path(self, path):
		try:
			if self.is_addon:
				path = path.joinpath(f'template_{self.rarity}')
				os.makedirs(path, exist_ok=True)

			path = path.joinpath(self.file_name)
			with open(path, 'wb') as file:
				for chunk in self.get_image_binary().iter_content(chunk_size=8192):
					file.write(chunk)

			logger.detail(
				'Saved file \'{}\' at \'{}\''
				, self.file_name
				, path
				, log_level=2
			)
		except Exception as exception:
			logger.result(
				'Could not save file {}: {}'
				, path
				, exception
				, log_level=2
			)
			exit()