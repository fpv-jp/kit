import bpy
import bmesh
import math

# まず現在のスクリーンから3Dビューエリアを探して全削除
view_3d_area = next(
    (area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None
)
if view_3d_area:
    with bpy.context.temp_override(area=view_3d_area):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
else:
    raise RuntimeError(
        "3Dビューが見つかりませんでした。スクリプトを3Dビューで実行してください。"
    )

# CM4のサイズに合わせた寸法
CM4_WIDTH = 55
CM4_HEIGHT = 40
MARGIN = 5
PLATE_WIDTH = CM4_WIDTH + MARGIN
PLATE_HEIGHT = CM4_HEIGHT + MARGIN
PLATE_THICKNESS = 2

# 板を作成
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, PLATE_THICKNESS))
main_plate = bpy.context.object
main_plate.scale = (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

# 中央をくり抜く穴を作成
INNER_CUT_MARGIN = 14
inner_cutout_width = PLATE_WIDTH * 2 - INNER_CUT_MARGIN * 2
inner_cutout_height = PLATE_HEIGHT * 2 - INNER_CUT_MARGIN * 2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,
        0,
        PLATE_THICKNESS / 2,
    ),
)
inner_cutout = bpy.context.object
inner_cutout.scale = (
    inner_cutout_width / 2,
    inner_cutout_height / 2,
    PLATE_THICKNESS * 2,
)
bpy.ops.object.transform_apply(scale=True)

# 板から中央の穴を引く
inner_cutout_modifier = main_plate.modifiers.new(name="", type="BOOLEAN")
inner_cutout_modifier.operation = "DIFFERENCE"
inner_cutout_modifier.object = inner_cutout
bpy.context.view_layer.objects.active = main_plate
bpy.ops.object.modifier_apply(modifier=inner_cutout_modifier.name)
bpy.data.objects.remove(inner_cutout, do_unlink=True)


# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------


def create_triangle(vertices):
    mesh = bpy.data.meshes.new("Triangle_Mesh")
    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(verts)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


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
    theta = math.radians(rotation)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    verts_rot = [
        (
            v[0] * cos_t - v[1] * sin_t,
            v[0] * sin_t + v[1] * cos_t,
            v[2],
        )
        for v in vertices
    ]
    triangle_mesh = create_triangle(verts_rot)
    triangle = bpy.data.objects.new(f"Triangle_Hole_{i}", triangle_mesh)
    bpy.context.collection.objects.link(triangle)
    triangle.location = (x, y, PLATE_THICKNESS / 2)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, PLATE_THICKNESS + 2)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, 0)
    bool_mod = main_plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = main_plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


x1 = 22
y1 = 14

triangle_positions = [
    (x1, y1, [(-2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 180),
    (-x1, y1, [(2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 180),
    (x1, -y1, [(2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 0),
    (-x1, -y1, [(-2.5, 2.5, 0), (-2.5, -2.5, 0), (2.5, -2.5, 0)], 0),
]


for i, (x, y, vertices, rotation) in enumerate(triangle_positions):
    theta = math.radians(rotation)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    verts_rot = [
        (
            v[0] * cos_t - v[1] * sin_t,
            v[0] * sin_t + v[1] * cos_t,
            v[2],
        )
        for v in vertices
    ]
    triangle_mesh = create_triangle(verts_rot)
    triangle = bpy.data.objects.new(f"Triangle_Hole_{i}", triangle_mesh)
    bpy.context.collection.objects.link(triangle)
    triangle.location = (x, y, PLATE_THICKNESS)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, PLATE_THICKNESS)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, PLATE_THICKNESS / 2)
    bool_mod = main_plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = main_plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------


def create_and_apply_protrusion(target_object, scale, location):
    """指定されたオブジェクトに突起物を追加する"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    protrusion_cube = bpy.context.object
    protrusion_cube.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    protrusion_modifier = target_object.modifiers.new(name="", type="BOOLEAN")
    protrusion_modifier.operation = "UNION"
    protrusion_modifier.object = protrusion_cube
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=protrusion_modifier.name)
    bpy.data.objects.remove(protrusion_cube, do_unlink=True)


# 突起物の寸法
PROTRUSION_HEIGHT = 21
PROTRUSION_HEIGHT2 = 10
PROTRUSION_DEPTH = 13.5

protrusion_z = PLATE_THICKNESS + PROTRUSION_DEPTH / 2

protrusion_x = PLATE_WIDTH / 2 - PLATE_THICKNESS / 2


# 左突起物
create_and_apply_protrusion(
    main_plate,
    scale=(PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH),
    location=(-protrusion_x, PLATE_WIDTH / 4.5, protrusion_z),
)
create_and_apply_protrusion(
    main_plate,
    scale=(PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH),
    location=(-protrusion_x, -PLATE_WIDTH / 4.5, protrusion_z),
)

# 右突起物
create_and_apply_protrusion(
    main_plate,
    scale=(PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH),
    location=(protrusion_x, PLATE_WIDTH / 4.5, protrusion_z),
)
create_and_apply_protrusion(
    main_plate,
    scale=(PLATE_THICKNESS, PROTRUSION_HEIGHT2, PROTRUSION_DEPTH),
    location=(protrusion_x, -PLATE_WIDTH / 4.5, protrusion_z),
)

protrusion_y = PLATE_HEIGHT / 2 - PLATE_THICKNESS / 2

# 下突起物
create_and_apply_protrusion(
    main_plate,
    scale=(PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH),
    location=(0, -protrusion_y, protrusion_z),
)

# 上突起物
create_and_apply_protrusion(
    main_plate,
    scale=(PROTRUSION_HEIGHT, PLATE_THICKNESS, PROTRUSION_DEPTH),
    location=(0, protrusion_y, protrusion_z),
)


# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
def create_and_apply_hole(target_object, radius, depth, location, rotation=(0, 0, 0)):
    """指定されたオブジェクトに穴を開ける"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    hole_cylinder = bpy.context.active_object
    hole_modifier = target_object.modifiers.new(name="", type="BOOLEAN")
    hole_modifier.operation = "DIFFERENCE"
    hole_modifier.object = hole_cylinder
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=hole_modifier.name)
    bpy.data.objects.remove(hole_cylinder, do_unlink=True)


# ホールサイズ
M2_5_HOLE_RADIUS = 1.25 + 0.25
M3_HOLE_RADIUS = 1.5 + 0.25

# 突起物の固定穴の位置
hole_z_position = PLATE_THICKNESS + PROTRUSION_DEPTH - M2_5_HOLE_RADIUS * 2

# 左突起物の水平穴
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(-protrusion_x, PLATE_WIDTH / 4.5, hole_z_position),
    rotation=(0, math.radians(90), 0),
)
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(-protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position),
    rotation=(0, math.radians(90), 0),
)

# 右突起物の水平穴
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(protrusion_x, PLATE_WIDTH / 4.5, hole_z_position),
    rotation=(0, math.radians(90), 0),
)
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(protrusion_x, -PLATE_WIDTH / 4.5, hole_z_position),
    rotation=(0, math.radians(90), 0),
)

# 下突起物の水平穴
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(7, -protrusion_y, hole_z_position),
    rotation=(math.radians(90), 0, 0),
)
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(-7, -protrusion_y, hole_z_position),
    rotation=(math.radians(90), 0, 0),
)

# 上突起物の水平穴
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(7, protrusion_y, hole_z_position),
    rotation=(math.radians(90), 0, 0),
)
create_and_apply_hole(
    main_plate,
    radius=M2_5_HOLE_RADIUS,
    depth=PLATE_THICKNESS + 2,
    location=(-7, protrusion_y, hole_z_position),
    rotation=(math.radians(90), 0, 0),
)


# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------


def create_and_apply_pin(target_object, radius, depth, location):
    """指定されたオブジェクトにピンを追加する"""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
    pin_cylinder = bpy.context.object
    pin_modifier = target_object.modifiers.new(name="", type="BOOLEAN")
    pin_modifier.operation = "UNION"
    pin_modifier.object = pin_cylinder
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=pin_modifier.name)
    bpy.data.objects.remove(pin_cylinder, do_unlink=True)


# ピンサイズ
# M2_PIN_RADIUS = 0.85
M2_PIN_RADIUS = 2.5

# CM4固定用ピン
# PIN_HEIGHT = 5.5
PIN_HEIGHT = 2.2
CM4_PIN_OFFSET_X = 23.5
CM4_PIN_OFFSET_Y = 16.5

create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (-CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y, 4),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y, 4),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (-CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y, 4),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y, 4),
)

M2_PIN_RADIUS = 0.85
PIN_HEIGHT = 6

create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (-CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y, PIN_HEIGHT),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y, PIN_HEIGHT),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (-CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y, PIN_HEIGHT),
)
create_and_apply_pin(
    main_plate,
    M2_PIN_RADIUS,
    PIN_HEIGHT,
    (CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y, PIN_HEIGHT),
)


def create_ring_with_center_hole(
    outer_diameter: float,
    inner_diameter: float,
    location: tuple[float, float, float],
    plate: bpy.types.Object,
):
    """リングをプレートに接着し、中心穴をプレートに貫通させる"""

    # 外側リング（プレートに結合）
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_diameter,
        depth=PLATE_THICKNESS,
        location=(location[0], location[1], PLATE_THICKNESS),
    )
    ring = bpy.context.active_object

    # プレートとUNION結合
    union_mod = plate.modifiers.new(name="Union_Ring", type="BOOLEAN")
    union_mod.operation = "UNION"
    union_mod.object = ring
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=union_mod.name)
    bpy.data.objects.remove(ring, do_unlink=True)

    # 穴（リングとプレートの両方に貫通）
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_diameter,
        depth=10,  # 貫通確実に
        location=(location[0], location[1], 0),
    )
    hole = bpy.context.active_object

    diff_mod = plate.modifiers.new(name="Hole_Cut", type="BOOLEAN")
    diff_mod.operation = "DIFFERENCE"
    diff_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=diff_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


M3 = 1.85
X_POS = 14
Y_POS = 20

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]


for i, (x, y) in enumerate(holes):
    create_ring_with_center_hole(
        outer_diameter=M3 * 2, inner_diameter=M3, location=(x, y, 0), plate=main_plate
    )
