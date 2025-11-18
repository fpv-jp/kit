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

PLATE_WIDTH = 29.0
PLATE_HEIGHT = 5
PLATE_THICKNESS = 16.5

plate = base.cube_create(
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, 0),
)
base.cube_cut(
    target=plate,
    scale=(19.8, 10, 12.8),
)


PLATE_WIDTH = 22
PLATE_HEIGHT = 86

PLATE_HEIGHT_ = 23.75

GAP = 14
plate.location = (GAP, PLATE_HEIGHT / 2 + 2.5, 0)

M3 = 1.75

## main2 -----------------------------------

PLATE_HEIGHT_2 = PLATE_HEIGHT / 2 - PLATE_HEIGHT_ + MAIN_THICKNESS

main2 = base.cube_create(
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT, PLATE_THICKNESS),
)
base.cube_cut(
    target=main2,
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, MAIN_THICKNESS / 2, MAIN_THICKNESS),
)
base.cube_add(
    target=main2,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, MAIN_THICKNESS / 2, PLATE_THICKNESS),
    location=(0, PLATE_HEIGHT_2, 0),
)
base.cube_cut(
    target=main2,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT + MAIN_THICKNESS, PLATE_THICKNESS),
    location=(0, 0, PLATE_THICKNESS / 2),
)
base.cube_cut(
    target=main2,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT_, PLATE_THICKNESS),
    location=(
        0,
        PLATE_HEIGHT / 2 - PLATE_HEIGHT_ / 2 + MAIN_THICKNESS * 1.5 - 0.375,
        MAIN_THICKNESS,
    ),
)

## main2 hole -----------------------------------
base.cylinder_cut(
    target=main2,
    radius=M3,
    depth=20,
    location=(0, 25.25, 0),
)
base.cylinder_cut(
    target=main2,
    radius=M3,
    depth=20,
    location=(7.0, -38.0, 0.0),
)
base.cylinder_cut(
    target=main2,
    radius=1.25,
    depth=3,
    location=(0, -42.5, -5),
    rotation=(math.pi / 2, 0, 0),
)

## main2 cut -----------------------------------
X = PLATE_WIDTH / 2 - MAIN_THICKNESS
base.cube_cut(
    target=main2,
    scale=(2, 5, 5),
    location=(X, (PLATE_HEIGHT) / 2 - PLATE_HEIGHT_, 0),
)
base.cube_cut(
    target=main2,
    scale=(2, 5, 5),
    location=(-X, (PLATE_HEIGHT) / 2 - PLATE_HEIGHT_, 0),
)

main2.location = (GAP, 0, 0)
base.join(main2, plate)

## main3 -----------------------------------

main3 = base.cube_create(
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT, PLATE_THICKNESS),
)
base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, MAIN_THICKNESS / 2, MAIN_THICKNESS),
)
base.cube_add(
    target=main3,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, MAIN_THICKNESS / 2, PLATE_THICKNESS),
    location=(0, PLATE_HEIGHT_2, 0),
)
base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT + MAIN_THICKNESS, PLATE_THICKNESS),
    location=(0, -PLATE_HEIGHT_ + MAIN_THICKNESS - 0.375, PLATE_THICKNESS / 2),
)
base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, PLATE_THICKNESS / 2 - MAIN_THICKNESS / 2),
)

base.cube_cut(
    target=main3,
    scale=(PLATE_WIDTH + MAIN_THICKNESS, PLATE_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, PLATE_THICKNESS / 2),
)

## main3 hole -----------------------------------
base.cylinder_cut(
    target=main3,
    radius=M3,
    depth=20,
    location=(0, 25.25, 0),
)
base.cylinder_cut(
    target=main3,
    radius=M3,
    depth=20,
    location=(-7.0, -38.0, 0),
)

## main3 cut -----------------------------------
base.cube_cut(
    target=main3,
    scale=(3, 2, 5),
    location=(-10.5, 28, 5),
)

main3.location = (-GAP, 0, 0)
