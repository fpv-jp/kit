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


PLATE_WIDTH = 35
PLATE_HEIGHT = 40
PLATE_THICKNESS = 1.5

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


ARM_HEIGHT = 4.3
ARM_HEIGHT2 = ARM_HEIGHT / 2 + PLATE_THICKNESS / 2

primitive_cube_add(
    target=main,
    name="Cube",
    operation="UNION",
    scale=(PLATE_WIDTH, PLATE_WIDTH, ARM_HEIGHT),
    location=(0, 0, 2.6),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        PLATE_WIDTH - PLATE_THICKNESS * 2,
        ARM_HEIGHT,
    ),
    location=(0, 0, ARM_HEIGHT2),
)

primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(27.5, 27.5, ARM_HEIGHT),
    location=(0, 0, 0),
)
primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(10, 7.5, ARM_HEIGHT),
    location=(PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(10, 7.5, ARM_HEIGHT),
    location=(-PLATE_WIDTH / 2, PLATE_WIDTH / 2, ARM_HEIGHT2),
)
primitive_cube_add(
    target=main,
    name="Cube",
    operation="DIFFERENCE",
    scale=(21, 21, ARM_HEIGHT),
    location=(0, -PLATE_WIDTH / 2, ARM_HEIGHT2),
)


PLATE_WIDTH

M3 = 1.85

X_POS = 14
Y_POS = 20

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
