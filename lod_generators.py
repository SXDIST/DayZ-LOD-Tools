import bpy
import bmesh
from mathutils import Vector
from . import utils

def generate_resolution_lods(context, obj):
    resolution_lods = context.scene.a3obe_resolution_lods
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Resolution LODs generation')
        return
        
    start_lod = 0 if resolution_lods.first_lod == 'LOD0' else 1

    # Create Visuals collection for resolution LODs
    visuals_collection = utils.get_or_create_collection(context, "Visuals")
    
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
        utils.add_named_property(obj, prop.name, prop.value)

    # Determine decimate values based on preset
    decimate_values = (resolution_lods.custom_decimate_values if resolution_lods.preset == 'CUSTOM'
                       else resolution_lods.tris_decimate_values if resolution_lods.preset == 'TRIS'
                       else resolution_lods.quads_decimate_values)

    # Create subsequent LODs
    for i, ratio in enumerate(decimate_values):
        lod_number = start_lod + i + 1
        dup_obj = utils.duplicate_object(context, obj)
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
            utils.add_named_property(dup_obj, prop.name, prop.value)

def generate_geometry_lod(context, obj):
    geometry_lod = context.scene.a3obe_geometry_lod
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Geometry LOD generation')
        return

    # Create Geometries collection for geometry LODs
    geometries_collection = utils.get_or_create_collection(context, "Geometries")
    
import bpy
import bmesh
from mathutils import Vector
from . import utils

def generate_resolution_lods(context, obj):
    resolution_lods = context.scene.a3obe_resolution_lods
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Resolution LODs generation')
        return
        
    start_lod = 0 if resolution_lods.first_lod == 'LOD0' else 1

    # Create Visuals collection for resolution LODs
    visuals_collection = utils.get_or_create_collection(context, "Visuals")
    
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
        utils.add_named_property(obj, prop.name, prop.value)

    # Determine decimate values based on preset
    decimate_values = (resolution_lods.custom_decimate_values if resolution_lods.preset == 'CUSTOM'
                       else resolution_lods.tris_decimate_values if resolution_lods.preset == 'TRIS'
                       else resolution_lods.quads_decimate_values)

    # Create subsequent LODs
    for i, ratio in enumerate(decimate_values):
        lod_number = start_lod + i + 1
        dup_obj = utils.duplicate_object(context, obj)
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
            utils.add_named_property(dup_obj, prop.name, prop.value)

def generate_geometry_lod(context, obj):
    geometry_lod = context.scene.a3obe_geometry_lod
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Geometry LOD generation')
        return

    # Create Geometries collection for geometry LODs
    geometries_collection = utils.get_or_create_collection(context, "Geometries")
    
    if geometry_lod.geometry_type == 'BOX':
        geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, bpy.data.meshes.new(geometry_lod.lod_name))
        geometries_collection.objects.link(geometry_lod_obj)
        utils.create_bounding_box(context, obj, geometry_lod_obj)
        set_geometry_lod_properties(geometry_lod_obj, geometry_lod)
        
        # Find components using A3OB
        try:
            # Check if A3OB addon is available
            if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                # Use temp_override to ensure correct context
                with context.temp_override(active_object=geometry_lod_obj, selected_objects=[geometry_lod_obj]):
                    bpy.ops.a3ob.find_components()
                print('INFO: A3OB components found successfully')
            else:
                print('WARNING: A3OB addon not available, skipping component detection')
        except Exception as e:
            print(f'WARNING: A3OB find_components failed: {str(e)}')

    elif geometry_lod.geometry_type == 'NONE':
        mesh = bpy.data.meshes.new(geometry_lod.lod_name)
        geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, mesh)
        geometries_collection.objects.link(geometry_lod_obj)
        set_geometry_lod_properties(geometry_lod_obj, geometry_lod)
        
        # Find components using A3OB
        try:
            # Check if A3OB addon is available
            if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
                # Use temp_override to ensure correct context
                with context.temp_override(active_object=geometry_lod_obj, selected_objects=[geometry_lod_obj]):
                    bpy.ops.a3ob.find_components()
                print('INFO: A3OB components found successfully')
            else:
                print('WARNING: A3OB addon not available, skipping component detection')
        except Exception as e:
            print(f'WARNING: A3OB find_components failed: {str(e)}')

def set_geometry_lod_properties(obj, geometry_lod):
    obj.a3ob_properties_object.is_a3_lod = True
    obj.a3ob_properties_object.lod = '6'
    # Add LOD value property for DayZ
    utils.add_named_property(obj, "lod", "1.000e+13")
    for prop in geometry_lod.named_properties:
        utils.add_named_property(obj, prop.name, prop.value)

def generate_memory_lod(context, obj):
    """Generate Memory LOD with various memory points"""
    memory_lod = context.scene.a3obe_memory_lod
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Memory LOD generation')
        return
    
    # Create Point Clouds collection
    point_clouds_collection = utils.get_or_create_collection(context, "Point Clouds")
    
    # Create memory object with points
    memory_obj = create_memory_points(context, obj, memory_lod)
    if not memory_obj:
        print('WARNING: Failed to create memory points')
        return
        
    point_clouds_collection.objects.link(memory_obj)
    
    # Set memory properties according to DayZ standards
    memory_obj.a3ob_properties_object.is_a3_lod = True
    memory_obj.a3ob_properties_object.lod = '9'
    
    # Add custom properties
    for prop in memory_lod.named_properties:
        utils.add_named_property(memory_obj, prop.name, prop.value)

def create_memory_points(context, source_obj, memory_lod):
    """Create memory points as mesh with vertices and vertex groups"""
    # Create mesh for memory points
    mesh = bpy.data.meshes.new("Memory")
    memory_obj = bpy.data.objects.new("Memory", mesh)
    
    # Calculate bounding box corners in world space
    bbox_corners = [source_obj.matrix_world @ Vector(corner) for corner in source_obj.bound_box]
    bbox_min = bbox_corners[0] # This might not be min in world space if rotated, but it corresponds to the corner
    # Actually for boundingbox_min/max DayZ usually expects the axis aligned box of the geometry?
    # But if we want points, we usually want the corners of the OBB (Oriented Bounding Box) or AABB?
    # Let's stick to the corners of the bound box transformed.
    # Wait, bbox_min/max usually implies AABB.
    # But let's look at invview first.
    
    # Calculate local center for invview
    local_bbox_center = sum((Vector(v) for v in source_obj.bound_box), Vector((0,0,0))) / 8
    
    # Create vertices for memory points
    vertices = []
    vertex_groups = []
    
    # Calculate invview point at 2.5 meters from object edge
    if memory_lod.invview_point:
        # Calculate object dimensions
        dimensions = source_obj.dimensions
        max_dimension = max(dimensions.x, dimensions.y, dimensions.z)
        # Place invview point 2.5 meters away from the furthest edge along local Y axis
        invview_distance = max_dimension / 2 + 2.5
        # Transform local offset from local center to world space
        invview_local = local_bbox_center + Vector((0, invview_distance, 0))
        invview_point = source_obj.matrix_world @ invview_local
        vertices.append(invview_point)
        vertex_groups.append("invview")
    
    if memory_lod.bounding_box_points:
        # For bounding box points, we usually want the min/max of the AABB in world space?
        # Or the local min/max transformed?
        # Let's use the local min/max transformed to keep it simple and consistent with previous behavior,
        # but correctly using matrix_world on the specific corners 0 and 6.
        vertices.extend([source_obj.matrix_world @ Vector(source_obj.bound_box[0]), 
                         source_obj.matrix_world @ Vector(source_obj.bound_box[6])])
        vertex_groups.extend(["boundingbox_min", "boundingbox_max"])
    
    if memory_lod.radius_point:
        # Place ce_radius at the same location as boundingbox_max
        vertices.append(source_obj.matrix_world @ Vector(source_obj.bound_box[6]))
        vertex_groups.append("ce_radius")
    
    if memory_lod.center_point:
        # Use the geometric center
        vertices.append(source_obj.matrix_world @ local_bbox_center)
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

def generate_fire_geometry_lod(context, obj):
    """Generate Fire Geometry LOD with subdivision and shrinkwrap"""
    fire_geometry_lod = context.scene.a3obe_fire_geometry_lod
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for Fire Geometry LOD generation')
        return
    
    # Create Geometries collection
    geometries_collection = utils.get_or_create_collection(context, "Geometries")
    
    # Create Convex Hull instead of Bounding Box
    fire_obj = utils.duplicate_object(context, obj)
    fire_obj.name = "Fire Geometry"
    fire_obj.data.name = "Fire Geometry"
    
    # Remove children and modifiers from the copy
    for child in fire_obj.children:
        bpy.data.objects.remove(child, do_unlink=True)
    fire_obj.modifiers.clear()
    
    # Create Convex Hull
    context.view_layer.objects.active = fire_obj
    fire_obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.convex_hull()
    
    # Apply simplification based on quality
    # Quality 1 (Low) -> High angle (20 degrees)
    # Quality 10 (High) -> Low angle (0 degrees)
    import math
    angle_limit = (10 - fire_geometry_lod.quality) * math.radians(2.5)
    bpy.ops.mesh.dissolve_limited(angle_limit=angle_limit)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move to Geometries collection
    if fire_obj.users_collection:
        for collection in fire_obj.users_collection:
            collection.objects.unlink(fire_obj)
    geometries_collection.objects.link(fire_obj)
    
    # Set fire geometry properties according to DayZ standards
    fire_obj.a3ob_properties_object.is_a3_lod = True
    fire_obj.a3ob_properties_object.lod = '15'
    
    # Add custom properties
    for prop in fire_geometry_lod.named_properties:
        utils.add_named_property(fire_obj, prop.name, prop.value)
    
    # Find components using A3OB
    try:
        # Check if A3OB addon is available
        if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
            # Use temp_override
            with context.temp_override(active_object=fire_obj, selected_objects=[fire_obj]):
                bpy.ops.a3ob.find_components()
            print('INFO: A3OB components found successfully')
        else:
            print('WARNING: A3OB addon not available, skipping component detection')
    except Exception as e:
        print(f'WARNING: A3OB find_components failed: {str(e)}')

def apply_fire_geometry_modifiers(fire_obj, original_obj, quality):
    """Apply subdivision and shrinkwrap modifiers to fire geometry"""
    # Select and activate fire object
    fire_obj.select_set(True)
    bpy.context.view_layer.objects.active = fire_obj
    
    # Apply scale to ensure modifiers work correctly
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
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

def generate_view_geometry_lod(context, obj):
    """Generate View Geometry LOD"""
    view_geometry_lod = context.scene.a3obe_view_geometry_lod
    
    if not obj or not obj.data:
        print('WARNING: No valid object selected for View Geometry LOD generation')
        return
    
    # Create Geometries collection
    geometries_collection = utils.get_or_create_collection(context, "Geometries")
    
    # Create view geometry object
    view_obj = utils.create_bounding_box(context, obj)
    if not view_obj:
        print('WARNING: Failed to create bounding box for View Geometry LOD')
        return
        
    view_obj.name = view_geometry_lod.lod_name
    
    # Move to Geometries collection
    if view_obj.users_collection:
        for collection in view_obj.users_collection:
            collection.objects.unlink(view_obj)
    geometries_collection.objects.link(view_obj)
    
    # Set view geometry properties according to DayZ standards
    view_obj.a3ob_properties_object.is_a3_lod = True
    view_obj.a3ob_properties_object.lod = '14'
    
    # Add custom properties
    for prop in view_geometry_lod.named_properties:
        utils.add_named_property(view_obj, prop.name, prop.value)
    
    # Find components using A3OB
    try:
        # Check if A3OB addon is available
        if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
            # Use temp_override
            with context.temp_override(active_object=view_obj, selected_objects=[view_obj]):
                bpy.ops.a3ob.find_components()
            print('INFO: A3OB components found successfully')
        else:
            print('WARNING: A3OB addon not available, skipping component detection')
    except Exception as e:
        print(f'WARNING: A3OB find_components failed: {str(e)}')
