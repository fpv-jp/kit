import bpy
import math

# 3Dビューを探して全削除
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


def add_protrusion_to_object(target_obj, protrusion_name, dimensions, position):
    """オブジェクトに突起物を追加する関数"""
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=position,
    )
    protrusion_obj = bpy.context.object
    protrusion_obj.scale = dimensions
    bpy.ops.object.transform_apply(scale=True)

    union_modifier = target_obj.modifiers.new(
        name=f"Union_{protrusion_name}", type="BOOLEAN"
    )
    union_modifier.operation = "UNION"
    union_modifier.object = protrusion_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)
    bpy.data.objects.remove(protrusion_obj, do_unlink=True)


def add_hole_to_object(
    target_obj, hole_name, hole_radius, hole_depth, position, rotation=(0, 0, 0)
):
    """オブジェクトに穴を追加する関数"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_radius,
        depth=hole_depth,
        location=position,
        rotation=rotation,
    )
    hole_obj = bpy.context.active_object
    hole_obj.name = hole_name

    difference_modifier = target_obj.modifiers.new(
        name=f"Difference_{hole_name}", type="BOOLEAN"
    )
    difference_modifier.operation = "DIFFERENCE"
    difference_modifier.object = hole_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=difference_modifier.name)
    bpy.data.objects.remove(hole_obj, do_unlink=True)


# 寸法定数
BASE_PLATE_THICKNESS = 2.5
# リング寸法
RING_OUTER_DIAMETER = 12.5
RING_INNER_DIAMETER = 7.25
RING_CENTER_OFFSET_X = 1.75

# 外側リング作成
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=RING_OUTER_DIAMETER,
    depth=BASE_PLATE_THICKNESS,
    location=(
        RING_CENTER_OFFSET_X,
        0,
        BASE_PLATE_THICKNESS,
    ),
)
main_ring = bpy.context.active_object
main_ring.name = "MainRing"

# 内側穴作成
bpy.ops.mesh.primitive_cylinder_add(
    vertices=64,
    radius=RING_INNER_DIAMETER,
    depth=BASE_PLATE_THICKNESS * 2,
    location=(
        RING_CENTER_OFFSET_X,
        0,
        BASE_PLATE_THICKNESS,
    ),
)
center_hole = bpy.context.active_object
center_hole_modifier = main_ring.modifiers.new(name="CenterHoleBoolean", type="BOOLEAN")
center_hole_modifier.object = center_hole
center_hole_modifier.operation = "DIFFERENCE"
bpy.context.view_layer.objects.active = main_ring
bpy.ops.object.modifier_apply(modifier=center_hole_modifier.name)
bpy.data.objects.remove(center_hole, do_unlink=True)

# プレート寸法
BASE_PLATE_WIDTH = 54
BASE_PLATE_HEIGHT = 44

# アーム寸法
ARM_WIDTH = 11

# 右アーム作成
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        (BASE_PLATE_WIDTH + RING_CENTER_OFFSET_X) / 3,
        0,
        BASE_PLATE_THICKNESS,
    ),
)
right_arm = bpy.context.active_object
right_arm.scale = (
    BASE_PLATE_WIDTH / 2 - RING_OUTER_DIAMETER / 2 - RING_CENTER_OFFSET_X / 2,
    ARM_WIDTH,
    BASE_PLATE_THICKNESS,
)
bpy.ops.object.transform_apply(scale=True)

# 右側突起物追加
add_protrusion_to_object(
    main_ring,
    protrusion_name="RightProtrusion",
    dimensions=(
        BASE_PLATE_THICKNESS,
        ARM_WIDTH + 0.001,
        ARM_WIDTH,
    ),
    position=(
        BASE_PLATE_WIDTH / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
        0,
        BASE_PLATE_THICKNESS / 2 + ARM_WIDTH / 2,
    ),
)

# 左アーム作成
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        -(BASE_PLATE_WIDTH + RING_CENTER_OFFSET_X) / 3,
        0,
        BASE_PLATE_THICKNESS,
    ),
)
left_arm = bpy.context.active_object
left_arm.scale = (
    BASE_PLATE_WIDTH / 2 - RING_OUTER_DIAMETER / 2 - RING_CENTER_OFFSET_X,
    ARM_WIDTH,
    BASE_PLATE_THICKNESS,
)
bpy.ops.object.transform_apply(scale=True)

# 左側突起物追加
add_protrusion_to_object(
    main_ring,
    protrusion_name="LeftProtrusion",
    dimensions=(
        BASE_PLATE_THICKNESS,
        ARM_WIDTH + 0.001,
        ARM_WIDTH,
    ),
    position=(
        -BASE_PLATE_WIDTH / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
        0,
        BASE_PLATE_THICKNESS / 2 + ARM_WIDTH / 2,
    ),
)

# 上アーム作成
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,
        BASE_PLATE_HEIGHT / 3 + RING_CENTER_OFFSET_X / 2 + 0.09,
        BASE_PLATE_THICKNESS,
    ),
)
top_arm = bpy.context.active_object
top_arm.scale = (
    ARM_WIDTH,
    BASE_PLATE_HEIGHT / 2 - RING_OUTER_DIAMETER / 2,
    BASE_PLATE_THICKNESS,
)
bpy.ops.object.transform_apply(scale=True)

# 上側突起物追加
add_protrusion_to_object(
    main_ring,
    protrusion_name="TopProtrusion",
    dimensions=(
        ARM_WIDTH,
        BASE_PLATE_THICKNESS,
        ARM_WIDTH,
    ),
    position=(
        0,
        BASE_PLATE_HEIGHT / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
        BASE_PLATE_THICKNESS / 2 + ARM_WIDTH / 2,
    ),
)

# 下アーム作成
bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,
        -BASE_PLATE_HEIGHT / 3 - RING_CENTER_OFFSET_X / 2 - 0.09,
        BASE_PLATE_THICKNESS,
    ),
)
bottom_arm = bpy.context.active_object
bottom_arm.scale = (
    ARM_WIDTH,
    BASE_PLATE_HEIGHT / 2 - RING_OUTER_DIAMETER / 2,
    BASE_PLATE_THICKNESS,
)
bpy.ops.object.transform_apply(scale=True)

# 下側突起物追加
add_protrusion_to_object(
    main_ring,
    protrusion_name="BottomProtrusion",
    dimensions=(
        ARM_WIDTH,
        BASE_PLATE_THICKNESS,
        ARM_WIDTH,
    ),
    position=(
        0,
        -BASE_PLATE_HEIGHT / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
        BASE_PLATE_THICKNESS / 2 + ARM_WIDTH / 2,
    ),
)

# # 穴径定数（ドリル径 + クリアランス）
# HOLE_M2_5_RADIUS = 1.25 + 0.25
# HOLE_M3_RADIUS = 1.5 + 0.25

# # 右側突起物に水平穴（上部）
# add_hole_to_object(
#     main_ring,
#     hole_name="RightHoleUpper",
#     hole_radius=HOLE_M3_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         BASE_PLATE_WIDTH / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
#         0,
#         ARM_WIDTH - HOLE_M3_RADIUS * 1.5,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 右側突起物に水平穴（中部）
# add_hole_to_object(
#     main_ring,
#     hole_name="RightHoleLower",
#     hole_radius=HOLE_M3_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         BASE_PLATE_WIDTH / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
#         0,
#         ARM_WIDTH - HOLE_M3_RADIUS * 1.5 - 15,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 右側突起物に水平穴（下部）
# add_hole_to_object(
#     main_ring,
#     hole_name="RightHoleBottom",
#     hole_radius=HOLE_M2_5_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         BASE_PLATE_WIDTH / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
#         0,
#         ARM_WIDTH / 2 + HOLE_M2_5_RADIUS * 1.5,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 左側突起物に水平穴（上部）
# add_hole_to_object(
#     main_ring,
#     hole_name="LeftHoleUpper",
#     hole_radius=HOLE_M3_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         -BASE_PLATE_WIDTH / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
#         0,
#         ARM_WIDTH - HOLE_M3_RADIUS * 1.5,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 左側突起物に水平穴（中部）
# add_hole_to_object(
#     main_ring,
#     hole_name="LeftHoleLower",
#     hole_radius=HOLE_M3_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         -BASE_PLATE_WIDTH / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
#         0,
#         ARM_WIDTH - HOLE_M3_RADIUS * 1.5 - 15,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 左側突起物に水平穴（下部）
# add_hole_to_object(
#     main_ring,
#     hole_name="LeftHoleBottom",
#     hole_radius=HOLE_M2_5_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         -BASE_PLATE_WIDTH / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
#         0,
#         ARM_WIDTH / 2 + HOLE_M2_5_RADIUS * 1.5,
#     ),
#     rotation=(0, math.radians(90), 0),
# )

# # 上側突起物に垂直穴
# add_hole_to_object(
#     main_ring,
#     hole_name="TopHole",
#     hole_radius=HOLE_M2_5_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         0,
#         BASE_PLATE_HEIGHT / 2 + BASE_PLATE_THICKNESS / 2 + 0.5,
#         ARM_WIDTH / 2 + HOLE_M2_5_RADIUS * 1.5,
#     ),
#     rotation=(math.radians(90), 0, 0),
# )

# # 下側突起物に垂直穴
# add_hole_to_object(
#     main_ring,
#     hole_name="BottomHole",
#     hole_radius=HOLE_M2_5_RADIUS,
#     hole_depth=BASE_PLATE_THICKNESS + 2,
#     position=(
#         0,
#         -BASE_PLATE_HEIGHT / 2 - BASE_PLATE_THICKNESS / 2 - 0.5,
#         ARM_WIDTH / 2 + HOLE_M2_5_RADIUS * 1.5,
#     ),
#     rotation=(math.radians(90), 0, 0),
# )


# 全アームをメインリングに結合
def join_arm_to_main_ring(arm_object):
    """アームをメインリングに結合する関数"""
    bpy.ops.object.select_all(action="DESELECT")
    main_ring.select_set(True)
    arm_object.select_set(True)
    bpy.context.view_layer.objects.active = main_ring
    bpy.ops.object.join()


# 各アームを順次結合
join_arm_to_main_ring(right_arm)
join_arm_to_main_ring(left_arm)
join_arm_to_main_ring(top_arm)
join_arm_to_main_ring(bottom_arm)
