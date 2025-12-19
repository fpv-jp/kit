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

MAIN_WIDTH = 23.2
MAIN_HEIGHT = 12.0
MAIN_DEPTH = 17.0

MAIN_THICKNESS = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH + 9, MAIN_HEIGHT, MAIN_DEPTH + MAIN_THICKNESS),
    location=(0, 0, MAIN_DEPTH / 2),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
    location=(0, 0, (MAIN_DEPTH + MAIN_THICKNESS) / 2),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH + 9, MAIN_HEIGHT - 6, MAIN_DEPTH - MAIN_THICKNESS),
    location=(0, 0, MAIN_DEPTH / 2),
)
base.cube_add(
    target=main,
    scale=(MAIN_WIDTH + 9, 5, MAIN_THICKNESS),
    location=(0, -8, 0),
)

M3 = 1.3
X = 12.5 + 1.2
base.punch_holes(
    target=main,
    radius=M3,
    depth=MAIN_DEPTH,
    holes=[(X, 0), (-X, 0)],
    height_pos=10,
)

main.location = (0, 10, 0)

###############################################################

M3 = 1.8

X = 14

base.cube_add(
    target=main,
    scale=(X * 2, M3 * 3, MAIN_THICKNESS),
)

holes = [(-X, 0), (X, 0)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, 0),
        depth=MAIN_THICKNESS,
    )

base.cube_cut(
    target=main,
    scale=(19, 10, MAIN_THICKNESS + 1),
    location=(0, 7, 0),
)
