import bpy

scene = bpy.context.scene

# 1. Set FPS to 30
scene.render.fps = 30
scene.render.fps_base = 1.0

# 2. Set 720p 9:16 Vertical Resolution (720x1280)
scene.render.resolution_x = 720
scene.render.resolution_y = 1280
scene.render.resolution_percentage = 100

# 3. Save file
bpy.ops.wm.save_mainfile()

print("SET_FPS_720P_SUCCESS: Set FPS to 30 and resolution to 720x1280 (9:16 720p Vertical)!")
