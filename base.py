import bpy
import bmesh
# import math
# import mathutils

# fmt: off
def init():
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

# === cube ===========

def cube_create(name, scale, location=(0, 0, 0), rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return obj

def cube_add(target, name, scale, location=(0, 0, 0), rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="UNION")

def cube_clear(target, name, scale, location=(0, 0, 0), rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="DIFFERENCE")

def plate_attach(target, name, plates):
    for i, (scale, location, rotation) in enumerate(plates):
        cube_add(target=target, name=f"{name}_{i}", scale=scale, location=location, rotation=rotation or (0, 0, 0))

def plate_cutout(target, name, plates):
    for i, (scale, location, rotation) in enumerate(plates):
        cube_clear(target=target, name=f"{name}_{i}", scale=scale, location=location, rotation=rotation or (0, 0, 0))

def frame_add(target, name, inner, thickness, location=(0, 0, 0), rotation=(0, 0, 0)):
    cube_add(target=target, name=f"{name}_outer", scale=(inner + thickness * 2, inner + thickness * 2, thickness), location=location, rotation=rotation)
    cube_clear(target=target, name=f"{name}_inner", scale=(inner, inner, thickness + 1), location=location, rotation=rotation)

# === cylinder ===========
# The cylinder should be a 32-sided polygon; if it is a 360-sided polygon, it will be difficult to process.

def cylinder_create(name, radius, depth, location=(0, 0, 0), rotation=(0, 0, 0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=vertices, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.transform_apply(scale=True)
    return obj

def cylinder_add(target, name, radius, depth, location=(0, 0, 0), rotation=(0, 0, 0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="UNION")

def cylinder_clear(target, name, radius, depth, location=(0, 0, 0), rotation=(0, 0, 0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="DIFFERENCE")

def mount_pins(target, name, radius, depth, pins, height_pos=0, rotation=(0, 0, 0), vertices=32):
    for i, (x, y) in enumerate(pins):
        cylinder_add(target=target, name=f"{name}_{i}", radius=radius, depth=depth, location=(x, y, height_pos), rotation=rotation, vertices=vertices)

def punch_holes(target, name, radius, depth, holes, height_pos=0, rotation=(0, 0, 0), vertices=32):
    for i, (x, y) in enumerate(holes):
        cylinder_clear(target=target, name=f"{name}_{i}", radius=radius, depth=depth, location=(x, y, height_pos), rotation=rotation, vertices=vertices)

def ring_add(target, name, outer_radius, inner_radius, location, depth, gap=1, rotation=(0, 0, 0), vertices=32):
    cylinder_add(target=target, name=f"{name}_outer", radius=outer_radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    cylinder_clear(target=target, name=f"{name}_inner", radius=inner_radius, depth=depth + gap, location=location, rotation=rotation, vertices=vertices)

# === hexagon ===========

def hexagon_add(target, name, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=6, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="UNION")

def hexagon_clear(target, name, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=6, location=location, rotation=rotation)
    modifier_apply(obj=bpy.context.active_object, target=target, name=name, operation="DIFFERENCE")

# === triangle ===========

def _triangle_apply(target, name, vertices, depth, location, rotation=(0, 0, 0)):
    mesh = bpy.data.meshes.new("Triangle_Mesh")

    bm = bmesh.new()
    face = bm.faces.new([bm.verts.new(v) for v in vertices])
    bm.normal_update()

    extruded = bmesh.ops.extrude_face_region(bm, geom=[face])
    extruded_verts = [ele for ele in extruded["geom"] if isinstance(ele, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=extruded_verts, vec=(0, 0, depth))

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("Triangle_Temp", mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler = rotation
    return obj

def triangle_add(target, name, vertices, depth, location=(0, 0, 0), rotation=(0, 0, 0)):
    obj = _triangle_apply(target=target, name=name, vertices=vertices, depth=depth, location=location, rotation=rotation)
    modifier_apply(obj=obj, target=target, name=name, operation="UNION")

def triangle_clear(target, name, vertices, depth, location=(0, 0, 0), rotation=(0, 0, 0)):
    obj = _triangle_apply(target=target, name=name, vertices=vertices, depth=depth, location=location, rotation=rotation)
    modifier_apply(obj=obj, target=target, name=name, operation="DIFFERENCE")

# === join ===========

def join(target, obj):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()
# fmt: on
