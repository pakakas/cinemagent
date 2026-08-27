import bpy

ref_filepath = "D:/videos/dl/bercanda guys.mp4"
char_filepath = "D:/videos/dl/guray.okewkey1786005072.mp4"

try:
    seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
    if not seq_ed:
        seq_ed = bpy.context.scene.sequence_editor_create()

    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None)
    
    # Clear existing strips
    for s in list(seq_coll):
        try:
            seq_coll.remove(s)
        except Exception:
            pass

    # 1. Channel 1: Reference Audio (from bercanda guys.mp4)
    ref_sound = seq_coll.new_sound(
        name="ref_motion_audio",
        filepath=ref_filepath,
        channel=1,
        frame_start=1
    )

    # 2. Channel 2: Reference Motion Video Guide (bercanda guys.mp4)
    ref_movie = seq_coll.new_movie(
        name="ref_motion_video",
        filepath=ref_filepath,
        channel=2,
        frame_start=1
    )
    ref_movie.blend_type = 'REPLACE'
    if hasattr(ref_movie, "blend_alpha"):
        ref_movie.blend_alpha = 0.45

    # 3. Channel 3: Target Character Overlay (Guray Rambut Oren)
    char_movie = seq_coll.new_movie(
        name="target_character_guray",
        filepath=char_filepath,
        channel=3,
        frame_start=1
    )
    char_movie.blend_type = 'ALPHA_OVER'
    if hasattr(char_movie, "blend_alpha"):
        char_movie.blend_alpha = 1.0

    # 4. Configure 720x1280 @ 30 FPS Canvas
    bpy.context.scene.render.resolution_x = 720
    bpy.context.scene.render.resolution_y = 1280
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.fps = 30
    bpy.context.scene.render.fps_base = 1.0

    # Reset transform scales to 1.0
    if hasattr(ref_movie, "transform"):
        ref_movie.transform.scale_x = 1.0
        ref_movie.transform.scale_y = 1.0
    if hasattr(char_movie, "transform"):
        char_movie.transform.scale_x = 1.0
        char_movie.transform.scale_y = 1.0

    # Update scene frame range
    bpy.context.scene.frame_start = 1
    max_f = max(
        int(getattr(ref_movie, "frame_start", 1) + getattr(ref_movie, "frame_final_duration", 0) - 1),
        int(getattr(char_movie, "frame_start", 1) + getattr(char_movie, "frame_final_duration", 0) - 1)
    )
    bpy.context.scene.frame_end = max_f

    # 5. Save mainfile to guray-dance.blend
    bpy.ops.wm.save_as_mainfile(filepath="D:/videos/guray-dance.blend", check_existing=False)

    print(f"COMPOSITING_SETUP_SUCCESS: Configured VSE Compositing Motion Swap pipeline with Alpha Over in guray-dance.blend!")
except Exception as e:
    print(f"COMPOSITING_SETUP_ERROR: {e}")
