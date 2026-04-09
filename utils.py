import bpy
import bmesh
from mathutils import Vector

def create_bounding_box(context, source_obj, target_obj=None):
    if not source_obj or not source_obj.data:
        return None
        
    bm = bmesh.new()
    bm.from_mesh(source_obj.data)
    coords = [source_obj.matrix_world @ v.co for v in bm.verts]
    bm.free()
    
    if not coords:
        return None
        
    x_coords = [v.x for v in coords]
    y_coords = [v.y for v in coords]
    z_coords = [v.z for v in coords]
    min_corner = Vector((min(x_coords), min(y_coords), min(z_coords)))
    max_corner = Vector((max(x_coords), max(y_coords), max(z_coords)))
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

def get_or_create_collection(context, collection_name):
    """Get or create a collection with the given name"""
    if collection_name in bpy.data.collections:
        return bpy.data.collections[collection_name]
    else:
        new_collection = bpy.data.collections.new(collection_name)
        context.scene.collection.children.link(new_collection)
        return new_collection

def get_or_create_subcollection(parent_collection, collection_name):
    """Get or create a subcollection within a parent collection"""
    # Check if subcollection already exists
    for child in parent_collection.children:
        if child.name == collection_name:
            return child
    
    # Create new subcollection
    new_collection = bpy.data.collections.new(collection_name)
    parent_collection.children.link(new_collection)
    return new_collection

def organize_collections(context):
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

def duplicate_object(context, obj, target_collection=None):
    if target_collection is None:
        target_collection = context.collection
    copy = obj.copy()
    copy.data = obj.data.copy()
    target_collection.objects.link(copy)
    for child in obj.children:
        child_copy = child.copy()
        if child_copy.data:
            child_copy.data = child_copy.data.copy()
        target_collection.objects.link(child_copy)
        child_copy.parent = copy
    return copy

def add_named_property(obj, name, value):
    if not hasattr(obj, 'a3ob_properties_object'):
        return
        
    props = obj.a3ob_properties_object.properties
    if not any(p.name == name for p in props):
        item = props.add()
        item.name = name
        item.value = value
