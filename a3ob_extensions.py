import os
import math
import bpy


P = bpy.props
T = bpy.types
U = bpy.utils
O = bpy.ops


class A3OBE_PT_AutoLOD(T.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Builder'
    bl_label = 'Auto LODs Generator'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        L = self.layout
        L.label(icon='FORCE_VORTEX')

    def draw(self, ctx):

        L = self.layout
        S = ctx.scene

        EPR = S.a3obe_resolution_lods
        EPG = S.a3obe_geometry_lod
        EPM = S.a3obe_memory_lod

        row = L.row(align=True)
        row.prop(EPR, 'active')

        if EPR.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPR, 'lod_prefix')

            row = box.row(align=True)
            row.prop(EPR, 'first_lod', expand=True)

            row = box.row(align=True)
            row.prop(EPR, 'preset', expand=True)

            match EPR.first_lod:
                case 'LOD0':
                    first_lod = 1
                case 'LOD1':
                    first_lod = 2

            match EPR.preset:
                case 'CUSTOM':
                    decimate_values = 'custom_decimate_values'
                case 'TRIS':
                    decimate_values = 'tris_decimate_values'
                case 'QUADS':
                    decimate_values = 'quads_decimate_values'

            for i in range(first_lod, first_lod + 4):

                row = box.row(align=True)
                row.enabled = EPR.preset == 'CUSTOM'

                row.prop(EPR, decimate_values, index=i-first_lod, text=f'LOD{i}')

            row = box.row(align=True)
            row.prop(EPR, 'autocenter_property')

            row = box.row(align=True)
            row.prop(EPR, 'lodnoshadow_property')

        row = L.row(align=True)
        row.prop(EPG, 'active')

        if EPG.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPG, 'lod_name')

            row = box.row(align=True)
            row.prop(EPG, 'convex_hull_mesh')

            row = box.row(align=True)
            row.prop(EPG, 'autocenter_property')

        row = L.row(align=True)
        row.prop(EPM, 'active')

        if EPM.active:

            box = L.box()

            row = box.row(align=True)
            row.prop(EPM, 'lod_name')

            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_min_point')

            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_max_point')

            row = box.row(align=True)
            row.prop(EPM, 'create_invview_point')

            row = box.row(align=True)
            row.prop(EPM, 'autocenter_property')

        row = L.row(align=True)
        row.scale_y = 2.0
        row.operator('a3obe.generate_lods')


class A3OBE_OT_GenerateLODs(T.Operator):
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

            if not EPR.autocenter_property:
                self.add_named_property(original_obj, 'autocenter', '0')

            if not EPR.lodnoshadow_property:
                self.add_named_property(original_obj, 'lodnoshadow', '1')

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

                if not EPR.autocenter_property:
                    self.add_named_property(duplicated_obj, 'autocenter', '0')

                if not EPR.lodnoshadow_property:
                    self.add_named_property(duplicated_obj, 'lodnoshadow', '1')

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


class A3OBE_PG_ResolutionLODs(T.PropertyGroup):

    active: P.BoolProperty(
        name='Generate Resolution LODs',
        default=True)

    lod_prefix: P.StringProperty(
        name='',
        description='Resolution LOD prefix',
        default='resolution_lod_')

    first_lod: P.EnumProperty(
        description='First LOD',
        items=[
            ('LOD0', 'LOD 0', ''),
            ('LOD1', 'LOD 1', ''),
        ], default='LOD1')

    preset: P.EnumProperty(
        description='Preset',
        items=[
            ('CUSTOM', 'Custom', ''),
            ('TRIS', 'Tris', ''),
            ('QUADS', 'Quads', ''),
        ], default='QUADS')

    custom_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.75, 0.50, 0.25, 0.10))

    tris_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.80, 0.60, 0.40, 0.20))

    quads_decimate_values: P.FloatVectorProperty(
        size=4, min=0.0, max=1.0,
        default=(0.50, 0.30, 0.20, 0.10))

    autocenter_property: P.BoolProperty(
        name='Disable "autocenter = 0" property',
        default=True)

    lodnoshadow_property: P.BoolProperty(
        name='Disable "lodnoshadow = 1" property',
        default=True)


class A3OBE_PG_GeometryLOD(T.PropertyGroup):

    active: P.BoolProperty(
        name = 'Generate Geometry LOD [WIP]',
        default = False)

    lod_name: P.StringProperty(
        name = '',
        description = 'Geometry LOD name',
        default = 'geometry_lod')

    convex_hull_mesh: P.BoolProperty(
        name = 'Create Convex Hull mesh',
        default = True)

    autocenter_property: P.BoolProperty(
        name = 'Disable "autocenter = 0" property',
        default = True)



class A3OBE_PG_MemoryLOD(T.PropertyGroup):

    active: P.BoolProperty(
        name = 'Generate Memory LOD [WIP]',
        default = False)

    lod_name: P.StringProperty(
        name = '',
        description = 'Memory LOD name',
        default = 'memory_lod')

    create_boundingbox_min_point: P.BoolProperty(
        name = 'Create BoundingBox_Min point',
        default = True)

    create_boundingbox_max_point: P.BoolProperty(
        name = 'Create BoundingBox_Max point',
        default = True)

    create_invview_point: P.BoolProperty(
        name = 'Create InvView point',
        default = True)

    autocenter_property: P.BoolProperty(
        name = 'Disable "autocenter = 0" property',
        default = True)



def register():
    T.Scene.a3obe_resolution_lods = P.PointerProperty(type=A3OBE_PG_ResolutionLODs)
    T.Scene.a3obe_geometry_lod = P.PointerProperty(type=A3OBE_PG_GeometryLOD)
    T.Scene.a3obe_memory_lod = P.PointerProperty(type=A3OBE_PG_MemoryLOD)
