import bpy
from bpy.types import Panel

class A3OBE_PT_AutoLOD(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Builder'
    bl_label = 'Auto LODs Generator'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, _):
        self.layout.label(icon='FORCE_VORTEX')

    def draw(self, ctx):
        L = self.layout
        S = ctx.scene

        EPR = S.a3obe_resolution_lods
        EPG = S.a3obe_geometry_lod
        EPM = S.a3obe_memory_lod

        row = L.row(align=True)
        row.prop(EPR, 'active', icon='MOD_DECIM')

        if EPR.active:
            box = L.box()
            box.label(text="Resolution LODs", icon='MESH_CUBE')

            row = box.row(align=True)
            row.prop(EPR, 'lod_prefix', icon='FONT_DATA')

            row = box.row(align=True)
            row.prop(EPR, 'first_lod', expand=True, icon='OUTLINER_OB_MESH')

            row = box.row(align=True)
            row.prop(EPR, 'preset', expand=True, icon='MODIFIER')

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
                row.prop(EPR, decimate_values, index=i-first_lod, text=f'LOD{i}', icon='MESH_DATA')

            box = L.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            props = EPR.named_properties
            for i, prop in enumerate(props):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property", text="Add Property", icon='PLUS')
            row = box.row()
            row.operator("a3obe.initialize_default_property", text="Initialize Default Property", icon='FILE_REFRESH')

        row = L.row(align=True)
        row.prop(EPG, 'active', icon='MODIFIER')

        if EPG.active:
            box = L.box()
            box.label(text="Geometry LOD", icon='MESH_CUBE')
            row = box.row(align=True)
            row.prop(EPG, 'lod_name', icon='FONT_DATA')
            row = box.row(align=True)
            row.prop(EPG, 'convex_hull_mesh', icon='MESH_GRID')
            row = box.row(align=True)
            row.prop(EPG, 'autocenter_property', icon='OBJECT_ORIGIN')

        row = L.row(align=True)
        row.prop(EPM, 'active', icon='MODIFIER')

        if EPM.active:
            box = L.box()
            box.label(text="Memory LOD", icon='MESH_CUBE')
            row = box.row(align=True)
            row.prop(EPM, 'lod_name', icon='FONT_DATA')
            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_min_point', icon='EMPTY_ARROWS')
            row = box.row(align=True)
            row.prop(EPM, 'create_boundingbox_max_point', icon='EMPTY_ARROWS')
            row = box.row(align=True)
            row.prop(EPM, 'create_invview_point', icon='VIEW_PAN')
            row = box.row(align=True)
            row.prop(EPM, 'autocenter_property', icon='OBJECT_ORIGIN')

        row = L.row(align=True)
        row.scale_y = 2.0
        row.operator('a3obe.generate_lods', icon='PLAY')

# Удаляем дублирующиеся функции register и unregister
# def register():
#     bpy.utils.register_class(A3OBE_PT_AutoLOD)
#
# def unregister():
#     bpy.utils.unregister_class(A3OBE_PT_AutoLOD)