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

M3 = 1.75
M2 = 1.5

# main -----------------------------------
MAIN_THICKNESS = 1.5

PLATE_WIDTH = 28
PLATE_HEIGHT = 5
PLATE_THICKNESS = 16.5

plate = base.cube_create(
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, 0),
)
base.cube_cut(
    target=plate,
    scale=(19.8, 10, 12.8),
    location=(0, 0, 0),
)
plate.location = (0, 58, PLATE_THICKNESS / 2)


## main2 -----------------------------------

PLATE_WIDTH = 20.5
PLATE_HEIGHT = 62
PLATE_DEPTH = PLATE_THICKNESS / 2

PLATE_HEIGHT_ = 23.75

main2 = base.cube_create(
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT + MAIN_THICKNESS, PLATE_DEPTH),
    location=(0, 0, 0),
)
base.cube_add(
    target=main2,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT_, MAIN_THICKNESS),
    location=(
        0,
        (PLATE_HEIGHT + PLATE_HEIGHT_ + MAIN_THICKNESS) / 2,
        (MAIN_THICKNESS - PLATE_DEPTH) / 2,
    ),
)
base.cube_cut(
    target=main2,
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_DEPTH),
    location=(0, 0, MAIN_THICKNESS),
)

base.cube_cut(
    target=main2,
    scale=(2.2, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(PLATE_WIDTH / 2 - MAIN_THICKNESS, 10, MAIN_THICKNESS + 3),
)

base.cube_cut(
    target=main2,
    scale=(2.2, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(-PLATE_WIDTH / 2 + MAIN_THICKNESS, 10, MAIN_THICKNESS + 3),
)

base.cube_cut(
    target=main2,
    scale=(1.75, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(0, -10, MAIN_THICKNESS + 3),
)

main2.location[2] = PLATE_DEPTH / 2
base.join(plate, main2)
plate.location[0] = -15


## main3 -----------------------------------

PLATE_WIDTH = 20.5
PLATE_HEIGHT = 62
PLATE_DEPTH = PLATE_THICKNESS / 2

PLATE_HEIGHT_ = 23.75

main3 = base.cube_create(
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT + MAIN_THICKNESS, PLATE_DEPTH),
    location=(0, 0, 0),
)
base.cube_add(
    target=main3,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT_, PLATE_THICKNESS - MAIN_THICKNESS),
    location=(
        0,
        (PLATE_HEIGHT + PLATE_HEIGHT_ + MAIN_THICKNESS) / 2,
        (PLATE_THICKNESS - MAIN_THICKNESS - PLATE_DEPTH) / 2,
    ),
)
base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_DEPTH),
    location=(0, 0, MAIN_THICKNESS),
)
base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH, PLATE_HEIGHT_, PLATE_THICKNESS),
    location=(
        0,
        (PLATE_HEIGHT + PLATE_HEIGHT_ + MAIN_THICKNESS) / 2,
        (PLATE_THICKNESS - PLATE_DEPTH) / 2 + MAIN_THICKNESS,
    ),
)

base.cube_cut(
    target=main3,
    scale=(3, 2, PLATE_THICKNESS),
    location=(-PLATE_WIDTH / 2, 40, PLATE_THICKNESS - 4),
)

main3.location[2] = PLATE_DEPTH / 2
main3.location[0] = 15
