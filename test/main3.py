import bpy
import bmesh
import math

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()

plate_width = 80
plate_height = 43
plate_depth = 2.5

bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
plate = bpy.context.object
plate.scale = (plate_width, plate_height, plate_depth)
bpy.ops.object.transform_apply(scale=True)


M5 = 2.5

PITCH = 27.5

holes = [
    (27.2, PITCH/2),
    (-27.2, PITCH/2),
    (31.35, -PITCH/2),
    (-31.35, -PITCH/2),
]

for i, (x, y) in enumerate(holes):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=M5, depth=plate_depth + 10, location=(x, y, 0)
    )
    hole = bpy.context.object
    bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
    bool_mod.operation = "DIFFERENCE"
    bool_mod.object = hole
    bpy.context.view_layer.objects.active = plate
    bpy.ops.object.modifier_apply(modifier=bool_mod.name)
    bpy.data.objects.remove(hole, do_unlink=True)


bpy.ops.mesh.primitive_cylinder_add(
    radius=20, depth=plate_depth + 10, location=(0, 0, 0)
)
hole = bpy.context.object
bool_mod = plate.modifiers.new(name=f"Bool_Hole{i}", type="BOOLEAN")
bool_mod.operation = "DIFFERENCE"
bool_mod.object = hole
bpy.context.view_layer.objects.active = plate
bpy.ops.object.modifier_apply(modifier=bool_mod.name)
bpy.data.objects.remove(hole, do_unlink=True)
