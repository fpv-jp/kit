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

# 初期化
base.init()

# main -----------------------------------
M3 = 1.75
M2 = 1.5

MAIN_WIDTH = 100.0
MAIN_HEIGHT = 80.0
MAIN_DEPTH = 13.5
MAIN_THICKNESS = 2.0

MAIN_SHRINK = 2.0

C = MAIN_THICKNESS + 1

main = base.cube_create(
    name="main",
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS - MAIN_SHRINK, MAIN_DEPTH),
    location=(0, 0, 0),
)

base.cube_cut(
    target=main,
    name="main",
    scale=(MAIN_WIDTH, MAIN_HEIGHT - MAIN_SHRINK, MAIN_DEPTH),
    location=(0, 0, MAIN_THICKNESS),
)

main.location = (0, MAIN_SHRINK, 0)

bottom = (MAIN_THICKNESS - MAIN_DEPTH) / 2


## sink -----------------------------------

M3 = 1.85

sink_x = 11
sink_y = 15

base.cube_cut(
    target=main,
    name="heat-sink",
    scale=(26, 26, C),
    location=(sink_x, sink_y, bottom),
)
holes2 = [
    (sink_x + 32, sink_y ),
    (sink_x , sink_y - 32),
]

for i, (x, y) in enumerate(holes2):
    base.cylinder_cut(
        target=main,
        name=f"fun-hole{i}",
        radius=M3,
        depth=C,
        location=(x, y, bottom),
    )

# gpio -----------------------------------
base.cube_cut(
    target=main,
    name="gpio",
    scale=(6, 51, C),
    location=(-40.9, 7.8, bottom),
)


## mount -----------------------------------

x = MAIN_WIDTH / 2.0
y = MAIN_HEIGHT / 2.0

M = 1.25

holes = [
    (x - (3 + M), y - (1.6 + M)),
    (x - (3 + M), -y + (17.6 + M)),
    (-x + (8.2 + M), y - (1.6 + M)),
    (-x + (8.2 + M), -y + (17.6 + M)),
]

base.punch_holes(
    target=main,
    name="punch_hole",
    radius=M3,
    depth=C,
    height_pos=bottom,
    holes=holes,
)


## usb -----------------------------------

main.location = (MAIN_WIDTH / 2, (MAIN_HEIGHT + MAIN_THICKNESS) / 2, -MAIN_DEPTH / 2)


x = 8.0
y = 10.0
z = 4.2 - 1.5

d = 11.8

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)

x = 16.7
y = 21.5
z = 15.3 - 1.5

d = 30.9

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)

x = 13.2
y = 17.5
z = 17.2 - 1.5

d = 47

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)


x = 13.2
y = 10.0
z = 8.5 - 1.5

d = 64

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)


x = 15.5
y = 10.0
z = 7.8 - 1.5

d = 83.25

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)

x = 9.5
y = 10.0
z = 4.8 - 1.5

d = 97.5

base.cube_cut(
    target=main,
    name="main",
    scale=(x, y, z),
    location=(d - x / 2, y / 2, -z / 2),
)

main.location = (0, 0, 0)
