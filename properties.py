import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty, FloatVectorProperty, CollectionProperty, PointerProperty
from bpy.types import PropertyGroup

class A3OBE_PG_NamedProperty(PropertyGroup):
    name: StringProperty(name="Name", default="")
    value: StringProperty(name="Value", default="")

class A3OBE_PG_ResolutionLODs(PropertyGroup):
    active: BoolProperty(name='Generate Resolution LODs', default=True)
    lod_prefix: StringProperty(name='', description='Resolution LOD prefix', default='resolution_lod_')
    first_lod: EnumProperty(description='First LOD', items=[('LOD0', 'LOD 0', ''), ('LOD1', 'LOD 1', '')], default='LOD1')
    preset: EnumProperty(description='Preset', items=[('CUSTOM', 'Custom', ''), ('TRIS', 'Tris', ''), ('QUADS', 'Quads', '')], default='QUADS')
    custom_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.75, 0.50, 0.25, 0.10))
    tris_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.80, 0.60, 0.40, 0.20))
    quads_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.50, 0.30, 0.20, 0.10))
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty)

class A3OBE_PG_GeometryLOD(PropertyGroup):
    active: BoolProperty(name='Generate Geometry LOD [WIP]', default=False)
    lod_name: StringProperty(name='', description='Geometry LOD name', default='geometry_lod')
    convex_hull_mesh: BoolProperty(name='Create Convex Hull mesh', default=True)
    autocenter_property: BoolProperty(name='Disable "autocenter = 0" property', default=True)

class A3OBE_PG_MemoryLOD(PropertyGroup):
    active: BoolProperty(name='Generate Memory LOD [WIP]', default=False)
    lod_name: StringProperty(name='', description='Memory LOD name', default='memory_lod')
    create_boundingbox_min_point: BoolProperty(name='Create BoundingBox_Min point', default=True)
    create_boundingbox_max_point: BoolProperty(name='Create BoundingBox_Max point', default=True)
    create_invview_point: BoolProperty(name='Create InvView point', default=True)
    autocenter_property: BoolProperty(name='Disable "autocenter = 0" property', default=True)
