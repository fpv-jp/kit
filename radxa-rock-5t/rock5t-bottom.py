import bpy
import math
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

base.init()

# main -----------------------------------
WALL = 1.75
MAIN_WIDTH = 110.2
MAIN_HEIGHT = 82.2
MAIN_DEPTH = 9.0
main = base.cube_create(
    scale=(MAIN_WIDTH + WALL, MAIN_HEIGHT + WALL, MAIN_DEPTH + WALL),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH + 0.1, MAIN_HEIGHT + 0.1, MAIN_DEPTH + 0.1),
    location=(0, 0, WALL),
)
BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2
base.punch_holes(
    target=main,
    radius=1.35,
    depth=MAIN_DEPTH + 5,
    holes=[
        (BASE_X - 3.56, -BASE_Y + 3.635),
        (-BASE_X + 48.591, -BASE_Y + 3.635),
        (-BASE_X + 3.462, -BASE_Y + 3.635),
        (-BASE_X + 3.344, BASE_Y - 21.7),
        (BASE_X - 3.66, BASE_Y - 29.705),
    ],
)
base.punch_holes(
    target=main,
    radius=1.6,
    depth=MAIN_DEPTH + 5,
    holes=[
        (-BASE_X + 22.48, BASE_Y - 39.18),
        (-BASE_X + 73.88, BASE_Y - 59.18),
    ],
)

## ---------------------------------------


def cube_cut2(scale, posx, posy):
    z = (-scale[2] + MAIN_DEPTH + WALL) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(posx, posy, z),
    )


cube_cut2(scale=(8.52, 11.8, 1.9), posx=BASE_X - 1.59, posy=-BASE_Y + (33.784 + 15.687 / 2 - 1.5))  # SD
cube_cut2(scale=(2.72, 7.5, 4.2), posx=BASE_X, posy=-BASE_Y + 23.0 + 7.5 / 2)
cube_cut2(scale=(8.52, 11.8, 1.9), posx=BASE_X - 1.59, posy=-BASE_Y + 14.05)  # SIM
