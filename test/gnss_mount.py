import bpy
import bmesh
import math


def clear_all_objects():
    """すべてのオブジェクトを削除"""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def create_cube(name, size, location, scale=None):
    """立方体を作成する"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name

    if scale:
        obj.scale = scale
    else:
        obj.scale = (size, size, size)

    bpy.ops.object.transform_apply(scale=True)
    return obj


def create_cylinder(name, radius, depth, location):
    """円柱を作成する"""
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    return obj


def apply_boolean_modifier(target_obj, modifier_obj, operation, modifier_name):
    """ブール演算を適用する"""
    bool_mod = target_obj.modifiers.new(name=modifier_name, type="BOOLEAN")
    bool_mod.operation = operation
    bool_mod.object = modifier_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)


def create_holes(target_obj, holes_data, hole_radius, depth):
    """穴を作成してブール演算で削除"""
    for i, (x, y) in enumerate(holes_data):
        hole = create_cylinder(f"Hole{i}", hole_radius, depth + 10, (x, y, depth))
        apply_boolean_modifier(target_obj, hole, "DIFFERENCE", f"Bool_Hole{i}")
        bpy.data.objects.remove(hole, do_unlink=True)


def create_rectangular_frame(
    inner_size, frame_thickness, frame_depth, position_z, clearance=0.2
):
    """四角の枠を作成する（中空）"""
    # 内側の実際のサイズ（箱のサイズ + クリアランス）
    inner_width = inner_size + clearance
    inner_height = inner_size + clearance

    # 外側のサイズ（内側 + 枠の厚み×2）
    frame_width = inner_width + 2 * frame_thickness
    frame_height = inner_height + 2 * frame_thickness

    # 枠の位置
    frame_z = position_z + frame_depth / 2

    # 外側の四角形
    frame_outer = create_cube(
        "Frame_Outer", 1, (0, 0, frame_z), (frame_width, frame_height, frame_depth)
    )

    # 内側の四角形（くり抜き用）
    frame_inner = create_cube(
        "Frame_Inner",
        1,
        (0, 0, frame_z),
        (inner_width, inner_height, frame_depth + 0.1),  # 少し高くして確実にくり抜く
    )

    # ブール演算で枠を作成
    apply_boolean_modifier(frame_outer, frame_inner, "DIFFERENCE", "Bool_Frame")

    # 内側の四角形を削除
    bpy.data.objects.remove(frame_inner, do_unlink=True)

    return frame_outer


def create_rectangular_box(width, height, depth, thickness, position_z, clearance=0.2):
    """四角の箱を作成する（底面付き）"""
    # 内側の実際のサイズ
    inner_width = width + clearance
    inner_height = height + clearance

    # 外側のサイズ
    outer_width = inner_width + 2 * thickness
    outer_height = inner_height + 2 * thickness

    # 箱の位置
    box_z = position_z + depth / 2

    # 外側の四角形
    box_outer = create_cube(
        "Box_Outer", 1, (0, 0, box_z), (outer_width, outer_height, depth)
    )

    # 内側の四角形（くり抜き用）
    # 底面を残すため、少し上に配置
    inner_z = position_z + (depth + thickness) / 2
    box_inner = create_cube(
        "Box_Inner",
        1,
        (0, 0, inner_z),
        (inner_width, inner_height, depth - thickness + 0.1),
    )

    # ブール演算で箱を作成
    apply_boolean_modifier(box_outer, box_inner, "DIFFERENCE", "Bool_Box")

    # 内側の四角形を削除
    bpy.data.objects.remove(box_inner, do_unlink=True)

    return box_outer


# 既存オブジェクトを削除
clear_all_objects()

# パラメータ設定
plate_width = 40
plate_height = 23.2
plate_depth = 1.5

# プレート作成
plate = create_cube(
    "Plate", 1, (0, 0, plate_depth / 2), (plate_width, plate_height, plate_depth)
)

# ネジ穴パラメータ
M3 = 1.75
PITCH = 16.4
holes_data = [
    (-PITCH, plate_width / 4 - M3 * 1.25),
    (PITCH, plate_width / 4 - M3 * 1.25),
]

# ネジ穴作成
create_holes(plate, holes_data, M3, plate_depth)

# 枠パラメータ
inner_box_size = 20.0
clearance = 0.2
frame_thickness = 1.5
frame_depth = 6

# 枠作成（中空の枠）
frame = create_rectangular_frame(
    inner_box_size, frame_thickness, frame_depth, plate_depth, clearance
)

# 枠をプレートに結合
apply_boolean_modifier(plate, frame, "UNION", "Bool_Frame")
bpy.data.objects.remove(frame, do_unlink=True)

# -----------------
# 中央の四角穴のサイズ
hole_width = 14.0
hole_height = 14.0
hole_depth = plate_depth + 0.1  # プレートを貫通

# 四角穴用の立方体を作成
rect_hole = create_cube(
    "Rect_Hole", 1, (0, 0, hole_depth / 2), (hole_width, hole_height, hole_depth)
)

# プレートに四角穴を開ける
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)

# -----------------
# 中央の四角穴のサイズ
hole_width = 9.1
hole_height = 9.0
hole_depth = 9  # プレートを貫通

# 四角穴用の立方体を作成
rect_hole2 = create_cube(
    "Rect_Hole2", 1, (0, -10.5, hole_depth / 2), (hole_width, hole_height, hole_depth)
)

# プレートに四角穴を開ける
apply_boolean_modifier(plate, rect_hole2, "DIFFERENCE", "Bool_Rect_Hole2")
bpy.data.objects.remove(rect_hole2, do_unlink=True)

# -----------------
# 中央の四角穴のサイズ
hole_width = 10
hole_height = 16.8
hole_depth = 10  # プレートを貫通

# 四角穴用の立方体を作成
rect_hole2 = create_cube(
    "Rect_Hole2",  #
    1,  #
    (
        hole_width * 2,  #
        -hole_height / 4,
        hole_depth / 2,
    ),
    (
        hole_height,  #
        hole_height,
        hole_depth,
    ),
)

# プレートに四角穴を開ける
apply_boolean_modifier(plate, rect_hole2, "DIFFERENCE", "Bool_Rect_Hole2")
bpy.data.objects.remove(rect_hole2, do_unlink=True)

# 四角穴用の立方体を作成
rect_hole2 = create_cube(
    "Rect_Hole2",  #
    1,  #
    (
        -hole_width * 2,  #
        -hole_height / 4,
        hole_depth / 2,
    ),
    (
        hole_height,  #
        hole_height,
        hole_depth,
    ),
)

# プレートに四角穴を開ける
apply_boolean_modifier(plate, rect_hole2, "DIFFERENCE", "Bool_Rect_Hole2")
bpy.data.objects.remove(rect_hole2, do_unlink=True)

# -----------------


# 最終的にプレートを選択
bpy.context.view_layer.objects.active = plate
plate.select_set(True)
