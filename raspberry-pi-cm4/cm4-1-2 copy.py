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


PLATE_WIDTH = 60
PLATE_HEIGHT = 45
PLATE_THICKNESS = 2

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
main = bpy.context.object
main.scale = (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
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


ARM_HEIGHT = 8.5

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(21, PLATE_HEIGHT, ARM_HEIGHT),
    location=(0, 0, ARM_HEIGHT / 2),
)


primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(PLATE_WIDTH, 10, ARM_HEIGHT),
    location=(0, 10, ARM_HEIGHT / 2),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(PLATE_WIDTH, 10, ARM_HEIGHT),
    location=(0, -10, ARM_HEIGHT / 2),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_HEIGHT - PLATE_THICKNESS * 2,
        ARM_HEIGHT,
    ),
    location=(0, 0, ARM_HEIGHT / 2 + PLATE_THICKNESS / 2),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(PLATE_WIDTH - 16, PLATE_HEIGHT - 16, ARM_HEIGHT),
    location=(0, 0, 0),
)

holes = [
    (PLATE_WIDTH / 2, PLATE_HEIGHT / 2),
    (PLATE_WIDTH / 2, -PLATE_HEIGHT / 2),
    (-PLATE_WIDTH / 2, PLATE_HEIGHT / 2),
    (-PLATE_WIDTH / 2, -PLATE_HEIGHT / 2),
]

for i, (x, y) in enumerate(holes):
    primitive_cube_add(
        target=main,
        name="Cube",
        operation="DIFFERENCE",
        scale=(8, 8, PLATE_THICKNESS),
        location=(x, y, 0),
        rotation=(0, 0, math.radians(45)),
    )

CM4_PIN_OFFSET_X = 23.5
CM4_PIN_OFFSET_Y = 16.5

M2_PIN_RADIUS1 = 2.5
PIN_HEIGHT1 = 2.75

M2_PIN_RADIUS2 = 0.85
PIN_HEIGHT2 = 6

holes = [
    (CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
    (CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
    (-CM4_PIN_OFFSET_X, CM4_PIN_OFFSET_Y),
    (-CM4_PIN_OFFSET_X, -CM4_PIN_OFFSET_Y),
]

for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Pin{i}",
        operation="UNION",
        radius=M2_PIN_RADIUS1,
        depth=PIN_HEIGHT1,
        location=(x, y, PIN_HEIGHT1 / 2),
    )
    primitive_cylinder_add(
        target=main,
        name=f"Pin{i}",
        operation="UNION",
        radius=M2_PIN_RADIUS2,
        depth=PIN_HEIGHT2,
        location=(x, y, PIN_HEIGHT2 / 2),
    )
    primitive_cube_add(
        target=main,
        name="Cube",
        operation="UNION",
        scale=(8, 8, PLATE_THICKNESS),
        location=(x, y, 0),
        rotation=(0, 0, math.radians(45)),
    )

M3 = 1.85

X_POS = 14
Y_POS = 24

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]


for i, (x, y) in enumerate(holes):
    primitive_cylinder_add(
        target=main,
        name=f"Ring{i}",
        operation="UNION",
        radius=M3 * 2,
        depth=PLATE_THICKNESS,
        location=(x, y, 0),
    )
    primitive_cylinder_add(
        target=main,
        name=f"Hole{i}",
        operation="DIFFERENCE",
        radius=M3,
        depth=PLATE_THICKNESS + 1,
        location=(x, y, 0),
    )
