import bpy

scene = bpy.context.scene

seq_ed = getattr(scene, "sequence_editor", None)
if seq_ed:
    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
    for s in seq_coll:
        if getattr(s, "type", "") == "MOVIE":
            if hasattr(s, "transform"):
                s.transform.scale_x = 1.0
                s.transform.scale_y = 1.0
                s.transform.offset_x = 0.0
                s.transform.offset_y = 0.0

if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("RESET_SCALE_SUCCESS: Reset transform scale to 1.0 (100% full frame uncropped)!")
