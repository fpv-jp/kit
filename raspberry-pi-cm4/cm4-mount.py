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
    name="main_plate",
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, PLATE_THICKNESS),
)

# 中央をくり抜く穴を作成
INNER_CUT_MARGIN = 14
inner_cutout_width = PLATE_WIDTH * 2 - INNER_CUT_MARGIN * 2
inner_cutout_height = PLATE_HEIGHT * 2 - INNER_CUT_MARGIN * 2

base.cube_cut(
    target=main_plate,
    name="inner_cutout",
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
        name=f"triangle_cut_{i}",
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
        name=f"triangle_add_{i}",
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

PIN_HEIGHT = 5
base.mount_pins(
    target=main_plate,
    radius=2.5,
    depth=PIN_HEIGHT,
    height_pos=(PIN_HEIGHT) / 2 + PLATE_THICKNESS,
    pins=pins,
)

PIN_HEIGHT = 8
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

# 突起物の寸法
PROTRUSION_HEIGHT = 21
PROTRUSION_HEIGHT2 = 10
PROTRUSION_DEPTH = 11.5

protrusion_z = PLATE_THICKNESS + PROTRUSION_DEPTH / 2
protrusion_x = PLATE_WIDTH / 2 - PLATE_THICKNESS / 2
protrusion_y = PLATE_HEIGHT / 2 - PLATE_THICKNESS / 2

base.plate_attach(
  target=main_plate,
  plates=[
      ((PLATE_THICKNESS, 4.5, PROTRUSION_DEPTH), (-protrusion_x, CM4_HEIGHT/2-4.5, protrusion_z), None),
      ((PLATE_THICKNESS, 3.5, PROTRUSION_DEPTH), (-protrusion_x, -PLATE_WIDTH / 3.5, protrusion_z), None),
      ((PLATE_THICKNESS, 3.5, PROTRUSION_DEPTH), (protrusion_x, PLATE_WIDTH / 3.5, protrusion_z), None),
      ((PLATE_THICKNESS, 3.5, PROTRUSION_DEPTH), (protrusion_x, -PLATE_WIDTH / 3.5, protrusion_z), None),
#      ((PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH), (0, -protrusion_y, protrusion_z), None),
#      ((PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH), (0, protrusion_y, protrusion_z), None),
  ],
)

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
## ホールサイズ
#M2_5_HOLE_RADIUS = 1.25 + 0.25
#M3_HOLE_RADIUS = 1.5 + 0.25

## 突起物の固定穴の位置
#hole_z_position = PLATE_THICKNESS + PROTRUSION_DEPTH - M2_5_HOLE_RADIUS * 2

#hole_rot_y = (0, math.radians(90), 0)
#hole_rot_x = (math.radians(90), 0, 0)

#hole_locations = [
#  (-protrusion_x, PLATE_WIDTH / 4.5, hole_z_position, hole_rot_y),
#  (-protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position, hole_rot_y),
#  (protrusion_x, PLATE_WIDTH / 4.5, hole_z_position, hole_rot_y),
#  (protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position, hole_rot_y),
#  (7, -protrusion_y, hole_z_position, hole_rot_x),
#  (-7, -protrusion_y, hole_z_position, hole_rot_x),
#  (7, protrusion_y, hole_z_position, hole_rot_x),
#  (-7, protrusion_y, hole_z_position, hole_rot_x),
#]

#for i, (x, y, z, rot) in enumerate(hole_locations):
#  base.cylinder_cut(
#      target=main_plate,
#      radius=M2_5_HOLE_RADIUS,
#      depth=PLATE_THICKNESS + 2,
#      location=(x, y, z),
#      rotation=rot,
#  )

# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------

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
    scale=(PLATE_WIDTH, PLATE_WIDTH, ARM_HEIGHT),
    location=(0, 0, ARM_HEIGHT / 2),
)

base.cube_cut(
    target=main,
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        ARM_HEIGHT,
    ),
    location=(0, 0, ARM_HEIGHT2),
)

base.cube_cut(target=main, scale=(20, 26, ARM_HEIGHT), location=(0, -3, 0))

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
