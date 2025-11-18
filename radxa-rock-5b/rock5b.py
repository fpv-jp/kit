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

# 初期化
base.init()

# main -----------------------------------
MAIN_WIDTH = 100.15
MAIN_HEIGHT = 74.25
MAIN_DEPTH = 11.8
MAIN_THICKNESS = 1.5

main = base.cube_create(
    name="main",
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, 0),
)

MAIN_HEIGHT2 = 56

base.cube_add(
    target=main,
    name="side_union",
    scale=(MAIN_WIDTH + MAIN_THICKNESS * 2, MAIN_HEIGHT2, MAIN_DEPTH),
    location=(
        0,
        (-MAIN_HEIGHT - MAIN_THICKNESS) / 2 + MAIN_HEIGHT2 / 2,
        (MAIN_DEPTH - MAIN_THICKNESS) / 2,
    ),
)
base.cube_cut(
    target=main,
    name="side_union",
    scale=(MAIN_WIDTH, MAIN_HEIGHT2, MAIN_DEPTH),
    location=(
        0,
        (-MAIN_HEIGHT - MAIN_THICKNESS) / 2 + MAIN_HEIGHT2 / 2 + MAIN_THICKNESS,
        (MAIN_DEPTH - MAIN_THICKNESS) / 2 + MAIN_THICKNESS,
    ),
)

M3 = 1.75

hole_gap_y = 8.6
prop_x1 = 93.15 / 2
prop_y1 = 49.0 / 2

holes = [
    (prop_x1, prop_y1 + hole_gap_y),
    (-prop_x1, prop_y1 + hole_gap_y),
    (prop_x1, -prop_y1 + hole_gap_y),
    (-prop_x1, -prop_y1 + hole_gap_y),
    (prop_x1 - 58.5, prop_y1 + hole_gap_y),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=main,
        name=f"hole_{i}",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

sink_x = 17
sink_y = -1

base.cube_cut(
    target=main,
    name="heat-sink",
    scale=(26, 26, MAIN_THICKNESS + 1),
    location=(sink_x, sink_y, 0),
)

M3 = 1.85

holes2 = [
    (sink_x + 24.2, sink_y + 4.3),
    (sink_x + 4.3, sink_y + 24.2),
]

for i, (x, y) in enumerate(holes2):
    base.cylinder_cut(
        target=main,
        name=f"fun-hole{i}",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

base.cube_cut(
    target=main,
    name="cut_9",
    scale=(51, 7, MAIN_THICKNESS + 1),
    location=((93.15 - 58.5) / 2, (MAIN_HEIGHT - 7) / 2, 0),
)

base.cube_cut(
    target=main,
    name="cut_10",
    scale=(6, 6, MAIN_THICKNESS + 1),
    location=(prop_x1 - 58.5, 26.5, 0),
)

main.location = (0, (MAIN_HEIGHT + MAIN_THICKNESS) / 2, 0)

##############################################

side_height = 12
side_height2 = (side_height - MAIN_THICKNESS) / 2

x = MAIN_WIDTH / 2 - 6.45
y = 14.5
base.cube_cut(
    target=main,
    name="cut_1",
    scale=(6.6, y, 6.5),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2 + 6.5 / 2),
)

x = x - 8.55
y = 14.5
base.cube_cut(
    target=main,
    name="cut_2",
    scale=(3.6, y, 11.5),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2 + MAIN_THICKNESS),
)

x = x - 9.80
y = 18
base.cube_cut(
    target=main,
    name="cut_3",
    scale=(5.7, y, side_height),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2),
)

x = x - 12.7
y = 18
base.cube_cut(
    target=main,
    name="cut_4",
    scale=(5.7, y, side_height),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2),
)

x = x - 15.5
y = 15.7
base.cube_cut(
    target=main,
    name="cut_5",
    scale=(13.5, y, side_height),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2),
)

x = x - 19.20
y = 16.1
base.cube_cut(
    target=main,
    name="cut_6",
    scale=(13.5, y, side_height),
    location=(x, (y - MAIN_THICKNESS) / 2, side_height2),
)

x = x - 26.80
y = 19.8
base.cube_cut(
    target=main,
    name="cut_7",
    scale=(16.1, y, side_height),
    location=(x + 9, (y - MAIN_THICKNESS) / 2, side_height2),
)

##############################################

base.cylinder_cut(
    target=main,
    name="antenna_hole",
    radius=3.25,
    location=(-MAIN_WIDTH / 2, 28, MAIN_DEPTH / 2),
    depth=5,
    rotation=(0, math.pi / 2, 0),
    vertices=64,
)
