import bpy
from bpy.types import Operator
from . import lod_generators
from . import utils

class A3OBE_OT_GenerateLODs(Operator):
    bl_idname = 'a3obe.generate_lods'
    bl_label = 'Generate LODs'
    bl_icon = 'PLAY'

    def execute(self, context):
        scene = context.scene
        resolution_lods = scene.a3obe_resolution_lods
        geometry_lod = scene.a3obe_geometry_lod
        memory_lod = scene.a3obe_memory_lod
        fire_geometry_lod = scene.a3obe_fire_geometry_lod
        view_geometry_lod = scene.a3obe_view_geometry_lod

        if not context.active_object:
            self.report({'WARNING'}, 'Select an object first!')
            return {'CANCELLED'}

        if not hasattr(context.active_object, 'a3ob_properties_object'):
            self.report({'WARNING'}, 'Active object does not have A3OB properties. Please select an object with A3OB properties.')
            return {'CANCELLED'}

        # Store reference to original object to prevent loss during generation
        original_obj = context.active_object

        if geometry_lod.active:
            lod_generators.generate_geometry_lod(context, original_obj)

        if memory_lod.active:
            lod_generators.generate_memory_lod(context, original_obj)

        if fire_geometry_lod.active:
            lod_generators.generate_fire_geometry_lod(context, original_obj)

        if view_geometry_lod.active:
            lod_generators.generate_view_geometry_lod(context, original_obj)

        if resolution_lods.active:
            lod_generators.generate_resolution_lods(context, original_obj)

        # Ensure correct collection order
        utils.organize_collections(context)

        return {'FINISHED'}

class A3OBE_OT_AddNamedProperty_Resolution(Operator):
    bl_idname = 'a3obe.add_named_property_resolution'
    bl_label = 'Add Property'
    bl_icon = 'PLUS'
    def execute(self, context):
        context.scene.a3obe_resolution_lods.named_properties.add()
        return {'FINISHED'}

class A3OBE_OT_AddNamedProperty_Geometry(Operator):
    bl_idname = 'a3obe.add_named_property_geometry'
    bl_label = 'Add Property'
    bl_icon = 'PLUS'
    def execute(self, context):
        context.scene.a3obe_geometry_lod.named_properties.add()
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty_Resolution(Operator):
    bl_idname = 'a3obe.remove_named_property_resolution'
    bl_label = 'Remove Property'
    bl_icon = 'X'
    index: bpy.props.IntProperty()
    def execute(self, context):
        props = context.scene.a3obe_resolution_lods.named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty_Geometry(Operator):
    bl_idname = 'a3obe.remove_named_property_geometry'
    bl_label = 'Remove Property'
    bl_icon = 'X'
    index: bpy.props.IntProperty()
    def execute(self, context):
        props = context.scene.a3obe_geometry_lod.named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_AddNamedProperty_Memory(Operator):
    bl_idname = 'a3obe.add_named_property_memory'
    bl_label = 'Add Property'
    bl_icon = 'PLUS'
    def execute(self, context):
        context.scene.a3obe_memory_lod.named_properties.add()
        return {'FINISHED'}

class A3OBE_OT_AddNamedProperty_FireGeometry(Operator):
    bl_idname = 'a3obe.add_named_property_fire_geometry'
    bl_label = 'Add Property'
    bl_icon = 'PLUS'
    def execute(self, context):
        context.scene.a3obe_fire_geometry_lod.named_properties.add()
        return {'FINISHED'}

class A3OBE_OT_AddNamedProperty_ViewGeometry(Operator):
    bl_idname = 'a3obe.add_named_property_view_geometry'
    bl_label = 'Add Property'
    bl_icon = 'PLUS'
    def execute(self, context):
        context.scene.a3obe_view_geometry_lod.named_properties.add()
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty_Memory(Operator):
    bl_idname = 'a3obe.remove_named_property_memory'
    bl_label = 'Remove Property'
    bl_icon = 'X'
    index: bpy.props.IntProperty()
    def execute(self, context):
        props = context.scene.a3obe_memory_lod.named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty_FireGeometry(Operator):
    bl_idname = 'a3obe.remove_named_property_fire_geometry'
    bl_label = 'Remove Property'
    bl_icon = 'X'
    index: bpy.props.IntProperty()
    def execute(self, context):
        props = context.scene.a3obe_fire_geometry_lod.named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty_ViewGeometry(Operator):
    bl_idname = 'a3obe.remove_named_property_view_geometry'
    bl_label = 'Remove Property'
    bl_icon = 'X'
    index: bpy.props.IntProperty()
    def execute(self, context):
        props = context.scene.a3obe_view_geometry_lod.named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_InitializeDefaultProperty(Operator):
    bl_idname = 'a3obe.initialize_default_property'
    bl_label = 'Initialize Default'
    bl_icon = 'FILE_REFRESH'
    def execute(self, context):
        resolution = context.scene.a3obe_resolution_lods
        if not any(p.name == 'lodnoshadow' for p in resolution.named_properties):
            prop = resolution.named_properties.add()
            prop.name = 'lodnoshadow'
            prop.value = '1'
            self.report({'INFO'}, 'Added lodnoshadow=1 to Resolution LODs')
        geometry = context.scene.a3obe_geometry_lod
        if not any(p.name == 'lodnoshadow' for p in geometry.named_properties):
            prop = geometry.named_properties.add()
            prop.name = 'lodnoshadow'
            prop.value = '1'
            self.report({'INFO'}, 'Added lodnoshadow=1 to Geometry LODs')
        return {'FINISHED'}