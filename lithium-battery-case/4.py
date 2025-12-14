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
MAIN_HEIGHT = 78.8 + GAP
MAIN_THICKNESS = 20.6

main = base.cube_create(
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT + WALL * 2 + 9.0, MAIN_THICKNESS),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT + 9.0, MAIN_THICKNESS),
    location=(0, 0, WALL),
)
base.cube_cut(
    target=main,
    scale=(11.75, WALL * 2, 6.75),
    location=(0, (MAIN_HEIGHT + 9.0 + WALL) / 2, -3),
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
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT2 + WALL * 2 + 12.0, MAIN_THICKNESS),
    location=(0, 0, WALL + 8.0),
)

# main.rotation_euler = (0, math.pi, 0)
# main.location=(0, 0, 5.55)
