import cv2
import numpy
import threading

from .Match import Match
from utils.enums import MATCH

class ImageMatcher:
	resources = None

	@classmethod
	def set_resources(cls, resources):
		cls.resources = resources

	def __init__(self, image_source, result_directory):
		self.image_source = cv2.imread(image_source)
		self.grayed_image_source = cv2.cvtColor(self.image_source, cv2.COLOR_BGR2GRAY)

		self.image_mask_against_duplicates = numpy.zeros(
			self.grayed_image_source.shape[:2],
			numpy.uint8
		)

		self.result_directory = result_directory

	def match_with_resource(self, resource, matched_locations, lock):
		width, height = resource.width, resource.height

		match_result = cv2.matchTemplate(
			self.grayed_image_source,
			resource.grayed_image,
			cv2.TM_CCOEFF_NORMED
		)

		threshold = resource.threshold
		location = numpy.where(match_result >= threshold)

		local_matched_locations = []
		for (x1, y1) in zip(*location[::-1]):
			if self.image_mask_against_duplicates[
				y1 + int(round(height / 2)),
				x1 + int(round(width / 2))
			] == 255:
				continue

			x2, y2 = x1 + width, y1 + height

			with lock:
				self.image_mask_against_duplicates[
					y1:y2,
					x1:x2
				] = 255

			local_matched_locations.append(
				Match(
					resource=resource,
					x1=x1, y1=y1,
					x2=x2, y2=y2,
					match_threshold=match_result[y1, x1],
					ignore=resource.ignore,
					image_source=self.image_source
				)
			)

		with lock:
			matched_locations.extend(local_matched_locations)

	def match_with_all_resources(self):
		matched_locations = []

		lock = threading.Lock()
		threads = []

		for resource in self.resources:
			thread = threading.Thread(
				target=self.match_with_resource,
				args=(resource, matched_locations, lock)
			)
			threads.append(thread)
			thread.start()

		for thread in threads:
			thread.join()

		matched_locations_no_ignore = []
		for match in matched_locations:
			match.log()
			match.paint()

			if not match.ignore:
				matched_locations_no_ignore.append(match)

		cv2.imwrite(self.result_directory + MATCH.FILENAME.value, self.image_source)

		return matched_locations_no_ignore


