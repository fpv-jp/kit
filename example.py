import bpy
import math
import sys
import types

text = bpy.data.texts.get("base.py")
module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

# 初期化
base.init()

# ==========================
#         Example
# ==========================
# main base
MAIN_WIDTH = 40
MAIN_HEIGHT = 40
MAIN_THICKNESS = 1.5
main = base.cube_create(name="main", scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS))

# cube booleans
base.cube_add(target=main, name="cube_add_demo", scale=(5, 5, 10), location=(8, 8, 0))
base.cube_clear(target=main, name="cube_clear_demo", scale=(4, 4, 2), location=(-8, -8, 0))

# plate helpers (list of (scale, location, rotation))
base.plate_attach(
    target=main,
    name="plate_attach_demo",
    plates=[
        ((20, 3, 20), (0, 15, 0), (0, 0, 0)),
        ((20, 3, 20), (0, -15, 0), (0, 0, 0)),
        ((20, 3, 20), (15, 0, 0), (0, 0, math.radians(90))),
        ((20, 3, 20), (-15, 0, 0), (0, 0, math.radians(90))),
    ],
)

base.plate_cutout(
    target=main,
    name="plate_cutout_demo",
    plates=[
        ((3, 5, 15), (0, 15, 0), (0, 0, 0)),
        ((3, 5, 15), (0, -15, 0), (0, 0, 0)),
        ((3, 5, 15), (15, 0, 0), (0, 0, math.radians(90))),
        ((3, 5, 15), (-15, 0, 0), (0, 0, math.radians(90))),
    ],
)

# cylinders (direct + helper wrappers)
base.cylinder_add(target=main, name="cyl_add_demo", radius=3, depth=15, location=(8, -8, 0))
base.cylinder_clear(target=main, name="cyl_clear_demo", radius=3, depth=2, location=(-8, 8, 0))

base.mount_pins(
    target=main,
    name="mount_pin_demo",
    radius=2.5,
    depth=5,
    height_pos=0,
    pins=[(17, 17), (17, -17), (-17, 17), (-17, -17)],
)

base.punch_holes(
    target=main,
    name="punch_hole_demo",
    radius=1.25,
    depth=6,
    height_pos=0,
    holes=[(17, 17), (17, -17), (-17, 17), (-17, -17)],
)

# hexagon booleans
base.hexagon_add(target=main, name="hex_add_demo", radius=6, depth=6, location=(0, 0, 0))
base.hexagon_clear(target=main, name="hex_clear_demo", radius=3, depth=7, location=(0, 0, 0))

## triangle booleans
base.triangle_add(
    target=main,
    name="tri_add_demo",
    depth=15,
    location=(3, 3, 0),
    vertices=[
        (0, 0, 0),
        (6, 0, 0),
        (0, 6, 0),
    ],
)
base.triangle_clear(
    target=main,
    name="tri_clear_demo",
    depth=10,
    location=(-9, -9, 0),
    vertices=[
        (0, 0, 0),
        (6, 0, 0),
        (0, 6, 0),
    ],
)

# standalone cylinder and join
standalone_cylinder = base.cylinder_create(
    name="standalone_cylinder",
    radius=2,
    depth=4,
    location=(8, 0, 0),
    rotation=(0, math.radians(45), 0),
)
base.join(main, standalone_cylinder)
