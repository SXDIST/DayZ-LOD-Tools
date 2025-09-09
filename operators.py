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
            self.generate_geometry_lod(context, original_obj)

        if memory_lod.active:
            self.generate_memory_lod(context, original_obj)

        if fire_geometry_lod.active:
            self.generate_fire_geometry_lod(context, original_obj)

        if view_geometry_lod.active:
            self.generate_view_geometry_lod(context, original_obj)

        if resolution_lods.active:
            self.generate_resolution_lods(context, original_obj)

        # Ensure correct collection order
        self.organize_collections(context)

        return {'FINISHED'}

    def generate_resolution_lods(self, context, obj):
        resolution_lods = context.scene.a3obe_resolution_lods
        
        if not obj or not obj.data:
            self.report({'WARNING'}, 'No valid object selected for Resolution LODs generation')
            return
            
        start_lod = 0 if resolution_lods.first_lod == 'LOD0' else 1

        # Create Visuals collection for resolution LODs
        visuals_collection = self.get_or_create_collection(context, "Visuals")
        
        # Move original object to Visuals collection
        if obj.users_collection:
            for collection in obj.users_collection:
                collection.objects.unlink(obj)
        visuals_collection.objects.link(obj)

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
            
            # Move duplicate to Visuals collection
            if dup_obj.users_collection:
                for collection in dup_obj.users_collection:
                    collection.objects.unlink(dup_obj)
            visuals_collection.objects.link(dup_obj)
            
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

    def generate_geometry_lod(self, context, obj):
        geometry_lod = context.scene.a3obe_geometry_lod
        
        if not obj or not obj.data:
            self.report({'WARNING'}, 'No valid object selected for Geometry LOD generation')
            return

        # Create Geometries collection for geometry LODs
        geometries_collection = self.get_or_create_collection(context, "Geometries")
        
        if geometry_lod.geometry_type == 'BOX':
            geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, bpy.data.meshes.new(geometry_lod.lod_name))
            geometries_collection.objects.link(geometry_lod_obj)
            self.create_bounding_box(context, obj, geometry_lod_obj)
            self.set_geometry_lod_properties(geometry_lod_obj, geometry_lod)
            
            # Find components using A3OB
            try:
                # Check if A3OB addon is available
                if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                    # Set the geometry object as active
                    context.view_layer.objects.active = geometry_lod_obj
                    geometry_lod_obj.select_set(True)
                    bpy.ops.a3ob.find_components()
                    self.report({'INFO'}, 'A3OB components found successfully')
                else:
                    self.report({'WARNING'}, 'A3OB addon not available, skipping component detection')
            except Exception as e:
                self.report({'WARNING'}, f'A3OB find_components failed: {str(e)}')

        elif geometry_lod.geometry_type == 'NONE':
            mesh = bpy.data.meshes.new(geometry_lod.lod_name)
            geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, mesh)
            geometries_collection.objects.link(geometry_lod_obj)
            self.set_geometry_lod_properties(geometry_lod_obj, geometry_lod)
            
            # Find components using A3OB
            try:
                # Check if A3OB addon is available
                if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                    # Set the geometry object as active
                    context.view_layer.objects.active = geometry_lod_obj
                    geometry_lod_obj.select_set(True)
                    bpy.ops.a3ob.find_components()
                    self.report({'INFO'}, 'A3OB components found successfully')
                else:
                    self.report({'WARNING'}, 'A3OB addon not available, skipping component detection')
            except Exception as e:
                self.report({'WARNING'}, f'A3OB find_components failed: {str(e)}')

    def set_geometry_lod_properties(self, obj, geometry_lod):
        obj.a3ob_properties_object.is_a3_lod = True
        obj.a3ob_properties_object.lod = '6'
        # Add LOD value property for DayZ
        self.add_named_property(obj, "lod", "1.000e+13")
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
        if not source_obj or not source_obj.data:
            return None
            
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        coords = [source_obj.matrix_world @ v.co for v in bm.verts]
        bm.free()
        
        if not coords:
            return None
            
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

    def get_or_create_collection(self, context, collection_name):
        """Get or create a collection with the given name"""
        if collection_name in bpy.data.collections:
            return bpy.data.collections[collection_name]
        else:
            new_collection = bpy.data.collections.new(collection_name)
            context.scene.collection.children.link(new_collection)
            return new_collection

    def get_or_create_subcollection(self, parent_collection, collection_name):
        """Get or create a subcollection within a parent collection"""
        # Check if subcollection already exists
        for child in parent_collection.children:
            if child.name == collection_name:
                return child
        
        # Create new subcollection
        new_collection = bpy.data.collections.new(collection_name)
        parent_collection.children.link(new_collection)
        return new_collection

    def organize_collections(self, context):
        """Organize collections in the correct order: Visuals, Geometries, Point Clouds"""
        scene = context.scene
        
        # Define the correct order
        collection_order = ["Visuals", "Geometries", "Point Clouds"]
        
        # Get all collections that exist
        existing_collections = []
        for collection_name in collection_order:
            if collection_name in bpy.data.collections:
                existing_collections.append(bpy.data.collections[collection_name])
        
        # Remove all collections from scene
        for collection in existing_collections:
            if collection.name in scene.collection.children:
                scene.collection.children.unlink(collection)
        
        # Add collections back in correct order
        for collection in existing_collections:
            scene.collection.children.link(collection)

    def generate_memory_lod(self, context, obj):
        """Generate Memory LOD with various memory points"""
        memory_lod = context.scene.a3obe_memory_lod
        
        if not obj or not obj.data:
            self.report({'WARNING'}, 'No valid object selected for Memory LOD generation')
            return
        
        # Create Point Clouds collection
        point_clouds_collection = self.get_or_create_collection(context, "Point Clouds")
        
        # Create memory object with points
        memory_obj = self.create_memory_points(context, obj, memory_lod)
        if not memory_obj:
            self.report({'WARNING'}, 'Failed to create memory points')
            return
            
        point_clouds_collection.objects.link(memory_obj)
        
        # Set memory properties according to DayZ standards
        memory_obj.a3ob_properties_object.is_a3_lod = True
        memory_obj.a3ob_properties_object.lod = '7'
        # Add LOD value property for DayZ
        self.add_named_property(memory_obj, "lod", "1.000e+15")
        
        # Add custom properties
        for prop in memory_lod.named_properties:
            self.add_named_property(memory_obj, prop.name, prop.value)

    def generate_fire_geometry_lod(self, context, obj):
        """Generate Fire Geometry LOD with subdivision and shrinkwrap"""
        fire_geometry_lod = context.scene.a3obe_fire_geometry_lod
        
        if not obj or not obj.data:
            self.report({'WARNING'}, 'No valid object selected for Fire Geometry LOD generation')
            return
        
        # Create Geometries collection
        geometries_collection = self.get_or_create_collection(context, "Geometries")
        
        # Create basic bounding box
        fire_obj = self.create_bounding_box(context, obj)
        if not fire_obj:
            self.report({'WARNING'}, 'Failed to create bounding box for Fire Geometry LOD')
            return
            
        fire_obj.name = "Fire Geometry"
        fire_obj.data.name = "Fire Geometry"
        
        # Move to Geometries collection
        if fire_obj.users_collection:
            for collection in fire_obj.users_collection:
                collection.objects.unlink(fire_obj)
        geometries_collection.objects.link(fire_obj)
        
        # Set fire geometry properties according to DayZ standards
        fire_obj.a3ob_properties_object.is_a3_lod = True
        fire_obj.a3ob_properties_object.lod = '7'
        # Add LOD value property for DayZ
        self.add_named_property(fire_obj, "lod", "7.000e+15")
        
        # Apply subdivision and shrinkwrap
        self.apply_fire_geometry_modifiers(fire_obj, obj, fire_geometry_lod.quality)
        
        # Add custom properties
        for prop in fire_geometry_lod.named_properties:
            self.add_named_property(fire_obj, prop.name, prop.value)
        
        # Find components using A3OB
        try:
            # Check if A3OB addon is available
            if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                # Set the fire geometry object as active
                context.view_layer.objects.active = fire_obj
                fire_obj.select_set(True)
                bpy.ops.a3ob.find_components()
                self.report({'INFO'}, 'A3OB components found successfully')
            else:
                self.report({'WARNING'}, 'A3OB addon not available, skipping component detection')
        except Exception as e:
            self.report({'WARNING'}, f'A3OB find_components failed: {str(e)}')

    def generate_view_geometry_lod(self, context, obj):
        """Generate View Geometry LOD"""
        view_geometry_lod = context.scene.a3obe_view_geometry_lod
        
        if not obj or not obj.data:
            self.report({'WARNING'}, 'No valid object selected for View Geometry LOD generation')
            return
        
        # Create Geometries collection
        geometries_collection = self.get_or_create_collection(context, "Geometries")
        
        # Create view geometry object
        view_obj = self.create_bounding_box(context, obj)
        if not view_obj:
            self.report({'WARNING'}, 'Failed to create bounding box for View Geometry LOD')
            return
            
        view_obj.name = view_geometry_lod.lod_name
        
        # Move to Geometries collection
        if view_obj.users_collection:
            for collection in view_obj.users_collection:
                collection.objects.unlink(view_obj)
        geometries_collection.objects.link(view_obj)
        
        # Set view geometry properties according to DayZ standards
        view_obj.a3ob_properties_object.is_a3_lod = True
        view_obj.a3ob_properties_object.lod = '6'
        # Add LOD value property for DayZ
        self.add_named_property(view_obj, "lod", "6.000e+15")
        
        # Add custom properties
        for prop in view_geometry_lod.named_properties:
            self.add_named_property(view_obj, prop.name, prop.value)
        
        # Find components using A3OB
        try:
            # Check if A3OB addon is available
            if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                # Set the view geometry object as active
                context.view_layer.objects.active = view_obj
                view_obj.select_set(True)
                bpy.ops.a3ob.find_components()
                self.report({'INFO'}, 'A3OB components found successfully')
            else:
                self.report({'WARNING'}, 'A3OB addon not available, skipping component detection')
        except Exception as e:
            self.report({'WARNING'}, f'A3OB find_components failed: {str(e)}')

    def create_memory_points(self, context, source_obj, memory_lod):
        """Create memory points as mesh with vertices and vertex groups"""
        # Create mesh for memory points
        mesh = bpy.data.meshes.new("Memory")
        memory_obj = bpy.data.objects.new("Memory", mesh)
        
        # Calculate bounding box corners
        bbox_min = source_obj.location + Vector((source_obj.bound_box[0]))
        bbox_max = source_obj.location + Vector((source_obj.bound_box[6]))
        center = source_obj.location
        
        # Create vertices for memory points
        vertices = []
        vertex_groups = []
        
        # Calculate invview point at 2.5 meters from object edge
        if memory_lod.invview_point:
            # Calculate object dimensions
            dimensions = source_obj.dimensions
            max_dimension = max(dimensions.x, dimensions.y, dimensions.z)
            # Place invview point 2.5 meters away from the furthest edge
            invview_distance = max_dimension / 2 + 2.5
            invview_point = center + Vector((0, invview_distance, 0))
            vertices.append(invview_point)
            vertex_groups.append("invview")
        
        if memory_lod.bounding_box_points:
            vertices.extend([bbox_min, bbox_max])
            vertex_groups.extend(["boundingbox_min", "boundingbox_max"])
        
        if memory_lod.radius_point:
            # Place ce_radius at the same location as boundingbox_max
            vertices.append(bbox_max)
            vertex_groups.append("ce_radius")
        
        if memory_lod.center_point:
            vertices.append(center)
            vertex_groups.append("ce_center")
        
        if not vertices:
            return None
        
        # Create mesh from vertices
        mesh.from_pydata(vertices, [], [])
        mesh.update()
        
        # Create vertex groups
        for group_name in set(vertex_groups):
            vg = memory_obj.vertex_groups.new(name=group_name)
            # Add vertices to appropriate groups
            for i, vg_name in enumerate(vertex_groups):
                if vg_name == group_name:
                    vg.add([i], 1.0, 'ADD')
        
        return memory_obj


    def apply_fire_geometry_modifiers(self, fire_obj, original_obj, quality):
        """Apply subdivision and shrinkwrap modifiers to fire geometry"""
        # Select and activate fire object
        fire_obj.select_set(True)
        bpy.context.view_layer.objects.active = fire_obj
        
        # Enter edit mode for subdivision
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Apply subdivisions
        bpy.ops.mesh.subdivide(number_cuts=quality)
        
        # Triangulate
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
        
        # Return to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add shrinkwrap modifier
        shrinkwrap = fire_obj.modifiers.new(name="Shrinkwrap", type='SHRINKWRAP')
        shrinkwrap.target = original_obj
        shrinkwrap.offset = 0.02
        shrinkwrap.wrap_mode = 'OUTSIDE_SURFACE'
        
        # Apply the modifier
        bpy.ops.object.modifier_apply(modifier="Shrinkwrap")

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