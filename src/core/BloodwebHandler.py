import math
import pyautogui
from time import sleep

from .ImageMatcher import ImageMatcher
from config.ConfigLoader import SETTINGS
from utils.CoordinateController import CoordinateController
from utils.enums import GRIND_STRATEGY, REGION_BLOODWEB, REGION_LEVEL
from utils.functions import create_directory
from utils.logger import logger

class BloodwebHandler:
	_initialized = False

	grind_strategy = {
		GRIND_STRATEGY.PRIORITY_THEN_CLOSER_TO_CENTER.value: lambda match, distance_fn: (
			-match.resource.priority,
			-distance_fn(match.center_x, match.center_y)
		),
		GRIND_STRATEGY.PRIORITY_THEN_FURTHER_TO_CENTER.value: lambda match, distance_fn: (
			-match.resource.priority,
			distance_fn(match.center_x, match.center_y)
		),
		GRIND_STRATEGY.DISTANCE_CLOSER.value: lambda match, distance_fn: (
			-distance_fn(match.center_x, match.center_y)
		),
		GRIND_STRATEGY.DISTANCE_FURTHER.value: lambda match, distance_fn: (
			distance_fn(match.center_x, match.center_y)
		),
		GRIND_STRATEGY.PRIORITY.value: lambda match, distance_fn: (
			-match.resource.priority
		)
	}

	strategy_lambda = None

	average_distance_between_two_nodes = None

	@classmethod
	def initialize(cls):
		cls.grind_strategy[GRIND_STRATEGY.DEFAULT.value] = (
			cls.grind_strategy[GRIND_STRATEGY.PRIORITY_THEN_CLOSER_TO_CENTER.value]
		)
		cls.strategy_lambda = cls.grind_strategy[SETTINGS.get('grind_strategy')]

		cls.average_distance_between_two_nodes = math.sqrt( 2 * ((85 // 2) ** 2) )

	def __new__(cls, *args, **kwargs):
		if cls._initialized is False:
			cls._initialized = True
			cls.initialize()
		return super().__new__(cls)

	def __init__(self):
		self.nodes = None

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
		).match_with_all_resources()

		self._set_node_locations(matched_bloodweb_nodes)

		self.click_all_nodes()

	def grind(self):
		iteration = 0

		while True:
			iteration += 1

			self.grind_once(iteration)

	def click_all_nodes(self):
		logger.log('\n')
		logger.log('Grinding: ')

		while self.nodes:
			self.click_next_node()

		self.click_next_bloodweb()

	def click_next_node(self):
		if not self.nodes:
			return

		node = self.nodes.pop()

		(click_x, click_y) = self.region_bloodweb.get_absolute_coordinate(
			node.center_x,
			node.center_y
		)

		logger.log(f'\tClicking \'{node.resource.path.name}\' ({click_x}, {click_y})')
		self._click(click_x, click_y)

		delay_until_next_node = (
			self.region_bloodweb.get_distance_from_center(
				node.center_x,
				node.center_y
			) / self.average_distance_between_two_nodes
		) * 0.500

		# gives enough time for the animations to end
		sleep(delay_until_next_node)

	def click_next_bloodweb(self):
		logger.log(f'\t=> Moving to the next bloodweb')

		(center_x, center_y) = self.region_bloodweb.get_center_as_region()

		self._click(center_x, center_y)

		sleep(4.5)

	def _set_node_locations(self, nodes):
		nodes.sort(key=lambda match:
			BloodwebHandler.strategy_lambda(
				match,
				self.region_bloodweb.get_distance_from_center
			)
		)
		self.nodes = nodes

	def _click(self, x, y):
		# sometimes the bloodweb doesn't handle the click, thus clicking thrice to guarantee
		for _ in range(3):
			pyautogui.mouseDown(x, y)
			sleep(0.400)
			pyautogui.mouseUp()

		# unselect anything that might be selected in the bloodweb (popups)
		pyautogui.moveTo(self.region_bloodweb.x, self.region_bloodweb.y)
		pyautogui.click()