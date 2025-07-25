import bpy
from bpy.types import Operator

class A3OBE_OT_GenerateLODs(Operator):
    bl_idname = 'a3obe.generate_lods'
    bl_label = 'Generate LODs'

    def execute(self, ctx):
        S = ctx.scene
        EPR = S.a3obe_resolution_lods
        EPG = S.a3obe_geometry_lod
        EPM = S.a3obe_memory_lod

        if not ctx.active_object:
            self.report({'WARNING'}, 'Select an object first!')
            return {'CANCELLED'}

        if EPR.active:
            if not any(prop.name == 'lodnoshadow' for prop in EPR.named_properties):
                item = EPR.named_properties.add()
                item.name = 'lodnoshadow'
                item.value = '1'

            match EPR.first_lod:
                case 'LOD0':
                    first_lod = 0
                case 'LOD1':
                    first_lod = 1

            original_obj = ctx.active_object
            original_obj.name = f'{EPR.lod_prefix}{first_lod}'
            original_obj.data.name = original_obj.name
            original_obj.data.use_auto_smooth = True

            original_obj.a3ob_properties_object.is_a3_lod = True
            original_obj.a3ob_properties_object.lod = '0'
            original_obj.a3ob_properties_object.resolution = first_lod

            for prop in EPR.named_properties:
                self.add_named_property(original_obj, prop.name, prop.value)

            match EPR.preset:
                case 'CUSTOM':
                    decimate_values = EPR.custom_decimate_values
                case 'TRIS':
                    decimate_values = EPR.tris_decimate_values
                case 'QUADS':
                    decimate_values = EPR.quads_decimate_values

            for i, decimate_value in enumerate(decimate_values):
                duplicated_obj = self.duplicate(ctx, original_obj)
                duplicated_obj.name = f'{EPR.lod_prefix}{first_lod + i + 1}'
                duplicated_obj.data.name = duplicated_obj.name

                decimate_modifier = duplicated_obj.modifiers.new(name='Decimate', type='DECIMATE')
                decimate_modifier.ratio = decimate_value
                decimate_modifier.use_collapse_triangulate = True

                weighted_normal_modifier = duplicated_obj.modifiers.new(name='WeightedNormal', type='WEIGHTED_NORMAL')
                weighted_normal_modifier.use_face_influence = True
                weighted_normal_modifier.keep_sharp = True

                duplicated_obj.a3ob_properties_object.is_a3_lod = True
                duplicated_obj.a3ob_properties_object.lod = '0'
                duplicated_obj.a3ob_properties_object.resolution = first_lod + i + 1

                for prop in EPR.named_properties:
                    self.add_named_property(duplicated_obj, prop.name, prop.value)

        if EPG.active:
            pass

        if EPM.active:
            pass

        return {'FINISHED'}

    def duplicate(self, ctx, obj):
        obj_copy = obj.copy()
        obj_copy.data = obj_copy.data.copy()
        ctx.collection.objects.link(obj_copy)
        return obj_copy

    def add_named_property(self, obj, name, value):
        properties = obj.a3ob_properties_object.properties
        if not any(x.name == name for x in properties):
            item = properties.add()
            item.name = name
            item.value = value

class A3OBE_OT_AddNamedProperty(Operator):
    bl_idname = 'a3obe.add_named_property'
    bl_label = 'Add Named Property'

    def execute(self, ctx):
        EPR = ctx.scene.a3obe_resolution_lods
        item = EPR.named_properties.add()
        item.name = ''
        item.value = ''
        return {'FINISHED'}

class A3OBE_OT_RemoveNamedProperty(Operator):
    bl_idname = 'a3obe.remove_named_property'
    bl_label = 'Remove Named Property'

    index: bpy.props.IntProperty()

    def execute(self, ctx):
        EPR = ctx.scene.a3obe_resolution_lods
        EPR.named_properties.remove(self.index)
        return {'FINISHED'}

class A3OBE_OT_InitializeDefaultProperty(Operator):
    bl_idname = 'a3obe.initialize_default_property'
    bl_label = 'Initialize Default Property'
    bl_description = 'Adds lodnoshadow = 1 to Named Properties if not present'

    def execute(self, ctx):
        EPR = ctx.scene.a3obe_resolution_lods
        if not any(prop.name == 'lodnoshadow' for prop in EPR.named_properties):
            item = EPR.named_properties.add()
            item.name = 'lodnoshadow'
            item.value = '1'
            self.report({'INFO'}, 'Added lodnoshadow = 1 to Named Properties')
        else:
            self.report({'WARNING'}, 'lodnoshadow is already present in Named Properties')
        return {'FINISHED'}
