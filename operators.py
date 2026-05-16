import os

import bpy
from bpy.types import Operator

from . import generators, updater
from .core import utils


class _AddNamedPropertyBase(Operator):
    bl_label = 'Add Property'
    bl_options = {'INTERNAL', 'UNDO'}
    _prop_path: str = ''

    def execute(self, context):
        getattr(context.scene, self._prop_path).named_properties.add()
        return {'FINISHED'}


class _RemoveNamedPropertyBase(Operator):
    bl_label = 'Remove Property'
    bl_options = {'INTERNAL', 'UNDO'}
    _prop_path: str = ''
    index: bpy.props.IntProperty()

    def execute(self, context):
        props = getattr(context.scene, self._prop_path).named_properties
        if 0 <= self.index < len(props):
            props.remove(self.index)
        return {'FINISHED'}


class A3OBE_OT_AddNamedProperty_Resolution(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_resolution'
    _prop_path = 'a3obe_resolution_lods'

class A3OBE_OT_AddNamedProperty_Geometry(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_geometry'
    _prop_path = 'a3obe_geometry_lod'

class A3OBE_OT_AddNamedProperty_Memory(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_memory'
    _prop_path = 'a3obe_memory_lod'

class A3OBE_OT_AddNamedProperty_FireGeometry(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_fire_geometry'
    _prop_path = 'a3obe_fire_geometry_lod'

class A3OBE_OT_AddNamedProperty_ViewGeometry(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_view_geometry'
    _prop_path = 'a3obe_view_geometry_lod'

class A3OBE_OT_AddNamedProperty_ViewPilot(_AddNamedPropertyBase):
    bl_idname = 'a3obe.add_named_property_view_pilot'
    _prop_path = 'a3obe_view_pilot_lod'


class A3OBE_OT_RemoveNamedProperty_Resolution(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_resolution'
    _prop_path = 'a3obe_resolution_lods'

class A3OBE_OT_RemoveNamedProperty_Geometry(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_geometry'
    _prop_path = 'a3obe_geometry_lod'

class A3OBE_OT_RemoveNamedProperty_Memory(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_memory'
    _prop_path = 'a3obe_memory_lod'

class A3OBE_OT_RemoveNamedProperty_FireGeometry(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_fire_geometry'
    _prop_path = 'a3obe_fire_geometry_lod'

class A3OBE_OT_RemoveNamedProperty_ViewGeometry(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_view_geometry'
    _prop_path = 'a3obe_view_geometry_lod'

class A3OBE_OT_RemoveNamedProperty_ViewPilot(_RemoveNamedPropertyBase):
    bl_idname = 'a3obe.remove_named_property_view_pilot'
    _prop_path = 'a3obe_view_pilot_lod'


class A3OBE_OT_GenerateLODs(Operator):
    bl_idname = 'a3obe.generate_lods'
    bl_label = 'Generate LODs'
    bl_icon = 'PLAY'
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene

        if not context.active_object:
            self.report({'WARNING'}, 'Select an object first!')
            return {'CANCELLED'}

        if not hasattr(context.active_object, 'a3ob_properties_object'):
            self.report({'WARNING'}, 'Active object does not have A3OB properties. Ensure Arma 3 Object Builder addon is installed.')
            return {'CANCELLED'}

        if context.active_object.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')

        original_obj = context.active_object

        if scene.a3obe_geometry_lod.active:
            generators.generate_geometry_lod(context, original_obj)

        if scene.a3obe_memory_lod.active:
            generators.generate_memory_lod(context, original_obj)

        if scene.a3obe_fire_geometry_lod.active:
            generators.generate_fire_geometry_lod(context, original_obj)

        if scene.a3obe_view_geometry_lod.active:
            generators.generate_view_geometry_lod(context, original_obj)

        if scene.a3obe_view_pilot_lod.active:
            generators.generate_view_pilot_lod(context, original_obj)

        if scene.a3obe_resolution_lods.active:
            generators.generate_resolution_lods(context, original_obj)

        utils.organize_collections(context)

        return {'FINISHED'}


class A3OBE_OT_CheckForUpdates(Operator):
    bl_idname = 'a3obe.check_for_updates'
    bl_label = 'Check for Updates'
    bl_description = 'Check GitHub for a newer version of this addon'

    def execute(self, context):
        updater.check()
        if updater.status == 'AVAILABLE':
            self.report({'INFO'}, f"Update available: v{updater.latest_version_str}")
        elif updater.status == 'UP_TO_DATE':
            self.report({'INFO'}, "Addon is up to date")
        else:
            self.report({'WARNING'}, f"Update check failed: {updater.error_message}")
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}


class A3OBE_OT_InstallUpdate(Operator):
    bl_idname = 'a3obe.install_update'
    bl_label = 'Install Update'
    bl_description = 'Download and install the latest version from GitHub'

    def execute(self, context):
        success, result = updater.download_and_install()
        if not success:
            self.report({'ERROR'}, f"Download failed: {result}")
            return {'CANCELLED'}
        try:
            bpy.ops.preferences.addon_install(overwrite=True, filepath=result)
        except Exception as e:
            self.report({'ERROR'}, f"Install failed: {e}")
            return {'CANCELLED'}
        finally:
            try:
                os.unlink(result)
            except OSError:
                pass
        updater.status = 'UP_TO_DATE'
        self.report({'INFO'}, "Update installed — please restart Blender to apply it")
        for area in context.screen.areas:
            area.tag_redraw()
        return {'FINISHED'}
