from core.image_processing.ImageProcessorAddon import ImageProcessorAddon
from core.image_processing.ImageProcessorItem import ImageProcessorItem
from core.image_processing.ImageProcessorOffering import ImageProcessorOffering
from core.image_processing.ImageProcessorPerk import ImageProcessorPerk

from utils.enums import OFFERING_TYPE, PERK_TYPE, ADDON_TYPE

if __name__ == '__main__':
	ImageProcessorOffering(OFFERING_TYPE.ALL).process_all_images()
	ImageProcessorOffering(OFFERING_TYPE.SURVIVOR).process_all_images()
	ImageProcessorOffering(OFFERING_TYPE.KILLER).process_all_images()
	ImageProcessorItem().process_all_images()
	ImageProcessorAddon(ADDON_TYPE.SURVIVOR).process_all_images()
	ImageProcessorAddon(ADDON_TYPE.KILLER).process_all_images()
	ImageProcessorPerk(PERK_TYPE.SURVIVOR).process_all_images()
	ImageProcessorPerk(PERK_TYPE.KILLER).process_all_images()
