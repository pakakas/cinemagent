import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

for seq in seq_list:
    if seq.type == 'MOVIE' and hasattr(seq, "transform"):
        t = seq.transform
        # Reset to 1.0 (Blender native VSE fit)
        t.scale_x = 1.0
        t.scale_y = 1.0
        t.offset_x = 0.0
        t.offset_y = 0.0

print("FIT_RESET_SUCCESS: Reset transform scale to 1.0!")
