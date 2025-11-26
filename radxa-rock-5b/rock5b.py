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
MAIN_WIDTH = 100.15
MAIN_HEIGHT = 74.25
MAIN_THICKNESS = 1.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

M3 = 1.65

hole_gap_y = 8.6
prop_x1 = 93.15 / 2
prop_y1 = 49.0 / 2
M3 = 1.75

holes = [
    (prop_x1, prop_y1 + hole_gap_y),
    (-prop_x1, prop_y1 + hole_gap_y),
    (prop_x1, -prop_y1 + hole_gap_y),
    (-prop_x1, -prop_y1 + hole_gap_y),
    (prop_x1 - 58.5, prop_y1 + hole_gap_y),
    #    (5, -prop_y1+hole_gap_y),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name="Cylinder",
        operation="DIFFERENCE",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

side_height = 11.8
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="UNION",
    scale=(MAIN_WIDTH, MAIN_THICKNESS, side_height),
    location=(
        0,
        (-MAIN_HEIGHT - MAIN_THICKNESS) / 2,
        (side_height - MAIN_THICKNESS) / 2,
    ),
)

main.location = (0, (MAIN_HEIGHT + MAIN_THICKNESS) / 2, 0)

side_height = 12
side_height2 = (side_height - MAIN_THICKNESS) / 2


x = MAIN_WIDTH / 2 - 6.45
y = 14.5
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(6.6, y, 6.5),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2 + 6.5 / 2,
    ),
)


x = x - 8.55
y = 14.5
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(3.6, y, 11.5),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2 + MAIN_THICKNESS,
    ),
)


x = x - 9.80
y = 18
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(5.7, y, side_height),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2,
    ),
)


x = x - 12.7
y = 18
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(5.7, y, side_height),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2,
    ),
)

x = x - 15.5
y = 15.7
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(13.5, y, side_height),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2,
    ),
)


x = x - 19.20
y = 16.1
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(13.5, y, side_height),
    location=(
        x,
        (y - MAIN_THICKNESS) / 2,
        side_height2,
    ),
)


x = x - 26.80
y = 19.8
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(16.1, y, side_height),
    location=(
        x + 9,
        (y - MAIN_THICKNESS) / 2,
        side_height2,
    ),
)

##############################################

main.location = (0, 0, 0)


primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(26, 26, side_height),
    location=(
        17,
        -1,
        0,
    ),
)


primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(51, 7, side_height),
    location=(
        (93.15 - 58.5) / 2,
        (MAIN_HEIGHT - 7) / 2,
        0,
    ),
)


primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(6, 6, side_height),
    location=(
        prop_x1 - 58.5,
        26.5,
        0,
    ),
)


HOLE_M3_RADIUS = 1.75
MAIN_HOLE_X_SPACING = 15.25

gap = -22
gap2 = 4

primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=HOLE_M3_RADIUS,
    depth=MAIN_THICKNESS + 1,
    location=(MAIN_HOLE_X_SPACING + gap, gap2, 0),
)
primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=HOLE_M3_RADIUS,
    depth=MAIN_THICKNESS + 1,
    location=(-MAIN_HOLE_X_SPACING + gap, gap2, 0),
)


M3 = 1.85

holes2 = [
    (41, 3.3),
    (21.3, 23.2),
]

for i, (x, y) in enumerate(holes2):
    primitive_cylinder_add(
        target=main,
        name=f"Hole2{i}",
        operation="DIFFERENCE",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )


primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=2.5,
    depth=MAIN_THICKNESS * 2 + 1,
    location=(-2.5, -17, MAIN_THICKNESS / 2),
)
