import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# 板を65mm x 212mm x 2.8mmで作成（中央を原点に配置）
plate_width = 65
plate_height = 212
plate_depth = 2.8

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, plate_depth / 2),
)
plate = bpy.context.object
plate.name = "Plate"
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)

# 既存の穴の位置
holes = [
    (24.5, 50.0),
    (-24.5, 50.0),
    (24.5, -8),
    (-24.5, -8),
]

# 既存の穴の位置
holes2 = [
    (16.4, 101.0),
    (-16.4, 101.0),
    (26.1, 40.75),
    (-26.1, 40.75),
    (28.5, -24.15),
    (-28.5, -24.15),
    (18.9, -101.8),
    (-18.9, -101.8),
]

M2 = 1.25
M2_5 = 1.5
M3 = 1.75

# 既存の穴を作成
for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2_5,
        depth=plate_depth + 10,
        location=(x, y, plate_depth / 2),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)

for i, (x, y) in enumerate(holes2):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M3,
        depth=plate_depth + 10,
        location=(x, y, plate_depth / 2),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


# 三角形の穴を作成
triangle_positions = [
    (30, 100, [(-3, 55, 0), (-3, -7, 0), (9, -7, 0)], 180),
    (-30, 100, [(3, 55, 0), (-9, -7, 0), (3, -7, 0)], 180),
    (30, -104, [(3, 80, 0), (-7, -3, 0), (3, -3, 0)], 0),
    (-30, -104, [(-3, 80, 0), (-3, -3, 0), (7, -3, 0)], 0),
]


def create_triangle(vertices):
    mesh = bpy.data.meshes.new("Triangle_Mesh")
    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(verts)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


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
    triangle.location = (x, y, plate_depth / 2)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, plate_depth + 10)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, 0)
    bool_mod = plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


# 六角形のくり抜きを作成
def create_hexagon(radius, height):
    """六角形を作成する関数"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=height,
        vertices=6,  # 六角形
        location=(0, 0, 0),
    )
    return bpy.context.object


# 六角形の位置とサイズを定義（既存の穴を避ける位置）
hexagon_cutouts = [
    # (x, y, radius, rotation_degrees)
    (0, 75, 18, 0),  # 上部中央
    (0, 42, 10, 0),  # 上部中央
    (14, 18, 11, 0),  # 中央
    (-14, 18, 11, 0),  # 中央
    (0, -20, 21, 0),  # 中央
    (12.5, -55, 10, 0),  # 中央下
    (-12.5, -55, 10, 0),  # 中央下
    (0, -85, 17.5, 0),  # 下部中央
]

for i, (x, y, radius, rotation) in enumerate(hexagon_cutouts):
    # 六角形を作成
    hexagon = create_hexagon(radius, plate_depth + 10)
    hexagon.name = f"Hexagon_Cutout_{i}"

    # 位置を設定
    hexagon.location = (x, y, plate_depth / 2)

    # 回転を適用
    hexagon.rotation_euler = (0, 0, math.radians(rotation))

    # ブール演算でくり抜き
    bool_mod = plate.modifiers.new(name=f"Bool_Hexagon_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hexagon

    # プレートをアクティブにしてブール演算を適用
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)

    # 六角形オブジェクトを削除
    bpy.data.objects.remove(hexagon, do_unlink=True)


camera_plate_width = 28.5
camera_plate_depth = 1.5

protrusion_width = 7.5
protrusion_height = 15

y_offset = 95

# 左右突起
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            (10.5 * 1.5) / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        2.5,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)

    # 突起をプレートに結合
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)


# 左右突起に水平穴を追加
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)

    # 水平方向（Y軸回転）のシリンダーを作成
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2_5,
        depth=1.5 + 2,
        location=(
            x_offset,  #
            y_offset,  #
            protrusion_height - M2_5 * 2.5,
        ),
        rotation=(
            0,  #
            math.pi / 2,  #
            0,
        ),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"

    # ブール演算で穴を開ける
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole

    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)


camera_plate_width = 27

y_offset = -70

# 左右突起
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            (10.5 * 1.5) / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        2.5,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)

    # 突起をプレートに結合
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,  #
        y_offset,  #
        protrusion_height - 2.5 / 4,
    ),
)
plate2 = bpy.context.object
plate2.name = "Plate2"
plate2.scale = (camera_plate_width, protrusion_height / 2, 2.5)
bpy.ops.object.transform_apply(scale=True)
bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
bool_mod.operation = "UNION"
bool_mod.object = plate2
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(plate2, do_unlink=True)


y_offset = -40

# 左右突起
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            (10.5 * 1.5) / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        2.5,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)

    # 突起をプレートに結合
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)


bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,  #
        y_offset,  #
        protrusion_height - 2.5 / 4,
    ),
)
plate3 = bpy.context.object
plate3.name = "Plate2"
plate3.scale = (camera_plate_width, protrusion_height / 2, 2.5)
bpy.ops.object.transform_apply(scale=True)

bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
bool_mod.operation = "UNION"
bool_mod.object = plate3
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(plate3, do_unlink=True)


camera_plate_width = 40
camera_plate_depth = 1.5
y_offset = -95

protrusion_width = 6
protrusion_height = 8

# 左右突起
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            protrusion_height / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        1.5,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)

    # 突起をプレートに結合
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)


# 左右突起に水平穴を追加
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)

    # 水平方向（Y軸回転）のシリンダーを作成
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2,
        depth=1.5 + 2,
        location=(
            x_offset,  #
            y_offset,  #
            protrusion_height - M2 * 2,
        ),
        rotation=(
            0,
            math.pi / 2,
            0,
        ),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"

    # ブール演算で穴を開ける
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole

    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)


ring_outer_radius = 10  # 外径
ring_inner_radius = 3.3  # 内径
ring_y_position = -95  # y座標位置

# 外側の円筒を作成
bpy.ops.mesh.primitive_cylinder_add(
    radius=ring_outer_radius,
    depth=plate_depth,
    location=(
        0,  #
        ring_y_position,
        plate_depth / 2,
    ),
)
ring_outer = bpy.context.object
ring_outer.name = "Ring_Outer"

# 内側の円筒（穴）を作成
bpy.ops.mesh.primitive_cylinder_add(
    radius=ring_inner_radius,
    depth=plate_depth + 2,
    location=(
        0,  #
        ring_y_position,
        plate_depth / 2,
    ),
)
ring_inner = bpy.context.object
ring_inner.name = "Ring_Inner"

bool_mod = ring_outer.modifiers.new(name="Bool_Ring_Hole", type="BOOLEAN")
bool_mod.operation = "DIFFERENCE"
bool_mod.object = ring_inner

bpy.context.view_layer.objects.active = ring_outer
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(ring_inner, do_unlink=True)

ring_outer.name = "Ring_Plate"
bool_mod = plate.modifiers.new(name="Bool_Ring_Union", type="BOOLEAN")
bool_mod.operation = "UNION"
bool_mod.object = ring_outer

bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(ring_outer, do_unlink=True)

# 完成した板を選択
plate.select_set(True)
bpy.context.view_layer.objects.active = plate
