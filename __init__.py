bl_info = {
    "name" : "Arma 3 Object Builder Extensions",
    "description" : "A set of usefull extensions for Arma 3 Object Builder addon",
    "author" : "Mikk, SXDIST",
    "blender" : (4, 5, 0),
    "category" : "3D View"
}

import bpy
from . import panel, operators, properties

def register():
    # Register all classes
    bpy.utils.register_class(panel.A3OBE_PT_AutoLOD)
    bpy.utils.register_class(operators.A3OBE_OT_GenerateLODs)
    bpy.utils.register_class(operators.A3OBE_OT_AddNamedProperty)
    bpy.utils.register_class(operators.A3OBE_OT_RemoveNamedProperty)
    bpy.utils.register_class(properties.A3OBE_PG_NamedProperty)
    bpy.utils.register_class(properties.A3OBE_PG_ResolutionLODs)
    bpy.utils.register_class(properties.A3OBE_PG_GeometryLOD)
    bpy.utils.register_class(properties.A3OBE_PG_MemoryLOD)

    # Add properties to Scene
    bpy.types.Scene.a3obe_resolution_lods = properties.PointerProperty(type=properties.A3OBE_PG_ResolutionLODs)
    bpy.types.Scene.a3obe_geometry_lod = properties.PointerProperty(type=properties.A3OBE_PG_GeometryLOD)
    bpy.types.Scene.a3obe_memory_lod = properties.PointerProperty(type=properties.A3OBE_PG_MemoryLOD)

    # Note: Initialization of lodnoshadow = 1 is moved to panel.draw to avoid access issues during registration

def unregister():
    # Unregister all classes
    bpy.utils.unregister_class(panel.A3OBE_PT_AutoLOD)
    bpy.utils.unregister_class(operators.A3OBE_OT_GenerateLODs)
    bpy.utils.unregister_class(operators.A3OBE_OT_AddNamedProperty)
    bpy.utils.unregister_class(operators.A3OBE_OT_RemoveNamedProperty)
    bpy.utils.unregister_class(properties.A3OBE_PG_NamedProperty)
    bpy.utils.unregister_class(properties.A3OBE_PG_ResolutionLODs)
    bpy.utils.unregister_class(properties.A3OBE_PG_GeometryLOD)
    bpy.utils.unregister_class(properties.A3OBE_PG_MemoryLOD)

    # Remove properties from Scene
    if hasattr(bpy.types.Scene, 'a3obe_resolution_lods'):
        del bpy.types.Scene.a3obe_resolution_lods
    if hasattr(bpy.types.Scene, 'a3obe_geometry_lod'):
        del bpy.types.Scene.a3obe_geometry_lod
    if hasattr(bpy.types.Scene, 'a3obe_memory_lod'):
        del bpy.types.Scene.a3obe_memory_lod

if __name__ == "__main__":
    register()