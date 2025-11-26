import bpy
import sys
import types

text = bpy.data.texts.get("base.py")

module_name = "base"
module = types.ModuleType(module_name)
exec(text.as_string(), module.__dict__)
sys.modules[module_name] = module

import base

# ==========================
#         Example
# ==========================
# main base
MAIN_WIDTH = 35
MAIN_HEIGHT = 40
MAIN_THICKNESS = 1.5
main = base.cube_create(name="main", scale=(MAIN_WIDTH, MAIN_HEIGHT, MAIN_THICKNESS))

# cube booleans
base.cube_add(target=main, name="cube_add_demo", scale=(5, 5, 2), location=(10, 10, 0))
base.cube_clear(target=main, name="cube_clear_demo", scale=(4, 4, 2), location=(-10, -10, 0))

# plate helpers (list of (scale, location, rotation))
base.plate_attach(target=main, name="plate_attach_demo", plates=[((3, 8, 1.5), (0, 15, 0), (0, 0, 0))])
base.plate_cutout(target=main, name="plate_cutout_demo", plates=[((3, 8, 1.5), (0, -15, 0), (0, 0, 0))])

# cylinders (direct + helper wrappers)
base.cylinder_add(target=main, name="cyl_add_demo", radius=2, depth=4, location=(12, 0, 0))
base.cylinder_clear(target=main, name="cyl_clear_demo", radius=2, depth=4, location=(-12, 0, 0))
base.mount_pins(target=main, name="mount_pin_demo", radius=1.5, depth=5, pins=[(15, 5)], height_pos=0)
base.punch_holes(target=main, name="punch_hole_demo", radius=1.2, depth=5, holes=[(-15, 5)], height_pos=0)

# hexagon booleans
base.hexagon_add(target=main, name="hex_add_demo", radius=2.5, depth=3, location=(0, 0, 0))
base.hexagon_clear(target=main, name="hex_clear_demo", radius=2, depth=3, location=(0, 0, 1))

# triangle booleans
base.triangle_add(target=main, name="tri_add_demo", vertices=[(0, 0, 0), (4, 0, 0), (0, 4, 0)], depth=2, location=(8, -8, 0))
base.triangle_clear(target=main, name="tri_clear_demo", vertices=[(0, 0, 0), (3, 0, 0), (0, 3, 0)], depth=2, location=(-8, 8, 0))

# standalone cylinder and join
standalone_cylinder = base.cylinder_create(name="standalone_cylinder", radius=2, depth=4, location=(0, 0, 4))
base.join(main, standalone_cylinder)
