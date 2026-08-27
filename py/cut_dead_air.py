import bpy

seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []

cut_start = 200 # Part 1 duration in frames (~8s)
cut_end = 675   # Dead air end frame (~27s)

movie_strip = None
sound_strip = None
for s in list(seq_list):
    if s.type == 'MOVIE' and not s.name.endswith("_part2"):
        movie_strip = s
    elif s.type == 'SOUND' and not s.name.endswith("_part2"):
        sound_strip = s

if movie_strip:
    orig_off_start = movie_strip.frame_offset_start
    orig_dur = getattr(movie_strip, "frame_duration", 6210)
    scale_x = getattr(movie_strip.transform, "scale_x", 1.0) if hasattr(movie_strip, "transform") else 1.0
    scale_y = getattr(movie_strip.transform, "scale_y", 1.0) if hasattr(movie_strip, "transform") else 1.0
    movie_path = movie_strip.filepath
    
    # 1. Trim Part 1
    movie_strip.frame_offset_end = orig_dur - orig_off_start - cut_start
    
    # 2. Create Part 2 strip for MOVIE
    p2_off_start = orig_off_start + cut_end
    p2_start_pos = 201
    
    p2_movie = seq_list.new_movie(
        name=movie_strip.name + "_part2",
        filepath=movie_path,
        channel=movie_strip.channel,
        frame_start=int(p2_start_pos - p2_off_start)
    )
    p2_movie.frame_offset_start = p2_off_start
    if hasattr(p2_movie, "transform"):
        p2_movie.transform.scale_x = scale_x
        p2_movie.transform.scale_y = scale_y

if sound_strip:
    orig_off_start = sound_strip.frame_offset_start
    orig_dur = getattr(sound_strip, "frame_duration", 6210)
    sound_path = getattr(sound_strip, "filepath", getattr(getattr(sound_strip, "sound", None), "filepath", ""))
    
    sound_strip.frame_offset_end = orig_dur - orig_off_start - cut_start
    
    p2_off_start = orig_off_start + cut_end
    p2_start_pos = 201
    
    if sound_path:
        p2_sound = seq_list.new_sound(
            name=sound_strip.name + "_part2",
            filepath=sound_path,
            channel=sound_strip.channel,
            frame_start=int(p2_start_pos - p2_off_start)
        )
        p2_sound.frame_offset_start = p2_off_start

if seq_list:
    max_f = max(int(getattr(s, "frame_start", 1) + getattr(s, "frame_offset_start", 0) + getattr(s, "frame_final_duration", 0) - 1) for s in seq_list)
    bpy.context.scene.frame_end = max_f

print("CUT_DEAD_AIR_SUCCESS: Cut 19s dead air (Bapa inside barn) and seamlessly spliced Part 1 & Part 2!")
