from bs4 import BeautifulSoup
import requests
from sys import exit

from .Icon import Icon
from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from core.image_processing.ImageProcessorPerk import ImageProcessorPerk
from utils.enums import ADDON_TYPE, ICON_TYPE, PERK_TYPE
from utils.functions import set_text_to_pascal_case
from utils.logger import logger

class ContentDownloader:
	content_url = 'https://deadbydaylight.fandom.com/wiki/{}'

	def __init__(self, content_name):
		self.content_name = set_text_to_pascal_case(content_name, separator=' ')

		logger.init(
			'download'
			, 'Processing download for \'{}\''
			, self.content_name
		)

		self.soup = self._get_source_html()
		self.is_killer = False

	def download(self):
		logger.supress('image')

		perks, addons = self.search_icons()

		logger.action(
			'Downloading perks ({})'
			, len(perks)
			, breakline=True
		)

		for icon in perks:
			self._download_perk(icon)

		logger.action(
			'Downloading addons ({})'
			, len(addons)
			, breakline=True
		)

		for icon in addons:
			self._download_addons(icon)

		logger.result(
			'Downloads concluded successfully.'
			, breakline=True
		)

	def search_icons(self):
		logger.action('Capturing icons:')

		perks_list = []
		addons_list = []

		try:
			perks_list = self._search_perks()
		except Exception as exception:
			logger.result(
				'Could not capture the expected 3 perks for \'{}\': {}'
				, self.content_name
				, exception
				, log_level=2
			)
			exit()

		(is_killer, addon_icons, exception) = self._search_addons()
		if exception is not None:
			logger.result(
				'Could not capture the expected 20 addons for the killer \'{}\': {}'
				, self.content_name
				, exception
				, log_level=2
			)
			exit()

		if addon_icons:
			addons_list = addon_icons

		self.is_killer = is_killer

		logger.action(
			'['
			, log_level=2
		)

		logger.detail(
			'{}'
			, '\n\t\t\t'.join([
				str(icon)
				for icon in (perks_list + addons_list)
			])
			, log_level=3
		)

		logger.action(
			']'
			, log_level=2
		)

		return (perks_list, addons_list)

	def _get_source_html(self):
		url = self.content_url.format(self.content_name)

		try:
			response = requests.get(url)
			response.raise_for_status()

			return BeautifulSoup(response.text, 'lxml')
		except Exception as exception:
			logger.result(
				'Could not get URL {}: {}'
				, url
				, exception
				, log_level=2
			)
			exit()

	def _search_perks(self):
		span = self.soup.find('span', {'id': 'Unique_Perks'})
		return self._search_icons_from_section(span, type=ICON_TYPE.PERK.value)

	def _search_addons(self):
		span = None
		icons = []
		exception = None

		try:
			span = self.soup.find(
				'span',
				id=lambda id: id and id.startswith('Add-ons_for_')
			)
			icons = self._search_icons_from_section(span, type=ICON_TYPE.ADDON.value)
		except Exception as _exception:
			exception = _exception
		finally:
			is_killer = span is not None
			exception = exception if is_killer else None
			return (is_killer, icons, exception)

	def _search_icons_from_section(self, section, type):
		table = section.find_next('table')
		icons = table.select('tr > th:first-of-type div:last-of-type a img.lazyload')
		return [ Icon(icon, type) for icon in icons ]

	def _download_perk(self, icon):
		path_resource_icon_base = ImageProcessorPerk(
			PERK_TYPE.KILLER.value
			if self.is_killer
			else PERK_TYPE.SURVIVOR.value
		).path_resource_icon_base

		icon.save_in_local_path(path_resource_icon_base)

	def _download_addons(self, icon):
		content_name = self._sanitize_name()

		path_resource_icon_base = ImageProcessorAddon(
			ADDON_TYPE.KILLER.value
		).path_resource_icon_base

		killer_path = path_resource_icon_base.joinpath(content_name)

		icon.save_in_local_path(killer_path)

	def _sanitize_name(self):
		content_name = self.content_name.lower()

		if content_name[0:4] == 'the ':
			content_name = content_name[4:]

		content_name = content_name.replace(' ', '_')

		return content_name