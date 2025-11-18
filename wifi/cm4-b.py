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

# CM4のサイズに合わせた寸法
PLATE_WIDTH = 64
PLATE_HEIGHT = 48
PLATE_THICKNESS = 2.25

# 板を作成
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, PLATE_THICKNESS))
main_plate = bpy.context.object
main_plate.name = "CM4_mounting_plate"
main_plate.scale = (PLATE_WIDTH, PLATE_HEIGHT, PLATE_THICKNESS)
bpy.ops.object.transform_apply(scale=True)

M7 = 3.5
X_PITCH = 26.5
Y_PITCH = 18.5

holes = [
    (-X_PITCH, -Y_PITCH),
    (X_PITCH, -Y_PITCH),
    (-X_PITCH, Y_PITCH),
    (X_PITCH, Y_PITCH),
]

for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M7,
        depth=PLATE_THICKNESS + 1,
        location=(
            x,  #
            y,  #
            PLATE_THICKNESS,
        ),
    )
    hole = bpy.context.object
    hole.name = f"Hole{i}"

    bool_mod = main_plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole

    bpy.context.view_layer.objects.active = main_plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


# 中央をくり抜く穴を作成
INNER_CUT_MARGIN = 17.5
inner_cutout_width = PLATE_WIDTH * 2 - INNER_CUT_MARGIN * 2
inner_cutout_height = PLATE_HEIGHT * 2 - INNER_CUT_MARGIN * 2

bpy.ops.mesh.primitive_cube_add(
    size=1,
    location=(
        0,
        0,
        PLATE_THICKNESS / 2,
    ),
)
inner_cutout = bpy.context.object
inner_cutout.scale = (
    inner_cutout_width / 2,
    inner_cutout_height / 2,
    PLATE_THICKNESS * 2,
)
bpy.ops.object.transform_apply(scale=True)

# 板から中央の穴を引く
inner_cutout_modifier = main_plate.modifiers.new(
    name="inner_cutout_boolean", type="BOOLEAN"
)
inner_cutout_modifier.operation = "DIFFERENCE"
inner_cutout_modifier.object = inner_cutout
bpy.context.view_layer.objects.active = main_plate
bpy.ops.object.modifier_apply(modifier=inner_cutout_modifier.name)
bpy.data.objects.remove(inner_cutout, do_unlink=True)


def create_and_apply_protrusion(target_object, protrusion_name, scale, location):
    """指定されたオブジェクトに突起物を追加する"""
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    protrusion_cube = bpy.context.object
    protrusion_cube.name = protrusion_name
    protrusion_cube.scale = scale
    bpy.ops.object.transform_apply(scale=True)

    protrusion_modifier = target_object.modifiers.new(
        name=f"boolean_{protrusion_name}", type="BOOLEAN"
    )
    protrusion_modifier.operation = "UNION"
    protrusion_modifier.object = protrusion_cube

    bpy.context.view_layer.objects.active = target_object
    bpy.ops.object.modifier_apply(modifier=protrusion_modifier.name)
    bpy.data.objects.remove(protrusion_cube, do_unlink=True)


# 突起物の寸法
PROTRUSION_WIDTH = 1.5
PROTRUSION_HEIGHT1 = 6
PROTRUSION_HEIGHT2 = 18
PROTRUSION_DEPTH = 7.5

PROTRUSION_HEIGHT1_PITCH = 41.25
PROTRUSION_HEIGHT2_PITCH = 56.25

protrusion_x = PROTRUSION_HEIGHT2_PITCH / 2 + PROTRUSION_WIDTH / 2

# 左突起物
create_and_apply_protrusion(
    main_plate,
    "left_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1, PROTRUSION_DEPTH),
    location=(-protrusion_x, 0, PLATE_THICKNESS + PROTRUSION_DEPTH / 2),
)
create_and_apply_protrusion(
    main_plate,
    "left_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1 / 1.5, PROTRUSION_DEPTH),
    location=(
        -protrusion_x,
        PROTRUSION_HEIGHT1_PITCH / 3.15,
        PLATE_THICKNESS + PROTRUSION_DEPTH / 2,
    ),
)
create_and_apply_protrusion(
    main_plate,
    "left_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1 / 1.5, PROTRUSION_DEPTH),
    location=(
        -protrusion_x,
        -PROTRUSION_HEIGHT1_PITCH / 3.15,
        PLATE_THICKNESS + PROTRUSION_DEPTH / 2,
    ),
)


# 右突起物
create_and_apply_protrusion(
    main_plate,
    "right_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1, PROTRUSION_DEPTH),
    location=(protrusion_x, 0, PLATE_THICKNESS + PROTRUSION_DEPTH / 2),
)
create_and_apply_protrusion(
    main_plate,
    "right_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1 / 1.5, PROTRUSION_DEPTH),
    location=(
        protrusion_x,
        PROTRUSION_HEIGHT1_PITCH / 3.15,
        PLATE_THICKNESS + PROTRUSION_DEPTH / 2,
    ),
)
create_and_apply_protrusion(
    main_plate,
    "right_mounting_protrusion",
    scale=(PROTRUSION_WIDTH, PROTRUSION_HEIGHT1 / 1.5, PROTRUSION_DEPTH),
    location=(
        protrusion_x,
        -PROTRUSION_HEIGHT1_PITCH / 3.15,
        PLATE_THICKNESS + PROTRUSION_DEPTH / 2,
    ),
)


protrusion_y = PROTRUSION_HEIGHT1_PITCH / 2 + PROTRUSION_WIDTH / 2

# 下突起物
create_and_apply_protrusion(
    main_plate,
    "bottom_mounting_protrusion",
    scale=(PROTRUSION_HEIGHT2, PROTRUSION_WIDTH, PROTRUSION_DEPTH),
    location=(0, -protrusion_y, PLATE_THICKNESS + PROTRUSION_DEPTH / 2),
)

# 上突起物
create_and_apply_protrusion(
    main_plate,
    "top_mounting_protrusion",
    scale=(PROTRUSION_HEIGHT2, PROTRUSION_WIDTH, PROTRUSION_DEPTH),
    location=(0, protrusion_y, PLATE_THICKNESS + PROTRUSION_DEPTH / 2),
)


# 三角形の穴を作成
x1 = 30.25
y1 = 22.25
triangle_positions = [
    (x1, y1, [(-3, 3, 0), (-3, -3, 0), (3, -3, 0)], 180),
    (-x1, y1, [(3, 3, 0), (-3, -3, 0), (3, -3, 0)], 180),
    (x1, -y1, [(3, 3, 0), (-3, -3, 0), (3, -3, 0)], 0),
    (-x1, -y1, [(-3, 3, 0), (-3, -3, 0), (3, -3, 0)], 0),
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
    triangle.location = (x, y, PLATE_THICKNESS / 2)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, PLATE_THICKNESS + 2)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, 0)
    bool_mod = main_plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = main_plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)


x1 = 22.5
y1 = 14.5
triangle_positions = [
    (x1, y1, [(-1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 180),
    (-x1, y1, [(1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 180),
    (x1, -y1, [(1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 0),
    (-x1, -y1, [(-1.5, 1.5, 0), (-1.5, -1.5, 0), (1.5, -1.5, 0)], 0),
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
    triangle.location = (x, y, PLATE_THICKNESS)
    bpy.context.view_layer.objects.active = triangle
    triangle.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, PLATE_THICKNESS)}
    )
    bpy.ops.object.mode_set(mode="OBJECT")
    triangle.location = (x, y, PLATE_THICKNESS / 2)
    bool_mod = main_plate.modifiers.new(name=f"Bool_Triangle_{i}", type="BOOLEAN")
    bool_mod.operation = "UNION"
    bool_mod.object = triangle
    bpy.context.view_layer.objects.active = main_plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(triangle, do_unlink=True)
