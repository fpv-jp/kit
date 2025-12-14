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

M3 = 1.75
M3_GAP = M3 * 2.1
M2 = 1.5

MAIN_THICKNESS = 1.5

# switch -----------------------------------

SWITCH_WIDTH = 29.0
SWITCH_HEIGHT = 16.5
SWITCH_THICKNESS = 5

switch = base.cube_create(
    scale=(SWITCH_WIDTH, SWITCH_HEIGHT, SWITCH_THICKNESS),
    location=(0, 0, 0),
)

SWITCH_WIDTH2 = 19.8
SWITCH_HEIGHT2 = 12.8
SWITCH_THICKNESS2 = 34.35

Z = SWITCH_THICKNESS2 / 2 - SWITCH_THICKNESS / 2

base.cube_add(
    target=switch,
    scale=(8 - MAIN_THICKNESS, SWITCH_HEIGHT2 + MAIN_THICKNESS, SWITCH_THICKNESS2),
    location=(0, 0, Z),
)
base.cube_cut(
    target=switch,
    scale=(SWITCH_WIDTH2, SWITCH_HEIGHT2, SWITCH_THICKNESS2 + 1),
    location=(0, 0, Z),
)

base.cylinder_cut(
    target=switch,
    radius=M3,
    depth=SWITCH_HEIGHT,
    location=(0, 0, 28.5),
    rotation=(math.pi / 2, 0, 0),
)

switch.location = (-30, 0, SWITCH_THICKNESS / 2)
# switch.location = (0, 30.25, -5.75)
# switch.rotation_euler = (math.pi / 2, 0, 0)

## bottom -----------------------------------

BOTTOM_WIDTH = 22
BOTTOM_HEIGHT = 115

CENTER_PLATE = 28

bottom = base.cube_create(
    scale=(BOTTOM_WIDTH + MAIN_THICKNESS, BOTTOM_HEIGHT, SWITCH_HEIGHT),
)

base.cube_cut(
    target=bottom,
    scale=(BOTTOM_WIDTH, BOTTOM_HEIGHT, SWITCH_HEIGHT),
    location=(0, MAIN_THICKNESS / 2, MAIN_THICKNESS),
)

CUT_WIDTH = BOTTOM_WIDTH + MAIN_THICKNESS + 1
CUT_HEIGHT = BOTTOM_HEIGHT / 2 - CENTER_PLATE
CUT_HEIGHT_Y = CUT_HEIGHT / 2 + CENTER_PLATE + MAIN_THICKNESS / 4
base.cube_cut(
    target=bottom,
    scale=(CUT_WIDTH, CUT_HEIGHT, SWITCH_HEIGHT),
    location=(0, CUT_HEIGHT_Y, MAIN_THICKNESS),
)
base.cube_cut(
    target=bottom,
    scale=(8 - MAIN_THICKNESS, CUT_HEIGHT, SWITCH_HEIGHT),
    location=(0, CUT_HEIGHT_Y, MAIN_THICKNESS / 2),
)

# center plate
base.cube_add(
    target=bottom,
    scale=(BOTTOM_WIDTH, MAIN_THICKNESS / 2, SWITCH_HEIGHT),
    location=(0, CENTER_PLATE, 0),
)

CUT_HEIGHT = BOTTOM_HEIGHT / 2 + CENTER_PLATE + MAIN_THICKNESS
CUT_HEIGHT_Y = CUT_HEIGHT / 2 - CENTER_PLATE - MAIN_THICKNESS / 2
CUT_THICKNESS = 4.5
base.cube_cut(
    target=bottom,
    scale=(CUT_WIDTH, CUT_HEIGHT, SWITCH_HEIGHT - CUT_THICKNESS),
    location=(0, -CUT_HEIGHT_Y, CUT_THICKNESS),
)

base.punch_holes(
    target=bottom,
    radius=M3,
    depth=BOTTOM_WIDTH + 1,
    holes=[
        (0, CENTER_PLATE + M3_GAP),
        (BOTTOM_WIDTH / 2 - M3_GAP, -BOTTOM_HEIGHT / 2 + M3_GAP),
    ],
)

bottom.location = (0, 0, SWITCH_HEIGHT / 2)

## top -----------------------------------

TOP_WIDTH = BOTTOM_WIDTH
TOP_HEIGHT = BOTTOM_HEIGHT

top = base.cube_create(
    scale=(TOP_WIDTH + MAIN_THICKNESS * 2, TOP_HEIGHT + MAIN_THICKNESS / 2, SWITCH_HEIGHT),
    location=(0, -MAIN_THICKNESS / 4, 0),
)
base.cube_cut(
    target=top,
    scale=(TOP_WIDTH, TOP_HEIGHT, SWITCH_HEIGHT),
    location=(0, MAIN_THICKNESS / 2, MAIN_THICKNESS),
)
CUT_WIDTH = TOP_WIDTH + MAIN_THICKNESS + 1
CUT_HEIGHT = TOP_HEIGHT / 2 - CENTER_PLATE
CUT_HEIGHT_Y = CUT_HEIGHT / 2 + CENTER_PLATE + MAIN_THICKNESS / 4
base.cube_cut(
    target=top,
    scale=(8 - MAIN_THICKNESS, CUT_HEIGHT, SWITCH_HEIGHT),
    location=(0, CUT_HEIGHT_Y, MAIN_THICKNESS / 2),
)

# center plate
base.cube_add(
    target=top,
    scale=(TOP_WIDTH, MAIN_THICKNESS / 2, SWITCH_HEIGHT),
    location=(0, CENTER_PLATE, 0),
)

base.punch_holes(
    target=top,
    radius=M3,
    depth=TOP_WIDTH + 1,
    holes=[
        (0, CENTER_PLATE + M3_GAP),
        (-TOP_WIDTH / 2 + M3_GAP, -TOP_HEIGHT / 2 + M3_GAP),
    ],
)

base.cube_cut(
    target=top,
    scale=(TOP_WIDTH + MAIN_THICKNESS + 3, TOP_HEIGHT + 3, MAIN_THICKNESS),
    location=(0, 0, SWITCH_HEIGHT / 2 - MAIN_THICKNESS / 2),
)

CUT_WIDTH = TOP_WIDTH + MAIN_THICKNESS
CUT_HEIGHT = TOP_HEIGHT / 2 + CENTER_PLATE + MAIN_THICKNESS / 4
CUT_HEIGHT_Y = -CUT_HEIGHT / 2 + CENTER_PLATE + MAIN_THICKNESS / 4
base.cube_cut(
    target=top,
    scale=(CUT_WIDTH, CUT_HEIGHT, SWITCH_HEIGHT),
    location=(0, CUT_HEIGHT_Y, SWITCH_HEIGHT - CUT_THICKNESS - MAIN_THICKNESS * 1.5),
)

base.cube_cut(
    target=top,
    scale=(TOP_WIDTH + MAIN_THICKNESS + 3, 3, 6),
    location=(10, 34, 4),
)

base.cube_cut(
    target=top,
    scale=(TOP_WIDTH + MAIN_THICKNESS + 3, 3, 6),
    location=(0, 45, 4),
)

base.cube_cut(
    target=top,
    scale=(4, 3, 8),
    location=(7, CENTER_PLATE, 0),
)

base.cube_cut(
    target=top,
    scale=(4, 3, 8),
    location=(-7, CENTER_PLATE, 0),
)

base.cylinder_cut(
    target=top,
    radius=M3,
    location=(5.5, -TOP_HEIGHT / 2, -2.5),
    depth=MAIN_THICKNESS + 1,
    rotation=(math.pi / 2, 0, 0),
)

base.cylinder_cut(
    target=top,
    radius=M3,
    location=(-5.5, -TOP_HEIGHT / 2, -2.5),
    depth=MAIN_THICKNESS + 1,
    rotation=(math.pi / 2, 0, 0),
)


top.location = (TOP_WIDTH + 4, 0, SWITCH_HEIGHT / 2)
