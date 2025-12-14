import bpy
import sys
import types
import math

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

base.init()

# main -----------------------------------
MAIN_WIDTH = 100.15
MAIN_HEIGHT = 74.25
MAIN_DEPTH = 8.0
MAIN_THICKNESS = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH + MAIN_THICKNESS),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 0.1, MAIN_HEIGHT - 0.1, MAIN_DEPTH),
    location=(0, 0, -MAIN_THICKNESS / 2),
)

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2

M3 = 1.7

P_X = -BASE_X + 3.5
P_Y = BASE_Y - 3.6

G_X = 93.15
G_Y = 49.0
G_X2 = 58.5

base.punch_holes(
    target=main,
    radius=M3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=[
        (P_X, P_Y),
        (P_X + G_X, P_Y),
        (P_X, P_Y - G_Y),
        (P_X + G_X, P_Y - G_Y),
        (P_X + G_X2, P_Y),
    ],
)

# --------------------------- CPU

base.cube_cut(
    target=main,
    scale=(26, 26, MAIN_DEPTH + MAIN_THICKNESS),
    location=(-BASE_X + 32.9, -BASE_Y + 35.9, 0),
)

M3 = 1.6

P_X = -BASE_X + 8.3 + M3
P_X2 = -BASE_X + 62.2 + M3
P_X3 = BASE_X - 37.3 - M3

P_Y = BASE_Y - 17.8 - M3
P_Y2 = BASE_Y - 50.8 - M3
P_Y3 = BASE_Y - 37.8 - M3

base.punch_holes(
    target=main,
    radius=M3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=[
        (P_X, P_Y),
        (P_X, P_Y2),
        (P_X2, P_Y),
        (P_X2, P_Y2),
        (P_X3, P_Y3),
    ],
)

# --------------------------- GPIO

GIPO_X = 50.7
GIPO_Y = 5.1

base.cube_cut(
    target=main,
    scale=(GIPO_X, GIPO_Y, MAIN_DEPTH + MAIN_THICKNESS),
    location=(-BASE_X + 32.6, BASE_Y - 3.4, 0),
)

GIPO_X = 5.0
GIPO_Y = 5.1

base.cube_cut(
    target=main,
    scale=(GIPO_X, GIPO_Y, MAIN_DEPTH + MAIN_THICKNESS),
    location=(BASE_X - 35.7 - GIPO_X / 2, BASE_Y - 7.7 - GIPO_Y / 2, 0),
)

# --------------------------- WIFI

WIFI_X = 21.9
WIFI_Y = 33.3

base.cube_cut(
    target=main,
    scale=(WIFI_X, WIFI_Y, MAIN_DEPTH + MAIN_THICKNESS),
    location=(BASE_X - 7.9 - WIFI_X / 2, BASE_Y - 9.1 - WIFI_Y / 2, 0),
)

# antenna
base.cylinder_cut(
    target=main,
    radius=3.2,
    location=(BASE_X, -9.0, -MAIN_THICKNESS / 2),
    depth=MAIN_DEPTH,
    rotation=(0, math.pi / 2, 0),
    vertices=64,
)


###############################################


def cube_cut(scale, pos):
    y = -BASE_Y + scale[1] / 2 - 2
    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(pos, y, z),
    )


H = 15

GAP = 0.5

base.cylinder_cut(
    target=main,
    radius=3.15 + GAP / 2,
    location=(-BASE_X + 6.4, -BASE_Y + 5 / 2 - 2, -2),
    depth=5,
    rotation=(math.pi / 2, 0, 0),
)


cube_cut(scale=(6.3 + GAP, H, 2.7), pos=-BASE_X + 6.4)  # DC
cube_cut(scale=(3.2 + GAP, 13.8, 10.0), pos=-BASE_X + 14.9)  # USB-C
cube_cut(scale=(5.6 + GAP, 21.5, H), pos=-BASE_X + 24.7)  # HDMI1
cube_cut(scale=(5.6 + GAP, 21.5, H), pos=-BASE_X + 37.4)  # HDMI2
cube_cut(scale=(13.0 + GAP, 17.0, H), pos=-BASE_X + 52.9)  # USB1
cube_cut(scale=(13.0 + GAP, 17.0, H), pos=-BASE_X + 71.6)  # USB2
cube_cut(scale=(16.0 + GAP, 20.5, H), pos=-BASE_X + 90.0)  # ETH

###############################################


def cube_cut2(scale, pos):
    y = BASE_Y - scale[1] / 2 + 2
    z = (scale[2] - MAIN_DEPTH - MAIN_THICKNESS) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(pos, y, z),
    )


cube_cut2(scale=(4.5 + GAP, 3.5, 3.5), pos=BASE_X - 10.8)  # BUTTON1
cube_cut2(scale=(4.5 + GAP, 3.5, 3.5), pos=BASE_X - 17.7)  # BUTTON1
cube_cut2(scale=(3.0 + GAP, 3.5, 2.0), pos=BASE_X - 23.7)  # LED
cube_cut2(scale=(6.5 + GAP, 3.5, 4.0), pos=BASE_X - 31.6)  # USB-B?

main.rotation_euler = (math.radians(180), 0, 0)
