from .ImageMatcher import ImageMatcher
from utils.CoordinateController import CoordinateController
from utils.enums import REGION_BLOODWEB, REGION_LEVEL
from utils.functions import create_directory
from utils.logger import logger

class BloodwebHandler:
	def __init__(self):
		self.region_bloodweb = CoordinateController(REGION_BLOODWEB)
		self.region_bloodweb.set_action_rectangle(
			x=260,
			y=160,
			width=850,
			height=780
		)

		self.region_level = CoordinateController(REGION_LEVEL)
		self.region_level.set_action_rectangle(
			x=380,
			y=70,
			width=300,
			height=40
		)

	def grind_once(self, iteration):
		result_directory = create_directory(
			logger.get_result_folder(),
			iteration
		)

		(screenshot_path, screenshot) = self.region_bloodweb.take_screenshot(result_directory)

		matched_bloodweb_nodes = ImageMatcher(
			image_source=screenshot_path,
			result_directory=result_directory
		).match_with_all_resources_v2()








	def grind(self):
		iteration = 0

		while True:
			iteration += 1

			self.grind_once(iteration)

			return