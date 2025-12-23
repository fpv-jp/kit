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

M3 = 1.8

BASE_PLATE_WIDTH = 34.0
BASE_PLATE_HEIGHT = 22.0
BASE_PLATE_THICKNESS = 2
CORNER_CUT_SIZE = 4.5

hexagonal_mesh = bpy.data.meshes.new("HexagonalPlate")
main = bpy.data.objects.new("HexagonalPlate", hexagonal_mesh)
bpy.context.collection.objects.link(main)
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

main.location = (0, 0, -BASE_PLATE_THICKNESS / 2)

x = 12.75

base.punch_holes(
    target=main,
    radius=M3,
    depth=BASE_PLATE_THICKNESS + 2,
    holes=[(x, 0), (-x, 0)],
)

base.cylinder_cut(
    target=main,
    radius=3.25,
    depth=BASE_PLATE_THICKNESS + 2,
#    location=(0, -.5, 0),
)

main.location = (0, 8.25, -BASE_PLATE_THICKNESS / 2)

#################################################

x = 19.5

holes = [(-x, 0), (x, 0)]

for i, (x, y) in enumerate(holes):
    base.ring_add(
        target=main,
        outer_radius=7.5,
        inner_radius=3.25,
        location=(x, y, 0),
        depth=BASE_PLATE_THICKNESS,
    )


##################################################

xy = 20.15
z = 6.7

main.location = (0, 17.5, -(z + BASE_PLATE_THICKNESS) / 2)

base.cube_add(
    target=main,
    scale=(xy + BASE_PLATE_THICKNESS, xy + BASE_PLATE_THICKNESS, z + BASE_PLATE_THICKNESS),
)
base.cube_cut(
    target=main,
    scale=(xy, xy, z),
    location=(0, 0, BASE_PLATE_THICKNESS),
)
base.cube_cut(
    target=main,
    scale=(9.0, 8.5, 10.0),
    location=(0, -xy / 2, 0),
)
