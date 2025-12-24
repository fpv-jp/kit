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

inner_box_size = 19.9
frame_thickness = 1.5
frame_depth = 7.5

frame = base.cube_create(
    scale=(
        inner_box_size + frame_thickness,
        inner_box_size + frame_thickness,
        frame_depth,
    ),
)

base.cube_cut(
    target=frame,
    scale=(inner_box_size, inner_box_size, frame_depth),
    location=(0, 0, frame_thickness),
)
base.cube_cut(
    target=frame,
    scale=(14.0, 14.0, 14.0),
)
frame.location = (0, 0, (frame_depth + frame_thickness) / 2)

########################################

M3 = 1.75
z = frame_thickness

########################################

PITCH = 18.9
y = 10.0

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
y = -9.0

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

PITCH = 17.0
y = -5.0

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

depth_antenna = 10
radius_antenn = 7.5

antenna = base.cylinder_create(
    radius=radius_antenn,
    depth=depth_antenna,
)

base.cube_add(
    target=antenna,
    scale=(radius_antenn * 2, radius_antenn + 2, frame_thickness + 1),
    location=(0, -4, -4),
    rotation=(math.pi / 6, 0, 0),
)

base.cylinder_cut(
    target=antenna,
    radius=radius_antenn - frame_thickness,
    location=(0, 0, -frame_thickness),
    depth=depth_antenna - frame_thickness,
)

base.cylinder_cut(
    target=antenna,
    radius=3.25,
    depth=depth_antenna + 1,
)

antenna.location = (0, 21.46, 2.46)
antenna.rotation_euler = (-math.pi / 6, 0, 0)

base.modifier_apply(obj=antenna, target=frame)

base.cube_cut(
    target=frame,
    scale=(80, 80, 10),
    location=(0, 0, -5 + frame_thickness / 2),
)

##########################################

erls = 5
erls_depth = 7.5

x = 13.5
y = 17.5

erls1 = base.cube_create(
    scale=(erls + frame_thickness * 2, erls + frame_thickness * 2, erls_depth),
)
base.cube_cut(
    target=erls1,
    scale=(erls, erls, erls_depth + 0.5),
)
base.cube_cut(
    target=erls1,
    scale=(erls, erls, erls_depth),
    location=(frame_thickness, 0, frame_thickness),
)

# -----------

erls2 = base.cube_create(
    scale=(erls + frame_thickness * 2, erls + frame_thickness * 2, erls_depth),
)
base.cube_cut(
    target=erls2,
    scale=(erls, erls, erls_depth + 0.5),
)
base.cube_cut(
    target=erls2,
    scale=(erls, erls, erls_depth),
    location=(-frame_thickness, 0, frame_thickness),
)

erls1.location = (x, y, (erls_depth + frame_thickness) / 2)
erls2.location = (-x, y, (erls_depth + frame_thickness) / 2)

base.modifier_apply(obj=erls1, target=frame)
base.modifier_apply(obj=erls2, target=frame)

##########################################

base.cube_cut(
    target=frame,
    scale=(9.0, 8.0, 10),
    location=(0, -9.0, 5),
)
