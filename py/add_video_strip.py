import bpy, os

filepath = "{FILEPATH}"
strip_name_raw = "{STRIP_NAME}"
res_x_str = "{RES_X}"
res_y_str = "{RES_Y}"
fps_str = "{FPS}"

res_x = int(res_x_str) if res_x_str.isdigit() else 720
res_y = int(res_y_str) if res_y_str.isdigit() else 1280
fps_val = int(fps_str) if fps_str.isdigit() else 30

if not strip_name_raw or strip_name_raw.startswith("{"):
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    strip_name_raw = base_name.replace(" ", "_").replace("-", "_")

try:
    seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
    if not seq_ed:
        seq_ed = bpy.context.scene.sequence_editor_create()

    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None)
    
    # 1. Add movie & sound strips dynamically
    movie_strip = seq_coll.new_movie(
        name=strip_name_raw + "_movie",
        filepath=filepath,
        channel=2,
        frame_start=1
    )
    
    sound_strip = seq_coll.new_sound(
        name=strip_name_raw + "_sound",
        filepath=filepath,
        channel=1,
        frame_start=1
    )

    # 2. Configure canvas resolution & FPS dynamically
    bpy.context.scene.render.resolution_x = res_x
    bpy.context.scene.render.resolution_y = res_y
    bpy.context.scene.render.resolution_percentage = 100
    bpy.context.scene.render.fps = fps_val
    bpy.context.scene.render.fps_base = 1.0

    # Auto-fit scale if landscape video in vertical canvas
    if res_y > res_x:
        base_vse_h = res_x * (9.0 / 16.0)
        scale_factor = res_y / base_vse_h
        if hasattr(movie_strip, "transform"):
            movie_strip.transform.scale_x = scale_factor
            movie_strip.transform.scale_y = scale_factor

    # 3. Update scene frame range
    bpy.context.scene.frame_start = 1
    max_f = int(getattr(movie_strip, "frame_start", 1) + getattr(movie_strip, "frame_final_duration", 0) - 1)
    bpy.context.scene.frame_end = max_f

    # 4. Save mainfile
    if bpy.data.filepath:
        bpy.ops.wm.save_mainfile()

    print(f"ADD_VIDEO_SUCCESS: Dynamically imported strip '{strip_name_raw}' from '{filepath}' at {res_x}x{res_y} @ {fps_val}FPS!")
except Exception as e:
    print(f"ADD_VIDEO_ERROR: {e}")
