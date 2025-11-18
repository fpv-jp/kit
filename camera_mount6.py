import bpy
import bmesh
import math


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

plate_width = 23.5
plate_height = 23.5
plate_depth = 8

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


def primitive_cube_add(target, name, operation, scale, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(
        size=1, scale=scale, location=location, rotation=rotation
    )
    obj = bpy.context.active_object
    bpy.ops.object.transform_apply(scale=True)
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)


def primitive_cylinder_add(
    target, name, operation, radius, depth, location, rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation
    )
    obj = bpy.context.active_object
    modifier = target.modifiers.new(name=name, type="BOOLEAN")
    modifier.operation = operation
    modifier.object = obj
    bpy.context.view_layer.objects.active = target
    bpy.ops.object.modifier_apply(modifier=modifier.name)
    bpy.data.objects.remove(obj, do_unlink=True)


############################################################

cube_width = 20
cube_height = 20

M2 = 1.25
M5 = 2.75

primitive_cylinder_add(
    target=main,
    name="Cylinder",
    operation="UNION",
    radius=M5,
    depth=23.5,
    location=(0, 0, 5.75),
    rotation=(0, math.pi / 2, 0),
)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="UNION",
    scale=(23.5, M5 * 2, 5),
    location=(0, 0, 5.75 - M5),
    # rotation=(math.pi / 1.5, 0, 0),
)

primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=M2,
    depth=24,
    location=(0, 0, 5.75),
    rotation=(0, math.pi / 2, 0),
)

# =======================================

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(cube_width, cube_height, 14),
    location=(0, 0, 4.5),
)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(10.9, 3.6, plate_depth),
    location=(2.0, 2.5, 0),
)

main.rotation_euler = (math.pi / 2.5, 0, 0)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(33, 18, 2),
    location=(0, 3, -11.41),
)

prop_x1 = 13.75
prop_y1 = 9.25
M3 = 1.75

holes = [
    (prop_x1, prop_y1),
    (-prop_x1, prop_y1),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name="Cylinder",
        operation="DIFFERENCE",
        radius=M3,
        depth=2.5,
        location=(x, y, -11.41),
    )
