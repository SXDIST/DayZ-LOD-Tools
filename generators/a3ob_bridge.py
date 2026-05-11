import bpy


def run_a3ob_component_search(context, active_obj):
    try:
        if hasattr(bpy.ops, 'a3ob') and hasattr(bpy.ops.a3ob, 'find_components'):
            with context.temp_override(active_object=active_obj, selected_objects=[active_obj]):
                bpy.ops.a3ob.find_components()
        else:
            print('WARNING: A3OB addon not available, skipping component detection')
    except Exception as e:
        print(f'WARNING: A3OB find_components failed: {e}')
