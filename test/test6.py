import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# カメラV2基板サイズ 25mm x 16.5mm x 1.5mmプレート
plate_width = 25
plate_height = 16.5
plate_depth = 1.5
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, plate_depth))
plate = bpy.context.object
plate.name = "Plate"
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)

# ネジ穴位置
M1_5 = 1
M2 = 1.25
M2_5 = 1.5

holes = [
    (-10.5, -6.25),
    (10.5, -6.25),
    (-10.5, 6.25),
    (10.5, 6.25),
]

for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2,
        depth=plate_depth + 10,
        location=(
            x,  #
            y,  #
            plate_depth,
        ),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"

    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole

    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)

protrusion_width = 7.5
protrusion_height = 23.5

# 左右突起
for side in [-1, 1]:
    x_offset = side * (9.6 + plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            0,  #
            plate_depth + protrusion_height / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        plate_depth,  #
        protrusion_width,  #
        protrusion_height,
    )
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)
    
    h=9.415
#-----------
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            17,  #
            h/2+plate_depth/2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        plate_depth,  #
        5.82,  #
        h,
    )
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)

#-----------
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            10,  #
            13,
        ),
        rotation=( math.radians(-30),0, 0,),
    )
    protrusion = bpy.context.object
    protrusion.scale = (
        plate_depth,  #
        20,  #
        5,
    )
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)

# 左右突起に水平穴を追加
for side in [-1, 1]:
    x_offset = side * (plate_width / 2 - plate_depth / 2)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2_5,
        depth=1.5 + 29,
        location=(
            x_offset,  #
            0,  #
            protrusion_height - M2_5 * 1.5,
        ),
        rotation=(
            0,
            math.pi / 2,
            0,
        ),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)

    bpy.ops.mesh.primitive_cylinder_add(
        radius=M1_5,
        depth=1.5 + 29,
        location=(
            x_offset,  #
            17,  
            9,
        ),
        rotation=(
            0,
            math.pi / 2,
            0,
        ),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)



def create_hexagon(radius, height):
    """六角形を作成する関数"""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius,
        depth=height,
        vertices=6,
        location=(0, 0, 0),
    )
    return bpy.context.object


hexagon_cutouts = [(0, 0, 6, 0)]

for i, (x, y, radius, rotation) in enumerate(hexagon_cutouts):
    hexagon = create_hexagon(radius, plate_depth + 10)
    hexagon.name = f"Hexagon_Cutout_{i}"
    hexagon.location = (x, y, plate_depth / 2)
    hexagon.rotation_euler = (0, 0, math.radians(rotation))
    bool_mod = plate.modifiers.new(name=f"Bool_Hexagon_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hexagon
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hexagon, do_unlink=True)

plate.select_set(True)
bpy.context.view_layer.objects.active = plate
