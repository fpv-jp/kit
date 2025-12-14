import bpy
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

# ネジ径定義
M2 = 1.25
M2_5 = 1.5
M3 = 1.75
M5 = 2.25

# プレート寸法
plate_width = 35
plate_height = 101.0 + 101.8 + M3 * 2
plate_depth = 2.8

# プレート作成
plate = base.cube_create(
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)

base.cube_cut(
    target=plate,
    scale=(plate_width - M3 * 10, plate_height - M3 * 8, plate_depth),
    location=(0, 0, 0),
)


TOP_X = 16.4
TOP_Y = 101.0

BOTTOM_X = 18.9
BOTTOM_Y = -101.8

# M3
holes2 = [
    (TOP_X, TOP_Y),
    (-TOP_X, TOP_Y),
    #    (26, 39.75),
    #    (-26, 39.75),
    #    (28.4, -25.15),
    #    (-28.4, -25.15),
    (BOTTOM_X, BOTTOM_Y),
    (-BOTTOM_X, BOTTOM_Y),
]

base.cube_add(
    target=plate,
    scale=(TOP_X * 2, M3 * 4, plate_depth),
    location=(0, TOP_Y, 0),
)
base.cube_add(
    target=plate,
    scale=(BOTTOM_X * 2, M3 * 4, plate_depth),
    location=(0, BOTTOM_Y, 0),
)
for i, (x, y) in enumerate(holes2):
    base.ring_add(
        target=plate,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, 0),
        depth=plate_depth,
    )

# M5
center_x = 28.0
center_y = 6.5
holes3 = [
    (center_x, center_y),
    (-center_x, center_y),
]
base.cube_add(
    target=plate,
    scale=(center_x * 2, M5 * 4, plate_depth),
    location=(0, center_y, 0),
)
for i, (x, y) in enumerate(holes3):
    base.ring_add(
        target=plate,
        outer_radius=M5 * 2,
        inner_radius=M5,
        location=(x, y, 0),
        depth=plate_depth,
    )


raspi_x = 24.5
raspi_y = 58.0
raspi_pos = 12.5

# M2.5
holes = [
    (raspi_x, raspi_pos + raspi_y),
    (-raspi_x, raspi_pos + raspi_y),
    (raspi_x, raspi_pos),
    (-raspi_x, raspi_pos),
]

base.cube_add(
    target=plate,
    scale=(raspi_x * 2, M2_5 * 4, plate_depth),
    location=(0, raspi_pos + raspi_y, 0),
)
base.cube_add(
    target=plate,
    scale=(raspi_x * 2, M2_5 * 4, plate_depth),
    location=(0, raspi_pos, 0),
)
for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=plate,
        outer_radius=M2_5 * 2,
        inner_radius=M2_5,
        location=(x, y, 0),
        depth=plate_depth,
    )
    base.ring_add(
        target=plate,
        outer_radius=M2_5 * 1.75,
        inner_radius=M2_5,
        location=(x, y, 2),
        depth=plate_depth * 1.2,
    )


# wifi ==============================================

x = 35
y = 35
h = 6

wifi = base.cube_create(
    scale=(x, y, h),
)
base.cube_cut(
    target=wifi,
    scale=(x - 3, y - 3, h),
)

# antenna
base.cube_cut(
    target=wifi,
    scale=(11, 11, h),
    location=(x / 2, -y / 2, 0),
)
base.cube_cut(
    target=wifi,
    scale=(11, 11, h),
    location=(-x / 2, -y / 2, 0),
)
# usb
base.cube_cut(
    target=wifi,
    scale=(22, 22, h),
    location=(0, x / 2, 0),
)

wifi.location = (0, -19, (h - plate_depth) / 2)
base.modifier_apply(obj=wifi, target=plate, name="wifi_union", operation="UNION")

# inductor ==============================================
h = 10
r = 9.5
inductor = base.cylinder_create(
    radius=r,
    depth=h,
)
base.cylinder_cut(
    target=inductor,
    radius=r - 1.5,
    depth=h,
    location=(0, 0, plate_depth),
)
base.cube_cut(
    target=inductor,
    scale=(r / 1.5, r, h),
    location=(0, -r / 2, 0),
)

inductor.location = (0, -45.0, (h - plate_depth) / 2)
base.modifier_apply(obj=inductor, target=plate, name="inductor_union", operation="UNION")

# ubec ==============================================

x = 25
y = 43
h = 12

ubec = base.cube_create(
    scale=(x, y, h),
)

base.cube_cut(
    target=ubec,
    scale=(x - 3, y - 3, h),
)

base.cube_cut(
    target=ubec,
    scale=(2, 4, h),
    location=(x / 2 - 2.5, -y / 2, 0),
)
base.cube_cut(
    target=ubec,
    scale=(2, 4, h),
    location=(-x / 2 + 2.5, -y / 2, 0),
)
base.cube_cut(
    target=ubec,
    scale=(18, 22, h),
    location=(0, x / 2, 0),
)

ubec.location = (0, -80, (h - plate_depth) / 2)
base.modifier_apply(obj=ubec, target=plate, name="ubec_union", operation="UNION")
