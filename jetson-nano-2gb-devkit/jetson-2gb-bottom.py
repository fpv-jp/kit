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
M3 = 1.75
M2 = 1.5

MAIN_WIDTH = 100.0
MAIN_HEIGHT = 80.0
MAIN_DEPTH = 3.5
MAIN_THICKNESS = 2.0

MAIN_SHRINK = 2.0

C = MAIN_THICKNESS + 1

main = base.cube_create(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS - MAIN_SHRINK, MAIN_DEPTH),
    location=(0, 0, 0),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH, MAIN_HEIGHT - MAIN_SHRINK, MAIN_DEPTH),
    location=(0, 0, -MAIN_THICKNESS),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 15, MAIN_HEIGHT - MAIN_SHRINK - 15, 10),
)


main.location = (0, MAIN_SHRINK, 0)

bottom = (MAIN_THICKNESS - MAIN_DEPTH) / 2

### mount -----------------------------------

x = MAIN_WIDTH / 2.0
y = MAIN_HEIGHT / 2.0

M = 1.25
# M7 = 3.75

holes = [
    (x - (3 + M), y - (1.6 + M)),
    (x - (3 + M), -y + (17.6 + M)),
    (-x + (8.2 + M), y - (1.6 + M)),
    (-x + (8.2 + M), -y + (17.6 + M)),
]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=4.75,
        inner_radius=M3,
        location=(x, y, (MAIN_DEPTH - MAIN_THICKNESS) / 2),
        depth=MAIN_THICKNESS,
    )

main.rotation_euler = (0, math.pi, 0)
