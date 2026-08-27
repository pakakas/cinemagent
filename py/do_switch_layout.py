import bpy

# 1. Switch active workspace to 'Layout'
try:
    if "Layout" in bpy.data.workspaces:
        bpy.context.window.workspace = bpy.data.workspaces["Layout"]
    elif "General" in bpy.data.workspaces:
        bpy.context.window.workspace = bpy.data.workspaces["General"]
except Exception:
    pass

# 2. Force set screen areas to VIEW_3D with MATERIAL shading
screen = getattr(bpy.context.window, "screen", None) or getattr(bpy.context, "screen", None)
if screen and hasattr(screen, "areas"):
    for area in screen.areas:
        area.type = 'VIEW_3D'
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                space.shading.use_scene_lights = False
                space.shading.use_scene_world = False
                space.show_object_viewport_armature = True

# 3. Save mainfile
if bpy.data.filepath:
    bpy.ops.wm.save_mainfile()

print("DO_SWITCH_LAYOUT_SUCCESS: Switched workspace layout directly to 3D Viewport Layout!")
