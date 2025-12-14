from math import floor

from config.ConfigLoaderSettings import SETTINGS

class ResolutionAdapter:
    DEFAULT_SCREEN_WIDTH = 1920

    @staticmethod
    def get_width(number):
        width_scale_factor = SETTINGS.get('screen_width') / ResolutionAdapter.DEFAULT_SCREEN_WIDTH
        return floor(number * width_scale_factor)