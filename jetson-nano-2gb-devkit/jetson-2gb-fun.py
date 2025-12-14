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

# main -----------------------------------
MAIN_WIDTH = 31
MAIN_HEIGHT = 31
MAIN_THICKNESS = 2.5

main = base.cube_create(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, 0),
)

base.cube_cut(
    target=main,
    scale=(26, 26, MAIN_THICKNESS + 1),
    location=(0, 0, 0),
)

prop_x1 = 10.0
prop_y1 = 10.0
M3 = 1.75

POS = 1.3
holes = [
    (prop_x1, prop_y1, POS, POS, 4.75, 5.25),
    (-prop_x1, prop_y1, -POS, POS, 5.25, 4.75),
    (prop_x1, -prop_y1, POS, -POS, 5.25, 4.75),
    #    (-prop_x1, -prop_y1, -POS, -POS, 4.75, 5.25),
]

for i, (x, y, a, b, n, m) in enumerate(holes):
    base.cylinder_add(
        target=main,
        radius=M3 * 1.55,
        depth=MAIN_THICKNESS,
        location=(x, y, 0),
    )
    base.cube_add(
        target=main,
        scale=(n, m, MAIN_THICKNESS),
        location=(x + a, y + b, 0),
        rotation=(0, 0, math.radians(45)),
    )
    base.cylinder_cut(
        target=main,
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

# main.rotation_euler[2] = math.radians(45)

M3 = 1.85

base.cube_add(
    target=main,
    scale=(M3 * 2, 16, MAIN_THICKNESS),
    location=(0, -23, 0),
)
base.cube_add(
    target=main,
    scale=(16, M3 * 2, MAIN_THICKNESS),
    location=(-23, 0, 0),
)

x = 32.0
holes2 = [(-x, 0), (0, -x)]

z = 12.0
for i, (x, y) in enumerate(holes2):
    base.ring_add(
        target=main,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, (z - MAIN_THICKNESS) / 2),
        depth=z,
    )
