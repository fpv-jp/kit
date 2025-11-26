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

def modifier_apply_UNION(obj, target, name, operation):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = "UNION"
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)

def modifier_apply_DIFFERENCE(obj, target, name, operation):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = "DIFFERENCE"
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)


def add_cube(target, name, operation, scale, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation=operation)

def primitive_cylinder_add(target, name, operation, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation=operation)

def primitive_hexagon_add(target, name, operation, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=6, location=location, rotation=rotation)
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
MAIN_WIDTH = 35
MAIN_HEIGHT = 40
MAIN_THICKNESS = 1.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS)
bpy.ops.object.transform_apply(scale=True)


# sub -----------------------------------
SUB_WIDTH = 35
SUB_HEIGHT = 40
SUB_THICKNESS = 1.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
sub = bpy.context.object
sub.scale = (SUB_WIDTH, SUB_HEIGHT, SUB_THICKNESS)
bpy.ops.object.transform_apply(scale=True)


sub.rotation_euler[0] = math.radians(-75)
sub.location[1] = -14
sub.location[2] = 5


# join -----------------------------------
join(main, sub)
