import os, sys, bpy

addon_src = r"f:\work\00-oss\maintenis\.inbox\blender-mcp-vse\addon.py"

try:
    # 1. Install addon file into Blender
    bpy.ops.preferences.addon_install(overwrite=True, filepath=addon_src)
    print("ADDON_INSTALL_SUCCESS: Installed addon.py from repository!")
    
    # 2. Enable module
    try:
        bpy.ops.preferences.addon_enable(module="addon")
        print("ADDON_ENABLE_SUCCESS: Enabled 'addon' module!")
    except Exception as e:
        print(f"ADDON_ENABLE_WARN: {e}")

    # 3. Save User Preferences so it stays permanently installed
    bpy.ops.wm.save_userpref()
    print("SAVE_USERPREF_SUCCESS: Saved Blender User Preferences!")

    print("INSTALL_BLENDER_MCP_VSE_COMPLETED")
except Exception as e:
    print(f"INSTALL_BLENDER_MCP_VSE_ERROR: {e}")
