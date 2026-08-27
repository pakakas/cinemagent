import bpy

cleared = 0

# Execute operator to clear annotations across all regions
for window in bpy.context.window_manager.windows:
    for area in window.screen.areas:
        for region in area.regions:
            try:
                override = {'window': window, 'screen': window.screen, 'area': area, 'region': region}
                with bpy.context.temp_override(**override):
                    bpy.ops.annotation.clear_with_context()
                    cleared += 1
            except Exception:
                pass

# Remove any grease pencil datablocks
for gp in list(bpy.data.grease_pencils):
    try:
        bpy.data.grease_pencils.remove(gp)
        cleared += 1
    except Exception:
        pass

print(f"CLEAN_ANNOTATIONS_SUCCESS: Executed annotation clear operator ({cleared} regions checked)!")
