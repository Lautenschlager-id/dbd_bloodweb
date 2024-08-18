import math

from .functions import take_screenshot
from .logger import logger

class CoordinateController:
	def __init__(self, region_enum):
		self.name = region_enum.NAME.value
		self.filename = region_enum.FILENAME.value

		self.x = None
		self.y = None
		self.width = None
		self.height = None

		self.center_x = None
		self.center_y = None

	def set_action_rectangle(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.center_x = x + width / 2
		self.center_y = y + height / 2

	def get_rectangle_as_region(self):
		return (
			self.x,
			self.y,
			self.width,
			self.height
		)

	def get_center_as_region(self):
		return (
			self.center_x,
			self.center_y
		)

	def get_distance_from_center(self, x, y):
		return math.sqrt(
			(self.center_x - x) ** 2
			+ (self.center_y - y) ** 2
		)

	def get_absolute_coordinate(self, x, y):
		return (
			self.x + x,
			self.y + y
		)

	def get_distance_from_center_with_absolute_coordinates(self, x, y):
		(x, y) = self.get_absolute_coordinate(x, y)
		return self.get_distance_from_center(x, y)

	def take_screenshot(self, save_directory=None, log_level=1):
		logger.action(
			'Taking screenshot of \'{}\''
			, self.name
			, log_level=log_level
		)

		save_directory = (
			save_directory + self.filename
			if self.filename is not None
			else None
		)

		return take_screenshot(
			region=self.get_rectangle_as_region(),
			save_path=save_directory
		)