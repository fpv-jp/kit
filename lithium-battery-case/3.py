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

## main -----------------------------------
WALL = 1.5

GAP = 0.2

MAIN_WIDTH = 75.6 + GAP
MAIN_HEIGHT = 77.8 + GAP
MAIN_THICKNESS = 12.6

main = base.cube_create(
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT + WALL * 2, MAIN_THICKNESS),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, WALL),
)

base.cube_add(
    target=main,
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT + WALL * 2 + 9.0, WALL),
    location=(0, 0, (WALL - MAIN_THICKNESS) / 2),
)

MAIN_WIDTH2 = 7.8
MAIN_HEIGHT2 = 66.2

MAIN_WIDTH3 = 6.5

pos = [27.3, 9.1, -9.1, -27.3]

for i, (p) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(MAIN_WIDTH2, MAIN_HEIGHT2, MAIN_THICKNESS),
        location=(p, 0, 0),
    )
    base.cube_cut(
        target=main,
        scale=(MAIN_WIDTH3, MAIN_HEIGHT + WALL * 5, MAIN_THICKNESS),
        location=(p, 0, WALL),
    )

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT2, MAIN_THICKNESS),
    location=(0, 0, WALL + 6.0),
)

M2_5 = 2.7 / 2

X_POS = (34.2 + M2_5) / 2
Y_POS = (52.5 + M2_5) / 2

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=main,
        radius=M2_5,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )
