import bpy

target_path = "{FILEPATH}"
try:
    bpy.data.filepath = target_path
    bpy.ops.wm.save_mainfile()
    print(f"SAVE_AS_SUCCESS: Saved project file to '{target_path}'!")
except Exception as e:
    print(f"SAVE_AS_ERROR: {e}")
