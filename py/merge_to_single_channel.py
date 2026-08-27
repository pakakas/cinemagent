import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

# Move all MOVIE strips onto Channel 8 and all SOUND strips onto Channel 7
for s in seq_list:
    if s.type == 'MOVIE':
        s.channel = 8
    elif s.type == 'SOUND':
        s.channel = 7

print("SINGLE_CHANNEL_SUCCESS: Moved all video strips to Channel 8 and audio strips to Channel 7!")
