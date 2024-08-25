import cv2
from pathlib import Path

from config.ConfigLoaderSettings import SETTINGS

class Resource:
    def __init__(self,
        path=None,
        priority=None,
        threshold=None,
        skip=None
    ):
        self.path = Path(path)

        grayed_image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

        self.width, self.height = grayed_image.shape[::-1]
        self.grayed_image = grayed_image

        self.priority = priority
        self.skip = skip

        self.threshold = threshold or (
            SETTINGS.get('default_match_and_skip_threshold') if skip
            else SETTINGS.get('default_match_and_grind_threshold')
        )

    def __str__(self):
        if self.skip:
            return f'Resource(path={self.path.name}, priority={self.priority}, threshold={self.threshold}, skip={self.skip})'
        else:
            return f'Resource(path={self.path.name}, width={self.width}, height={self.height}, threshold={self.threshold}, priority={self.priority})'