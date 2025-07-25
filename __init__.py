bl_info = {
    "name": "Arma 3 Object Builder Extensions",
    "description": "Extensions for Arma 3 Object Builder",
    "author": "Mikk, SXDIST",
    "blender": (4, 5, 0),
    "category": "3D View"
}

import bpy
from . import panel, operators, properties

def ensure_lodnoshadow(scene):
    resolution_lods = scene.a3obe_resolution_lods
    if not any(p.name == 'lodnoshadow' for p in resolution_lods.named_properties):
        prop = resolution_lods.named_properties.add()
        prop.name = 'lodnoshadow'
        prop.value = '1'

    geometry_lod = scene.a3obe_geometry_lod
    if not any(p.name == 'autocenter' for p in geometry_lod.named_properties):
        prop = geometry_lod.named_properties.add()
        prop.name = 'autocenter'
        prop.value = '0'

def on_scene_load(dummy):
    for scene in bpy.data.scenes:
        ensure_lodnoshadow(scene)

def register():
    for cls in (
        properties.A3OBE_PG_NamedProperty,
        properties.A3OBE_PG_ResolutionLODs,
        properties.A3OBE_PG_GeometryLOD,
        operators.A3OBE_OT_GenerateLODs,
        operators.A3OBE_OT_AddNamedProperty_Resolution,
        operators.A3OBE_OT_AddNamedProperty_Geometry,
        operators.A3OBE_OT_RemoveNamedProperty_Resolution,
        operators.A3OBE_OT_RemoveNamedProperty_Geometry,
        panel.A3OBE_PT_AutoLOD,
    ):
        try:
            bpy.utils.register_class(cls)
        except ValueError:
            pass

    bpy.types.Scene.a3obe_resolution_lods = bpy.props.PointerProperty(type=properties.A3OBE_PG_ResolutionLODs)
    bpy.types.Scene.a3obe_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_GeometryLOD)

    if on_scene_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(on_scene_load)

def unregister():
    if on_scene_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(on_scene_load)

    del bpy.types.Scene.a3obe_resolution_lods
    del bpy.types.Scene.a3obe_geometry_lod

    for cls in reversed((
        panel.A3OBE_PT_AutoLOD,
        operators.A3OBE_OT_RemoveNamedProperty_Geometry,
        operators.A3OBE_OT_RemoveNamedProperty_Resolution,
        operators.A3OBE_OT_AddNamedProperty_Geometry,
        operators.A3OBE_OT_AddNamedProperty_Resolution,
        operators.A3OBE_OT_GenerateLODs,
        properties.A3OBE_PG_GeometryLOD,
        properties.A3OBE_PG_ResolutionLODs,
        properties.A3OBE_PG_NamedProperty,
    )):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass