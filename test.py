total_grind_until_read_bloodweb_level = 0
levels_to_skip = 0


def set(lvl):
    global total_grind_until_read_bloodweb_level
    global levels_to_skip

    print(f'\t\t- Taking screenshot, seeing level: \'{lvl}\'')

    current_level = lvl

    total_grind_until_read_bloodweb_level = 0
    levels_to_skip = 0

    if current_level >= 12:
        total_grind_until_read_bloodweb_level = 49 - current_level
    elif current_level == 11:
        levels_to_skip = 1
        total_grind_until_read_bloodweb_level = 0
    elif current_level <= 10:
        levels_to_skip = 10 - current_level
        total_grind_until_read_bloodweb_level = levels_to_skip - 1


def check(lvl):
    global total_grind_until_read_bloodweb_level
    global levels_to_skip

    if total_grind_until_read_bloodweb_level <= 0:
        set(lvl)
    else:
        levels_to_skip -= 1
        total_grind_until_read_bloodweb_level -= 1


def click_center(lvl, skipping=False):
    global total_grind_until_read_bloodweb_level
    global levels_to_skip

    if skipping:
        print(f'\t\t - Skipping level \'{lvl}\': [skip = {levels_to_skip}]')
    else:
        print(f'\t\t - Clicking on center at level \'{lvl}\': [grind = {total_grind_until_read_bloodweb_level}, skip = {levels_to_skip}]')
    print(f'\t\t\t - Sleeping 4.5s')

    check(((lvl + 1) - 1) % 50 + 1)


def main():
    global total_grind_until_read_bloodweb_level
    global levels_to_skip

    print('Opened application:')


    ini = 11
    set(ini)

    count = ini - 1
    end = 0
    while True:
        count += 1
        if count > 70:
            return

        lvl = (count - 1) % 50 + 1
        print(f'\tSeeing level \'{lvl}\'')


        if levels_to_skip > 0:
            click_center(lvl, skipping=True)
            continue

        click_center(lvl)


main()