import bpy
import bmesh

from ..core import utils
from ..constants import LOD_FIRE_GEOMETRY, COLLECTION_GEOMETRIES
from .a3ob_bridge import run_a3ob_component_search


def generate_fire_geometry_lod(context, obj):
    fire_geometry_lod = context.scene.a3obe_fire_geometry_lod

    if not obj or not obj.data:
        print('WARNING: No valid object selected for Fire Geometry LOD generation')
        return False

    geometries_collection = utils.get_or_create_collection(context, COLLECTION_GEOMETRIES)

    fire_obj = utils.duplicate_object(context, obj, geometries_collection)
    fire_obj.name = "Fire Geometry"
    fire_obj.data.name = "Fire Geometry"

    for child in list(fire_obj.children):
        bpy.data.objects.remove(child, do_unlink=True)
    fire_obj.modifiers.clear()

    # Build convex hull via bmesh API — no context/mode dependency
    _build_convex_hull(fire_obj)

    decimate_ratio = max(0.1, fire_geometry_lod.quality / 10.0)

    if decimate_ratio < 1.0:
        decimate = fire_obj.modifiers.new(name='Decimate_Quality', type='DECIMATE')
        decimate.ratio = decimate_ratio
        with context.temp_override(active_object=fire_obj, selected_objects=[fire_obj]):
            bpy.ops.object.modifier_apply(modifier='Decimate_Quality')

    triangulate = fire_obj.modifiers.new(name='Triangulate', type='TRIANGULATE')
    triangulate.min_vertices = 4
    triangulate.keep_custom_normals = False
    triangulate.quad_method = 'BEAUTY'
    triangulate.ngon_method = 'BEAUTY'
    with context.temp_override(active_object=fire_obj, selected_objects=[fire_obj]):
        bpy.ops.object.modifier_apply(modifier='Triangulate')

    fire_obj.a3ob_properties_object.is_a3_lod = True
    fire_obj.a3ob_properties_object.lod = LOD_FIRE_GEOMETRY

    for prop in fire_geometry_lod.named_properties:
        utils.add_named_property(fire_obj, prop.name, prop.value)

    run_a3ob_component_search(context, fire_obj)
    return True


def _build_convex_hull(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    result = bmesh.ops.convex_hull(bm, input=bm.verts)
    # Collect all non-hull verts (interior + unused); deleting verts also removes dependent geometry
    non_hull = result.get("geom_interior", []) + result.get("geom_unused", [])
    verts_to_delete = [g for g in non_hull if isinstance(g, bmesh.types.BMVert)]
    if verts_to_delete:
        bmesh.ops.delete(bm, geom=verts_to_delete, context='VERTS')
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
