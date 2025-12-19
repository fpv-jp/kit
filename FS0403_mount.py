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

MAIN_WIDTH = 25
MAIN_HEIGHT = 16.5
MAIN_DEPTH = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 7, MAIN_HEIGHT - 7, MAIN_DEPTH + 1),
)

M2 = 1.2
X = 10.5
Y = 6.25


base.cube_cut(
    target=main,
    scale=(3, 3, MAIN_DEPTH + 1),
    location=(-X - 2, Y + 2, 0),
    rotation=(0, 0, math.pi / 4),
)
base.cube_cut(
    target=main,
    scale=(3, 3, MAIN_DEPTH + 1),
    location=(-X - 2, -Y - 2, 0),
    rotation=(0, 0, math.pi / 4),
)


holes = [(X, Y), (X, -Y), (-X, Y), (-X, -Y)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=M2 * 2,
        inner_radius=M2,
        location=(x, y, 0),
        depth=MAIN_DEPTH,
    )

#############################################################

ARM_HEIGHT = 26.0
ARM_DEPTH = 4.5

left = base.cube_create(
    scale=(MAIN_DEPTH, ARM_HEIGHT, ARM_DEPTH),
)

M1_3 = 0.75

Y = ARM_HEIGHT / 2 - M1_3 * 1.9
Z = ARM_DEPTH / 2 - M1_3 * 1.9

base.punch_holes(
    target=left,
    radius=M1_3,
    depth=MAIN_DEPTH + 1,
    holes=[(0, Y), (0, -Y)],
    height_pos=Z,
    rotation=(0, math.pi / 2, 0),
)

SIDE = (MAIN_WIDTH + MAIN_DEPTH) / 2

left.location = (
    SIDE,
    3.75,
    (ARM_DEPTH - MAIN_DEPTH) / 2,
)

base.modifier_apply(obj=left, target=main, operation="UNION")
