import bpy
import bmesh
import math
import mathutils


# fmt: off
for area in bpy.context.screen.areas:
    if area.type == "VIEW_3D":
        with bpy.context.temp_override(area=area):
            bpy.ops.object.select_all(action="SELECT")
            bpy.ops.object.delete()
        break
else:
    raise RuntimeError("It appears that no 3D View was found. Please run the script in a 3D View.")

def modifier_apply(obj, target, name, operation):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)

def primitive_cube_add(target, name, operation, scale, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation=operation)

def primitive_cylinder_add(target, name, operation, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation=operation)

def primitive_triangle_add(target, name, operation, vertices, depth, location, rotation=(0, 0, 0)):
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

def join(target, obj):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()
# fmt: on

# main -----------------------------------
WALL = 2
MAIN_WIDTH = 75.5 + WALL
MAIN_HEIGHT = 77.5 + WALL
MAIN_THICKNESS = 15 + WALL

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

X_POS = 18.6
Y_POS = 0
holes = [
    (-X_POS / 2, Y_POS),
    (X_POS / 2, Y_POS),
    (-X_POS * 1.5, Y_POS),
    (X_POS * 1.5, Y_POS),
]

for i, (x, y) in enumerate(holes):
    primitive_cube_add(
        target=main,
        name="Cube",
        operation="UNION",
        scale=(
            6.5,
            MAIN_HEIGHT + 4.6 * 2,
            WALL,
        ),
        location=(x, y, -MAIN_THICKNESS / 2 + WALL / 2),
    )
    primitive_cube_add(
        target=main,
        name="Cube",
        operation="DIFFERENCE",
        scale=(
            6.5,
            MAIN_HEIGHT + 4.6 * 2,
            MAIN_THICKNESS,
        ),
        location=(x, y, WALL),
    )

X_POS = 34.0 / 2
Y_POS = 52.5 / 2
M2_5 = 1.5

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]


for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="DIFFERENCE",
        radius=M2_5,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )


primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        MAIN_WIDTH - WALL,
        MAIN_HEIGHT - WALL,
        MAIN_THICKNESS,
    ),
    location=(0, 0, WALL),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        MAIN_WIDTH - WALL + WALL,
        MAIN_HEIGHT - WALL - 3.8 * 2,
        MAIN_THICKNESS,
    ),
    location=(0, 0, WALL + 5.8),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        63,
        45,
        MAIN_THICKNESS,
    ),
    location=(0, 0, 0),
)

# main2 -----------------------------------
MAIN2_WIDTH = 100.15
MAIN2_HEIGHT = 74.25
MAIN2_THICKNESS = 2.0

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main2 = bpy.context.object
main2.scale = (MAIN2_WIDTH, MAIN2_HEIGHT, MAIN2_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

hole_gap_y = 8.6
prop_x1 = 93.15 / 2
prop_y1 = 49.0 / 2
M3 = 1.75
M2 = 1.5

holes = [
    (prop_x1, prop_y1 + hole_gap_y),
    (-prop_x1, prop_y1 + hole_gap_y),
    (prop_x1, -prop_y1 + hole_gap_y),
    (-prop_x1, -prop_y1 + hole_gap_y),
    (prop_x1 - 58.5, prop_y1 + hole_gap_y),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main2,
        name="Cylinder",
        operation="DIFFERENCE",
        radius=M3,
        depth=MAIN2_THICKNESS + 1,
        location=(x, y, 0),
    )

primitive_cube_add(
    target=main2,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(MAIN2_WIDTH - 15, MAIN2_HEIGHT - 15, MAIN2_THICKNESS),
    location=(0, 0, 0),
)

main2.rotation_euler = (0, 0, math.radians(90))
main2.location = (0, 0, -7.5)

primitive_cylinder_add(
    target=main,
    name="Cylinder",
    operation="DIFFERENCE",
    radius=M3,
    depth=MAIN2_THICKNESS + 3,
    location=(-(prop_y1 + hole_gap_y), prop_x1 - 58.5, -7.5),
)

join(main, main2)
