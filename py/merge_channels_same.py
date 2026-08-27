import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

for s in seq_list:
    if s.type == 'MOVIE':
        s.channel = 2
    elif s.type == 'SOUND':
        s.channel = 1

print("SAME_CHANNELS_SUCCESS: Placed all video strips on Channel 2 and all audio strips on Channel 1!")
