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

# plate_width = 23.5
# plate_height = 23.5
plate_depth = 7.5


cube_width = 20
cube_height = 20
cube_thickness = 1.75

main = base.cube_create(
    name="main",
    scale=(cube_width + cube_thickness * 2, cube_height + cube_thickness * 2, plate_depth),
    location=(0, 0, 0),
)

#############################################################

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(9.9, 3.7, plate_depth),
    location=(0, 8.15, 0),
)

#############################################################

M2 = 1.25
M5 = 2.75

base.cylinder_add(
    target=main,
    name="Cylinder",
    radius=M5,
    depth=23.5,
    location=(0, 0, 4.25),
    rotation=(0, math.pi / 2, 0),
)

base.cylinder_cut(
    target=main,
    name="Hole",
    radius=M2,
    depth=24,
    location=(0, 0, 4.25),
    rotation=(0, math.pi / 2, 0),
)

#############################################################
# cube_thickness = 2.0

base.cube_cut(
    target=main,
    name="CubeCut",
    scale=(cube_width, cube_height, plate_depth * 2),
    location=(0, 0, cube_thickness + plate_depth / 2),
)

z = -11.46

main.rotation_euler = (math.pi / 2.5, 0, 0)

base.cube_add(
    target=main,
    name="Cube",
    scale=(23.5, 22, cube_thickness),
    location=(0, 5.5, z),
)

M3 = 1.75
base.cylinder_cut(
    target=main,
    name="Cylinder",
    radius=M3,
    depth=2.5,
    location=(0, 10, z),
)

#############################################################

M2_5 = 1.75

x = 15.0
y = 20.0

holes2 = [
    (x, y),
    (-x, y),
]

main2 = base.cube_create(
    name="m3_mounting_protrusion", scale=(x * 2, M2_5 * 4, cube_thickness), location=(0, y, z)
)

for i, (x, y) in enumerate(holes2):
    base.ring_add(
        target=main2,
        name=f"m3_ring_{i}",
        outer_radius=M2_5 * 2,
        inner_radius=M2_5,
        location=(x, y, z),
        depth=cube_thickness,
    )

base.join(main, main2)
