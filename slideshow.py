#!/usr/bin/env python
"""slideshow.py

Copyright (c) 2013, 2015, Corey Goldberg
              2020,       Ryan Matlock

Dev: https://github.com/cgoldberg/py-slideshow
License: GPLv3


Modifications:
- [ ] option to enable pan/zoom (disabled by default)
- [ ] option to control time image is on screen
- [ ] option to control transition type (hard or dissolve) -- this might not be
      trivial with pyglet
- [ ] option to update images if new ones are added while slideshow is running
- [ ] option to run infinitely/once through stack of images
- [ ] option to display images at random or ordered by name
- [ ] ability to navigate forwards and backwards with arrow keys
"""


import argparse
import random
import os
import sys
import pyglet


def update_pan_zoom_speeds():
    global _pan_speed_x
    global _pan_speed_y
    global _zoom_speed
    _pan_speed_x = random.randint(-8, 8)
    _pan_speed_y = random.randint(-8, 8)
    _zoom_speed = random.uniform(-0.02, 0.02)
    return _pan_speed_x, _pan_speed_y, _zoom_speed


def update_pan(dt):
    sprite.x += dt * _pan_speed_x
    sprite.y += dt * _pan_speed_y


def update_zoom(dt):
    sprite.scale += dt * _zoom_speed


def update_image(dt):
    img = pyglet.image.load(random.choice(image_paths))
    sprite.image = img
    sprite.scale = get_scale(window, img)
    sprite.x = 0
    sprite.y = 0
    update_pan_zoom_speeds()
    window.clear()


def get_image_paths(input_dir='.'):
    paths = []
    for root, dirs, files in os.walk(input_dir, topdown=True):
        for file in sorted(files):
            if file.endswith(('jpg', 'jpeg', 'png', 'gif')):
                path = os.path.abspath(os.path.join(root, file))
                paths.append(path)
    return paths


def get_scale(window, image):
    if image.width > image.height:
        scale = float(window.width) / image.width
    else:
        scale = float(window.height) / image.height
    return scale


def next_image():
    print('NEXT!')


def prev_image():
    print('jump to prev image')

# maybe I also want to be able to jump to beginning or end of slideshow 🤷
def first_image():
    print('jump to first image')


def last_image():
    print('jump to last image')


NEXT_KEYS = [
    pyglet.window.key.RIGHT,
    pyglet.window.key.DOWN,
    pyglet.window.key.D,  # as in WASD
    pyglet.window.key.S,
    pyglet.window.key.N,  # as in next
    pyglet.window.key.SPACE,  # eh, seems natural enough
    pyglet.window.key.L,  # for monsters who use vi 😉
    pyglet.window.key.J,
]

PREV_KEYS = [
    pyglet.window.key.LEFT,
    pyglet.window.key.UP,
    pyglet.window.key.A,  # as in WASD
    pyglet.window.key.W,
    pyglet.window.key.P,  # as in prev
    pyglet.window.key.BACKSPACE,  # eh, seems natural enough
    pyglet.window.key.H,  # for monsters who use vi 😉
    pyglet.window.key.K,
]

FIRST_KEYS = [
    pyglet.window.key.HOME,
    pyglet.window.key._1,
]

LAST_KEYS = [
    pyglet.window.key.END,
    pyglet.window.key._0,
]


# see
# https://pyglet.readthedocs.io/en/latest/programming_guide/events.html#stacking-event-handlers
# def on_key_press(symbol, modifiers):
#     if symbol == key.SPACE:
#         fire_laser()
def on_key_press(symbol, modifiers):
    if symbol in NEXT_KEYS:
        next_image()
    elif symbol in PREV_KEYS:
        prev_image()
    elif symbol in FIRST_KEYS:
        first_image()
    elif symbol in LAST_KEYS:
        last_image()
    else:
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--dir',
        help='directory of images',
    )
    parser.add_argument(
        '-p', '--panzoom',
        help='enable panning and zooming',
        action='store_true'
    )
    parser.add_argument(
        '-t', '--time',
        help='time image is on screen (in seconds)',
        default=5.0,
        type=float
    )
    parser.add_argument(
        '-u', '--update',
        help='update image stack when new images are added to directory',
        default=True,
        action='store_true'
    )
    duration = parser.add_mutually_exclusive_group()
    duration.add_argument(
        '-I', '--infinite',
        help='loop through images infinitely',
        default=True,
        action='store_true'
    )
    duration.add_argument(
        '-O', '--once',
        help='loop through images once',
        action='store_true'
    )
    duration.add_argument(
        '-N', '--ntimes',
        help='loop through images N times',
        type=int
    )
    order = parser.add_mutually_exclusive_group()
    order.add_argument(
        '-r', '--random',
        help='randomly choose images from directory',
        action='store_true'
    )
    order.add_argument(
        '-s', '--sequential',
        help='sequentially choose images from directory',
        default=True,
        action='store_true'
    )

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = vars(parser.parse_args())
    print(args)

    global window
    window = pyglet.window.Window(fullscreen=True)

    @window.event
    def on_draw():
        sprite.draw()

    window.push_handlers(on_key_press)

    _pan_speed_x, _pan_speed_y, _zoom_speed = update_pan_zoom_speeds()

    global image_paths
    image_paths = get_image_paths(args['dir'])
    global img
    img = pyglet.image.load(random.choice(image_paths))
    global sprite
    sprite = pyglet.sprite.Sprite(img)
    sprite.scale = get_scale(window, img)

    pyglet.clock.schedule_interval(update_image, args['time'])
    pyglet.clock.schedule_interval(update_pan, 1/60.0)
    pyglet.clock.schedule_interval(update_zoom, 1/60.0)

    pyglet.app.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())
