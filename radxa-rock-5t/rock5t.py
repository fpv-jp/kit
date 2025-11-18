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
    location=(0, 0, -WALL),
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

# ---------------------------------------

def cube_cut(scale, pos):
    y = BASE_Y - scale[1] / 2 + 3.62
    z = (scale[2] - MAIN_DEPTH - WALL) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(pos, y, z),
    )

H = 15
cube_cut(scale=(10.7, 14.1, H), pos=BASE_X - 5.968)  # DC
cube_cut(scale=(13.5, 18.2, H), pos=BASE_X - 20.44)  # USB1
cube_cut(scale=(13.5, 18.2, H), pos=BASE_X - 37.38)  # USB2
cube_cut(scale=(6.2, 22.7, H), pos=-BASE_X + 56.16)  # HDMI1
cube_cut(scale=(6.2, 22.7, H), pos=-BASE_X + 42.31)  # HDMI2
cube_cut(scale=(16.9, 21.6, H), pos=-BASE_X + 28.115)  # LAN1
cube_cut(scale=(16.9, 21.6, H), pos=-BASE_X + 9.091)  # LAN2

def cube_cut2(scale, posx, posy):
    z = (scale[2] - MAIN_DEPTH - WALL) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(posx, posy, z),
    )

CPU = 26.0
cube_cut2(scale=(CPU, CPU, H), posx=-BASE_X + 35.46 + CPU / 2, posy=-BASE_Y + 28.385 + CPU / 2)  # CPU
cube_cut2(scale=(13.1, 17.1, H), posx=-BASE_X + 13.71, posy=-BASE_Y + 25.483)  # Wifi
cube_cut2(scale=(51.01, 5.23, H), posx=BASE_X - 32.743, posy=-BASE_Y + 3.485)  # GPIO

cube_cut2(scale=(3.09, 5.79, H), posx=-BASE_X + 8.525, posy=BASE_Y - 25.955)  # J201
cube_cut2(scale=(3.09, 10.71, H), posx=-BASE_X + 8.491, posy=-BASE_Y + 10.683)  # J202

# side -------------
cube_cut2(scale=(8.52, 15.687, 5.6), posx=BASE_X - 1.59, posy=BASE_Y - (33.784 + 15.687 / 2))
cube_cut2(scale=(2.72, 2.583, 3.5), posx=BASE_X, posy=BASE_Y - 20.946)
cube_cut2(scale=(2.72, 2.626, 3.5), posx=BASE_X, posy=BASE_Y - 55.171)

# back -------------
cube_cut2(scale=(2.72, 2.626, 3.5), posx=-BASE_X + 10.64, posy=-BASE_Y)
cube_cut2(scale=(6.50, 2.626, 5.2), posx=-BASE_X + 19.35, posy=-BASE_Y)
cube_cut2(scale=(9.21, 2.626, 3), posx=-BASE_X + (28.67 + 9.21 / 2), posy=-BASE_Y)
cube_cut2(scale=(2.72, 2.626, 1.5), posx=-BASE_X + 42.647, posy=-BASE_Y)

main.rotation_euler = (math.radians(180), 0, 0)
