import bpy

scene = bpy.context.scene

# Match source video resolution (576 x 1024) and 25 FPS
scene.render.resolution_x = 576
scene.render.resolution_y = 1024
scene.render.resolution_percentage = 100
scene.render.fps = 25
scene.render.fps_base = 1.0

# Reset movie strip scale to 1.0 (1:1 pixel match)
seq_ed = getattr(scene, "sequence_editor", None)
if seq_ed:
    seq_coll = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
    for s in seq_coll:
        if getattr(s, "type", "") == "MOVIE":
            if hasattr(s, "transform"):
                s.transform.scale_x = 1.0
                s.transform.scale_y = 1.0
                s.transform.offset_x = 0.0
                s.transform.offset_y = 0.0

if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("MATCH_SOURCE_SUCCESS: Matched canvas resolution (576x1024) and FPS (25) to source video!")
