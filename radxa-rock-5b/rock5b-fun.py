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
MAIN_THICKNESS = 1.5

main = base.cube_create(
    name="main",
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, 0),
)

base.cube_cut(
    target=main,
    name="cut_center",
    scale=(26, 26, MAIN_THICKNESS + 1),
    location=(0, 0, 0),
)

prop_x1 = 10
prop_y1 = 10
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
        name=f"ring_outer_{i}",
        radius=M3 * 1.55,
        depth=MAIN_THICKNESS,
        location=(x, y, 0),
    )
    base.cube_add(
        target=main,
        name=f"ring_tab_{i}",
        scale=(n, m, MAIN_THICKNESS),
        location=(x + a, y + b, 0),
        rotation=(0, 0, math.radians(45)),
    )
    base.cylinder_cut(
        target=main,
        name=f"ring_inner_{i}",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

main.rotation_euler[2] = math.radians(45)

M3 = 1.85

X_POS = 14
Y_POS = 20

holes2 = [
    (X_POS, Y_POS),
    (-X_POS, Y_POS),
]

for i, (x, y) in enumerate(holes2):
    base.cylinder_add(
        target=main,
        name=f"ring2_outer_{i}",
        radius=M3 * 2,
        depth=MAIN_THICKNESS * 2,
        location=(x, y, MAIN_THICKNESS / 2),
    )
    base.cylinder_cut(
        target=main,
        name=f"ring2_inner_{i}",
        radius=M3,
        depth=MAIN_THICKNESS * 2 + 1,
        location=(x, y, MAIN_THICKNESS / 2),
    )

base.cube_add(
    target=main,
    name="tab_right",
    scale=(3, 12, MAIN_THICKNESS * 2),
    location=(X_POS, 12, MAIN_THICKNESS / 2),
)
base.cube_add(
    target=main,
    name="tab_left",
    scale=(3, 12, MAIN_THICKNESS * 2),
    location=(-X_POS, 12, MAIN_THICKNESS / 2),
)
base.cube_add(
    target=main,
    name="tab_top",
    scale=(23, 3.9, MAIN_THICKNESS * 2),
    location=(0, 20, MAIN_THICKNESS / 2),
)
