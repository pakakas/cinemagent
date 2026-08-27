import bpy

try:
    filepath = bpy.data.filepath
    bpy.ops.wm.save_mainfile(filepath=filepath)
    print(f"SAVE_SUCCESS: Saved active blend file to '{filepath}'!")
except Exception as e:
    print(f"SAVE_ERROR: {e}")
