import bpy

for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type in ('SEQUENCE_EDITOR', 'VIEW_3D', 'TIMELINE'):
            override = {'window': window, 'screen': screen, 'area': area}
            with bpy.context.temp_override(**override):
                bpy.ops.screen.animation_cancel()
            break

print("STOP_PLAYBACK_SUCCESS: Animation playback paused!")
