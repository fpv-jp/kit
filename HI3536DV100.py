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

base.init()

# main -----------------------------------
MAIN_THICKNESS = 1.75
M4 = 2.0
M8 = 4.0

MAIN_WIDTH = 119.2
MAIN_HEIGHT = 47.2
MAIN_DEPTH = 10.8

main = base.cube_create(
    scale=(
        MAIN_WIDTH + MAIN_THICKNESS * 2,
        MAIN_HEIGHT + MAIN_THICKNESS * 2,
        MAIN_DEPTH + MAIN_THICKNESS,
    ),
)
base.corner_cut(
    target=main, width=MAIN_WIDTH, height=MAIN_HEIGHT, depth=MAIN_DEPTH, thickness=MAIN_THICKNESS
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
    location=(0, 0, MAIN_THICKNESS / 2),
)


base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 26, MAIN_HEIGHT - 18, MAIN_DEPTH + MAIN_THICKNESS),
    location=(3.5, 0, 0),
)

X = (MAIN_WIDTH - M4) / 2
Y = MAIN_HEIGHT / 2 - 17.0 - M4 / 2 - MAIN_THICKNESS
holes = [(X - 2.2 - MAIN_THICKNESS, Y), (-X + 10.0 + MAIN_THICKNESS / 2, Y)]
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=M8,
        inner_radius=M4,
        location=(x, y, -MAIN_DEPTH / 2 + 1.0),
        depth=MAIN_THICKNESS + 2.0,
    )

y = MAIN_THICKNESS * 3
pos_z = (MAIN_DEPTH - MAIN_THICKNESS) / 2 + 3.8

# main2 -----------------------------------
main.location = (MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, MAIN_DEPTH / 2 - MAIN_THICKNESS)
pos = [
    (9.2, 1.8, 11.1),  # DC
    (15.0, 15.6, 16.2),  # USB
    (16.4, 34.2, 12.6),  # ETH
]
for i, (x, p, z) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(x, y, MAIN_DEPTH),
        location=(x / 2 + p, 0, pos_z),
    )

# main3 -----------------------------------
main.location = (-MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, MAIN_DEPTH / 2 - MAIN_THICKNESS)
pos = [
    (15.2, 46.5, 6.2),  # HDMI
    (30.9, 9.7, 12.7),  # DVI
    (5.4, 1.7, 5.7),  # AUX
]
for i, (x, p, z) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(x, y, MAIN_DEPTH),
        location=(-x / 2 - p, 0, pos_z),
    )

main.location = (0, 0, 0)
