from pathlib import Path
import re
import subprocess
import os
import cv2
import numpy
import pyautogui
from time import sleep
import math
import fnmatch
import datetime
import logging
import unicodedata
import pytesseract

logger = logging.getLogger()

def setup_logger(folder):
    log_file = 'logs.txt'
    logging.basicConfig(
        filename=folder + log_file,
        level=logging.INFO,
        format="%(asctime)s: %(message)s"
    )
    logging.getLogger().addHandler(logging.StreamHandler())


class TransformImage:
    re_template = re.compile(r'template_(\d)')


    def get_template_id(self, path):
        # [1-6]
        return TransformImage.re_template.search(str(path)).group(1)


    def get_bg_template(self, id):
        return str(self.path_bg_template.joinpath(f'{id}.png'))


    def get_additional_template(self, id):
        return str(self.path_additional_template.joinpath(f'{id}.png'))


    def get_template_by_path(self, path):
        return self.get_bg_template(self.get_template_id(path))


    def get_additional_template_by_path(self, path):
        return self.get_additional_template(self.get_template_id(path))


    def init_processed_path(self, path):
        output_dir = str(path.parent).replace('\\originals\\', '\\processed\\')
        os.makedirs(output_dir, exist_ok=True)

        output_path = str(path).replace('\\originals\\', '\\processed\\').replace('.webp', '.png')
        return output_path


    def process_image(self, path, custom_output_template_id=None):
        custom_path = None
        if custom_output_template_id is not None:
            custom_path = Path(TransformImage.re_template.sub(f'template_{custom_output_template_id}', str(path)))
        process_path = custom_path or path

        output_path = self.init_processed_path(process_path)

        magick_commands = [
            self.set_webp_icon_to_png(path)
        ]

        if getattr(self, 'hide_bg', None) is None:
            magick_commands.append(self.add_bg_template(process_path))

        magick_commands.append(self.resize_png())

        if getattr(self, 'hide_additional', None) is None:
            if getattr(self, 'path_additional_template', None) is not None:
                magick_commands.insert(3 if self.additional_resize_first else 2, self.add_additional_template(process_path))

        magick_commands = ' | '.join(magick_commands)
        magick_commands += self.send_data_to_path(output_path)

        subprocess.call(magick_commands, shell=True)


    def set_webp_icon_to_png(self, path):
        magick_command = f'magick {str(path)} png:-'
        return magick_command


    def add_bg_template(self, path):
        bg_template = self.get_template_by_path(path)
        magick_command = f'magick composite -gravity center - {bg_template} png:-'
        return magick_command


    def resize_png(self):
        magick_command = f'magick - -resize {self.icon_width}x png:-'
        return magick_command


    def add_additional_template(self, path):
        additional_template = self.get_additional_template_by_path(path)
        magick_command = f'magick composite -gravity {self.additional_position} -geometry {self.additional_offset}{self.additional_offset} {additional_template} - png:-'
        return magick_command


    def send_data_to_path(self, output_path):
        command = f' > {output_path}'
        return command


    def process_all_images(self):
        if getattr(self, 'reuse_resource_for_all_templates', None) == True:
            custom_template_id_list = []
            for file in self.path_bg_template.glob('*.png'):
                custom_template_id_list.append(file.name[:-4])

        else:
            custom_template_id_list = [None]

        for file in self.icon_path.rglob('*.webp'):
            if file.is_file():
                logger.info(f'Processing image {file}')
                for template_id in custom_template_id_list:
                    self.process_image(file, custom_output_template_id=template_id)


class TransformOffering(TransformImage):
    def __init__(self, type):
        self.path_bg_template = Path('./images/templates/offerings')
        self.icon_path = Path('./images/originals/offerings/').joinpath(type)
        self.icon_width = 70

        #self.hide_bg = True
        #self.hide_additional = True


class TransformPerk(TransformImage):
    def __init__(self, type):
        self.path_bg_template = Path('./images/templates/perks')
        self.path_additional_template = Path('./images/templates/perks/additional')
        self.icon_path = Path('./images/originals/perks/').joinpath(type).joinpath('template_1')
        self.icon_width = 70
        self.additional_position = 'center'
        self.additional_offset = '+0'
        self.additional_resize_first = False
        self.reuse_resource_for_all_templates=True

        #self.hide_bg = True
        #self.hide_additional = True


class TransformItem(TransformImage):
    def __init__(self):
        self.path_bg_template = Path('./images/templates/items')
        self.icon_path = Path('./images/originals/items/survivors')
        self.icon_width = 55

        #self.hide_bg = True
        #self.hide_additional = True


class TransformAddon(TransformImage):
    def __init__(self, type, killer_name=None):
        self.path_bg_template = Path('./images/templates/items')
        self.path_additional_template = Path('./images/templates/addons/additional')

        self.icon_path = Path('./images/originals/addons').joinpath(type)
        if killer_name is not None:
            self.icon_path = self.icon_path.joinpath(killer_name)

        self.icon_width = 58
        self.additional_position = 'northeast'
        self.additional_offset = '-5'
        self.additional_resize_first = True

        #self.hide_bg = True
        #self.hide_additional = True


    def get_additional_template_by_path(self, path):
        return str(self.path_additional_template.joinpath('small.png'))


class CoordinateOffset:
    def __init__(self, name):
        self.name = name
        self.region_x = None
        self.region_y = None
        self.region_width = None
        self.region_height = None
        self.center_x = None
        self.center_y = None


    def set_region(self, x, y, width, height):
        self.region_x = x
        self.region_y = y
        self.region_width = width
        self.region_height = height


    def get_region(self):
        return (self.region_x, self.region_y, self.region_width, self.region_height)


    def set_center(self, x, y):
        self.center_x = x
        self.center_y = y


    def get_center(self):
        return (self.center_x, self.center_y)


    def normalize_xy1(self, x1, y1, increment=0):
        return (self.region_x + x1 + increment, self.region_y + y1 + increment)


    def calculate_distance_from_center(self, x, y):
        return math.sqrt( (self.center_x - x) ** 2 + (self.center_y - y) ** 2 )


    def get_region_screenshot(self):
        logger.info(f'Taking {self.name} screenshot')
        return pyautogui.screenshot(region=self.get_region())


class Template:
    def __init__(self, template=None, w=None, h=None, path=None,
        priority=None, ignore=None, raw_path=None, threshold=None):

        default_threshold = 0.75
        if ignore:
            # ignoring has to be more stricit
            default_threshold += 0.03

        self.template = template
        self.w = w
        self.h = h
        self.path = path
        self.priority = priority
        self.ignore = ignore
        self.raw_path = raw_path
        self.threshold = threshold or default_threshold


    def __str__(self):
        if self.ignore:
            return f'Template(path={self.path.name}, priority={self.priority}, threshold={self.threshold}, ignore={self.ignore})'
        else:
            return f'Template(path={self.path.name}, w={self.w}, h={self.h}, threshold={self.threshold}, priority={self.priority})'


class TextProcessor:
    template_by_color = {
        "brown": 1,
        "yellow": 2,
        "green": 3,
        "purple": 4,
        "red": 5,
        "orange": 6,
    }

    icon_type = {
        "addon": "IconAddon_",
        "item": "IconItems_",

        "offer": "IconFavors_",
        "offering": "IconFavors_",

        "perk": "IconPerks_",

        "map": "maps*IconFavors_",
        "realm": "maps*IconFavors_",
        "level": "maps*IconFavors_",
    }

    fnmatch_any_char = '[!:]'
    re_special_characters = re.compile(r'[\u0300-\u036f&@#]')

    re_input_text = re.compile(r'^\s*(?:(\S+?)\s+)?(\S+?)\s*:\s*(.+)$')

    def add_any_character_to_text(text):
        normalized_text = unicodedata.normalize('NFD', text)
        replaced_text = TextProcessor.re_special_characters.sub(
            TextProcessor.fnmatch_any_char,
            normalized_text)
        return replaced_text


    def text_to_camel_case(text):
        words = re.split(r'[\s_]+', text)
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


    def text_to_unix_file_name(text):
        # purple item: flashlight -> template_4*IconItems_*flashlight*
        # item: flashlight -> IconItems_*flashlight*
        content = TextProcessor.re_input_text.search(text.lower())
        if content is None:
            return text

        (color, type, description) = content.groups()

        type = TextProcessor.icon_type.get(type)
        if type is None:
            return text

        color = TextProcessor.template_by_color.get(color)
        color = '*' if color is None else f'template_{color}'

        description = TextProcessor.add_any_character_to_text(
            TextProcessor.text_to_camel_case(description)
        )

        return f'*{color}*{type}*{description}*'


    def check_paths_list(paths):
        for index in range(len(paths)):
            path = paths[index]

            is_list = isinstance(path, list)

            pattern = TextProcessor.text_to_unix_file_name(path[0] if is_list else path)

            if is_list:
                path[0] = pattern
            else:
                paths[index] = pattern

        return paths


class ImageResource:
    def get_result_path(result_folder):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')
        sub_folder = f'{result_folder}/{timestamp}/'

        os.makedirs(sub_folder, exist_ok=True)

        return sub_folder


    def process_bloodweb_screenshot(result_folder, screenshot, save=True):
        file = 'bloodweb.png'
        path = result_folder + file

        if save:
            screenshot.save(path)

        return path


    def get_template_paths(type, killer_name=None,
        disable_addons=False, disable_items=False,
        disable_offerings=False, disable_perks=False):

        is_survivor = type == 'survivors'

        template_paths = []

        if not disable_offerings:
            template_paths.append(Path('./images/processed/offerings/all'))
            template_paths.append(Path('./images/processed/offerings').joinpath(type))


        if not disable_items and is_survivor:
            template_paths.append(Path('./images/processed/items/survivors'))


        if not disable_perks:
            template_paths.append(Path('./images/processed/perks/').joinpath(type))


        if not disable_addons:
            if is_survivor:
                template_paths.append(Path('./images/processed/addons/survivors'))
            else:
                template_paths.append(Path('./images/processed/addons/killers/all'))
                template_paths.append(Path('./images/processed/addons/killers').joinpath(killer_name))

        return template_paths


    def populate_templates(ref_lists, pattern_list, priority=None, ignore=False):
        (ref_templates_list, ref_files, ref_identified_file) = ref_lists

        for index in range(len(pattern_list)):
            obj = pattern_list[index]

            pattern, threshold = None, None
            if isinstance(obj, list):
                pattern, threshold = obj
            else:
                pattern = obj

            pattern = f'*{pattern}*'

            matched_at_least_once = False
            for file in ref_files:
                if ref_identified_file.get(file) is None and fnmatch.fnmatch(file, pattern):
                    matched_at_least_once = True
                    ref_identified_file[file] = True

                    ref_templates_list.append(
                        Template(
                            raw_path=file,
                            priority=priority or index,
                            threshold=threshold,
                            ignore=ignore
                        )
                    )


            if not matched_at_least_once:
                logger.info(f'\t/!\\ Pattern \'{pattern}\' did not match any file')


    def filter_templates_by_list(template_paths, whitelist=None, blacklist=None):
        whitelist = whitelist and TextProcessor.check_paths_list(whitelist) or ['*']
        blacklist = blacklist and TextProcessor.check_paths_list(blacklist) or []

        templates = []

        files = [
            f'.\\{file}'
            for path in template_paths
                for file in path.rglob('*.png')
                    if file.is_file()
        ]

        identified_file = {}
        ImageResource.populate_templates((templates, files, identified_file), whitelist)
        ImageResource.populate_templates((templates, files, identified_file), blacklist, -1, True)

        for index in range(len(templates)):
            template = templates[index]
            path = Path(template.raw_path)

            gray_image = cv2.imread(template.raw_path, cv2.IMREAD_GRAYSCALE)
            w, h = gray_image.shape[::-1]

            template.template = gray_image
            template.w = w
            template.h = h
            template.path = path


        templates.sort(key=lambda template: template.priority)

        logger.info('\n')
        for template in templates:
            logger.info(f'\t{str(template)}')


        return templates


    def select_templates(type, killer_name=None,
        disable_addons=False, disable_items=False,
        disable_offerings=False, disable_perks=False,
        whitelist=None, blacklist=None):

        logger.info('Selecting templates:')

        template_paths = ImageResource.get_template_paths(type, killer_name,
            disable_addons, disable_items,
            disable_offerings, disable_perks)

        templates = ImageResource.filter_templates_by_list(template_paths, whitelist, blacklist)

        return templates


class Matcher:
    def match_template(self, result_folder, source_image, image_templates):
        logger.info('Matched templates:')

        image = cv2.imread(source_image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detected_positions = []
        mask_duplicate_rectangles = numpy.zeros(gray_image.shape[:2], numpy.uint8)

        for template in image_templates:
            width, height = template.w, template.h

            match_result = cv2.matchTemplate(gray_image, template.template, cv2.TM_CCOEFF_NORMED)

            threshold = template.threshold
            location = numpy.where(match_result >= threshold)

            for (x, y) in zip(*location[::-1]):
                if mask_duplicate_rectangles[
                    y + int(round(height / 2)),
                    x + int(round(width / 2))
                ] == 255:
                    continue

                x2, y2 = x + width, y + height

                mask_duplicate_rectangles[
                    y:y + height,
                    x:x + width
                ] = 255

                if not template.ignore:
                    detected_positions.append((x, y, x2, y2, template, match_result[y, x]))
                else:
                    # mark red
                    cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 2)


        for (x1, y1, x2, y2, template, matched_threshold) in detected_positions:
            logger.info(f'\tFound \'{template.path.name}\' with threshold [{matched_threshold:.5f}] at [{x1}, {y1}, {x2}, {y2}]')
            #mark green
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


        result_file = 'matched_result.png'
        cv2.imwrite(result_folder + result_file, image)

        #cv2.imshow('Matched Result', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return detected_positions


class Nodes:
    re_bloodlevel = re.compile(r'BLOODWEB LEVEL (\d+)', re.IGNORECASE)

    def __init__(self, nodes=None):
        self.nodes = nodes

        self.bloodweb_coordinate = CoordinateOffset('bloodweb')
        self.bloodweb_coordinate.set_region(x=230, y=160, width=920, height=800)
        self.bloodweb_coordinate.set_center(x=460, y=400)

        self.level_coordinate = CoordinateOffset('bloodweb_level')
        self.level_coordinate.set_region(x=380, y=70, width=300, height=40)

        self.avg_node_distance = math.sqrt( 2 * ((85 // 2) ** 2) )

        self.bloodweb_level = None
        self.levels_to_grind_until_check_bloodweb_level = 0
        self.levels_to_skip = 0


    def get_bloodweb_level(self):
        logger.info('\n')

        screenshot = self.level_coordinate.get_region_screenshot()
        text = pytesseract.image_to_string(screenshot)
        level = int(Nodes.re_bloodlevel.search(text).group(1))

        logger.info(f'\t=> Identified current bloodweb level: {level}')

        self.bloodweb_level = level
        self.set_total_grind_until_read_bloodweb_level()

        return level


    def set_total_grind_until_read_bloodweb_level(self):
        current_level = self.bloodweb_level

        self.total_grind_until_read_bloodweb_level = 0
        self.levels_to_skip = 0

        # in theory, reading more than once per run wouldn't be needed, but it's nice to keep the value updated

        # 1. Screenshot first run
        # 2. If level >= 12, click and only check again when it's level 1
        # 3. If level between 1 and 9, skip
        # 3.1. If level is 9, screenshot after click_center to check if it's 10
        # 4. If level is 10, click
        # 4.1. If level is 10, screenshot after click_center to check if it's 11
        # 5. If level is 11, skip
        # 5.1. If level is 9, screenshot after click_center to check if it's 12

        if current_level >= 12:
            self.total_grind_until_read_bloodweb_level = 50 - current_level

        elif current_level == 11:
            self.levels_to_skip = 1
            self.total_grind_until_read_bloodweb_level = 0

        elif current_level <= 10:
            self.levels_to_skip = 10 - current_level
            self.total_grind_until_read_bloodweb_level = self.levels_to_skip - 1


    def check_bloodweb_level(self):
        if self.total_grind_until_read_bloodweb_level <= 0:
            self.get_bloodweb_level()
            self.set_total_grind_until_read_bloodweb_level()
        else:
            self.levels_to_skip -= 1
            self.total_grind_until_read_bloodweb_level -= 1


    def set_nodes(self, nodes):
        self.nodes = nodes
        self.nodes.sort(key=lambda node: (
            -node[4].priority,
            -self.bloodweb_coordinate.calculate_distance_from_center(node[0], node[1])
        ))


    def click(self, x, y):
        for _ in range(3):
            pyautogui.mouseDown(x, y)
            sleep(0.4)
            pyautogui.mouseUp()

        pyautogui.moveTo(80, 80)
        pyautogui.click()


    def click_node(self):
        if not self.nodes:
            return

        node = self.nodes.pop()

        (x, y) = self.bloodweb_coordinate.normalize_xy1(node[0], node[1], 30)

        logger.info(f'\tClicking \'{node[4].path.name}\'')
        self.click(x, y)

        node_delay_between_clicks = 0 + (
            self.bloodweb_coordinate.calculate_distance_from_center(x, y) / self.avg_node_distance
        ) * 0.500

        sleep(node_delay_between_clicks)


    def click_all_nodes(self):
        logger.info('\n')
        logger.info('Grinding:')

        while self.nodes:
            self.click_node()

        self.click_center()


    def click_center(self, skipping=False):
        logger.info(f'\t=> {"Skipping" if skipping else "Moving"} to the next bloodweb')

        (x, y) = self.bloodweb_coordinate.get_center()
        (x, y) = self.bloodweb_coordinate.normalize_xy1(x, y)
        self.click(x, y)

        sleep(4.5)

        self.check_bloodweb_level()


def process_all_images():
    #TransformOffering("all").process_all_images()
    #TransformOffering("survivors").process_all_images()
    #TransformOffering("killers").process_all_images()
    #TransformItem().process_all_images()
    #TransformAddon("survivors").process_all_images()
    #TransformAddon("killers").process_all_images()
    #TransformPerk("survivors").process_all_images()
    #TransformPerk("killers").process_all_images()

    #TransformClass(param).process_image(Path('./images/originals/.../.webp'))
    pass


presets = {
    "survivors": {
        "whitelist": [
            'purple     item    :   flashlight',
            'green      item    :   flashlight',
            'yellow     item    :   flashlight',
            '           addon   :   styptic',
            'green      addon   :   battery',
            'yellow     addon   :   battery',
            'brown      addon   :   battery',
            'purple     item    :   medkit',
            'purple     item    :   toolbox',
            'green      item    :   toolbox',
            'red        addon   :   *',
            'green      item    :   medkit',
            'yellow     item    :   aid kit',
            '           offer   :   bloody party',
            '           offer   :   escape cake',
            '           offer   :   ward',
            '           addon   :   sapphire lens',
            '           addon   :   halogen',
            '           addon   :   socket swivels',
            '           map     :   jigsaw',
            '           map     :   shattered glasses',
            'yellow     addon   :   wire spool',
            '           addon   :   bandages',
            '           addon   :   cutting wire',
            'green      addon   :   hacksaw',
        ],
        "blacklist": [
            'brown      item    :   worn out tools',
            'brown      addon   :   power bulb',
            'brown      offer   :   *',
            'yellow     offer   :   *',
            '           addon   :   abdominal dressing',
        ]
    },
    "killers": {
        "nurse": {
            "whitelist": [
                'addon: ataxic respiration',
                'addon: catatonic boys treasure',
                'offer: bloody party',
                'offer: ward',
                'purple offer: oak',
            ]
        },
        "hag": {
            "whitelist": [
                'addon: rusty shackles',
                'map: marys letter',
                ['addon: scarred hand', 0.8],
                'addon: mint rag',
                'addon: swamp orchid necklet',
                'addon: cracked turtle egg',
                'addon: dried cicada',
                ['map: rpd badge', 0.6785],
                'offer: bloody party',
                'map: jigsaw'
                'purple offer: oak',
                'offer: ward',
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
            ]
        },
        "clown": {
            "whitelist": [
                'addon: cigar box',
                'red addon: redhead',
                'addon: flask of bleach',
                'purple addon: gin bottle',
                'offer: bloody party',
                'offer: ward',
                'purple offer: oak',
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
            ]
        },
        "shape": {
            "whitelist": [
                'red addon: tombstone',
                'red addon: tuft',
                'purple addon: scratched mirror',
                'map: marys letter',
                'map: shattered glasses',
                'purple addon: vanity mirror',
                'purple addon: tombstone piece',
                'green addon: memorial',
                'offer: bloody party',
                'green addon: jewellery box',
                'offer: ward',
                ['map: rpd badge', 0.6785],
                'map: jigsaw',
                'purple offer: oak',
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
            ]
        },
        "doctor": {
            "whitelist": [
                'purple addon: discipline',
                ['green addon: discipline', 0.88],
                'red addon: queen',
                'red addon: king',
                'offer: bloody party',
                'offer: ward',
                'purple offer: oak',
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
            ]
        },
        "huntress": {
            "whitelist": [
                'purple addon: glowing',
                'addon: wooden fox',
                'green addon: rose root',
                'red addon: head',
                'green addon: flower',
                'offer: bloody party',
                'map: marys letter',
                'offer: ward',
                ['map: rpd badge', 0.6785],
                'purple offer: oak',
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
            ]
        },
        "twins": {
            "whitelist": [
                'red addon: cloth',
                'addon: forest stew',
                'red addon: pendant',
                'addon: spinning top',
                'addon: perfume',
                'addon: rattle',
                'offer: bloody party',
                'map: jigsaw',
                'offer: ward',
                ['map: rpd badge', 0.672],
                'map: marys letter',
                ['purple offer: oak', 0.758],
            ],
            "blacklist": [
                'brown offer: *',
                'yellow offer: *',
                'offer: cut coin',
                'addon: tiny fingernail',
                'map: cookbook'
            ]
        },
    }
}


def main():
    main_result_folder = ImageResource.get_result_path('./results')
    setup_logger(main_result_folder)

    template_type = "killers"
    template_killer_name = "twins"

    preset = presets.get(template_type)
    if template_killer_name is not None:
        preset = preset.get(template_killer_name)

    templates_to_match = ImageResource.select_templates(
        template_type,
        killer_name=template_killer_name,
        whitelist=preset.get("whitelist"),
        blacklist=preset.get("blacklist")
    )

    node_handler = Nodes()
    matcher = Matcher()

    logger.info('\n')
    node_handler.get_bloodweb_level()

    while True:
        result_folder = ImageResource.get_result_path(main_result_folder)

        logger.info('\n')

        screenshot_path = ImageResource.process_bloodweb_screenshot(
            result_folder,
            node_handler.bloodweb_coordinate.get_region_screenshot(),
            save=True)

        if node_handler.levels_to_skip > 0:
            node_handler.click_center(skipping=True)
            continue

        nodes = matcher.match_template(
            result_folder,
            screenshot_path,
            templates_to_match)

        node_handler.set_nodes(nodes)
        node_handler.click_all_nodes()


if __name__ == "__main__":
    #process_all_images()
    main()
