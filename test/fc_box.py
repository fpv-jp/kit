import bpy
import bmesh
import math

# パラメータ設定
plate_width = 47
plate_height = 47
plate_depth = 2

# 枠パラメータ
frame_depth = 21.5


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


def create_rectangular_frame():
    """四角の枠を作成する（中空）"""

    # 枠の位置
    frame_z = frame_depth / 2

    # 外側の四角形
    frame_outer = create_cube(
        "Frame_Outer",  #
        1,
        (0, 0, frame_z),
        (plate_width + plate_depth / 2, plate_height + plate_depth / 2, frame_depth),
    )

    # 内側の四角形（くり抜き用）
    frame_inner = create_cube(
        "Frame_Inner",  #
        1,
        (0, 0, frame_z),
        (plate_width - plate_depth, plate_height - plate_depth, frame_depth + 0.1),
    )

    # ブール演算で枠を作成
    apply_boolean_modifier(frame_outer, frame_inner, "DIFFERENCE", "Bool_Frame")

    # 内側の四角形を削除
    bpy.data.objects.remove(frame_inner, do_unlink=True)

    return frame_outer


# 既存オブジェクトを削除
clear_all_objects()

# プレート作成
plate = create_cube(
    "Plate",  #
    1,
    (0, 0, plate_depth / 2),
    (plate_width, plate_height, plate_depth),
)

# ネジ穴パラメータ
M3 = 1.75
holes_data = [(-15.25, 15.25), (15.25, 15.25), (-15.25, -15.25), (15.25, -15.25)]

# ネジ穴作成
create_holes(plate, holes_data, M3, plate_depth)

# 枠作成（中空の枠）
frame = create_rectangular_frame()

# 枠をプレートに結合
apply_boolean_modifier(plate, frame, "UNION", "Bool_Frame")
bpy.data.objects.remove(frame, do_unlink=True)


rect_hole = create_cube(
    "Rect_Hole1",  #
    1,
    (8, 0, plate_depth + 6.25),
    (14, plate_height + 5, 6),
)
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)


rect_hole = create_cube(
    "Rect_Hole1",  #
    1,
    (-8, 0, plate_depth + 6.25),
    (14, plate_height + 5, 6),
)
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)


rect_hole = create_cube(
    "Rect_Hole1",  #
    1,
    (0, -20, plate_depth + 16),
    (14, plate_height / 2, 8),
)
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)


rect_hole = create_cube(
    "Rect_Hole2",  #
    1,
    (42, 0, 0),
    (plate_width + 0.1, 26, 50),
)
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)

rect_hole = create_cube(
    "Rect_Hole3",  #
    1,
    (-30, 0, 10),
    (20, 20, 6),
)
apply_boolean_modifier(plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)


# 最終的にプレートを選択
bpy.context.view_layer.objects.active = plate
plate.select_set(True)
