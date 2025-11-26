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

M3 = 1.75
M2 = 1.5

#######################################################
PLATE_WIDTH = 28
PLATE_HEIGHT = 16.5
PLATE_THICKNESS = 4
ARM_HEIGHT = 7.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
plate = bpy.context.object
plate.scale = (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
bpy.ops.object.transform_apply(scale=True)


primitive_cube_add(
    target=plate,
    name="Cube",
    operation="UNION",
    scale=(
        PLATE_WIDTH + 15,
        MAIN_THICKNESS,
        ARM_HEIGHT,
    ),
    location=(0, 3, (ARM_HEIGHT - PLATE_THICKNESS) / 2),
)


primitive_cube_add(
    target=plate,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        19.8,
        12.8,
        8,
    ),
    location=(0, 0, 2),
)
primitive_cube_add(
    target=plate,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        PLATE_WIDTH - 6,
        PLATE_HEIGHT - MAIN_THICKNESS * 2,
        8,
    ),
    location=(0, 0, 6),
)


primitive_cylinder_add(
    target=plate,
    name="Cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=MAIN_THICKNESS + 1,
    location=(18, 3, 2),
    rotation=(math.radians(90), 0, 0),
)

primitive_cylinder_add(
    target=plate,
    name="Cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=MAIN_THICKNESS + 1,
    location=(-18, 3, 2),
    rotation=(math.radians(90), 0, 0),
)
