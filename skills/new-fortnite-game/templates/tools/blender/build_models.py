"""Builds models headless and writes .glb files + preview renders to build/models (adapted from Casino Royale).

  blender --background --factory-startup --python tools/blender/build_models.py -- example_prop [other_module ...]

Each module has a build() function that uses uefn_common. Then import build/models/*.glb into UEFN
(see the new-fortnite-game skill, references/asset-pipeline.md).
"""

import importlib
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if not args:
    print("usage: blender --background --factory-startup --python build_models.py -- <module> [...]")
    sys.exit(2)
failed = []
for name in args:
    try:
        importlib.import_module(name).build()
    except Exception:  # noqa: BLE001 - report every failure, keep building the rest
        traceback.print_exc()
        failed.append(name)
print("BUILD_DONE failed=%s" % ",".join(failed))
sys.exit(1 if failed else 0)
