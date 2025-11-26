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


def add_protrusion_to_object(
    target_obj, protrusion_name, dimensions, position, rotation=(0, 0, 0)
):
    """オブジェクトに突起物を追加する関数"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=position, rotation=rotation)
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

    # ブール演算でカットを適用
    cut_modifier = target_obj.modifiers.new(name=f"Cut_{cut_name}", type="BOOLEAN")
    cut_modifier.operation = "DIFFERENCE"
    cut_modifier.object = cut_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=cut_modifier.name)
    bpy.data.objects.remove(cut_obj, do_unlink=True)


# add_protrusion_to_object(
#    hexagonal_plate,
#    protrusion_name="UpperArmRight",
#    dimensions=(55.5, 6, 40.3),
#    position=(
#        0,
#        6,
#        40.3/2+3,
#    ),
#    rotation=(math.radians(-20), 0, 0),
# )


# ----------------------
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmRight",
    dimensions=(28, 2, 6),
    position=(0, -5, 6),
)

width1 = 59.5
height1 = 20


add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmRight",
    dimensions=(2, 5, height1),
    position=(9, 7, 11),
)
add_angled_cut_to_protrusion(
    hexagonal_plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(5, 5, 20),
    cut_position=(9, 4.5, 13.5),
    cut_rotation=(math.radians(-15), 0, 0),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmRight",
    dimensions=(2, 5, height1),
    position=(-9, 7, 11),
)
add_angled_cut_to_protrusion(
    hexagonal_plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(5, 5, 20),
    cut_position=(-9, 4.5, 13.5),
    cut_rotation=(math.radians(-15), 0, 0),
)

# ----------------------
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmRight",
    dimensions=(width1, 2, height1),
    position=(0, 10, 11),
)


# ----------------------
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmRight",
    dimensions=(2, 15, height1),
    position=(
        width1 / 2 - BASE_PLATE_THICKNESS / 2,
        2.5,
        11,
    ),
)
add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="UpperArmRight",
    dimensions=(2, 15, height1),
    position=(
        -width1 / 2 + BASE_PLATE_THICKNESS / 2,
        2.5,
        11,
    ),
)

add_protrusion_to_object(
    hexagonal_plate,
    protrusion_name="LowerArmRight",
    dimensions=(width1, 4, 2),
    position=(0, 0, 2),
)


HOLE_M3_RADIUS = 1.75
MAIN_HOLE_X_SPACING = 15.25

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


def create_cube(name, size, location, scale=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    if scale:
        obj.scale = scale
    else:
        obj.scale = (size, size, size)
    bpy.ops.object.transform_apply(scale=True)
    return obj


def apply_boolean_modifier(target_obj, modifier_obj, operation, modifier_name):
    bool_mod = target_obj.modifiers.new(name=modifier_name, type="BOOLEAN")
    bool_mod.operation = operation
    bool_mod.object = modifier_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)


rect_hole = create_cube("Rect_Hole2", 1, (0, 10, 11.5), (14, 5, 13))
apply_boolean_modifier(hexagonal_plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)

rect_hole = create_cube("Rect_Hole2", 1, (18, 10, 11.5), (14, 5, 13))
apply_boolean_modifier(hexagonal_plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)
rect_hole = create_cube("Rect_Hole2", 1, (25, 2, 11.5), (15, 8, 13))
apply_boolean_modifier(hexagonal_plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)

rect_hole = create_cube("Rect_Hole2", 1, (-18, 10, 11.5), (14, 5, 13))
apply_boolean_modifier(hexagonal_plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)
rect_hole = create_cube("Rect_Hole2", 1, (-25, 2, 11.5), (15, 8, 13))
apply_boolean_modifier(hexagonal_plate, rect_hole, "DIFFERENCE", "Bool_Rect_Hole")
bpy.data.objects.remove(rect_hole, do_unlink=True)
