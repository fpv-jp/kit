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

# CM4のサイズに合わせた寸法
CM4_WIDTH = 55
CM4_HEIGHT = 40
MARGIN = 5
PLATE_WIDTH = CM4_WIDTH + MARGIN
PLATE_HEIGHT = CM4_HEIGHT + MARGIN
PLATE_THICKNESS = 1.5

# 板を作成
main_plate = base.cube_create(
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, PLATE_THICKNESS),
)

# 中央をくり抜く穴を作成
INNER_CUT_MARGIN = 14
inner_cutout_width = PLATE_WIDTH * 2 - INNER_CUT_MARGIN * 2
inner_cutout_height = PLATE_HEIGHT * 2 - INNER_CUT_MARGIN * 2

base.cube_cut(
    target=main_plate,
    scale=(inner_cutout_width / 2, inner_cutout_height / 2, PLATE_THICKNESS * 2),
    location=(0, 0, PLATE_THICKNESS / 2),
)

## ----------------------------------------------------------------------------------------------------------------
## ----------------------------------------------------------------------------------------------------------------
## ----------------------------------------------------------------------------------------------------------------

# 三角形の穴を作成
x1 = 28.25
y1 = 20.75

triangle_positions = [
    (x1, y1, [(-3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 180),
    (-x1, y1, [(3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 180),
    (x1, -y1, [(3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 0),
    (-x1, -y1, [(-3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 0),
]

for i, (x, y, vertices, rotation) in enumerate(triangle_positions):
    base.triangle_cut(
        target=main_plate,
        vertices=vertices,
        depth=PLATE_THICKNESS + 2,
        location=(x, y, 0),
        rotation=(0, 0, math.radians(rotation)),
    )

x1 = 22
y1 = 14

triangle_positions = [
    (x1, y1, [(-2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 180),
    (-x1, y1, [(2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 180),
    (x1, -y1, [(2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 0),
    (-x1, -y1, [(-2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 0),
]

for i, (x, y, vertices, rotation) in enumerate(triangle_positions):
    base.triangle_add(
        target=main_plate,
        vertices=vertices,
        depth=PLATE_THICKNESS,
        location=(x, y, PLATE_THICKNESS / 2),
        rotation=(0, 0, math.radians(rotation)),
    )

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

CM4_PIN_OFFSET_X = 23.5
CM4_PIN_OFFSET_Y = 16.5

pins = [
    (-CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
    (CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
    (-CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
    (CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
]

PIN_HEIGHT = 8.5
base.mount_pins(
    target=main_plate,
    radius=2.5,
    depth=PIN_HEIGHT,
    height_pos=(PIN_HEIGHT) / 2 + PLATE_THICKNESS,
    pins=pins,
)

PIN_HEIGHT = 11
base.mount_pins(
    target=main_plate,
    radius=0.85,
    depth=PIN_HEIGHT,
    height_pos=(PIN_HEIGHT) / 2 + PLATE_THICKNESS,
    pins=pins,
)

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

CLAW_X = 2.5
CLAW_Y = 7.0
CLAW_Z = 14.95
scale = (CLAW_X, CLAW_Y, CLAW_Z)

gap_x = 0.75

CLAW_POS_X = (CM4_WIDTH + CLAW_X) / 2 + gap_x
CLAW_POS_Y = 15.5
CLAW_POS_Z = (CLAW_Z + PLATE_THICKNESS) / 2

base.plate_attach(
    target=main_plate,
    plates=[
        (scale, (CLAW_POS_X, CLAW_POS_Y, CLAW_POS_Z), None),
        (scale, (-CLAW_POS_X, CLAW_POS_Y, CLAW_POS_Z), None),
        (scale, (CLAW_POS_X, -CLAW_POS_Y, CLAW_POS_Z), None),
        (scale, (-CLAW_POS_X, -CLAW_POS_Y, CLAW_POS_Z), None),
    ],
)

x1 = 26.51
y1 = CLAW_POS_Y - CLAW_Y / 2
vertices = [(6.0, 0, 0), (0, 6.0, 0), (0, 0, 0)]

R45 = math.radians(45)
R90 = math.radians(90)
R180 = math.radians(180)

triangle_positions_ = [
    (x1, y1 + CLAW_Y, (R90, R45, 0)),
    (-x1, y1, (R90, R45, R180)),
    (x1, -y1, (R90, R45, 0)),
    (-x1, -y1 - CLAW_Y, (R90, R45, R180)),
]

for i, (x, y, rotation) in enumerate(triangle_positions_):
    base.triangle_add(
        target=main_plate,
        vertices=vertices,
        depth=CLAW_Y,
        location=(x, y, CLAW_Z + PLATE_THICKNESS),
        rotation=rotation,
    )

x1 = 27.6 + gap_x

vertices = [(2.5, 0, 0), (0, 2.5, 0), (0, 0, 0)]

triangle_positions_ = [
    (x1, y1, (R90, 0, R180)),
    (-x1, y1 + CLAW_Y, (R90, 0, 0)),
    (x1, -y1 - CLAW_Y, (R90, 0, R180)),
    (-x1, -y1, (R90, 0, 0)),
]

for i, (x, y, rotation) in enumerate(triangle_positions_):
    base.triangle_add(
        target=main_plate,
        vertices=vertices,
        depth=CLAW_Y,
        location=(x, y, PLATE_THICKNESS),
        rotation=rotation,
    )

base.cube_cut(
    target=main_plate,
    scale=(CM4_WIDTH + 10, CM4_HEIGHT + 10, 6),
    location=(0, 0, CLAW_Z + 6),
)

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

PLATE_WIDTH = 35
PLATE_HEIGHT = 40
PLATE_THICKNESS = 1.5

main = base.cube_create(scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS), location=(0, 0, 0))

ARM_HEIGHT = 4.5
ARM_HEIGHT2 = ARM_HEIGHT / 2 + PLATE_THICKNESS / 2

base.cube_add(
    target=main,
    scale=(PLATE_WIDTH, PLATE_WIDTH, ARM_HEIGHT),
    location=(0, 0, ARM_HEIGHT / 2),
)

base.cube_cut(
    target=main,
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2 + .1,
        PLATE_WIDTH - PLATE_THICKNESS * 2 + .1,
        ARM_HEIGHT,
    ),
    location=(0, 0, ARM_HEIGHT2),
)

base.cube_cut(target=main, scale=(24, 29, PLATE_THICKNESS), location=(0, -2, 0))

base.cube_cut(
    target=main,
    scale=(18, 18, ARM_HEIGHT),
    location=(PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
base.cube_cut(
    target=main,
    scale=(18, 18, ARM_HEIGHT),
    location=(-PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
base.cube_cut(
    target=main,
    scale=(22, 22, ARM_HEIGHT),
    location=(0, -PLATE_WIDTH / 2, ARM_HEIGHT2),
)

main.location = (0, 0, PLATE_THICKNESS)
base.join(main, main_plate)

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

M3 = 1.8

holes = [
    (-14, -20),
    (14, -20),
    (-14, 20),
    (14, 20),
]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, PLATE_THICKNESS),
        depth=PLATE_THICKNESS,
    )
