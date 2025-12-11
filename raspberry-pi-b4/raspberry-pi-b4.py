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

raspi_x = 24.5
raspi_y = 13.5

# M2.5
holes = [
    (raspi_x, raspi_y + 58.0),
    (-raspi_x, raspi_y + 58.0),
    (raspi_x, raspi_y),
    (-raspi_x, raspi_y),
]

base.cube_add(
    target=plate,
    scale=(raspi_x * 2, M2_5 * 4, plate_depth),
    location=(0, raspi_y + 58.0, 0),
)
base.cube_add(
    target=plate,
    scale=(raspi_x * 2, M2_5 * 4, plate_depth),
    location=(0, raspi_y, 0),
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
        location=(x, y, 1),
        depth=plate_depth * 1.2,
    )


# M3
holes2 = [
    (16.4, 101.0),
    (-16.4, 101.0),
    #    (26, 39.75),
    #    (-26, 39.75),
    #    (28.4, -25.15),
    #    (-28.4, -25.15),
    (18.9, -101.8),
    (-18.9, -101.8),
]

base.cube_add(
    target=plate,
    scale=(16.4 * 2, M3 * 4, plate_depth),
    location=(0, 101.0, 0),
)
base.cube_add(
    target=plate,
    scale=(18.9 * 2, M3 * 4, plate_depth),
    location=(0, -101.8, 0),
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
center_y = 6.5
holes3 = [
    (28.0, center_y),
    (-28.0, center_y),
]
base.cube_add(
    target=plate,
    scale=(28.0 * 2, M5 * 4, plate_depth),
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

# ==============================================

x = 35
y = 35
h = 5

wifi = base.cube_create(
    scale=(x, y, h),
)
base.cube_cut(
    target=wifi,
    scale=(x - 3, y - 3, h),
)

base.cube_cut(
    target=wifi,
    scale=(18, 18, h),
    location=(x / 2, -y / 2, 0),
)
base.cube_cut(
    target=wifi,
    scale=(18, 18, h),
    location=(-x / 2, -y / 2, 0),
)
base.cube_cut(
    target=wifi,
    scale=(22, 22, h),
    location=(0, x / 2, 0),
)
base.cube_add(
    target=wifi,
    scale=(x, y, plate_depth),
    location=(0, 0, (plate_depth - h) / 2),
)
base.cube_cut(
    target=wifi,
    scale=(x - 12, y - 12, plate_depth + 1),
    location=(0, 0, (plate_depth - h) / 2),
)

wifi.location = (0, -25, (h - plate_depth) / 2)
base.modifier_apply(obj=wifi, target=plate, name="wifi_union", operation="UNION")

## ==============================================

x = 25
y = 43
h = 11

ubec = base.cube_create(
    scale=(x, y, h),
)

base.cube_cut(
    target=ubec,
    scale=(x - 3, y - 3, h),
)

base.cube_cut(
    target=ubec,
    scale=(10, 10, h),
    location=(x / 2, -y / 2, 0),
)
base.cube_cut(
    target=ubec,
    scale=(10, 10, h),
    location=(-x / 2, -y / 2, 0),
)
base.cube_cut(
    target=ubec,
    scale=(22, 22, h),
    location=(0, x / 2, 0),
)
base.cube_add(
    target=ubec,
    scale=(x, y, plate_depth),
    location=(0, 0, (plate_depth - h) / 2),
)
base.cube_cut(
    target=ubec,
    scale=(x - 12, y - 12, plate_depth + 1),
    location=(0, 0, (plate_depth - h) / 2),
)

ubec.location = (0, -80, (h - plate_depth) / 2)
base.modifier_apply(obj=ubec, target=plate, name="ubec_union", operation="UNION")
