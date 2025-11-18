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

plate_width = 63.5
plate_height = 172
plate_depth = 2

gap_depth = plate_depth / 2

main = base.cube_create(name="main", scale=(plate_width, plate_height, plate_depth))

M2 = 1.25
M2_5 = 1.5
M3 = 1.75
M48 = 48.25

prop_x = 57.0
prop_y = 48.0

holes = [
    (prop_x, prop_y),
    (prop_x, -prop_y),
    (-prop_x, prop_y),
    (-prop_x, -prop_y),
]

base.punch_holes(
    target=main,
    name="cylinder_large",
    radius=M48,
    depth=plate_depth + 1,
    holes=holes,
    height_pos=0,
    vertices=128,
)

prop_x1 = 13.75
prop_y1 = 83.0

prop_x2 = 28.75
prop_y2 = 0.0

prop_x3 = 7.0
prop_y3 = 43.5

holes = [
    (prop_x1, prop_y1),
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
    (-prop_x1, -prop_y1),
    (prop_x2, prop_y2),
    (-prop_x2, prop_y2),
    (prop_x3, prop_y3),
    (-prop_x3, prop_y3),
]

base.punch_holes(
    target=main,
    name="cylinder_small",
    radius=M2_5,
    depth=plate_depth + 1,
    holes=holes,
    height_pos=0,
)

base.cube_cut(
    target=main,
    name="cube_cut_center",
    scale=(32, 32, plate_depth + 1),
    location=(0, 5, 0),
    rotation=(0, 0, math.radians(45)),
)

prop_x1 = 32.5
prop_y1 = 77.0

holes = [
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
]

for i, (x, y) in enumerate(holes):
    base.triangle_cut(
        target=main,
        name=f"triangle_cut_1_{i}",
        vertices=[(0, x, 0), (-9, 0, 0), (9, 0, 0)],
        depth=plate_depth + 1,
        location=(0, y, -plate_depth / 1.5),
    )

vertices = [(0, -20, 0), (-11, 11, 0), (0, 0, 0)]

base.triangle_cut(
    target=main,
    name="triangle_cut_2_left",
    vertices=vertices,
    depth=plate_depth + 1,
    location=(-2.5, -23, -plate_depth / 1.5),
)

base.triangle_cut(
    target=main,
    name="triangle_cut_2_right",
    vertices=vertices,
    depth=plate_depth + 1,
    location=(2.5, -23, -plate_depth / 1.5),
    rotation=(0, math.radians(180), 0),
)

prop_x1 = 21.5
prop_y1 = 86.0

holes = [
    (prop_x1, prop_y1),
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
    (-prop_x1, -prop_y1),
]

for i, (x, y) in enumerate(holes):
    base.cube_cut(
        target=main,
        name=f"cube_cut_corner_{i}",
        scale=(10, 10, plate_depth + 1),
        location=(x, y, 0),
        rotation=(0, 0, math.radians(45)),
    )

base.cylinder_cut(
    target=main,
    name="cylinder_tail",
    radius=3.0,
    depth=plate_depth + 1,
    location=(0, -plate_height / 2 + 1, 0),
)
