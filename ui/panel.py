import bpy
from bpy.types import Panel


class A3OBE_PT_AutoLOD(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Builder'
    bl_label = 'Auto LODs Generator'
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(icon='FORCE_VORTEX')

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        resolution_lods = scene.a3obe_resolution_lods
        geometry_lod = scene.a3obe_geometry_lod
        memory_lod = scene.a3obe_memory_lod
        fire_geometry_lod = scene.a3obe_fire_geometry_lod
        view_geometry_lod = scene.a3obe_view_geometry_lod
        view_pilot_lod = scene.a3obe_view_pilot_lod

        # Resolution LODs
        row = layout.row(align=True)
        row.prop(resolution_lods, 'active', icon='MOD_DECIM', text="Resolution LODs")

        if resolution_lods.active:
            box = layout.box()
            box.label(text="Resolution LODs", icon='MESH_CUBE')
            row = box.row(align=True)
            row.prop(resolution_lods, 'lod_prefix', icon='FONT_DATA')
            row = box.row(align=True)
            row.prop(resolution_lods, 'first_lod', expand=True, icon='OUTLINER_OB_MESH')
            row = box.row(align=True)
            row.prop(resolution_lods, 'preset', expand=True, icon='MODIFIER')
            first_lod = 1 if resolution_lods.first_lod == 'LOD1' else 0
            preset = resolution_lods.preset
            decimate_values = 'custom_decimate_values' if preset == 'CUSTOM' else 'tris_decimate_values' if preset == 'TRIS' else 'quads_decimate_values'
            for i in range(first_lod, first_lod + 4):
                row = box.row(align=True)
                row.enabled = preset == 'CUSTOM'
                row.prop(resolution_lods, decimate_values, index=i - first_lod, text=f'LOD{i}', icon='MESH_DATA')
            box.separator()
            row = box.row(align=True)
            row.prop(view_pilot_lod, 'active', icon='VIEW_CAMERA', text="View Pilot LOD")
            if view_pilot_lod.active:
                sub = box.box()
                row = sub.row(align=True)
                row.prop(view_pilot_lod, 'mesh_type', expand=True)
            box = layout.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            for i, prop in enumerate(resolution_lods.named_properties):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property_resolution", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property_resolution", text="Add Property", icon='PLUS')
            if view_pilot_lod.active:
                box = layout.box()
                box.label(text="View Pilot - Named Properties", icon='PROPERTIES')
                for i, prop in enumerate(view_pilot_lod.named_properties):
                    row = box.row(align=True)
                    row.prop(prop, "name", text="", icon='FILE_TEXT')
                    row.prop(prop, "value", text="", icon='TEXT')
                    row.operator("a3obe.remove_named_property_view_pilot", text="", icon='X').index = i
                row = box.row()
                row.operator("a3obe.add_named_property_view_pilot", text="Add Property", icon='PLUS')

        # Geometry LOD
        row = layout.row(align=True)
        row.prop(geometry_lod, 'active', icon='MODIFIER', text="Geometry LOD")

        if geometry_lod.active:
            box = layout.box()
            box.label(text="Geometry LOD", icon='MESH_CUBE')
            row = box.row(align=True)
            row.prop(geometry_lod, 'lod_name', icon='FONT_DATA')
            row = box.row(align=True)
            row.prop(geometry_lod, 'geometry_type', expand=True, icon='MESH_CUBE')
            box = layout.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            for i, prop in enumerate(geometry_lod.named_properties):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property_geometry", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property_geometry", text="Add Property", icon='PLUS')

        # Memory LOD
        row = layout.row(align=True)
        row.prop(memory_lod, 'active', icon='EMPTY_AXIS', text="Memory LOD")

        if memory_lod.active:
            box = layout.box()
            box.label(text="Memory LOD", icon='EMPTY_AXIS')

            standard_box = box.box()
            standard_box.label(text="Standard Points", icon='MESH_CUBE')
            row = standard_box.row(align=True)
            row.prop(memory_lod, 'invview_point', icon='MESH_UVSPHERE')
            row = standard_box.row(align=True)
            row.prop(memory_lod, 'bounding_box_points', icon='MESH_CUBE')
            row = standard_box.row(align=True)
            row.prop(memory_lod, 'radius_point', icon='MESH_UVSPHERE')
            row = standard_box.row(align=True)
            row.prop(memory_lod, 'center_point', icon='MESH_UVSPHERE')

            box = layout.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            for i, prop in enumerate(memory_lod.named_properties):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property_memory", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property_memory", text="Add Property", icon='PLUS')

        # Fire Geometry LOD
        row = layout.row(align=True)
        row.prop(fire_geometry_lod, 'active', icon='MODIFIER', text="Fire Geometry LOD")

        if fire_geometry_lod.active:
            box = layout.box()
            box.label(text="Fire Geometry LOD", icon='MODIFIER')
            row = box.row(align=True)
            row.label(text="Quality:")
            row.prop(fire_geometry_lod, 'quality', text="", slider=True)
            box = layout.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            for i, prop in enumerate(fire_geometry_lod.named_properties):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property_fire_geometry", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property_fire_geometry", text="Add Property", icon='PLUS')

        # View Geometry LOD
        row = layout.row(align=True)
        row.prop(view_geometry_lod, 'active', icon='VIEW3D', text="View Geometry LOD")

        if view_geometry_lod.active:
            box = layout.box()
            box.label(text="View Geometry LOD", icon='VIEW3D')
            row = box.row(align=True)
            row.prop(view_geometry_lod, 'lod_name', icon='FONT_DATA')
            box = layout.box()
            box.label(text="Named Properties", icon='PROPERTIES')
            for i, prop in enumerate(view_geometry_lod.named_properties):
                row = box.row(align=True)
                row.prop(prop, "name", text="", icon='FILE_TEXT')
                row.prop(prop, "value", text="", icon='TEXT')
                row.operator("a3obe.remove_named_property_view_geometry", text="", icon='X').index = i
            row = box.row()
            row.operator("a3obe.add_named_property_view_geometry", text="Add Property", icon='PLUS')

        row = layout.row(align=True)
        row.scale_y = 2.0
        row.operator('a3obe.generate_lods', icon='PLAY', text="Generate LODs")
