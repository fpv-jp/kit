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

MAIN_WIDTH = 81.6 + GAP
MAIN_HEIGHT = 81.8 + GAP
MAIN_THICKNESS = 20.6

main = base.cube_create(
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT + WALL * 5, MAIN_THICKNESS),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT + WALL * 3, MAIN_THICKNESS),
    location=(0, 0, WALL),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH + WALL * 2, MAIN_HEIGHT + 0.2, MAIN_THICKNESS),
    location=(0, 0, MAIN_THICKNESS - 8.8),
)
base.cube_cut(
    target=main,
    scale=(12.5, WALL * 2, 7.5),
    location=(0, (MAIN_WIDTH + WALL * 4) / 2, -3),
)

MAIN_WIDTH2 = 8.2
MAIN_HEIGHT2 = 67.2

pos = [30, 10, -10, -30]

for i, (p) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(MAIN_WIDTH2, MAIN_HEIGHT2, MAIN_THICKNESS),
        location=(p, 0, 0),
    )

# main.rotation_euler = (0, math.pi, 0)
# main.location=(0, 0, 6.75)
