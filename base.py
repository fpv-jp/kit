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

def modifier_apply(target, obj, name="modifier_apply", operation="UNION"):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.solver = "EXACT"  # more robust for coplanar pieces
    modifier.use_self = True
    modifier.double_threshold = 0.0001
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)

# === cube ===========

def cube_create(scale, name="cube_create", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    bpy.ops.object.transform_apply(scale=True)
    return obj

def corner_cut(target, width, height, depth, thickness):
    X = width /2
    Y = height /2

    PX = X+thickness
    PY = Y+thickness 

    S = (thickness*2, thickness*2, depth+thickness)

    plate_cutout(
        target=target,
        plates=[(S, (PX,PY,0), None), (S, (PX,-PY,0), None), (S, (-PX,PY,0), None), (S, (-PX,-PY,0), None),],
    )
    mount_pins(
        target=target,
        radius=thickness,
        depth=depth+thickness,
        pins=[(X, Y),(X, -Y),(-X, Y),(-X, -Y)],
    )

def cube_add(target, scale, name="cube_add", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="UNION")

def cube_cut(target, scale, name="cube_cut", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):  # alias
    bpy.ops.mesh.primitive_cube_add(size=1, scale=scale, location=location, rotation=rotation)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="DIFFERENCE")

def plate_attach(target, plates, name="plate_attach"):
    for i, (scale, location, rotation) in enumerate(plates):
        cube_add(target=target, scale=scale, name=f"{name}_{i}", location=location or (0, 0, 0), rotation=rotation or (0, 0, 0))

def plate_cutout(target, plates, name="plate_cutout"):
    for i, (scale, location, rotation) in enumerate(plates):
        cube_cut(target=target, scale=scale, name=f"{name}_{i}", location=location or (0, 0, 0), rotation=rotation or (0, 0, 0))

def frame_add(target, inner, thickness, name="frame_add", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    cube_add(target=target, scale=(inner + thickness * 2, inner + thickness * 2, thickness), name=f"{name}_outer", location=location, rotation=rotation)
    cube_cut(target=target, scale=(inner, inner, thickness + 1), name=f"{name}_inner", location=location, rotation=rotation)

# === cylinder ===========
# The cylinder should be a 32-sided polygon; if it is a 360-sided polygon, it will be difficult to process.

def cylinder_create(radius, depth, name="cylinder_create", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=vertices, location=location, rotation=rotation)
    obj = bpy.context.object
    obj.name = name
    bpy.ops.object.transform_apply(scale=True)
    return obj

def cylinder_add(target, radius, depth, name="cylinder_add", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="UNION")

def cylinder_cut(target, radius, depth, name="cylinder_cut", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), vertices=32):  # alias
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=location, rotation=rotation, vertices=vertices)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="DIFFERENCE")

def mount_pins(target, radius, depth, pins, name="mount_pins", height_pos=0, rotation=(0.0, 0.0, 0.0), vertices=32):
    for i, (x, y) in enumerate(pins):
        cylinder_add(target=target, radius=radius, depth=depth, name=f"{name}_{i}", location=(x, y, height_pos), rotation=rotation, vertices=vertices)

def punch_holes(target, radius, depth, holes, name="punch_holes", height_pos=0, rotation=(0.0, 0.0, 0.0), vertices=32):
    for i, (x, y) in enumerate(holes):
        cylinder_cut(target=target, radius=radius, depth=depth, name=f"{name}_{i}", location=(x, y, height_pos), rotation=rotation, vertices=vertices)

def ring_add(target, outer_radius, inner_radius, depth, name="ring_add", gap=1, location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0), vertices=32):
    cylinder_add(target=target, radius=outer_radius, depth=depth, name=f"{name}_outer", location=location, rotation=rotation, vertices=vertices)
    cylinder_cut(target=target, radius=inner_radius, depth=depth + gap, name=f"{name}_inner", location=location, rotation=rotation, vertices=vertices)

# === hexagon ===========

def hexagon_add(target, radius, depth, location, name="hexagon_add", rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=6, location=location, rotation=rotation)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="UNION")

def hexagon_clear(target, radius, depth, location, name="hexagon_clear", rotation=(0.0, 0.0, 0.0)):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=6, location=location, rotation=rotation)
    modifier_apply(target=target, obj=bpy.context.active_object, name=name, operation="DIFFERENCE")

def hexagon_cut(target, radius, depth, location, name="hexagon_cut", rotation=(0.0, 0.0, 0.0)):  # alias
    hexagon_clear(target=target, radius=radius, depth=depth, location=location, name=name, rotation=rotation)

# === triangle ===========

def _triangle_apply(vertices, depth, location, rotation=(0.0, 0.0, 0.0)):
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

def triangle_add(target, vertices, depth, name="triangle_add", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    obj = _triangle_apply(vertices=vertices, depth=depth, location=location, rotation=rotation)
    modifier_apply(target=target, obj=obj, name=name, operation="UNION")

def triangle_cut(target, vertices, depth, name="triangle_clear", location=(0.0, 0.0, 0.0), rotation=(0.0, 0.0, 0.0)):
    obj = _triangle_apply(vertices=vertices, depth=depth, location=location, rotation=rotation)
    modifier_apply(target=target, obj=obj, name=name, operation="DIFFERENCE")

# === join ===========

def join(target, obj):
    bpy.ops.object.select_all(action="DESELECT")
    target.select_set(True)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.join()
# fmt: on
