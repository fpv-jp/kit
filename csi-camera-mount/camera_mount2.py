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

plate_width = 25
plate_height = 16.5
plate_depth = 1.5

main = base.cube_create(
    name="main",
    scale=(plate_width, plate_height, plate_depth),
)

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(plate_width - 7, plate_height - 7, plate_depth + 1),
)


M2 = 1.2
M2_5 = 1.5
M3 = 1.75

holes = [
    (-10.5, -6.25),
    (10.5, -6.25),
    (-10.5, 6.25),
    (10.5, 6.25),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=main,
        name=f"Hole{i}",
        radius=M2,
        depth=plate_depth + 1,
        location=(x, y, 0),
    )

#############################################################

arm_width = 33.5
arm_height = 5

left = base.cube_create(
    name="Cube",
    scale=(plate_depth, arm_width, arm_height),
)

holes = [
    (0, arm_width / 2 - M2 * 1.75),
    (0, -(arm_width / 2 - M2 * 1.75)),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=left,
        name=f"Hole{i}",
        radius=M2,
        depth=plate_depth + 1,
        location=(x, y, 0),
        rotation=(0, math.pi / 2, 0),
    )

left.location = ((plate_width + plate_depth) / 2, 4.75, (arm_height - plate_depth) / 2)
base.modifier_apply(obj=left, target=main, name="left_union", operation="UNION")

#############################################################

arm_width = 5
arm_height = 5.5

right = base.cube_create(
    name="Cube",
    scale=(plate_depth, arm_width, arm_height),
)

pin_heght = plate_depth + 2

base.cylinder_add(
    target=right,
    name="Hole",
    radius=M3,
    depth=pin_heght,
    location=(-pin_heght/2 , 0, 0),
    rotation=(0, math.pi / 2, 0),
)
    
right.location = (-(plate_width + plate_depth) / 2, 3.75, (arm_height - plate_depth) / 2)
base.modifier_apply(obj=right, target=main, name="right_union", operation="UNION")
