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

PLATE_WIDTH = 35
PLATE_HEIGHT = 40
PLATE_THICKNESS = 1.5

main = base.cube_create(
    name="main", scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS), location=(0, 0, 0)
)

ARM_HEIGHT = 4.5
ARM_HEIGHT2 = ARM_HEIGHT / 2 + PLATE_THICKNESS / 2

base.cube_add(
    target=main,
    name="arm_outer",
    scale=(PLATE_WIDTH, PLATE_WIDTH, ARM_HEIGHT),
    location=(0, 0, ARM_HEIGHT/2),
)

base.cube_cut(
    target=main,
    name="arm_inner_1",
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        ARM_HEIGHT,
    ),
    location=(0, 0, ARM_HEIGHT2)
)

base.cube_cut(target=main, name="arm_inner_2", scale=(20, 26, ARM_HEIGHT), location=(0, -3, 0))

base.cube_cut(
    target=main,
    name="arm_inner_corner_1",
    scale=(18, 18, ARM_HEIGHT),
    location=(PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
base.cube_cut(
    target=main,
    name="arm_inner_corner_2",
    scale=(18, 18, ARM_HEIGHT),
    location=(-PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
base.cube_cut(
    target=main,
    name="arm_inner_back",
    scale=(22, 22, ARM_HEIGHT),
    location=(0, -PLATE_WIDTH / 2, ARM_HEIGHT2),
)

M3 = 1.85

holes = [
    (-14, -20),
    (14, -20),
    (-14, 20),
    (14, 20),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_add(
        target=main,
        name=f"ring_outer_{i}",
        radius=M3 * 2,
        depth=PLATE_THICKNESS,
        location=(x, y, 0),
    )
    base.cylinder_cut(
        target=main,
        name=f"ring_inner_{i}",
        radius=M3,
        depth=PLATE_THICKNESS + 1,
        location=(x, y, 0),
    )
