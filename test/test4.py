import bpy
import bmesh
import math

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

plate_width = 46
plate_height = 43
plate_depth = 1.75

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
plate = bpy.context.object
plate.name = "Plate"
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


M2_5 = 1.5

holes = [
    (18.9, -plate_height / 2 + M2_5 * 2.5),
    (-18.9, -plate_height / 2 + M2_5 * 2.5),
]


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


add_protrusion_to_object_rotation(
    plate,
    protrusion_name="UpperArmRight",
    dimensions=(31.8, plate_depth, 8),
    position=(
        0,
        plate_height / 2 - plate_depth / 2,
        4 + plate_depth / 2,
    ),
    rotation=(0, 0, 0),
)


add_protrusion_to_object_rotation(
    plate,
    protrusion_name="UpperArmRight",
    dimensions=(31.8, plate_depth, 8),
    position=(
        0,
        plate_height / 2 - plate_depth / 2 - 23,
        4 + plate_depth / 2,
    ),
    rotation=(0, 0, 0),
)


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
    cut_dimensions=(20, 42, 20),
    cut_position=(
        0,
        -8,
        0,
    ),
    cut_rotation=(0, 0, 0),
)

add_angled_cut_to_protrusion(
    plate,
    cut_name="UpperCornerCut",
    cut_dimensions=(20, 42, 20),
    cut_position=(
        0,
        8,
        10 + plate_depth / 2,
    ),
    cut_rotation=(0, 0, 0),
)

triangle_positions = [
    (30, 0, [(0, 60, 0), (-3, -23, 0), (14, -23, 0)], 180),
    (-30, 0, [(0, 60, 0), (-14, -23, 0), (3, -23, 0)], 180),

    (10, -64, [(0, 60, 0), (-3, -23, 0), (14, -23, 0)], 0),
    (-10, -64, [(0, 60, 0), (-14, -23, 0), (3, -23, 0)], 0),
]


def create_triangle(vertices):
    mesh = bpy.data.meshes.new("Triangle_Mesh")
    bm = bmesh.new()
    verts = [bm.verts.new(v) for v in vertices]
    bm.faces.new(verts)
    bm.to_mesh(mesh)
    bm.free()
    return mesh


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
    triangle.location = (x, y, -1)
    bool_mod = plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)
