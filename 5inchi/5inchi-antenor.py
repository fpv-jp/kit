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
OBJ = bmesh.new()

W = BASE_PLATE_WIDTH / 2
H = BASE_PLATE_HEIGHT / 2

hexagon_vertices = [
    # 上辺
    (-W + CORNER_CUT_SIZE, H, 0),
    (W - CORNER_CUT_SIZE, H, 0),
    # 右辺
    (W, H / 2 - CORNER_CUT_SIZE, 0),
    (W, -H / 2 + CORNER_CUT_SIZE, 0),
    # 下辺
    (W - CORNER_CUT_SIZE, -H, 0),
    (-W + CORNER_CUT_SIZE, -H, 0),
    # 左辺
    (-W, -H / 2 + CORNER_CUT_SIZE, 0),
    (-W, H / 2 - CORNER_CUT_SIZE, 0),
]

VERTICES = []
for vertex in hexagon_vertices:
    VERTICES.append(OBJ.verts.new(vertex))
OBJ.faces.new(VERTICES)

GEOMETRY = bmesh.ops.extrude_face_region(OBJ, geom=OBJ.faces[:])
bmesh.ops.translate(
    OBJ,
    vec=(0, 0, BASE_PLATE_THICKNESS),
    verts=[v for v in GEOMETRY["geom"] if isinstance(v, bmesh.types.BMVert)],
)

OBJ.normal_update()
OBJ.faces.ensure_lookup_table()
OBJ.to_mesh(hexagonal_mesh)
OBJ.free()

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
    scale=(xy + BASE_PLATE_THICKNESS, xy + BASE_PLATE_THICKNESS + 0.2, z + BASE_PLATE_THICKNESS),
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
