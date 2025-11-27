import bpy
import bmesh
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

PLATE_WIDTH = 28
PLATE_HEIGHT = 58

PLATE_THICKNESS = 4

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 4, 0))
main = bpy.context.object
main.scale = (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

def modifier_apply(obj, target, name, operation):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)

def primitive_cube_add(target, name, operation, scale, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(
        size=1, scale=scale, location=location, rotation=rotation
    )
    modifier_apply(
        obj=bpy.context.active_object, target=target, name=name, operation=operation
    )

def primitive_cylinder_add(
    target, name, operation, radius, depth, location, rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation
    )
    modifier_apply(
        obj=bpy.context.active_object, target=target, name=name, operation=operation
    )

def primitive_triangle_add(
    target, name, operation, vertices, depth, location, rotation=(0, 0, 0)
):
    mesh = bpy.data.meshes.new("Triangle_Mesh")
    bm = bmesh.new()
    bm_verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(bm_verts)
    bm.to_mesh(mesh)
    bm.free()
    obj = bpy.data.objects.new("Triangle_Temp", mesh)
    bpy.context.collection.objects.link(obj)

    obj.location = location
    obj.rotation_euler = rotation
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, depth)})
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode="OBJECT")

    modifier_apply(obj=obj, target=target, name=name, operation=operation)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_HEIGHT - PLATE_THICKNESS * 2,
        PLATE_THICKNESS + 1,
    ),
    location=(0, 4, 0),
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
    primitive_cylinder_add(
        target=main,
        name=f"Ring{i}",
        operation="UNION",
        radius=M3 * 2,
        depth=PLATE_THICKNESS,
        location=(x, y, 0),
    )
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="DIFFERENCE",
        radius=M3,
        depth=PLATE_THICKNESS + 1,
        location=(x, y, 0),
    )

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="UNION",
    vertices=[(0, 10, 0), (-6, 0, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(10, -17, -PLATE_THICKNESS / 2),
)

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="UNION",
    vertices=[(0, 10, 0), (6, 0, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(-10, -17, -PLATE_THICKNESS / 2),
)

main.rotation_euler[0] = math.radians(-75)
main.location[1] = -14
main.location[2] = 29.5

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

BASE_PLATE_WIDTH = 40
BASE_PLATE_HEIGHT = 30
BASE_PLATE_THICKNESS = 2
CORNER_CUT_SIZE = 6.5

hexagonal_mesh = bpy.data.meshes.new("HexagonalPlate")
hexagonal_plate = bpy.data.objects.new("HexagonalPlate", hexagonal_mesh)
bpy.context.collection.objects.link(hexagonal_plate)
bmesh_obj = bmesh.new()

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

bmesh_vertices = []
for vertex in hexagon_vertices:
    bmesh_vertices.append(bmesh_obj.verts.new(vertex))

bmesh_obj.faces.new(bmesh_vertices)
extruded_geometry = bmesh.ops.extrude_face_region(bmesh_obj, geom=bmesh_obj.faces[:])
bmesh.ops.translate(
    bmesh_obj,
    vec=(0, 0, BASE_PLATE_THICKNESS),
    verts=[v for v in extruded_geometry["geom"] if isinstance(v, bmesh.types.BMVert)],
)

bmesh_obj.normal_update()
bmesh_obj.faces.ensure_lookup_table()
bmesh_obj.to_mesh(hexagonal_mesh)
bmesh_obj.free()

bpy.context.view_layer.objects.active = hexagonal_plate
hexagonal_plate.select_set(True)
hexagonal_plate.location = (0, 0, BASE_PLATE_THICKNESS / 2)

# 穴径定数
HOLE_M2_5_RADIUS = 1.5
HOLE_M3_RADIUS = 1.75

# 基本穴の位置
MAIN_HOLE_X_SPACING = 15.25

primitive_cylinder_add(
    target=hexagonal_plate,
    name="Hole",
    operation="DIFFERENCE",
    radius=HOLE_M3_RADIUS,
    depth=PLATE_THICKNESS + 5,
    location=(MAIN_HOLE_X_SPACING, 0, 0),
)
primitive_cylinder_add(
    target=hexagonal_plate,
    name="Hole",
    operation="DIFFERENCE",
    radius=HOLE_M3_RADIUS,
    depth=PLATE_THICKNESS + 5,
    location=(-MAIN_HOLE_X_SPACING, 0, 0),
)

bpy.ops.object.select_all(action="DESELECT")
main.select_set(True)
hexagonal_plate.select_set(True)
bpy.context.view_layer.objects.active = main
bpy.ops.object.join()
