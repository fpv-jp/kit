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

plate_width = 23.5
plate_height = 23.5
plate_depth = 8

main = base.cube_create(
    name="main",
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)


############################################################

cube_width = 20
cube_height = 20

M2 = 1.25
M5 = 2.75

base.cylinder_add(
    target=main,
    name="Cylinder",
    radius=M5,
    depth=23.5,
    location=(0, 0, 5.75),
    rotation=(0, math.pi / 2, 0),
)

base.cube_add(
    target=main,
    name="CubeCut",
    scale=(23.5, M5 * 2, 5),
    location=(0, 0, 5.75 - M5),
    # rotation=(math.pi / 1.5, 0, 0),
)

base.cylinder_cut(
    target=main,
    name="Hole",
    radius=M2,
    depth=24,
    location=(0, 0, 5.75),
    rotation=(0, math.pi / 2, 0),
)

# =======================================

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(cube_width, cube_height, 14),
    location=(0, 0, 4.5),
)

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(10.9, 3.6, plate_depth),
    location=(2.0, 2.5, 0),
)

main.rotation_euler = (math.pi / 2.5, 0, 0)

base.cube_add(
    target=main,
    name="Cube",
    scale=(33, 18, 2),
    location=(0, 3, -11.41),
)

prop_x1 = 13.75
prop_y1 = 9.25
M3 = 1.75

holes = [
    (prop_x1, prop_y1),
    (-prop_x1, prop_y1),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=main,
        name="Cylinder",
        radius=M3,
        depth=2.5,
        location=(x, y, -11.41),
    )
