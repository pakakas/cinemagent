import bpy

scene = bpy.context.scene
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

print("CANVAS_9_16_SUCCESS: Set render resolution to 1080x1920 (9:16 Vertical Aspect Ratio)!")
