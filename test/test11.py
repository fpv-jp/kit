import bpy
import bmesh
import math

# まず現在のスクリーンから3Dビューエリアを探して全削除
view_3d_area = next(
    (area for area in bpy.context.screen.areas if area.type == "VIEW_3D"), None
)
if view_3d_area:
    with bpy.context.temp_override(area=view_3d_area):
        bpy.ops.object.select_all(action="SELECT")
        bpy.ops.object.delete()
else:
    raise RuntimeError(
        "3Dビューが見つかりませんでした。スクリプトを3Dビューで実行してください。"
    )

# ----------------------------------------------------
# ----------------------------------------------------
# ----------------------------------------------------

XXX = 14
YYY = 50
ZZZ = 2
OFFSET = XXX / 2 - ZZZ / 2.5


LLL = 115

# 板を作成
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, LLL, 0))
main_plate = bpy.context.object
main_plate.scale = dimensions = (XXX, YYY, ZZZ)
bpy.ops.object.transform_apply(scale=True)


def add_protrusion_to_object(target_obj, dimensions, position, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position, rotation=rotation)
    protrusion_obj = bpy.context.object
    protrusion_obj.scale = dimensions
    bpy.ops.object.transform_apply(scale=True)
    union_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
    union_modifier.operation = "UNION"
    union_modifier.object = protrusion_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)
    bpy.data.objects.remove(protrusion_obj, do_unlink=True)


add_protrusion_to_object(
    main_plate,
    dimensions=(5, LLL, ZZZ),
    position=(0, LLL / 2, 0),
    rotation=(0, 0, 0),
)

add_protrusion_to_object(
    main_plate,
    dimensions=(ZZZ, LLL, 4),
    position=(0, LLL / 2, 1),
    rotation=(0, 0, 0),
)


add_protrusion_to_object(
    main_plate,
    dimensions=(8, 13, ZZZ),
    position=(0, -2.3, 0),
    #    rotation=(math.radians(-10), 0, 0),
)


def create_and_apply_hole(target_object, radius, depth, location, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation,
    )
    hole_cylinder = bpy.context.active_object
    hole_modifier = target_object.modifiers.new(name="", type="BOOLEAN")
    hole_modifier.operation = "DIFFERENCE"
    hole_modifier.object = hole_cylinder
    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=hole_modifier.name)
    bpy.data.objects.remove(hole_cylinder, do_unlink=True)


M3 = 1.85

create_and_apply_hole(
    main_plate,
    radius=M3,
    depth=30,
    location=(0, -5, 0),
    #    rotation=(math.radians(-10), 0, 0),
)
