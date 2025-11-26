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


plate_width = 25
plate_height = 16.5
plate_depth = 1.5

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
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(plate_width - 7, plate_height - 7, plate_depth + 1),
    location=(0, 0, 0),
)


M2 = 1.2
M2_5 = 1.5

holes = [
    (-10.5, -6.25),
    (10.5, -6.25),
    (-10.5, 6.25),
    (10.5, 6.25),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="DIFFERENCE",
        radius=M2,
        depth=plate_depth + 1,
        location=(x, y, 0),
    )


arm_width = 33.5
arm_height = 5

hole_gap = M2 * 1.75

arm_position_y = (plate_height + plate_depth) / 2

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(arm_width, plate_depth, arm_height),
    location=(0, arm_position_y, (arm_height - plate_depth) / 2),
)

primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=M2,
    depth=plate_depth + 1,
    location=(arm_width / 2 - hole_gap, arm_position_y, arm_height / 2.5),
    rotation=(math.pi / 2, 0, 0),
)

primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=M2,
    depth=plate_depth + 1,
    location=(-arm_width / 2 + hole_gap, arm_position_y, arm_height / 2.5),
    rotation=(math.pi / 2, 0, 0),
)
