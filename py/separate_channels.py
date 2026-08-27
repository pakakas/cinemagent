import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

for s in seq_list:
    if s.name.endswith("_part2"):
        if s.type == 'MOVIE':
            s.channel = 10
        elif s.type == 'SOUND':
            s.channel = 9

print("SEPARATE_CHANNELS_SUCCESS: Restored Part 2 strips onto separate tracks (Channel 10 Video, Channel 9 Audio)!")
