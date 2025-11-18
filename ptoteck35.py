import bpy
import bmesh
import math
import mathutils


def clear_scene():
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            with bpy.context.temp_override(area=area):
                bpy.ops.object.select_all(action="SELECT")
                bpy.ops.object.delete()
            break
    else:
        raise RuntimeError(
            "3Dビューが見つかりませんでした。スクリプトを3Dビューで実行してください。"
        )


clear_scene()

plate_width = 63.5
plate_height = 172
plate_depth = 2

gap_depth = plate_depth / 2


bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


def modifier_apply(obj, target, name, operation):
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)


def primitive_cube_add(target, name, operation, scale, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(
        size=1, scale=scale, location=location, rotation=rotation
    )
    modifier_apply(
        obj=bpy.context.active_object, target=target, name=name, operation=operation
    )


def primitive_cylinder_add(
    target, name, operation, radius, depth, location, rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation
    )
    modifier_apply(
        obj=bpy.context.active_object, target=target, name=name, operation=operation
    )


def primitive_triangle_add(
    target, name, operation, vertices, depth, location, rotation=(0, 0, 0)
):
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


M2 = 1.25
M2_5 = 1.5
M3 = 1.75
M48 = 48.25

prop_x = 57.0
prop_y = 48.0

holes = [
    (prop_x, prop_y),
    (prop_x, -prop_y),
    (-prop_x, prop_y),
    (-prop_x, -prop_y),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name="cylinder",
        operation="DIFFERENCE",
        radius=M48,
        depth=plate_depth + 1,
        location=(x, y, 0),
    )


prop_x1 = 13.75
prop_y1 = 83.0

prop_x2 = 28.75
prop_y2 = 0.0

prop_x3 = 7.0
prop_y3 = 43.5

holes = [
    (prop_x1, prop_y1),
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
    (-prop_x1, -prop_y1),
    (prop_x2, prop_y2),
    (-prop_x2, prop_y2),
    (prop_x3, prop_y3),
    (-prop_x3, prop_y3),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name="cylinder",
        operation="DIFFERENCE",
        radius=M2_5,
        depth=plate_depth + 1,
        location=(x, y, 0),
    )


primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(32, 32, plate_depth + 1),
    location=(0, 5, 0),
    rotation=(0, 0, math.radians(45)),
)

prop_x1 = 32.5
prop_y1 = 77.0

holes = [
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
]

for i, (x, y) in enumerate(holes):
    primitive_triangle_add(
        target=main,
        name="Triangle",
        operation="DIFFERENCE",
        vertices=[(0, x, 0), (-9, 0, 0), (9, 0, 0)],
        depth=plate_depth + 1,
        location=(0, y, -plate_depth / 1.5),
    )

vertices = [(0, -20, 0), (-11, 11, 0), (0, 0, 0)]

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="DIFFERENCE",
    vertices=vertices,
    depth=plate_depth + 1,
    location=(-2.5, -23, -plate_depth / 1.5),
)

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="DIFFERENCE",
    vertices=vertices,
    depth=plate_depth + 1,
    location=(2.5, -23, -plate_depth / 1.5),
    rotation=(0, math.radians(180), 0),
)


prop_x1 = 21.5
prop_y1 = 86.0

holes = [
    (prop_x1, prop_y1),
    (prop_x1, -prop_y1),
    (-prop_x1, prop_y1),
    (-prop_x1, -prop_y1),
]


for i, (x, y) in enumerate(holes):
    primitive_cube_add(
        target=main,
        name="CubeCut",
        operation="DIFFERENCE",
        scale=(10, 10, plate_depth + 1),
        location=(x, y, 0),
        rotation=(0, 0, math.radians(45)),
    )


ant_y = -80
ant_z = 3

primitive_cylinder_add(
    target=main,
    name="cylinder",
    operation="UNION",
    radius=3.4,
    depth=12,
    location=(0, 0 + ant_y, 0 + ant_z),
    rotation=(math.radians(25), 0, 0),
)
primitive_cylinder_add(
    target=main,
    name="cylinder",
    operation="DIFFERENCE",
    radius=2.15,
    depth=12.1,
    location=(0, 0 + ant_y, 0 + ant_z),
    rotation=(math.radians(25), 0, 0),
)
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(1.5, 3, 20),
    location=(0, 3 + ant_y, 0 + ant_z),
    rotation=(math.radians(25), 0, 0),
)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(1.5, 3, 20),
    location=(0, 3 + ant_y, 0 + ant_z),
    rotation=(math.radians(25), 0, 0),
)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(5.5, 3, 4),
    location=(14, -3.9, 0),
    rotation=(0, 0, math.radians(45)),
)

#####################################
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(plate_width, plate_height, 10),
    location=(0, 0, -6),
)
