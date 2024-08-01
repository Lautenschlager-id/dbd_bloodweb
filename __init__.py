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
import configparser
import sys

import drawing_utils
from menu import show_menu
from drawing_coords import run_cursor_overlay


config = configparser.ConfigParser()
config.read('config.ini')


item_size = config.getint('Settings', 'item_size')
offering_size = config.get('Settings', 'offering_size')
addon_size = config.get('Settings', 'addon_size')
perk_size = config.get('Settings', 'perk_size')

res_width = config.get('Resolution', 'res_width')
res_heigth = config.get('Resolution', 'res_heigth')

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


    def process_image(self, path):
        output_path = self.init_processed_path(path)

        magick_commands = [
            self.set_webp_icon_to_png(path)
        ]

        if getattr(self, 'hide_bg', None) is None:
            magick_commands.append(self.add_bg_template(path))

        magick_commands.append(self.resize_png(path))

        if getattr(self, 'hide_additional', None) is None:
            if getattr(self, 'path_additional_template', None) is not None:
                magick_commands.insert(3 if self.additional_resize_first else 2, self.add_additional_template(path))

        magick_commands = ' | '.join(magick_commands)

        # Replace the last "png:-" to the actual output_path
        magick_commands = re.sub(
            r'^(.+ )\S+:-(.*?)$',
            lambda r: f'{r.group(1)}{output_path}{r.group(2)}',
            magick_commands)

        subprocess.call(magick_commands, shell=True)


    def set_webp_icon_to_png(self, path):
        magick_command = f'magick {str(path)} png:-'
        return magick_command


    def add_bg_template(self, path):
        bg_template = self.get_template_by_path(path)
        magick_command = f'magick composite -gravity center - {bg_template} png:-'
        return magick_command


    def resize_png(self, path):
        magick_command = f'magick - -resize {self.icon_width}x png:-'
        return magick_command


    def add_additional_template(self, path):
        additional_template = self.get_additional_template_by_path(path)
        magick_command = f'magick composite -gravity {self.additional_position} -geometry {self.additional_offset}{self.additional_offset} {additional_template} - png:-'
        return magick_command


    def process_all_images(self):
        for file in self.icon_path.rglob('*.webp'):
            if file.is_file():
                logger.info(f'Processing image {file}')
                self.process_image(file)


class TransformOffering(TransformImage):
    def __init__(self, type):
        self.path_bg_template = Path('./images/templates/offerings')
        self.icon_path = Path('./images/originals/offerings/').joinpath(type)
        self.icon_width = offering_size

        #self.hide_bg = True
        #self.hide_additional = True


class TransformPerk(TransformImage):
    def __init__(self, type):
        self.path_bg_template = Path('./images/templates/perks')
        self.path_additional_template = Path('./images/templates/perks/additional')
        self.icon_path = Path('./images/originals/perks/').joinpath(type)
        self.icon_width = perk_size
        self.additional_position = 'center'
        self.additional_offset = '+0'
        self.additional_resize_first = False

        #self.hide_bg = True
        #self.hide_additional = True


class TransformItem(TransformImage):
    def __init__(self):
        self.path_bg_template = Path('./images/templates/items')
        self.icon_path = Path('./images/originals/items/survivors')
        self.icon_width = item_size

        #self.hide_bg = True
        #self.hide_additional = True


class TransformAddon(TransformImage):
    def __init__(self, type, killer_name=None):
        self.path_bg_template = Path('./images/templates/items')
        self.path_additional_template = Path('./images/templates/addons/additional')

        self.icon_path = Path('./images/originals/addons').joinpath(type)
        if killer_name is not None:
            self.icon_path = self.icon_path.joinpath(killer_name)

        self.icon_width = addon_size
        self.additional_position = 'northeast'
        self.additional_offset = '-5'
        self.additional_resize_first = True

        #self.hide_bg = True
        #self.hide_additional = True


    def get_additional_template_by_path(self, path):
        return str(self.path_additional_template.joinpath('small.png'))


class CoordinateOffset:
    def __init__(self):
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


class Template:
    def __init__(self, template=None, w=None, h=None, path=None,
        priority=None, ignore=None, raw_path=None):
        self.template = template
        self.w = w
        self.h = h
        self.path = path
        self.priority = priority
        self.ignore = ignore
        self.raw_path = raw_path


    def __str__(self):
        return f'Template(path={self.path.name}, w={self.w}, h={self.h}, priority={self.priority}, ignore={self.ignore})'


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
        return [TextProcessor.text_to_unix_file_name(path) for path in paths]


class ImageResource:
    def get_result_path(result_folder):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S.%f')
        sub_folder = f'{result_folder}/{timestamp}/'

        os.makedirs(sub_folder, exist_ok=True)

        return sub_folder


    def take_screenshot(result_folder, region=None, save=True):
        file = 'bloodweb.png'
        path = result_folder + file

        screenshot = pyautogui.screenshot(region=region)

        if save:
            screenshot.save(path)

        return path


    def select_templates(type, killer_name=None,
        disable_addons=False, disable_items=False,
        disable_offerings=False, disable_perks=False,
        whitelist=None, blacklist=None):

        logger.info('Selected templates:')

        is_survivor = type == 'survivors'

        directory_paths = []

        if not disable_offerings:
            directory_paths.append(Path('./images/processed/offerings/all'))
            directory_paths.append(Path('./images/processed/offerings').joinpath(type))


        if not disable_items and is_survivor:
            directory_paths.append(Path('./images/processed/items/survivors'))


        if not disable_perks:
            directory_paths.append(Path('./images/processed/perks/').joinpath(type))


        if not disable_addons:
            if is_survivor:
                directory_paths.append(Path('./images/processed/addons/survivors'))
            else:
                directory_paths.append(Path('./images/processed/addons/killers/all'))
                directory_paths.append(Path('./images/processed/addons/killers').joinpath(killer_name))


        whitelist = TextProcessor.check_paths_list(whitelist)
        blacklist = TextProcessor.check_paths_list(blacklist)

        templates = []

        for path in directory_paths:
            for file in path.rglob('*.png'):
                if file.is_file():
                    raw_path = f'.\\{file}'

                    priority = None

                    if whitelist is None:
                        priority = 1

                    else:
                        for index in range(len(whitelist)):
                            if fnmatch.fnmatch(raw_path, f'*{whitelist[index]}*'):
                                priority = index
                                break

                    if priority is not None:
                        templates.append(Template(raw_path=raw_path, priority=priority))

                    elif (
                        blacklist is None
                        or any(fnmatch.fnmatch(file, f'*{pattern}*') for pattern in blacklist)
                    ):
                        templates.append(Template(raw_path=raw_path, priority=-1, ignore=True))


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
        for template in templates:
            logger.info(f'\t{str(template)}')


        return templates


class Matcher:
    def match_template(self, result_folder, source_image, image_templates, threshold=0.75, debug=True):
        logger.info('Matched templates:')

        image = cv2.imread(source_image)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detected_positions = []
        mask_duplicate_rectangles = numpy.zeros(gray_image.shape[:2], numpy.uint8)

        for template in image_templates:
            width, height = template.w, template.h

            match_result = cv2.matchTemplate(gray_image, template.template, cv2.TM_CCOEFF_NORMED)

            _threshold = threshold
            if (template.ignore):
                # ignoring has to be more stricit
                _threshold = threshold + 0.03

            location = numpy.where(match_result >= _threshold)

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
                    detected_positions.append((x, y, x2, y2, template))
                elif debug:
                    # mark red
                    cv2.rectangle(image, (x, y), (x2, y2), (0, 0, 255), 2)


        for (x1, y1, x2, y2, template) in detected_positions:
            logger.info(f'\tFound \'{template.path.name}\' at [{x1}, {y1}, {x2}, {y2}]')
            #mark green
            if debug:
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)


        if debug:
            result_file = 'matched_result.png'
            cv2.imwrite(result_folder + result_file, image)

        #cv2.imshow('Matched Result', image)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        return detected_positions


class Nodes:
    def __init__(self, nodes=None):
        self.nodes = nodes

        self.coordinate_offset = CoordinateOffset()
        self.coordinate_offset.set_region(x=230, y=160, width=920, height=800)
        self.coordinate_offset.set_center(x=460, y=400)

        self.avg_node_distance = math.sqrt( 2 * ((85 // 2) ** 2) )


    def set_nodes(self, nodes):
        self.nodes = nodes
        self.nodes.sort(key=lambda node: (
            -node[4].priority,
            -self.coordinate_offset.calculate_distance_from_center(node[0], node[1])
        ))


    def click(self, x, y):
        for _ in range(3):
            pyautogui.mouseDown(x, y)
            sleep(0.4)
            pyautogui.mouseUp()

        pyautogui.moveTo(50, 50)


    def click_node(self):
        if not self.nodes:
            return

        node = self.nodes.pop()

        (x, y) = self.coordinate_offset.normalize_xy1(node[0], node[1], 30)

        logger.info(f'\tClicking \'{node[4].path.name}\'')
        self.click(x, y)

        node_delay_between_clicks = 1 + (
            self.coordinate_offset.calculate_distance_from_center(x, y) / self.avg_node_distance
        ) * 0.500

        sleep(node_delay_between_clicks)


    def click_all_nodes(self):
        logger.info('\n')
        logger.info('Grinding:')

        while self.nodes:
            self.click_node()

        self.click_center()


    def click_center(self):
        logger.info('\t=> Moving to next bloodweb')
        (x, y) = self.coordinate_offset.get_center()
        (x, y) = self.coordinate_offset.normalize_xy1(x, y)
        self.click(x, y)


def process_all_images():
    print("Processing images...")
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



def showBloodwebBoundries():
    while True:
        print("\n")
        print("=" * 40)
        print(" " * 12 + "Bloodweb" + " " * 12)
        print( "=" * 40)
        print("1. Draw Rectangle")
        print("2. Leave")
        print("\n")

        choice = input("Pick option (1 ou 2): ")

        if choice == "1":
            try:
                print("Rectangle coord:")
                print("\n")
                x1, y1 = map(int, input("Coord top Left (x1 y1): ").split())
                print("\n")
                x2, y2 = map(int, input("Coord bottom right (x2 y2): ").split())
                
                drawing_utils.draw_transparent_rectangle_on_screen((x1, y1), (x2, y2))
                
                
                
            except ValueError:
                print("Invalid entry..")
        
        elif choice == "2":
            print("Leaving...")
            break
        
        else:
            print("Try again.")
    print("Pressione Enter para fechar o retângulo e retornar ao menu.")

def main():
    main_result_folder = ImageResource.get_result_path('./results')
    setup_logger(main_result_folder)

    templates_to_match = ImageResource.select_templates("survivors", killer_name=None,
        whitelist=[
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
        blacklist=[
            'brown      item    :   worn out tools',
            'brown      addon   :   power bulb',
            'brown      offer   :   *',
            'yellow     offer   :   *',
            '           addon   :   abdominal dressing',
        ])

    node_handler = Nodes()
    matcher = Matcher()

    while True:
        result_folder = ImageResource.get_result_path(main_result_folder)

        logger.info('\n')

        screenshot_path = ImageResource.take_screenshot(
            result_folder,
            node_handler.coordinate_offset.get_region(),
            save=True)

        nodes = matcher.match_template(
            result_folder,
            screenshot_path,
            templates_to_match)

        node_handler.set_nodes(nodes)
        node_handler.click_all_nodes()

        sleep(5.5)
        
class MenuActions:
    def process_all_images(self):
        print("Processing all images...")
        process_all_images()

    def run(self):
        print("Running the application...")
        main()

    def bloodweb(self):
        print("Opening Bloodweb...")
        showBloodwebBoundries()

    def leave(self):
        print("Leaving...")
        sys.exit()  

    def getCoord(self):
        print("look at your mouse cursor")
        run_cursor_overlay()

    def perform_action(self, choice):
        if choice == '1':
            self.process_all_images()
        elif choice == '2':
            self.run()
        elif choice == '3':
            self.bloodweb()
        elif choice == '4':
            self.getCoord()
        elif choice == '5':
            self.leave()
        else:
            print("Invalid choice, please try again.")

            

def run():
    actions = MenuActions()

    while True:
        choice = show_menu()
        if choice == '5':
            actions.perform_action(choice)
            break
        actions.perform_action(choice)

if __name__ == "__main__":
    run()



