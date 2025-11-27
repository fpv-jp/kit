import bpy
import math
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

# 初期化
base.init()

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

XXX = 21
YYY = 50
ZZZ = 2
OFFSET = XXX / 2 - ZZZ / 2.5

main_plate = base.cube_create(name="main_plate", scale=(XXX, YYY, 23), location=(0, 0, OFFSET))

base.plate_attach(
    target=main_plate,
    name="protrusions",
    plates=[
        ((ZZZ, 50.3, 26), (7, -3, 4), (math.radians(15), 0, 0)),
        ((ZZZ, 50.3, 26), (-7, -3, 4), (math.radians(15), 0, 0)),
        ((ZZZ, 40, 20), (0, -11, 14), (math.radians(15), 0, 0)),
    ],
)

# -------------------------
base.cube_clear(
    target=main_plate,
    name="angled_cut",
    scale=(XXX + 1, YYY - ZZZ * 2, XXX + 10),
    location=(0, 0, 7 + OFFSET),
    rotation=(0, 0, 0),
)

HOLE_M3_RADIUS = 1.75

# -------------------------
base.cylinder_clear(
    target=main_plate,
    name="hole_right",
    radius=HOLE_M3_RADIUS,
    depth=60,
    location=(7, 0, XXX / 2 - HOLE_M3_RADIUS - 0.5 + OFFSET),
    rotation=(math.radians(90), 0, 0),
)
base.cylinder_clear(
    target=main_plate,
    name="hole_left",
    radius=HOLE_M3_RADIUS,
    depth=60,
    location=(-7, 0, XXX / 2 - HOLE_M3_RADIUS - 0.5 + OFFSET),
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

for i, (x, y) in enumerate(holes):
    base.cube_add(
        target=main_plate,
        name=f"m3_base_{i}",
        scale=(x * 2, M3 * 4, ZZZ),
        location=(0, y, 0.2),
    )

for i, (x, y) in enumerate(holes):
    base.cylinder_add(
        target=main_plate,
        name=f"ring_outer_{i}",
        radius=M3 * 2,
        depth=ZZZ,
        location=(x, y, 0.2),
    )
    base.cylinder_clear(
        target=main_plate,
        name=f"ring_inner_{i}",
        radius=M3,
        depth=ZZZ + 1.0,
        location=(x, y, 0),
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
