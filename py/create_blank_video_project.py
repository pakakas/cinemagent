import bpy

target_path = "D:/videos/blank-video.blend"

try:
    # 1. Clear all sequence editor strips
    seq_ed = getattr(bpy.context.scene, "sequence_editor", None)
    if seq_ed:
        seq_list = getattr(seq_ed, "sequences", None) or getattr(seq_ed, "strips", None) or []
        for s in list(seq_list):
            try:
                seq_list.remove(s)
            except Exception:
                pass
    else:
        bpy.context.scene.sequence_editor_create()

    # 2. Configure 9:16 vertical render resolution (1080x1920)
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1920
    bpy.context.scene.render.resolution_percentage = 100

    # 3. Save as D:/videos/blank-video.blend
    bpy.ops.wm.save_as_mainfile(filepath=target_path, check_existing=False)
    print(f"BLANK_VIDEO_PROJECT_SUCCESS: Created clean blank video project at '{target_path}'!")
except Exception as e:
    print(f"BLANK_VIDEO_PROJECT_ERROR: {e}")
