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

plate_width = 16.4 * 2
plate_height = 25
plate_depth = 2.8

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
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)

    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value": (0, 0, depth)})
    bpy.ops.object.mode_set(mode="OBJECT")

    obj.location = location
    obj.rotation_euler = rotation

    modifier_apply(
        obj=bpy.context.active_object, target=target, name=name, operation=operation
    )


############################################################

arm_width = 18.5
arm_side_long = 17
arm_height = 33

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(arm_side_long, arm_width, plate_depth),
    location=(arm_side_long, 0, 0),
)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(plate_width - 12, plate_height - 12, plate_depth + 1),
    location=(0, 0, 0),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(plate_depth, arm_width, arm_height),
    location=(arm_side_long * 1.5, 0, (arm_height - plate_depth) / 2),
)

servo_z_pos = 16
servo_z_pitch = 14.25

M5 = 2.75

primitive_cylinder_add(
    target=main,
    name="cylinder",
    operation="UNION",
    radius=M5,
    depth=plate_depth,
    location=(arm_side_long * 1.5, 0, servo_z_pos + servo_z_pitch),
    rotation=(0, math.pi / 2, 0),
)


############################################################

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(9,arm_width-plate_depth*3,plate_depth + 1),
    location=(19.6, 0, 0),
)


cut_z = 23
cut_y = 12.75


primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(plate_depth + 1, cut_y, cut_z),
    location=(arm_side_long * 1.5, 0, servo_z_pos),
)


M2 = 1.25

primitive_cylinder_add(
    target=main,
    name="cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=plate_depth + 1,
    location=(arm_side_long * 1.5, 0, servo_z_pos + servo_z_pitch),
    rotation=(0, math.pi / 2, 0),
)

primitive_cylinder_add(
    target=main,
    name="cylinder",
    operation="DIFFERENCE",
    radius=M2,
    depth=plate_depth + 1,
    location=(arm_side_long * 1.5, 0, servo_z_pos - servo_z_pitch),
    rotation=(0, math.pi / 2, 0),
)

M3 = 1.75
M7 = 3.75

holes = [
    (16.4, 0),
    (-16.4, 0),
]

gap_y = 16.4 - 7.65

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="UNION",
        radius=M7,
        depth=plate_depth,
        location=(x, y + gap_y, 0),
    )

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="DIFFERENCE",
        radius=M3,
        depth=plate_depth,
        location=(x, y + gap_y, 0),
    )

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="UNION",
    vertices=[(0, 20, 0), (-4, 0, 0), (0, 0, 0)],
    depth=plate_depth,
    location=((arm_side_long + plate_width) / 2, arm_width / 2, gap_depth),
    rotation=(math.pi / 2, 0, 0),
)

primitive_triangle_add(
    target=main,
    name="Triangle",
    operation="UNION",
    vertices=[(0, 20, 0), (-4, 0, 0), (0, 0, 0)],
    depth=plate_depth,
    location=((arm_side_long + plate_width) / 2, -6.45, gap_depth),
    rotation=(math.pi / 2, 0, 0),
)


M15 = 7.75
hhh=11
primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="UNION",
    radius=M15,
    depth=hhh,
    location=(0, -15.5,hhh/2-gap_depth),
)

primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=20,
    depth=13,
    location=(0, -16,14),
    rotation = (11 * math.pi / 14, 0, math.pi)
)

M7 = 3.5
primitive_cylinder_add(
    target=main,
    name="Hole",
    operation="DIFFERENCE",
    radius=M7,
    depth=30,
    location=(0, -16 ,5),
    rotation = (11 * math.pi / 14, 0, math.pi)
)

#M10 = 5
#primitive_cylinder_add(
#    target=main,
#    name="Hole",
#    operation="DIFFERENCE",
#    radius=M10,
#    depth=10,
#    location=(0, -12 ,0),
#    rotation = (11 * math.pi / 14, 0, math.pi)
#)

primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(11,11,11),
    location=(0,-11,0),
    rotation = (11 * math.pi / 14, 0, math.pi)
)
primitive_cube_add(
    target=main,
    name="CubeCut",
    operation="DIFFERENCE",
    scale=(11,11,11),
    location=(0,-4.8,2.25),
#    rotation = (11 * math.pi / 14, 0, math.pi)
)
