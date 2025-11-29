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

# プレート寸法
plate_width = 16.4 * 2
plate_height = 101.0 + 101.8 + M3 * 2
plate_depth = 2.8

def add_protrusion(target, name, scale, location):
    base.cube_add(target=target, name=name, scale=scale, location=location)


# プレート作成
plate = base.cube_create(
    name="plate",
    scale=(plate_width, plate_height, plate_depth),
    location=(0, 0, 0),
)

base.cube_clear(
    target=plate,
    name="UpperCornerCut",
    scale=(plate_width - 12, plate_height - 12, plate_depth),
    location=(0, 0, 0),
)


# M2.5 リング位置
holes = [
    (24.5, 65.0),
    (-24.5, 65.0),
    (24.5, 7),
    (-24.5, 7),
]


for i, (x, y) in enumerate(holes):
    add_protrusion(
        target=plate,
        name=f"m2_5_mounting_protrusion_{i}",
        scale=(x * 2, M2_5 * 4, plate_depth),
        location=(0, y, 0),
    )

# M2.5 リングの生成
for i, (x, y) in enumerate(holes):
    base.add_ring(
        target=plate,
        name=f"m2_5_ring_{i}",
        outer_radius=M2_5 * 2,
        inner_radius=M2_5,
        location=(x, y, 0),
        depth=plate_depth,
    )


# M3 リング位置
holes2 = [
    (16.4, 101.0),
    (-16.4, 101.0),
    (26, 39.75),
    (-26, 39.75),
    (28.4, -25.15),
    (-28.4, -25.15),
    (18.9, -101.8),
    (-18.9, -101.8),
]

for i, (x, y) in enumerate(holes2):
    add_protrusion(
        target=plate,
        name=f"m3_mounting_protrusion_{i}",
        scale=(x * 2, M3 * 4, plate_depth),
        location=(0, y, 0),
    )

# M3 リングの生成
for i, (x, y) in enumerate(holes2):
    base.add_ring(
        target=plate,
        name=f"m3_ring_{i}",
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, 0),
        depth=plate_depth,
    )
