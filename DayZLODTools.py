bl_info = {
    "name": "DayZ LOD Tools",
    "blender": (2, 80, 0),
    "category": "Object",
    "location": "View3D > Tool Shelf > LOD Tools",
    "description": "Automatically create LOD (Level of Detail) versions of the selected object",
    "author": "Your Name",
    "version": (1, 0),
    "wiki_url": "Your Wiki URL",
    "tracker_url": "Your Tracker URL",
    "support": "COMMUNITY",
}

import bpy

class LODPanelProperties(bpy.types.PropertyGroup):
    use_change_names: bpy.props.BoolProperty(name="Change Names", default=True)
    preset: bpy.props.EnumProperty(
        name="Preset",
        items=[
            ('FOR_QUADS', "For Quads", "Create LODs for quadrangulate objects"),
            ('FOR_TRIS', "For Tris", "Create LODs for triangulate objects"),
            ('CUSTOM', "Custom", "Create LODs with custom settings"),
        ],
        default='FOR_QUADS',
    )
    decimate_values_for_quads: bpy.props.FloatVectorProperty(
        name="Decimate Values (For Quads)",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.5, 0.3, 0.2, 0.1),
    )
    decimate_values_for_tris: bpy.props.FloatVectorProperty(
        name="Decimate Values (For Tris)",
        size=4,
        min=0.0,
        max=1.0,
        default=(0.8, 0.6, 0.4, 0.2),
    )

    def create_lods(self, context, ratios, mode):
        if not context.selected_objects:
            self.report({'INFO'}, 'No object selected. Please select an object.')
            return {'CANCELLED'}

        original_obj = context.active_object
        original_obj.name = 'LOD0'

        for i, ratio in enumerate(ratios):
            bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
            new_obj = context.active_object

            for modifier in new_obj.modifiers:
                new_obj.modifiers.remove(modifier)

            decimate_modifier = new_obj.modifiers.new(name=f'Decimate_{i}', type='DECIMATE')
            decimate_modifier.ratio = ratio

            weighted_normal_modifier = new_obj.modifiers.new(name=f'Weighted_Normal_{i}', type='WEIGHTED_NORMAL')
            weighted_normal_modifier.keep_sharp = True
            weighted_normal_modifier.use_face_influence = True

            if self.use_change_names:
                new_obj.name = f'LOD{i + 1}'

        return {'FINISHED'}

class OBJECT_PT_DayZLODToolsPanel(bpy.types.Panel):
    bl_label = "DayZ LOD Tools"
    bl_idname = "PT_DayZ_LOD_Tools_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'LOD Tools'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        box = layout.box()	
        row = box.row()
        row.prop(context.scene.lod_panel, "preset", text="")

        row = box.row(align=True)
        row.label(text="Decimate Values:")

        # Check the preset and enable/disable the properties accordingly
        is_custom_preset = context.scene.lod_panel.preset == 'CUSTOM'

        if context.scene.lod_panel.preset == 'FOR_QUADS':
            for i in range(4):
                row = box.row(align=True)
                row.enabled = is_custom_preset
                row.prop(context.scene.lod_panel, f"decimate_values_for_quads", index=i, text=f"LOD{i + 1}", emboss=is_custom_preset)
        elif context.scene.lod_panel.preset == 'FOR_TRIS':
            for i in range(4):
                row = box.row(align=True)
                row.enabled = is_custom_preset
                row.prop(context.scene.lod_panel, f"decimate_values_for_tris", index=i, text=f"LOD{i + 1}", emboss=is_custom_preset)
        else:
            for i in range(4):
                row = box.row(align=True)
                row.enabled = is_custom_preset
                row.prop(context.scene.lod_panel, f"decimate_values_for_quads", index=i, text=f"LOD{i + 1}", emboss=is_custom_preset)

        row = box.row(align=True)
        row.scale_y = 2.0
        row.operator("object.create_lods")

class OBJECT_OT_CreateLODs(bpy.types.Operator):
    bl_idname = "object.create_lods"
    bl_label = "Create LODs"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        lod_panel = context.scene.lod_panel
        if context.scene.lod_panel.preset == 'FOR_QUADS':
            ratios = lod_panel.decimate_values_for_quads
        elif context.scene.lod_panel.preset == 'FOR_TRIS':
            ratios = lod_panel.decimate_values_for_tris
        else:
            ratios = lod_panel.decimate_values_for_quads
        return lod_panel.create_lods(context, ratios, 'quadrangulate')

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_CreateLODs.bl_idname)

def register():
    bpy.utils.register_class(LODPanelProperties)
    bpy.types.Scene.lod_panel = bpy.props.PointerProperty(type=LODPanelProperties)
    bpy.utils.register_class(OBJECT_OT_CreateLODs)
    bpy.utils.register_class(OBJECT_PT_DayZLODToolsPanel)

def unregister():
    bpy.utils.unregister_class(LODPanelProperties)
    del bpy.types.Scene.lod_panel
    bpy.utils.unregister_class(OBJECT_OT_CreateLODs)
    bpy.utils.unregister_class(OBJECT_PT_DayZLODToolsPanel)

if __name__ == "__main__":
    register()
