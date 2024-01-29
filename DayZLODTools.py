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

class OBJECT_PT_dayz_lod_tools_panel(bpy.types.Panel):
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

class OBJECT_OT_create_lods_quadrangulate(bpy.types.Operator):
    bl_idname = "object.create_lods_quadrangulate"
    bl_label = "Create LOD's (for Quadrangulate object)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Проверяем, есть ли хотя бы один объект в выделении
        if not context.selected_objects:
            self.report({'INFO'}, 'No object selected. Please select an object.')
            return {'CANCELLED'}

        original_obj = context.active_object

        # Переименовываем оригинальный объект в LOD0
        original_obj.name = 'LOD0'

        # Дублируем объект 4 раза
        for i, ratio in enumerate([0.8, 0.6, 0.4, 0.2]):
            new_obj = original_obj.copy()
            context.collection.objects.link(new_obj)

            # Добавляем модификатор Decimate
            decimate_modifier = new_obj.modifiers.new(name=f'Decimate_{i}', type='DECIMATE')
            # Настройки модификатора Decimate
            decimate_modifier.ratio = ratio  # Устанавливаем различные значения Decimate

            # Добавляем модификатор Weighted Normal
            weighted_normal_modifier = new_obj.modifiers.new(name=f'Weighted_Normal_{i}', type='WEIGHTED_NORMAL')
            # Включаем опцию Keep Sharp
            weighted_normal_modifier.keep_sharp = True
            weighted_normal_modifier.use_face_influence = True
            
            # Переименовываем объект
            new_obj.name = f'LOD{i + 1}'

        return {'FINISHED'}

class OBJECT_OT_create_lods_triangulate(bpy.types.Operator):
    bl_idname = "object.create_lods_triangulate"
    bl_label = "Create LOD's (for Triangulate object)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Проверяем, есть ли хотя бы один объект в выделении
        if not context.selected_objects:
            self.report({'INFO'}, 'No object selected. Please select an object.')
            return {'CANCELLED'}

        original_obj = context.active_object

        # Переименовываем оригинальный объект в LOD0
        original_obj.name = 'LOD0'

        # Дублируем объект 4 раза
        for i, ratio in enumerate([0.5, 0.3, 0.2, 0.1]):
            new_obj = original_obj.copy()
            context.collection.objects.link(new_obj)

            # Добавляем модификатор Decimate
            decimate_modifier = new_obj.modifiers.new(name=f'Decimate_{i}', type='DECIMATE')
            # Настройки модификатора Decimate
            decimate_modifier.ratio = ratio  # Устанавливаем различные значения Decimate

            # Добавляем модификатор Weighted Normal
            weighted_normal_modifier = new_obj.modifiers.new(name=f'Weighted_Normal_{i}', type='WEIGHTED_NORMAL')
            # Включаем опцию Keep Sharp
            weighted_normal_modifier.keep_sharp = True
            weighted_normal_modifier.use_face_influence = True
            
            # Переименовываем объект
            new_obj.name = f'LOD{i + 1}'

        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_create_lods_quadrangulate.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_create_lods_quadrangulate)
    bpy.utils.register_class(OBJECT_OT_create_lods_triangulate)
    bpy.utils.register_class(OBJECT_PT_dayz_lod_tools_panel)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_lods_quadrangulate)
    bpy.utils.unregister_class(OBJECT_OT_create_lods_triangulate)
    bpy.utils.unregister_class(OBJECT_PT_dayz_lod_tools_panel)

if __name__ == "__main__":
    register()
