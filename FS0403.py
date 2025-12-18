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

MAIN_WIDTH = 27.4
MAIN_HEIGHT = 8.0
MAIN_DEPTH = 7.2

MAIN_THICKNESS = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

MAIN_WIDTH2 = 20.0

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH2, MAIN_HEIGHT, MAIN_DEPTH / 2),
    location=(0, 0, MAIN_DEPTH / 4),
)

M2 = 0.95
X = 11.0 + M2
M4 = 4.1
M5_6 = 2.3

ARM = 10.0
ARM2 = 36.0

MAIN_AXIS = MAIN_WIDTH2 / 2 - M4

BASE_Z = -MAIN_DEPTH / 4

base.cube_add(
    target=main,
    scale=(MAIN_DEPTH / 2, ARM, MAIN_DEPTH / 2),
    location=(MAIN_AXIS, ARM / 2, BASE_Z),
)

base.ring_add(
    target=main,
    outer_radius=M4 + MAIN_THICKNESS + 1,
    inner_radius=M4,
    location=(MAIN_AXIS, 0, BASE_Z),
    depth=MAIN_DEPTH / 2,
)
base.punch_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH,
    holes=[(X, 0), (-X, 0)],
)
base.punch_holes(
    target=main,
    radius=M5_6,
    depth=MAIN_DEPTH,
    holes=[(MAIN_WIDTH2 / 2 - 10.55 + M5_6, 0)],
)
base.punch_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH,
    holes=[(MAIN_WIDTH2 / 2 - 13.3 + M2, 0)],
)

#############################################

base.cube_add(
    target=main,
    scale=(ARM2, MAIN_THICKNESS + 1, MAIN_DEPTH / 2),
    location=(MAIN_AXIS, ARM, BASE_Z),
)

R = 0.6

base.punch_holes(
    target=main,
    radius=R,
    depth=MAIN_THICKNESS + 1,
    height_pos=BASE_Z,
    holes=[
        (MAIN_AXIS + 16.0, ARM),
        (MAIN_AXIS - 16.0, ARM),
    ],
    rotation=(math.pi / 2, 0, 0),
)

base.ring_add(
    target=main,
    outer_radius=R * 3,
    inner_radius=R,
    location=(MAIN_AXIS + 16.0, ARM + 0.5, BASE_Z),
    depth=MAIN_THICKNESS + 2,
    rotation=(math.pi / 2, 0, 0),
)
base.ring_add(
    target=main,
    outer_radius=R * 3,
    inner_radius=R,
    location=(MAIN_AXIS - 16.0, ARM + 0.5, BASE_Z),
    depth=MAIN_THICKNESS + 2,
    rotation=(math.pi / 2, 0, 0),
)
