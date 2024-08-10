import cv2
from pathlib import Path

from config.ConfigLoader import SETTINGS

class Resource:
    def __init__(self,
        path=None,
        priority=None,
        threshold=None,
        ignore=None
    ):
        self.path = Path(path)

        gray_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        self.width, self.height = gray_image.shape[::-1]
        self.template = gray_image

        self.priority = priority
        self.ignore = ignore

        self.threshold = threshold or (
            SETTINGS.get('default_ignore_threshold') if ignore
            else SETTINGS.get('default_matching_threshold')
        )

    def __str__(self):
        if self.ignore:
            return f'Resource(path={self.path.name}, priority={self.priority}, threshold={self.threshold}, ignore={self.ignore})'
        else:
            return f'Resource(path={self.path.name}, w={self.width}, h={self.height}, threshold={self.threshold}, priority={self.priority})'