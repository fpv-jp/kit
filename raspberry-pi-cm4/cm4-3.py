import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# 基本プレート寸法
BASE_PLATE_WIDTH = 40
BASE_PLATE_HEIGHT = 30
BASE_PLATE_THICKNESS = 2
CORNER_CUT_SIZE = 6.5

# 六角形プレート作成
hexagonal_mesh = bpy.data.meshes.new("HexagonalPlate")
hexagonal_plate = bpy.data.objects.new("HexagonalPlate", hexagonal_mesh)
bpy.context.collection.objects.link(hexagonal_plate)
bmesh_obj = bmesh.new()

# 六角形の頂点計算
half_width = BASE_PLATE_WIDTH / 2
half_height = BASE_PLATE_HEIGHT / 2

hexagon_vertices = [
    # 上辺
    (-half_width + CORNER_CUT_SIZE, half_height, 0),
    (half_width - CORNER_CUT_SIZE, half_height, 0),
    # 右辺
    (half_width, half_height / 2 - CORNER_CUT_SIZE, 0),
    (half_width, -half_height / 2 + CORNER_CUT_SIZE, 0),
    # 下辺
    (half_width - CORNER_CUT_SIZE, -half_height, 0),
    (-half_width + CORNER_CUT_SIZE, -half_height, 0),
    # 左辺
    (-half_width, -half_height / 2 + CORNER_CUT_SIZE, 0),
    (-half_width, half_height / 2 - CORNER_CUT_SIZE, 0),
]

# 頂点をbmeshに追加
bmesh_vertices = []
for vertex in hexagon_vertices:
    bmesh_vertices.append(bmesh_obj.verts.new(vertex))

# 面を作成し、厚みを追加
bmesh_obj.faces.new(bmesh_vertices)
extruded_geometry = bmesh.ops.extrude_face_region(bmesh_obj, geom=bmesh_obj.faces[:])
bmesh.ops.translate(
    bmesh_obj,
    vec=(0, 0, BASE_PLATE_THICKNESS),
    verts=[v for v in extruded_geometry["geom"] if isinstance(v, bmesh.types.BMVert)],
)

# メッシュを更新
bmesh_obj.normal_update()
bmesh_obj.faces.ensure_lookup_table()
bmesh_obj.to_mesh(hexagonal_mesh)
bmesh_obj.free()

# プレートを配置
bpy.context.view_layer.objects.active = hexagonal_plate
hexagonal_plate.select_set(True)
hexagonal_plate.location = (0, 0, BASE_PLATE_THICKNESS / 2)


def add_protrusion_to_object(target_obj, protrusion_name, dimensions, position):
    """オブジェクトに突起物を追加する関数"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position)
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


# 穴径定数
HOLE_M2_5_RADIUS = 1.5
HOLE_M3_RADIUS = 1.75

# 基本穴の位置
MAIN_HOLE_X_SPACING = 15.25

# メインねじ穴を作成
add_hole_to_object(
    hexagonal_plate,
    hole_name="MainHoleLeft",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 1,
    position=(-MAIN_HOLE_X_SPACING, 0, BASE_PLATE_THICKNESS),
)
add_hole_to_object(
    hexagonal_plate,
    hole_name="MainHoleRight",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 1,
    position=(MAIN_HOLE_X_SPACING, 0, BASE_PLATE_THICKNESS),
)

# アーム寸法
ARM_X_SPACING = 14.25
ARM_Y_SPACING = BASE_PLATE_HEIGHT / 4

UPPER_ARM_WIDTH = 18
LOWER_ARM_WIDTH = 23
ARM_HEIGHT = 6
ARM_THICKNESS = 2.5

# 上部アーム突起を作成
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmRight",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, UPPER_ARM_WIDTH),
    position=(ARM_X_SPACING, ARM_Y_SPACING, UPPER_ARM_WIDTH / 2 + ARM_THICKNESS),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmLeft",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, UPPER_ARM_WIDTH),
    position=(-ARM_X_SPACING, ARM_Y_SPACING, UPPER_ARM_WIDTH / 2 + ARM_THICKNESS),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmCenter",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, UPPER_ARM_WIDTH - HOLE_M3_RADIUS * 4),
    position=(0, ARM_Y_SPACING, (UPPER_ARM_WIDTH - HOLE_M3_RADIUS * 2.5) / 2),
)

# 下部アーム突起を作成
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmRight",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, LOWER_ARM_WIDTH),
    position=(ARM_X_SPACING, -ARM_Y_SPACING, LOWER_ARM_WIDTH / 2 + ARM_THICKNESS),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmLeft",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, LOWER_ARM_WIDTH),
    position=(-ARM_X_SPACING, -ARM_Y_SPACING, LOWER_ARM_WIDTH / 2 + ARM_THICKNESS),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmCenter",
    dimensions=(ARM_THICKNESS, ARM_HEIGHT, LOWER_ARM_WIDTH - HOLE_M3_RADIUS * 4),
    position=(0, -ARM_Y_SPACING, (LOWER_ARM_WIDTH - HOLE_M3_RADIUS * 2.5) / 2),
)

# 上部ブリッジ構造を作成
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperBridgeHorizontal",
    dimensions=(ARM_Y_SPACING * 4, ARM_HEIGHT, ARM_THICKNESS),
    position=(0, ARM_Y_SPACING, UPPER_ARM_WIDTH - HOLE_M3_RADIUS * 3.5),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperBridgeVerticalRight",
    dimensions=(ARM_THICKNESS, ARM_X_SPACING + 1.5, ARM_THICKNESS * 2),
    position=(ARM_X_SPACING, 0, UPPER_ARM_WIDTH),
)

# 下部ブリッジ構造を作成
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerBridgeHorizontal",
    dimensions=(ARM_Y_SPACING * 4, ARM_HEIGHT, ARM_THICKNESS),
    position=(0, -ARM_Y_SPACING, LOWER_ARM_WIDTH - HOLE_M3_RADIUS * 3.5),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerBridgeVerticalLeft",
    dimensions=(ARM_THICKNESS, ARM_X_SPACING + 1.5, ARM_THICKNESS * 2),
    position=(-ARM_X_SPACING, 0, UPPER_ARM_WIDTH),
)

# 上部アーム水平穴を作成
add_hole_to_object(
    hexagonal_plate,
    hole_name="UpperArmHoleRight",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 2,
    position=(ARM_X_SPACING, ARM_Y_SPACING, UPPER_ARM_WIDTH - HOLE_M3_RADIUS / 2),
    rotation=(0, math.pi / 2, 0),
)
add_hole_to_object(
    hexagonal_plate,
    hole_name="UpperArmHoleLeft",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 2,
    position=(-ARM_X_SPACING, ARM_Y_SPACING, UPPER_ARM_WIDTH - HOLE_M3_RADIUS / 2),
    rotation=(0, math.pi / 2, 0),
)

# 下部アーム水平穴を作成
add_hole_to_object(
    hexagonal_plate,
    hole_name="LowerArmHoleRight",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 2,
    position=(ARM_X_SPACING, -ARM_Y_SPACING, LOWER_ARM_WIDTH - HOLE_M3_RADIUS / 2),
    rotation=(0, math.pi / 2, 0),
)
add_hole_to_object(
    hexagonal_plate,
    hole_name="LowerArmHoleLeft",
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 2,
    position=(-ARM_X_SPACING, -ARM_Y_SPACING, LOWER_ARM_WIDTH - HOLE_M3_RADIUS / 2),
    rotation=(0, math.pi / 2, 0),
)

