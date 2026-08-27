import bpy

scene = bpy.context.scene

# 1. Stop animation playback if active
try:
    if getattr(bpy.context.screen, "is_animation_playing", False):
        bpy.ops.screen.animation_cancel()
except Exception:
    pass

# 2. Reset playhead current frame to 1
scene.frame_current = 1
scene.frame_set(1)

# 3. Save clean file state
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("RESET_PLAYER_SUCCESS: Stopped animation playback and reset playhead to Frame 1!")
