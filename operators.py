import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector

class A3OBE_OT_GenerateLODs(Operator):
    bl_idname = 'a3obe.generate_lods'
    bl_label = 'Generate LODs'
    bl_icon = 'PLAY'

    def execute(self, context):
        scene = context.scene
        resolution_lods = scene.a3obe_resolution_lods
        geometry_lod = scene.a3obe_geometry_lod

        if not context.active_object:
            self.report({'WARNING'}, 'Select an object first!')
            return {'CANCELLED'}

        if not hasattr(context.active_object, 'a3ob_properties_object'):
            self.report({'WARNING'}, 'Active object does not have A3OB properties. Please select an object with A3OB properties.')
            return {'CANCELLED'}

        if resolution_lods.active:
            self.generate_resolution_lods(context)

        if geometry_lod.active:
            self.generate_geometry_lod(context)

        return {'FINISHED'}

    def generate_resolution_lods(self, context):
        resolution_lods = context.scene.a3obe_resolution_lods
        obj = context.active_object
        start_lod = 0 if resolution_lods.first_lod == 'LOD0' else 1

        # Set up the original object as the first LOD
        obj.name = f'{resolution_lods.lod_prefix}{start_lod}'
        obj.data.name = obj.name
        obj.a3ob_properties_object.is_a3_lod = True
        obj.a3ob_properties_object.lod = '0'
        obj.a3ob_properties_object.resolution = start_lod
        for prop in resolution_lods.named_properties:
            self.add_named_property(obj, prop.name, prop.value)

        # Determine decimate values based on preset
        decimate_values = (resolution_lods.custom_decimate_values if resolution_lods.preset == 'CUSTOM'
                           else resolution_lods.tris_decimate_values if resolution_lods.preset == 'TRIS'
                           else resolution_lods.quads_decimate_values)

        # Create subsequent LODs
        for i, ratio in enumerate(decimate_values):
            lod_number = start_lod + i + 1
            dup_obj = self.duplicate(context, obj)
            dup_obj.name = f'{resolution_lods.lod_prefix}{lod_number}'
            dup_obj.data.name = dup_obj.name
            decimate = dup_obj.modifiers.new(name='Decimate', type='DECIMATE')
            decimate.ratio = ratio
            decimate.use_collapse_triangulate = True
            weighted_normal = dup_obj.modifiers.new(name='WeightedNormal', type='WEIGHTED_NORMAL')
            weighted_normal.use_face_influence = True
            weighted_normal.keep_sharp = True
            dup_obj.a3ob_properties_object.is_a3_lod = True
            dup_obj.a3ob_properties_object.resolution = lod_number
            for prop in resolution_lods.named_properties:
                self.add_named_property(dup_obj, prop.name, prop.value)

    def generate_geometry_lod(self, context):
        geometry_lod = context.scene.a3obe_geometry_lod
        obj = context.active_object

        if geometry_lod.geometry_type == 'BOX':
            geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, bpy.data.meshes.new(geometry_lod.lod_name))
            context.collection.objects.link(geometry_lod_obj)
            self.create_bounding_box(context, obj, geometry_lod_obj)
            self.set_geometry_lod_properties(geometry_lod_obj, geometry_lod)

        elif geometry_lod.geometry_type == 'MULTIPLE_BOXES':
            temp_obj = obj.copy()
            context.collection.objects.link(temp_obj)
            temp_obj.select_set(True)
            context.view_layer.objects.active = temp_obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.separate(type='LOOSE')
            bpy.ops.object.mode_set(mode='OBJECT')
            part_objs = [o for o in context.selected_objects if len(o.data.vertices) > 0 and o != temp_obj]

            for i, part in enumerate(part_objs):
                box_obj = self.create_bounding_box(context, part)
                box_obj.name = f'{geometry_lod.lod_name}_{i}'
                self.set_geometry_lod_properties(box_obj, geometry_lod)

            # Clean up temporary objects
            bpy.data.objects.remove(temp_obj, do_unlink=True)
            for part in part_objs:
                bpy.data.objects.remove(part, do_unlink=True)

        elif geometry_lod.geometry_type == 'NONE':
            mesh = bpy.data.meshes.new(geometry_lod.lod_name)
            geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, mesh)
            context.collection.objects.link(geometry_lod_obj)
            self.set_geometry_lod_properties(geometry_lod_obj, geometry_lod)

    def set_geometry_lod_properties(self, obj, geometry_lod):
        obj.a3ob_properties_object.is_a3_lod = True
        obj.a3ob_properties_object.lod = '6'
        for prop in geometry_lod.named_properties:
            self.add_named_property(obj, prop.name, prop.value)

    def duplicate(self, context, obj):
        copy = obj.copy()
        copy.data = obj.data.copy()
        context.collection.objects.link(copy)
        for child in obj.children:
            child_copy = child.copy()
            if child_copy.data:
                child_copy.data = child_copy.data.copy()
            context.collection.objects.link(child_copy)
            child_copy.parent = copy
        return copy

    def create_bounding_box(self, context, source_obj, target_obj=None):
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        coords = [source_obj.matrix_world @ v.co for v in bm.verts]
        bm.free()
        min_corner = Vector((min(v.x for v in coords), min(v.y for v in coords), min(v.z for v in coords)))
        max_corner = Vector((max(v.x for v in coords), max(v.y for v in coords), max(v.z for v in coords)))
        size = max_corner - min_corner
        center = (max_corner + min_corner) / 2
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=center)
        box_obj = context.active_object
        box_obj.scale = size
        if target_obj:
            target_obj.data = box_obj.data.copy()
            target_obj.location = box_obj.location
            target_obj.scale = size
            bpy.data.objects.remove(box_obj, do_unlink=True)
        else:
            return box_obj

    def add_named_property(self, obj, name, value):
        props = obj.a3ob_properties_object.properties
        if not any(p.name == name for p in props):
            item = props.add()
            item.name = name
            item.value = value

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