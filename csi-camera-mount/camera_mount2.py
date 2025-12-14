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

base.init()

MAIN_WIDTH = 25
MAIN_HEIGHT = 16.5
MAIN_DEPTH = 1.5

main = base.cube_create(
    scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_DEPTH),
)

base.cube_cut(
    target=main,
    scale=(MAIN_WIDTH - 7, MAIN_HEIGHT - 7, MAIN_DEPTH + 1),
)


M2 = 1.2
X = 10.5
Y = 6.25

base.punch_holes(
    target=main,
    radius=M2,
    depth=MAIN_DEPTH + 1,
    holes=[(X, Y), (X, -Y), (-X, Y), (-X, -Y)],
)

#############################################################

PIN_HEIGHT = 33.5
ARM_DEPTH = 5

left = base.cube_create(
    scale=(MAIN_DEPTH, PIN_HEIGHT, ARM_DEPTH),
)

Y = PIN_HEIGHT / 2 - M2 * 1.75

base.punch_holes(
    target=left,
    radius=M2,
    depth=MAIN_DEPTH + 1,
    holes=[(0, Y), (0, -Y)],
    rotation=(0, math.pi / 2, 0),
)

SIDE = (MAIN_WIDTH + MAIN_DEPTH) / 2

left.location = (
    SIDE,
    4.75,
    (ARM_DEPTH - MAIN_DEPTH) / 2,
)

base.modifier_apply(obj=left, target=main, operation="UNION")

##############################################################

M3 = 1.75

PIN_WIDTH = 5
PIN_HEIGHT = 5.5

right = base.cube_create(
    scale=(MAIN_DEPTH, PIN_WIDTH, PIN_HEIGHT),
)

PIN = MAIN_DEPTH + 2

base.cylinder_add(
    target=right,
    radius=M3,
    depth=PIN,
    location=(-PIN / 2, 0, 0),
    rotation=(0, math.pi / 2, 0),
)

right.location = (
    -SIDE,
    3.75,
    (PIN_HEIGHT - MAIN_DEPTH) / 2,
)

base.modifier_apply(obj=right, target=main, operation="UNION")
