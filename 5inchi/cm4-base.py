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

main = base.cube_create(scale=(PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS), location=(0, 4, 0))

base.cube_cut(
    target=main,
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_HEIGHT - PLATE_THICKNESS * 2,
        PLATE_THICKNESS + 1,
    ),
    location=(0, 4, 0),
)

base.cube_add(
    target=main,
    scale=(
        PLATE_WIDTH,
        PLATE_THICKNESS / 1.25,
        PLATE_THICKNESS / 1.25,
    ),
    location=(0, 31.5, -PLATE_THICKNESS / 3),
    rotation=(math.radians(55), 0, 0),
)

M3 = 1.8

holes = [
    (-14, -20),
    (14, -20),
    (-14, 20),
    (14, 20),
]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=M3 * 2,
        inner_radius=M3,
        location=(x, y, 0),
        depth=PLATE_THICKNESS,
    )

base.triangle_add(
    target=main,
    vertices=[(-5, 0, 0), (0, 20, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(10, -21, -PLATE_THICKNESS / 2),
)
base.triangle_add(
    target=main,
    vertices=[(0, 20, 0), (5, 0, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(-10, -21, -PLATE_THICKNESS / 2),
)

base.triangle_add(
    target=main,
    vertices=[(-3, 0, 0), (0, -6, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(10, 29, -PLATE_THICKNESS / 2),
)
base.triangle_add(
    target=main,
    vertices=[(0, -6, 0), (3, 0, 0), (0, 0, 0)],
    depth=PLATE_THICKNESS,
    location=(-10, 29, -PLATE_THICKNESS / 2),
)

main.rotation_euler[0] = math.radians(-75)
main.location[1] = -14
main.location[2] = 33

## # ----------------------------------------------------
## # ----------------------------------------------------
## # ----------------------------------------------------

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

base.punch_holes(
    target=hexagonal_plate,
    radius=M3,
    depth=PLATE_THICKNESS + 1,
    height_pos=0,
    holes=[(15.25, 0), (-15.25, 0)],
)

base.join(target=main, obj=hexagonal_plate)
