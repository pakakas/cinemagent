import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

# Compact all channels cleanly starting from Channel 1 to 4:
# Channel 1: Audio Part 1
# Channel 2: Video Part 1
# Channel 3: Audio Part 2
# Channel 4: Video Part 2

for s in seq_list:
    if not s.name.endswith("_part2"):
        if s.type == 'SOUND':
            s.channel = 1
        elif s.type == 'MOVIE':
            s.channel = 2
    else:
        if s.type == 'SOUND':
            s.channel = 3
        elif s.type == 'MOVIE':
            s.channel = 4

print("COMPACT_CHANNELS_SUCCESS: Compacted timeline channels cleanly to 1, 2, 3, 4!")
