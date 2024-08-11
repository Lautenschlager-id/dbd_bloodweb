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

	def take_screenshot(self, save_directory=None):
		logger.log(f'Taking screenshot: {self.name}')

		save_directory = (
			save_directory + self.filename
			if self.filename is not None
			else None
		)

		return take_screenshot(
			region=self.get_rectangle_as_region(),
			save_path=save_directory
		)