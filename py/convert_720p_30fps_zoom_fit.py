import bpy

scene = bpy.context.scene

# 1. Set 720p 9:16 resolution (720 x 1280) and 30 FPS
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.render.fps_base = 1.0

# 2. Zoom fit scale: 1.25x (576x1024 -> 720x1280 border-to-border fit)
scale_factor = 720.0 / 576.0 # 1.25

seq_ed = getattr(scene, "sequence_editor", None)
if seq_ed:
    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
    for s in seq_coll:
        if getattr(s, "type", "") == "MOVIE":
            if hasattr(s, "transform"):
                s.transform.scale_x = scale_factor
                s.transform.scale_y = scale_factor
                s.transform.offset_x = 0.0
                s.transform.offset_y = 0.0

if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("CONVERT_720P_ZOOM_FIT_SUCCESS: Set resolution to 720x1280 @ 30 FPS with 1.25x zoom fit scale!")
