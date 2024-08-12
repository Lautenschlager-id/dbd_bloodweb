import math
import pyautogui
import pytesseract
import re
from time import sleep

from .ImageMatcher import ImageMatcher
from config.ConfigLoaderSettings import SETTINGS
from utils.CoordinateController import CoordinateController
from utils.enums import GRIND_STRATEGY, REGION_BLOODWEB, REGION_LEVEL
from utils.functions import create_directory
from utils.logger import logger

class BloodwebHandler:
	_initialized = False

	has_bloodweb_level_controller = None
	RE_BLOODWEB_LEVEL = re.compile(r'BLOODWEB LEVEL (\d+)', re.IGNORECASE)

	strategy_lambda = None

	average_distance_between_two_nodes = None

	maximum_prestiges = -1

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

	@classmethod
	def initialize(cls):
		cls.grind_strategy[GRIND_STRATEGY.DEFAULT.value] = (
			cls.grind_strategy[GRIND_STRATEGY.PRIORITY_THEN_CLOSER_TO_CENTER.value]
		)
		cls.strategy_lambda = cls.grind_strategy[SETTINGS.get('grind_strategy')]

		cls.average_distance_between_two_nodes = math.sqrt( 2 * ((85 // 2) ** 2) )

		if SETTINGS.get('use_bloodweb_level_controller') is False:
			pass_fn = lambda *_: None
			cls.get_bloodweb_level = pass_fn
			cls._check_bloodweb_level_metadata = pass_fn
			cls._set_bloodweb_level_metadata = pass_fn

	@classmethod
	def set_maximum_prestiges(cls, maximum_prestiges):
		logger.log(f'Set maximum prestiges on this run to \'{maximum_prestiges}\'')
		cls.maximum_prestiges = maximum_prestiges

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

		self.captured_bloodweb_level = None
		# Current level included; Used for levels [1,11]\{10}
		self.skip_x_bloodweb_levels = 0
		# Current level is not included; Used for level transitions 9>10, 10>11, 11>12, 49>50, 50>1
		self.get_bloodweb_level_after_x_levels = 0

	def grind_once(self, iteration):
		logger.log(
			'\n[bloodweb] Grinding on iteration <%s>'
			, iteration
		)

		result_directory = create_directory(
			logger.get_result_folder(),
			f'{iteration:03d}'
		)

		(screenshot_path, _) = self.region_bloodweb.take_screenshot(result_directory)

		matched_bloodweb_nodes = ImageMatcher(
			image_source=screenshot_path,
			result_directory=result_directory
		).match_with_all_resources()

		if self.skip_x_bloodweb_levels > 0:
			self.click_next_bloodweb(skip=True)
			return

		self._set_node_locations(matched_bloodweb_nodes)

		self.click_all_nodes()

	def grind(self):
		logger.log('\n[bloodweb] Initializing grinding system')

		iteration = 0

		# set strategy based on initial level
		self.get_bloodweb_level()

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
			self.region_bloodweb.get_distance_from_center(click_x, click_y)
			/ self.average_distance_between_two_nodes
		) * 0.500

		# gives enough time for the animations to end
		sleep(delay_until_next_node)

	def click_next_bloodweb(self, skip=False, level_up=False):
		logger.log(
			'\t=> Leveling up to the next prestige level'
			if level_up else
			f'\t=> {"Skipping" if skip else "Moving"} to the next bloodweb'
		)

		(center_x, center_y) = self.region_bloodweb.get_center_as_region()

		self._click(center_x, center_y)

		if self.captured_bloodweb_level == 50:
			if level_up is False:
				sleep(3.5)
				# clicks twice in the center, one to grind, one to level_up
				self.click_next_bloodweb(level_up=True)
				return

			else:
				self.maximum_prestiges -= 1
				if self.maximum_prestiges == 0:
					logger.log('\nSystem has hit the set maximum prestiges.')
					exit()

		sleep(4.5)
		self._check_bloodweb_level_metadata()

	def get_bloodweb_level(self):
		logger.log('\n[bloodweb] Capturing bloodweb level:')

		captured = False
		while not captured:
			try:
				(_, screenshot) = self.region_level.take_screenshot()
				captured_text = pytesseract.image_to_string(screenshot)
				captured_level = int(self.RE_BLOODWEB_LEVEL.search(captured_text).group(1))

				captured = True
			except:
				# if any error ocurred, especially on captured_level, then try again
				sleep(0.500)

		logger.log(
			'\t=> Identified current level: %s'
			, captured_level
		)

		self.captured_bloodweb_level = captured_level
		self._set_bloodweb_level_metadata()

	def _set_node_locations(self, nodes):
		nodes.sort(key=lambda match:
			BloodwebHandler.strategy_lambda(
				match,
				self.region_bloodweb.get_distance_from_center
			)
		)
		self.nodes = nodes

	def _click(self, x, y):
		return
		# sometimes the bloodweb doesn't handle the click, thus clicking thrice to guarantee
		for _ in range(3):
			pyautogui.mouseDown(x, y)
			sleep(0.400)
			pyautogui.mouseUp()

		# unselect anything that might be selected in the bloodweb (popups)
		pyautogui.moveTo(self.region_bloodweb.x, self.region_bloodweb.y)
		pyautogui.click()

	def _check_bloodweb_level_metadata(self):
		if self.get_bloodweb_level_after_x_levels <= 0:
			self.get_bloodweb_level()
		else:
			self.skip_x_bloodweb_levels -= 1
			self.get_bloodweb_level_after_x_levels -= 1

	def _set_bloodweb_level_metadata(self):
		captured_bloodweb_level = self.captured_bloodweb_level

		self.get_bloodweb_level_after_x_levels = 0
		self.skip_x_bloodweb_levels = 0

		if captured_bloodweb_level >= 12:
			# covers level transition: 49>50

			# checks that after grinding lvl 49, the next lvl is 50
			# lvl 50 requires clicking the center twice (grind -> level up)
			self.get_bloodweb_level_after_x_levels = 49 - captured_bloodweb_level

		elif captured_bloodweb_level == 11:
			# covers level grinding: 11
			# covers level transition: 11>12

			# skips lvl 11 (no entity)
			self.skip_x_bloodweb_levels = 1
			# checks that after grinding lvl 11, the next lvl is 12
			self.get_bloodweb_level_after_x_levels = 0

		elif captured_bloodweb_level <= 10:
			# covers level grinding: 1, 2, 3, 4, 5, 6, 7, 8, 9
			# covers level transitions: 1>2, 2>3, 3>4, 4>5, 5>6, 6>7, 7>8, 8>9, 9>10

			# skips lvl 1, 2, 3, 4, 5, 6, 7, 8, 9 (no entity)
			# zeroes out on lvl 10, so it grinds correctly
			self.skip_x_bloodweb_levels = 10 - captured_bloodweb_level
			# checks that after grinding lvl 9, the next lvl is 10
			self.get_bloodweb_level_after_x_levels = self.skip_x_bloodweb_levels - 1 # (10-9)=1-1=0

		if self.skip_x_bloodweb_levels > 0:
			logger.log(
				'\t=> Skipping the next <%s> levels'
				, self.skip_x_bloodweb_levels
			)

		logger.log(
			'\t=> Bloodweb level will be captured again after <%s> levels'
			, self.get_bloodweb_level_after_x_levels
		)