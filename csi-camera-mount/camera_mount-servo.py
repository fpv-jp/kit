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

plate_width = 16.4 * 2
plate_height = 25
plate_depth = 2.8

gap_depth = plate_depth / 2

main = base.cube_create(
    name="main",
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(plate_width - 12, plate_height - 12, plate_depth + 1),
    location=(0, 0, 0),
)

############################################################

side_width = 18.5
side_left_long = 17
side_height = 33.0

left = base.cube_create(
    name="left",
    scale=(side_left_long, side_width, plate_depth),
    location=(0, 0, 0),
)

base.cube_add(
    target=left,
    name="Cube",
    scale=(plate_depth, side_width, side_height),
    location=(side_left_long / 2, 0, (side_height - plate_depth) / 2),
)

base.triangle_add(
    target=left,
    name="Triangle",
    vertices=[(0, 20, 0), (-4, 0, 0), (0, 0, 0)],
    depth=side_width,
    location=(side_left_long / 2 - plate_depth / 2, side_width / 2, plate_depth / 2),
    rotation=(math.pi / 2, 0, 0),
)

p = plate_depth * 2
cut_z = 23
cut_y = 12.75

base.cube_cut(
    target=left,
    name="side_left_long",
    scale=(side_width, cut_y, cut_z),
    location=(side_width / 2, 0, side_height / 2 - plate_depth / 2),
)
base.cube_cut(
    target=left,
    name="side_left",
    scale=(side_width - p, cut_y, side_height),
    location=(plate_depth / 4, 0, 0),
)

M2 = 1.25
M5 = 2.75

servo_z_pos = 16
servo_z_pitch = 14.25

base.ring_add(
    target=left,
    name="m2_5_ring1",
    outer_radius=M5,
    inner_radius=M2,
    location=(side_left_long / 2, 0, servo_z_pos + servo_z_pitch),
    depth=plate_depth,
    rotation=(0, math.pi / 2, 0),
)
base.cylinder_cut(
    target=left,
    name="m2_5_ring2",
    radius=M2,
    location=(side_left_long / 2, 0, servo_z_pos - servo_z_pitch),
    depth=plate_depth,
    rotation=(0, math.pi / 2, 0),
)
 
left.location = (18, 0, 0)
base.modifier_apply(obj=left, target=main, name="left_union", operation="UNION")

#############################################################

side_width = M5 * 2
side_height = 22.5

right = base.cube_create(
    name="right",
    scale=(plate_depth, side_width, side_height),
    location=(0, 0, 0),
)

base.ring_add(
    target=right,
    name="m2_5_ring2",
    outer_radius=M5,
    inner_radius=2,
    location=(0, 0, side_height / 2),
    depth=plate_depth,
    rotation=(0, math.pi / 2, 0),
)

right.location = (-16.4, 0, side_height / 2 - plate_depth / 2)
base.modifier_apply(obj=right, target=main, name="right_union", operation="UNION")

#############################################################

M3 = 1.75
M7 = 3.75

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
