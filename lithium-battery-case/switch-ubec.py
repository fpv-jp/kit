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
PLATE_HEIGHT = 16.5
PLATE_THICKNESS = 5

plate = base.cube_create(
    name="plate",
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, 0),
)

base.cube_clear(
    target=plate,
    name="cube_clear",
    scale=(19.8, 12.8, 10),
    location=(0, 0, 2),
)
plate.location = (0, 58, PLATE_HEIGHT / 2)
plate.rotation_euler = (-math.pi / 2, 0, 0)

# main2 -----------------------------------

PLATE_WIDTH = 20.5
PLATE_HEIGHT = 62
PLATE_DEPTH = 10

main2 = base.cube_create(
    name="main2",
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT + MAIN_THICKNESS, PLATE_DEPTH),
    location=(0, 0, 0),
)

base.cube_add(
    target=main2,
    name="cube_add",
    scale=(PLATE_WIDTH + MAIN_THICKNESS, 40, MAIN_THICKNESS),
    location=(0, 40, (MAIN_THICKNESS - PLATE_DEPTH) / 2),
)

base.cube_clear(
    target=main2,
    name="cube_clear2",
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_DEPTH),
    location=(0, 0, MAIN_THICKNESS),
)

base.cube_clear(
    target=main2,
    name="cube_clear2",
    scale=(2.2, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(PLATE_WIDTH / 2 - MAIN_THICKNESS, 10, MAIN_THICKNESS),
)

base.cube_clear(
    target=main2,
    name="cube_clear2",
    scale=(2.2, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(-PLATE_WIDTH / 2 + MAIN_THICKNESS, 10, MAIN_THICKNESS),
)

base.cube_clear(
    target=main2,
    name="cube_clear0",
    scale=(1.75, PLATE_HEIGHT + 5, PLATE_DEPTH),
    location=(0, -10, MAIN_THICKNESS),
)

main2.location[2] = PLATE_DEPTH / 2

base.join(plate, main2)
