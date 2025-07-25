bl_info = {
    "name": "Arma 3 Object Builder Extensions",
    "description": "Extensions for Arma 3 Object Builder",
    "author": "Mikk, SXDIST",
    "blender": (4, 5, 0),
    "category": "3D View"
}

import bpy
from . import panel, operators, properties

def ensure_default_properties(scene):

    res_props = scene.a3obe_resolution_lods.named_properties
    if not any(p.name == 'lodnoshadow' for p in res_props):
        prop = res_props.add()
        prop.name = 'lodnoshadow'
        prop.value = '1'

    geo_props = scene.a3obe_geometry_lod.named_properties
    if not any(p.name == 'autocenter' for p in geo_props):
        prop = geo_props.add()
        prop.name = 'autocenter'
        prop.value = '0'

def on_scene_load(dummy):
    for scene in bpy.data.scenes:
        ensure_default_properties(scene)

classes = (
    properties.A3OBE_PG_NamedProperty,
    properties.A3OBE_PG_ResolutionLODs,
    properties.A3OBE_PG_GeometryLOD,
    operators.A3OBE_OT_GenerateLODs,
    operators.A3OBE_OT_AddNamedProperty_Resolution,
    operators.A3OBE_OT_AddNamedProperty_Geometry,
    operators.A3OBE_OT_RemoveNamedProperty_Resolution,
    operators.A3OBE_OT_RemoveNamedProperty_Geometry,
    panel.A3OBE_PT_AutoLOD,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.a3obe_resolution_lods = bpy.props.PointerProperty(type=properties.A3OBE_PG_ResolutionLODs)
    bpy.types.Scene.a3obe_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_GeometryLOD)
    if on_scene_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_scene_load)

def unregister():
    if on_scene_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_scene_load)
    del bpy.types.Scene.a3obe_resolution_lods
    del bpy.types.Scene.a3obe_geometry_lod
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)