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

MAIN_WIDTH = 14.5
MAIN_HEIGHT = 10.0
MAIN_DEPTH = 5.25

MAIN_THICKNESS = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

outer_radius = MAIN_WIDTH / 2

base.ring_add(
    target=main,
    outer_radius=outer_radius,
    inner_radius=outer_radius - MAIN_THICKNESS,
    location=(0, 0, MAIN_DEPTH / 2),
    depth=MAIN_HEIGHT,
    rotation=(math.pi / 2, 0, 0),
)

###############################################################

M3 = 1.8

main.location = (0, M3, 0)

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
    scale=(MAIN_WIDTH - MAIN_THICKNESS * 2, 100, MAIN_DEPTH),
)

###############################################################

base.cube_cut(
    target=main,
    scale=(40, 40, 5),
    location=(0, 0, -(5 + MAIN_THICKNESS) / 2),
)
