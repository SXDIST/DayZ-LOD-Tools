import bpy
import bmesh
import math
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
        dup_obj = utils.duplicate_object(context, obj, visuals_collection)
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
            utils.add_named_property(dup_obj, prop.name, prop.value)


def run_a3ob_component_search(context, active_obj):
    try:
        if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
            with context.temp_override(active_object=active_obj, selected_objects=[active_obj]):
                bpy.ops.a3ob.find_components()
            print('INFO: A3OB components found successfully')
        else:
            print('WARNING: A3OB addon not available, skipping component detection')
    except Exception as e:
        print(f'WARNING: A3OB find_components failed: {str(e)}')

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
        
        run_a3ob_component_search(context, geometry_lod_obj)

    elif geometry_lod.geometry_type == 'NONE':
        mesh = bpy.data.meshes.new(geometry_lod.lod_name)
        geometry_lod_obj = bpy.data.objects.new(geometry_lod.lod_name, mesh)
        geometries_collection.objects.link(geometry_lod_obj)
        set_geometry_lod_properties(geometry_lod_obj, geometry_lod)
        
        run_a3ob_component_search(context, geometry_lod_obj)

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
    
    # Pre-calculate bounding component for reuse
    bbox_max_world = None
    if memory_lod.bounding_box_points or memory_lod.radius_point:
        bbox_max_world = source_obj.matrix_world @ Vector(source_obj.bound_box[6])
    
    if memory_lod.bounding_box_points:
        bbox_min_world = source_obj.matrix_world @ Vector(source_obj.bound_box[0])
        vertices.extend([bbox_min_world, bbox_max_world])
        vertex_groups.extend(["boundingbox_min", "boundingbox_max"])
    
    if memory_lod.radius_point:
        # Place ce_radius at the same location as boundingbox_max
        vertices.append(bbox_max_world)
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
    fire_obj = utils.duplicate_object(context, obj, geometries_collection)
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
    
    # Generate the hull. Blender selects the exterior vertices of the new hull.
    bpy.ops.mesh.convex_hull()
    
    # Invert selection to highlight internal vertices, then delete them
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='VERT')
    
    # Switch back to OBJECT mode for modifier application
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Calculate decimate ratio based on quality parameter
    # Quality 1 -> 0.1 ratio (10% polygons kept, very low poly)
    # Quality 10 -> 1.0 ratio (100% polygons kept, maximum detail)
    decimate_ratio = max(0.1, fire_geometry_lod.quality / 10.0)
    
    if decimate_ratio < 1.0:
        decimate = fire_obj.modifiers.new(name='Decimate_Quality', type='DECIMATE')
        decimate.ratio = decimate_ratio
        bpy.ops.object.modifier_apply(modifier='Decimate_Quality')
    
    # Add and apply Triangulate modifier to guarantee valid physics mesh (no N-gons)
    triangulate = fire_obj.modifiers.new(name='Triangulate', type='TRIANGULATE')
    triangulate.min_vertices = 4
    triangulate.keep_custom_normals = False
    triangulate.quad_method = 'BEAUTY'
    triangulate.ngon_method = 'BEAUTY'
    bpy.ops.object.modifier_apply(modifier="Triangulate")
    
    # Set fire geometry properties according to DayZ standards
    fire_obj.a3ob_properties_object.is_a3_lod = True
    fire_obj.a3ob_properties_object.lod = '15'
    
    # Add custom properties
    for prop in fire_geometry_lod.named_properties:
        utils.add_named_property(fire_obj, prop.name, prop.value)
    
    run_a3ob_component_search(context, fire_obj)


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
    
    run_a3ob_component_search(context, view_obj)
