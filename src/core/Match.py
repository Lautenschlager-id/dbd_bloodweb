import cv2

from config.ConfigLoaderSettings import SETTINGS
from utils.enums import PAINT
from utils.logger import logger

class Match:
	def __init__(self,
		resource,
		x1, y1,
		x2, y2,
		match_threshold,
		ignore,
		image_source
	):
		self.resource = resource

		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2

		self.center_x = (x1 + x2) / 2
		self.center_y = (y1 + y2) / 2

		self.match_threshold = match_threshold
		self.ignore = ignore
		self.image_source = image_source

	def log(self):
		position = f'at [({self.x1}, {self.y1}), ({self.x2}, {self.y2})]'

		if not self.ignore:
			logger.log(
				f'\tFound \'{self.resource.path.name}\' '
				f'with threshold [{self.match_threshold:.5f}] '
				+ position
			)
		elif SETTINGS.get('log_ignored_matches'):
			logger.log(
				f'\tIgnored \'{self.resource.path.name}\' '
				+ position
			)

	def paint(self):
		cv2.rectangle(
			self.image_source,
			(self.x1, self.y1),
			(self.x2, self.y2),
			(
				PAINT.RED.value
				if self.ignore
				else PAINT.GREEN.value
			),
			PAINT.THICKNESS.value
		)