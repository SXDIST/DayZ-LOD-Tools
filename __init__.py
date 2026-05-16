bl_info = {
    "name": "Arma 3 Object Builder Extensions",
    "description": "Extensions for Arma 3 Object Builder",
    "author": "SXDIST",
    "blender": (5, 0, 1),
    "version": (5, 0, 2),
    "category": "3D View"
}

import bpy

from . import properties, operators, updater
from .ui import panel
from .constants import PROP_LOD_NO_SHADOW, PROP_AUTOCENTER

_prev_scene_count = 0


def ensure_default_properties(scene):
    res_props = scene.a3obe_resolution_lods.named_properties
    if not any(p.name == PROP_LOD_NO_SHADOW for p in res_props):
        prop = res_props.add()
        prop.name = PROP_LOD_NO_SHADOW
        prop.value = '1'

    geo_props = scene.a3obe_geometry_lod.named_properties
    if not any(p.name == PROP_AUTOCENTER for p in geo_props):
        prop = geo_props.add()
        prop.name = PROP_AUTOCENTER
        prop.value = '0'


def _deferred_init():
    global _prev_scene_count
    for scene in bpy.data.scenes:
        ensure_default_properties(scene)
    _prev_scene_count = len(bpy.data.scenes)
    return None


@bpy.app.handlers.persistent
def on_scene_load(dummy):
    global _prev_scene_count
    for scene in bpy.data.scenes:
        ensure_default_properties(scene)
    _prev_scene_count = len(bpy.data.scenes)


@bpy.app.handlers.persistent
def on_depsgraph_update(scene, depsgraph):
    global _prev_scene_count
    n = len(bpy.data.scenes)
    if n != _prev_scene_count:
        _prev_scene_count = n
        for s in bpy.data.scenes:
            ensure_default_properties(s)


classes = (
    properties.A3OBE_PG_NamedProperty,
    properties.A3OBE_PG_ResolutionLODs,
    properties.A3OBE_PG_GeometryLOD,
    properties.A3OBE_PG_MemoryLOD,
    properties.A3OBE_PG_FireGeometryLOD,
    properties.A3OBE_PG_ViewGeometryLOD,
    properties.A3OBE_PG_ViewPilotLOD,
    operators.A3OBE_OT_GenerateLODs,
    operators.A3OBE_OT_CheckForUpdates,
    operators.A3OBE_OT_InstallUpdate,
    operators.A3OBE_OT_AddNamedProperty_Resolution,
    operators.A3OBE_OT_AddNamedProperty_Geometry,
    operators.A3OBE_OT_AddNamedProperty_Memory,
    operators.A3OBE_OT_AddNamedProperty_FireGeometry,
    operators.A3OBE_OT_AddNamedProperty_ViewGeometry,
    operators.A3OBE_OT_AddNamedProperty_ViewPilot,
    operators.A3OBE_OT_RemoveNamedProperty_Resolution,
    operators.A3OBE_OT_RemoveNamedProperty_Geometry,
    operators.A3OBE_OT_RemoveNamedProperty_Memory,
    operators.A3OBE_OT_RemoveNamedProperty_FireGeometry,
    operators.A3OBE_OT_RemoveNamedProperty_ViewGeometry,
    operators.A3OBE_OT_RemoveNamedProperty_ViewPilot,
    panel.A3OBE_PT_AutoLOD,
)


def register():
    global _prev_scene_count
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.a3obe_resolution_lods = bpy.props.PointerProperty(type=properties.A3OBE_PG_ResolutionLODs)
    bpy.types.Scene.a3obe_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_GeometryLOD)
    bpy.types.Scene.a3obe_memory_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_MemoryLOD)
    bpy.types.Scene.a3obe_fire_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_FireGeometryLOD)
    bpy.types.Scene.a3obe_view_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_ViewGeometryLOD)
    bpy.types.Scene.a3obe_view_pilot_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_ViewPilotLOD)

    if on_scene_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_scene_load)
    if on_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)

    updater.set_local_version(bl_info["version"])
    bpy.app.timers.register(_deferred_init, first_interval=0.0)


def unregister():
    if on_scene_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_scene_load)
    if on_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(on_depsgraph_update)
    del bpy.types.Scene.a3obe_resolution_lods
    del bpy.types.Scene.a3obe_geometry_lod
    del bpy.types.Scene.a3obe_memory_lod
    del bpy.types.Scene.a3obe_fire_geometry_lod
    del bpy.types.Scene.a3obe_view_geometry_lod
    del bpy.types.Scene.a3obe_view_pilot_lod
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
