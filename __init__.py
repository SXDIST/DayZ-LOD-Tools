bl_info = {
    "name": "Arma 3 Object Builder Extensions",
    "description": "Extensions for Arma 3 Object Builder",
    "author": "Mikk, SXDIST",
    "blender": (4, 5, 0),
    "category": "3D View"
}

import bpy
from . import panel, operators, properties

def register():
    bpy.utils.register_class(properties.A3OBE_PG_NamedProperty)
    bpy.utils.register_class(properties.A3OBE_PG_ResolutionLODs)
    bpy.utils.register_class(properties.A3OBE_PG_GeometryLOD)
    bpy.utils.register_class(operators.A3OBE_OT_GenerateLODs)
    bpy.utils.register_class(operators.A3OBE_OT_AddNamedProperty_Resolution)
    bpy.utils.register_class(operators.A3OBE_OT_AddNamedProperty_Geometry)
    bpy.utils.register_class(operators.A3OBE_OT_RemoveNamedProperty_Resolution)
    bpy.utils.register_class(operators.A3OBE_OT_RemoveNamedProperty_Geometry)
    bpy.utils.register_class(panel.A3OBE_PT_AutoLOD)

    bpy.types.Scene.a3obe_resolution_lods = bpy.props.PointerProperty(type=properties.A3OBE_PG_ResolutionLODs)
    bpy.types.Scene.a3obe_geometry_lod = bpy.props.PointerProperty(type=properties.A3OBE_PG_GeometryLOD)

def unregister():
    bpy.utils.unregister_class(panel.A3OBE_PT_AutoLOD)
    bpy.utils.unregister_class(operators.A3OBE_OT_GenerateLODs)
    bpy.utils.unregister_class(operators.A3OBE_OT_AddNamedProperty_Resolution)
    bpy.utils.unregister_class(operators.A3OBE_OT_AddNamedProperty_Geometry)
    bpy.utils.unregister_class(operators.A3OBE_OT_RemoveNamedProperty_Resolution)
    bpy.utils.unregister_class(operators.A3OBE_OT_RemoveNamedProperty_Geometry)
    bpy.utils.unregister_class(properties.A3OBE_PG_NamedProperty)
    bpy.utils.unregister_class(properties.A3OBE_PG_ResolutionLODs)
    bpy.utils.unregister_class(properties.A3OBE_PG_GeometryLOD)

    del bpy.types.Scene.a3obe_resolution_lods
    del bpy.types.Scene.a3obe_geometry_lod

if __name__ == "__main__":
    register()