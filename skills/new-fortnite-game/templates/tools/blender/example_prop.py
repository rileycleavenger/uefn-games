"""Example model module: a 1-tile (5.12 m) wide market stall frame. Copy this file per asset family.

  blender --background --factory-startup --python tools/blender/build_models.py -- example_prop
"""

import uefn_common as c

TILE = 5.12  # Fortnite build grid, metres


def build():
    c.reset_scene()
    wood = c.material("M_StallWood", (0.35, 0.2, 0.1), roughness=0.7)
    cloth = c.material("M_StallCloth", (0.75, 0.12, 0.1), roughness=0.9)
    parts = []
    for x in (-TILE / 2 + 0.1, TILE / 2 - 0.1):
        for y in (-0.9, 0.9):
            parts.append(c.box("Post", (0.12, 0.12, 2.6), loc=(x, y, 1.3), mat=wood, bevel=0.01))
    parts.append(c.box("Counter", (TILE - 0.2, 0.6, 0.08), loc=(0, -0.9, 1.0), mat=wood, bevel=0.01))
    parts.append(c.box("Roof", (TILE, 2.2, 0.05), loc=(0, 0, 2.65), rot=(8, 0, 0), mat=cloth))
    stall = c.join(parts, "SM_MarketStall")
    c.export_glb(stall, "SM_MarketStall", budget="simple")
    c.render_preview([stall], "SM_MarketStall")
