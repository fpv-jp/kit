import bpy
import bmesh
import math

# 既存オブジェクトを削除
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

# 板を65mm x 212mm x 2.8mmで作成（中央を原点に配置）
plate_width = 65
plate_height = 212
plate_depth = 2.8

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(0, 0, plate_depth / 2),
)
plate = bpy.context.object
plate.name = "Plate"
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


def create_triangle(vertices):
    mesh = bpy.data.meshes.new("Triangle_Mesh")
    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(verts)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


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


add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(40, 176, 15),
    cut_position=(0, 0, 0),
    # cut_rotation=(0, 0, math.radians(45)),
    cut_rotation=(0, 0, 0),
)


# 既存の穴の位置
holes = [
    (24.5, 65.0),
    (-24.5, 65.0),
    (24.5, 7),
    (-24.5, 7),
]

# 既存の穴の位置
holes2 = [
    (16.4, 101.0),
    (-16.4, 101.0),
    #------------------
    (26, 39.75),
    (-26, 39.75),
    #------------------
    (28.4, -25.15),
    (-28.4, -25.15),
    #------------------
    (18.9, -101.8),
    (-18.9, -101.8),
]

M2 = 1.25
M2_5 = 1.5
M3 = 1.75

# 既存の穴を作成
for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2_5,
        depth=plate_depth + 10,
        location=(x, y, plate_depth / 2),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)

for i, (x, y) in enumerate(holes2):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M3,
        depth=plate_depth + 10,
        location=(x, y, plate_depth / 2),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


camera_plate_width = 28.5
camera_plate_depth = 1.5
y_offset = 95

for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            (10.5 * 1.5) / 2,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (2.5, 7.5, 12)
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)


for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2_5,
        depth=1.5 + 2,
        location=(
            x_offset,  #
            y_offset,  #
            12 - M2_5 * 2.5,
        ),
        rotation=(0, math.pi / 2, 0),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)


camera_plate_width = 30
camera_plate_depth = 1.5

y_offset = -95

# 左右突起
for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cube_add(
        size=1,  #
        location=(
            x_offset,  #
            y_offset,  #
            4,
        ),
    )
    protrusion = bpy.context.object
    protrusion.scale = (1.5, 6, 8)
    bpy.ops.object.transform_apply(scale=True)
    bool_mod = plate.modifiers.new(name=f"Bool_Protrusion_{side}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = protrusion
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(protrusion, do_unlink=True)

for side in [-1, 1]:
    x_offset = side * (camera_plate_width / 2 - camera_plate_depth / 2)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M2,
        depth=1.5 + 2,
        location=(
            x_offset,  #
            y_offset,  #
            8 - M2 * 2,
        ),
        rotation=(0, math.pi / 2, 0),
    )
    h_hole = bpy.context.object
    h_hole.name = f"HorizontalHole_{side}"
    bool_mod = plate.modifiers.new(name=f"Bool_HHole_{side}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = h_hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(h_hole, do_unlink=True)


# 三角形の穴を作成
triangle_positions = [
    (30, 100, [(-3, 55, 0), (-3, -7, 0), (9, -7, 0)], 180),
    (-30, 100, [(3, 55, 0), (-9, -7, 0), (3, -7, 0)], 180),
    (30, -104, [(3, 80, 0), (-7, -3, 0), (3, -3, 0)], 0),
    (-30, -104, [(-3, 80, 0), (-3, -3, 0), (7, -3, 0)], 0),
]


for i, (x, y, vertices, rotation) in enumerate(triangle_positions):
    theta = math.radians(rotation)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    verts_rot = [
        (
            v[0] * cos_t - v[1] * sin_t,
            v[0] * sin_t + v[1] * cos_t,
            v[2],
        )
        for v in vertices
    ]
    triangle_mesh = create_triangle(verts_rot)
    triangle = bpy.data.objects.new(f"Triangle_Hole_{i}", triangle_mesh)
    bpy.context.collection.objects.link(triangle)
    triangle.location = (x, y, plate_depth / 2)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, plate_depth + 10)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, 0)
    bool_mod = plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


triangle_positions = [
    (
        17,
        81,
        [
            (-3, 35, 0),
            (-3, -7, 0),
            (5, -7, 0),
        ],
        180,
    ),
    (
        -17,
        81,
        [
            (3, 35, 0),
            (-5, -7, 0),
            (3, -7, 0),
        ],
        180,
    ),
    (
        17,
        -85,
        [
            (3, 60, 0),
            (-3, -3, 0),
            (3, -3, 0),
        ],
        0,
    ),
    (
        -17,
        -85,
        [
            (-3, 60, 0),
            (-3, -3, 0),
            (3, -3, 0),
        ],
        0,
    ),
]


for i, (x, y, vertices, rotation) in enumerate(triangle_positions):
    theta = math.radians(rotation)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    verts_rot = [
        (
            v[0] * cos_t - v[1] * sin_t,
            v[0] * sin_t + v[1] * cos_t,
            v[2],
        )
        for v in vertices
    ]
    triangle_mesh = create_triangle(verts_rot)
    triangle = bpy.data.objects.new(f"Triangle_Hole_{i}", triangle_mesh)
    bpy.context.collection.objects.link(triangle)
    triangle.location = (x, y, plate_depth / 2)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, plate_depth)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, 0)
    bool_mod = plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


def add_protrusion_to_object(
    target_obj, protrusion_name, dimensions, position, rotation=(0, 0, 0)
):
    """オブジェクトに突起物を追加する関数"""
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


add_protrusion_to_object(
    plate,
    protrusion_name="LowerArmRight",
    dimensions=(42, 10, plate_depth),
    position=(0, 39.75, plate_depth / 2),
)

add_protrusion_to_object(
    plate,
    protrusion_name="LowerArmRight",
    dimensions=(42, 10, plate_depth),
    position=(0, -25.15, plate_depth / 2),
)

add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(20, 14, 15),
    cut_position=(0, -90, 0),
    # cut_rotation=(0, 0, math.radians(45)),
    cut_rotation=(0, 0, 0),
)

plate.select_set(True)
bpy.context.view_layer.objects.active = plate
