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

# main -----------------------------------
WALL = 2
MAIN_WIDTH = 76 + WALL
MAIN_HEIGHT = 78 + WALL
MAIN_THICKNESS = 15 + WALL

main = base.cube_create(
    name="main",
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS),
    location=(0, 0, 0),
)

base.cube_clear(
    target=main,
    name="cube_clear1",
    scale=(MAIN_WIDTH - WALL, MAIN_HEIGHT - WALL, MAIN_THICKNESS),
    location=(0, 0, WALL),
)

base.cube_clear(
    target=main,
    name="cube_clear2",
    scale=(MAIN_WIDTH - 25, MAIN_HEIGHT - 35, MAIN_THICKNESS),
    location=(0, 0, 0),
)

base.cube_clear(
    target=main,
    name="cube_clear3",
    scale=(MAIN_WIDTH + 25, 70, 10),
    location=(0, 0, 5),
)

X_POS = 18.6
Y_POS = 0.0
holes = [
    (-X_POS / 2, Y_POS),
    (X_POS / 2, Y_POS),
    (-X_POS * 1.5, Y_POS),
    (X_POS * 1.5, Y_POS),
]

for i, (x, y) in enumerate(holes):
    base.cube_clear(
        target=main,
        name="Cube",
        scale=(
            6.5,
            MAIN_HEIGHT + 4.6 * 2,
            MAIN_THICKNESS,
        ),
        location=(x, y, WALL),
    )

X_POS = 36 / 2
Y_POS = 55 / 2
M2_5 = 1.5

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]

for i, (x, y) in enumerate(holes):
    base.cylinder_clear(
        target=main,
        name=f"Hole{i}",
        radius=M2_5,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

# main2 -----------------------------------
M3 = 1.75
M2 = 1.5

MAIN2_WIDTH = 100
MAIN2_HEIGHT = 80
MAIN2_THICKNESS = 2.0

main2 = base.cube_create(
    name="main2",
    scale=(MAIN2_WIDTH, MAIN2_HEIGHT, MAIN2_THICKNESS),
    location=(0, 0, 0),
)

base.cube_clear(
    target=main2,
    name="CubeCut",
    scale=(MAIN2_WIDTH - 36, MAIN2_HEIGHT - 10, MAIN2_THICKNESS),
    location=(0, 0, 0),
)

x = MAIN2_WIDTH / 2
y = MAIN2_HEIGHT / 2

M = 1.25

holes2 = [
    (x - (2.6 + M), y - (2.6 + M)),
    (x - (2.6 + M), -y + (15.6 + M)),
    (-x + (8.6 + M), y - (2.6 + M)),
    (-x + (8.6 + M), -y + (15.6 + M)),
]

for i, (x, y) in enumerate(holes2):
    base.cylinder_clear(
        target=main2,
        name="Cylinder",
        radius=M3,
        depth=MAIN2_THICKNESS + 1,
        location=(x, y, 0),
    )

main2.rotation_euler = (0, 0, math.radians(90))
main2.location = (0, -3, -7.5)

base.join(main, main2)

# main3 -----------------------------------
