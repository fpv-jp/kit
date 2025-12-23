import bpy
import sys
import types
import math

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

# 初期化
base.init()

inner_box_size = 20.0
clearance = 0.2
frame_thickness = 1.5
frame_depth = 7

inner_width = inner_box_size + clearance
inner_height = inner_box_size + clearance
frame_width = inner_width + frame_thickness * 2
frame_height = inner_height + frame_thickness * 2
frame_z = frame_depth / 2

frame = base.cube_create(
    scale=(
        inner_width + frame_thickness * 2,
        inner_height + frame_thickness * 2,
        frame_depth + frame_thickness,
    ),
    location=(0, 0, 0),
)

base.cube_cut(
    target=frame,
    scale=(inner_width, inner_height, frame_depth),
    location=(0, 0, frame_thickness / 2),
)
base.cube_cut(
    target=frame,
    scale=(14.0, 14.0, frame_thickness + 2),
    location=(0, 0, frame_thickness / 2 - frame_depth / 2),
)
base.cube_cut(target=frame, scale=(9.1, 9.0, 9), location=(0, -10.5, 0))


M3 = 1.75
z = -frame_depth / 2

########################################

PITCH = 18.9
y = 10

base.cube_add(
    target=frame,
    scale=(PITCH * 2, M3 * 4, frame_thickness),
    location=(0, y, z),
)

holes = [(-PITCH, y), (PITCH, y)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=frame,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, z),
        depth=frame_thickness,
    )

########################################

PITCH = 27.0
y = -9

base.cube_add(
    target=frame,
    scale=(PITCH * 2, M3 * 4, frame_thickness),
    location=(0, y, z),
)

holes = [(-PITCH, y), (PITCH, y)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=frame,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, z),
        depth=frame_thickness,
    )

#########################################

depth_antenna = 10
radius_antenn1 = 7.5
radius_antenn2 = 3.25

PITCH = 17.0
y = -5

holes = [(-PITCH, y), (PITCH, y)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=frame,
        outer_radius=6.5,
        inner_radius=3.25,
        location=(x, y, z),
        depth=frame_thickness,
    )

#########################################

antenna = base.cylinder_create(
    radius=radius_antenn1,
    depth=depth_antenna,
)

base.cube_add(
    target=antenna,
    scale=(radius_antenn1 * 2, radius_antenn1 + 2, frame_thickness + 1),
    location=(0, -4, -4),
    rotation=(math.pi / 6, 0, 0),
)

base.cylinder_cut(
    target=antenna,
    radius=radius_antenn1 - frame_thickness,
    location=(0, 0, -frame_thickness),
    depth=depth_antenna - frame_thickness,
)

base.cylinder_cut(
    target=antenna,
    radius=radius_antenn2,
    depth=depth_antenna + 1,
)

antenna.location = (0, 22.6, -2)
antenna.rotation_euler = (-math.pi / 6, 0, 0)

base.modifier_apply(obj=antenna, target=frame)

base.cube_cut(
    target=frame,
    scale=(100, 100, 10),
    location=(0, 0, -9.25),
)

#########################################

erls = 5

x = 11
y = 17
z = -3

base.frame_add(
    target=frame,
    inner=erls,
    thickness=frame_thickness,
    location=(x, y, z - 0.5),
)
base.frame_add(
    target=frame,
    inner=erls,
    thickness=frame_thickness,
    location=(-x, y, z - 0.5),
)

#########################################
