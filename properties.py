import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty, FloatVectorProperty, CollectionProperty, PointerProperty, IntProperty
from bpy.types import PropertyGroup

class A3OBE_PG_NamedProperty(PropertyGroup):
    name: StringProperty(name="Name", description="Name of the custom property", default="")
    value: StringProperty(name="Value", description="Value of the custom property", default="")

class A3OBE_PG_ResolutionLODs(PropertyGroup):
    active: BoolProperty(name="Generate Resolution LODs", description="Enable generation of resolution LODs", default=True)
    lod_prefix: StringProperty(name="Prefix", description="Prefix for resolution LOD object names", default="LOD ")
    first_lod: EnumProperty(items=[('LOD0', "LOD 0", "Start with LOD 0", 'OUTLINER_OB_MESH', 0),
                                  ('LOD1', "LOD 1", "Start with LOD 1", 'OUTLINER_OB_MESH', 1)],
                           default='LOD1', description="Select the starting LOD level")
    preset: EnumProperty(items=[('CUSTOM', "Custom", "Use custom decimate values", 'MODIFIER', 0),
                               ('TRIS', "Tris", "Use tris-based decimate values", 'MODIFIER', 1),
                               ('QUADS', "Quads", "Use quads-based decimate values", 'MODIFIER', 2)],
                        default='QUADS', description="Choose a preset for decimation ratios")
    custom_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.75, 0.50, 0.25, 0.10),
                                               description="Custom decimate ratios for LODs 0-3")
    tris_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.80, 0.60, 0.40, 0.20),
                                             description="Tris-based decimate ratios for LODs 0-3")
    quads_decimate_values: FloatVectorProperty(size=4, min=0.0, max=1.0, default=(0.50, 0.30, 0.20, 0.10),
                                              description="Quads-based decimate ratios for LODs 0-3")
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty, description="List of custom properties for resolution LODs")

class A3OBE_PG_GeometryLOD(PropertyGroup):
    active: BoolProperty(name="Generate Geometry LOD", description="Enable generation of geometry LOD", default=True)
    lod_name: StringProperty(name="Name", description="Name of the geometry LOD object", default="Geometry")
    geometry_type: EnumProperty(items=[('BOX', "Box", "Generate a single bounding box", 'MESH_CUBE', 0),
                                      ('NONE', "None", "Create empty object with properties", 'EMPTY_DATA', 1)],
                                default='BOX', description="Choose the type of geometry LOD to generate")
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty, description="List of custom properties for geometry LOD")

class A3OBE_PG_MemoryLOD(PropertyGroup):
    active: BoolProperty(name="Generate Memory LOD", description="Enable generation of memory LOD", default=False)
    
    # Standard Points
    invview_point: BoolProperty(name="Inview Point", description="Add invview point to memory", default=True)
    bounding_box_points: BoolProperty(name="Bounding Box Points", description="Add boundingbox_min and boundingbox_max points", default=True)
    radius_point: BoolProperty(name="Radius Point", description="Add ce_radius point to memory", default=False)
    center_point: BoolProperty(name="Center Point", description="Add ce_center point to memory", default=False)
    
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty, description="List of custom properties for memory LOD")

class A3OBE_PG_FireGeometryLOD(PropertyGroup):
    active: BoolProperty(name="Generate Fire Geometry LOD", description="Enable generation of fire geometry LOD", default=False)
    quality: IntProperty(name="Fire Geometry Quality", description="1 = low polygon count, 10 = high polygon count", min=1, max=10, default=2)
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty, description="List of custom properties for fire geometry LOD")

class A3OBE_PG_ViewGeometryLOD(PropertyGroup):
    active: BoolProperty(name="Generate View Geometry LOD", description="Enable generation of view geometry LOD", default=False)
    lod_name: StringProperty(name="Name", description="Name of the view geometry LOD object", default="View Geometry")
    named_properties: CollectionProperty(type=A3OBE_PG_NamedProperty, description="List of custom properties for view geometry LOD")