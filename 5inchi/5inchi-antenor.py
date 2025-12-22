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

PLATE_WIDTH = 28
PLATE_HEIGHT = 58

PLATE_THICKNESS = 4

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
