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

MAIN_WIDTH = 85.0
MAIN_HEIGHT = 56.0
MAIN_DEPTH = 8.0
MAIN_THICKNESS = 2.0

main = base.cube_create(
    scale=(MAIN_WIDTH + MAIN_THICKNESS, MAIN_HEIGHT + MAIN_THICKNESS, MAIN_DEPTH),
)

BASE_X = MAIN_WIDTH / 2
BASE_Y = MAIN_HEIGHT / 2

M2_7 = 1.35

scale = (M2_7 * 2, M2_7 * 2, MAIN_DEPTH)
rotation = (0.0, 0.0, 0.0)

base.plate_cutout(
    target=main,
    plates=[
        (scale, (BASE_X, BASE_Y, 0), rotation),
        (scale, (BASE_X, -BASE_Y, 0), rotation),
        (scale, (-BASE_X, BASE_Y, 0), rotation),
        (scale, (-BASE_X, -BASE_Y, 0), rotation),
    ],
)
c = [
    (BASE_X - M2_7, BASE_Y - M2_7),
    (BASE_X - M2_7, -BASE_Y + M2_7),
    (-BASE_X + M2_7, BASE_Y - M2_7),
    (-BASE_X + M2_7, -BASE_Y + M2_7),
]
base.mount_pins(
    target=main,
    radius=M2_7 * 1.74,
    depth=MAIN_DEPTH,
    pins=c,
)

H = -MAIN_THICKNESS / 2

base.punch_holes(
    target=main,
    radius=M2_7 + 0.1,
    depth=MAIN_DEPTH,
    height_pos=H,
    holes=c,
)

GAP = 0.2

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - M2_7 * 2, MAIN_HEIGHT + GAP, MAIN_DEPTH),
    location=(0, 0, H),
)
base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH + GAP, MAIN_HEIGHT - M2_7 * 2, MAIN_DEPTH),
    location=(0, 0, H),
)

################################################

P_X = -BASE_X + 3.5
P_Y = BASE_Y - 3.5

XX = 58.0
YY = 49.0

c = [
    (P_X, P_Y),
    (P_X, P_Y - YY),
    (P_X + XX, P_Y),
    (P_X + XX, P_Y - YY),
]
base.mount_pins(
    target=main,
    radius=M2_7 + 1,
    depth=MAIN_THICKNESS,
    pins=c,
    height_pos=MAIN_DEPTH / 2 - MAIN_THICKNESS,
)
base.punch_holes(
    target=main,
    radius=M2_7,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=c,
)
base.punch_holes(
    target=main,
    radius=2.0,
    depth=MAIN_DEPTH + MAIN_THICKNESS,
    holes=[
        (P_X, P_Y - 6.0),
        (P_X + XX, P_Y - YY + 6.0),
    ],
)

################################################

BORN = 7.5
base.cube_cut(
    target=main,
    scale=(XX - BORN, YY - BORN, MAIN_DEPTH),
    location=(-10.0, 0, MAIN_THICKNESS),
)

base.cube_cut(
    target=main,
    scale=(13.5, YY - BORN, MAIN_DEPTH),
    location=(29.5, 0, MAIN_THICKNESS),
)

###############################################

BASE_Z = (MAIN_DEPTH - MAIN_THICKNESS) / 2 - 3.5


def cube_cut(scale, Y):
    X = BASE_X - scale[0] / 2 + 1
    Z = BASE_Z - scale[2] / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(X, Y, Z),
    )


cube_cut(scale=(20, 16.2, 13.3), Y=BASE_Y - 10.2)
cube_cut(scale=(10, 13.2, 14.5), Y=BASE_Y - 29.1)
cube_cut(scale=(10, 13.2, 14.5), Y=BASE_Y - 47.0)


###############################################


def cube_cut2(scale, X):
    Y = BASE_Y - scale[1] / 2 + 1
    Z = BASE_Z - scale[2] / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(X, Y, Z),
    )


cube_cut2(scale=(9.1, 10.0, 13.3), X=-BASE_X + 11.2)
cube_cut2(scale=(7.1, 10.0, 14.5), X=-BASE_X + 25.8)
cube_cut2(scale=(7.1, 10.0, 14.5), X=-BASE_X + 39.2)


###############################################


def cube_cut3(scale, Y):
    X = -BASE_X + scale[0] / 2 - 1
    Z = BASE_Z - scale[2] / 2
    base.cube_cut(
        target=main,
        scale=scale,
        location=(X, Y, Z),
    )


cube_cut3(scale=(20, 2.0, 13.3), Y=BASE_Y - 13.3)
cube_cut3(scale=(20, 3.0, 13.3), Y=BASE_Y - 18.4)


def cube_cut4(scale, Y):
    X = -BASE_X + scale[0] / 2 - 1
    Z = BASE_Z - scale[2] / 2 + 3.5
    base.cube_cut(
        target=main,
        scale=scale,
        location=(X, Y, Z),
    )


cube_cut4(scale=(20, 12.0, 13.3), Y=0)


main.rotation_euler = (math.radians(180), 0, 0)

# main.location=(BASE_X, BASE_Y, 0)
