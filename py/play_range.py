import bpy

start_frame = {START_FRAME}
bpy.context.scene.frame_current = int(start_frame)

for window in bpy.context.window_manager.windows:
    screen = window.screen
    for area in screen.areas:
        if area.type in ('SEQUENCE_EDITOR', 'VIEW_3D', 'TIMELINE'):
            override = {'window': window, 'screen': screen, 'area': area}
            with bpy.context.temp_override(**override):
                bpy.ops.screen.animation_play()
            break

print(f"PLAY_RANGE_SUCCESS: Set frame to {start_frame} and started playback!")
