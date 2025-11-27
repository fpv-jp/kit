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

PLATE_WIDTH = 28
PLATE_HEIGHT = 58

PLATE_THICKNESS = 4

main = base.cube_create(
    name="main", scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS), location=(0, 4, 0)
)

base.cube_clear(
    target=main,
    name="inner_cut",
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_HEIGHT - PLATE_THICKNESS * 2,
        PLATE_THICKNESS + 1,
    ),
    location=(0, 4, 0),
)

M3 = 1.8

holes = [
    (-14, -20),
    (14, -20),
    (-14, 20),
    (14, 20),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_add(target=main, name=f"ring_outer_{i}", radius=M3 * 2, depth=PLATE_THICKNESS, location=(x, y, 0))
    base.cylinder_clear(target=main, name=f"ring_inner_{i}", radius=M3, depth=PLATE_THICKNESS + 1, location=(x, y, 0))

base.triangle_add(target=main, name="triangle_left", vertices=[(-5, 0, 0), (0, 20, 0), (0, 0, 0)], depth=PLATE_THICKNESS, location=(10, -21, -PLATE_THICKNESS / 2))
base.triangle_add(target=main, name="triangle_right", vertices=[(0, 20, 0), (5, 0, 0), (0, 0, 0)], depth=PLATE_THICKNESS, location=(-10, -21, -PLATE_THICKNESS / 2))

main.rotation_euler[0] = math.radians(-75)
main.location[1] = -14
main.location[2] = 33

# # ----------------------------------------------------
# # ----------------------------------------------------
# # ----------------------------------------------------

BASE_PLATE_WIDTH = 40
BASE_PLATE_HEIGHT = 30
BASE_PLATE_THICKNESS = 2
CORNER_CUT_SIZE = 6.5

hexagonal_plate = base.cube_create(
    name="hexagonal_plate",
    scale=(BASE_PLATE_WIDTH, BASE_PLATE_HEIGHT, BASE_PLATE_THICKNESS),
    location=(0, 0, BASE_PLATE_THICKNESS / 2),
)

half_width = BASE_PLATE_WIDTH / 2
half_height = BASE_PLATE_HEIGHT / 2
cut_scale = (CORNER_CUT_SIZE * 2, CORNER_CUT_SIZE * 2, BASE_PLATE_THICKNESS * 2)
corner_positions = [
    (half_width, half_height),
    (-half_width, half_height),
    (half_width, -half_height),
    (-half_width, -half_height),
]

for i, (cx, cy) in enumerate(corner_positions):
    base.cube_clear(
        target=hexagonal_plate,
        name=f"corner_cut_{i}",
        scale=cut_scale,
        location=(cx, cy, BASE_PLATE_THICKNESS / 2),
        rotation=(0, 0, math.radians(45)),
    )

base.punch_holes(
    target=hexagonal_plate,
    name="mount_hole",
    radius=M3,
    depth=PLATE_THICKNESS + 1,
    height_pos=0,
    holes=[(15.25, 0), (-15.25, 0)],
)

base.join(target=main, obj=hexagonal_plate)
