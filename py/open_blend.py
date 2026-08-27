import bpy

target_path = "{FILEPATH}"
try:
    bpy.ops.wm.open_mainfile(filepath=target_path, load_ui=True)
    print(f"OPEN_BLEND_SUCCESS: Opened {target_path}")
except Exception as e:
    print(f"OPEN_BLEND_ERROR: {e}")
