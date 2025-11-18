import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# カメラV2基板サイズ 25mm x 16.5mm x 1.5mmプレート
plate_width = 35
plate_height = 35
plate_depth = 1.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
plate = bpy.context.object
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)

# ネジ穴
M3 = 1.85
X_POS = 14
Y_POS = 20

holes = [
    (-X_POS, -Y_POS),
    (X_POS, -Y_POS),
    (-X_POS, Y_POS),
    (X_POS, Y_POS),
]


def create_ring_with_center_hole(
    outer_diameter: float,
    inner_diameter: float,
    location: tuple[float, float, float],
    plate: bpy.types.Object,
):
    """リングをプレートに接着し、中心穴をプレートに貫通させる"""

    # 外側リング（プレートに結合）
    bpy.ops.mesh.primitive_cylinder_add(
        radius=outer_diameter,
        depth=plate_depth,
        location=(location[0], location[1], 0),
    )
    ring = bpy.context.active_object

    # プレートとUNION結合
    union_mod = plate.modifiers.new(name="Union_Ring", type="BOOLEAN")
    union_mod.operation = "UNION"
    union_mod.object = ring
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=union_mod.name)
    bpy.data.objects.remove(ring, do_unlink=True)

    # 穴（リングとプレートの両方に貫通）
    bpy.ops.mesh.primitive_cylinder_add(
        radius=inner_diameter,
        depth=10,  # 貫通確実に
        location=(location[0], location[1], 0),
    )
    hole = bpy.context.active_object

    diff_mod = plate.modifiers.new(name="Hole_Cut", type="BOOLEAN")
    diff_mod.operation = "DIFFERENCE"
    diff_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=diff_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


for i, (x, y) in enumerate(holes):
    create_ring_with_center_hole(
        outer_diameter=M3 * 2, inner_diameter=M3, location=(x, y, 0), plate=plate
    )


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


P_Basic = 32

L_Wall = 21
A_Wall = 1.5
H_Wall = 3.5


add_protrusion_to_object(
    plate,
    dimensions=(L_Wall, A_Wall, H_Wall),
    position=(0, -(P_Basic + A_Wall) / 2, (plate_depth + H_Wall) / 2),
    rotation=(0, 0, 0),
)
add_protrusion_to_object(
    plate,
    dimensions=(A_Wall, L_Wall, H_Wall),
    position=((P_Basic + A_Wall) / 2, 0, (plate_depth + H_Wall) / 2),
    rotation=(0, 0, 0),
)
add_protrusion_to_object(
    plate,
    dimensions=(A_Wall, L_Wall, H_Wall),
    position=(-(P_Basic + A_Wall) / 2, 0, (plate_depth + H_Wall) / 2),
    rotation=(0, 0, 0),
)


def add_angled_cut_to_protrusion(
    target_obj, cut_dimensions, cut_position, cut_rotation=(0, 0, 0)
):
    bpy.ops.mesh.primitive_cube_add(
        size=1, location=cut_position, rotation=cut_rotation
    )
    cut_obj = bpy.context.object
    cut_obj.scale = cut_dimensions
    bpy.ops.object.transform_apply(scale=True)
    cut_modifier = target_obj.modifiers.new(name="", type="BOOLEAN")
    cut_modifier.operation = "DIFFERENCE"
    cut_modifier.object = cut_obj
    bpy.context.view_layer.objects.active = target_obj
    bpy.ops.object.modifier_apply(modifier=cut_modifier.name)
    bpy.data.objects.remove(cut_obj, do_unlink=True)


# -------------------------
add_angled_cut_to_protrusion(
    plate,
    cut_dimensions=(28, 28, 10),
    cut_position=(0, 0, 0),
    cut_rotation=(0, 0, 0),
)

add_angled_cut_to_protrusion(
    plate,
    cut_dimensions=(18, 18, 10),
    cut_position=(0, 9, 0),
    cut_rotation=(0, 0, 0),
)

add_protrusion_to_object(
    plate,
    dimensions=(L_Wall + 4, A_Wall, H_Wall),
    position=(0, (P_Basic + A_Wall) / 2, (plate_depth + H_Wall) / 2),
    rotation=(0, 0, 0),
)
