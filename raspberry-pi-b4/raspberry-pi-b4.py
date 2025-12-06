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
    name="plate",
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)

base.cube_clear(
    target=plate,
    name="UpperCornerCut",
    scale=(plate_width - M3 * 8, plate_height - M3 * 8, plate_depth),
    location=(0, 0, 0),
)

# M2.5
holes = [
    (24.5, 65.0),
    (-24.5, 65.0),
    (24.5, 7),
    (-24.5, 7),
]
for i, (x, y) in enumerate(holes):
    base.cube_add(target=plate, name=f"m2_5_mounting_protrusion_{i}", scale=(x * 2, M2_5 * 4, plate_depth), location=(0, y, 0))
    base.ring_add(target=plate, name=f"m2_5_ring_{i}", outer_radius=M2_5 * 2, inner_radius=M2_5, location=(x, y, 0), depth=plate_depth)
    base.ring_add(target=plate, name=f"m2_5_mount_ring_{i}", outer_radius=M2_5 * 1.75, inner_radius=M2_5, location=(x, y, 1), depth=plate_depth * 1.5)


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
for i, (x, y) in enumerate(holes2):
    base.cube_add(target=plate, name=f"m3_mounting_protrusion_{i}", scale=(x * 2, M3 * 4, plate_depth), location=(0, y, 0))
    base.ring_add(target=plate, name=f"m3_ring_{i}", outer_radius=M3 * 2, inner_radius=M3, location=(x, y, 0), depth=plate_depth)

# M5
holes3 = [
    (28.0, 0),
    (-28.0, 0),
]
for i, (x, y) in enumerate(holes3):
    base.cube_add(target=plate, name=f"m3_mounting_protrusion_{i}", scale=(x * 2, M5 * 4, plate_depth), location=(0, y, 0))
    base.ring_add(target=plate, name=f"m3_ring_{i}", outer_radius=M5 * 2, inner_radius=M5, location=(x, y, 0), depth=plate_depth)


# ==============================================

x=35
y=35
wifi = base.cube_create(
    name="wifi", scale=(x, y, plate_depth), location=(0, 0, 0)
)

h = 4
height = h / 2 + plate_depth / 2

base.cube_add(
    target=wifi,
    name="arm_outer",
    scale=(x, y, h),
    location=(0, 0, h/2),
)

base.cube_clear(
    target=wifi,
    name="arm_inner_1",
    scale=(x - 3, y - 3, h),
    location=(0, 0, height)
)

base.cube_clear(target=wifi, name="arm_inner_2", scale=(24, 24, h), location=(0, 0, 0))

base.cube_clear(
    target=wifi,
    name="arm_inner_corner_1",
    scale=(18, 18, h),
    location=(x / 2, -y / 2, height),
)
base.cube_clear(
    target=wifi,
    name="arm_inner_corner_2",
    scale=(18, 18, h),
    location=(-x / 2, -y / 2, height),
)
base.cube_clear(
    target=wifi,
    name="arm_inner_back",
    scale=(22, 22, h),
    location=(0, x / 2, height),
)

wifi.location=(0, -25, 0)

base.join(plate, wifi)

# ==============================================

x=25
y=43
ubec = base.cube_create(
    name="ubec", scale=(x, y, plate_depth), location=(0, 0, 0)
)

h = 6
height = h / 2 + plate_depth / 2

base.cube_add(
    target=ubec,
    name="arm_outer",
    scale=(x, y, h),
    location=(0, 0, h/2),
)

base.cube_clear(
    target=ubec,
    name="arm_inner_1",
    scale=(x - 3, y - 3, h),
    location=(0, 0, height)
)

base.cube_clear(target=ubec, name="arm_inner_2", scale=(22, 29, h), location=(0, 0, 0))

base.cube_clear(
    target=ubec,
    name="arm_inner_corner_1",
    scale=(10, 10, h),
    location=(x / 2, -y / 2, height),
)
base.cube_clear(
    target=ubec,
    name="arm_inner_corner_2",
    scale=(10, 10, h),
    location=(-x / 2, -y / 2, height),
)
base.cube_clear(
    target=ubec,
    name="arm_inner_back",
    scale=(22, 22, h),
    location=(0, x / 2, height),
)

ubec.location=(0, -80, 0)

base.join(plate, ubec)
