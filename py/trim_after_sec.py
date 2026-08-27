import bpy

target_sec = {TARGET_SECONDS}
seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

fps = bpy.context.scene.render.fps # 25
part1_max_frames = int(target_sec * fps)

p1_movie = None
p1_sound = None
p2_movie = None
p2_sound = None

for s in seq_list:
    if not s.name.endswith("_part2"):
        if s.type == 'MOVIE': p1_movie = s
        elif s.type == 'SOUND': p1_sound = s
    else:
        if s.type == 'MOVIE': p2_movie = s
        elif s.type == 'SOUND': p2_sound = s

# Set Part 1 duration
if p1_movie:
    orig_off_start = p1_movie.frame_offset_start
    orig_dur = getattr(p1_movie, "frame_duration", 6210)
    p1_movie.frame_offset_end = orig_dur - orig_off_start - part1_max_frames
    p1_movie.channel = 2

if p1_sound:
    orig_off_start = p1_sound.frame_offset_start
    orig_dur = getattr(p1_sound, "frame_duration", 6210)
    p1_sound.frame_offset_end = orig_dur - orig_off_start - part1_max_frames
    p1_sound.channel = 1

# Snap Part 2 directly after Part 1
new_p2_start = part1_max_frames + 1

if p2_movie:
    p2_movie.frame_start = int(new_p2_start - p2_movie.frame_offset_start)
    p2_movie.channel = 2

if p2_sound:
    p2_sound.frame_start = int(new_p2_start - p2_sound.frame_offset_start)
    p2_sound.channel = 1

# ALWAYS FORCE-LOCK ALL MOVIE TO CHANNEL 2 AND ALL SOUND TO CHANNEL 1
for s in seq_list:
    if s.type == 'MOVIE':
        s.channel = 2
    elif s.type == 'SOUND':
        s.channel = 1

bpy.context.scene.frame_start = 1

if seq_list:
    max_f = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_offset_start", 0) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_end = max_f

print(f"TRIM_AFTER_SEC_SUCCESS: Set Part 1 duration to {target_sec}s and locked ALL video strips to Channel 2 & audio to Channel 1!")
