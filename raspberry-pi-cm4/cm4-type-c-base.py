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

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

XXX = 21
YYY = 50
ZZZ = 2
OFFSET = XXX / 2 - ZZZ / 2.5

# 板を作成
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, OFFSET))
main_plate = bpy.context.object
main_plate.scale = dimensions = (XXX, YYY, 23)
bpy.ops.object.transform_apply(scale=True)


def add_protrusion_to_object(target_obj, dimensions, position, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position, rotation=rotation)
    protrusion_obj = bpy.context.object
    protrusion_obj.scale = dimensions
    bpy.ops.object.transform_apply(scale=True)
    union_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.object = protrusion_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)
    bpy.data.objects.remove(protrusion_obj, do_unlink=True)


def add_angled_cut_to_protrusion(
    target_obj, cut_dimensions, cut_position, cut_rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=cut_position, rotation=cut_rotation
    )
    cut_obj = bpy.context.object
    cut_obj.scale = cut_dimensions
    bpy.ops.object.transform_apply(scale=True)
    cut_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
    cut_modifier.operation = "DIFFERENCE"
    cut_modifier.object = cut_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=cut_modifier.name)
    bpy.data.objects.remove(cut_obj, do_unlink=True)


add_protrusion_to_object(
    main_plate,
    dimensions=(ZZZ, 50.3, 26),
    position=(7, -3, 4),
    rotation=(math.radians(15), 0, 0),
)
add_protrusion_to_object(
    main_plate,
    dimensions=(ZZZ, 50.3, 26),
    position=(-7, -3, 4),
    rotation=(math.radians(15), 0, 0),
)
add_protrusion_to_object(
    main_plate,
    dimensions=(ZZZ, 40, 20),
    position=(0, -11, 14),
    rotation=(math.radians(15), 0, 0),
)

# -------------------------
add_angled_cut_to_protrusion(
    main_plate,
    cut_dimensions=(XXX + 1, YYY - ZZZ * 2, XXX + 10),
    cut_position=(0, 0, 7+ OFFSET),
    cut_rotation=(0, 0, 0),
)


def add_hole_to_object(
    target_obj, hole_radius, hole_depth, position, rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_radius,
        depth=hole_depth,
        location=position,
        rotation=rotation,
    )
    hole_obj = bpy.context.active_object
    difference_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
    difference_modifier.operation = "DIFFERENCE"
    difference_modifier.object = hole_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=difference_modifier.name)
    bpy.data.objects.remove(hole_obj, do_unlink=True)


HOLE_M3_RADIUS = 1.75

# -------------------------
add_hole_to_object(
    main_plate,
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=60,
    position=(7, 0, XXX / 2 - HOLE_M3_RADIUS -0.5  + OFFSET),
    rotation=(math.radians(90), 0, 0),
)
# -------------------------
add_hole_to_object(
    main_plate,
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=60,
    position=(-7, 0, XXX / 2 - HOLE_M3_RADIUS -0.5 + OFFSET),
    rotation=(math.radians(90), 0, 0),
)


M3 = 1.85
X_POS = 14
Y_POS = 20

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]


def create_ring_with_center_hole(
    outer_diameter: float,
    inner_diameter: float,
    location: tuple[float, float, float],
    plate: bpy.types.Object,
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_diameter,
        depth=ZZZ,
        location=(location[0], location[1], 0.2),
    )
    ring = bpy.context.active_object
    union_mod = plate.modifiers.new(name="", type="BOOLEAN")
    union_mod.operation = "UNION"
    union_mod.object = ring
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=union_mod.name)
    bpy.data.objects.remove(ring, do_unlink=True)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_diameter,
        depth=ZZZ + 1.0,
        location=(location[0], location[1], 0),
    )
    hole = bpy.context.active_object
    diff_mod = plate.modifiers.new(name="", type="BOOLEAN")
    diff_mod.operation = "DIFFERENCE"
    diff_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=diff_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


def create_and_apply_protrusion(target_object, scale, location):
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


for i, (x, y) in enumerate(holes):
    create_and_apply_protrusion(
        main_plate,
        scale=(x * 2, M3 * 4, ZZZ),
        location=(0, y, 0.2),
    )

# M3 リングの生成
for i, (x, y) in enumerate(holes):
    create_ring_with_center_hole(
        outer_diameter=M3 * 2, inner_diameter=M3, location=(x, y, 0), plate=main_plate
    )


main_plate.rotation_euler[0] = math.radians(75)
main_plate.location[2] = 28

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

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
    target_obj, hole_radius, hole_depth, position, rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=hole_radius,
        depth=hole_depth,
        location=position,
        rotation=rotation,
    )
    hole_obj = bpy.context.active_object
    difference_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
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

# -------------------------
add_hole_to_object(
    hexagonal_plate,
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 1,
    position=(-MAIN_HOLE_X_SPACING, 0, BASE_PLATE_THICKNESS),
)
# -------------------------
add_hole_to_object(
    hexagonal_plate,
    hole_radius=HOLE_M3_RADIUS,
    hole_depth=BASE_PLATE_THICKNESS + 1,
    position=(MAIN_HOLE_X_SPACING, 0, BASE_PLATE_THICKNESS),
)


bpy.ops.object.select_all(action="DESELECT")
main_plate.select_set(True)
hexagonal_plate.select_set(True)
bpy.context.view_layer.objects.active = main_plate
bpy.ops.object.join()
