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
MAIN_WIDTH = 100.15
MAIN_HEIGHT = 74.25
MAIN_DEPTH = 6.0
MAIN_THICKNESS = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH + MAIN_THICKNESS),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 0.1, MAIN_HEIGHT - 0.1, MAIN_DEPTH),
    location=(0, 0, MAIN_THICKNESS / 2),
)

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2

M3 = 1.7

P_X = -BASE_X + 3.5
P_Y = BASE_Y - 3.6

G_X = 93.15
G_Y = 49.0
G_X2 = 58.5

base.punch_holes(
    target=main,
    radius=M3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=[
        (P_X, P_Y),
        (P_X + G_X, P_Y),
        (P_X, P_Y - G_Y),
        (P_X + G_X, P_Y - G_Y),
        (P_X + G_X2, P_Y),
    ],
)

M3 = 1.6

P_X = -BASE_X + 8.3 + M3
P_X2 = -BASE_X + 62.2 + M3
P_X3 = BASE_X - 37.3 - M3

P_Y = BASE_Y - 17.8 - M3
P_Y2 = BASE_Y - 50.8 - M3
P_Y3 = BASE_Y - 37.8 - M3

base.punch_holes(
    target=main,
    radius=M3,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=[
        (P_X, P_Y),
        (P_X, P_Y2),
        (P_X2, P_Y),
        (P_X2, P_Y2),
        (P_X3, P_Y3),
    ],
)

################################################

def cube_cut2(scale, pos):
    y = BASE_Y - scale[1] / 2 + 2
    z = (-scale[2] + MAIN_DEPTH + MAIN_THICKNESS) / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(pos, y, z),
    )

cube_cut2(scale=(11.0, 3.5, 1.5), pos=BASE_X - 14.3)  # SD
