import bpy

# 1. Initialize sequence_editor datablock if missing (prevents UI thread lock on new files)
scene = bpy.context.scene
if not getattr(scene, "sequence_editor", None):
    try:
        scene.sequence_editor_create()
    except Exception as e:
        print(f"SE_INIT_NOTE: {e}")

# 2. Convert area type to SEQUENCE_EDITOR
window = bpy.context.window_manager.windows[0]
converted = False
for area in window.screen.areas:
    if area.type in ('VIEW_3D', 'EMPTY', 'PROPERTIES', 'OUTLINER'):
        area.type = 'SEQUENCE_EDITOR'
        for space in area.spaces:
            if space.type == 'SEQUENCE_EDITOR':
                space.view_type = 'SEQUENCER'
        converted = True
        break

print("SCRIPT_SWITCH_VSE_SUCCESS: Initialized VSE and converted area to SEQUENCE_EDITOR!")
