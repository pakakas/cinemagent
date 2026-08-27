import bpy

try:
    bpy.ops.preferences.addon_enable(module="blender_mcp_vse")
    bpy.ops.wm.save_userpref()
    print("ADDON_ENABLE_SUCCESS: Enabled blender_mcp_vse module in Blender Preferences!")
except Exception as e:
    print(f"ADDON_ENABLE_ERROR: {e}")
