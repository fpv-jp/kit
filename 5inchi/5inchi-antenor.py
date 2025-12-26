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

base.init()

M3 = 1.8

BASE_PLATE_WIDTH = 34.0
BASE_PLATE_HEIGHT = 22.0
BASE_PLATE_THICKNESS = 2

hexagonal_mesh = bpy.data.meshes.new("HexagonalPlate")
main = bpy.data.objects.new("HexagonalPlate", hexagonal_mesh)
bpy.context.collection.objects.link(main)
OBJ = bmesh.new()

W = BASE_PLATE_WIDTH / 2  # half width
H = BASE_PLATE_HEIGHT / 2  # half height
C = 4.5  # CORNER_CUT_SIZE

hexagon_vertices = [
    (-W + C + 2, H, 0),
    (W - C - 2, H, 0),
    (W, H / 2 - C, 0),
    (W, -H / 2 + C, 0),
    (W - C, -H, 0),
    (-W + C, -H, 0),
    (-W, -H / 2 + C, 0),
    (-W, H / 2 - C, 0),
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
)
base.cylinder_cut(
    target=main,
    radius=1.8,
    depth=BASE_PLATE_THICKNESS + 2,
    location=(0, 7.0, 0),
)
base.cube_cut(
    target=main,
    scale=(1.0, 7.0, 5.0),
    location=(0, BASE_PLATE_HEIGHT / 2, 0),
)

# claw1 ------------
claw1 = base.cube_create(
    scale=(3, 3, 4),
)
base.cube_cut(
    target=claw1,
    scale=(3, 3, 4),
    location=(0, -1.5, -1.5),
)
claw1.location = (9, 8.5, 2.5)
base.modifier_apply(obj=claw1, target=main)

# claw2 ------------
claw2 = base.cube_create(
    scale=(3, 3, 4),
)
base.cube_cut(
    target=claw2,
    scale=(3, 3, 4),
    location=(0, -1.5, -1.5),
)
claw2.location = (-9, 8.5, 2.5)
base.modifier_apply(obj=claw2, target=main)

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
