import curses
import random
import sys
import time

GREEN, RED, BLUE, YELLOW, WHITE, MAGENTA, GOLDEN = 1, 2, 3, 4, 5, 6, 7
NEEDLE_CHAR = "^"
TRUNK_CHAR = "#"
GIFT_CHAR = "[]"
USAGE = """
A simple Christmas and New Year card CLI program with animation. 

Options:
    -t <time>             Time in seconds between each tick. Default 0.15
    -m1 <message1>        Custom message for the top of the screen
    -m2 <message2>        Custom message for the bottom of the screen
    -f <from>             Signature for the bottom message
    -v <vertical_offset>  Vertical offset for the tree. Default 3
"""
TREE_HEIGHT = 10
TRUNK_WIDTH = 3
TRUNK_HEIGHT = 5
MESSAGE1 = "Merry Christmas & Happy New Year 2024!"
MESSAGE2 = "Best wishes,"
FROM = "Puffdayo"
VERTICAL_OFFSET = 3
LIGHTS_CHARS = "o*+"

lights = []


def draw_tree(stdscr, max_y, max_x):
    # Draw upper tree
    upper_tree_height = TREE_HEIGHT // 2
    for i in range(upper_tree_height):
        for j in range(-i, i + 1):
            stdscr.addch(max_y // 2 - TREE_HEIGHT - upper_tree_height + 3 + i + VERTICAL_OFFSET, max_x // 2 + j,
                         NEEDLE_CHAR,
                         curses.color_pair(GREEN))

    # Draw main tree body
    for i in range(TREE_HEIGHT):
        for j in range(-i, i + 1):
            stdscr.addch(max_y // 2 - TREE_HEIGHT + i + VERTICAL_OFFSET, max_x // 2 + j, NEEDLE_CHAR,
                         curses.color_pair(GREEN))

    # Draw trunk
    for i in range(TRUNK_HEIGHT):
        for j in range(TRUNK_WIDTH):
            stdscr.addch(max_y // 2 + 3 - TRUNK_HEIGHT + i + VERTICAL_OFFSET, max_x // 2 - TRUNK_WIDTH // 2 + j,
                         TRUNK_CHAR,
                         curses.color_pair(RED))


def initialize_lights(stdscr, max_y, max_x):
    global lights
    lights = []
    for i in range(TREE_HEIGHT):
        for j in range(-i, i + 1):
            if random.random() < 0.1:
                light_char = random.choice(LIGHTS_CHARS)
                color = random.choice([8, 9, 10])
                light = {'y': max_y // 2 - TREE_HEIGHT + i + VERTICAL_OFFSET,
                         'x': max_x // 2 + j,
                         'char': light_char,
                         'color': color,
                         'is_on': True}
                lights.append(light)


def draw_lights(stdscr):
    for light in lights:
        if light['is_on']:
            stdscr.addch(light['y'], light['x'], light['char'],
                         curses.color_pair(light['color']))
        else:
            stdscr.addch(light['y'], light['x'], NEEDLE_CHAR,
                         curses.color_pair(GREEN))


def toggle_lights():
    global lights
    for light in lights:
        light['is_on'] = not light['is_on']


def draw_gifts(stdscr, max_y, max_x):
    gifts_positions = [
        (max_y // 2 + TREE_HEIGHT - 6 + VERTICAL_OFFSET, max_x // 2 - 6),
        (max_y // 2 + TREE_HEIGHT - 6 + VERTICAL_OFFSET, max_x // 2 + 4),
        (max_y // 2 + TREE_HEIGHT - 5 + VERTICAL_OFFSET, max_x // 2 + 1),
        (max_y // 2 + TREE_HEIGHT - 7 + VERTICAL_OFFSET, max_x // 2 - 3),
    ]

    for (y, x) in gifts_positions:
        stdscr.addstr(y, x, GIFT_CHAR, curses.color_pair(MAGENTA))


def draw_snowflakes(stdscr, flakes, max_x, max_y):
    for flake in flakes:
        if random.random() < 0.1:  # 10% chance to be golden
            color_pair = GOLDEN
        else:
            color_pair = WHITE

        stdscr.addch(flake['y'], flake['x'], '*', curses.color_pair(color_pair))
        flake['y'] += 1
        if flake['y'] >= max_y - 5:
            flake['y'] = 0


def draw_message(stdscr, max_y, max_x):
    stdscr.addstr(1, 2, MESSAGE1, curses.color_pair(WHITE))
    stdscr.addstr(max_y - 3, max_x - len(MESSAGE2) - 2, MESSAGE2, curses.color_pair(WHITE))
    stdscr.addstr(max_y - 2, max_x - len(FROM) - 3, FROM, curses.color_pair(WHITE))


def main(stdscr):
    time_delay = 0.15
    update_interval = 1.0
    last_update_time = time.time()
    global MESSAGE1, MESSAGE2, FROM, VERTICAL_OFFSET

    args = sys.argv[1:]
    for i in range(len(args)):
        if args[i] == "-t" and i + 1 < len(args):
            try:
                time_delay = float(args[i + 1])
            except ValueError:
                print("Invalid time value.")
                return
        elif args[i] == "-m1" and i + 1 < len(args):
            MESSAGE1 = args[i + 1]
        elif args[i] == "-m2" and i + 1 < len(args):
            MESSAGE2 = args[i + 1]
        elif args[i] == "-f" and i + 1 < len(args):
            FROM = args[i + 1]
        elif args[i] == "-v" and i + 1 < len(args):
            try:
                VERTICAL_OFFSET = int(args[i + 1])
            except ValueError:
                print("Invalid vertical offset value.")
                return
        elif args[i] in ("-h", "--help"):
            print(USAGE)
            return

    curses.start_color()
    curses.init_pair(GREEN, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(RED, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(BLUE, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(YELLOW, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(WHITE, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(MAGENTA, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(GOLDEN, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    curses.init_pair(8, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(9, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_BLACK)

    stdscr.nodelay(True)

    max_y, max_x = stdscr.getmaxyx()
    flakes = [{'x': i, 'y': random.randint(0, max_y - 5)} for i in range(max_x)]

    initialize_lights(stdscr, max_y, max_x)

    while True:
        stdscr.clear()
        draw_snowflakes(stdscr, flakes, max_x, max_y)
        draw_tree(stdscr, max_y, max_x)
        current_time = time.time()
        if current_time - last_update_time > update_interval:
            toggle_lights()
            initialize_lights(stdscr, max_y, max_x)
            last_update_time = current_time
        draw_lights(stdscr)
        draw_gifts(stdscr, max_y, max_x)
        draw_message(stdscr, max_y, max_x)
        stdscr.refresh()
        time.sleep(time_delay)

        if stdscr.getch() == ord('q'):
            break

        for flake in flakes:
            flake['y'] += 1
            if flake['y'] >= max_y:
                flake['y'] = 0


if __name__ == "__main__":
    curses.wrapper(main)
