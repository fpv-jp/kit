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

M2 = 1.25
M3 = 1.75
M5 = 2.75
M7 = 3.75

plate_width = 16.4 * 2
plate_height = 25
plate_depth = 2.8

main = base.cube_create(
    name="main",
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)

base.cube_clear(
    target=main,
    name="CubeCut",
    scale=(plate_width - 12, plate_height - 12, plate_depth + 1),
    location=(0, 0, 0),
)

y = 14
base.cube_add(
    target=main,
    name="side_left",
    scale=(11.5, 17, y),
    location=(22.15, -2, (y - plate_depth) / 2),
)
base.cube_clear(
    target=main,
    name="side_left",
    scale=(11.5, 17, y),
    location=(22.15 - plate_depth, -2, (y - plate_depth) / 2 + plate_depth),
)
base.cube_clear(
    target=main,
    name="side_left",
    scale=(11.5, 17 - plate_depth * 3, y),
    location=(22.15, -2, (y - plate_depth) / 2),
)

#############################################################

side_width = 33.0
side_height = 18.5
side_height2 = 22.5

left = base.cube_create(
    name="Cube",
    scale=(plate_depth, side_width, side_height),
    location=(0, 0, 0),
)

cut_z = 12.5
cut_y = 23.0

base.cube_clear(
    target=left,
    name="side_left_long",
    scale=(side_width, cut_y, cut_z),
)

holes = [
    (0, 16),
    (0, -16),
]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=left,
        name=f"ring_{i}",
        outer_radius=M5,
        inner_radius=M2,
        location=(x, y, 0),
        depth=plate_depth,
        rotation=(0, math.pi / 2, 0),
    )

left.location = (26.5, -5.5, side_height2 - M5 / 2)
base.modifier_apply(obj=left, target=main, name="left_union", operation="UNION")

##############################################################

right = base.cube_create(
    name="right",
    scale=(plate_depth, M5 * 2, side_height2),
    location=(0, 0, 0),
)

base.ring_add(
    target=right,
    name="m2_5_ring2",
    outer_radius=M5,
    inner_radius=2,
    location=(0, 0, side_height2 / 2),
    depth=plate_depth,
    rotation=(0, math.pi / 2, 0),
)

right.location = (-16.4, 0, side_height2 / 2 - plate_depth / 2)
base.modifier_apply(obj=right, target=main, name="right_union", operation="UNION")

##############################################################

holes = [
    (16.4, 16.4 - 7.65),
    (-16.4, 16.4 - 7.65),
]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        name=f"ring_{i}",
        outer_radius=M7,
        inner_radius=M3,
        location=(x, y, 0),
        depth=plate_depth,
    )
