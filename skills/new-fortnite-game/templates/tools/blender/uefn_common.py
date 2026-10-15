"""Shared helpers for headless Blender model scripts that feed UEFN (adapted from Casino Royale's tools/blender/common.py).

Conventions (so meshes drop into UEFN without fixing):
  - 1 Blender unit = 1 m. UEFN shows it as 100 cm after the glTF import (Interchange).
  - Z-up, modelled around the pivot (put the pivot where the object should sit on the floor: z = 0 at its base).
  - After the glTF round trip a mesh's X/Y/Z extents in Blender are its X/Y/Z extents in Unreal (Y is mirrored).
    Scene Graph's Left-Up-Forward axes are a Verse-side convention; assets still import in Unreal's XYZ.
  - Fortnite's build grid is 5.12 m (512 cm) and the player is about 1.92 m tall: size modular pieces to the grid.
  - Materials are Principled BSDF; glTF carries base colour, metallic, roughness, normal and emission into UEFN.
  - Budgets (Epic's FortniteReady guidance, not hard limits): LOD0 ~400-2,500 tris simple, 700-6,000 medium,
    1,200-9,000 complex; textures 2048 px or less, power of two. export_glb() fails the build past the budget.

Run through build_models.py:
  blender --background --factory-startup --python tools/blender/build_models.py -- example_prop
"""

import math
import os

import bpy
from mathutils import Vector

OUT_DIR = os.environ.get("MODELS_OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "build", "models"))
TRI_BUDGET = {"simple": 2500, "medium": 6000, "complex": 9000}
MAX_TEXTURE = 2048


# ---------------------------------------------------------------------------- scene
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 1.0
    return scene


def material(name, color, metallic=0.0, roughness=0.5, emission=None, emission_strength=0.0):
    """A Principled BSDF material (reused by name)."""
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    if emission:
        bsdf.inputs["Emission Color"].default_value = (*emission, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength
    mat.diffuse_color = (*color, 1.0)
    return mat


def _finish(obj, mat, bevel=0.0, segments=2):
    if mat:
        obj.data.materials.append(mat)
    if bevel > 0:
        mod = obj.modifiers.new("Bevel", "BEVEL")
        mod.width = bevel
        mod.segments = segments
        mod.limit_method = "ANGLE"
    return obj


def box(name, size, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, bevel=0.0, segments=2):
    """An axis-aligned box of `size` (x, y, z) metres centred on `loc`, rotated by `rot` (degrees)."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc, rotation=[math.radians(a) for a in rot])
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    return _finish(obj, mat, bevel, segments)


def cylinder(name, radius, depth, loc=(0, 0, 0), rot=(0, 0, 0), mat=None, verts=24, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc,
                                        rotation=[math.radians(a) for a in rot])
    obj = bpy.context.active_object
    obj.name = name
    return _finish(obj, mat, bevel)


def join(objects, name):
    """Applies modifiers and joins objects into one mesh object named `name`."""
    bpy.ops.object.select_all(action="DESELECT")
    for o in objects:
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        for m in list(o.modifiers):
            bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.context.view_layer.objects.active = objects[0]
    bpy.ops.object.join()
    obj = bpy.context.active_object
    obj.name = obj.data.name = name
    return obj


# ---------------------------------------------------------------------------- output
def finish_mesh(obj, uv_size=1.0, smooth_angle=50.0):
    """Applies modifiers and transforms, box-projects UVs (1 UV unit = `uv_size` m) and smooths by angle with
    face-area weighted normals (big flat faces stay flat; bevels read as round)."""
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    for m in list(obj.modifiers):
        bpy.ops.object.modifier_apply(modifier=m.name)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    if not obj.data.uv_layers:
        obj.data.uv_layers.new(name="UVMap")
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.cube_project(cube_size=uv_size)
    bpy.ops.object.mode_set(mode="OBJECT")
    if smooth_angle:
        bpy.ops.object.shade_smooth_by_angle(angle=math.radians(smooth_angle))
        mod = obj.modifiers.new("WeightedNormal", "WEIGHTED_NORMAL")
        mod.mode = "FACE_AREA"
        mod.keep_sharp = True
        bpy.ops.object.modifier_apply(modifier=mod.name)


def triangles(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def check_textures():
    """Fails on images that are too big or not power-of-two (UEFN wants mips; non-mip textures fail validation)."""
    for img in bpy.data.images:
        w, h = img.size
        if w == 0:
            continue
        if max(w, h) > MAX_TEXTURE or (w & (w - 1)) or (h & (h - 1)):
            raise RuntimeError("texture %s is %dx%d: use a power of two <= %d" % (img.name, w, h, MAX_TEXTURE))


def export_glb(obj, filename, budget="medium", uv_size=1.0):
    """Exports one object to OUT_DIR/<filename>.glb and prints a MODEL line. Raises if it is over budget."""
    os.makedirs(OUT_DIR, exist_ok=True)
    finish_mesh(obj, uv_size)
    tris = triangles(obj)
    if tris > TRI_BUDGET[budget]:
        raise RuntimeError("%s has %d tris, over the %s budget of %d" % (filename, tris, budget, TRI_BUDGET[budget]))
    check_textures()
    path = os.path.abspath(os.path.join(OUT_DIR, filename + ".glb"))
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_apply=True,
                              export_yup=True, export_materials="EXPORT")
    d = obj.dimensions
    print("MODEL %s tris=%d size_cm=(%.0f, %.0f, %.0f) -> %s" % (filename, tris, d.x * 100, d.y * 100, d.z * 100, path))
    return path


def render_preview(objects, filename, cam_dir=(1.0, -1.2, 0.6), size=(900, 900), scale_ref=True):
    """Renders `objects` to OUT_DIR/previews/<filename>.png (EEVEE, 3-point light). With scale_ref, a 1.92 m
    grey pillar (Fortnite player height) stands beside the model so scale is obvious in the review."""
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = size
    world = bpy.data.worlds.new("PreviewWorld")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.08, 0.08, 0.1, 1.0)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
    scene.world = world

    bpy.context.view_layer.update()
    lo, hi = Vector((1e9,) * 3), Vector((-1e9,) * 3)
    for o in objects:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo, hi = Vector(map(min, lo, w)), Vector(map(max, hi, w))
    if scale_ref:
        ref = box("ScaleRef_1m92", (0.4, 0.4, 1.92), loc=(hi.x + 0.6, (lo.y + hi.y) / 2, 0.96),
                  mat=material("M_ScaleRef", (0.5, 0.5, 0.5), roughness=0.8))
        objects = list(objects) + [ref]
        lo, hi = Vector(map(min, lo, Vector((hi.x + 0.4, lo.y, 0)))), Vector(map(max, hi, Vector((hi.x + 0.8, hi.y, 1.92))))
    center, radius = (lo + hi) / 2, max((hi - lo).length / 2, 0.05)

    cam_data = bpy.data.cameras.new("PreviewCam")
    cam_data.lens = 70
    cam = bpy.data.objects.new("PreviewCam", cam_data)
    scene.collection.objects.link(cam)
    fov = 2 * math.atan(cam_data.sensor_width / (2 * cam_data.lens))
    cam.location = center + Vector(cam_dir).normalized() * (radius / math.sin(fov / 2) * 1.08)
    cam.rotation_euler = (center - cam.location).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    for name, offset, energy in (("Key", (2, -2, 3), 220), ("Fill", (-3, -1, 1), 70), ("Rim", (-1, 3, 2.5), 160)):
        light = bpy.data.lights.new(name, "AREA")
        light.energy = energy * radius * radius * 4
        light.size = radius * 2
        lo_obj = bpy.data.objects.new(name, light)
        lo_obj.location = center + Vector(offset) * radius * 1.5
        lo_obj.rotation_euler = (center - lo_obj.location).to_track_quat("-Z", "Y").to_euler()
        scene.collection.objects.link(lo_obj)

    out = os.path.abspath(os.path.join(OUT_DIR, "previews", filename + ".png"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    scene.render.filepath = out
    bpy.ops.render.render(write_still=True)
    print("PREVIEW %s" % out)
    return out
