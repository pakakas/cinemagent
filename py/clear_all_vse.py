import bpy

scene = bpy.context.scene

# 1. Clear all VSE strips (Movie, Sound, Effects, Transforms)
seq_ed = getattr(scene, "sequence_editor", None)
if seq_ed:
    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
    for s in list(seq_coll):
        try:
            seq_coll.remove(s)
        except Exception:
            pass

# 2. Reset timeline frame range
scene.frame_start = 1
scene.frame_end = 250
scene.frame_current = 1

# 3. Clear all Grease Pencil / Annotation layers
try:
    if hasattr(bpy.data, "grease_pencils"):
        for gp in list(bpy.data.grease_pencils):
            try:
                bpy.data.grease_pencils.remove(gp)
            except Exception:
                pass
except Exception:
    pass

# Redraw UI areas
for win in bpy.context.window_manager.windows:
    screen = win.screen
    if screen:
        for area in screen.areas:
            area.tag_redraw()

# 4. Save clean blend file
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("CLEAR_ALL_SUCCESS: Cleared all VSE strips, annotations, and reset timeline frame range!")
