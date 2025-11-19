import bpy
import bmesh
import math


def clear_scene():
    """3Dビューのオブジェクトをすべて削除"""
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            with bpy.context.temp_override(area=area):
                bpy.ops.object.select_all(action="SELECT")
                bpy.ops.object.delete()
            break
    else:
        raise RuntimeError(
            "3Dビューが見つかりませんでした。スクリプトを3Dビューで実行してください。"
        )


# ==== 実行開始 ====
clear_scene()


# ネジ径定義
M2 = 1.25
M2_5 = 1.5
M3 = 1.75

# プレート寸法
plate_width = 16.4 * 2
plate_height = 14
plate_depth = 2.8


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
        depth=plate_depth,
        location=(location[0], location[1], 0),
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
        depth=plate_depth + 1.0,  # 貫通確実に
        location=(location[0], location[1], 0),
    )
    hole = bpy.context.active_object

    diff_mod = plate.modifiers.new(name="Hole_Cut", type="BOOLEAN")
    diff_mod.operation = "DIFFERENCE"
    diff_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=diff_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


def create_and_apply_protrusion(target_object, protrusion_name, scale, location):
    """指定されたオブジェクトに突起物を追加する"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    protrusion_cube = bpy.context.object
    protrusion_cube.name = protrusion_name
    protrusion_cube.scale = scale
    bpy.ops.object.transform_apply(scale=True)

    protrusion_modifier = target_object.modifiers.new(
        name=f"boolean_{protrusion_name}", type="BOOLEAN"
    )
    protrusion_modifier.operation = "UNION"
    protrusion_modifier.object = protrusion_cube

    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=protrusion_modifier.name)
    bpy.data.objects.remove(protrusion_cube, do_unlink=True)


def add_angled_cut_to_protrusion(
    target_obj, cut_name, cut_dimensions, cut_position, cut_rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=cut_position, rotation=cut_rotation
    )
    cut_obj = bpy.context.object
    cut_obj.name = f"Cut_{cut_name}"
    cut_obj.scale = cut_dimensions
    bpy.ops.object.transform_apply(scale=True)
    cut_modifier = target_obj.modifiers.new(name=f"Cut_{cut_name}", type="BOOLEAN")
    cut_modifier.operation = "DIFFERENCE"
    cut_modifier.object = cut_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=cut_modifier.name)
    bpy.data.objects.remove(cut_obj, do_unlink=True)


# プレート作成
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, plate_height/2, 0),
)
plate = bpy.context.object
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


# M3 リング位置
holes2 = [
    (18.9, 0),
    (-18.9, 0),
]

for i, (x, y) in enumerate(holes2):
    create_and_apply_protrusion(
        plate,
        "top_mounting_protrusion",
        scale=(x * 2, M3 * 4, plate_depth),
        location=(0, y, 0),
    )

# M3 リングの生成
for i, (x, y) in enumerate(holes2):
    create_ring_with_center_hole(
        outer_diameter=M3 * 2, inner_diameter=M3, location=(x, y, 0), plate=plate
    )

protrusion_width = 7.5
protrusion_height = 8

# 左右突起
for side in [-1, 1]:
    x_offset = side * (10 + plate_depth/2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            9,  #
            protrusion_height/2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        plate_depth,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)


bpy.ops.mesh.primitive_cube_add(
    size=1,  #
    location=(
        0,  #
        -plate_depth/2,  #
        protrusion_height/2,
    ),
)
protrusion = bpy.context.object
protrusion.scale = (
    protrusion_height,
    plate_depth,  #
    protrusion_width,  #
)
bpy.ops.object.transform_apply(scale=True)
bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
bool_mod.operation = "UNION"
bool_mod.object = protrusion
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(protrusion, do_unlink=True)
