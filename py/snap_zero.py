import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

for s in seq_list:
    offset = getattr(s, "frame_offset_start", 0)
    # Set frame_start so the visible left handle (frame_final_start) lands on Frame 1.0
    s.frame_start = 1.0 - offset

bpy.context.scene.frame_start = 1

if seq_list:
    max_f = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_offset_start", 0) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_end = max_f

print("SNAP_ZERO_SUCCESS: Shifted strip handles so visible content starts exactly at Frame 1.0 (Second 0.0)!")
