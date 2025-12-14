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
MAIN_DEPTH = 7.2

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
    location=(0, 0, -MAIN_THICKNESS / 2),
)

X = (MAIN_WIDTH - M4) / 2
Y = MAIN_HEIGHT / 2 - 17.0 - M4 / 2 - MAIN_THICKNESS
holes = [(X - 2.2 - MAIN_THICKNESS, Y), (-X + 10.0 + MAIN_THICKNESS / 2, Y)]
for i, (x, y) in enumerate(holes):
    base.cylinder_cut(
        target=main,
        radius=M4,
        location=(x, y, MAIN_DEPTH / 2),
        depth=10,
    )


# CPU
x = 29.0
y = 29.0
pos_x = (MAIN_WIDTH - x) / 2
pos_y = (MAIN_HEIGHT - y) / 2
base.cube_cut(
    target=main,
    scale=(x, y, 10),
    location=(pos_x - 34.3, -pos_y + 1.5, 0),
    rotation=(0, 0, math.radians(1.5)),
)

# SATA PWR
x = 9.5
y = 16.5
pos_x = (MAIN_WIDTH - x) / 2
pos_y = (MAIN_HEIGHT - y) / 2
base.cube_cut(
    target=main,
    scale=(x, y, 10),
    location=(-pos_x, -pos_y + 7.0, 0),
)

# SATA DATA
x = 7.5
y = 14.8
pos_x = (MAIN_WIDTH - x) / 2
pos_y = (MAIN_HEIGHT - y) / 2
base.cube_cut(
    target=main,
    scale=(x, y, 10),
    location=(pos_x - 1.4, -pos_y + 2.8, 0),
)

# BATTERY
x = 23.5
y = 6.2
pos_x = (MAIN_WIDTH - x) / 2
pos_y = (MAIN_HEIGHT - y) / 2
base.cube_cut(
    target=main,
    scale=(x, y, 10),
    location=(pos_x - 10.5, pos_y - 10.85, 0),
)


y = 20.25
pos_z = 18.85

# main2 -----------------------------------
main.location = (MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, MAIN_DEPTH / 2 - MAIN_THICKNESS)
pos = [
    (9.2, 1.4, 11.1),  # DC
    (15.0, 15.6, 16.2),  # USB
    (16.4, 34.2, 12.6),  # ETH
]
for i, (x, p, z) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(x, y, z),
        location=(x / 2 + p, -y / 2 + MAIN_THICKNESS, (z - pos_z) / 2),
    )

## main3 -----------------------------------
main.location = (-MAIN_WIDTH / 2, -MAIN_HEIGHT / 2, MAIN_DEPTH / 2 - MAIN_THICKNESS)
pos = [
    (15.2, 46.5, 6.2),  # HDMI
    (30.9, 9.7, 12.7),  # DVI
    (5.4, 1.7, 5.7),  # AUX
]
for i, (x, p, z) in enumerate(pos):
    base.cube_cut(
        target=main,
        scale=(x, y, z),
        location=(-x / 2 - p, y / 2, (z - pos_z) / 2),
    )

main.location = (0, 0, 0)
main.rotation_euler[1] = math.pi
