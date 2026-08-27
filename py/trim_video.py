import bpy

start_seconds = {START_SECONDS}
seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

fps = bpy.context.scene.render.fps
cut_frames = int(start_seconds * fps)

trimmed_count = 0
for seq in seq_list:
    if hasattr(seq, "frame_offset_start") and hasattr(seq, "frame_start"):
        seq.frame_offset_start = cut_frames
        # Set frame_start so visible cut content starts at Frame 1.0
        seq.frame_start = 1.0 - cut_frames
        trimmed_count += 1

bpy.context.scene.frame_start = 1

if seq_list:
    max_f = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_offset_start", 0) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_end = max_f

print(f"TRIM_SUCCESS: Trimmed strips starting from {start_seconds}s and shifted visible content to Frame 1.0 (Second 0.0)!")
