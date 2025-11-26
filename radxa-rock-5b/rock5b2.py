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
MAIN_THICKNESS = 2.0

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS)
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
        target=main,
        name="Cylinder",
        operation="DIFFERENCE",
        radius=M3,
        depth=MAIN_THICKNESS + 1,
        location=(x, y, 0),
    )

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(MAIN_WIDTH - 15, MAIN_HEIGHT - 15, MAIN_THICKNESS),
    location=(0, 0, 0),
)

#######################################################
PLATE_WIDTH = 28
PLATE_HEIGHT = 15
PLATE_THICKNESS = 4
ARM_HEIGHT = 7.5

p_x = -28.3
p_y = -33.25

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        PLATE_WIDTH + 0.5,
        8,
        MAIN_THICKNESS + 1,
    ),
    location=(p_x, p_y, 0),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(
        7.5,
        MAIN_HEIGHT - 7,
        MAIN_THICKNESS,
    ),
    location=(-11.925, -3.5, 0),
)

primitive_cylinder_add(
    target=main,
    name="Cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=MAIN_THICKNESS + 1,
    location=(p_x - 18, p_y, 0),
)

primitive_cylinder_add(
    target=main,
    name="Cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=MAIN_THICKNESS + 1,
    location=(p_x + 18, p_y, 0),
)
