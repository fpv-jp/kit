import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()


def add_protrusion_to_object_rotation(
    target_obj, protrusion_name, dimensions, position, rotation
):
    bpy.ops.mesh.primitive_cube_add(size=1, location=position, rotation=rotation)
    protrusion_obj = bpy.context.object
    protrusion_obj.scale = dimensions
    bpy.ops.object.transform_apply(scale=True)

    union_modifier = target_obj.modifiers.new(
        name=f"Union_{protrusion_name}", type="BOOLEAN"
    )
    union_modifier.operation = "UNION"
    union_modifier.object = protrusion_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=union_modifier.name)
    bpy.data.objects.remove(protrusion_obj, do_unlink=True)


def add_angled_cut_to_protrusion(
    target_obj, cut_name, cut_dimensions, cut_position, cut_rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=cut_position, rotation=cut_rotation
    )
    cut_obj = bpy.context.object
    cut_obj.name = f"Cut_{cut_name}"
    cut_obj.scale = cut_dimensions
    bpy.ops.object.transform_apply(scale=True)
    cut_modifier = target_obj.modifiers.new(name=f"Cut_{cut_name}", type="BOOLEAN")
    cut_modifier.operation = "DIFFERENCE"
    cut_modifier.object = cut_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=cut_modifier.name)
    bpy.data.objects.remove(cut_obj, do_unlink=True)


bar_depth = 3.5
plate_depth = 1.75

plate_width = 37
plate_height = 37


bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
plate = bpy.context.object
plate.name = "Plate"
plate.scale = (plate_width, plate_height, bar_depth + plate_depth)
bpy.ops.object.transform_apply(scale=True)


add_protrusion_to_object_rotation(
    plate,
    protrusion_name="UpperArmRight",
    dimensions=(31.8, 31.8, plate_depth),
    position=(
        0,
        0,
        -plate_depth,
    ),
    rotation=(0, 0, math.radians(45)),
)

add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(27.5, 18, 10),
    cut_position=(
        0,
        0,
        0,
    ),
    cut_rotation=(0, 0, math.radians(45)),
)

add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(32, 18, 5),
    cut_position=(
        -17.75,
        17.75,
        3,
    ),
    cut_rotation=(0, 0, math.radians(45)),
)
#add_angled_cut_to_protrusion(
#    plate,
#    cut_name="UpperCornerCut",
#    cut_dimensions=(35, 19.11, 10),
#    cut_position=(
#        18,
#        -18,
#        0,
#    ),
#    cut_rotation=(0, 0, math.radians(45)),
#)

add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(35.75, 35.75, bar_depth),
    cut_position=(
        0,
        0,
        plate_depth / 2,
    ),
    cut_rotation=(0, 0, math.radians(45)),
)


# ネジ穴
M3 = 1.75
holes = [
    (-15.25, -15.25),
    (15.25, -15.25),
    (-15.25, 15.25),
    (15.25, 15.25),
]

for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M3,
        depth=plate_depth + 30,
        location=(x, y, plate_depth),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)

plate.select_set(True)
bpy.context.view_layer.objects.active = plate
