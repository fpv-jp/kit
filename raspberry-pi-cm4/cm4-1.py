import bpy
import math
import sys
import types

for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        with bpy.context.temp_override(area=area):
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
        break
else:
    raise RuntimeError("It appears that no 3D View was found. Please run the script in a 3D View.")

try:
    import base
except ModuleNotFoundError:
    text = bpy.data.texts.get("base.py")
    if not text:
        raise
    module = types.ModuleType("base")
    exec(text.as_string(), module.__dict__)
    sys.modules["base"] = module
    import base

# CM4のサイズに合わせた寸法
CM4_WIDTH = 55
CM4_HEIGHT = 40
MARGIN = 5
PLATE_WIDTH = CM4_WIDTH + MARGIN
PLATE_HEIGHT = CM4_HEIGHT + MARGIN
PLATE_THICKNESS = 2

# メインの板
main_plate = base.cube_create(
    name="main_plate",
    scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS),
    location=(0, 0, PLATE_THICKNESS),
)

# 中央をくり抜く穴を作成
INNER_CUT_MARGIN = 14
inner_cutout_width = PLATE_WIDTH * 2 - INNER_CUT_MARGIN * 2
inner_cutout_height = PLATE_HEIGHT * 2 - INNER_CUT_MARGIN * 2

base.cube_clear(
    target=main_plate,
    name="inner_cutout",
    scale=(inner_cutout_width / 2, inner_cutout_height / 2, PLATE_THICKNESS * 2),
    location=(0, 0, PLATE_THICKNESS / 2),
)


# 三角形の穴を作成
x1 = 28.25
y1 = 20.75

triangle_clear_positions = [
    (x1, y1, [(-3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 180),
    (-x1, y1, [(3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 180),
    (x1, -y1, [(3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 0),
    (-x1, -y1, [(-3.0, 3.0, 0), (-3.0, -3.0, 0), (3.0, -3.0, 0)], 0),
]

for i, (x, y, vertices, rotation_deg) in enumerate(triangle_clear_positions):
    base.triangle_clear(
        target=main_plate,
        name=f"triangle_cut_{i}",
        vertices=vertices,
        depth=PLATE_THICKNESS + 2,
        location=(x, y, 0),
        rotation=(0, 0, math.radians(rotation_deg)),
    )

x1 = 22.5
y1 = 14.5

triangle_add_positions = [
    (x1, y1, [(-1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 180),
    (-x1, y1, [(1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 180),
    (x1, -y1, [(1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 0),
    (-x1, -y1, [(-1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 0),
]


for i, (x, y, vertices, rotation_deg) in enumerate(triangle_add_positions):
    base.triangle_add(
        target=main_plate,
        name=f"triangle_add_{i}",
        vertices=vertices,
        depth=PLATE_THICKNESS,
        location=(x, y, PLATE_THICKNESS / 2),
        rotation=(0, 0, math.radians(rotation_deg)),
    )


# 突起物の寸法
PROTRUSION_HEIGHT = 21
PROTRUSION_HEIGHT2 = 10
PROTRUSION_DEPTH = 11.5

protrusion_z = PLATE_THICKNESS + PROTRUSION_DEPTH / 2

protrusion_x = PLATE_WIDTH / 2 - PLATE_THICKNESS / 2

protrusion_y = PLATE_HEIGHT / 2 - PLATE_THICKNESS / 2

base.plate_attach(
    target=main_plate,
    name="protrusions",
    plates=[
        ((PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH), (-protrusion_x, PLATE_WIDTH / 4.5, protrusion_z), None),
        ((PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH), (-protrusion_x, -PLATE_WIDTH / 4.5, protrusion_z), None),
        ((PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH), (protrusion_x, PLATE_WIDTH / 4.5, protrusion_z), None),
        ((PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH), (protrusion_x, -PLATE_WIDTH / 4.5, protrusion_z), None),
        ((PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH), (0, -protrusion_y, protrusion_z), None),
        ((PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH), (0, protrusion_y, protrusion_z), None),
    ],
)

# ホールサイズ
M2_5_HOLE_RADIUS = 1.25 + 0.25
M3_HOLE_RADIUS = 1.5 + 0.25

# 突起物の固定穴の位置
hole_z_position = PLATE_THICKNESS + PROTRUSION_DEPTH - 2.5

hole_rotation_y = (0, math.radians(90), 0)
hole_rotation_x = (math.radians(90), 0, 0)

hole_locations = [
    (-protrusion_x, PLATE_WIDTH / 4.5, hole_z_position, hole_rotation_y),
    (-protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position, hole_rotation_y),
    (protrusion_x, PLATE_WIDTH / 4.5, hole_z_position, hole_rotation_y),
    (protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position, hole_rotation_y),
    (7, -protrusion_y, hole_z_position, hole_rotation_x),
    (-7, -protrusion_y, hole_z_position, hole_rotation_x),
    (7, protrusion_y, hole_z_position, hole_rotation_x),
    (-7, protrusion_y, hole_z_position, hole_rotation_x),
]

for i, (x, y, z, rotation) in enumerate(hole_locations):
    base.cylinder_clear(
        target=main_plate,
        name=f"horizontal_hole_{i}",
        radius=M2_5_HOLE_RADIUS,
        depth=PLATE_THICKNESS + 2,
        location=(x, y, z),
        rotation=rotation,
    )

# ピンサイズ
M2_PIN_RADIUS = 0.85

# CM4固定用ピン
PIN_HEIGHT = 5.5
CM4_PIN_OFFSET_X = 23.5
CM4_PIN_OFFSET_Y = 16.5

base.mount_pins(
    target=main_plate,
    name="cm4_pins",
    radius=M2_PIN_RADIUS,
    depth=PIN_HEIGHT,
    height_pos=4,
    pins=[
        (-CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
        (CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
        (-CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
        (CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
    ],
)
