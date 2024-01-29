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

class OBJECT_PT_DayZLODToolsPanel(bpy.types.Panel):
    bl_label = "DayZ LOD Tools"
    bl_idname = "PT_DayZ_LOD_Tools_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tools'
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("object.create_lods_quadrangulate")

        row = layout.row()
        row.operator("object.create_lods_triangulate")

class OBJECT_OT_CreateLODsQuadrangulate(bpy.types.Operator):
    bl_idname = "object.create_lods_quadrangulate"
    bl_label = "Create LODs (for Quadrangulate object)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, 'No object selected. Please select an object.')
            return {'CANCELLED'}

        original_obj = context.active_object
        original_obj.name = 'LOD0'

        for i, ratio in enumerate([0.5, 0.3, 0.2, 0.1]):
            # Дублируем объект с Duplicate Objects
            bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
            new_obj = context.active_object

            # Удаляем все модификаторы
            for modifier in new_obj.modifiers:
                new_obj.modifiers.remove(modifier)

            # Добавляем модификатор Decimate
            decimate_modifier = new_obj.modifiers.new(name=f'Decimate_{i}', type='DECIMATE')
            decimate_modifier.ratio = ratio

            # Добавляем модификатор Weighted Normal
            weighted_normal_modifier = new_obj.modifiers.new(name=f'Weighted_Normal_{i}', type='WEIGHTED_NORMAL')
            weighted_normal_modifier.keep_sharp = True
            weighted_normal_modifier.use_face_influence = True
            
            new_obj.name = f'LOD{i + 1}'

        return {'FINISHED'}

class OBJECT_OT_CreateLODsTriangulate(bpy.types.Operator):
    bl_idname = "object.create_lods_triangulate"
    bl_label = "Create LODs (for Triangulate object)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.selected_objects:
            self.report({'INFO'}, 'No object selected. Please select an object.')
            return {'CANCELLED'}

        original_obj = context.active_object
        original_obj.name = 'LOD0'

        for i, ratio in enumerate([0.8, 0.6, 0.4, 0.2]):
            # Дублируем объект с Duplicate Objects
            bpy.ops.object.duplicate(linked=False, mode='TRANSLATION')
            new_obj = context.active_object

            # Удаляем все модификаторы
            for modifier in new_obj.modifiers:
                new_obj.modifiers.remove(modifier)

            # Добавляем модификатор Decimate
            decimate_modifier = new_obj.modifiers.new(name=f'Decimate_{i}', type='DECIMATE')
            decimate_modifier.ratio = ratio

            # Добавляем модификатор Weighted Normal
            weighted_normal_modifier = new_obj.modifiers.new(name=f'Weighted_Normal_{i}', type='WEIGHTED_NORMAL')
            weighted_normal_modifier.keep_sharp = True
            weighted_normal_modifier.use_face_influence = True
            
            new_obj.name = f'LOD{i + 1}'

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_CreateLODsQuadrangulate.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_CreateLODsQuadrangulate)
    bpy.utils.register_class(OBJECT_OT_CreateLODsTriangulate)
    bpy.utils.register_class(OBJECT_PT_DayZLODToolsPanel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateLODsQuadrangulate)
    bpy.utils.unregister_class(OBJECT_OT_CreateLODsTriangulate)
    bpy.utils.unregister_class(OBJECT_PT_DayZLODToolsPanel)

if __name__ == "__main__":
    register()
